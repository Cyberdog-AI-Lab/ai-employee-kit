#!/usr/bin/env python3
"""Synthetic copy-helper regressions; no discovery, business execution or network.

Python 3.10+ with PyYAML. Fixtures use OS temp by default, or --temp-root.
Checks use explicit exceptions, so python -O does not disable them.
"""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import traceback
from unittest.mock import patch

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
HELPER = BASE / 'prepare_sample_workspace.py'
VALIDATOR = BASE / 'verify_employee_workspace.py'
spec = importlib.util.spec_from_file_location('sample_copy', HELPER)
copy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(copy)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def manifest(src):
    write(src / 'bundle-manifest.json', json.dumps(copy.snapshot(src)))


def fixture(root):
    kit = root / 'kit'
    src = kit / 'sample/workspaces/sales'
    write(src / 'AGENTS.md', '# Employee\nKeep source inputs unchanged.\n')
    write(src / 'CLAUDE.md', '@AGENTS.md\n')
    write(src / '.claude/skills/work-001/SKILL.md',
          '---\nname: work-001\ndescription: Analyze fictional input.\n---\n# Procedure\nKeep originals.\n')
    (src / '.agents/skills').mkdir(parents=True)
    (src / '.agents/skills/work-001').symlink_to('../../.claude/skills/work-001', target_is_directory=True)
    write(src / 'inputs/data.csv', 'id,value\nA,3\n')
    (kit / 'scripts').mkdir()
    for path in (VALIDATOR, HELPER):
        shutil.copy2(path, kit / 'scripts' / path.name)
    manifest(src)
    return kit, src


def inventory(root):
    # Include housekeeping and manifest bytes when checking source preservation.
    result = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            p = Path(current) / name
            rel = str(p.relative_to(root))
            if p.is_symlink():
                result[rel] = ('symlink', os.readlink(p))
            elif p.is_file():
                result[rel] = ('file', hashlib.sha256(p.read_bytes()).hexdigest())
    return result


def reject(call, reason, destination=None):
    try:
        call()
    except (ValueError, OSError) as exc:
        require(reason in str(exc), 'expected reason ' + reason + '; observed: ' + str(exc))
        if destination is not None:
            require(not destination.exists() and not destination.is_symlink(), 'rejection created destination')
        return {'required_reason_fragment': reason, 'observed_reason': str(exc)}
    raise AssertionError('Expected rejection: ' + reason)


