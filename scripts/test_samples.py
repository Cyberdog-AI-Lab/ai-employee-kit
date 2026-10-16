#!/usr/bin/env python3
"""Regressions for the direct employee layout and provenance bindings.

Use real, small minutes fixtures copied into temporary directories. No AI work,
network, external software, or user data is run. Explicit checks survive python -O.
"""
from pathlib import Path
import argparse
import importlib.util
import json
import shutil
import sys
import tempfile
import traceback

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('samples', HERE / 'verify_samples.py')
samples = importlib.util.module_from_spec(spec)
spec.loader.exec_module(samples)


def require(value, message):
    if not value:
        raise AssertionError(message)


def reseal(root):
    path = root / 'bundle-manifest.json'
    data = samples.read(path)
    data.update(samples.copy.snapshot(root))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def change_json(path, mutate):
    data = samples.read(path)
    mutate(data)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--temp-root', type=Path, help='fixture parent; default OS temporary directory outside KIT')
    args = parser.parse_args()
    if args.temp_root is None and Path(tempfile.gettempdir()).resolve().is_relative_to(HERE.parent):
        parser.error('Default temporary directory must be outside KIT; set --temp-root')
    results = []
    template = HERE.parent / 'sample/minutes'

    def run(name, mutate, failure, seal=True):
        with tempfile.TemporaryDirectory(prefix='employee-sample-test-', dir=args.temp_root) as directory:
            root = Path(directory) / 'minutes'
            shutil.copytree(template, root, symlinks=True)
            try:
                mutate(root)
                if seal:
                    reseal(root)
                result = samples.check_case(root, 'minutes')
                failed = [x['name'] for x in result['checks'] if not x['passed']]
                if failure is None:
                    require(result['all_passed'], repr(failed))
                else:
                    require(not result['all_passed'] and failure in failed, repr(failed))
                results.append({'case': name, 'passed': True, 'detected': failed})
            except Exception:
                results.append({'case': name, 'passed': False, 'error': traceback.format_exc()})

    run('complete_employee_stands_alone', lambda w: None, None)
    run('inert_AGENTS_name_is_not_a_config', lambda w: (w / 'AGENTS.md').rename(w / 'employee-agents.sample.md'), 'native_employee_structure')
    run('missing_Codex_discovery_connection', lambda w: (w / '.agents/skills/work-002').unlink(), 'native_employee_structure')
    run('README_cannot_route_to_another_employee', lambda w: (w / 'README.md').write_text('[real config](../AGENTS.md)'), 'employee_local_markdown_links')
    run('missing_hearing_record', lambda w: (w / 'interview.md').unlink(), 'required.interview.md')
    run('modified_output_even_with_fresh_bundle_hash', lambda w: (next((w / 'outputs').glob('*/report.html'))).write_text('changed'), 'run_output.report.html')
    run('modified_config_even_with_fresh_bundle_hash', lambda w: (w / 'AGENTS.md').write_text((w / 'AGENTS.md').read_text() + '\nNew policy.\n'), 'run_config.AGENTS.md')
    run('modified_skill_reference_even_with_fresh_bundle_hash', lambda w: (w / '.claude/skills/work-002/references/input-contract.md').write_text('Changed business input contract.\n'), 'run_config..claude/skills/work-002/references/input-contract.md')
    run('modified_input_even_with_fresh_bundle_hash', lambda w: (w / 'inputs/README.md').write_text('changed'), 'run_inputs_match')
    run('failed_saved_independent_record', lambda w: change_json(next((w / 'records/verification').glob('*/independent.json')), lambda d: d.update(all_passed=False)), 'saved_independent_record_passed')
    run('independent_record_bytes_bound_to_run', lambda w: change_json(next((w / 'records/verification').glob('*/independent.json')), lambda d: d.update(extra='changed')), 'independent_record_hash')
    run('sample_cannot_claim_human_acceptance', lambda w: change_json(w / 'sample.json', lambda d: d.update(human_acceptance=True)), 'human_acceptance_not_claimed')
    run('mismatched_run_id', lambda w: change_json(next((w / 'records/runs').glob('*/run-manifest.json')), lambda d: d.update(run_id='wrong-run')), 'run_identity')
    run('tamper_without_resealing_bundle', lambda w: (w / 'README.md').write_text('changed'), 'bundle_all_entries_and_hashes', seal=False)

    with tempfile.TemporaryDirectory(prefix='employee-layout-test-', dir=args.temp_root) as directory:
        root = Path(directory)
        shutil.copytree(HERE.parent / 'sample', root / 'sample', symlinks=True)
        try:
            before = samples.verify(root)
            require(before['all_passed'], 'Complete fixture did not pass')
            (root / 'sample/workspaces').mkdir()
            shutil.move(root / 'sample/minutes', root / 'sample/workspaces/minutes')
            after = samples.verify(root)
            require(not after['all_passed'] and not after['checks'][0]['passed'], 'Legacy split layout was accepted')
            require(not after['results']['minutes']['all_passed'], 'Direct minutes root was optional')
            results.append({'case': 'legacy_workspaces_detour_is_rejected', 'passed': True})
        except Exception:
            results.append({'case': 'legacy_workspaces_detour_is_rejected', 'passed': False, 'error': traceback.format_exc()})
    report = {'all_passed': all(x['passed'] for x in results), 'summary': {'total': len(results), 'passed': sum(x['passed'] for x in results)}, 'cases': results, 'human_acceptance': False, 'scope': __doc__}
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered)
        print(json.dumps({k: report[k] for k in ('all_passed', 'summary')}))
    else:
        print(rendered, end='')
    return 0 if report['all_passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
