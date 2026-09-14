"""Review traditional Chinese prose while preserving executable fenced examples."""
import argparse
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/claude-code-series/advanced/evidence/live'
parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
# Reviewed from a conversion diff. Do not convert valid Traditional Chinese
# spellings such as 查核, 干擾, 只有, or 才 merely because a converter suggests it.
replacements=dict(zip('装传内续盖断统还没确无据两报进结释验换参', '裝傳內續蓋斷統還沒確無據兩報進結釋驗換參'))
replacements.update({'属于':'屬於','日志':'日誌','准備':'準備'})
def convert_prose(value):
    for before,after in replacements.items():value=value.replace(before,after)
    return value
rows=[]
for number in range(61,97):
    path=ROOT/f'docs/claude-code-series/lessons/{number}.md'
    before=path.read_text(encoding='utf-8');parts=re.split(r'(```.*?```)',before,flags=re.S)
    after=''.join(part if part.startswith('```') else convert_prose(part) for part in parts)
    if before!=after:
        rows.append({'number':number,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'diff':'\n'.join(difflib.unified_diff(before.splitlines(),after.splitlines(),n=0))})
        if args.apply:path.write_text(after,encoding='utf-8')
report={'checked_at':datetime.now(timezone.utc).isoformat(),'mode':'apply' if args.apply else 'review','tool':'Manually reviewed replacement list; fenced examples preserved byte-for-byte','changed_lessons':rows}
(OUT/('editorial-applied.json' if args.apply else 'editorial-review.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'lessons':len(rows),'numbers':[row['number'] for row in rows]}))
