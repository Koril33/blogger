"""Check coverage, finding anchors, source records and the unchanged note snapshot."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = Path('C:/Project/blog')
coverage = json.loads((HERE / 'coverage.json').read_text(encoding='utf8'))
findings = json.loads((HERE / 'findings.json').read_text(encoding='utf8'))
source_checks = json.loads((HERE / 'source-checks.json').read_text(encoding='utf8'))
report = (HERE / 'REPORT.md').read_text(encoding='utf8')
checklist = (HERE / 'article-checklist.md').read_text(encoding='utf8')
lines = report.splitlines()
assert re.findall(r'^### A(\d{3})$', report, re.M) == [f'{i:03}' for i in range(1, 176)]
assert re.findall(r'^#### (R\d{3})$', report, re.M) == [f'R{i:03}' for i in range(1, 321)]
assert len(re.findall(r'^\| A\d{3} \|', checklist, re.M)) == 175
assert sum(x['finding_count'] for x in coverage['articles']) == 320
assert len([x for x in coverage['articles'] if x['finding_count']]) == 138
files = sorted(ROOT.rglob('*.md'), key=lambda x: str(x.relative_to(ROOT)).casefold())
assert [x.relative_to(ROOT).as_posix() for x in files] == [x['path'] for x in coverage['articles']]
for article in coverage['articles']:
    assert lines[article['report_line'] - 1] == f"### A{article['id']:03}"
    assert hashlib.sha256((ROOT / article['path']).read_bytes()).hexdigest() == article['sha256']
for finding in findings:
    original = (ROOT / finding['path']).read_text(encoding='utf8').splitlines()
    assert original[finding['line'] - 1] == finding['actual_line'], finding['id']
    assert lines[coverage['finding_report_lines'][finding['id']] - 1] == f"#### {finding['id']}"
    assert all(url.startswith('https://') for url in finding['sources'])
    assert f"](<C:/Project/blog/{finding['path']}:{finding['line']}>)" in report
canonical = lambda url: url.split('#')[0]
recorded = {canonical(x['url']) for x in source_checks}
cited = {canonical(url) for x in findings for url in x['sources']}
assert cited <= recorded, sorted(cited - recorded)
# All table headers and separator rows must have the same number of cells.
for document in (report, checklist):
    doclines = document.splitlines()
    for n, line in enumerate(doclines):
        if re.match(r'^\|(?:\s*:?-+:?\s*\|)+$', line):
            assert line.count('|') == doclines[n - 1].count('|'), n
status = subprocess.run(['git', '-c', 'safe.directory=C:/Project/blog', '-C', ROOT.as_posix(),
                         'status', '--short'], capture_output=True, text=True, check=True).stdout
head = subprocess.run(['git', '-c', 'safe.directory=C:/Project/blog', '-C', ROOT.as_posix(),
                       'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
assert not status, status
assert head == coverage['git_head']
result = {'validated': True, 'markdown_files': 175, 'findings': 320, 'articles_with_findings': 138,
          'all_original_line_anchors_match': True, 'all_report_line_links_match': True,
          'all_original_sha256_match': True, 'all_cited_pages_have_access_records': True,
          'source_pages_distinct_excluding_fragments': len(cited),
          'original_git_worktree_clean': True, 'original_git_head': head,
          'report_lines': len(lines), 'checklist_rows': 175}
(HERE / 'validation-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps(result, ensure_ascii=False))
