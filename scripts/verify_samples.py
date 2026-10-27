#!/usr/bin/env python3
"""Validate minimal sample employees and latest-output provenance; never run their work.

Python 3.10+ and PyYAML. Includes all bundle files/relative links, native layout,
local Markdown file destinations, current configuration and saved input/output hashes.
Historical evidence remains at an immutable Git commit; it is not fetched here.
Does not independently recompute business outcomes, fetch remote links, verify all
Markdown anchor syntax, discover skills in Codex, or claim human acceptance.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from urllib.parse import unquote

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CASES = ('sales', 'minutes', 'reconciliation')


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


copy = load_module('sample_copy', HERE / 'prepare_sample_workspace.py')
layout = load_module('employee_layout', HERE / 'verify_employee_workspace.py')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local(root, base, name):
    if not isinstance(name, str) or not name or Path(name).is_absolute() or '\\' in name:
        raise ValueError('Expected a nonempty relative path: ' + repr(name))
    target = (base / name).resolve()
    if not target.is_relative_to(root.resolve()) or not target.exists():
        raise ValueError('Missing or outside employee: ' + name)
    return target


def check_case(root, case):
    checks = []

    def check(name, passed, detail=None):
        checks.append({'name': name, 'passed': bool(passed), 'detail': detail})

    try:
        if root.is_symlink() or not root.is_dir():
            raise ValueError('Employee root must be a real directory')
        root = root.resolve()
        # The safe snapshot audit bounds every symlink before other file reads.
        snap = copy.snapshot(root)
        manifest = read(root / 'bundle-manifest.json')
        check('bundle_all_entries_and_hashes', snap == {k: manifest[k] for k in ('files', 'symlinks')})
        check('no_inert_sample_files', not any('.sample.md' in x for x in snap['files']))
        for name in ('AGENTS.md', 'CLAUDE.md', 'README.md', 'interview.md', 'sample.json', 'records/definition.md'):
            check('required.' + name, (root / name).is_file())
        for name in ('inputs', 'outputs', 'records', '.agents/skills', '.claude/skills'):
            check('required.' + name, (root / name).is_dir())
        structure = layout.check_workspace(root)
        check('native_employee_structure', structure['static_checks_passed'], structure['errors'])
        data = read(root / 'sample.json')
        check('identity', data['schema_version'] == 2 and data['layout_version'] == 'sample-layout-v003' and data['case'] == case)
        check('human_acceptance_not_claimed', data['human_acceptance'] is False)
        for key in ('hearing_record', 'definition_record'):
            check('entry.' + key, local(root, root, data[key]).is_file())
        # Scan actual files, not duplicate symlink trees. Archived .txt quotations
        # retain historical paths and are not current navigation documents.
        checked_links = 0
        errors = []
        for relative in snap['files']:
            p = root / relative
            if p.suffix not in ('.md', '.markdown'):
                continue
            refs, missing = layout.markdown_links(p.read_text(encoding='utf-8'))
            errors.extend({'file': relative, 'undefined_reference': x} for x in missing)
            for ref in refs:
                if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', ref) or ref.startswith('//'):
                    if ref.lower().startswith('file:'):
                        errors.append({'file': relative, 'nonportable_link': ref})
                    continue
                rel = unquote(ref.split('#', 1)[0].split('?', 1)[0])
                if not rel:
                    continue
                checked_links += 1
                try:
                    local(root, p.parent, rel)
                except (ValueError, OSError, RuntimeError) as exc:
                    errors.append({'file': relative, 'link': ref, 'error': str(exc)})
        check('employee_local_markdown_links', not errors, {'checked': checked_links, 'errors': errors})
        run = data['latest_run']
        run_dir = root / 'outputs' / run['id']
        check('latest_run_directly_inside_employee', run_dir.is_dir() and run_dir.parent == root / 'outputs')
        output_paths = [local(root, root, name) for name in run['output_sha256']]
        check('only_latest_output', set((root / 'outputs').iterdir()) == {run_dir})
        check('output_location', all(p.parent == run_dir for p in output_paths))
        check('output_coverage', set(output_paths) == set(run_dir.iterdir()) and {p.name for p in output_paths} >= {'report.html', 'report.json'})
        expected_configs = {'AGENTS.md', 'CLAUDE.md', 'interview.md', 'records/definition.md'}
        expected_configs.update(p for p in snap['files'] if p.startswith('.claude/skills/'))
        check('current_configuration_coverage', set(data['current_definition_sha256']) == expected_configs)
        for name, digest in data['current_definition_sha256'].items():
            check('current_config.' + name, sha(local(root, root, name)) == digest)
        input_hashes = {p: h for p, h in snap['files'].items() if p.startswith('inputs/')}
        check('run_inputs_match', data['input_sha256'] == input_hashes)
        for name, digest in run['output_sha256'].items():
            check('run_output.' + Path(name).name, sha(local(root, root, name)) == digest)
        report = read(run_dir / 'report.json')
        check('report_identity_and_acceptance', report['run_id'] == run['id'] and report['human_acceptance'] is False)
        check('run_parameters', report['parameters'] == run['parameters'])
        check('cleanup_does_not_claim_rerun', data['cleanup']['business_rerun'] is False)
        commit = run['source_commit']
        check('immutable_history_commit', isinstance(commit, str) and re.fullmatch(r'[0-9a-f]{40}', commit) is not None)
        repository = 'https://github.com/Cyberdog-AI-Lab/ai-employee-kit'
        base = f'{repository}/blob/{commit}/sample/{case}/records'
        check('historical_record_locations', run['records_url'] == f'{repository}/tree/{commit}/sample/{case}/records'
              and run['manifest_url'] == f"{base}/runs/{run['id']}/run-manifest.json"
              and run['independent_verification']['url'] == f"{base}/verification/{run['id']}/independent.json")
        # These are a compact summary of the saved run, not newly executed checks.
        historical = run['independent_verification']
        check('historical_summary_shape', historical['passed_at_source_commit'] is True
              and type(historical['checks']) is int and historical['checks'] > 0
              and isinstance(historical['sha256'], str) and re.fullmatch(r'[0-9a-f]{64}', historical['sha256']) is not None)
        executed = run['executed_definition_sha256']
        check('executed_configuration_hash_format', all(isinstance(x, str) and re.fullmatch(r'[0-9a-f]{64}', x) is not None for x in executed.values()))
        if case == 'sales':
            recorded = {row['file']:row['sha256'] for row in report['definition_hashes']}
        elif case == 'minutes':
            recorded = report['definition']['hashes']
        else:
            recorded = {name:row['sha256'] for name,row in report['definition_files'].items()}
        # Historical definition paths need not exist in today's package. Bind
        # ALL entries recorded by the original report, not merely current ones.
        principal = {'AGENTS.md'} | {p for p in expected_configs if p.endswith('/SKILL.md')}
        check('executed_configuration_coverage', set(executed) == set(recorded))
        check('report_executed_definition_binding', principal <= set(recorded) and executed == recorded)
        if case == 'sales':
            input_rows = report['input_files']
            reported_inputs = {row['file']:row['sha256'] for row in input_rows}
        elif case == 'minutes':
            input_rows = report['input_files']
            reported_inputs = {row['path']:row['sha256'] for row in input_rows}
        else:
            input_rows = report['inputs']
            reported_inputs = {name:row['sha256'] for name,row in input_rows.items()}
        check('report_input_binding', len(input_rows) == len(reported_inputs) and reported_inputs == input_hashes)
        check('minimal_records', set(p for p in snap['files'] if p.startswith('records/')) == {'records/definition.md'})
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
        check('validation_completed', False, str(exc))
    return {'case': case, 'all_passed': all(x['passed'] for x in checks), 'checks': checks}


def verify(root):
    root = Path(root).resolve()
    sample = root / 'sample'
    actual = sorted(p.name for p in sample.iterdir() if p.is_dir())
    checks = [{'name': 'one_direct_folder_per_employee', 'passed': actual == sorted(CASES), 'actual': actual}]
    results = {case: check_case(sample / case, case) for case in CASES}
    return {'all_passed': all(c['passed'] for c in checks) and all(r['all_passed'] for r in results.values()),
            'scope': __doc__, 'saved_samples_only': True, 'checks': checks, 'results': results,
            'recognition_verified_by_this_script': False, 'historical_evidence_fetched': False, 'business_recomputed': False, 'human_acceptance': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=HERE.parent)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify(args.root)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered)
        print(json.dumps({'all_passed': result['all_passed'], 'checks': sum(len(r['checks']) for r in result['results'].values()) + len(result['checks']), 'output': str(args.output)}))
    else:
        print(rendered, end='')
    return 0 if result['all_passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
