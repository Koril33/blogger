from pathlib import Path
import json
import sys

ROOT = Path('C:/Project/blog')
OUT = Path(__file__).parent
FILES = sorted(ROOT.rglob('*.md'), key=lambda p: str(p.relative_to(ROOT)).casefold())

def catalog():
    items = []
    for i, p in enumerate(FILES, 1):
        text = p.read_text(encoding='utf-8-sig')
        items.append({'id': i, 'path': p.relative_to(ROOT).as_posix(), 'lines': len(text.splitlines()), 'chars': len(text)})
    (OUT / 'catalog.json').write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
    for x in items:
        print(f"{x['id']:03} | {x['lines']:4} | {x['chars']:6} | {x['path']}")
    print('TOTAL', len(items), sum(x['chars'] for x in items))

def read(start, end, mode, lo=1, hi=1000000):
    for i in range(start, end + 1):
        p = FILES[i - 1]
        print(f'\n===== {i:03}: {p.relative_to(ROOT).as_posix()} =====')
        in_code = False
        block = []
        for num, line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(), 1):
            if not lo <= num <= hi:
                if line.lstrip().startswith('```'): in_code = not in_code
                continue
            if mode == 'full':
                print(f'{num}: {line}')
                continue
            if line.lstrip().startswith('```'):
                in_code = not in_code
                if not in_code and block:
                    print(f'CODE {block[0][0]}-{block[-1][0]}:')
                    print('\n'.join(f'{n}: {s}' for n, s in block))
                    block = []
                continue
            if in_code:
                if mode == 'prose':
                    continue
                if line.strip() and (line.lstrip().startswith(('#include', '#define', '#if', '#endif')) or not line.lstrip().startswith(('#', '//', '*', '<!--'))):
                    block.append((num,line))
                elif line.lstrip().startswith(('#', '//')) and any(c in line for c in '的一是将为'):
                    block.append((num,line))
            elif mode != 'code' and line.strip() and not line.lstrip().startswith('!['):
                print(f'{num}: {line}')
        if block:
            print(f'CODE {block[0][0]}-{block[-1][0]}:')
            print('\n'.join(f'{n}: {s}' for n, s in block))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        catalog()
    else:
        if len(sys.argv)>5:
            read(int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],int(sys.argv[4]),int(sys.argv[5]))
        else:
            read(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3] if len(sys.argv)>3 else 'compact')
