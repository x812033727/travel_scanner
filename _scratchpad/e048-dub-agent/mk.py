# mk.py <locale>: build docs/videos/zhong-tian-qu-qi-e048/dub.<locale>.json from <locale>.txt
# each line: id | text | say (blank = none) | emotion (blank = copy video.json)
import json, sys, os
L = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
R = '/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e048'
v = json.load(open(R + '/video.json', encoding='utf-8'))
emo = {l['id']: l.get('emotion', '') for s in v['scenes'] for l in s.get('lines', [])}
out = {}
for raw in open(f'{here}/{L}.txt', encoding='utf-8'):
    raw = raw.rstrip('\n')
    if not raw.strip() or raw.startswith('#'): continue
    p = [x.strip() for x in raw.split('|')]
    p += [''] * (4 - len(p))
    i, t, s, e = p[:4]
    assert i in emo, i
    o = {'text': t, 'emotion': e or emo[i]}
    if s: o['say'] = s
    out[i] = o
miss = [i for i in emo if i not in out]
assert not miss, miss
out = {i: out[i] for i in emo}
open(f'{R}/dub.{L}.json', 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(L, len(out), 'lines written')
