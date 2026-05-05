"""build_html.py — 把 psych_template.html + data/questions/*.json 組成 index.html。

把 template 中 <script id="qdata"> 占位區段替換成完整的 QUESTIONS 陣列。
"""
import json
import re
from pathlib import Path

# 題庫載入順序（左→右、舊→新）。新增學校試卷時加進這個 list。
FILE_ORDER = [
    'FJU_107.json', 'FJU_108.json', 'FJU_109.json',
    'FJU_111.json', 'FJU_112.json', 'FJU_113.json',
    'FJU_114A.json', 'FJU_114B.json',
    'NTU_108.json', 'NTU_109.json', 'NTU_111.json',
    'NTU_112.json', 'NTU_113.json', 'NTU_114.json',
    'NCKU_107.json', 'NCKU_108.json', 'NCKU_109.json',
    'NCKU_111.json', 'NCKU_112.json', 'NCKU_113.json', 'NCKU_114.json',
]

ROOT = Path(__file__).parent
DATA_DIR = ROOT / 'data' / 'questions'
TEMPLATE = ROOT / 'psych_template.html'
OUT = ROOT / 'index.html'


def load_questions():
    out = []
    for fn in FILE_ORDER:
        p = DATA_DIR / fn
        if not p.exists():
            print(f'  SKIP missing: {fn}')
            continue
        d = json.loads(p.read_text(encoding='utf-8'))
        qs = d.get('questions') if isinstance(d, dict) else d
        out.extend(qs)
        print(f'  + {fn}: {len(qs)}')
    return out


def main():
    print('Loading questions ...')
    questions = load_questions()
    print(f'  TOTAL: {len(questions)}')

    print('Reading template ...')
    html = TEMPLATE.read_text(encoding='utf-8')

    payload = json.dumps(questions, ensure_ascii=False)
    new_script = f'<script id="qdata">window.__QUESTIONS__ = {payload};</script>'

    pattern = re.compile(r'<script id="qdata">.*?</script>', re.DOTALL)
    if not pattern.search(html):
        raise SystemExit('placeholder <script id="qdata"> not found in template')
    new_html = pattern.sub(lambda _: new_script, html, count=1)

    OUT.write_text(new_html, encoding='utf-8')
    print(f'Wrote {OUT.name}: {len(new_html):,} bytes ({len(questions)} questions)')


if __name__ == '__main__':
    main()
