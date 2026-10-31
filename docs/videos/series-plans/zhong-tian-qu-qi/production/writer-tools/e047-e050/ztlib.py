"""Shared builder for 種田娶妻打天下 e056-e060 (video.json, overlays.json, clip lists, script.md, storyboard.md)."""
import json, os, subprocess, re

ROOT = "/home/user/travel_scanner"
P = f"{ROOT}/docs/videos/series-plans/zhong-tian-qu-qi"
H = f"{P}/production/hailuo"
e040 = json.load(open(f"{ROOT}/docs/videos/zhong-tian-qu-qi-e040/video.json"))
CAST = {c["id"]: c for c in json.load(open(f"{P}/production/cast.json"))["characters"]}

EN = {"xuyan": "Xu Yan", "aling": "A-ling", "qinshuang": "Qin Shuang", "tangxiaotang": "Tang Xiaotang", "erniu": "Wang Erniu",
      "xiaohe": "little Xiaohe", "lengtie": "Leng Tie", "changgonggong": "Eunuch Chang", "huxianling": "Magistrate Hu",
      "shimujiang": "Carpenter Shi", "hanbo": "Elder Han", "dutie": "Du Tie", "shaonian": "The lookout boy",
      "jinjuntongling": "The guard commander"}
HER = {"aling", "qinshuang", "tangxiaotang", "xiaohe"}
TANG = "Tang Xiaotang in her high-collared peach-pink ruqun with the collar closed at her throat and the small gold abacus at her waist"
ALING = "A-ling in her plain grey-white dress with the single wooden hairpin in her black hair"
NIGHT = "the cold moonlight and deep blue night stay unchanged"


def ch(i):
    c = CAST[i]
    return {"id": i, "name": c["name"], "appearance": c["appearance"], "voice": c["voice"]}


def minor(i, name, appearance, voice, style):
    return {"id": i, "name": name, "appearance": appearance,
            "voice": {"provider": "gemini", "name": voice, "style": "標準國語，咬字清楚，台北人平常說話的語調；" + style}}


