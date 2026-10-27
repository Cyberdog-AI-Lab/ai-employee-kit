"""Local HTTP regressions: real files, refresh, missing inputs, and read boundaries."""
import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.parse import quote

import serve


class DashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='employee-dashboard-')
        cls.root = Path(cls.temp.name)
        for case in serve.CASES:
            root = cls.root / 'sample' / case
            for d in ('inputs', 'outputs/run-001', '.claude/skills/work-001', '.agents/skills', 'records'):
                (root/d).mkdir(parents=True, exist_ok=True)
            (root/'AGENTS.md').write_text('# Test employee\n<a id="emp-001"></a>\n## Purpose\nRead only.\n<a id="emp-002"></a>\n')
            (root/'interview.md').write_text('# Hearing\n## Work\n**問い：What?**\n\nFictional data.\n')
            for n in ('CLAUDE.md', 'README.md', 'records/definition.md', '.claude/skills/work-001/SKILL.md'):
                (root/n).write_text('Fixture only.\n')
            (root/'.agents/skills/work-001').symlink_to('../../.claude/skills/work-001')
            (root/'inputs/a.csv').write_text('id,value\nA,1\n')
            (root/'inputs/quoted.md').write_text('<script>window.untrusted = true</script>\n')
            (root/'outputs/run-001/report.html').write_text('<!doctype html><script>document.body.dataset.ready="yes"</script>')
            (root/'outputs/run-001/report.json').write_text('{"run_id":"run-001"}')
            (root/'bundle-manifest.json').write_text('{}')
            (root/'sample.json').write_text(json.dumps({'case':case,'latest_run':{'id':'run-001','parameters':{'input_dir':'inputs'},'output_sha256':{f'outputs/run-001/report.{ext}':'hash' for ext in ('html','json')}}}))
        cls.server = serve.make_server(cls.root, 0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join(); cls.temp.cleanup()

    def request(self, path, method='GET', headers=None):
        conn = http.client.HTTPConnection('127.0.0.1', self.server.server_port)
        conn.request(method, path, headers=headers or {})
        response = conn.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        conn.close()
        return result

    def test_summary_preserves_literal_parameter_placeholders(self):
        self.assertEqual(serve.plain('`outputs/<新しいrun-id>/`'), 'outputs/<新しいrun-id>/')
        self.assertEqual(serve.plain('<a id="section"></a>本文'), '本文')

    def test_three_employees_and_real_files(self):
        code, _, body = self.request('/api/catalog')
        self.assertEqual(code,200)
        people=json.loads(body)['employees']
        self.assertEqual([p['id'] for p in people],list(serve.CASES))
        self.assertEqual(people[0]['purpose'],'Read only.')
        self.assertEqual(people[0]['questions'][0]['answer'],'Fictional data.')
        self.assertTrue(all(not p['problems'] for p in people))

    def test_every_advertised_source_matches_original_bytes(self):
        for person in serve.catalog(self.root)['employees']:
            for entry in person['files']:
                with self.subTest(file=entry['path']):
                    code, headers, body=self.request(entry['source_url'])
                    self.assertEqual(code,200)
                    self.assertEqual(body,(self.root/'sample'/person['id']/entry['path']).read_bytes())
                    self.assertEqual(headers['Content-Type'],'text/plain; charset=utf-8')

    def test_html_preview_is_exact_and_sandboxed(self):
        code,headers,body=self.request('/preview/sales/outputs/run-001/report.html')
        self.assertEqual(code,200)
        self.assertEqual(body,(self.root/'sample/sales/outputs/run-001/report.html').read_bytes())
        self.assertIn('sandbox allow-scripts;',headers['Content-Security-Policy'])
        self.assertIn("connect-src 'none'",headers['Content-Security-Policy'])
        self.assertNotIn('allow-same-origin',headers['Content-Security-Policy'])

    def test_preview_does_not_execute_input_html(self):
        self.assertEqual(self.request('/preview/sales/inputs/quoted.md')[0],400)

    def test_raw_html_is_plain_text_and_not_sniffed(self):
        _,headers,body=self.request('/source/sales/inputs/quoted.md')
        self.assertEqual(headers['X-Content-Type-Options'],'nosniff')
        self.assertTrue(headers['Content-Type'].startswith('text/plain'))
        self.assertIn(b'<script>',body)

    def test_file_change_is_visible_without_build(self):
        p=self.root/'sample/sales/inputs/new.csv';p.write_text('new\n')
        try:
            paths=[f['path'] for f in serve.catalog(self.root)['employees'][0]['files']]
            self.assertIn('inputs/new.csv',paths)
            p.write_text('updated\n')
            self.assertEqual(self.request('/source/sales/inputs/new.csv')[2],b'updated\n')
        finally:p.unlink()

    def test_latest_outputs_follow_manifest_not_filename_guess(self):
        root=self.root/'sample/sales';p=root/'sample.json';before=p.read_bytes()
        later=root/'outputs/run-002';later.mkdir();(later/'report.html').write_text('new report')
        try:
            data=json.loads(before);data['latest_run']={'id':'run-002','output_sha256':{'outputs/run-002/report.html':'hash'}};p.write_text(json.dumps(data))
            output=[f for f in serve.catalog(self.root)['employees'][0]['files'] if f['group']=='outputs']
            self.assertEqual([f['path'] for f in output],['outputs/run-002/report.html'])
            self.assertEqual(self.request('/source/sales/outputs/run-001/report.html')[0],400)
        finally:p.write_bytes(before);(later/'report.html').unlink();later.rmdir()

    def test_missing_output_has_visible_catalog_problem(self):
        p=self.root/'sample/sales/outputs/run-001/report.json';before=p.read_bytes();p.unlink()
        try:
            person=serve.catalog(self.root)['employees'][0]
            self.assertTrue(any('report.json' in x for x in person['problems']))
            self.assertEqual(self.request('/source/sales/outputs/run-001/report.json')[0],404)
        finally:p.write_bytes(before)

    def test_invalid_case_is_rejected(self):
        self.assertEqual(self.request('/source/private/AGENTS.md')[0],400)

    def test_error_messages_do_not_project_absolute_paths(self):
        p=self.root/'sample/sales/AGENTS.md';before=p.read_bytes();p.unlink()
        try:
            person=serve.catalog(self.root)['employees'][0]
            self.assertIn('見つかりません',person['error'])
            self.assertNotIn(str(self.root),json.dumps(person))
        finally:p.write_bytes(before)
        for exc in (PermissionError(13,'Denied','/Users/private/name'),RuntimeError('loop at /Users/private/name')):
            self.assertNotIn('/Users/',serve.public_error(exc))

    def test_malformed_manifest_returns_clear_error_without_connection_drop(self):
        p=self.root/'sample/sales/sample.json';before=p.read_bytes()
        try:
            for data in ([],None,{'case':'sales','latest_run':[]},{'case':'sales','latest_run':{'id':'run-001','output_sha256':[]}}):
                p.write_text(json.dumps(data))
                self.assertIn('error',serve.catalog(self.root)['employees'][0])
                code,_,body=self.request('/source/sales/AGENTS.md')
                self.assertEqual(code,400)
                self.assertIn('error',json.loads(body))
        finally:p.write_bytes(before)

    def test_missing_purpose_anchors_do_not_expose_whole_agents_as_summary(self):
        p=self.root/'sample/sales/AGENTS.md';before=p.read_bytes()
        try:
            p.write_text('# Test employee\nFull instructions must stay in source view.\n')
            person=serve.catalog(self.root)['employees'][0]
            self.assertNotIn('Full instructions',person['purpose'])
            self.assertTrue(person['problems'])
            self.assertTrue(person['files'])
        finally:p.write_bytes(before)

    def test_missing_input_directory_and_broken_links_are_visible(self):
        p=self.root/'sample/sales/inputs';moved=p.with_name('inputs-parked');p.rename(moved)
        try:self.assertIn('inputs',serve.catalog(self.root)['employees'][0]['error'])
        finally:moved.rename(p)
        broken=p/'broken.txt';broken.symlink_to('missing.txt')
        try:self.assertIn('リンク',serve.catalog(self.root)['employees'][0]['error'])
        finally:broken.unlink()

    def test_codex_symlink_escape_is_not_served(self):
        p=self.root/'sample/sales/.agents/skills/outside';p.symlink_to(self.root)
        try:
            self.assertIn('error',serve.catalog(self.root)['employees'][0])
        finally:p.unlink()

    def test_path_traversal_and_backslash_are_rejected(self):
        for path in ('../../AGENTS.md','../minutes/AGENTS.md','%2e%2e/%2e%2e/AGENTS.md','inputs%5ca.csv','%00'):
            with self.subTest(path=path):self.assertEqual(self.request('/source/sales/'+path)[0],400)

    def test_unlisted_private_file_is_not_served(self):
        p=self.root/'sample/sales/private.txt';p.write_text('must not be served')
        try:self.assertEqual(self.request('/source/sales/private.txt')[0],400)
        finally:p.unlink()

    def test_symlink_escape_rejected(self):
        outside=self.root/'outside.txt';outside.write_text('private')
        p=self.root/'sample/sales/inputs/escape.txt';p.symlink_to(outside)
        try:
            self.assertIn('error',serve.catalog(self.root)['employees'][0])
            self.assertEqual(self.request('/source/sales/inputs/escape.txt')[0],400)
        finally:p.unlink();outside.unlink()

    def test_only_loopback_host_and_same_origin(self):
        self.assertEqual(self.request('/api/catalog',headers={'Host':'attacker.invalid'})[0],403)
        self.assertEqual(self.request('/api/catalog',headers={'Origin':'https://attacker.invalid'})[0],403)

    def test_download_is_exact_attachment(self):
        code,headers,body=self.request('/download/sales/inputs/a.csv')
        self.assertEqual(code,200)
        self.assertIn('attachment;',headers['Content-Disposition'])
        self.assertEqual(body,b'id,value\nA,1\n')

    def test_head_has_no_body_and_same_length(self):
        _,headers,body=self.request('/source/sales/inputs/a.csv','HEAD')
        self.assertEqual(body,b'');self.assertEqual(int(headers['Content-Length']),len(b'id,value\nA,1\n'))

    def test_no_write_endpoint(self):
        self.assertEqual(self.request('/source/sales/inputs/a.csv','POST')[0],501)
        self.assertEqual((self.root/'sample/sales/inputs/a.csv').read_text(),'id,value\nA,1\n')

    def test_no_repo_directory_listing(self):
        for path in ('/sample/','/.git/config','/docs/seminar/','/serve.py'):
            self.assertEqual(self.request(path)[0],404)

    def test_static_ui_is_local_and_has_restrictive_policy(self):
        for path in ('/','/app.js','/styles.css','/source-pages.js','/markdown-view.js','/vendor/markdown-it.min.js'):
            code,headers,_=self.request(path)
            self.assertEqual(code,200)
            self.assertIn("connect-src 'self'",headers['Content-Security-Policy'])
        js=(serve.ASSETS/'app.js').read_text()
        self.assertNotIn('innerHTML',js)
        self.assertNotIn('insertAdjacentHTML',js)


if __name__=='__main__':
    unittest.main(verbosity=2)
