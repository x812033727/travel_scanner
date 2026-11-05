#!/usr/bin/env python3
"""Build one zhong-tian episode (video.json, overlays.json, storyboard.md) from a spec module,
then run `cli.mjs script`, gen-dh.mjs and the three checks. Usage: build_ep.py spec47.py"""
import importlib.util, json, os, re, subprocess, sys

ROOT = "/home/user/travel_scanner"
P = f"{ROOT}/docs/videos/series-plans/zhong-tian-qu-qi"
H = f"{P}/production/hailuo"
CAST = {c["id"]: c for c in json.load(open(f"{P}/production/cast.json"))["characters"]}
EN = {"chengshanzhang": "Headmaster Cheng", "fengxuezheng": "Examiner Feng", "weixun": "Wei Xun", "dutie": "Du Tie",
      "chuzhifu": "Prefect Chu", "xudalang": "Xu Dalang", "zhouyuanwai": "Zhou Yuanwai", "xuyan": "Xu Yan",
      "qinshuang": "Qin Shuang", "tangxiaotang": "Tang Xiaotang"}
HER = {"qinshuang", "tangxiaotang", "aling", "xiaohe"}
NIGHT = "the cold moonlight and deep blue night stay unchanged"
INSERT_OPEN = "The shot opens directly on this close insert from its very first frame: "

spec_path = sys.argv[1]
spec_mod = importlib.util.spec_from_file_location("spec", spec_path)
S = importlib.util.module_from_spec(spec_mod)
spec_mod.loader.exec_module(S)
num = S.NUM
slug = f"zhong-tian-qu-qi-e0{num}"
out = f"{ROOT}/docs/videos/{slug}"
os.makedirs(out, exist_ok=True)

def strip_end(t):
    return re.sub(r"[。]$", "", t)

chars = []
for cid in S.CHARS:
    if cid in CAST:
        c = CAST[cid]
        chars.append({"id": c["id"], "name": c["name"], "appearance": c["appearance"], "voice": c["voice"]})
    else:
        chars.append(S.MINOR[cid])
names = {c["id"]: c["name"] for c in chars}

scenes, overlays, rows = [], {}, []
li = 0
for i, sh in enumerate(S.SHOTS, 1):
    sid = f"s{i:02d}"
    lines = []
    for (spk, text, emo) in sh.get("lines", []):
        li += 1
        lines.append({"id": f"zq{num}a{li:02d}", "speaker": spk, "text": text, "emotion": emo})
    on = [l for l in lines if l["speaker"] != "xitong" and l["speaker"] in sh.get("chars", [])]
    by = {}
    for l in on:
        by.setdefault(l["speaker"], []).append(f"「{strip_end(l['text'])}」")
    talk = "; ".join(
        f"{EN.get(k, k)} speaks {f'{len(v)} short Mandarin lines, ' + ' then '.join(v) if len(v) > 1 else 'a short Mandarin line, ' + v[0]}, {'her' if k in HER else 'his'} lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes"
        for k, v in by.items())
    motion = sh["motion"]
    if sh.get("insert"):
        motion = INSERT_OPEN + motion
    if talk:
        motion = f"{talk}; {motion}"
    if sh.get("night"):
        motion = f"{motion}; {sh['night'] if isinstance(sh['night'], str) else NIGHT}"
    scene = {"id": sid}
    if sh.get("ch"):
        scene["chapter"] = sh["ch"]
    scene["template"] = "shot"
    if sh.get("act"):
        scene["action_seconds"] = sh["act"]
    scene["lines"] = lines
    scene["data"] = {"camera": sh["cam"], "prompt": f"{sh['set']}: {sh['prompt']}", "motion": motion, "characters": sh.get("chars", [])}
    if len(motion) > 300: print("MOTION TOO LONG", sid, len(motion))
    if len(scene["data"]["prompt"]) > 1000: print("PROMPT TOO LONG", sid)
    scenes.append(scene)
    if sh.get("ov"):
        overlays[sid] = [{"text": t, "kind": k} for (t, k) in sh["ov"]]
    rows.append((sid, sh, lines))

