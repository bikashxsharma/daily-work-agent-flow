#!/usr/bin/env python3.11
"""Exercise Codex's native sandbox on disposable files, without model inference."""
from pathlib import Path
import subprocess
import tempfile
import uuid


with tempfile.TemporaryDirectory(prefix='daily-work-native-') as tmp:
    root = Path(tmp).resolve()
    repo = root / 'repository'
    outside = Path(__file__).resolve().parents[2] / ('.daily-work-probe-' + uuid.uuid4().hex)
    repo.mkdir()
    (repo / 'evidence.txt').write_text('readable')
    subprocess.run(['git', 'init', '-q', str(repo)], check=True)
    for profile in ('dw-analysis', 'dw-review', 'dw-code'):
        source = """
from pathlib import Path
import json,sys
repo, outside = map(Path, sys.argv[1:3])
results = {'read': (repo/'evidence.txt').read_text() == 'readable'}
for name, target in [('workspace_write', repo/'probe.txt'), ('outside_write', outside)]:
    try:
        with target.open('x') as stream:
            stream.write('probe')
        results[name] = True
        target.unlink()
    except PermissionError:
        results[name] = False
print(json.dumps(results))
expected = {'read': True, 'workspace_write': sys.argv[3] == 'write', 'outside_write': False}
sys.exit(0 if results == expected else 1)
"""
        result = subprocess.run(['codex', 'sandbox', '--profile', profile,
                                 '--permission-profile', ':workspace' if profile == 'dw-code' else ':read-only',
                                 '--cd', str(repo),
                                 '--', 'python3.11', '-c', source, str(repo), str(outside),
                                 'write' if profile == 'dw-code' else 'read'],
                                capture_output=True, text=True, timeout=30)
        print(profile, result.returncode, result.stdout.strip())
        if result.returncode:
            raise SystemExit(result.stderr or 'Sandbox boundary did not match expected permissions')
print('PASS native read-only and workspace-write boundaries')
