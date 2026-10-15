"""Verify saved reference samples; this does not run an AI or accept its work."""
from pathlib import Path
import csv
import hashlib
import json
import re
from html.parser import HTMLParser
from html import unescape


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pointer(document, location):
    value = document
    for key in location.lstrip('/').split('/'):
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def minutes_checks(d, e, source, markdown):
    tasks = {x['id']: x for x in d['tasks']}
    expected_ids = {f'M{i:02}' for i in range(1, 8)}
    lines = source.read_text().splitlines()
    checks = {
        'meeting_id': d['meeting_id'] == e['meeting_id'],
        'meeting_date': d['summary']['meeting_date'] == e['date'],
        'decision_only_M02': len(d['decisions']) == 1 and d['decisions'][0]['source_ids'] == ['M02'],
        'decision_facts': all(x in d['decisions'][0]['text'] for x in e['decisions']),
        'proposal_only_M04': len(d['proposals']) == 1 and d['proposals'][0]['source_ids'] == e['proposal_source_ids'],
        'proposal_not_decision': '決定はしていない' in d['proposals'][0]['text'],
        'task_ids': len(tasks) == len(d['tasks']) == 2 and set(tasks) == set(e['actions']),
        'all_source_ids': set(d['source_index']) == expected_ids,
        'original_lines': all(x['raw_text'] == lines[x['line_number'] - 1] and x['raw_text'].startswith('[' + key + ']') for key, x in d['source_index'].items()),
        'source_targets': all(item['id'] == pointer(d, item['json_pointer'])['id'] and key in pointer(d, item['json_pointer'])['source_ids'] for key, x in d['source_index'].items() for item in x['output_items']),
        'next_meeting_unknown': [x['value'] for x in d['undecided'] if x['kind'] == 'next_meeting_date'] == [e['next_meeting_date']],
        'human_acceptance_false': d['human_acceptance'] is False,
        'input_hash': sha(source) == d['input']['sha256'] == d['input']['sha256_after'],
    }
    for key, expected in e['actions'].items():
        actual = tasks[key]
        checks[key + '_facts'] = all(actual[field] == expected[field] for field in ['owner', 'deadline', 'source_ids'])
        if 'deadline_candidates' in expected:
            checks[key + '_candidates'] = [x['value'] for x in actual['deadline_candidates']] == expected['deadline_candidates']
    checks['candidate_sources'] = tasks['A01']['deadline_candidates'] == [
        {'value': '2026-10-20', 'source_ids': ['M03']},
        {'value': '2026-10-22', 'source_ids': ['M06']},
    ]
    rows = {line.split('|')[1].strip(): [x.strip() for x in line.split('|')[1:-1]] for line in markdown.splitlines() if re.match(r'\| A0[12] \|', line)}
    checks['markdown_task_values'] = all(rows[key][2] == ('null' if task['owner'] is None else task['owner']) and rows[key][4] == ('null' if task['deadline'] is None else task['deadline']) for key, task in tasks.items())
    checks['markdown_unknown_next_date'] = any('| next_meeting_date | null |' in line for line in markdown.splitlines())
    checks['markdown_decision_and_proposal'] = all(x['text'] in markdown for x in d['decisions'] + d['proposals'])
    checks['markdown_source_coverage'] = all('[' + key + ']' in markdown for key in expected_ids)
    return checks


def sales_checks(d, e, source, html):
    counts = d['row_counts']
    actual = {
        'period': [d['start_date'], d['end_date']],
        'input_rows': counts['input_data_rows'],
        'period_rows': counts['accepted'] + counts['pending_quantity'],
        'included_rows': counts['accepted'],
        'unresolved_rows': sorted(x['sale_id'] for x in d['trace'] if x['classification'] == 'pending_quantity'),
        'out_of_period': sorted(x['sale_id'] for x in d['trace'] if x['classification'] == 'outside_period'),
        'known_subtotal_jpy': d['known_totals']['amount_jpy'],
        'included_quantity': d['known_totals']['quantity'],
        'by_product_jpy': {x['product']: x['amount_jpy'] for x in d['by_product']},
        'by_date_jpy': {x['date']: x['amount_jpy'] for x in d['by_date']},
        'by_channel_jpy': {x['channel']: x['amount_jpy'] for x in d['by_channel']},
        'line_amounts_jpy': {x['sale_id']: x['amount_jpy'] for x in d['trace'] if x['classification'] == 'accepted'},
        'total_is_provisional': d['is_provisional'],
    }
    checks = {key: value == e[key] for key, value in actual.items()}
    with source.open(newline='') as handle:
        original = list(csv.DictReader(handle))
    checks['original_rows'] = len(original) == len(d['trace']) and all(t['original'] == row and t['physical_line_start'] == i + 2 and t['physical_line_end'] == i + 2 for i, (t, row) in enumerate(zip(d['trace'], original)))
    missing = [x for x in d['trace'] if x['sale_id'] == 'S006'][0]
    checks['unknown_is_not_zero'] = missing['quantity'] is None and missing['amount_jpy'] is None and missing['original']['quantity'] == ''
    checks['source_hash'] = sha(source) == e['source_sha256']
    checks['human_acceptance_false'] = d['human_acceptance'] is False

    class Scan(HTMLParser):
        def __init__(self):
            super().__init__()
            self.tags, self.attrs = [], []

        def handle_starttag(self, tag, attrs):
            self.tags.append(tag)
            self.attrs.extend(attrs)

    scan = Scan()
    scan.feed(html)
    checks['three_svg_graphs'] = scan.tags.count('svg') == 3
    checks['no_active_or_embedded_tags'] = not set(scan.tags) & {'script', 'iframe', 'object', 'embed', 'link', 'img'}
    checks['no_event_handlers'] = not any(k.lower().startswith('on') for k, _ in scan.attrs)
    checks['no_remote_resources'] = not any(k in {'src', 'href'} and v and v.startswith(('http:', 'https:', '//', 'data:')) for k, v in scan.attrs)
    checks['html_critical_values'] = ('9,150' in html or '9150' in html) and '暫定' in html and all(row['sale_id'] in html for row in original)
    return checks


