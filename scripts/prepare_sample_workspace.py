#!/usr/bin/env python3
"""Copy a verified sample to a new directory outside the KIT; never execute its work.

Regular non-symlink .DS_Store files are copied but excluded from SHA snapshots.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import shutil
import stat


def snapshot(root):
    root = Path(root).resolve()
    files, links = {}, {}

    def resolve_local(path, depth=0):
        # Bound each component before inspecting it; Path.resolve() could follow
        # a relative link outside W and only then reveal that it escaped.
        if depth > 40:
            raise ValueError('Nonportable or broken symlink (cycle or excessive chain): ' + str(path))
        current = root
        for part in path.relative_to(root).parts:
            if not current.is_dir():
                raise ValueError('Nonportable or broken symlink: ' + str(path))
            if part == '..':
                if current == root:
                    raise ValueError('Nonportable or broken symlink (outside workspace): ' + str(path))
                current = current.parent
                continue
            current = current / part
            try:
                mode = current.lstat().st_mode
            except OSError as exc:
                raise ValueError('Nonportable or broken symlink: ' + str(path)) from exc
            if stat.S_ISLNK(mode):
                target = Path(os.readlink(current))
                if target.is_absolute():
                    raise ValueError('Nonportable or broken symlink (absolute target): ' + str(current))
                current = resolve_local(current.parent / target, depth + 1)
        return current

    directories = [root]
    while directories:
        for f in sorted(directories.pop().iterdir()):
            rel = str(f.relative_to(root))
            mode = f.lstat().st_mode
            if stat.S_ISLNK(mode):
                resolve_local(f)
                links[rel] = os.readlink(f)
            elif stat.S_ISDIR(mode):
                directories.append(f)
            elif stat.S_ISREG(mode) and f.name != '.DS_Store' and rel != 'bundle-manifest.json':
                files[rel] = hashlib.sha256(f.read_bytes()).hexdigest()
    return {'files': dict(sorted(files.items())), 'symlinks': dict(sorted(links.items()))}


def prepare(case, destination, kit=None):
    kit = Path(kit or Path(__file__).resolve().parents[1]).resolve()
    if case not in ('sales', 'minutes', 'reconciliation'):
        raise ValueError('Unknown sample')
    source = kit / 'sample' / case
    lexical = Path(destination).expanduser().absolute()
    try:
        target = lexical.resolve()
    except RuntimeError as exc:
        raise ValueError('Cannot resolve destination (symlink loop): ' + str(lexical)) from exc
    if target == kit or kit in target.parents or target in kit.parents:
        raise ValueError('Destination and KIT must not contain each other')
    if lexical.exists() or lexical.is_symlink():
        raise ValueError('Destination already exists; choose a new directory')
    # Audit links before reading the manifest, which may itself be a symlink.
    source_snapshot = snapshot(source)
    manifest = json.loads((source / 'bundle-manifest.json').read_text())
    expected = {'files': manifest['files'], 'symlinks': manifest['symlinks']}
    if source_snapshot != expected:
        raise ValueError('Bundle hash/entry mismatch')
    spec = importlib.util.spec_from_file_location('employee_layout', kit / 'scripts/verify_employee_workspace.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    structure = module.check_workspace(source)
    if not structure['static_checks_passed']:
        raise ValueError('Source layout invalid: ' + repr(structure['errors']))
    shutil.copytree(source, target, symlinks=True)
    if snapshot(target) != expected:
        raise ValueError('Copied content mismatch; preserved destination for inspection')
    result = module.check_workspace(target, kit)
    receipt = {
        'prepared_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'case': case, 'source': str(source), 'destination': str(target),
        'bundle_manifest_sha256': hashlib.sha256((source / 'bundle-manifest.json').read_bytes()).hexdigest(),
        'copy_content_matches': True,
        'snapshot_exclusions': ['bundle-manifest.json', 'regular non-symlink .DS_Store files at any depth'],
        'housekeeping_behavior': 'Regular non-symlink .DS_Store files are copied but not hashed; symlinks are always checked.',
        'source_static_checks_passed': True,
        'source_separation_note': 'Storage bundle intentionally inside KIT; only external destination is a runnable workspace.',
        'structure': result, 'recognition_verified': False, 'business_verified': False, 'human_acceptance': False,
        'note': 'Generation records are historical. Start a NEW conversation with this destination as cwd; supply a new work request and its required parameters.',
    }
    (target / 'workspace-copy-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    if not result['all_passed']:
        raise ValueError('Destination layout invalid; preserved destination and receipt for inspection')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=['sales', 'minutes', 'reconciliation'])
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args.case, args.destination), ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, RuntimeError) as exc:
        parser.exit(1, str(exc) + '\n')
