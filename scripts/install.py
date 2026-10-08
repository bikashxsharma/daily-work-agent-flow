#!/usr/bin/env python3.11
"""Install only owned symlinks. No edits to existing config, instructions, or repositories."""
import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def links(home, codex_home):
    return ([(p, home / '.agents/skills' / p.name) for p in sorted((ROOT / 'skills').iterdir()) if p.is_dir()]
            + [(p, codex_home / 'agents' / p.name) for p in sorted((ROOT / 'agents').glob('*.toml'))]
            + [(p, codex_home / p.name) for p in sorted((ROOT / 'profiles').glob('*.config.toml'))])


def install(pairs, apply=False, uninstall=False):
    # Preflight every destination before the first mutation.
    for source, target in pairs:
        if target.is_symlink() and target.resolve() == source.resolve():
            continue
        if target.exists() or target.is_symlink():
            raise ValueError(f'Conflict; preserved existing destination: {target}')
    for source, target in pairs:
        owned = target.is_symlink() and target.resolve() == source.resolve()
        action = 'remove' if uninstall and owned else 'keep' if owned else 'skip' if uninstall else 'link'
        print(f'{action}: {target} -> {source}')
        if apply and action == 'link':
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(source, target_is_directory=source.is_dir())
        elif apply and action == 'remove':
            target.unlink()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Otherwise only display the changes')
    parser.add_argument('--uninstall', action='store_true', help='Remove only exact links owned by this setup')
    parser.add_argument('--home', type=Path, default=Path.home(), help='For isolated installation tests')
    parser.add_argument('--codex-home', type=Path)
    args = parser.parse_args()
    codex_home = args.codex_home or Path(os.environ.get('CODEX_HOME', str(args.home / '.codex')))
    try:
        install(links(args.home.resolve(), codex_home.resolve()), args.apply, args.uninstall)
    except ValueError as exc:
        parser.exit(1, str(exc) + '\n')
