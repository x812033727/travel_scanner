import json, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/e053-dub-agent')
from lines import L
D = '/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e053'
v = json.load(open(f'{D}/video.json'))
lines = [l for s in v['scenes'] for l in s.get('lines', [])]
for loc in sys.argv[1:]:
    arr = L[loc]
    assert len(arr) == len(lines), (loc, len(arr))
    out = {}
    for l, e in zip(lines, arr):
        t, s = (e if isinstance(e, tuple) else (e, None))
        o = {"text": t, "emotion": l['emotion']}
        if s: o["say"] = s
        out[l['id']] = o
    open(f'{D}/dub.{loc}.json', 'w').write(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(loc, len(out))
