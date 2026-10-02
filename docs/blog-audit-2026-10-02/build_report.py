"""Build the Chinese review deliverables from the checked findings; never edit notes."""
from pathlib import Path
from collections import Counter, defaultdict
from urllib.parse import urlparse, unquote
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = Path('C:/Project/blog')
catalog = json.loads((HERE / 'catalog.json').read_text(encoding='utf8'))
findings = json.loads((HERE / 'findings.json').read_text(encoding='utf8'))
probes = json.loads((HERE / 'probe-results.json').read_text(encoding='utf8'))
groups = defaultdict(list)
for finding in findings:
    groups[finding['article']].append(finding)
counts = Counter(x['category'] for x in findings)
priorities = Counter(x['priority'] for x in findings)

def mdtext(value):
    return value.replace('\\', '\\\\').replace('[', '\\[').replace(']', '\\]').replace('|', '\\|').replace('<', '&lt;').replace('>', '&gt;')

def filelink(label, path, line=None):
    target = Path(path).as_posix()
    if line is not None:
        target += f':{line}'
    return f'[{mdtext(label)}](<{target}>)'

def inline(value):
    value = value.strip()
    width = max([len(x) for x in re.findall(r'`+', value)] + [0]) + 1
    mark = '`' * width
    return f'{mark} {value} {mark}'

labels = {
    'docs.python.org': 'Python 官方文档',
    'peps.python.org': 'Python PEP',
    'requests.readthedocs.io': 'Requests 文档／源码',
    'docs.oracle.com': 'Oracle／Java 官方文档',
    'docs.spring.io': 'Spring 官方文档',
    'spring.io': 'Spring 官方说明',
    'jakarta.ee': 'Jakarta 规范',
    'nginx.org': 'NGINX 官方文档',
    'www.rfc-editor.org': 'RFC',
    'sqlite.org': 'SQLite 官方文档',
    'www.sqlite.org': 'SQLite 官方文档',
    'www.postgresql.org': 'PostgreSQL 官方文档',
    'dev.mysql.com': 'MySQL 官方文档',
    'redis.io': 'Redis 官方文档',
    'redis.readthedocs.io': 'redis-py 官方文档',
    'www.elastic.co': 'Elastic 官方文档',
    'www.gnu.org': 'GNU 官方手册',
    'man7.org': 'Linux／工具手册',
    'www.man7.org': 'Linux／工具手册',
    'man.openbsd.org': 'OpenBSD 官方手册',
    'manpages.debian.org': 'Debian 工具手册',
    'developer.mozilla.org': 'MDN 文档',
    'core.telegram.org': 'Telegram Bot API',
    'www.rabbitmq.com': 'RabbitMQ 官方文档',
    'flask.palletsprojects.com': 'Flask 官方文档',
    'werkzeug.palletsprojects.com': 'Werkzeug 官方文档',
    'fastapi.tiangolo.com': 'FastAPI 官方文档',
    'grafana.com': 'Grafana 官方文档',
    'prometheus.io': 'Prometheus 官方文档',
    'xlinux.nist.gov': 'NIST 算法与数据结构词典',
    'pages.nist.gov': 'NIST 指南',
    'www.nist.gov': 'NIST',
    'www.pi4j.com': 'Pi4J v1 源码',
    'www.raspberrypi.com': 'Raspberry Pi 官方文档',
    'www.who.int': 'WHO 资料',
    'www.npc.gov.cn': '全国人大：宪法',
    'www.unicode.org': 'Unicode 标准',
    'cheatsheetseries.owasp.org': 'OWASP 指南',
    'loggingsucks.com': '原作者文章',
    'how.complexsystems.fail': '原作者文章',
    'history.aip.org': '美国物理学会历史资料',
    'amturing.acm.org': 'ACM 图灵奖资料',
}

def source_label(url):
    u = urlparse(url)
    if u.netloc in ('github.com', 'raw.githubusercontent.com'):
        pieces = u.path.strip('/').split('/')
        return '仓库源码：' + '/'.join(pieces[:2]) + ' · ' + pieces[-1]
    last = unquote(u.path.rstrip('/').split('/')[-1])
    if u.netloc == 'www.rfc-editor.org':
        m = re.search(r'rfc(\d+)', u.path)
        return f'RFC {m.group(1)}' if m else 'RFC'
    base = labels.get(u.netloc, u.netloc)
    if last and last.lower() not in ('index.html', 'index.htm', 'index.rst', 'stable', 'latest', 'en', 'en-us'):
        base += ' · ' + last.removesuffix('.html')
    if u.fragment:
        base += ' · ' + unquote(u.fragment)
    return base

