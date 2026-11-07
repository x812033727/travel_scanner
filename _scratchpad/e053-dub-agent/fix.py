# usage: fix.py <locale> id:field=value ...   (field = say|emotion|text)
import json, sys
loc = sys.argv[1]
p = f'/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e053/dub.{loc}.json'
d = json.load(open(p))
for a in sys.argv[2:]:
    k, rest = a.split(':', 1); f, val = rest.split('=', 1)
    d[k][f] = val
    o = d[k]; d[k] = {"text": o["text"], "emotion": o["emotion"], **({"say": o["say"]} if "say" in o else {})}
    print(k, json.dumps(d[k], ensure_ascii=False))
open(p, 'w').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
