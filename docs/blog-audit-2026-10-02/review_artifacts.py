from pathlib import Path
import json,re,ast,difflib
HERE=Path(__file__).parent
ROOT=Path('C:/Project/blog')
CAT=json.loads((HERE/'catalog.json').read_text(encoding='utf8'))
FILES=sorted(ROOT.rglob('*.md'),key=lambda p:str(p.relative_to(ROOT)).casefold())
def norm(s): return re.sub(r'[^\w\u4e00-\u9fff]+','',s).lower()
fs=[dict(x) for f in sorted(HERE.glob('findings-*.json')) for x in json.loads(f.read_text(encoding='utf8'))]
for idx,x in enumerate(fs,1):
    x['draft_id']=idx
    lines=FILES[x['article']-1].read_text(encoding='utf8').splitlines()
    hint=x['line']
    segments=[norm(s) for s in re.split(r'[…；/]|\.\.\.',x['quote']) if len(norm(s))>=3]
    candidates=[]
    for i,line in enumerate(lines,1):
        n=norm(line)
        if not n or line.startswith(('![','http','date:','title:')): continue
        matched=[s for s in segments if s in n]
        if matched:
            strength=max(min(len(s),30)/30 for s in matched)
            candidates.append((strength-abs(i-hint)*0.0008,i))
    if candidates:
        x['line']=max(candidates)[1]
    x['actual_line']=lines[x['line']-1] if x['line']<=len(lines) else ''
    x['line_changed']=x['line']!=hint
    x['hint_line']=hint
(HERE/'reviewed-draft.json').write_text(json.dumps(fs,ensure_ascii=False,indent=2),encoding='utf8')
for x in fs:
    if x['line_changed'] or not any(s in norm(x['actual_line']) for s in [norm(v) for v in re.split(r'[…；/]|\.\.\.',x['quote']) if len(norm(v))>=3]):
        print(f"D{x['draft_id']:03} A{x['article']:03} L{x['hint_line']}->{x['line']} Q:{x['quote']}\n  {x['actual_line'][:210]}")
errors=[]; links=[]
for i,f in enumerate(FILES,1):
    text=f.read_text(encoding='utf8'); lines=text.splitlines(); fence=False; language=''; start=0; code=[]
    for l,line in enumerate(lines,1):
        if line.startswith('```'):
            if fence:
                if language.lower() in ('py','python','python3'):
                    try: ast.parse('\n'.join(code))
                    except SyntaxError as e: errors.append(dict(article=i,line=start+(e.lineno or 1),problem=e.msg,code='\n'.join(code)[:400]))
                fence=False
            else: fence=True;language=line[3:].strip();start=l;code=[]
        elif fence: code.append(line)
        else:
            for m in re.finditer(r'\]\((https?://[^\s)]+)\)',line):
                u=m.group(1)
                if re.search(r'[\u4e00-\u9fff]',u) and ('，' in u or '。' in u or '：' in u or '可以' in u or '这里' in u or '里面' in u): links.append(dict(article=i,line=l,url=u))
(HERE/'syntax-candidates.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2),encoding='utf8')
(HERE/'malformed-links.json').write_text(json.dumps(links,ensure_ascii=False,indent=2),encoding='utf8')
print('syntax_candidates',len(errors),'malformed_links',len(links))
