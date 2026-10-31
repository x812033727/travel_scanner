"""Builder for zhong-tian-qu-qi episodes: spec module -> video.json, overlays.json, storyboard.md, brief.md.
Usage: python3 build.py e051
"""
import importlib, json, os, re, subprocess, sys

REPO = "/home/user/travel_scanner"
HERE = os.path.dirname(os.path.abspath(__file__))
P = f"{REPO}/docs/videos/series-plans/zhong-tian-qu-qi"
H = f"{P}/production/hailuo"
CAST = {c["id"]: c for c in json.load(open(f"{P}/production/cast.json"))["characters"]}
EN = {"chengshanzhang": "Headmaster Cheng", "fengxuezheng": "Examiner Feng", "weixun": "Wei Xun", "dutie": "Du Tie", "chuzhifu": "Prefect Chu", "dengyasi": "Sergeant Deng", "lengtie": "Leng Tie", "xudalang": "Xu Dalang", "hanbo": "Elder Han", "xuyan": "Xu Yan", "aling": "A-ling", "qinshuang": "Qin Shuang", "tangxiaotang": "Tang Xiaotang", "xiaohe": "little Xiaohe", "erniu": "Wang Erniu", "qianyuanwai": "Qian Yuanwai",
      "yayi": "the yamen runner", "tongpan": "the vice-prefect", "zhifufuren": "the prefect's wife", "xinchai": "the courier", "zhanggui": "the innkeeper"}
HER = {"aling", "qinshuang", "tangxiaotang", "xiaohe", "zhifufuren"}
BASE = json.load(open(f"{REPO}/docs/videos/zhong-tian-qu-qi-e042/video.json"))


def speak_clause(sid, texts):
    t = [f"「{re.sub('。$', '', x)}」" for x in texts]
    who = EN[sid][0].upper() + EN[sid][1:]
    pro = "her" if sid in HER else "his"
    if len(t) == 1:
        return f"{who} speaks a short Mandarin line, {t[0]}, {pro} lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes"
    return f"{who} speaks {len(t)} short Mandarin lines, {' then '.join(t)}, {pro} lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes"


