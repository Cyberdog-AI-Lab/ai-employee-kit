#!/usr/bin/env python3
"""Read-only KIT static checks, with a bounded Markdown dependency parser.

This is neither a complete Markdown validator nor runtime/discovery verification.
"""
from pathlib import Path
from urllib.parse import unquote
import argparse
import hashlib
import json
import os
import re
import stat
import sys

try:
    import yaml
except ImportError:
    raise SystemExit('PyYAML is required; use scripts/requirements-validation.txt in your validation environment.')


class UniqueLoader(yaml.SafeLoader):
    pass


def mapping(loader, node, deep=False):
    result = {}
    for key, value in node.value:
        k = loader.construct_object(key, deep=deep)
        if k in result:
            raise ValueError('duplicate YAML key: ' + str(k))
        result[k] = loader.construct_object(value, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
FRONTMATTER = re.compile(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)(.*)\Z', re.S)
FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})([^\n]*)$')
# Single-line destinations, one balanced parentheses level, optional quoted title.
DESTINATION = r'(?:<[^<>\n]*>|(?:\\[^\n]|[^\s()<>\\]|\((?:\\.|[^()\n])*\))+)'
TITLE = r'''(?:[ \t]+(?:"[^"\n]*"|'[^'\n]*'|\([^()\n]*\)))?'''
INLINE = re.compile(r'\[([^\[\]\n]*)\]\([ \t]*(' + DESTINATION + r')' + TITLE + r'[ \t]*\)')
DEFINITION = re.compile(r'^ {0,3}\[([^\[\]\n]+)\]:[ \t]*(' + DESTINATION + r')' + TITLE + r'[ \t]*$', re.M)
REFERENCE = re.compile(r'\[([^\[\]\n]+)\](?:\[([^\[\]\n]*)\])?')
LIST_MARKER = re.compile(r'^( *)([-+*]|[0-9]{1,9}[.)])( {1,4})(\S.*|)$')
MARKDOWN_SUFFIXES = {'.md', '.markdown'}


def without_code(text):
    """Bounded list/fence scanner, not a CommonMark block parser.

    A list marker is prose at columns 0..3 or 0..3 columns beyond an active
    parent's content indent. Four additional columns are code, even if the
    line looks like a list marker. Tabs expand to four-column stops. Lazy list
    continuation and blockquote containers are outside this subset.
    """
    outside, blocks, body = [], [], []
    opening = None
    fence_indent = 0
    lists = []  # (marker indentation, content indentation)
    info = ''
    for line in text.splitlines(keepends=True):
        line = line.expandtabs(4)
        bare = line.rstrip('\r\n')
        if opening:
            candidate = bare[fence_indent:] if bare.startswith(' ' * fence_indent) else bare
            if re.fullmatch(r' {0,3}' + re.escape(opening[0]) + '{' + str(len(opening)) + r',}[ \t]*', candidate):
                blocks.append((info, ''.join(body)))
                opening, body = None, []
            else:
                body.append(line)
            outside.append('\n')
            continue
        if not bare.strip():
            outside.append('\n')
            continue
        indent = len(bare) - len(bare.lstrip(' '))
        marker = LIST_MARKER.match(bare)
        while lists and indent < lists[-1][1]:
            lists.pop()
        base_indent = lists[-1][1] if lists else 0
        if indent - base_indent >= 4:
            outside.append('\n')
            continue
        if marker:
            content_indent = len(marker[1]) + len(marker[2]) + len(marker[3])
            lists.append((indent, content_indent))
            prose_line = bare[content_indent:]
            base_indent = content_indent
        else:
            prose_line = bare[base_indent:]
        match = FENCE.match(prose_line)
        if match:
            opening, info = match[1], match[2].strip().lower()
            fence_indent = base_indent
            outside.append('\n')
        else:
            outside.append(prose_line + '\n')
    if opening:
        blocks.append((info, ''.join(body)))
    prose = ''.join(outside)
    prose = re.sub(r'(?<!`)(`+)(?!`)[\s\S]*?(?<!`)\1(?!`)', '', prose)
    return prose, blocks


