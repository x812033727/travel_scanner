#!/usr/bin/env python3
"""第 4 集重拍首格（2026-11-10，站主看片後）：c29、c30、c36 -> fix2-stills.json（與 e006 stills.json 同格式）。

獨立審片：c29 月棠換成較老的臉、c30 外送員跑進屋內且安全帽與袋子換了、c36 林美鳳換了衣服髮型與臉。
連戲照成片裡現有的鏡：外送員照 c27（白色安全帽、灰外套、深色箱型外送袋），林美鳳照 c33（紅棕波浪髮、酒紅針織、珍珠項鍊）。
refs 裡 `CUT:` 是從後台成片抽的格（$TN_WORK/e004fix2/refs/），其他在 refs/。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "e006"))
import make_stills as m  # noqa: E402

OUT = Path(__file__).resolve().parent / "fix2-stills.json"
NOON = "A bright clear noon at the open side door of an old house kitchen"
COURIER = ("a delivery man in his twenties in a plain GREY zip jacket and a plain WHITE motorcycle helmet pulled low, the visor shadow over his eyes, "
           "holding one plain DARK box-shaped insulated delivery bag with no logo")
S = []


def still(shot, refs, prompt):
    S.append({"shot": shot, "shares_with": [], "refs": refs, "prompt": prompt})


still("c29", [m.YT_P, "CUT:ref-c27.png"], (
    f"{m.PRE} {NOON}, seen from just outside the doorway looking in. FIRST, at the LEFT edge of the frame, very close to the lens and heavily blurred: "
    "the right shoulder of a man in a GREY jacket and the back of a plain WHITE helmet, no face. On screen right, a MEDIUM CLOSE-UP, chest up: the "
    f"YOUNG woman from image 1, eighteen years old, smooth young skin, no wrinkles, {m.YT}, standing just inside the doorway, holding a white porcelain bowl "
    "of steaming plain rice porridge in both hands in front of her. Her face in three-quarter profile turned toward screen left, toward the blurred man, "
    "eyes gently curved, brows relaxed, a small kind smile with closed lips, never looking at the camera. Behind her, out of focus: a square wooden "
    "table and a white gas stove in a plain kitchen. " + m.OTS))
still("c30", ["CUT:ref-c27.png", m.YT_P], (
    f"{m.PRE.replace('image 1', 'image 1')} OUTDOORS at noon, seen from inside a kitchen doorway looking OUT. FIRST, at the RIGHT edge of the frame, very "
    "close to the lens and heavily blurred: a young woman's left shoulder in a MOON-WHITE high collar, one black braid over it, and her two hands in "
    "moon-white cuffs holding a white porcelain bowl, no face. On screen left, standing OUTSIDE on the sunlit stone-paved path beyond the doorstep, the "
    f"courtyard wall behind him: ONLY ONE man, {COURIER} from image 1, the helmet's shadow hiding his eyes so only his mouth and chin show, holding the "
    "dark delivery bag up in front of his chest with both hands, mouth corners pulled down, lips pressed, awkward. He does not look at the camera. No "
    "kitchen behind him; only the bright stone path and a grey courtyard wall. " + m.OTS))
still("c36", [m.MF_P, "CUT:ref-c33.png"], (
    f"{m.PRE} {NOON}, seen from inside the kitchen looking toward the open doorway; behind her only the out-of-focus bright stone path outside. A CLOSE-UP, "
    "chest up: ONLY ONE woman, the woman from image 1 dressed exactly as in image 2: shoulder-length glossy AUBURN-brown wavy hair, a fitted WINE-RED "
    "long-sleeved knit dress with a high round neckline, a long pearl necklace, red nails, red lips; her RIGHT hand clutching the pearl necklace at her "
    "throat, her left hand holding the handle of a dark insulated bag at the bottom edge. Her face in three-quarter profile turned toward screen right, "
    "cheeks flushed red, brows pushed up and together, eyes wide and glaring toward screen right, lips tight, not smiling, never looking at the camera. "
    + m.ONE_F))


if __name__ == "__main__":
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(OUT, len(S))
