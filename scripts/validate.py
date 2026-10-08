#!/usr/bin/env python3.11
"""Validate central sources and installed links; --live queries Codex without model turns."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib
from codex_rpc import Client
from install import ROOT, links

NAMES = {'feature-discovery', 'feature-plan', 'feature-implement',
         'quick-fix', 'feature-review', 'feature-delivery'}


def validate(live=False):
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
        print(('PASS ' if condition else 'FAIL ') + message)

    check({p.name for p in (ROOT / 'skills').iterdir() if p.is_dir()} == NAMES, 'six skills exist')
    for name in sorted(NAMES):
        path = ROOT / 'skills' / name / 'SKILL.md'
        text = path.read_text()
        match = re.match(r'^---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n', text)
        check(bool(match and match.group(1) == name), f'{name}: valid simple YAML frontmatter')
    for path in ROOT.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if not target.startswith(('https:', 'http:', '#', '/')):
                check((path.parent / target.split('#')[0]).exists(), f'reference {path.relative_to(ROOT)} -> {target}')
    profiles = {}
    for path in (ROOT / 'profiles').glob('*.toml'):
        profiles[path.name.removesuffix('.config.toml')] = tomllib.loads(path.read_text())
    for path in (ROOT / 'agents').glob('*.toml'):
        data = tomllib.loads(path.read_text())
        check(all(data.get(k) for k in ('name', 'description', 'developer_instructions',
                                       'model', 'model_reasoning_effort', 'sandbox_mode')), f'agent {path.name}')
    home = Path.home()
    codex_home = Path(os.environ.get('CODEX_HOME', str(home / '.codex')))
    for source, target in links(home, codex_home):
        check(target.is_symlink() and target.resolve() == source, f'installed link {target}')
    if live:
        with Client(['--strict-config'], ROOT) as client:
            models = client.call('model/list', {'limit': 100})['data']
            catalog = {m['model']: {e['reasoningEffort'] for e in m['supportedReasoningEfforts']} for m in models}
            skills = client.call('skills/list', {'cwds': [str(ROOT)], 'forceReload': True})['data'][0]
            found = {s['name'] for s in skills['skills'] if s['enabled']}
            check(NAMES <= found, 'Codex discovers all six enabled user skills')
            check(not skills.get('errors'), 'Codex skill parser reports no errors')
        for name, profile in profiles.items():
            check(profile['model_reasoning_effort'] in catalog.get(profile['model'], set()),
                  f'{name}: model and reasoning in signed-in catalog')
            # app-server intentionally rejects --profile in 0.160.1. Verify native
            # profile loading through the supported prompt renderer (no inference).
            rendered = subprocess.run(['codex', '--profile', name,
                                       'debug', 'prompt-input', 'Workflow configuration check only.'],
                                      cwd=ROOT, capture_output=True, text=True, timeout=45)
            check(rendered.returncode == 0, f'{name}: native profile loads')
            if rendered.returncode:
                print(rendered.stderr[-1500:])
            overrides = []
            for key in ('model', 'model_reasoning_effort', 'sandbox_mode', 'approval_policy'):
                overrides += ['-c', key + '=' + json.dumps(profile[key])]
            with Client(['--strict-config', *overrides], ROOT) as client:
                effective = client.call('config/read', {'cwd': str(ROOT), 'includeLayers': False})['config']
                for key in ('model', 'model_reasoning_effort', 'sandbox_mode', 'approval_policy'):
                    check(effective.get(key) == profile[key], f'{name}: supported {key} value')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    try:
        failures = validate(args.live)
    except Exception as exc:
        sys.exit(f'Validation failed: {exc}')
    sys.exit(1 if failures else 0)