def fenced_wrapper(text):
    """Heuristic for a whole quoted document or the known explanatory template."""
    outside, blocks = without_code(text)
    if not blocks:
        return False
    if not outside.strip():
        return True
    document_block = any(info in ('', 'md', 'markdown') and
                         re.search(r'(?m)^#{1,6}\s|^---\s*$|FIX-\d{3}', body)
                         for info, body in blocks)
    explanatory = re.search(
        r'非実行テンプレート|このファイルを実際のAGENTS\.mdとして使用しない|'
        r'以下のコードフェンスは生成後の形の見本|配置時は[^\n]*外側コードフェンス|'
        r'reference copy|template preview|not (?:a )?(?:production|deployed)', outside, re.I)
    return bool(document_block and explanatory)


def markdown_links(text):
    """Return supported destinations and unresolved explicit reference labels.

Single-line inline/image links and full/collapsed/defined shortcut references;
angle destinations and titles are supported. Bare angle text is not a local link.
"""
    text, _ = without_code(text)
    # HTML comments are prose examples, not dependencies. General HTML is unsupported.
    text = re.sub(r'<!--[\s\S]*?-->', '', text)
    normalize = lambda value: ' '.join(value.split()).casefold()
    definitions = {}
    for match in DEFINITION.finditer(text):
        definitions.setdefault(normalize(match[1]), match[2])
    text = DEFINITION.sub('', text)
    refs = [m[2] for m in INLINE.finditer(text)]
    text = INLINE.sub('', text)
    missing = []
    for match in REFERENCE.finditer(text):
        label = normalize(match[2] or match[1])
        if label in definitions:
            refs.append(definitions[label])
        elif match[2] is not None:
            missing.append(label)
    return [re.sub(r'\\([!"#$%&\'()*+,\-./:;<=>?@\[\]\\^_`{|}~])', r'\1',
                   ref[1:-1] if ref.startswith('<') else ref) for ref in refs], missing