def product_checks(d, e, source, markdown):
    original = json.loads(source.read_text())
    actual = {x['sku']: x for x in d['products']}
    expected = {x['sku']: x for x in e['products']}
    decoded_markdown = unescape(markdown)
    checks = {
        'input_matches_heldout': original == e,
        'dataset_id': d['dataset_id'] == e['dataset_id'],
        'fictional': d['fictional'] is e['fictional'] is True,
        'all_products_once': len(actual) == len(d['products']) == len(expected) and set(actual) == set(expected),
        'input_hash': sha(source) == d['input_sha256'],
        'human_acceptance_false': d['human_acceptance'] is False,
        'no_excluded_products': d['excluded_products'] == [],
    }
    for sku, item in actual.items():
        index = next(i for i, product in enumerate(original['products']) if product['sku'] == sku)
        prefix = f'/products/{index}/'
        checks[sku + '_original_facts'] = all(item[key] == value and type(item[key]) is type(value) for key, value in expected[sku].items())
        checks[sku + '_field_references'] = all(item[key] == pointer(original, location) and location == prefix + key for key, location in item['field_sources'].items())
        claims = item['claim_sources']
        checks[sku + '_claim_coverage'] = 1 <= len(claims) <= 2 and ''.join(x['claim'] for x in claims) == item['introduction']
        checks[sku + '_claim_references'] = all(x['sources'] and all(location.startswith((prefix + 'content', prefix + 'features/')) and isinstance(pointer(original, location), str) for location in x['sources']) for x in claims)
        checks[sku + '_markdown_values'] = all(value in decoded_markdown for value in [item['name'], item['content'], item['introduction'], *item['features'], *item['unknowns']])
        expected_price = '価格未定・要確認' if item['price_jpy'] is None else str(item['price_jpy']) + '円'
        checks[sku + '_price_display'] = item['price_display'] == expected_price and f'| 価格 | {expected_price} | {prefix}price_jpy |' in decoded_markdown
    checks['markdown_validation_table'] = all(f"| {x['label']} | {x['result']} | {x['detail']} |" in decoded_markdown for x in d['validation']['checks'])
    return checks


def main():
    root = Path(__file__).resolve().parents[1]
    results = {}
    for case in ['sales', 'minutes', 'product']:
        base = root / 'sample' / case
        report = json.loads((base / 'output/report.json').read_text())
        expected = json.loads((base / 'expected.json').read_text())
        provenance = json.loads((base / 'provenance.json').read_text())
        source = list((base / 'input').iterdir())
        if len(source) != 1:
            raise ValueError(f'{case}: expected exactly one fixture')
        suffix = 'html' if case == 'sales' else 'md'
        rendered = (base / ('output/report.' + suffix)).read_text()
        checks = globals()[case + '_checks'](report, expected, source[0], rendered)
        recorded_files = provenance['public_files_sha256']
        actual_files = {str(f.relative_to(base)) for f in base.rglob('*') if f.is_file() and f.name != 'provenance.json'}
        checks['manifest_coverage'] = set(recorded_files) == actual_files
        checks['public_file_hashes'] = all(sha(base / name) == digest for name, digest in recorded_files.items())
        checks['original_report_identity'] = report['public_export']['original_report_sha256'] == provenance['original_files']['output/report.json']['sha256']
        checks['reference_only'] = provenance['publication_form'] == 'inert_reference_sample' and report['public_export']['business_rerun'] is False
        checks['no_human_acceptance_claim'] = provenance['human_acceptance'] is False and provenance['human_definition_review'] is False
        checks['recorded_independent_result'] = json.loads((base / 'validation/result.json').read_text())['all_passed'] is True
        results[case] = {'passed': all(checks.values()), 'checks': checks}
    print(json.dumps({'saved_samples_only': True, 'human_acceptance': False, 'results': results}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(x['passed'] for x in results.values()) else 1)


if __name__ == '__main__':
    main()
