#!/usr/bin/env python3
"""Print a compact reading view of one episode: chapters, every line with its speaker, and each
silent action shot's motion. Usage: python3 dialogue.py --ep N [--out FILE]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
ep = int(args[args.index("--ep") + 1])
out = args[args.index("--out") + 1] if "--out" in args else os.path.join(HERE, f"ep{ep}", "dialogue.txt")
d = os.path.join(HERE, f"ep{ep}")
header = json.load(open(os.path.join(d, "header.json"), encoding="utf-8"))
names = {c["id"]: c["name"].split("「")[0] for c in header["characters"]}
names["narrator"] = "旁白"
lines = []
for act in ["a01", "a02", "a03", "a04", "a05"]:
    path = os.path.join(d, "acts", f"{act}.json")
    if not os.path.exists(path):
        continue
    for s in json.load(open(path, encoding="utf-8")):
        if s.get("chapter"):
            lines.append(f"\n== {s['chapter']} ==")
        sid = s["id"]
        data = s.get("data", {})
        if s["template"] != "shot":
            spoken = " / ".join(l["text"] for l in s.get("lines", []))
            lines.append(f"{sid} [卡 {data.get('title')}｜{data.get('subtitle', '')}] {spoken}")
            continue
        cam = data.get("camera", "")
        looks = data.get("character_looks")
        tag = f" looks={looks}" if looks else ""
        if s.get("action_seconds"):
            lines.append(f"{sid} [{cam}]{tag} ⟨動作{s['action_seconds']}s⟩ {data.get('motion', '')[:140]}")
        else:
            spoken = " ".join(f"{names.get(l.get('speaker', 'narrator'), l.get('speaker'))}：{l['text']}" for l in s.get("lines", []))
            lines.append(f"{sid} [{cam}]{tag} {spoken}")
open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"wrote {out} ({len(lines)} rows)")
