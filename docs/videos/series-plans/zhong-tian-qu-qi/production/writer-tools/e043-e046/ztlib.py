# Builder for zhong-tian-qu-qi e043-e046 video.json (scratch tool, not committed).
import json, os, re

REPO = "/home/user/travel_scanner"
CAST = json.load(open(f"{REPO}/docs/videos/series-plans/zhong-tian-qu-qi/production/cast.json"))
E42 = json.load(open(f"{REPO}/docs/videos/zhong-tian-qu-qi-e042/video.json"))
CASTMAP = {c["id"]: c for c in CAST["characters"]}
for c in E42["characters"]:
    CASTMAP.setdefault(c["id"], c)

STY = "標準國語，咬字清楚，台北人平常說話的語調；"
MINOR = {
    "shuli": None,  # from e042
    "zhanggui": None,
    "xunkao": {"id": "xunkao", "name": "巡考", "appearance": "East Asian man of forty, stocky with a heavy jaw and a bored scowl, a dark grey proctor's robe with a black sash and a black gauze cap, a wooden tally board in one hand", "voice": {"provider": "gemini", "name": "Alnilam", "style": STY + "四十歲的貢院巡考，男聲、不耐煩、照章辦事，說話短"}},
    "xunbing": {"id": "xunbing", "name": "巡兵", "appearance": "East Asian man of thirty, lean and sunburned with a suspicious squint, a red-bordered padded soldier's tunic, a black cloth cap, a spear in one hand", "voice": {"provider": "gemini", "name": "Orus", "style": STY + "三十歲的州府巡兵，男聲、粗聲粗氣、疑心重，被人一打岔就不耐煩"}},
    "shuliqi": {"id": "shuliqi", "name": "書吏娘子", "appearance": "East Asian woman of forty, round-faced and plump with quick sharp eyes, hair in a plain bun with one silver pin, a dark green cotton jacket with a high round collar over a long dark skirt", "voice": {"provider": "gemini", "name": "Kore", "style": STY + "四十歲的書吏娘子，女聲、愛說話又貪小便宜，收了東西就壓低聲音說得飛快"}},
    "yayi": {"id": "yayi", "name": "衙役", "appearance": "East Asian man of thirty, burly with a thick neck, a black runner's tunic with a red sash, a black cap, a long red-and-black wooden staff", "voice": {"provider": "gemini", "name": "Alnilam", "style": STY + "三十歲的州府衙役，男聲、嗓門大、拉長音吆喝"}},
}
EN = {"xuyan": "Xu Yan", "tangxiaotang": "Tang Xiaotang", "qinshuang": "Qin Shuang", "chengshanzhang": "Headmaster Cheng", "fengxuezheng": "Examiner Feng", "weixun": "Wei Xun", "dutie": "Du Tie", "chuzhifu": "Prefect Chu", "xudalang": "Xu Dalang", "shuli": "The registrar", "xunkao": "The proctor", "xunbing": "The patrolman", "shuliqi": "The clerk's wife", "yayi": "The runner", "zhanggui": "The innkeeper"}
HER = {"tangxiaotang", "qinshuang", "shuliqi"}
NAMEZH = {}


def character(cid):
    if cid in MINOR and MINOR[cid]:
        c = MINOR[cid]
    else:
        c = CASTMAP[cid]
    return {"id": c["id"], "name": c["name"], "appearance": c["appearance"], "voice": c["voice"]}


def speak_clause(cid, texts):
    q = [f"「{t.rstrip('。')}」" for t in texts]
    pron = "her" if cid in HER else "his"
    if len(q) == 1:
        s = f"a short Mandarin line, {q[0]}"
    else:
        s = f"{len(q)} short Mandarin lines, " + " then ".join(q)
    return f"{EN[cid]} speaks {s}, {pron} lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes"


def build(ep, sets, shots, meta, out):
    scenes = []
    n = 0
    used = []
    for sh in shots:
        st = sets[sh["set"]]
        lines = []
        for spk, text, emo in sh.get("lines", []):
            n += 1
            lines.append({"id": f"zq{ep}a{n:02d}", "speaker": spk, "text": text, "emotion": emo})
            if spk not in used:
                used.append(spk)
        chars = sh.get("chars", [])
        for c in chars:
            if c not in used:
                used.append(c)
        prompt = f"{st['open']}: {sh['comp']}"
        off = []
        for spk, _, _ in sh.get("lines", []):
            if spk not in chars and spk not in off:
                off.append(spk)
        offtxt = []
        for spk in off:
            offtxt.append("the system voice speaks off screen" if spk == "xitong" else f"{EN[spk] if spk in EN else spk} speaks off screen")
        if offtxt and "off screen" not in sh["comp"].split(";")[-1]:
            prompt += "; " + " and ".join(offtxt)
        talk = []
        by = {}
        for spk, text, _ in sh.get("lines", []):
            if spk in chars and spk != "xitong":
                by.setdefault(spk, []).append(text)
        for spk, ts in by.items():
            talk.append(speak_clause(spk, ts))
        motion = "; ".join(talk + [sh["act"]])
        if st.get("night"):
            motion += "; " + st["night"]
        scene = {"id": sh["id"]}
        if sh.get("ch"):
            scene["chapter"] = sh["ch"]
        scene["template"] = "shot"
        if not lines:
            scene["action_seconds"] = sh["sec"]
        scene["lines"] = lines
        scene["data"] = {"camera": sh["cam"], "prompt": prompt, "motion": motion, "characters": chars}
        assert len(prompt) <= 1000, (sh["id"], len(prompt))
        assert len(motion) <= 300, (sh["id"], len(motion), motion)
        assert len(sh["cam"]) <= 120
        assert len(chars) <= 3, sh["id"]
        scenes.append(scene)
    chars_all = [character(c) for c in used]
    v = {
        "schema_version": 1,
        "slug": f"zhong-tian-qu-qi-e0{ep}",
        "format": "drama",
        "target_minutes": [1, 2],
        "voice": E42["voice"],
        "look": E42["look"],
        "characters": chars_all,
        "music": {"prompt": meta["music"], "gain_db": -20, "duck_db": -10},
        "subtitles": E42["subtitles"],
        "youtube": {"category_id": 24, "made_for_kids": False, "default_language": "zh-TW", "title": meta["title"], "description": meta["description"], "tags": E42["youtube"]["tags"], "video_id": None},
        "thumbnail": {"template": "thumb", "data": {"headline": meta["headline"], "tag": "種田娶妻打天下", "shot": meta["thumb_shot"]}},
        "scenes": scenes,
    }
    d = f"{REPO}/docs/videos/zhong-tian-qu-qi-e0{ep}"
    os.makedirs(d, exist_ok=True)
    with open(f"{d}/video.json", "w") as f:
        f.write(json.dumps(v, ensure_ascii=False, indent=2) + "\n")
    # Chinese storyboard rows for the node table writer
    rows = [{"id": s["id"], "ch": s.get("ch"), "zh": s["zh"], "kind": s.get("kind", "片段")} for s in shots]
    with open(f"{out}/zh-e0{ep}.json", "w") as f:
        json.dump(rows, f, ensure_ascii=False)
    with open(f"{d}/overlays.json", "w") as f:
        f.write(json.dumps(meta["overlays"], ensure_ascii=False, indent=2) + "\n")
    print("lines", n, "shots", len(scenes))
