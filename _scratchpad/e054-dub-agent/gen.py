# gen.py <locale> : writes docs/videos/zhong-tian-qu-qi-e054/dub.<locale>.json from lines/<locale>.txt
# lines file: one line per id: "NN|text|say" (say optional); emotion override: "NN|text|say|emotion"
import json, sys, os
R = "/home/user/travel_scanner"
here = os.path.dirname(os.path.abspath(__file__))
loc = sys.argv[1]
v = json.load(open(f"{R}/docs/videos/zhong-tian-qu-qi-e054/video.json"))
lines = [l for s in v["scenes"] for l in s.get("lines", [])]
rows = {}
for raw in open(f"{here}/lines/{loc}.txt", encoding="utf-8"):
    raw = raw.rstrip("\n")
    if not raw.strip() or raw.startswith("#"):
        continue
    parts = raw.split("|")
    rows["zq54a" + parts[0].zfill(2)] = parts[1:]
out = {}
for l in lines:
    p = rows[l["id"]]
    e = {"text": p[0], "emotion": l["emotion"]}
    if len(p) > 2 and p[2]:
        e["emotion"] = p[2]
    if len(p) > 1 and p[1] and p[1] != p[0]:
        e["say"] = p[1]
    out[l["id"]] = e
missing = set(rows) - {l["id"] for l in lines}
assert not missing, missing
with open(f"{R}/docs/videos/zhong-tian-qu-qi-e054/dub.{loc}.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(loc, len(out))
