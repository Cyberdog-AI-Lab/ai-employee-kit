#!/usr/bin/env python3
"""Read-only, offline sample showcase. Python 3.10+, standard library only."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path, PurePosixPath
import re
import stat
from urllib.parse import quote, unquote, urlsplit

CASES = ('sales', 'minutes', 'reconciliation')
ASSETS = Path(__file__).resolve().parent
STATIC = {'/': 'index.html', '/index.html': 'index.html', '/app.js': 'app.js', '/source-pages.js': 'source-pages.js', '/styles.css': 'styles.css', '/markdown-view.js': 'markdown-view.js', '/vendor/markdown-it.min.js': 'vendor/markdown-it.min.js'}
TEXT_TYPES = {'.md', '.markdown', '.json', '.csv', '.tsv', '.txt', '.xml', '.log', '.yaml', '.yml', '.toml', '.py', '.js', '.css', '.html', '.svg'}


def public_error(exc):
    """Never project exception paths or low-level runtime details."""
    if isinstance(exc, FileNotFoundError):
        return 'ファイルが見つかりません。「再読込」で一覧を更新してください。'
    if isinstance(exc, UnicodeError):
        return 'UTF-8のテキストとして読み込めません。元ファイルを確認してください。'
    if isinstance(exc, json.JSONDecodeError):
        return 'sample.jsonのJSON形式を確認してください。'
    if isinstance(exc, OSError):
        return 'ファイルを読み込めません。権限と保存状態を確認してください。'
    if isinstance(exc, ValueError):
        return str(exc)  # Only our fixed validation messages remain here.
    return '表示元の構成を読み込めません。sample.jsonとリンクを確認してください。'


def plain(text):
    text = re.sub(r'<a\b[^>]*>\s*</a>', '', text)
    text = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', text)
    return re.sub(r'[*`]', '', text).replace('\\\n', '\n').strip()


def bounded(root, relative):
    """Resolve only a named file inside one employee; reject traversal/escape."""
    if not isinstance(relative, str) or not relative or '\\' in relative or '\x00' in relative:
        raise ValueError('不正なファイル名です。')
    p = PurePosixPath(relative)
    if p.is_absolute() or '..' in p.parts:
        raise ValueError('社員フォルダの外は参照できません。')
    candidate = root.joinpath(*p.parts)
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise ValueError('社員フォルダの外へ向くリンクです。')
    return candidate


def regular(root, relative):
    p = bounded(root, relative)
    if not stat.S_ISREG(p.stat().st_mode):
        raise ValueError('通常のファイルではありません。')
    return p


def file_tree(root, relative):
    base = bounded(root, relative)
    if not base.is_dir():
        raise ValueError(f'{relative}フォルダが見つかりません。')
    paths = []
    # Never follow directory symlinks. All named entries are checked again before
    # reading, including symlinked files, so unrelated folders cannot be exposed.
    todo = [base]
    while todo:
        directory = todo.pop()
        for p in sorted(directory.iterdir()):
            name = str(p.relative_to(root))
            bounded(root, name)
            if p.is_symlink() and not p.exists():
                raise ValueError('参照先が存在しないリンクがあります。')
            if p.is_dir() and not p.is_symlink():
                todo.append(p)
            elif p.is_file() and p.name not in ('.DS_Store',):
                regular(root, name)
                paths.append(name)
    return sorted(paths)


def employee_root(kit, case):
    if case not in CASES:
        raise ValueError('この社員は登録されていません。')
    sample = kit / 'sample'
    root = sample / case
    if root.is_symlink() or not root.is_dir() or not root.resolve().is_relative_to(kit.resolve()):
        raise ValueError('社員フォルダが見つかりません。')
    return root


def manifest(kit, case):
    root = employee_root(kit, case)
    data = json.loads(regular(root, 'sample.json').read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('sample.jsonはJSONオブジェクトで指定してください。')
    if data.get('case') != case:
        raise ValueError('sample.jsonの社員名が一致しません。')
    run = data.get('latest_run')
    if not isinstance(run, dict) or not isinstance(run.get('output_sha256'), dict):
        raise ValueError('sample.jsonのlatest_runとoutput_sha256を確認してください。')
    run_id = run.get('id')
    if not isinstance(run_id, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', run_id):
        raise ValueError('最新実行の識別子が不正です。')
    outputs = list(run['output_sha256'])
    for name in outputs:
        if PurePosixPath(name).parent != PurePosixPath('outputs') / run_id:
            raise ValueError('最新成果の場所が一致しません。')
        bounded(root, name)
    return root, data, outputs


def allowed_files(kit, case):
    root, data, outputs = manifest(kit, case)
    groups = {
        'definition': ['AGENTS.md', 'CLAUDE.md'] + file_tree(root, '.claude/skills'),
        'interview': ['interview.md'],
        'inputs': file_tree(root, 'inputs'),
        'outputs': outputs,
        'reference': ['README.md', 'records/definition.md', 'sample.json', 'bundle-manifest.json'],
    }
    return root, data, groups


def source(kit, case, name):
    root, _, groups = allowed_files(kit, case)
    if name not in {p for group in groups.values() for p in group}:
        raise ValueError('このファイルは表示対象ではありません。')
    return regular(root, name)


def endpoint(kind, case, name):
    return f'/{kind}/{case}/{quote(name, safe="/")}'


def catalog(kit):
    people = []
    for case in CASES:
        try:
            root, data, groups = allowed_files(kit, case)
            agents = regular(root, 'AGENTS.md').read_text(encoding='utf-8')
            hearing = regular(root, 'interview.md').read_text(encoding='utf-8')
            heading = re.search(r'^#\s+(.+)', agents, re.M)
            title = plain(heading.group(1)).split(' — ')[0] if heading else case
            purpose_section = re.search(r'<a id="emp-001"></a>(.*?)<a id="emp-002"></a>', agents, re.S)
            purpose = plain(re.sub(r'^#+[^\n]*\n', '', purpose_section.group(1), flags=re.M)) if purpose_section else 'AGENTS.mdの全文で仕事内容を確認してください。'
            questions = []
            for part in re.split(r'^## ', hearing, flags=re.M)[1:]:
                q = re.search(r'\*\*問い：(.+?)\*\*', part)
                if q:
                    answer = part[q.end():].strip().split('\n\n', 1)[0]
                    questions.append({'question': plain(q.group(1)), 'answer': plain(answer)})
            files = []
            problems = [] if purpose_section else ['AGENTS.md: 仕事内容の見出し（EMP-001）を抽出できません。全文を参照してください。']
            for group, names in groups.items():
                for name in names:
                    try:
                        p = regular(root, name)
                        info = p.stat()
                        files.append({'path': name, 'group': group, 'name': p.name,
                                      'size': info.st_size, 'modified': info.st_mtime,
                                      'text': p.suffix.lower() in TEXT_TYPES,
                                      'source_url': endpoint('source', case, name),
                                      'download_url': endpoint('download', case, name),
                                      'preview_url': endpoint('preview', case, name) if group == 'outputs' and p.suffix == '.html' else None})
                    except (OSError, ValueError, RuntimeError) as exc:
                        problems.append(f'{name}: {public_error(exc)}')
            connections = []
            link_dir = bounded(root, '.agents/skills')
            if link_dir.is_dir():
                for p in sorted(link_dir.iterdir()):
                    if p.is_symlink():
                        bounded(root, str(p.relative_to(root)))
                        if not p.exists():
                            raise ValueError('Codex用Skillのリンク先が見つかりません。')
                        connections.append({'from': str(p.relative_to(root)), 'to': str(p.readlink())})
            people.append({'id': case, 'title': title, 'purpose': purpose, 'questions': questions,
                           'parameters': data['latest_run'].get('parameters', {}),
                           'run_id': data['latest_run']['id'], 'human_acceptance': data.get('human_acceptance', False),
                           'definition_version': data.get('definition_version'), 'files': files,
                           'connections': connections, 'problems': problems})
        except (OSError, ValueError, KeyError, TypeError, AttributeError, RuntimeError) as exc:
            people.append({'id': case, 'title': case, 'error': public_error(exc), 'files': [], 'questions': []})
    return {'employees': people, 'read_at': datetime.now(timezone.utc).isoformat()}


class Handler(BaseHTTPRequestHandler):
    server_version = 'EmployeeShowcase/1'

    def send_bytes(self, status, body, mime, *, policy=None, filename=None):
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('Content-Security-Policy', policy or "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'self'")
        if filename:
            self.send_header('Content-Disposition', "attachment; filename*=UTF-8''" + quote(filename, safe=''))
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)

    def json_response(self, data, status=200):
        self.send_bytes(status, json.dumps(data, ensure_ascii=False).encode(), 'application/json; charset=utf-8')

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        # Restrict local Host/Origin to reduce DNS-rebinding/cross-site access.
        port = self.server.server_port
        if self.headers.get('Host') not in (f'127.0.0.1:{port}', f'localhost:{port}'):
            self.json_response({'error': 'ローカル接続のみ利用できます。'}, 403)
            return
        origin = self.headers.get('Origin')
        if origin and origin not in (f'http://127.0.0.1:{port}', f'http://localhost:{port}'):
            self.json_response({'error': '別のページからは参照できません。'}, 403)
            return
        try:
            route = unquote(urlsplit(self.path).path)
            if route == '/favicon.ico':
                self.send_bytes(204, b'', 'image/x-icon')
            elif route in STATIC:
                p = ASSETS / STATIC[route]
                mime = {'.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript'}[p.suffix]
                self.send_bytes(200, p.read_bytes(), mime + '; charset=utf-8')
            elif route == '/api/catalog':
                self.json_response(catalog(self.server.kit))
            elif route.startswith(('/source/', '/preview/', '/download/')):
                _, kind, case, name = route.split('/', 3)
                p = source(self.server.kit, case, name)
                body = p.read_bytes()
                if kind == 'preview':
                    _, _, outputs = manifest(self.server.kit, case)
                    if name not in outputs or p.suffix != '.html':
                        raise ValueError('HTML成果物だけをプレビューできます。')
                    # Preserve report bytes. Let its local inline charts run,
                    # but deny network APIs/subresources, top navigation, forms
                    # and origin access. A report can still navigate itself.
                    self.send_bytes(200, body, 'text/html; charset=utf-8', policy="sandbox allow-scripts; default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; font-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'self'")
                elif kind == 'download':
                    self.send_bytes(200, body, 'application/octet-stream', filename=p.name)
                else:
                    if p.suffix.lower() not in TEXT_TYPES:
                        raise ValueError('この形式はダウンロードして確認してください。')
                    self.send_bytes(200, body, 'text/plain; charset=utf-8')
            else:
                self.json_response({'error': 'ページが見つかりません。'}, 404)
        except (BrokenPipeError, ConnectionResetError):
            pass  # Changing files/tabs can cancel a large response.
        except FileNotFoundError as exc:
            self.json_response({'error': public_error(exc)}, 404)
        except (ValueError, KeyError, TypeError, AttributeError, RuntimeError) as exc:
            self.json_response({'error': public_error(exc)}, 400)
        except OSError as exc:
            self.json_response({'error': public_error(exc)}, 500)


def make_server(kit, port=8765):
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.kit = Path(kit).resolve()
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--root', type=Path, default=ASSETS.parent, help='KIT root; default parent of dashboard/')
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error('port must be 0..65535')
    try:
        server = make_server(args.root, args.port)
    except OSError as exc:
        parser.exit(1, f'起動できません: {exc}\n別の --port を指定してください。\n')
    print(f'AI社員ラボ: http://127.0.0.1:{server.server_port}\n終了: Ctrl+C / 読み取り専用 / 外部接続不要', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
