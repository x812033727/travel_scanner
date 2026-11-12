#!/usr/bin/env python3
"""第 7 集首格第二輪（2026-11-10）：第一輪獨立挑圖 26 鏡定 12 鏡，其餘照審稿的改法 -> stills-redo2.json。

- 修圖（latent image1，refs 第一張是最接近的候選 `ST:<檔名>`，在 $TN_WORK/e007ff/st/）：c04、c06、c07、c13、c15、c22，
  c14（第一輪 B 左右翻轉後補淚光）；已選的 c05、c08、c20 抹掉背景模糊的招牌字（`PICK:<鏡>`）。
- 重畫（照 stills.json 原句，前面加審稿的規則）：c01、c09、c12、c25、c26、c27、c29。
教訓：模型會在公車上放乘客、在院子掛燈籠；林美鳳拿著壽衣會變成穿在身上；用 image N 指人容易左右對調，改用外貌與位置描述。
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills-redo2.json"
BASE = {s["shot"]: s for s in json.loads((HERE / "stills.json").read_text(encoding="utf-8"))}
NOTEXT = "No subtitles, no captions, no text, numbers, signs, LED displays or screens anywhere in the picture."
KEEP = "Keep everything else exactly the same: the place, the light, the camera angle, faces, hair and clothes. No other change. "
NOLANTERN = "No lanterns, no hanging lamps with tassels anywhere."
ROBE = ("an empty off-white burial robe exactly like the one in the robe picture (high stand-up collar, frog buttons down the right side, "
        "long sleeves, mid-calf length), only the robe, no trousers")
S = []


def edit(shot, ref, prompt):
    S.append({"shot": shot, "shares_with": [], "refs": [ref], "prompt": prompt + " " + KEEP + NOTEXT, "latent": "image1"})


def redraw(shot, rules, refs=None):
    b = BASE[shot]
    s = {"shot": shot, "shares_with": b["shares_with"], "refs": refs or b["refs"], "prompt": rules + " " + b["prompt"]}
    if b.get("latent"):
        s["latent"] = b["latent"]
    S.append(s)


edit("c04", "ST:c04-b.png", "Edit image 1. Remove the card and the left hand completely. Her bare right hand rests flat on top of the small grey box, right beside the "
     "one copper coin lying on the box; she holds nothing.")
edit("c06", "ST:c06-a.png", "Edit image 1. Remove the blurred passenger's head behind her right shoulder at the lower right, replacing it with plain bus window. "
     "Her eyes look down to the lower left.")
edit("c07", "ST:c07-b.png", "Edit image 1. Remove the orange LED display and every sign. His eyes are wide and fixed on the phone on the selfie stick, eyebrows "
     "raised high, a wide excited closed-mouth grin.")
edit("c13", "ST:c13-a.png", "Edit image 1. The blurred person at the left edge becomes a different girl seen only from behind: a blurred NAVY school-blazer "
     "shoulder and the back of a black high ponytail, no face, no cheek, no light-brown hair. The light-brown-haired girl on the right lifts one corner of "
     "her mouth in a sneer, not smiling, no teeth.")
edit("c14", "ST:c14-bflip.png", "Edit image 1. Her eyes glisten with clear tears, no redness, no red marks; brows pushed up and together; lips pressed and "
     "trembling. Behind her the gate is a plain vertical-bar metal gate in a cream wall with a dark red base.")
edit("c15", "ST:c15-a.png", "Edit image 1. The plastic cup has NO lid at all, its open rim visible, one straw standing in the milk tea; the school bag below is "
     "unzipped with its mouth open upward and the cup held just above that opening, not yet pouring; one corner of her mouth lifted in a sneer, no teeth.")
edit("c22", "ST:c22-a.png", "Edit image 1. The cup has NO lid, no print, it is an empty clear plastic cup with one straw; her expression: one eyebrow raised, "
     "mouth corners turned down, looking down at the person in front of her, not smiling.")
edit("c05", "PICK:c05", "Edit image 1. Remove the blurred red shop sign outside the left window and the red-and-yellow sticker on the upper right of the windshield, "
     "leaving plain blurred street and clear glass.")
edit("c08", "PICK:c08", "Edit image 1. Remove the small red sign in the background, leaving plain bus wall.")
edit("c20", "PICK:c20", "Edit image 1. Make the square and round plaques on both gate pillars plain blank, with nothing on them.")

redraw("c01", "Every seat in view is EMPTY: no seated passengers, no heads above any seat back, nobody else on the bus except the people described. "
       "The young woman at the front has her face clearly visible in three-quarter profile turned toward screen left, LONG sleeves to the wrist, a NAVY "
       "ankle-length skirt. The schoolgirl wears white ankle socks and a navy pleated skirt below the knee.")
redraw("c09", "In the foreground only a thin blurred sliver of a young woman's RIGHT shoulder and the black braid lying over it at the far LEFT edge, less "
       "than one fifth of the frame, her head out of frame, no cheek. No seated passengers, no LED display, no route number.")
redraw("c12", "Positions are fixed: on the RIGHT, standing in front of the wall right of the guard booth, a girl with LONG STRAIGHT LIGHT-BROWN hair, no "
       "bangs, holding an open navy school bag in one hand and a lidless clear plastic cup of milk tea with a straw in the other; on the LEFT, just "
       "stepping in from the left edge, a girl with BLUNT BANGS and a BLACK HIGH PONYTAIL hugging a white paper bag, no school bag. Both faces in "
       "three-quarter profile toward each other, neither looks at the camera.")
redraw("c25", "The young woman in the foreground is cropped by the RIGHT frame edge, filling the right quarter, very blurred, seen only from behind, a "
       f"navy school bag hanging from her left hand. The woman in the wine-red dress holds {ROBE}, folded flat into a neat rectangle against her chest, the "
       f"stand-up collar visible on top; her face in three-quarter profile turned toward screen right toward the foreground figure, not toward the camera. {NOLANTERN}")
redraw("c26", "The foreground shows only the back of a young woman's head and left shoulder at the RIGHT edge, blurred, no cheek, no nose, her hair in "
       "one black braid. The woman in the wine-red dress has her head turned 45 degrees toward screen right, a thin fake smile with closed lips, holding "
       f"{ROBE} folded flat against her chest. {NOLANTERN}")
redraw("c27", f"She is NOT wearing the robe; she wears only her wine-red knit dress. She holds {ROBE} up by its shoulder seams with both hands, shaken "
       "open and hanging down, held out toward screen right at arm's length like showing a garment; her face in three-quarter profile toward screen "
       f"right, a cold smile with closed lips. {NOLANTERN}")
redraw("c29", "Exactly one blurred shoulder at the RIGHT edge only, nothing at the left edge. She is NOT wearing the robe; she wears her wine-red knit "
       f"dress and holds {ROBE} up by its shoulder seams with both hands, shaken open, held out toward screen right; her face in three-quarter profile "
       f"toward screen right, glaring, not smiling. {NOLANTERN}")


if __name__ == "__main__":
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(OUT, len(S))