def success(kit, src, dst):
    receipt = copy.prepare('sales', dst, kit)
    require(receipt['copy_content_matches'] and receipt['structure']['all_passed'], 'copy/static check failed')
    link = dst / '.agents/skills/work-001'
    require(link.is_symlink() and os.readlink(link) == '../../.claude/skills/work-001', 'relative connection changed')
    require((dst / 'inputs/data.csv').read_bytes() == (src / 'inputs/data.csv').read_bytes(), 'input changed')
    for record in (receipt, receipt['structure']):
        require(all(record[k] is False for k in ('recognition_verified', 'business_verified', 'human_acceptance')),
                'copy receipt claims runtime verification')
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--temp-root', type=Path, help='fixture parent; default: OS temporary directory outside K')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.temp_root is None and Path(tempfile.gettempdir()).resolve().is_relative_to(BASE.parent):
        parser.error('default temporary directory must be outside K; set --temp-root explicitly')
    results = []
    with tempfile.TemporaryDirectory(prefix='employee-copy-tests-', dir=args.temp_root) as td:
        root = Path(td).resolve()
        fixture_parent = str(root.parent.resolve())

        def run(label, exercise, setup=lambda base, kit, src: None):
            base = root / label
            kit, src = fixture(base)
            result = {'case': label}
            try:
                setup(base, kit, src)
                before = inventory(src)
                result.update(exercise(base, kit, src) or {})
                require(inventory(src) == before, 'helper changed source inputs/configuration')
                result.update(passed=True, source_unchanged=True)
            except Exception:
                result.update(passed=False, failure=traceback.format_exc())
            results.append(result)

        run('copy_preserves_hidden_config_relative_link_and_inputs',
            lambda b, k, s: {'copy_content_matches': success(k, s, b / 'copied')['copy_content_matches']})

        def existing(b, k, s):
            dst = b / 'existing'
            write(dst / 'keep.txt', 'retain')
            result = reject(lambda: copy.prepare('sales', dst, k), 'already exists')
            require((dst / 'keep.txt').read_text() == 'retain', 'existing destination modified')
            return result
        run('existing_destination', existing)
        run('nested_in_kit', lambda b, k, s: reject(
            lambda: copy.prepare('sales', k / 'new', k), 'must not contain', k / 'new'))
        run('destination_is_kit', lambda b, k, s: reject(
            lambda: copy.prepare('sales', k, k), 'must not contain'))
        run('destination_ancestor_of_kit', lambda b, k, s: reject(
            lambda: copy.prepare('sales', b, k), 'must not contain'))

        def alias(b, k, s):
            parent = b / 'alias-parent'
            parent.symlink_to(k, target_is_directory=True)
            return reject(lambda: copy.prepare('sales', parent / 'new', k), 'must not contain', k / 'new')
        run('symlinked_parent_resolves_into_kit', alias)
        run('aliased_destination_is_kit', lambda b, k, s: reject(
            lambda: copy.prepare('sales', b / 'alias', k), 'must not contain'),
            lambda b, k, s: (b / 'alias').symlink_to(k))

        def dangling(b, k, s):
            link = b / 'destination-link'
            link.symlink_to(b / 'not-created')
            result = reject(lambda: copy.prepare('sales', link, k), 'already exists')
            require(link.is_symlink() and not (b / 'not-created').exists(), 'dangling destination replaced')
            return result
        run('dangling_destination_link', dangling)
        run('tampered_bundle', lambda b, k, s: reject(
            lambda: copy.prepare('sales', b / 'tampered', k), 'hash/entry mismatch', b / 'tampered'),
            lambda b, k, s: write(s / 'inputs/data.csv', 'changed'))

        def absolute_skill(b, k, s):
            link = s / '.agents/skills/work-001'
            link.unlink()
            link.symlink_to(s / '.claude/skills/work-001')
        run('absolute_skill_link', lambda b, k, s: reject(
            lambda: copy.prepare('sales', b / 'absolute', k), 'Nonportable', b / 'absolute'), absolute_skill)

        def housekeeping(b, k, s):
            paths = ['.DS_Store', 'inputs/.DS_Store', '.agents/skills/.DS_Store',
                     '.claude/skills/.DS_Store', '.claude/skills/work-001/.DS_Store']
            expected = json.loads((s / 'bundle-manifest.json').read_text())
            # Simulate Finder modifying an already manifested bundle.
            require(copy.snapshot(s) == expected, 'regular housekeeping affected manifest comparison')
            receipt = success(k, s, b / 'copied')
            for rel in paths:
                require((b / 'copied' / rel).read_bytes() == (s / rel).read_bytes(), 'housekeeping not copied: ' + rel)
            require('not hashed' in receipt['housekeeping_behavior'], 'exclusion not disclosed')
            return {'copied_housekeeping_files': paths, 'regular_housekeeping_excluded_from_snapshot': True}
        run('regular_DS_Store_after_manifest_is_copied_not_hashed', housekeeping,
            lambda b, k, s: [write(s / rel, 'Finder metadata ' + rel) for rel in
                ['.DS_Store', 'inputs/.DS_Store', '.agents/skills/.DS_Store',
                 '.claude/skills/.DS_Store', '.claude/skills/work-001/.DS_Store']])

        def portable_metadata_setup(b, k, s):
            (s / '.DS_Store').symlink_to('inputs/data.csv')
            manifest(s)
        def portable_metadata(b, k, s):
            require(copy.snapshot(s)['symlinks']['.DS_Store'] == 'inputs/data.csv', 'metadata symlink ignored')
            success(k, s, b / 'copied')
            require((b / 'copied/.DS_Store').is_symlink(), 'metadata symlink not copied')
            return {'metadata_symlink_checked_and_preserved': True}
        run('relative_DS_Store_symlink_is_recorded_and_copied', portable_metadata, portable_metadata_setup)
        for kind, target, reason in [('absolute', 'inputs/data.csv', 'absolute target'),
                                     ('broken', 'absent', 'Nonportable'),
                                     ('unmanifested', 'inputs/data.csv', 'hash/entry mismatch')]:
            run('DS_Store_symlink_' + kind,
                lambda b, k, s, reason=reason: reject(lambda: copy.prepare('sales', b / 'rejected', k), reason, b / 'rejected'),
                lambda b, k, s, kind=kind, target=target: (s / '.DS_Store').symlink_to(s / target if kind == 'absolute' else target))
        run('DS_Store_directory_content_is_not_ignored', lambda b, k, s: reject(
            lambda: copy.prepare('sales', b / 'rejected', k), 'hash/entry mismatch', b / 'rejected'),
            lambda b, k, s: write(s / '.DS_Store/actual-data.txt', 'actual resource'))
        run('other_hidden_file_is_not_ignored', lambda b, k, s: reject(
            lambda: copy.prepare('sales', b / 'rejected', k), 'hash/entry mismatch', b / 'rejected'),
            lambda b, k, s: write(s / '.hidden', 'actual resource'))

        def container_setup(b, k, s):
            path = s / '.agents/skills'
            path.rename(s / '.agents/moved-skills')
            path.symlink_to('moved-skills', target_is_directory=True)
            manifest(s)
        run('relative_container_symlink_rejected_before_copy', lambda b, k, s: reject(
            lambda: copy.prepare('sales', b / 'rejected', k), 'container must be an actual directory', b / 'rejected'),
            container_setup)
        run('whole_bundle_absolute_unreferenced_link', lambda b, k, s: reject(
            lambda: copy.prepare('sales', b / 'rejected', k), 'absolute target', b / 'rejected'),
            lambda b, k, s: (s / 'unused').symlink_to(s / 'inputs/data.csv'))

        def external_setup(b, k, s):
            write(b / 'external.txt', 'must not be read')
            (s / 'bundle-manifest.json').unlink()
            (s / 'bundle-manifest.json').symlink_to('../../../../external.txt')
        def external_manifest(b, k, s):
            read_text = Path.read_text
            def guarded(path, *args, **kwargs):
                require(path.resolve() != b / 'external.txt', 'external manifest was read')
                return read_text(path, *args, **kwargs)
            with patch.object(Path, 'read_text', guarded):
                return reject(lambda: copy.prepare('sales', b / 'rejected', k), 'outside workspace', b / 'rejected')
        run('external_manifest_symlink_not_read', external_manifest, external_setup)

        def loop_setup(b, k, s):
            (b / 'loop').symlink_to('loop')
        run('destination_symlink_loop_is_clean_error', lambda b, k, s: reject(
            lambda: copy.prepare('sales', b / 'loop/new', k), 'Cannot resolve destination'), loop_setup)
        def loop_cli(b, k, s):
            command = [sys.executable, '-I', '-B', str(k / 'scripts/prepare_sample_workspace.py'), 'sales', str(b / 'loop/new')]
            completed = subprocess.run(command, text=True, capture_output=True, check=False)
            require(completed.returncode == 1, 'CLI loop exit was not 1')
            require('Traceback' not in completed.stderr, 'CLI loop raised traceback')
            require('Cannot resolve destination' in completed.stderr or 'Too many levels of symbolic links' in completed.stderr,
                    'CLI loop reason missing: ' + completed.stderr)
            return {'required_reason_fragment': 'destination resolution / symlink loop',
                    'stderr': completed.stderr.strip(), 'exit_code': completed.returncode, 'traceback': False}
        run('destination_symlink_loop_CLI_no_traceback', loop_cli, loop_setup)
        run('bundle_symlink_loop_is_clean_error', lambda b, k, s: reject(
            lambda: copy.prepare('sales', b / 'rejected', k), 'cycle or excessive chain', b / 'rejected'),
            lambda b, k, s: (s / 'loop').symlink_to('loop'))

    report = {
        'all_passed': all(c['passed'] for c in results),
        'summary': {'total': len(results), 'passed': sum(c['passed'] for c in results),
                    'failed': sum(not c['passed'] for c in results)},
        'recorded_at_utc': datetime.now(timezone.utc).isoformat(), 'command_argv': sys.orig_argv,
        'python_executable': sys.executable, 'python_version': platform.python_version(),
        'isolated_mode': bool(sys.flags.isolated), 'optimization_level': sys.flags.optimize,
        'fixture_parent': fixture_parent, 'temporary_fixtures_removed': not root.exists(),
        'helper_sha256': hashlib.sha256(HELPER.read_bytes()).hexdigest(),
        'validator_sha256': hashlib.sha256(VALIDATOR.read_bytes()).hexdigest(),
        'test_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'Synthetic copy-helper fixtures only; no employee business execution.',
        'recognition_verified': False, 'business_verified': False, 'human_acceptance': False, 'cases': results,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered, encoding='utf-8')
        print(json.dumps({k: report[k] for k in ('all_passed', 'summary', 'isolated_mode')}))
        for result in results:
            if not result['passed']:
                print(json.dumps(result))
    else:
        print(rendered, end='')
    return 0 if report['all_passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
