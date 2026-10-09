#!/usr/bin/env python3.11
"""Launch native Codex with explicit repository and phase permissions. Python 3.11+."""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import tomllib
from codex_rpc import Client

ROOT = Path(__file__).resolve().parents[1]
ROLES = {
    'discovery': ('feature-discovery', 'dw-discovery'),
    'plan': ('feature-plan', 'dw-analysis'),
    'implement': ('feature-implement', 'dw-code'),
    'quick-fix': ('quick-fix', 'dw-quick'),
    'review': ('feature-review', 'dw-review'),
    'delivery': ('feature-delivery', 'dw-delivery'),
}


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()


def repository(path):
    return Path(git(path, 'rev-parse', '--show-toplevel')).resolve()


def context(repo):
    root = repository(repo)
    index = root / 'documents/documents-knowledge-base.md'
    routing = root / '.ai-workflow/repository-context.md'
    candidates = ['docs/README.md', 'docs/index.md', 'docs/architecture.md', 'README.md']
    return {'cwd': str(Path(repo).resolve()), 'root': str(root),
            'status': git(root, 'status', '--short'),
            'routing_file': str(routing) if routing.is_file() else None,
            'knowledge_base': str(index) if index.is_file() else None,
            'documentation_candidates': [x for x in candidates if (root / x).is_file()]}


