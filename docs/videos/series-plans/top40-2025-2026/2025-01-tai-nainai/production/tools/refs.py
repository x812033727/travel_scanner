#!/usr/bin/env python3
"""《恁祖媽今年18》的定妝照與場景圖：產生 `h3.sh images` 的 manifest（Qwen-Image-Edit，標準函式庫）。

  refs.py portraits --ids yuetang-18,yuetang-18:shouyi,fubo [--takes 2] --work DIR
  refs.py aged --from DIR/yuetang-18-shouyi-t1.png [--takes 2] --work DIR      # 九十六歲以十八歲為 image 1
  refs.py sets --ids shenjia-citang:1,shenjia-citang:3,shenjia-zhengting [--takes 2] --work DIR
  refs.py props --ids changmingdeng,baoxinling [--takes 1] --work DIR
  refs.py looks --ids meifeng:home,xiaoman:damp --base DIR [--takes 1] --work DIR   # 換裝：以 DIR/<id>-portrait-t1.png 為 image 1 只換衣服

產出 `DIR/refs-<kind>.json`，圖片名照 compile.py 找參考圖的規則：`<id>-portrait-tN.png`、換裝 `<id>-<look>-tN.png`、
`set-<場景>-tN.png`（有燈的分數 `set-<場景>-lamp<N>-tN.png`）、`prop-<道具>-tN.png`；N 是 take。選定之後改名成 t1 放進 refs。
寫法照 `minimax-h3-colab/references/lessons.md` 第 9、13 節：第一張以空白灰底當 image 1；胸像只貼頭肩看得到的外貌；
不寫 film still；場景寫空房間、空白的牌匾、從門口看的左右。
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAST = HERE.parent / "cast.json"
PORTRAIT, SET, PROP = (1248, 1664), (1920, 1088), (1312, 736)

REAL = ("Style: a photorealistic live-action photograph for a modern Taiwanese family drama, shot on a cinema camera with an 85mm lens, "
        "natural soft key light, realistic skin with fine pores and natural texture, realistic hair and fabric, shallow depth of field. "
        "Not a painting, not 3D CG, not anime, not a cartoon. The picture fills the whole frame edge to edge: no black bars, no letterbox, no border. "
        "Clean image with nothing written anywhere, no watermark, no logo, no signature.")
BLANK = "image 1 is only a blank mid-grey canvas: take nothing from it but the plain grey backdrop."
FRAME = ("A tight head-and-shoulders casting portrait: the frame ends just below the collarbones and the face fills the upper half of the frame, large and sharp. "
         "Front view, looking at the camera, calm neutral expression, mouth closed, not smiling. Plain mid-grey studio backdrop. "
         "Only the head, neck and shoulders are in the frame: no hands, no legs, no feet. ")
BODY_ONLY = ("shoes", "heels", "hands folded", "hand", "back very straight", "back still straight", "trousers", "skirt", "ring")
# 試鏡學到的：只寫「eighteen」會畫成二三十歲；福伯不寫老相會畫成七十歲；辮子要寫「only one」
EXTRA = {
    "yuetang-18": "a young girl of eighteen with a youthful teenage face, smooth young skin and a fresh, delicate classical beauty, clearly a teenager and not an adult woman; ",
    "fubo": "a very old man of eighty-eight, clearly near ninety: sunken cheeks, a thin neck, deep lines and a few age spots, thin white eyebrows; ",
}
HAIR = {"yuetang-18": " Her hair is gathered into ONE single thick braid that hangs in front of her right shoulder (on the left side of the picture); there is no second braid."}
SET_LAYOUT = {
    "shenjia-citang": ("Layout seen from the doorway: the long altar table across the back wall with the lamp in its middle and one red candle on each side of the lamp; "
                       "the medicine cabinet stands against the LEFT wall; the round bronze mirror on its wooden stand and the reclining chair are on the RIGHT side; "
                       "the lamp is small, about thirty centimetres tall, its little flame burning inside the clear glass chimney."),
}
NO_TEXT = ("The room is completely empty, with nobody in it. No hanging scrolls, no calligraphy, no couplets. "
           "Every tablet, plaque, board and wall is plain and blank, bare wood and bare plaster.")


def bust(look: str) -> str:
    keep = [p for p in look.split(", ") if not any(re.search(rf"\b{w}\b", p) for w in BODY_ONLY)]
    return ", ".join(p for p in keep if p.strip() not in ("clearly visible", "barely visible"))  # a clause split off a hand sentence


def write_png(path: Path, size: tuple[int, int]) -> None:
    w, h = size
    row = b"\x00" + bytes([128]) * (w * 3)
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(row * h, 9)) + chunk(b"IEND", b""))


def job(id_: str, refs: list[str], prompt: str, size: tuple[int, int], seed: int) -> dict:
    return {"id": id_, "title": id_, "reference_images": refs, "prompt": prompt, "width": size[0], "height": size[1], "seed": seed,
            "lora": False, "steps": 20, "cfg": 4, "latent": "empty", "output_name": f"{id_}.png"}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=["portraits", "aged", "sets", "props", "looks"])
    ap.add_argument("--base", help="looks: the folder with the chosen <id>-portrait-t1.png")
    ap.add_argument("--ids", default="")
    ap.add_argument("--from", dest="src")
    ap.add_argument("--takes", type=int, default=2)
    ap.add_argument("--first-take", type=int, default=1)
    ap.add_argument("--seed", type=int, default=620000)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    cast = json.loads(CAST.read_text(encoding="utf-8"))
    chars = {c["id"]: c for c in cast["characters"]}
    looks = {(c["id"], s["id"]): s["appearance"] for c in cast["characters"] for s in c.get("shot_looks", [])}
    work = Path(a.work).resolve()
    write_png(work / "base" / "grey-portrait.png", PORTRAIT)
    write_png(work / "base" / "grey-set.png", SET)
    write_png(work / "base" / "grey-prop.png", PROP)
    takes = range(a.first_take, a.first_take + a.takes)
    jobs, seed = [], a.seed
    if a.kind == "portraits":
        for item in a.ids.split(","):
            cid, _, look = item.partition(":")
            text = looks[(cid, look)] if look else chars[cid]["appearance"]
            pron = "He" if re.search(r"\b(man|boy)\b", chars[cid]["appearance"]) else "She"
            name = f"{cid}-{look}" if look else f"{cid}-portrait"
            for t in takes:
                prompt = f"{BLANK} {FRAME}{pron} is: {EXTRA.get(cid, '')}{bust(text)}.{HAIR.get(cid, '')} {pron} is the only person in the frame. {REAL}"
                jobs.append(job(f"{name}-t{t}", ["base/grey-portrait.png"], prompt, PORTRAIT, seed)); seed += 1
    elif a.kind == "aged":
        src = Path(a.src).resolve()
        if not src.is_file():
            sys.exit(f"refs.py: {src} not found")
        old = bust(chars["yuetang-96"]["appearance"])
        for t in takes:
            prompt = ("image 1 is the casting photo of Shen Yuetang at eighteen. Show the SAME woman seventy-eight years later, at ninety-six: "
                      "keep her brow shape, eye shape, the structure of her face and her calm gaze from image 1 so anyone can tell it is the same person, "
                      "and keep the framing, the plain grey backdrop and the lighting of image 1. "
                      f"{FRAME}She is: {old}. Her thin white hair is in ONE single thin braid in front of her right shoulder. She is the only person in the frame. {REAL}")
            jobs.append(job(f"yuetang-96-portrait-t{t}", [str(src)], prompt, PORTRAIT, seed)); seed += 1
    elif a.kind == "sets":
        sets = {s["id"]: s["prompt"] for s in cast["sets"]}
        for item in a.ids.split(","):
            sid, _, lamp = item.partition(":")
            text = sets[sid].replace("ancestral tablets behind it out of focus", "a row of plain blank wooden ancestral tablets behind it, out of focus")
            if lamp:
                text += f"; the lamp shows {cast['lamp']['levels'][lamp]}"
            name = f"set-{sid}-lamp{lamp}" if lamp else f"set-{sid}"
            for t in takes:
                prompt = (f"image 1 is only a blank mid-grey canvas: take nothing from it. A wide shot of an empty room at night: {text}. "
                          f"{SET_LAYOUT.get(sid, '')} {NO_TEXT} {REAL}")
                jobs.append(job(f"{name}-t{t}", ["base/grey-set.png"], prompt, SET, seed)); seed += 1
    elif a.kind == "looks":
        # 分開畫的兩個 look 會是兩個人（2026-11-06 試鏡）：以選定的基本款為 image 1、latent image1，只換衣服
        base = Path(a.base or "").resolve()
        for item in a.ids.split(","):
            cid, _, look = item.partition(":")
            src = base / f"{cid}-portrait-t1.png"
            if not src.is_file():
                sys.exit(f"refs.py: {src} not found; choose the base portrait first")
            for t in takes:
                prompt = (f"Edit image 1: keep the face, skin, hairstyle, the framing, the plain grey backdrop and the lighting exactly the same. "
                          f"Change only what differs in this look: {bust(looks[(cid, look)])}. {REAL}")
                jobs.append(dict(job(f"{cid}-{look}-t{t}", [str(src)], prompt, PORTRAIT, seed), latent="image1")); seed += 1
    else:
        props = {p["id"]: p for p in cast["props"]}
        for pid in a.ids.split(","):
            for t in takes:
                prompt = (f"image 1 is only a blank mid-grey canvas: take nothing from it but the plain grey backdrop. A product-style reference photograph of one object "
                          f"alone on a plain mid-grey backdrop, centred and fully in frame: {props[pid]['prompt']}. Nothing else in the frame. {REAL}")
                jobs.append(job(f"prop-{pid.removeprefix('prop-')}-t{t}", ["base/grey-prop.png"], prompt, PROP, seed)); seed += 1
    out = work / f"refs-{a.kind}.json"
    out.write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{out}: {len(jobs)} jobs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
