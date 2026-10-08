#!/usr/bin/env python3.11
"""Launch native Codex with explicit repository and phase permissions. Python 3.11+."""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
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
    # The coordinator can write; its analysis workers always run separately read-only.
    readonly = args.phase in ('discovery', 'review', 'plan') and not args.auto_implement
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
    if effective is not None:
        # The OS sandbox does not constrain remote MCP effects. Disable every server
        # from the effective user/profile/project configuration for these local workflows.
        for name in effective.get('mcp_servers', {}):
            options += ['-c', 'mcp_servers.' + json.dumps(name) + '.enabled=false']
    prompt = '$' + skill + (' --auto-implement' if args.auto_implement else '') + ' ' + args.task
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
    if args.exec:
        return ['codex', 'exec', *options, '--cd', str(repo), '--ephemeral', prompt]
    return ['codex', *options, '--cd', str(repo), prompt]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=[*ROLES, 'context'])
    parser.add_argument('task', nargs='?', default='')
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--auto-implement', action='store_true')
    parser.add_argument('--exec', action='store_true', help='Fresh noninteractive phase; no chat history')
    parser.add_argument('--dry-run', action='store_true', help='Print command; skip capability preflight')
    args = parser.parse_intermixed_args()
    if args.phase == 'context':
        print(json.dumps(context(args.repo), indent=2))
        return
    if not args.task.strip():
        parser.error('Provide a task or repository-relative Markdown input path')
    effective = None
    if not args.dry_run:
        # Configuration inspection does not run a turn, initialize connectors, or execute hooks.
        with Client(['--strict-config'], repository(args.repo)) as client:
            effective = client.call('config/read', {
                'cwd': str(repository(args.repo)), 'includeLayers': False})['config']
    command = build_command(args, effective)
    if args.dry_run:
        print('Dry run: MCP disabling is added after effective-config preflight.')
        print(shlex.join(command))
    else:
        os.execvp(command[0], command)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, subprocess.CalledProcessError, OSError) as exc:
        sys.exit(str(exc))