empty = {70, 92, 125, 146}
partial = {138: '只有两个项目名，尚未提供标题所说的完整 CLI 编写与发布流程。',
           161: '示例停在 DraftRepository，尚未提供前言预告的认证页面、CRUD 页面和部署流程。'}
ledger = []
for article in catalog:
    path = ROOT / article['path']
    content = path.read_text(encoding='utf-8-sig')
    assert len(content.splitlines()) == article['lines'], article['path']
    assert len(content) == article['chars'], article['path']
    title = re.search(r'^title:\s*(.*)$', content, re.M)
    date = re.search(r'^date:\s*(.*)$', content, re.M)
    title = title.group(1).strip().strip('"\'') if title else path.parent.name
    draft = bool(re.search(r'^draft:\s*true\s*$', content, re.M))
    items = groups[article['id']]
    status = '正文已核阅；有修改意见' if items else '正文已核阅；未发现可确认的明显错误'
    if article['id'] in empty:
        status = '空提纲／参考资料；无实质技术正文'
    elif article['id'] in partial:
        status = '内容未完成；现有文本已核阅'
    elif article['id'] == 1:
        status = '个人简介已阅；未发现可确认的明显字词错误'
    ledger.append({**article, 'title': title, 'date': date.group(1).strip() if date else '',
                   'draft': draft, 'review_status': status, 'finding_count': len(items),
                   'categories': dict(Counter(x['category'] for x in items)),
                   'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})

doc = []
def put(*lines):
    for line in lines:
        doc.extend(line.split('\n'))

put('# Blog 全文核查与修改意见', '', '核查日期：2026-10-02。原文目录：`C:/Project/blog`。', '',
    '已逐篇核阅目录内的 **175 个 Markdown 文件**（包括个人简介、草稿与未完成笔记），共约 **108 万字符、44,423 行**，字符数包含代码和 front matter。共整理 **320 条修改意见，涉及 138 个文件**。原文未修改；下文提供原文定位、问题说明、修改建议及相应依据。', '',
    '| 类型 | 条数 | 含义 |', '| --- | ---: | --- |',
    f'| 事实／技术错误 | {counts["事实/技术错误"]} | 明确的概念、数字、代码、命令或配置错误；也包含与正文矛盾的实现 |',
    f'| 条件／版本澄清 | {counts["条件/版本澄清"]} | 补充适用前提、历史版本或现行标准；不全部等于原文事实错误 |',
    f'| 字词／链接 | {counts["字词/链接"]} | 明显错字、名称拼写、误译和链接目标错误 |', '',
    '条数按“修改意见组”统计：一条可合并同篇重复错字或相同成因的问题；跨篇重复问题分别定位。混合问题按主要技术含义归类。因此，320 不是独立错误单词的总数。', '',
    '## 如何阅读与核查边界', '',
    'P1 为建议优先修改的事项，可能造成错误实验结论、消息丢失、更新失败、递归告警或错误安全判断；P2 为其他技术修正与条件说明；P3 为字词和链接修正。这是修订顺序建议。', '',
    '逐篇清单列出全部文件，包含没有发现问题的文章，便于检查遗漏：' + filelink('175 个文件的核查清单', HERE / 'article-checklist.md') + '。', '',
    '依据优先采用协议规范、项目官方文档、官方源码、作者原始资料和工具手册。历史教程按其使用版本判断；仅因今天有新版本，不直接判旧笔记错误。译文中的错误若原作者也有，会在具体条目中说明，并建议加译者注。字词、算术和同篇代码／配置矛盾可直接由原文核对。', '',
    '**覆盖范围：**Markdown 正文、front matter、文本形式的命令和代码均已核阅。代码以静态检查为主，争议行为另做针对性验证；未在所有硬件、Linux 发行版、Java 和服务部署环境完整复现，配图和截图也未逐张 OCR。因此，“未发现可确认的明显错误”不表示所有运行结果、图片数据或私人经历均已独立验证。个人感受、设计偏好及缺少外部证据的经历不作事实性否定。', '',
    '**来源读取边界：**部分历史网页抓取受限，核查时使用对应官方手册、版本源码或搜索可取得的材料补证。报告引用链接供复查；来源访问记录保留成功与失败，不把无法抓取等同于链接已失效。', '',
    '## 建议优先修改的例子', '',
    '| 条目 | 需要修改的核心问题 |', '| --- | --- |')
highlights = {
    'R046': 'MySQL 备份脚本不能保证恢复到指定新库，且转储失败仍可能淘汰旧备份。',
    'R061': 'Redis pipeline 性能测试没有排入 GET 命令，原耗时与性能结论需要撤回并重测。',
    'R025': '直接截断序列化后的 JSON，可能产生无法解析的日志，且未控制 UTF-8 字节数。',
    'R216': '告警发送失败后再用同一个告警 logger 记录异常，会递归提交告警。',
    'R241': 'RabbitMQ 的 Future 完成不代表处理成功；失败也 ACK 会丢失可重试消息。',
    'R249': '同源策略不能作为 CSRF 防御；跨源请求并不都被阻止。',
    'R262': '更新器没有核实下载完整性；截断的文件也可能进入替换流程。',
    'R263': '更新器先删除旧 EXE，后续移动失败时可能失去可运行版本。',
    'R270': 'X-Forwarded-For 可能是代理链，不能直接当作一个可信 IP 查询。',
    'R282': '密码哈希、TLS 加密和日志脱敏需要区分；日志应省略密码。',
}
for fid, description in highlights.items():
    put(f'| [{fid}](#{fid.lower()}) | {description} |')
put('', '## 逐篇修改意见', '')
article_lines = {}
finding_lines = {}
for article in ledger:
    a = article['id']
    article_lines[a] = len(doc) + 1
    put(f'### A{a:03d}', '', '**' + mdtext(article['title']) + '**', '',
        '原文：' + filelink(article['path'], ROOT / article['path']) + '。', '',
        f'记录日期：{article["date"] or "未标注"}；状态：' + ('草稿；' if article['draft'] else '') + article['review_status'] + '。', '')
    if a in empty:
        put('只有提纲、前言标题或参考链接，缺少可核实的技术正文。本轮不把这种空提纲计作内容正确的技术文章。', '')
    elif a in partial:
        put(partial[a], '')
    if not groups[a]:
        if a not in empty:
            put('本轮未发现可确认的明显事实、代码或字词错误。此结论受上文核查范围限制。', '')
        continue
    for x in groups[a]:
        finding_lines[x['id']] = len(doc) + 1
        put(f'#### {x["id"]}', '', f'**{x["category"]} · {x["type"]} · {x["priority"]}**', '',
            '定位：' + filelink(f'原文第 {x["line"]} 行', ROOT / x['path'], x['line']) + '；待改表述／主题：' + inline(x['quote']) + '。', '')
        original = x['actual_line'].strip()
        # Avoid duplicating credential values in a review excerpt.
        sensitive = bool(re.search(r'password|passwd|secret|api[_-]?key|wlan\.connect|access[_-]?key', original, re.I))
        if original and not sensitive:
            excerpt = original[:240] + ('…' if len(original) > 240 else '')
            put('原文定位行（节选）：' + inline(excerpt), '')
        put('问题：' + x['problem'], '', '建议修改：' + x['suggestion'], '')
        if x['sources']:
            sources = '；'.join('[' + mdtext(source_label(url)) + '](' + url + ')' for url in x['sources'])
            put('依据：' + sources + '。', '')
        else:
            put('依据：原文文字、算术或同篇代码／配置对照；不涉及需外部确认的新增事实。', '')

passed = sum(x.get('passed') is True for x in probes['results'])
skipped = sum('skipped' in x for x in probes['results'])
put('## 验证与复核记录', '',
    f'本地针对性验证 **{passed} 项通过、{skipped} 项跳过**。环境为 Python 3.13.5、SQLite {probes["sqlite"]}；验证了 SQLite NULL 主键及自增元数据、logging 过滤与 QueueHandler 行为、JSON 截断、导入语法、Future 失败结果、更新器参数检查、搜索参数编码和截断 HTTP 响应读取等。', '',
    '本地未安装 Requests，因此对应本地探针跳过；`raise_for_status()` 和异常多继承关系改由 Requests 官方源码核对。探针验证的是具体行为，不能代替整篇示例的端到端运行。结果：' + filelink('probe-results.json', HERE / 'probe-results.json') + '。', '',
    '复核撤回了以下候选，未计入 320 条意见：', '',
    '- SQLite CLI 接受 `.headers` 的无歧义前缀 `.header`，不能判为无效命令。',
    '- 防火墙教程已展示 `--permanent` 和 reload，不能概括成文章所有运行时修改均不生效。',
    '- SHA-512 与 SHA-256 的性能受实现和硬件影响，缺少对照数据的速度判断未列为确认错误。',
    '- BusyBox 恢复 rpm 的文章是特定静态构建的个人实践，已给出静态前提，不能凭工具功能边界否定该经历。', '',
    'Redis 大偏移分页的候选也未列入：原文实际使用 score 范围分页，偏移扫描成本的说明成立。', '',
    '便于后续逐条修订的结构化清单：' + filelink('findings.json', HERE / 'findings.json') + '；覆盖、状态和原文 SHA-256 快照：' + filelink('coverage.json', HERE / 'coverage.json') + '。', '',
    '原文 Git HEAD：`882620b614f45d2873a372926993120cee6e663f`。交付前检查原文工作树无改动。行号以此次本地快照为准；今后修改原文后应重新定位。', '')
report = '\n'.join(doc)
(HERE / 'REPORT.md').write_text(report, encoding='utf8')

check = ['# Blog 逐篇核查清单', '',
         '范围：`C:/Project/blog` 中全部 175 个 Markdown 文件；核查日期：2026-10-02。正文已阅包含静态代码检查，不代表所有环境均已复现；图片未逐张 OCR。', '',
         '完整理由、修改建议和来源见 ' + filelink('REPORT.md', HERE / 'REPORT.md') + '。标注草稿仍纳入核查；无实质正文的提纲单列。', '',
         '| 编号 | 文章／文件 | 状态 | 事实／技术 | 条件／版本 | 字词／链接 | 详细意见 |',
         '| --- | --- | --- | ---: | ---: | ---: | --- |']
for article in ledger:
    a = article['id']
    label = article['title'] + '（' + article['path'].removesuffix('/index.md') + '）'
    category = article['categories']
    status = ('草稿；' if article['draft'] else '') + article['review_status']
    check.append(f'| A{a:03d} | ' + filelink(label, ROOT / article['path']) + ' | ' + status +
                 f' | {category.get("事实/技术错误", 0)} | {category.get("条件/版本澄清", 0)} | {category.get("字词/链接", 0)} | ' +
                 filelink(f'{article["finding_count"]} 条／状态说明', HERE / 'REPORT.md', article_lines[a]) + ' |')
check.extend(['', f'合计：175 个文件；138 个文件有修改意见；{len(findings)} 条意见。', ''])
(HERE / 'article-checklist.md').write_text('\n'.join(check), encoding='utf8')
for article in ledger:
    article['report_line'] = article_lines[article['id']]
coverage = {
    'review_date': '2026-10-02', 'root': ROOT.as_posix(),
    'git_head': '882620b614f45d2873a372926993120cee6e663f',
    'scope': '全部Markdown文本及代码静态核阅；争议行为针对性验证；未完整复现全部环境，未逐图OCR',
    'total_files': len(ledger), 'total_chars_including_code_and_frontmatter': sum(x['chars'] for x in ledger),
    'total_lines': sum(x['lines'] for x in ledger), 'total_findings': len(findings),
    'categories': dict(counts), 'priorities': dict(priorities),
    'local_probes': {'passed': passed, 'skipped': skipped}, 'articles': ledger,
    'finding_report_lines': finding_lines,
}
(HERE / 'coverage.json').write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding='utf8')
urls = sorted(set(url for x in findings for url in x['sources']))
(HERE / 'source-urls.json').write_text(json.dumps(urls, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps({'files': len(ledger), 'findings': len(findings), 'categories': dict(counts),
                  'report_chars': len(report), 'sources_distinct_urls': len(urls),
                  'probes_passed': passed, 'probes_skipped': skipped}, ensure_ascii=False))