class Ep:
    def __init__(self, num, characters):
        self.num = num
        self.slug = f"zhong-tian-qu-qi-e0{num}"
        self.out = f"{ROOT}/docs/videos/{self.slug}"
        self.characters = characters
        self.names = {c["id"]: c["name"] for c in characters}
        self.scenes, self.zh, self.n = [], {}, 0
        self.overlays = {}

    def speak(self, lines, chars):
        on = [l for l in lines if l[0] in chars and "畫外" not in l[2]]
        if not on:
            return ""
        whos = list(dict.fromkeys(l[0] for l in on))
        if len(whos) > 1:
            said = " then ".join(f"{EN[w][0].upper() + EN[w][1:]} speaks " + " ".join("「" + l[1].rstrip("。") + "」" for l in on if l[0] == w) for w in whos)
            return f"{said}, each speaking in Mandarin with lips, jaw and cheeks moving clearly with every syllable; "
        parts = []
        for who in whos:
            texts = [l[1].rstrip("。") for l in on if l[0] == who]
            pron = "her" if who in HER else "his"
            if len(texts) == 1:
                parts.append(f"{EN[who]} speaks a short Mandarin line, 「{texts[0]}」, {pron} lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes")
            else:
                parts.append(f"{EN[who]} speaks {len(texts)} short Mandarin lines, {' then '.join('「'+t+'」' for t in texts)}, {pron} lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes")
        return "; then ".join(parts) + "; "

    def shot(self, sid, camera, loc, comp, motion, chars, lines=(), chapter=None, action=None, zh="", panel=None):
        sid = f"s{len(self.scenes) + 1:02d}"
        ls = []
        for spk, text, emo in lines:
            self.n += 1
            ls.append({"id": f"zq{self.num}a{self.n:02d}", "speaker": spk, "text": text, "emotion": emo})
        m = self.speak(lines, chars) + motion
        s = {"id": sid}
        if chapter:
            s["chapter"] = chapter
        s["template"] = "shot"
        if action:
            s["action_seconds"] = action
        s["lines"] = ls
        s["data"] = {"camera": camera, "prompt": f"{loc}: {comp}", "motion": m, "characters": list(chars)}
        assert len(s["data"]["prompt"]) <= 1000, (sid, len(s["data"]["prompt"]))
        if len(m) > 300: print("LONG MOTION", sid, len(m))
        assert len(camera) <= 120
        assert len(chars) <= 3, sid
        assert not re.search(r"\bcamera\b", motion, re.I), sid
        self.scenes.append(s)
        self.zh[sid] = (chapter, zh)
        if panel:
            self.overlays[sid] = panel

    def write(self, music, title, description, thumb, tags=None):
        video = {
            "schema_version": 1, "slug": self.slug, "format": "drama",
            "target_minutes": [2, 3] if self.num in (59, 60) else [1, 2],
            "voice": e040["voice"], "look": e040["look"], "characters": self.characters,
            "music": {"prompt": music, "gain_db": -20, "duck_db": -10},
            "subtitles": e040["subtitles"],
            "youtube": {"category_id": 24, "made_for_kids": False, "default_language": "zh-TW",
                        "title": f"{title}｜種田娶妻打天下 第{self.num}集", "description": description,
                        "tags": tags or ["種田娶妻打天下", "AI短劇", "穿越", "種田", "系統"], "video_id": None},
            "thumbnail": {"template": "thumb", "data": thumb},
            "scenes": self.scenes,
        }
        os.makedirs(self.out, exist_ok=True)
        open(f"{self.out}/video.json", "w").write(json.dumps(video, ensure_ascii=False, indent=2) + "\n")
        open(f"{self.out}/overlays.json", "w").write(json.dumps(self.overlays, ensure_ascii=False, indent=2) + "\n")
        print(len(self.scenes), "shots,", self.n, "lines")
        r = subprocess.run(["node", f"{H}/gen-dh.mjs", f"{self.out}/video.json", f"{H}/local/empty-lock.json", str(self.num),
                            f"{H}/ff-dh-e0{self.num}.json", f"{H}/clips-dh-e0{self.num}.json"], capture_output=True, text=True)
        print(r.stdout, r.stderr)
        self.gen_out = r.stdout
        subprocess.run(["node", "tools/video/cli.mjs", "script", "--slug", self.slug], cwd=ROOT)

    def storyboard(self, title, head, foot):
        r = subprocess.run(["node", ".agents/skills/youtube-video/scripts/drama_craft_check.mjs", f"{self.out}/video.json", "--json"],
                           cwd=ROOT, capture_output=True, text=True)
        d = json.loads(r.stdout)
        rows = {x["id"]: x for x in d["rows"]}
        self.rows = rows
        ff = {j["id"]: j for j in json.load(open(f"{H}/ff-dh-e0{self.num}.json"))}
        self.ff = ff
        clips = json.load(open(f"{H}/clips-dh-e0{self.num}.json"))
        self.secs = {k.split("-")[1]: v[2] for k, v in clips.items()}
        out = [f"# 第 {self.num} 集〈{title}〉分鏡表", "", "<!-- 給人讀的中文版；製作用的英文提示詞在 video.json，系統面板文字在 overlays.json。 -->", ""]
        out += [f"- {h}" for h in head]
        out += ["", "| 鏡 | 開始 | 秒 | 種類 | 景別、運鏡 | 畫面 | 台詞 | 面板（overlays） |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for s in self.scenes:
            chap, zh = self.zh[s["id"]]
            if chap:
                out.append(f"| **{chap}** |||||||")
            row = rows[s["id"]]
            st = row["start"]
            lines = "<br>".join(
                f"{self.names[l['speaker']]}{'（畫外）' if ('畫外' in l['emotion'] or (l['speaker'] not in s['data']['characters'])) else ''}：{l['text']}"
                for l in s["lines"]) or "—"
            pan = "<br>".join(f"{o['text']}（{o['kind']}）" for o in self.overlays.get(s["id"], [])) or "—"
            out.append(f"| {s['id']} | {int(st // 60)}:{int(st % 60):02d} | {row['seconds']:.1f} | 片段 | {s['data']['camera']} | {zh} | {lines} | {pan} |")
        out.append("")
        out += [f"- {f}" for f in foot]
        open(f"{self.out}/storyboard.md", "w").write("\n".join(out) + "\n")
        print("total", d["total_seconds"])

    def setcount(self):
        c = {}
        miss = []
        for sid, j in self.ff.items():
            sets = [r for r in j["refs"] if r.startswith("dh-set-")]
            for x in sets:
                c[x] = c.get(x, 0) + 1
            if not sets:
                miss.append(sid)
        return c, miss


def fmt(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def _rows(ep):
    r = subprocess.run(["node", ".agents/skills/youtube-video/scripts/drama_craft_check.mjs", f"{ep.out}/video.json", "--json"],
                       cwd=ROOT, capture_output=True, text=True)
    d = json.loads(r.stdout)
    return {x["id"]: x for x in d["rows"]}, d["total_seconds"]


def fill(ep, text):
    rows, _ = _rows(ep)
    text = re.sub(r"\{t:(s\d\d)\}", lambda m: fmt(rows[m.group(1)]["start"]), text)
    text = re.sub(r"\{e:(s\d\d)\}", lambda m: fmt(rows[m.group(1)]["start"] + rows[m.group(1)]["seconds"]), text)
    return text


def listing(ep):
    rows, tot = _rows(ep)
    for s in ep.scenes:
        r = rows[s["id"]]
        print(s["id"], fmt(r["start"]), f"{r['seconds']:.1f}", s["data"]["camera"], "|", " / ".join(f"{l['speaker']}:{l['text']}" for l in s["lines"]))
    print("total", tot)


def auto(ep):
    clips = json.load(open(f"{H}/clips-dh-e0{ep.num}.json"))
    secs = [v[2] for v in clips.values()]
    six, five = secs.count(6), secs.count(5)
    ff = json.load(open(f"{H}/ff-dh-e0{ep.num}.json"))
    sets = {}
    for j in ff:
        for r in j["refs"]:
            if r.startswith("dh-set-"):
                sets.setdefault(r[:-4], []).append(j["id"])
    cams = {"locked": 0, "推近": 0, "拉遠": 0, "右搖": 0, "左搖": 0, "上搖": 0}
    for s in ep.scenes:
        c = s["data"]["camera"].lower()
        if "locked" in c: cams["locked"] += 1
        elif "push in" in c: cams["推近"] += 1
        elif "pull out" in c: cams["拉遠"] += 1
        elif "pan right" in c: cams["右搖"] += 1
        elif "pan left" in c: cams["左搖"] += 1
        elif "tilt up" in c: cams["上搖"] += 1
    cam = "、".join(f"`{k}` {v} 鏡" if k == "locked" else f"{k} {v} 鏡" for k, v in cams.items() if v)
    return six, five, sets, cam


def finish(ep, title, head, foot, brief):
    six, five, sets, cam = auto(ep)
    ep.storyboard(title, [fill(ep, h.replace("{six}", str(six)).replace("{five}", str(five)).replace("{cam}", cam)) for h in head],
                  [fill(ep, f) for f in foot])
    open(f"{ep.out}/brief.md", "w").write(fill(ep, brief).rstrip() + "\n")
    print({k: len(v) for k, v in sets.items()})