def main(name):
    spec = importlib.import_module(name)
    ep = spec.EP
    slug = f"zhong-tian-qu-qi-e{ep:03d}"
    out = f"{REPO}/docs/videos/{slug}"
    os.makedirs(out, exist_ok=True)
    chars = []
    for cid in spec.CHARACTERS:
        if cid in CAST:
            c = CAST[cid]
            chars.append({"id": c["id"], "name": c["name"], "appearance": c["appearance"], "voice": c["voice"]})
        else:
            chars.append(spec.MINOR[cid])
    names = {c["id"]: c["name"] for c in chars}
    scenes = []
    n = 0
    for i, s in enumerate(spec.SHOTS, 1):
        sid = f"s{i:02d}"
        lines = []
        on = [c for c in s.get("chars", [])]
        by = {}
        for (spk, text, emo) in s.get("lines", []):
            n += 1
            off = spk != "xitong" and spk not in on
            lines.append({"id": f"zq{ep}a{n:02d}", "speaker": spk, "text": text, "emotion": ("畫外，" + emo) if off and not emo.startswith("畫外") else emo})
            if not off and spk != "xitong":
                by.setdefault(spk, []).append(text)
        motion = s["motion"]
        talk = "; ".join(speak_clause(k, v) for k, v in by.items())
        if talk:
            motion = f"{talk}; {motion}"
        if s.get("night"):
            motion += f", and {spec.LIGHT[s['night']]}"
        comp = re.sub(r"((?:close-up|shot)) of ([A-Z][\w'-]*(?: [A-Z][\w'-]*)?) on screen", r"\1, \2 on screen", s['comp'])
        prompt = f"{spec.LOC[s['loc']]}: {comp}".replace("A-ling off screen", "Aling off screen")
        motion = motion.replace("A-ling off screen", "Aling off screen")
        offs = [k for (k, _, _) in s.get("lines", []) if k != "xitong" and k not in on]
        if offs and "off screen" not in prompt:
            prompt += f"; {EN[offs[0]]} speaks off screen"
        if any(k == "xitong" for (k, _, _) in s.get("lines", [])) and "system voice" not in prompt:
            prompt += "; the system voice speaks off screen"
        if len(motion) > 300: print("MOTION TOO LONG", sid, len(motion), len(motion) - len(s["motion"]))
        if len(prompt) > 1000: print("PROMPT TOO LONG", sid, len(prompt))
        scene = {"id": sid}
        if s.get("chapter"):
            scene["chapter"] = s["chapter"]
        scene["template"] = "shot"
        if not lines:
            scene["action_seconds"] = s.get("act", 2)
        scene["lines"] = lines
        scene["data"] = {"camera": s["cam"], "prompt": prompt, "motion": motion, "characters": on}
        scenes.append(scene)
    doc = {k: BASE[k] for k in ["schema_version"]}
    doc["slug"] = slug
    for k in ["format", "target_minutes", "voice", "look"]:
        doc[k] = BASE[k]
    doc["target_minutes"] = spec.TARGET_MINUTES
    doc["characters"] = chars
    doc["music"] = {"prompt": spec.MUSIC, "gain_db": -20, "duck_db": -10}
    doc["subtitles"] = BASE["subtitles"]
    yt = dict(BASE["youtube"])
    yt["title"] = spec.TITLE
    yt["description"] = spec.DESCRIPTION
    doc["youtube"] = yt
    doc["thumbnail"] = {"template": "thumb", "data": {"headline": spec.THUMB[0], "tag": "種田娶妻打天下", "shot": spec.THUMB[1]}}
    doc["scenes"] = scenes
    json.dump(doc, open(f"{out}/video.json", "w"), ensure_ascii=False, indent=2)
    open(f"{out}/video.json", "a").write("\n")
    ov = {}
    for i, s in enumerate(spec.SHOTS, 1):
        if s.get("panel"):
            ov[f"s{i:02d}"] = [{"text": t, "kind": k} for (t, k) in s["panel"]]
    json.dump(ov, open(f"{out}/overlays.json", "w"), ensure_ascii=False, indent=2)
    open(f"{out}/overlays.json", "a").write("\n")
    # gen-dh
    r = subprocess.run(["node", f"{H}/gen-dh.mjs", f"{out}/video.json", f"{H}/local/empty-lock.json", str(ep), f"{H}/ff-dh-e{ep:03d}.json", f"{H}/clips-dh-e{ep:03d}.json"], capture_output=True, text=True, cwd=REPO)
    gen = r.stdout.strip() + r.stderr.strip()
    print(gen)
    ff = json.load(open(f"{H}/ff-dh-e{ep:03d}.json"))
    clips = json.load(open(f"{H}/clips-dh-e{ep:03d}.json"))
    secs = {}
    for v in clips.values():
        secs[v[2]] = secs.get(v[2], 0) + 1
    setcount = {}
    for j in ff:
        st = [x for x in j["refs"] if x.startswith("dh-set-")]
        key = st[0][:-4] if st else "NONE"
        setcount[key] = setcount.get(key, 0) + 1
    print("sets", setcount)
    # timeline
    t = json.loads(subprocess.run(["node", f"{HERE}/tl.mjs", f"{out}/video.json"], capture_output=True, text=True).stdout)
    total = t["total"]
    rows = []
    for i, s in enumerate(spec.SHOTS, 1):
        sid = f"s{i:02d}"
        st, du = t["scenes"][sid]
        if s.get("chapter"):
            rows.append(f"| **{s['chapter']}** |||||||")
        ls = []
        for (spk, text, emo) in s.get("lines", []):
            off = spk == "xitong" or spk not in s.get("chars", [])
            ls.append(f"{names[spk]}{'（畫外）' if off else ''}：{text}")
        pan = "<br>".join(f"{tx}（{k}）" for (tx, k) in s.get("panel", [])) or "—"
        tag = s.get("tag", "")
        zh = (f"【{tag}】" if tag else "") + (s["zh"][len(tag) + 1:] if tag and s["zh"].startswith(tag + "：") else s["zh"]) + ("（無台詞）" if not ls else "")
        rows.append(f"| {sid} | {int(st//60)}:{int(st%60):02d} | {du:.1f} | 片段 | {s['cam']} | {zh} | {'<br>'.join(ls) or '—'} | {pan} |")
    n6 = secs.get(6, 0); n5 = secs.get(5, 0)
    head = [f"# 第 {ep} 集〈{spec.EP_TITLE}〉分鏡表", "", "<!-- 給人讀的中文版；製作用的英文提示詞在 video.json，系統面板文字在 overlays.json。 -->", "",
            f"- {len(spec.SHOTS)} 個鏡頭、{len([s for s in spec.SHOTS if s.get('chapter')])} 段（{'／'.join(s['chapter'] for s in spec.SHOTS if s.get('chapter'))}），估計約 {round(total)} 秒（照 lint 估法；真人語速通常再長一成左右，約 {round(total*1.1)} 秒）；細綱 {spec.OUTLINE_SECONDS} 秒",
            f"- 預算：片段 {len(clips)} 支（靜圖 0 張），沒有「切素材」鏡。片段在 Colab 用 H3 Ref2VA 做（`production/colab/README.md`，沒有首格；第 33 集起路線 A）；`gen-dh.mjs` 算 {n6} 支 6 秒、{n5} 支 5 秒（海螺點數換算約 {int(re.search(r"total ≈ (\d+)", gen).group(1)):,} 點，只當對照；首格清單 {len(ff)} 張只當參照圖清單）"]
    head += spec.HEAD
    table = ["", "| 鏡 | 開始 | 秒 | 種類 | 景別、運鏡 | 畫面 | 台詞 | 面板（overlays） |", "| --- | --- | --- | --- | --- | --- | --- | --- |"] + rows + [""]
    open(f"{out}/storyboard.md", "w").write("\n".join(head + table + spec.FOOT) + "\n")
    open(f"{out}/brief.md", "w").write(spec.BRIEF.strip() + "\n")
    # timings for brief writing
    print("total", round(total, 1), "lines", n, "shots", len(spec.SHOTS))
    for i, s in enumerate(spec.SHOTS, 1):
        sid = f"s{i:02d}"
        st, du = t["scenes"][sid]
        print(sid, f"{int(st//60)}:{int(st%60):02d}", f"{du:.1f}", s.get("tag", ""), "|", " / ".join(x[1] for x in s.get("lines", [])))


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    main(sys.argv[1])
