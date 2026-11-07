# fix.py <locale> <json of {id: {say?, emotion?}}> : patch dub.<locale>.json in place.
import json, sys
p = f"/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e052/dub.{sys.argv[1]}.json"
d = json.load(open(p))
for i, ch in json.loads(sys.argv[2]).items():
    e = d[i]
    for k in ("text", "say", "emotion"):
        if k in ch:
            e[k] = ch[k]
    if e.get("say") == e["text"]:
        e.pop("say")
    d[i] = {"text": e["text"], "emotion": e["emotion"], **({"say": e["say"]} if "say" in e else {})}
open(p, "w").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print("patched", list(json.loads(sys.argv[2])))