def check_workspace(root, kit=None):
    root = Path(root).absolute()
    errors, details, warnings, skills = [], [], [], []
    hashes, config_hashes, cache = {}, {}, {}
    audited_links = {}
    pending, scanned = [], set()
    separation = {'status': 'not_checked', 'passed': None, 'kit_root': None}

    def fail(code, message):
        if message not in errors:
            errors.append(message)
            details.append({'code': code, 'message': message})

    try:
        root = root.resolve()
    except (OSError, RuntimeError) as exc:
        fail('workspace_root_invalid', 'cannot resolve workspace root: ' + str(exc))

    def resolve_path(path, depth=0):
        """Walk actual entries, including symlink targets, without reading outside W."""
        path = Path(path)
        try:
            parts = path.relative_to(root).parts
        except ValueError:
            fail('path_outside_workspace', 'path outside workspace: ' + str(path))
            return None
        if depth > 40:
            fail('symlink_cycle', 'symlink cycle or excessive chain: ' + str(path))
            return None
        current = root
        try:
            for part in parts:
                if not current.is_dir():
                    fail('not_directory', 'path component is not a directory: ' + str(current))
                    return None
                if part == '..':
                    if current == root:
                        fail('path_outside_workspace', 'path escapes workspace: ' + str(path))
                        return None
                    current = current.parent
                    continue
                entries = {p.name for p in current.iterdir()}
                if part not in entries:
                    variants = sorted(n for n in entries if n.casefold() == part.casefold())
                    if variants:
                        fail('path_capitalization', f'exact path capitalization required: {current / part}; found {variants}')
                    else:
                        fail('missing_path', 'missing path: ' + str(current / part))
                    return None
                current = current / part
                if current.is_symlink():
                    target = Path(os.readlink(current))
                    if target.is_absolute():
                        fail('absolute_symlink', 'absolute symlink is not portable: ' + str(current))
                        if not target.is_relative_to(root):
                            fail('path_outside_workspace', 'symlink target outside workspace: ' + str(current))
                        return None
                    resolved = resolve_path(current.parent / target, depth + 1)
                    if resolved is None:
                        fail('invalid_symlink_target', 'broken or invalid symlink target: ' + str(current))
                        return None
                    current = resolved
            return current
        except (OSError, RuntimeError) as exc:
            fail('path_access', f'cannot inspect path: {path}: {exc}')
            return None

    def audit_symlinks():
        """Inspect all physical entries in W; never descend through a symlink.

        This catches nonportable links in otherwise unreachable distribution
        files too. Only reached dependencies are read/hashed by read_file.
        """
        directories = [root]
        while directories:
            directory = directories.pop()
            try:
                for entry in sorted(directory.iterdir()):
                    mode = entry.lstat().st_mode
                    if stat.S_ISLNK(mode):
                        audited_links[str(entry.relative_to(root))] = os.readlink(entry)
                        resolve_path(entry)
                    elif stat.S_ISDIR(mode):
                        directories.append(entry)
            except (OSError, RuntimeError) as exc:
                fail('path_access', f'cannot audit symlinks: {directory}: {exc}')

    def read_file(path, configuration=False):
        real = resolve_path(path)
        if real is None:
            return None
        if not real.is_file():
            fail('not_file', 'expected regular file: ' + str(path))
            return None
        try:
            if real not in cache:
                cache[real] = real.read_bytes()
            data = cache[real]
        except OSError as exc:
            fail('file_read', f'cannot read file: {path}: {exc}')
            return None
        digest = hashlib.sha256(data).hexdigest()
        # Include logical connection and real dependency paths for auditability.
        key = str(path.relative_to(root))
        hashes[key] = digest
        hashes[str(real.relative_to(root))] = digest
        if configuration:
            config_hashes[key] = digest
        if real.suffix.lower() in MARKDOWN_SUFFIXES:
            pending.append(real)
        return data

    def read_text(path, configuration=False):
        data = read_file(path, configuration)
        if data is None:
            return ''
        try:
            text = data.decode('utf-8')
        except UnicodeError as exc:
            fail('text_encoding', f'cannot decode UTF-8: {path}: {exc}')
            return ''
        if configuration and re.search(r'\{\{[^}]+\}\}', text):
            fail('unexpanded_template', 'unexpanded template: ' + str(path))
        return text

    def tree(path, ancestors=frozenset()):
        real = resolve_path(path)
        if real is None:
            return {}
        if not real.is_dir():
            fail('not_directory', 'expected directory: ' + str(path))
            return {}
        if real in ancestors:
            fail('directory_cycle', 'directory symlink cycle: ' + str(path))
            return {}
        result = {}
        try:
            entries = sorted(real.iterdir())
        except OSError as exc:
            fail('path_access', f'cannot list directory: {path}: {exc}')
            return result
        for entry in entries:
            if entry.name == '.DS_Store' and not entry.is_symlink() and entry.is_file():
                continue
            logical = path / entry.name
            resolved = resolve_path(logical)
            if resolved is None:
                continue
            if resolved.is_dir():
                for rel, digest in tree(logical, ancestors | {real}).items():
                    result[entry.name + '/' + rel] = digest
            else:
                data = read_file(logical)
                if data is not None:
                    result[entry.name] = hashlib.sha256(data).hexdigest()
        return result

    if kit is None:
        warnings.append('K/W separation not checked: supply --kit-root; all_passed is false even if static_checks_passed is true.')
    else:
        try:
            kit = Path(kit).resolve(strict=True)
            if not kit.is_dir():
                raise ValueError('kit root is not a directory')
            separate = not (root == kit or root in kit.parents or kit in root.parents)
            separation.update(status='checked', passed=separate, kit_root=str(kit))
            if not separate:
                fail('kit_workspace_overlap', 'K and W must not contain each other')
        except (OSError, RuntimeError, ValueError) as exc:
            fail('kit_root_invalid', 'cannot check kit root: ' + str(exc))

    audit_symlinks()
    containers = {}
    for rel in ('.agents', '.agents/skills', '.claude', '.claude/skills'):
        path = root / rel
        parent = str(Path(rel).parent)
        if parent != '.' and not containers.get(parent):
            containers[rel] = False
            continue
        if path.is_symlink():
            fail('container_not_directory', 'container must be an actual directory, not a symlink: ' + rel)
            containers[rel] = False
            continue
        real = resolve_path(path)
        containers[rel] = real is not None and real.is_dir()
        if real is not None and not containers[rel]:
            fail('container_not_directory', 'container must be an actual directory: ' + rel)

    agents = read_text(root / 'AGENTS.md', True)
    if not agents.strip():
        fail('empty_agents', 'AGENTS.md is empty or unreadable')
    try:
        if any(p.name.casefold() == 'agents.override.md' for p in root.iterdir()):
            fail('agents_override', 'AGENTS.override.md (including case variants) shadows AGENTS.md; inspect active instruction chain')
    except OSError as exc:
        fail('path_access', 'cannot list workspace: ' + str(exc))
    if len(agents.encode('utf-8')) > 32768:
        fail('agents_size', 'AGENTS.md alone exceeds default 32 KiB instruction budget')
    if fenced_wrapper(agents):
        fail('fenced_agents_wrapper', 'AGENTS.md is a fenced reference wrapper, not the deployed body')
    claude = read_text(root / 'CLAUDE.md', True)
    if '@AGENTS.md' not in claude.splitlines():
        fail('claude_import', 'CLAUDE.md must import @AGENTS.md as a line')

    discovered = root / '.agents/skills'
    canonical = root / '.claude/skills'

    def skill_entries(path):
        real = resolve_path(path)
        if real is None:
            return []
        if not real.is_dir():
            fail('not_directory', 'expected directory: ' + str(path))
            return []
        try:
            return [path / p.name for p in sorted(real.iterdir())
                    if not (p.name == '.DS_Store' and not p.is_symlink() and p.is_file())]
        except OSError as exc:
            fail('path_access', f'cannot list skills: {path}: {exc}')
            return []

    folders = skill_entries(discovered) if containers['.agents/skills'] else []
    sources = skill_entries(canonical) if containers['.claude/skills'] else []
    if not folders:
        fail('no_discoverable_skills', 'no discoverable .agents/skills/<name>/SKILL.md')
    names = set()
    for folder in folders:
        if folder.is_symlink():
            expected = '../../.claude/skills/' + folder.name
            if os.readlink(folder) != expected:
                fail('skill_symlink_target', f'skill symlink must target exactly {expected}: {folder}')
        real = resolve_path(folder)
        if real is None:
            continue
        if not real.is_dir():
            fail('skill_entry_not_directory', 'skill entry is not a directory: ' + str(folder))
            continue
        source = canonical / folder.name
        f = folder / 'SKILL.md'
        text = read_text(f, True)
        source_text = read_text(source / 'SKILL.md', True)
        if tree(source) != tree(folder):
            fail('copy_divergence', 'canonical/connection contents differ: ' + folder.name)
        match = FRONTMATTER.fullmatch(text)
        if not match:
            fail('skill_frontmatter', 'SKILL.md needs frontmatter at byte zero: ' + str(f))
            continue
        try:
            meta = yaml.load(match[1], Loader=UniqueLoader)
        except (yaml.YAMLError, ValueError, TypeError) as exc:
            fail('invalid_yaml', f'invalid YAML {f}: {exc}')
            continue
        if not isinstance(meta, dict):
            fail('frontmatter_mapping', 'frontmatter must be a mapping: ' + str(f))
            continue
        name, desc = meta.get('name'), meta.get('description')
        if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
            fail('skill_name', 'invalid KIT skill name: ' + str(f))
            continue
        if name != folder.name:
            fail('skill_name_folder', 'name/folder mismatch: ' + str(f))
        if name in names:
            fail('duplicate_skill_name', 'duplicate skill name: ' + name)
        names.add(name)
        if not isinstance(desc, str) or not desc.strip():
            fail('skill_description', 'description must be a nonempty string: ' + str(f))
        if not match[2].strip():
            fail('empty_skill_body', 'empty skill body: ' + str(f))
        if fenced_wrapper(match[2]):
            fail('fenced_skill_wrapper', 'SKILL.md body is a fenced reference wrapper: ' + str(f))
        # Source content is also checked when a divergent copy was supplied.
        source_match = FRONTMATTER.fullmatch(source_text)
        if not source_match:
            fail('skill_frontmatter', 'SKILL.md needs frontmatter at byte zero: ' + str(source / 'SKILL.md'))
        skills.append({'name': name, 'discovery_path': str(f.relative_to(root)),
                       'canonical_path': str((source / 'SKILL.md').relative_to(root)),
                       'connection': 'symlink' if folder.is_symlink() else 'copy'})
    for folder in sources:
        if folder.name not in {p.name for p in folders}:
            fail('canonical_not_discoverable', 'canonical skill not discoverable: ' + folder.name)
        real = resolve_path(folder)
        if real is not None and not real.is_dir():
            fail('skill_entry_not_directory', 'canonical skill entry is not a directory: ' + str(folder))

    while pending:
        path = pending.pop()
        if path in scanned:
            continue
        scanned.add(path)
        text = read_text(path)
        frontmatter = FRONTMATTER.fullmatch(text)
        if frontmatter:
            text = frontmatter[2]
        refs, missing = markdown_links(text)
        for label in missing:
            fail('undefined_reference', f'undefined Markdown reference: {path} -> [{label}]')
        for ref in refs:
            if ref.lower().startswith('file:') or re.match(r'^[A-Za-z]:[\\/]', ref):
                fail('nonrelative_local_link', f'local link must be portable and relative: {path} -> {ref}')
                continue
            # Other URI schemes and network-path references are never fetched.
            if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', ref) or ref.startswith('//'):
                warnings.append(f'external URI not checked: {path.relative_to(root)} -> {ref}')
                continue
            rel = unquote(ref.split('#', 1)[0].split('?', 1)[0])
            if not rel:
                continue  # Anchor existence is outside this subset.
            if Path(rel).is_absolute() or '\\' in rel:
                fail('nonrelative_local_link', f'local link must be portable and relative: {path} -> {ref}')
                continue
            dst = path.parent / rel
            resolved = resolve_path(dst)
            if resolved is None:
                fail('invalid_local_link', f'broken, mis-cased or escaping local link: {path} -> {ref}')
            elif resolved.is_dir():
                tree(resolved)
            else:
                read_file(resolved)

    warnings.append('Static subset only: complete Markdown, anchors, HTML/embedded paths, account/ancestor instructions, D separation, approvals, skill selector, tool permissions, task outcomes and human acceptance are not verified. Wrapper detection is heuristic.')
    static_passed = not errors
    return {'workspace': str(root), 'all_passed': static_passed and separation['passed'] is True,
            'static_checks_passed': static_passed, 'kit_workspace_separation': separation,
            'validation_scope': 'KIT static layout and documented Markdown dependency subset only',
            'symlink_audit': {'scope': 'whole_workspace', 'follows_directory_symlinks': False,
                              'links': dict(sorted(audited_links.items()))},
            'errors': errors, 'error_details': details, 'warnings': list(dict.fromkeys(warnings)),
            'skills': skills, 'configuration_sha256': dict(sorted(config_hashes.items())),
            'reachable_local_file_sha256': dict(sorted(hashes.items())),
            'markdown_files_scanned': sorted(str(p.relative_to(root)) for p in scanned),
            'recognition_verified': False, 'business_verified': False, 'human_acceptance': False}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('workspace', type=Path)
    ap.add_argument('--kit-root', type=Path, help='required for all_passed; omission records not_checked')
    args = ap.parse_args()
    result = check_workspace(args.workspace, args.kit_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result['all_passed'] else 1)
