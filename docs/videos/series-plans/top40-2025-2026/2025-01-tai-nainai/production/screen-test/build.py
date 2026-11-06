#!/usr/bin/env python3
"""《祖奶奶今年十八》試鏡：從 cast.json 產生 Colab 的 manifest 與提示詞（不花錢、不碰權杖）。

  build.py r1    [--work DIR] [--placeholders]
      第一輪定妝照與場景圖（Qwen-Image-Edit）：image 1 是一張空白灰底（這部還沒有定妝照可當參考）。
  build.py r2    --pick yuetang-18=a --pick yuetang-18-3d=a [--work DIR] [--placeholders]
      第二輪：以選中的十八歲為 image 1 畫九十六歲（一人兩貌）與手背細紋插鏡。
  build.py st1   --pick meifeng=a --pick yuetang-96=a --pick meifeng-3d=a [--work DIR] [--placeholders]
      片段第一段：Ref2VA 960×544（跑之前 `H3_PROFILE=hero bootstrap.sh patch`）。
  build.py st2   [--work DIR]
      片段第二段：草稿第 0 格 cover-crop 到 1312×736 當 keyframe，σ0.5（要 ffmpeg 與 st1/out/*.mp4）。

圖片工具把輸出檔名的「/」換成「-」，所以檔案是 r1-<id>.png。--pick 的值是 take 字母（r1 的 a、b）；沒給的角色用 a。--placeholders 在缺圖的地方先放一張灰圖，
只給離線檢查用（check 過了不代表圖畫好了）。工作目錄預設 $VIDEO_WORKDIR/_series/tai-nainai/screen-test
（沒設時 ~/mokaair-work/videos/...）；定妝照 manifest 的路徑相對 manifest 所在的目錄，片段的用絕對路徑。標準函式庫，用 python3 -I 跑。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAST = HERE.parent / "cast.json"

PORTRAIT = (1248, 1664)  # 3:4 胸像，跟《種田》的定妝照同構圖
SET = (1920, 1088)
INSERT = (1312, 736)
DRAFT = (960, 544)

REAL = (
    "Style: a photorealistic live-action photograph for a modern Taiwanese family drama, shot on a cinema camera with an 85mm lens, "
    "natural soft key light, realistic skin with fine pores and natural texture, realistic hair and fabric, shallow depth of field. "
    "Not a painting, not 3D CG, not anime, not a cartoon. The picture fills the whole frame edge to edge: no black bars, no letterbox, no border. "
    "Clean image with nothing written anywhere, no watermark, no logo, no signature."
)
CG = (
    "Style: a high-end 3D CG animated drama still, Unreal Engine 5 cinematic character render: stylized semi-realistic characters with refined faces, "
    "detailed skin that is clearly CG and not a photograph, individually rendered hair strands, physically simulated cloth, warm cinematic light, "
    "shallow depth of field. Not a photograph, not live action, not anime. The picture fills the whole frame edge to edge: no black bars, no letterbox, no border. "
    "Clean image with nothing written anywhere, no watermark, no logo, no signature."
)
BLANK = "image 1 is only a blank mid-grey canvas: take nothing from it but the plain grey backdrop."
PORTRAIT_FRAME = (
    "A tight head-and-shoulders casting portrait: the frame ends just below the collarbones and the face fills the upper half of the frame, large and sharp. "
    "Front view, looking at the camera, calm neutral expression, mouth closed, not smiling. Plain mid-grey studio backdrop. "
    "Only the head, neck and shoulders are in the frame: no hands, no legs, no feet. "
)
YOUTH = "a young girl of eighteen with a youthful teenage face, smooth young skin and a fresh, delicate beauty, clearly a teenager and not an adult woman; "
BODY_ONLY = ("shoes", "heels", "hands folded", "back very straight", "back still straight", "trousers", "skirt", "ring")


def bust(look: str) -> str:
    """The appearance without what a head-and-shoulders frame cannot show (shoes, hands, skirt): those pull the model to full body."""
    keep = [part for part in look.split(", ") if not any(re.search(rf"\b{word}\b", part) for word in BODY_ONLY)]
    return ", ".join(keep)
NO_TEXT_SET = (
    "The room is completely empty, with nobody in it. No hanging scrolls, no calligraphy, no couplets. "
    "Every tablet, plaque, board and wall is plain and blank, bare wood and bare plaster."
)

CLIP_TAIL_REAL = "One continuous shot. Natural, realistic live-action human motion; faces, hair and costumes stay as in their reference pictures."
CLIP_TAIL_CG = "One continuous shot. Smooth, weighty 3D CG character animation; faces, hair and costumes stay as in their reference pictures."
FACES_RULE = (
    "Besides them, only the other people the composition names are in the frame; no second copy of anyone appears. "
    "Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the face, hair and costume only, never the mood."
)


def load_cast() -> dict:
    cast = json.loads(CAST.read_text(encoding="utf-8"))
    chars = {c["id"]: c for c in cast["characters"]}
    looks = {(c["id"], s["id"]): s["appearance"] for c in cast["characters"] for s in c.get("shot_looks", [])}
    sets = {s["id"]: s["prompt"] for s in cast["sets"]}
    return {"chars": chars, "looks": looks, "sets": sets, "lamp": cast["lamp"]["levels"]}


def write_png(path: Path, size: tuple[int, int], grey: int = 128) -> None:
    w, h = size
    row = b"\x00" + bytes([grey]) * (w * 3)
    raw = zlib.compress(row * h, 9)

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + chunk(b"IDAT", raw) + chunk(b"IEND", b""))


def work_dir(flag: str | None) -> Path:
    if flag:
        return Path(flag).expanduser().resolve()
    base = Path(os.environ.get("VIDEO_WORKDIR") or Path.home() / "mokaair-work" / "videos")
    return base / "_series" / "tai-nainai" / "screen-test"


def need(path: Path, size: tuple[int, int], placeholders: bool) -> None:
    if path.is_file() and path.stat().st_size:
        return
    if not placeholders:
        sys.exit(f"build.py: {path} is missing; draw it first, pick another take with --pick, or pass --placeholders for an offline check")
    write_png(path, size, grey=96)
    print(f"placeholder: {path}")


def job(id_: str, title: str, refs: list[str], prompt: str, size: tuple[int, int], seed: int, out: str) -> dict:
    return {
        "id": id_, "title": title, "reference_images": refs, "prompt": prompt,
        "width": size[0], "height": size[1], "seed": seed, "lora": False, "steps": 20, "cfg": 4,
        "latent": "empty", "output_name": out,
    }


def r1(cast: dict, work: Path) -> dict:
    write_png(work / "base" / "grey-portrait.png", PORTRAIT)
    write_png(work / "base" / "grey-set.png", SET)
    c, looks, sets = cast["chars"], cast["looks"], cast["sets"]
    people = [
        ("yuetang-18", "沈月棠（十八歲，壽衣）", YOUTH + bust(looks[("yuetang-18", "shouyi")]), "She"),
        ("meifeng", "林美鳳", bust(c["meifeng"]["appearance"]), "She"),
        ("fubo", "福伯", bust(c["fubo"]["appearance"]), "He"),
    ]
    jobs = []
    seed = 611000
    for pid, title, look, pron in people:
        for take in ("a", "b"):
            prompt = f"{BLANK} {PORTRAIT_FRAME}{pron} is: {look}. {pron} is the only person in the frame. {REAL}"
            jobs.append(job(f"{pid}-{take}", f"{title} 真人 {take}", ["base/grey-portrait.png"], prompt, PORTRAIT, seed, f"r1-{pid}-{take}.png"))
            seed += 1
        prompt = f"{BLANK} {PORTRAIT_FRAME}{pron} is: {look}. {pron} is the only person in the frame. {CG}"
        jobs.append(job(f"{pid}-3d-a", f"{title} 3D", ["base/grey-portrait.png"], prompt, PORTRAIT, seed, f"r1-{pid}-3d-a.png"))
        seed += 1
    citang = (sets["shenjia-citang"]
              .replace("ancestral tablets behind it out of focus", "a row of plain blank wooden ancestral tablets behind it, out of focus")
              .replace("red candles", "two red candles, one on each side of the lamp"))
    citang += (f"; the lamp shows {cast['lamp']['3']}, the small flame burning inside the clear glass chimney. "
               "Layout seen from the doorway: the altar table across the back wall, the medicine cabinet against the LEFT wall, "
               "the round bronze mirror on its wooden stand and the reclining chair on the RIGHT side")
    zhengting = sets["shenjia-zhengting"]
    for sid, title, text, style, tag in [
        ("set-citang", "祠堂 真人", citang, REAL, "a"),
        ("set-zhengting", "正廳 真人", zhengting, REAL, "a"),
        ("set-zhengting-3d", "正廳 3D", zhengting, CG, "a"),
    ]:
        prompt = (
            "image 1 is only a blank mid-grey canvas: take nothing from it. A wide shot of an empty room at night: "
            f"{text}. {NO_TEXT_SET} {style}"
        )
        jobs.append(job(f"{sid}-{tag}", title, ["base/grey-set.png"], prompt, SET, seed, f"r1-{sid}-{tag}.png"))
        seed += 1
    return {"jobs": jobs}


def r2(cast: dict, work: Path, pick: dict, placeholders: bool) -> dict:
    c, looks = cast["chars"], cast["looks"]
    old = bust(c["yuetang-96"]["appearance"])
    jobs = []
    for suffix, style, seed in (("", REAL, 612000), ("-3d", CG, 612010)):
        young = f"r1-yuetang-18{suffix}-{pick.get('yuetang-18' + suffix, 'a')}.png"
        need(work / young, PORTRAIT, placeholders)
        takes = ("c", "d") if not suffix else ("b",)  # a/b（全身，2026-11-06 第一次）臉太小，改畫胸像
        for n, take in enumerate(takes):
            prompt = (
                "image 1 is the casting photo of Shen Yuetang at eighteen. Show the SAME woman seventy-eight years later, at ninety-six: "
                "keep her brow shape, eye shape, the structure of her face and her calm gaze from image 1 so anyone can tell it is the same person, "
                "and keep the framing, the plain grey backdrop and the lighting of image 1. "
                f"{PORTRAIT_FRAME}She is: {old}. She is the only person in the frame. {style}"
            )
            jobs.append(job(f"yuetang-96{suffix}-{take}", f"沈月棠（九十六歲）{'3D' if suffix else '真人'} {take}", [young], prompt, PORTRAIT, seed + n, f"r2-yuetang-96{suffix}-{take}.png"))
    young = f"r1-yuetang-18-{pick.get('yuetang-18', 'a')}.png"
    prompt = (
        "image 1 is the casting photo of the young woman Shen Yuetang: keep her skin tone and the moon-white cotton sleeves. "
        "An extreme close-up insert of her two hands folded in front of her waist, the right hand resting on the left, the moon-white long cotton cuffs at the wrists, "
        "a thick old silver ring on her left ring finger with its small square seal face turned toward the palm; "
        "the back of her right hand is young and smooth except for one single fine wrinkle line across it, clearly visible in soft light; nothing else is aged. "
        f"{looks[('yuetang-18', 'wrinkle')]}. Only the hands and cuffs are in the frame, no face. {REAL}"
    )
    jobs.append(job("insert-wrinkle-a", "手背細紋插鏡 真人", [young], prompt, INSERT, 612020, "r2-insert-wrinkle-a.png"))
    return {"jobs": jobs}


SHOTS = [
    # id, 誰（角色 id, 參考圖鍵）, 場景鍵, 秒, 正文（構圖與動作）
    {
        "id": "e001-c14", "who": [("meifeng", "Lin Meifeng")], "set": "set-zhengting", "seconds": 6, "style": "real",
        "composition": "Inside the main hall of the old Shen house at night under a warm hanging lamp: a medium close-up of Lin Meifeng standing on screen left by the long dark rosewood table, "
        "her face turned toward the small courtyard door at the back of screen right, the plain white plaster wall behind her. She is the only person in the frame.",
        "action": "She stares at the doorway; her smile fades little by little until it is gone, and she drops her hands. Lin Meifeng speaks a Mandarin line, 「這丫頭跑什麼跑，那串破鈴鐺，吵死人了」, "
        "her lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes, impatient and sharp. The camera pushes in with small amplitude at slow speed.",
    },
    {
        "id": "e001-c17", "who": [("yuetang-96", "Shen Yuetang at ninety-six")], "set": "set-citang", "seconds": 5, "style": "real", "lamp": "1",
        "composition": "Inside the dim ancestral hall of the old Shen house at night: a close-up of Shen Yuetang at ninety-six leaning back in an old wooden reclining chair with a cane seat, "
        "her head resting against the chair back, her hands folded; out of focus at the back of screen left the small glow of the lamp chimney; behind her only a dark wall and one corner of the bronze mirror's wooden stand. "
        "She is the only person in the frame.",
        "action": "She slowly closes her eyes and lets out one long breath; her folded hands loosen a little but stay folded. Her mouth stays closed. Her face is calm and dignified, not sickly; this is not a death scene, "
        "the lamp keeps burning. The camera pushes in with small amplitude at slow speed, from her chest to her face.",
    },
    {
        "id": "e001-c20", "who": [("yuetang-18", "Shen Yuetang")], "set": "set-citang", "seconds": 6, "style": "real", "lamp": "3",
        "composition": "Inside the ancestral hall of the old Shen house at night: a medium close-up of the eighteen-year-old Shen Yuetang sitting in an old wooden reclining chair, wearing the off-white burial robe, "
        "her thick black braid over her right shoulder; behind her only a dark wall and the bronze mirror's wooden stand; warm orange-gold lamplight from screen left. She is the only person in the frame.",
        "action": "She pushes on the armrest and sits up straight, then raises both hands in front of her eyes: the backs of her hands are young and smooth, the thick old silver ring sits snugly on her left ring finger. "
        "She turns her palms up, turns them back, and slowly bends and straightens her fingers, five fingers on each hand. Her mouth stays closed; her look is quiet disbelief, not smiling. "
        "The camera pushes in with small amplitude at slow speed.",
    },
    {
        "id": "e001-c23", "who": [("yuetang-18", "Shen Yuetang")], "set": "set-citang", "seconds": 6, "style": "real", "lamp": "3",
        "composition": "Inside the ancestral hall of the old Shen house at night: a close-up of the eighteen-year-old Shen Yuetang from the chest up, the stand-up collar of the off-white burial robe buttoned to her throat; "
        "warm orange-gold lamplight and candlelight from screen left outline her oval face; behind her only a dark wall. She is the only person in the frame.",
        "action": "She lowers her hand and, by old habit, folds both hands at her waist; she turns her head to look toward the lamp on screen left with a calm, deep gaze, then lowers her eyes to the cuff of her robe. "
        "Her mouth stays closed, she is not smiling. The camera pushes in with small amplitude at slow speed, from her chest to her face.",
    },
]
SHOTS.append({**SHOTS[0], "id": "e001-c14-3d", "style": "cg"})


def appearance(cast: dict, pid: str) -> str:
    if pid == "yuetang-18":
        return cast["looks"][("yuetang-18", "shouyi")]
    return cast["chars"][pid]["appearance"]


def st1(cast: dict, work: Path, pick: dict, placeholders: bool) -> dict:
    jobs = []
    (work / "st1" / "prompts").mkdir(parents=True, exist_ok=True)
    for n, shot in enumerate(SHOTS):
        cg = shot["style"] == "cg"
        suffix = "-3d" if cg else ""
        refs, anchors = [], []
        for pid, name in shot["who"]:
            folder = "r2" if pid == "yuetang-96" else "r1"
            ref = work / f"{folder}-{pid}{suffix}-{pick.get(pid + suffix, 'a')}.png"
            need(ref, PORTRAIT, placeholders)
            refs.append(str(ref))
            anchors.append(f"{name} shown in <Picture {len(refs)}> keeps exactly the same face, hair and costume as the picture: {appearance(cast, pid)}")
        set_ref = work / f"r1-{shot['set']}{suffix}-a.png"
        need(set_ref, SET, placeholders)
        refs.append(str(set_ref))
        tags = ", ".join(f"<Picture {i}>" for i in range(1, len(refs))) + f" and <Picture {len(refs)}>"
        lamp = f" On the altar the brass oil lamp shows {cast['lamp'][shot['lamp']]}; the light stays steady through the shot." if shot.get("lamp") else ""
        style = "3D CG." if cg else "Live-action."
        prompt = (
            f"For the target video, {tags} are referenced throughout.\n\n"
            f"integrated_multimodal_description: [Shot 1] {style} " + "; ".join(anchors) +
            f"; the location shown in <Picture {len(refs)}> is the set, keeping its layout and props. "
            f"Initial composition: {shot['composition']}{lamp} {FACES_RULE} {shot['action']} {CLIP_TAIL_CG if cg else CLIP_TAIL_REAL}\n"
            "overall_soundscape: N/A\nnon_diegetic_music: N/A\n"
        )
        pf = work / "st1" / "prompts" / f"{shot['id']}.txt"
        pf.write_text(prompt, encoding="utf-8")
        jobs.append({
            "id": shot["id"], "title": f"tai-nainai screen test {shot['id']} ref2va", "inference_mode": "reference",
            "reference_images": refs, "prompt_file": f"prompts/{shot['id']}.txt",
            "prompt_sha256": hashlib.sha256(pf.read_bytes()).hexdigest(), "duration_seconds": shot["seconds"],
            "width": DRAFT[0], "height": DRAFT[1], "output_path": str(work / "st1" / "out" / f"{shot['id']}.mp4"), "seed": 613000 + n,
        })
    return {"jobs": jobs}


def st2(work: Path) -> dict:
    if not shutil.which("ffmpeg"):
        sys.exit("build.py: st2 needs ffmpeg")
    st1m = json.loads((work / "st1" / "st1.json").read_text(encoding="utf-8"))
    jobs = []
    (work / "st2" / "keyframes").mkdir(parents=True, exist_ok=True)
    (work / "st2" / "prompts").mkdir(parents=True, exist_ok=True)
    for j in st1m["jobs"]:
        draft = Path(j["output_path"])
        if not draft.is_file():
            print(f"skip {j['id']}: no draft at {draft}")
            continue
        key = work / "st2" / "keyframes" / f"{j['id']}.png"
        w, h = INSERT
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(draft), "-frames:v", "1",
                        "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}", str(key)], check=True)
        shot = next(s for s in SHOTS if s["id"] == j["id"])
        style = "3D CG." if shot["style"] == "cg" else "Live-action."
        lamp = f" The brass oil lamp shows {load_cast()['lamp'][shot['lamp']]}." if shot.get("lamp") else ""
        prompt = (f"{style} The scene shown in <Picture 1> continues, preserving every face, costume, prop and the set layout. "
                  f"{shot['composition']}{lamp} {shot['action']} {CLIP_TAIL_CG if shot['style'] == 'cg' else CLIP_TAIL_REAL}\n")
        pf = work / "st2" / "prompts" / f"{j['id']}.txt"
        pf.write_text(prompt, encoding="utf-8")
        jobs.append({"id": j["id"], "input_video": str(draft), "first_frame": str(key), "prompt_file": str(pf),
                     "output_name": f"{j['id']}.mp4", "seed": j["seed"], "sigma_start": 0.5, "steps": 10})
    return {"jobs": jobs}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("round", choices=["r1", "r2", "st1", "st2"])
    ap.add_argument("--work")
    ap.add_argument("--pick", action="append", default=[], help="role=take, e.g. yuetang-18=b")
    ap.add_argument("--placeholders", action="store_true")
    a = ap.parse_args(argv)
    pick = dict(p.split("=", 1) for p in a.pick)
    work = work_dir(a.work)
    work.mkdir(parents=True, exist_ok=True)
    cast = load_cast()
    manifest = {"r1": lambda: r1(cast, work), "r2": lambda: r2(cast, work, pick, a.placeholders),
                "st1": lambda: st1(cast, work, pick, a.placeholders), "st2": lambda: st2(work)}[a.round]()
    out = {"r1": work / "r1.json", "r2": work / "r2.json", "st1": work / "st1" / "st1.json", "st2": work / "st2" / "st2.json"}[a.round]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{out}: {len(manifest['jobs'])} jobs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
