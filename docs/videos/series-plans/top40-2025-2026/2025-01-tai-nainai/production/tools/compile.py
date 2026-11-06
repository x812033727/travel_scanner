#!/usr/bin/env python3
"""《祖奶奶今年十八》一集：script.md ＋ shots-en.json → video.json、brief.md 與 Colab Ref2VA 第一段 manifest（標準函式庫）。

  compile.py 1 [--check] [--manifest --refs DIR --work DIR [--width 960 --height 544] [--only c01,c02] [--placeholders]]

- script.md 是源頭（中文分鏡、台詞、秒數）；shots-en.json 是逐鏡的英文正文，每鏡記著那一列中文的 `zh_sha256`。
  中文改了而英文沒跟著改，就列出哪幾鏡並以 1 停下（`--check` 只做這件事）。
- 台詞照 script.md：說話人對 cast.json、語氣（括號）進 emotion、標記（→ 答在、← 因為、結尾、懸念）拿掉。
  shots-en.json 的 `speaker_overrides` 可以指定對不到 cast.json 的說話人（例如第 60 集「電話那頭」是顧承霖）。
- 沒有台詞的鏡用 `action_seconds`（script.md 的秒數四捨五入、夾在 1–8）。
- `--manifest`：每鏡的參考圖 = 畫面裡的角色定妝照（`<id>-portrait-t1.png`，換裝 `<id>-<look>-t1.png`）＋場景圖
  （`set-<場景>-t1.png`；祠堂有燈的分數時先找 `set-<場景>-lamp<N>-t1.png`），在 --refs 裡找；正文照
  `minimax-h3-colab/references/motion-quality.md` 與 lessons.md 第 2、12、13 節組。每 20 鏡一份。
路徑：script.md 在 docs/videos/tai-nainai-eNNN/，shots-en.json 在同一個資料夾。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import parse_script  # noqa: E402

ROOT = HERE.parents[6]
CAST = HERE.parent / "cast.json"
SERIES = "祖奶奶今年十八"
LINE_PREFIX = "t"
TAIL = ("One continuous shot. Natural, realistic live-action human motion; faces, hair and costumes stay as in their reference pictures; "
        "nothing written anywhere in the frame.")
FACES_RULE = ("Besides them, only the other people the composition names are in the frame; no second copy of anyone appears. "
              "Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the face, hair and costume only, never the mood.")
EN_NAMES = {
    "yuetang-18": "Shen Yuetang", "yuetang-96": "Shen Yuetang at ninety-six", "yuqin": "Shen Yuqin", "jianbang": "Shen Jianbang",
    "zhiyuan": "Shen Zhiyuan", "xiaoman": "Shen Xiaoman", "fubo": "Fu Bo", "jianye": "Shen Jianye", "meifeng": "Lin Meifeng",
    "zhixing": "Shen Zhixing", "zhouhuaian": "Zhou Huai'an", "guchenglin": "Gu Chenglin", "guyuanshan": "Gu Yuanshan",
    "yuanshan-20": "the young Gu Yuanshan", "jiangmubai": "Jiang Mubai", "suxiao": "Su Xiao", "laochen": "Old Chen",
    "hexiaoyang": "He Xiaoyang", "lindao": "Director Lin", "zuofu": "Shen Zuofu", "akai": "Officer Kai", "qianlaoban": "Boss Qian",
    "wuxiaozhang": "Principal Wu", "chenlaoshi": "Teacher Chen", "heqisheng": "He Qisheng", "zhengyishi": "Dr. Zheng",
    "linzhuren": "Director Lin of the care home", "gaojingli": "Manager Gao", "denglao": "Elder Deng", "chuntao": "Granny Chuntao",
}
STRIP_EMOTION = re.compile(r"`[a-z0-9-]+`，?|96，?|畫外，?|心裡話，?|嘴閉著，?|背對鏡頭，?")


def episode_dir(ep: int) -> Path:
    return ROOT / "docs" / "videos" / f"tai-nainai-e{ep:03d}"


def load(ep: int) -> tuple[dict, dict, dict]:
    parsed = parse_script.parse(episode_dir(ep) / "script.md")
    en_path = episode_dir(ep) / "shots-en.json"
    en = json.loads(en_path.read_text(encoding="utf-8")) if en_path.is_file() else {"shots": {}}
    cast = json.loads(CAST.read_text(encoding="utf-8"))
    return parsed, en, cast


def drift(parsed: dict, en: dict) -> list[str]:
    problems = []
    ids = []
    for sc in parsed["scenes"]:
        for s in sc["shots"]:
            ids.append(s["id"])
            e = en["shots"].get(s["id"])
            if not e:
                problems.append(f"{s['id']}: shots-en.json 沒有這一鏡")
            elif e.get("zh_sha256") != s["row_sha256"]:
                problems.append(f"{s['id']}: script.md 那一列改過了（{s['row_sha256'][:12]}），英文正文要跟著改再更新 zh_sha256")
    for extra in set(en["shots"]) - set(ids):
        problems.append(f"{extra}: shots-en.json 有、script.md 沒有")
    return problems


def emotion(notes: str) -> str | None:
    text = STRIP_EMOTION.sub("", notes).strip("，, ")
    return text[:80] or None


def character_entry(c: dict) -> dict:
    out = {k: c[k] for k in ("id", "name", "appearance", "voice") if k in c}
    if c.get("shot_looks"):
        out["shot_looks"] = [{"id": s["id"], "appearance": s["appearance"]} for s in c["shot_looks"]]
    return out


def section(text: str, title: str) -> str:
    m = re.search(rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def build_video(parsed: dict, en: dict, cast: dict) -> tuple[dict, str]:
    ep = parsed["episode"]
    chars = {c["id"]: c for c in cast["characters"]}
    extras = {e["id"]: e for e in cast["extras"]}
    script = (episode_dir(ep) / "script.md").read_text(encoding="utf-8")
    heading = re.search(r"^# .*?第\s*(\d+)\s*集：(.+)$", script, re.M)
    ep_title = heading.group(2).strip() if heading else f"第{ep}集"
    overrides = en.get("speaker_overrides", {})
    scenes, used, n = [], [], 0
    total = 0.0
    for sc in parsed["scenes"]:
        for s in sc["shots"]:
            e = en["shots"][s["id"]]
            lines = []
            for d in s["dialogue"]:
                who = overrides.get(s["id"]) if not d["speaker"] else d["speaker"]
                if not who:
                    raise SystemExit(f"{s['id']}: 說話人 {d['speaker_label']!r} 對不到 cast.json，在 shots-en.json 的 speaker_overrides 指定")
                n += 1
                line = {"id": f"{LINE_PREFIX}{ep:03d}{n:03d}", "speaker": who, "text": d["text"]}
                emo = emotion(d["notes"])
                if emo:
                    line["emotion"] = emo
                lines.append(line)
                used.append(who)
            shot_chars = list(e.get("characters", []))[:3]
            used += shot_chars
            data = {"prompt": e["prompt"][:1000], "camera": e["camera"], "characters": shot_chars}
            if e.get("motion"):
                data["motion"] = e["motion"]
            looks = {k: v for k, v in (e.get("looks") or {}).items() if k in shot_chars}
            if looks:
                data["character_looks"] = looks
            scene = {"id": s["id"], "template": "shot", "lines": lines, "data": data}
            if sc["shots"][0] is s:
                scene["chapter"] = sc["title"].split("，")[-1]
            if not lines and not e.get("motion"):
                raise SystemExit(f"{s['id']}: 沒有台詞的鏡要在 shots-en.json 寫 motion（看得到的動作，一句）")
            if not lines:
                scene["action_seconds"] = max(1, min(8, round(s["seconds"] or 4)))
            scenes.append(scene)
            total += s["seconds"] or 0
    roster = []
    for cid in dict.fromkeys(used):
        if cid in chars:
            roster.append(character_entry(chars[cid]))
        elif cid in extras:
            x = extras[cid]
            roster.append({"id": cid, "name": x["name"], "appearance": x["appearance"], "voice": x["voice"]})
    story = section(script, "劇情")
    video = {
        "schema_version": 1,
        "slug": f"tai-nainai-e{ep:03d}",
        "format": "drama",
        "target_minutes": [round(max(total / 60 - 0.5, 1), 1), round(total / 60 + 1, 1)],
        "voice": {"provider": "gemini", "name": "Sulafat", "style": "標準國語，咬字清楚，台北人平常說話的語調；沉穩的說書人"},
        "look": {k: cast["look"][k] for k in ("preset", "style", "negative", "motion", "candidates")},
        "characters": roster,
        "music": {"prompt": en.get("music", "a slow solo guzheng over soft low strings, warm and restrained, no vocals")},
        "subtitles": {"burn_in": False, "style": "drama"},
        "youtube": {
            "category_id": 24, "made_for_kids": False, "default_language": "zh-TW",
            "title": en.get("youtube_title") or f"{ep_title}｜{SERIES} 第{ep}集",
            "description": (en.get("youtube_description") or re.sub(r"\s+", "", story))[:4800],
            "tags": [SERIES, "AI短劇", "家族劇", "老靈魂"],
            "video_id": None,
        },
        "thumbnail": {"template": "thumb", "data": {"headline": en.get("thumbnail", {}).get("headline", ep_title), "tag": SERIES,
                                                    "shot": en.get("thumbnail", {}).get("shot", scenes[0]["id"])}},
        "scenes": scenes,
    }
    cast_lines = []
    for r in roster:
        note = (chars.get(r["id"]) or {}).get("notes", "")
        cast_lines.append(f"- {r['name']}（{r['id']}）：聲音 {r['voice']['name']}。{note}".rstrip())
    brief = (
        f"# 《{SERIES}》第 {ep} 集〈{ep_title}〉\n\n"
        f"## 故事前提\n\n{story}\n\n{section(script, '這集接在哪')}\n\n"
        f"## 角色\n\n" + "\n".join(cast_lines) + "\n\n"
        "## 站主觀點\n\n"
        "照 `plan.json` 的 reference.how：只學「老靈魂＋輩分錯位＋重整家族」的套路，人名、家族、劇情、台詞全部原創。"
        "站主 2026-11-06 試鏡後定走真人風格（3D 不行），片段先做到 1312×736。"
        "這部沒有系統、沒有面板；長明燈是唯一的特效，老化只用化妝與光。分鏡與台詞的權威版本是同一個資料夾的 `script.md`。\n"
    )
    return video, brief


def write_png(path: Path, size: tuple[int, int]) -> None:
    w, h = size
    row = b"\x00" + bytes([96]) * (w * 3)
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(row * h, 9)) + chunk(b"IEND", b""))


def find_ref(refs: Path, names: list[str], size: tuple[int, int], placeholders: bool, missing: list[str]) -> Path:
    for name in names:
        if (refs / name).is_file():
            return refs / name
    if placeholders:
        write_png(refs / names[-1], size)
        return refs / names[-1]
    missing.append(names[-1])
    return refs / names[-1]


def build_manifests(parsed: dict, en: dict, cast: dict, args) -> list[Path]:
    ep = parsed["episode"]
    chars = {c["id"]: c for c in cast["characters"]}
    looks = {(c["id"], s["id"]): s["appearance"] for c in cast["characters"] for s in c.get("shot_looks", [])}
    refs, work = Path(args.refs).resolve(), Path(args.work).resolve()
    only = set(args.only.split(",")) if args.only else None
    (work / "prompts").mkdir(parents=True, exist_ok=True)
    jobs, missing = [], []
    for sc in parsed["scenes"]:
        for s in sc["shots"]:
            if only and s["id"] not in only:
                continue
            e = en["shots"][s["id"]]
            images, anchors = [], []
            for cid in e.get("ref_characters", e.get("characters", []))[:3]:
                look = (e.get("looks") or {}).get(cid)
                names = ([f"{cid}-{look}-t1.png"] if look else []) + [f"{cid}-portrait-t1.png"]
                images.append(find_ref(refs, names, (1248, 1664), args.placeholders, missing))
                text = looks.get((cid, look)) or chars[cid]["appearance"]
                anchors.append(f"{EN_NAMES.get(cid, chars[cid]['name'])} shown in <Picture {len(images)}> keeps exactly the same face, hair and costume as the picture: {text}")
            set_id = e.get("set") or (sc["sets"][0] if sc["sets"] else None)
            if set_id:
                lamp = e.get("lamp")
                names = ([f"set-{set_id}-lamp{lamp}-t1.png"] if lamp else []) + [f"set-{set_id}-t1.png"]
                images.append(find_ref(refs, names, (1920, 1088), args.placeholders, missing))
                anchors.append(f"the location shown in <Picture {len(images)}> is the set, keeping its layout and props")
            lamp_text = f" The brass oil lamp shows {cast['lamp']['levels'][str(e['lamp'])]}; the light stays as it is through the shot." if e.get("lamp") and not e.get("lamp_changes") else ""
            tags = ", ".join(f"<Picture {i}>" for i in range(1, len(images))) + (f" and <Picture {len(images)}>" if len(images) > 1 else "<Picture 1>")
            body = (f"For the target video, {tags} are referenced throughout.\n\n"
                    f"integrated_multimodal_description: [Shot 1] Live-action. " + "; ".join(anchors) + ". "
                    f"Initial composition: {e['prompt']}{lamp_text} {FACES_RULE if e.get('characters') else ''} "
                    f"The camera: {e['camera']}. {TAIL}\noverall_soundscape: N/A\nnon_diegetic_music: N/A\n")
            pf = work / "prompts" / f"{s['id']}.txt"
            pf.write_text(body, encoding="utf-8")
            secs = max(5, min(10, int(-(-((s["seconds"] or 5) + 0.5) // 1))))
            jobs.append({"id": s["id"], "title": f"tai-nainai-e{ep:03d} {s['id']} ref2va", "inference_mode": "reference",
                         "reference_images": [str(p) for p in images], "prompt_file": f"prompts/{s['id']}.txt",
                         "prompt_sha256": hashlib.sha256(pf.read_bytes()).hexdigest(), "duration_seconds": secs,
                         "width": args.width, "height": args.height, "output_path": str(work / "out" / f"{s['id']}.mp4"),
                         "seed": 700000 + ep * 100 + len(jobs)})
    if missing:
        raise SystemExit("缺參考圖（先畫或加 --placeholders 做離線檢查）：" + ", ".join(sorted(set(missing))))
    out = []
    for i in range(0, len(jobs), 20):
        p = work / f"ref-e{ep:03d}-part{i // 20 + 1}.json"
        p.write_text(json.dumps({"jobs": jobs[i:i + 20]}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        out.append(p)
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode", type=int)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--manifest", action="store_true")
    ap.add_argument("--refs")
    ap.add_argument("--work")
    ap.add_argument("--width", type=int, default=960)
    ap.add_argument("--height", type=int, default=544)
    ap.add_argument("--only")
    ap.add_argument("--placeholders", action="store_true")
    a = ap.parse_args(argv)
    parsed, en, cast = load(a.episode)
    problems = drift(parsed, en)
    if problems:
        print("\n".join(problems))
        return 1
    if a.check:
        print(f"e{a.episode:03d}: {sum(len(s['shots']) for s in parsed['scenes'])} 鏡，英文正文都對得上 script.md")
        return 0
    if a.manifest:
        if not (a.refs and a.work):
            ap.error("--manifest needs --refs and --work")
        for p in build_manifests(parsed, en, cast, a):
            print(p)
        return 0
    video, brief = build_video(parsed, en, cast)
    d = episode_dir(a.episode)
    (d / "video.json").write_text(json.dumps(video, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (d / "brief.md").write_text(brief, encoding="utf-8")
    print(f"{d / 'video.json'}: {len(video['scenes'])} 鏡、{sum(len(s['lines']) for s in video['scenes'])} 句、{len(video['characters'])} 個角色")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
