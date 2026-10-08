#!/usr/bin/env python3.11
"""Read installed capabilities without running an inference or changing a repository."""
import argparse
import json
from pathlib import Path
from codex_rpc import Client

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=Path.cwd())
args = parser.parse_args()
options = ['--strict-config']
with Client(options, args.repo) as client:
    config = client.call('config/read', {'cwd': str(args.repo.resolve()), 'includeLayers': False})['config']
    print(json.dumps({'config': {k: config.get(k) for k in
        ('model', 'model_reasoning_effort', 'sandbox_mode', 'approval_policy', 'agents', 'features')},
        'mcp_server_names': list(config.get('mcp_servers', {}))}, indent=2))
    models = client.call('model/list', {'limit': 100})
    print(json.dumps({'models': models}, indent=2))
    skills = client.call('skills/list', {'cwds': [str(args.repo.resolve())], 'forceReload': True})
    print(json.dumps({'skills': skills}, indent=2))
