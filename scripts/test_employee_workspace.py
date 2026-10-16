#!/usr/bin/env python3
"""Synthetic regression fixtures only; no discovery, business execution or network.

Run with python3 -I -B scripts/test_employee_workspace.py. Temporary fixtures use
the OS temporary directory (or --temp-root), and are removed after the test run.
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

# An explicit sibling import also works with python -I (no cwd/script sys.path).
sys.dont_write_bytecode = True
VALIDATOR = Path(__file__).resolve().with_name('verify_employee_workspace.py')
spec = importlib.util.spec_from_file_location('employee_workspace_validator', VALIDATOR)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
check_workspace = validator.check_workspace


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def fixture(w):
    write(w / 'AGENTS.md', '# Demo employee\nKeep source inputs. Use [rules](rules.md).\n')
    write(w / 'CLAUDE.md', '@AGENTS.md\n')
    write(w / 'rules.md', 'Fictional local work only.\n')
    write(skill(w), '---\nname: demo-work\ndescription: Compare the supplied fictional records.\n---\n\nFollow [rules](../../../rules.md).\n')
    (w / '.agents/skills').mkdir(parents=True)
    connection(w).symlink_to('../../.claude/skills/demo-work', target_is_directory=True)


def skill(w):
    return w / '.claude/skills/demo-work/SKILL.md'


def connection(w):
    return w / '.agents/skills/demo-work'


def change(w, old, new):
    path = skill(w)
    write(path, path.read_text().replace(old, new))


def copy_connection(w):
    connection(w).unlink()
    shutil.copytree(skill(w).parent, connection(w))


def relink(w, target):
    connection(w).unlink()
    connection(w).symlink_to(target, target_is_directory=True)


def case_rename(w, rel, name):
    path = w / rel
    temporary = path.with_name('__case_rename__')
    path.rename(temporary)
    temporary.rename(path.with_name(name))


def wrapper(w, marker='```', explanation=''):
    write(w / 'AGENTS.md', explanation + '\n' + marker + 'markdown\n' +
          ('# Demo employee\nKeep source inputs.\n' * 30) + marker + '\n')


def code_example(w):
    write(w / 'AGENTS.md', '# Demo employee\nPreserve originals and use [rules](rules.md).\n\n'
          'Use this command to inspect the supplied fixture:\n```sh\ncat "file.txt"\n'
          '# [not a dependency](missing-code.md)\n```\n\n'
          'Document the result with this small Markdown example:\n~~~markdown\n'
          '# Result\n[an example](missing-example.md)\n~~~\n'
          'Keep decisions grounded in the supplied records.\n'
          '`[inline example](missing-inline.md)`\n'
          '    [indented example](missing-indented.md)\n')
    change(w, 'Follow [rules](../../../rules.md).',
           'Follow [rules](../../../rules.md).\n```python\nprint("example")\n```\n'
           'Record uncertainty before delivering the result.')


def dependency(w, text):
    write(w / 'AGENTS.md', '# Demo employee\nPreserve originals.\n' + text + '\n')


def recursive(w, broken=False):
    dependency(w, '[first](references/one.md)')
    write(w / 'references/one.md', '[second][next]\n\n[next]: <two.md> "More"\n')
    write(w / 'references/two.md', '[back](one.md) and [file](data.bin)\n')
    if not broken:
        (w / 'references/data.bin').write_bytes(bytes(range(256)))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def assert_hashes(w, result, paths):
    for rel in paths:
        expected = hashlib.sha256((w / rel).read_bytes()).hexdigest()
        require(result['reachable_local_file_sha256'].get(rel) == expected,
                'missing or incorrect SHA-256: ' + rel)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--temp-root', type=Path, help='fixture parent; default: OS temporary directory outside K')
    args = parser.parse_args()
    if args.temp_root is None and Path(tempfile.gettempdir()).resolve().is_relative_to(VALIDATOR.parent.parent):
        parser.error('default temporary directory must be outside K; set --temp-root explicitly')
    results = []
    with tempfile.TemporaryDirectory(prefix='employee-layout-tests-', dir=args.temp_root) as t:
        base = Path(t).resolve()
        fixture_parent = str(base.parent.resolve())
        kit = base / 'kit'
        kit.mkdir()

        def run(name, mutate=lambda w: None, code=None, fragment=None, inspect=None,
                kit_value=kit, expected=None):
            w = base / name
            fixture(w)
            case = {'case': name, 'expected_pass': code is None if expected is None else expected,
                    'required_reason_code': code, 'required_reason_fragment': fragment}
            try:
                mutate(w)
                actual_kit = kit_value(w) if callable(kit_value) else kit_value
                # A failing path must not merely avoid publishing an external
                # hash: fail the test if the validator reads/lists outside W.
                original_read, original_iterdir = Path.read_bytes, Path.iterdir
                def guarded_read(path):
                    require(path.resolve().is_relative_to(w.resolve()), 'read outside W: ' + str(path))
                    return original_read(path)
                def guarded_iterdir(path):
                    require(path.resolve().is_relative_to(w.resolve()), 'list outside W: ' + str(path))
                    return original_iterdir(path)
                with patch.object(Path, 'read_bytes', guarded_read), patch.object(Path, 'iterdir', guarded_iterdir):
                    result = check_workspace(w, actual_kit)
                codes = [e['code'] for e in result['error_details']]
                case.update(actual_pass=result['all_passed'], observed_reason_codes=codes,
                            errors=result['errors'], separation=result['kit_workspace_separation'])
                require(result['all_passed'] == case['expected_pass'], 'unexpected pass/fail result')
                if code:
                    require(code in codes, 'expected reason code absent: ' + code)
                else:
                    require(not result['errors'], 'valid or omitted-kit fixture has errors')
                if fragment:
                    require(any(fragment in e['message'] and (code is None or e['code'] == code)
                                for e in result['error_details']), 'expected diagnostic fragment absent')
                require(result['recognition_verified'] is False and result['business_verified'] is False
                        and result['human_acceptance'] is False, 'runtime/acceptance claim must remain false')
                if inspect:
                    inspect(w, result)
                case['passed'] = True
            except Exception:
                case.update(passed=False, failure=traceback.format_exc())
            results.append(case)

        run('valid_symlink_with_kit', inspect=lambda w, r: (
            require(r['kit_workspace_separation']['status'] == 'checked', 'separation was not checked'),
            assert_hashes(w, r, ['AGENTS.md', 'CLAUDE.md', 'rules.md',
                                '.claude/skills/demo-work/SKILL.md', '.agents/skills/demo-work/SKILL.md'])))
        run('valid_copy', copy_connection)
        run('omitted_kit_is_incomplete', kit_value=None, expected=False, inspect=lambda w, r: (
            require(r['static_checks_passed'], 'structural checks should pass'),
            require(r['kit_workspace_separation'] == {'status': 'not_checked', 'passed': None, 'kit_root': None},
                    'omitted separation must be explicit'),
            require(any('not checked' in s for s in r['warnings']), 'missing omitted-kit warning')))
        run('kit_contains_workspace', code='kit_workspace_overlap', kit_value=base)
        run('workspace_is_kit', code='kit_workspace_overlap', kit_value=lambda w: w)
        run('workspace_contains_kit', lambda w: (w / 'nested-kit').mkdir(),
            code='kit_workspace_overlap', kit_value=lambda w: w / 'nested-kit')
        run('kit_alias_overlap', lambda w: (base / 'kit-alias').symlink_to(w),
            code='kit_workspace_overlap', kit_value=base / 'kit-alias')
        run('missing_kit', code='kit_root_invalid', kit_value=base / 'absent-kit')
        run('missing_AGENTS', lambda w: (w / 'AGENTS.md').rename(w / 'employee-agents.sample.md'),
            'missing_path', 'AGENTS.md')
        run('missing_CLAUDE', lambda w: (w / 'CLAUDE.md').unlink(), 'missing_path', 'CLAUDE.md')
        for rel, renamed in [('AGENTS.md', 'agents.md'), ('CLAUDE.md', 'claude.md'),
                             ('.agents', '.Agents'), ('.claude', '.Claude'),
                             ('.agents/skills', 'Skills'), ('.claude/skills', 'Skills'),
                             ('.claude/skills/demo-work/SKILL.md', 'skill.md')]:
            run('case_' + rel.replace('/', '_'), lambda w, rel=rel, renamed=renamed: case_rename(w, rel, renamed),
                'path_capitalization', rel.split('/')[-1])
        run('copy_SKILL_case', lambda w: (copy_connection(w),
            case_rename(w, '.agents/skills/demo-work/SKILL.md', 'skill.md')), 'path_capitalization', 'SKILL.md')
        run('missing_discovery_directory', lambda w: (w / '.agents/skills').rename(w / '.agents/other-skills'),
            'missing_path', '.agents/skills')
        run('link_text_file', lambda w: (connection(w).unlink(), write(connection(w), '../../.claude/skills/demo-work')),
            'skill_entry_not_directory')
        run('absolute_symlink', lambda w: relink(w, skill(w).parent), 'skill_symlink_target', '../../.claude/skills/demo-work')
        run('equivalent_nonexact_symlink', lambda w: relink(w, '../../.claude/skills/../skills/demo-work'),
            'skill_symlink_target')
        run('wrong_internal_identical_target', lambda w: (shutil.copytree(skill(w).parent, w / 'duplicate'),
            relink(w, '../../duplicate')), 'skill_symlink_target')
        run('external_skill_target', lambda w: relink(w, base), 'path_outside_workspace')
        run('broken_skill_symlink', lambda w: relink(w, '../../missing'), 'invalid_symlink_target')
        run('broken_exact_skill_symlink', lambda w: shutil.rmtree(skill(w).parent), 'invalid_symlink_target')
        run('skill_symlink_cycle', lambda w: relink(w, 'demo-work'), 'symlink_cycle')
        external = base / 'external-resource.txt'
        write(external, 'External synthetic fixture; validator must not hash this.\n')
        no_external_hash = lambda w, r: require(hashlib.sha256(external.read_bytes()).hexdigest()
            not in r['reachable_local_file_sha256'].values(), 'external file was hashed')
        run('external_skill_resource', lambda w: (skill(w).parent / 'resource.txt').symlink_to(external),
            'path_outside_workspace', inspect=no_external_hash)
        run('broken_skill_resource', lambda w: (skill(w).parent / 'resource.txt').symlink_to('missing.txt'),
            'invalid_symlink_target')
        run('external_resource_directory', lambda w: (skill(w).parent / 'references').symlink_to(base),
            'path_outside_workspace', inspect=no_external_hash)
        run('resource_directory_cycle', lambda w: (skill(w).parent / 'cycle').symlink_to('.'), 'directory_cycle')
        run('backtick_wrapper', wrapper, 'fenced_agents_wrapper')
        run('tilde_wrapper', lambda w: wrapper(w, '~~~~'), 'fenced_agents_wrapper')
        run('long_explanatory_wrapper', lambda w: wrapper(w, '```',
            '# 生成社員AGENTS — 非実行テンプレート\n' +
            ('この説明は配置された社員本文ではありません。' * 30)), 'fenced_agents_wrapper')
        run('english_explanatory_wrapper', lambda w: wrapper(w, '~~~',
            '# Reference copy\n' + ('The following is a template preview. ' * 30)), 'fenced_agents_wrapper')
        run('valid_code_examples', code_example)
        run('override_shadows_root', lambda w: write(w / 'AGENTS.override.md', 'Other role'), 'agents_override')
        run('fenced_SKILL', lambda w: write(skill(w), '```markdown\n' + skill(w).read_text() + '```\n'), 'skill_frontmatter')
        run('fenced_skill_body', lambda w: change(w, 'Follow [rules](../../../rules.md).',
            '~~~markdown\n# All procedures\nPreserve originals.\n~~~'), 'fenced_skill_wrapper')
        run('missing_description', lambda w: change(w, 'description: Compare the supplied fictional records.\n', ''), 'skill_description')
        run('boolean_description', lambda w: change(w, 'Compare the supplied fictional records.', 'true'), 'skill_description')
        run('blank_description', lambda w: change(w, 'Compare the supplied fictional records.', '"   "'), 'skill_description')
        run('duplicate_yaml_key', lambda w: change(w, 'name: demo-work', 'name: demo-work\nname: second'), 'invalid_yaml', 'duplicate YAML key')
        run('name_mismatch', lambda w: change(w, 'name: demo-work', 'name: other-work'), 'skill_name_folder')
        run('invalid_name', lambda w: change(w, 'name: demo-work', 'name: BAD_name'), 'skill_name')
        run('unexpanded_template', lambda w: change(w, 'Follow [rules]', '{{missing}} Follow [rules]'), 'unexpanded_template')
        run('missing_CLAUDE_import', lambda w: write(w / 'CLAUDE.md', 'Reference only'), 'claude_import')
        run('copy_divergence', lambda w: (copy_connection(w), write(connection(w) / 'extra.txt', 'Changed')), 'copy_divergence')
        run('over_32KiB', lambda w: write(w / 'AGENTS.md', '# Role\n' + 'あ' * 11000), 'agents_size')
        run('exactly_32KiB', lambda w: write(w / 'AGENTS.md', 'a' * 32768))
        run('missing_inline_dependency', lambda w: (w / 'rules.md').unlink(), 'invalid_local_link', 'rules.md')
        run('missing_angle_dependency', lambda w: dependency(w, '[rules](<missing file.md> "Title")'),
            'invalid_local_link', 'missing file.md')
        run('valid_angle_and_encoded_dependency', lambda w: (write(w / 'with space.md', '# Local\n'),
            dependency(w, '[a](<with space.md> "Title") [b](with%20space.md#anchor)')),
            inspect=lambda w, r: assert_hashes(w, r, ['with space.md']))
        run('balanced_destination_parentheses', lambda w: (write(w / 'rules(v1).md', '# Local'),
            dependency(w, '[v1](rules(v1).md)')),
            inspect=lambda w, r: assert_hashes(w, r, ['rules(v1).md']))
        for label, use in [('full', '[rules][ RULES ]'), ('collapsed', '[rules][]'), ('shortcut', '[rules]')]:
            run('missing_reference_' + label, lambda w, use=use: dependency(w, use + '\n\n[rules]: <missing.md> "Title"'),
                'invalid_local_link', 'missing.md')
        run('undefined_full_reference', lambda w: dependency(w, '[rules][undefined]'), 'undefined_reference', 'undefined')
        run('unused_definition_not_dependency', lambda w: dependency(w, 'Preserve originals.\n\n[unused]: missing.md'))
        run('recursive_dependency_missing', lambda w: recursive(w, True), 'invalid_local_link', 'data.bin')
        run('recursive_dependency_cycle_and_binary_hash', recursive, inspect=lambda w, r: (
            assert_hashes(w, r, ['references/one.md', 'references/two.md', 'references/data.bin']),
            require('references/two.md' in r['markdown_files_scanned'], 'transitive Markdown was not scanned')))
        run('skill_reference_recursive_missing', lambda w: write(skill(w).parent / 'references/detail.md', '[broken](missing.md)'),
            'invalid_local_link', 'missing.md')
        run('linked_directory_hashes', lambda w: (write(w / 'documents/details.md', '[binary](data.bin)'),
            write(w / 'documents/data.bin', 'binary fixture'), dependency(w, '[docs](documents/)')),
            inspect=lambda w, r: assert_hashes(w, r, ['documents/details.md', 'documents/data.bin']))
        run('dependency_wrong_case', lambda w: dependency(w, '[rules](Rules.md)'), 'path_capitalization', 'Rules.md')
        run('dependency_escapes_workspace', lambda w: dependency(w, '[outside](../external-resource.txt)'),
            'path_outside_workspace', inspect=no_external_hash)
        run('dependency_external_symlink', lambda w: ((w / 'external.txt').symlink_to(external),
            dependency(w, '[outside](external.txt)')), 'path_outside_workspace', inspect=no_external_hash)
        run('dependency_broken_symlink', lambda w: ((w / 'broken.txt').symlink_to('absent.txt'),
            dependency(w, '[missing](broken.txt)')), 'invalid_symlink_target')
        run('absolute_local_link', lambda w: dependency(w, '[absolute](' + str(w / 'rules.md') + ')'), 'nonrelative_local_link')
        run('file_URI_rejected', lambda w: dependency(w, '[file](' + (w / 'rules.md').as_uri() + ')'),
            'nonrelative_local_link')
        run('windows_absolute_link', lambda w: dependency(w, '[file](C:/outside.md)'), 'nonrelative_local_link')
        run('file_component_not_directory', lambda w: dependency(w, '[rules](rules.md/../rules.md)'), 'not_directory')
        run('code_example_before_active_prose', lambda w: write(w / 'AGENTS.md',
            '```python\nprint("example")\n```\n# Demo employee\nPreserve originals; use [rules](rules.md).\n'))
        run('external_URI_is_explicitly_unchecked', lambda w: dependency(w, '[web](https://example.invalid/reference)'),
            inspect=lambda w, r: require(any('external URI not checked' in s for s in r['warnings']), 'URI scope missing'))
        run('DS_Store_only_ignored', lambda w: (write(w / '.agents/skills/.DS_Store', 'macOS metadata'),
            write(w / '.claude/skills/.DS_Store', 'macOS metadata'), copy_connection(w),
            write(skill(w).parent / '.DS_Store', 'different metadata')),
            inspect=lambda w, r: require(not any('.DS_Store' in p for p in r['reachable_local_file_sha256']), 'housekeeping hashed'))
        run('other_hidden_skill_entry_not_ignored', lambda w: write(w / '.agents/skills/.other', 'unexpected'), 'skill_entry_not_directory')
        run('other_hidden_resource_not_ignored', lambda w: (copy_connection(w), write(skill(w).parent / '.hidden', 'actual resource')),
            'copy_divergence')
        run('DS_Store_symlink_not_ignored', lambda w: (skill(w).parent / '.DS_Store').symlink_to(external), 'path_outside_workspace')

        # L1: all four containers must be actual directories, even if a link
        # points at an otherwise correct, byte-identical tree inside W.
        def container(w, rel, kind):
            path = w / rel
            moved = path.with_name('moved-' + path.name)
            path.rename(moved)
            if kind == 'file':
                write(path, 'not a directory')
            else:
                target = moved if kind.endswith('internal') else base
                if kind.startswith('relative'):
                    target = os.path.relpath(target, path.parent)
                path.symlink_to(target, target_is_directory=True)
        for rel in ('.agents', '.agents/skills', '.claude', '.claude/skills'):
            for kind in ('absolute_internal', 'relative_internal', 'absolute_external', 'relative_external', 'file'):
                run('container_' + rel.replace('/', '_') + '_' + kind,
                    lambda w, rel=rel, kind=kind: container(w, rel, kind), 'container_not_directory', rel)

        def absolute_file(w, rel):
            path = w / rel
            moved = path.with_name('actual-' + path.name)
            path.rename(moved)
            path.symlink_to(moved)
        for rel in ('AGENTS.md', 'CLAUDE.md', 'rules.md', '.claude/skills/demo-work/SKILL.md'):
            run('absolute_file_' + rel.replace('/', '_'), lambda w, rel=rel: absolute_file(w, rel),
                'absolute_symlink', rel)
        run('absolute_unreferenced_link', lambda w: ((w / 'unused').mkdir(),
            (w / 'unused/link').symlink_to(w / 'rules.md')), 'absolute_symlink', 'unused/link')
        run('relative_chain_to_absolute_link', lambda w: ((w / 'absolute.md').symlink_to(w / 'rules.md'),
            (w / 'alias.md').symlink_to('absolute.md'), dependency(w, '[alias](alias.md)')),
            'absolute_symlink', 'absolute.md')
        run('unreferenced_relative_external_link', lambda w: (w / 'unused').symlink_to('../external-resource.txt'),
            'path_outside_workspace', inspect=no_external_hash)
        run('relative_dependency_symlink_is_portable', lambda w: ((w / 'alias.md').symlink_to('rules.md'),
            dependency(w, '[alias](alias.md)')), inspect=lambda w, r: require(
                r['symlink_audit']['links']['alias.md'] == 'rules.md', 'relative link not audited'))
        run('root_DS_Store_symlink_not_ignored', lambda w: (w / '.DS_Store').symlink_to(external),
            'absolute_symlink', '.DS_Store')
        run('relative_DS_Store_symlink_is_hashed', lambda w: (skill(w).parent / '.DS_Store').symlink_to('SKILL.md'),
            inspect=lambda w, r: assert_hashes(w, r, ['.claude/skills/demo-work/.DS_Store']))
        run('DS_Store_directory_not_ignored', lambda w: (copy_connection(w),
            write(skill(w).parent / '.DS_Store/resource.md', '# Actual resource')), 'copy_divergence')

        # L3: list marker lines are scanned only in supported list context.
        for marker in ('-', '+', '*', '1.', '12)'):
            run('nested_list_missing_' + marker, lambda w, marker=marker: dependency(w,
                '- parent\n    ' + marker + ' child\n        - [missing](nested-missing.md)'),
                'invalid_local_link', 'nested-missing.md')
        run('nested_list_valid_hash', lambda w: (write(w / 'nested.md', '# Nested dependency'), dependency(w,
            '- parent\n    - child\n        - [rules](nested.md)')),
            inspect=lambda w, r: assert_hashes(w, r, ['nested.md']))
        run('tab_nested_list_missing', lambda w: dependency(w, '- parent\n\t- [missing](tab-missing.md)'),
            'invalid_local_link', 'tab-missing.md')
        run('nested_list_reference_missing', lambda w: dependency(w,
            '- parent\n    - [rules][r]\n\n[r]: nested-missing.md'), 'invalid_local_link', 'nested-missing.md')
        run('loose_nested_list_missing', lambda w: dependency(w,
            '- parent\n\n    - [missing](loose-missing.md)'), 'invalid_local_link', 'loose-missing.md')
        run('indented_marker_code_is_not_dependency', lambda w: dependency(w,
            '\n    - [example](missing-code.md)\n\t1. [example](missing-tab-code.md)'))
        run('list_indented_code_is_not_dependency', lambda w: dependency(w,
            '- parent\n\n      - [example](missing-list-code.md)\n      [example](missing-code.md)'))
        run('nested_fenced_code_is_not_dependency', lambda w: dependency(w,
            '- parent\n    - child\n      ```markdown\n      - [example](missing-fence.md)\n      ```\n'
            '    - [rules](rules.md)'), inspect=lambda w, r: assert_hashes(w, r, ['rules.md']))
        run('nested_inline_code_is_not_dependency', lambda w: dependency(w,
            '- parent\n    - `[example](missing-inline.md)`'))

        # L4: whitespace separates shortcut references; it never joins a full
        # reference. Adjacent undefined references remain a reasoned failure.
        run('spaced_brackets_are_prose', lambda w: dependency(w, '[a] [b] [c]\t[d]'))
        run('spaced_brackets_keep_defined_shortcut', lambda w: dependency(w,
            '[a] [b]\n\n[b]: shortcut-missing.md'), 'invalid_local_link', 'shortcut-missing.md')
        run('spaced_collapsed_brackets_are_prose', lambda w: dependency(w, '[a] []'))
        run('adjacent_undefined_collapsed_reference', lambda w: dependency(w, '[a][]'), 'undefined_reference', '[a]')

        def cli_check(w, result):
            for extra, expected_exit, expected_status in [(['--kit-root', str(kit)], 0, 'checked'), ([], 1, 'not_checked')]:
                completed = subprocess.run([sys.executable, '-I', '-B', str(VALIDATOR), str(w), *extra],
                                           text=True, capture_output=True, check=False)
                require(completed.returncode == expected_exit, 'CLI exit mismatch: ' + completed.stderr)
                output = json.loads(completed.stdout)
                require(output['kit_workspace_separation']['status'] == expected_status, 'CLI separation status mismatch')
        run('isolated_CLI_exit_and_separation', inspect=cli_check)

    report = {'all_passed': all(c['passed'] for c in results),
              'summary': {'total': len(results), 'passed': sum(c['passed'] for c in results),
                          'failed': sum(not c['passed'] for c in results)},
              'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
              'command_argv': sys.orig_argv, 'python_executable': sys.executable,
              'python_version': platform.python_version(), 'pyyaml_version': validator.yaml.__version__,
              'isolated_mode': bool(sys.flags.isolated), 'validator_path': str(VALIDATOR),
              'fixture_parent': fixture_parent, 'temporary_fixtures_removed': not base.exists(),
              'validator_sha256': hashlib.sha256(VALIDATOR.read_bytes()).hexdigest(),
              'test_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'Synthetic static-validator regression fixtures only; no generated workspace tested.',
              'recognition_verified': False, 'business_verified': False, 'human_acceptance': False,
              'cases': results}
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered, encoding='utf-8')
        print(json.dumps({key: report[key] for key in ['all_passed', 'summary', 'isolated_mode']}, ensure_ascii=False))
        for case in results:
            if not case['passed']:
                print(json.dumps(case, ensure_ascii=False))
    else:
        print(rendered, end='')
    return 0 if report['all_passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