def build_command(args, effective=None):
    skill, profile_name = ROLES[args.phase]
    repo = repository(args.repo)
    if args.auto_implement and args.phase not in ('plan', 'delivery'):
        raise ValueError('--auto-implement is only valid for plan or delivery')
    if args.write_plan and args.phase not in ('plan', 'delivery'):
        raise ValueError('--write-plan is only valid for plan or delivery')
    if (args.auto_implement or args.write_plan) and args.exec:
        raise ValueError('--auto-implement/--write-plan belong on the coordinator, not an --exec phase worker')
    # Planning is read-only by default. A coordinator is writable only when
    # implementation or the explicitly requested Markdown artifact requires it.
    readonly = (args.phase in ('discovery', 'review') or
                (args.phase == 'plan' and not args.auto_implement and not args.write_plan))
    if args.auto_implement and args.phase == 'plan':
        profile_name = 'dw-delivery'
    profile = tomllib.loads((ROOT / 'profiles' / (profile_name + '.config.toml')).read_text())
    options = ['--strict-config', '--profile', profile_name,
               '--model', profile['model'],
               '-c', 'model_reasoning_effort=' + json.dumps(profile['model_reasoning_effort']),
               '--sandbox', 'read-only' if readonly else 'workspace-write',
               '-c', 'approval_policy=' + json.dumps('never' if readonly else 'on-request'),
               '-c', 'sandbox_workspace_write.writable_roots=[]',
               '-c', 'sandbox_workspace_write.network_access=false',
               '-c', 'web_search="disabled"',
               '-c', 'features.hooks=false', '-c', 'features.plugins=false',
               '-c', 'features.remote_plugin=false', '-c', 'features.apps=false',
               '-c', 'features.enable_mcp_apps=false']
    if readonly:
        options += ['-c', 'agents.enabled=false']
    allowed_mcp = set(args.allow_mcp)
    if effective is not None:
        # The OS sandbox does not constrain remote MCP effects. Disable every server
        # except services explicitly opted into this invocation by launcher flag.
        configured = set(effective.get('mcp_servers', {}))
        missing = allowed_mcp - configured
        if missing:
            raise ValueError('Requested MCP server is not configured: ' + ', '.join(sorted(missing)))
        for name in sorted(configured):
            enabled = 'true' if name in allowed_mcp else 'false'
            options += ['-c', 'mcp_servers.' + json.dumps(name) + '.enabled=' + enabled]
    flags = []
    if args.auto_implement:
        flags.append('--auto-implement')
    if args.write_plan:
        flags.append('--write-plan')
    if args.verbose:
        flags.append('--verbose')
    prompt = '$' + skill + ((' ' + ' '.join(flags)) if flags else '') + ' ' + args.task
    prompt += ('\n\nWorkflow launcher: active repository is ' + str(repo) +
               '. Read the selected skill at ' + str(ROOT / 'skills' / skill / 'SKILL.md') + '.')
    if readonly:
        prompt += (' This is the isolated read-only phase worker; perform this phase here, '
                   'do not launch another worker. Return the report in your final response. '
                   'No artifact writes, implementation, remediation, or model spawning.')
    else:
        prompt += (' You are the workspace-write coordinator. Use scripts/workflow.py from '
                   + str(ROOT) + ' with --exec for separate read-only analysis/review workers. '
                   'Display their complete specification/plan before applying approval gates.')
        if args.phase == 'plan' and args.write_plan:
            prompt += (' After the read-only planner returns, save the exact complete plan in this '
                       'repository with scripts/artifact.py save --feature <slug> --kind plan '
                       '--next, report its '
                       'repository-relative path, and do not modify application code before the '
                       'applicable approval gate.')
        elif args.phase == 'plan':
            prompt += (' Do not create or modify a plan artifact because --write-plan was not '
                       'provided. Planning itself remains delegated to the read-only worker.')
    if args.verbose:
        prompt += (' Verbose reporting is enabled for this invocation: provide the skill-specific '
                   'evidence summaries and no hidden reasoning or complete tool logs. This session '
                   'was launched with model ' + profile['model'] + ' and reasoning effort ' +
                   profile['model_reasoning_effort'] + '; report that launcher-selected usage. '
                   'Forward --verbose to phase workers.')
    if allowed_mcp:
        prompt += (' The user explicitly opted into these MCP servers for this invocation only: '
                   + ', '.join(sorted(allowed_mcp)) + '. Use only those named services and only '
                   'for the separately requested operation. Forward the matching --allow-mcp '
                   'arguments only to phase workers that need that operation.')
    else:
        prompt += ' MCP servers and external connectors are disabled for this invocation.'
    if args.exec:
        return ['codex', 'exec', *options, '--cd', str(repo), '--ephemeral', prompt]
    return ['codex', *options, '--cd', str(repo), prompt]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=[*ROLES, 'context'])
    parser.add_argument('task', nargs='?', default='')
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--auto-implement', action='store_true')
    parser.add_argument('--write-plan', action='store_true',
                        help='Persist only the proposed Markdown plan in the active repository')
    parser.add_argument('--verbose', action='store_true', help='Expand evidence summaries only')
    parser.add_argument('--allow-mcp', action='append', default=[], metavar='NAME',
                        help='Explicitly enable one configured MCP server for this invocation')
    parser.add_argument('--exec', action='store_true', help='Fresh noninteractive phase; no chat history')
    parser.add_argument('--dry-run', action='store_true', help='Print command without launching Codex')
    args = parser.parse_intermixed_args()
    if args.phase == 'context':
        print(json.dumps(context(args.repo), indent=2))
        return
    if not args.task.strip():
        parser.error('Provide a task or repository-relative Markdown input path')
    effective = None
    if args.allow_mcp and not args.dry_run:
        # Configuration inspection does not run a turn, initialize connectors, or execute hooks.
        with Client(['--strict-config'], repository(args.repo)) as client:
            effective = client.call('config/read', {
                'cwd': str(repository(args.repo)), 'includeLayers': False})['config']
    command = build_command(args, effective)
    if args.dry_run:
        print('Dry run: default launches use an isolated Codex home without MCP configuration.')
        print(shlex.join(command))
    else:
        if args.allow_mcp:
            os.execvp(command[0], command)
        # A malformed external MCP entry can prevent Codex from loading even when
        # disabled by a CLI override. Do not load the user's integration config.
        with tempfile.TemporaryDirectory(prefix='daily-work-codex-') as directory:
            home = Path(directory)
            original = Path(os.environ.get('CODEX_HOME', Path.home() / '.codex'))
            (home / 'config.toml').write_text('')
            for name in ('auth.json', 'skills'):
                source = original / name
                if source.exists():
                    (home / name).symlink_to(source, target_is_directory=source.is_dir())
            for profile in (ROOT / 'profiles').glob('*.config.toml'):
                (home / profile.name).symlink_to(profile)
            environment = os.environ.copy()
            environment['CODEX_HOME'] = str(home)
            raise SystemExit(subprocess.call(command, env=environment))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, subprocess.CalledProcessError, OSError) as exc:
        sys.exit(str(exc))
