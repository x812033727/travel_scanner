# usage: python3 gen.py <locale> : reads data/<locale>.txt (59 lines "text | say | emotion"), writes dub.<locale>.json
import json, sys, os
R = "/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e049"
here = os.path.dirname(os.path.abspath(__file__))
loc = sys.argv[1]
v = json.load(open(f"{R}/video.json"))
lines = [l for s in v["scenes"] for l in s.get("lines", [])]
rows = [r for r in open(f"{here}/data/{loc}.txt", encoding="utf8").read().split("\n") if r.strip() and not r.startswith("#")]
assert len(rows) == len(lines), (len(rows), len(lines))
out = {}
for l, r in zip(lines, rows):
    parts = [p.strip() for p in r.split(" | ")]
    parts += [""] * (3 - len(parts))
    text, say, emo = parts[:3]
    e = {"text": text, "emotion": emo or l["emotion"]}
    if say: e["say"] = say
    out[l["id"]] = e
open(f"{R}/dub.{loc}.json", "w", encoding="utf8").write(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(loc, len(out))