doc = {
    "schema_version": 1, "slug": slug, "format": "drama", "target_minutes": S.TARGET_MINUTES,
    "voice": {"provider": "gemini", "name": "Sulafat", "style": "標準國語，咬字清楚，台北人平常說話的語調；沉穩的說書人"},
    "look": json.load(open(f"{ROOT}/docs/videos/zhong-tian-qu-qi-e042/video.json"))["look"],
    "characters": chars,
    "music": {"prompt": S.MUSIC, "gain_db": -20, "duck_db": -10},
    "subtitles": {"burn_in": False, "style": "drama"},
    "youtube": {"category_id": 24, "made_for_kids": False, "default_language": "zh-TW", "title": S.YT_TITLE,
                "description": S.YT_DESC, "tags": ["種田娶妻打天下", "AI短劇", "穿越", "種田", "系統"], "video_id": None},
    "thumbnail": {"template": "thumb", "data": {"headline": S.THUMB[0], "tag": "種田娶妻打天下", "shot": S.THUMB[1]}},
    "scenes": scenes,
}
json.dump(doc, open(f"{out}/video.json", "w"), ensure_ascii=False, indent=1)
open(f"{out}/video.json", "a").write("\n")
json.dump(overlays, open(f"{out}/overlays.json", "w"), ensure_ascii=False, indent=2)
open(f"{out}/overlays.json", "a").write("\n")

# Durations as shot_reading reads them.
sr = subprocess.run(["node", f"{ROOT}/.agents/skills/animation-camera/scripts/shot_reading.mjs", f"{out}/video.json"], capture_output=True, text=True).stdout
dur = {m.group(1): float(m.group(2)) for m in re.finditer(r"^\[(s\d+)\] \S+ · 約 ([\d.]+) s", sr, re.M)}

def mmss(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02d}"

t = 0.0
table = ["| 鏡 | 開始 | 秒 | 種類 | 景別、運鏡 | 畫面 | 台詞 | 面板（overlays） |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
starts = {}
for sid, sh, lines in rows:
    if sh.get("ch"):
        table.append(f"| **{sh['ch']}** |||||||")
    starts[sid] = t
    d = dur.get(sid, 0)
    tag = f"【{sh['tag']}】" if sh.get("tag") and not sh["zh"].startswith(f"【{sh['tag']}】") else ""
    ls = "<br>".join(f"{names[l['speaker']]}{'' if l['speaker'] in sh.get('chars', []) and l['speaker'] != 'xitong' else '（畫外）'}：{l['text']}" for l in lines) or "—"
    if not lines:
        zh = sh["zh"] + "（無台詞）"
    else:
        zh = sh["zh"]
    ov = "<br>".join(f"{tx}（{k}）" for tx, k in sh.get("ov", [])) or "—"
    table.append(f"| {sid} | {mmss(t)} | {d:.1f} | 片段 | {sh['cam']} | {tag}{zh} | {ls} | {ov} |")
    t += d
total = t
head = [f"# 第 {num} 集〈{S.TITLE}〉分鏡表", "", "<!-- 給人讀的中文版；製作用的英文提示詞在 video.json，系統面板文字在 overlays.json。 -->", ""]
head += [f"- {x}" for x in S.SB_HEAD(total, starts, dur)]
foot = [f"- {x}" for x in S.SB_FOOT]
open(f"{out}/storyboard.md", "w").write("\n".join(head + [""] + table + [""] + foot) + "\n")
open(f"{out}/brief.md", "w").write(S.BRIEF(starts, dur, total))

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return (r.stdout + r.stderr).strip()

print(run(["node", "tools/video/cli.mjs", "script", "--slug", slug]))
print(run(["node", f"{H}/gen-dh.mjs", f"{out}/video.json", f"{H}/local/empty-lock.json", str(num), f"{H}/ff-dh-e0{num}.json", f"{H}/clips-dh-e0{num}.json"]))
print(run(["node", "tools/video/cli.mjs", "lint", "--slug", slug]))
cc = run(["node", ".agents/skills/youtube-video/scripts/drama_craft_check.mjs", f"{out}/video.json"])
print("\n".join(l for l in cc.splitlines() if not l.startswith(("ok ", "info"))))
print(sr.strip().splitlines()[-1])
for m in re.finditer(r"^\s+(?:陷阱|TRAP|⚠|!).*$", sr, re.M):
    print(m.group(0))
ff = json.load(open(f"{H}/ff-dh-e0{num}.json"))
from collections import Counter
print("sets:", Counter(next((r for r in j["refs"] if "set-" in r), "NONE") for j in ff))
print(f"total {total:.1f} s, {len(rows)} shots, {li} lines")
