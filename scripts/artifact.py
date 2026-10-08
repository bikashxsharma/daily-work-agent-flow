#!/usr/bin/env python3.11
"""Separate, deterministic artifact persistence. Never call from a read-only phase."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
from workflow import git, repository


def reject_links(root, path):
    path.relative_to(root)
    cursor = root
    for part in path.relative_to(root).parts:
        cursor /= part
        if cursor.is_symlink():
            raise ValueError(f'Refusing symlink in artifact path: {cursor}')


def initialize(repo):
    root = repository(repo)
    directory = root / '.ai-workflow'
    reject_links(root, directory)
    if git(root, 'ls-files', '--', '.ai-workflow'):
        raise ValueError('.ai-workflow contains tracked files; choose a user-approved external location')
    if directory.exists() and not directory.is_dir():
        raise ValueError('.ai-workflow is not a directory')
    # --git-path handles linked worktrees, where .git is a file.
    exclude = Path(git(root, 'rev-parse', '--path-format=absolute', '--git-path', 'info/exclude'))
    if exclude.is_symlink():
        raise ValueError('Refusing symlinked Git exclusion file')
    probe = subprocess.run(['git', '-C', str(root), 'check-ignore', '-q', '--', '.ai-workflow/'])
    if probe.returncode not in (0, 1):
        raise ValueError('Cannot verify local Git exclusion')
    if probe.returncode == 1:
        exclude.parent.mkdir(parents=True, exist_ok=True)
        existing = exclude.read_text() if exclude.exists() else ''
        with exclude.open('a') as stream:
            stream.write(('\n' if existing and not existing.endswith('\n') else '') + '/.ai-workflow/\n')
    directory.mkdir(exist_ok=True)
    verified = subprocess.run(['git', '-C', str(root), 'check-ignore', '-q', '--', '.ai-workflow/'])
    if verified.returncode != 0:
        raise ValueError('Repository ignore rules override local exclusion; choose an external artifact location')
    return directory


def next_kind(root, feature, kind):
    base = root / '.ai-workflow/features' / feature
    if not (base / (kind + '.md')).exists():
        return kind
    number = 2
    while (base / f'{kind}-{number}.md').exists():
        number += 1
    return f'{kind}-{number}'


def save(repo, feature, kind, content, use_next=False):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', feature):
        raise ValueError('Feature must be a lowercase slug')
    if not re.fullmatch(r'(specification|plan|implementation|review|decisions)(?:-[1-9][0-9]*)?', kind):
        raise ValueError('Unsupported artifact name; original drafts are never overwritten')
    root = repository(repo)
    if use_next:
        if re.search(r'-[1-9][0-9]*$', kind):
            raise ValueError('--next requires an unnumbered artifact kind')
        kind = next_kind(root, feature, kind)
    target = root / '.ai-workflow/features' / feature / (kind + '.md')
    reject_links(root, target)
    if target.exists():
        raise ValueError(f'Artifact exists; use a new numbered version: {target}')
    initialize(root)
    if subprocess.run(['git', '-C', str(root), 'check-ignore', '-q', '--',
                       str(target.relative_to(root))]).returncode != 0:
        raise ValueError('Artifact is not excluded by Git; refusing to write it')
    target.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation refuses both ordinary collisions and symlink targets.
    with target.open('x') as stream:
        stream.write(content)
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['init', 'save'])
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--feature')
    parser.add_argument('--kind')
    parser.add_argument('--source', type=Path, help='Finalized Markdown; omitted means stdin')
    parser.add_argument('--next', action='store_true', help='Choose the next available numbered filename')
    args = parser.parse_args()
    try:
        if args.operation == 'init':
            print(initialize(args.repo))
        else:
            if not args.feature or not args.kind:
                parser.error('save requires --feature and --kind')
            content = args.source.read_text() if args.source else sys.stdin.read()
            if not content.strip():
                parser.error('Artifact content is empty')
            print(save(args.repo, args.feature, args.kind, content, args.next))
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, str(exc) + '\n')
