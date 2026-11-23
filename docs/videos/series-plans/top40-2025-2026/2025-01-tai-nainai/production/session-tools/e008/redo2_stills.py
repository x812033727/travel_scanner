#!/usr/bin/env python3
"""第 8 集首格第二輪（2026-11-11）：第一輪 21 鏡定 11 鏡（含共用），其餘照獨立挑圖的改法 -> stills-redo2.json。

- 修最接近的那張（latent image1，`ST:` 是 $TN_WORK/e008ff/st/）：c03、c04、c07、c08、c13、c14、c21、c25、c26，每張只改一兩件事。
- c05、c19 從場景圖分兩步：這輪是第一步（只放主角），第二步等挑定再加第三個人。
- c11 照救急規則拿掉；c27 第一輪漏畫，照 stills.json 原句畫。
這批反覆出現的錯：正面看鏡頭、壽衣畫成白板、前景變成分身或銀髮、視線方向反、福伯衣服偏深灰（定妝照本身偏灰）。
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills-redo2.json"
BASE = {s["shot"]: s for s in json.loads((HERE / "stills.json").read_text(encoding="utf-8"))}
NOTEXT = "No subtitles, no text anywhere; no screen anywhere."
KEEP = "Keep everything else exactly the same: faces, hair, clothes, positions, expressions, the place, the light and the camera angle. "
ROBE = "the off-white robe of image 2 (only the robe: high stand collar, side frog buttons, long sleeves, no trousers)"
S = []


def edit(shot, refs, prompt):
    S.append({"shot": shot, "shares_with": [], "refs": refs, "prompt": prompt + " " + KEEP + NOTEXT, "latent": "image1"})


edit("c03", ["ST:c03-b.png", "prop-shouyi-t1.png"],
     f"Edit image 1. Exactly two changes. One: put {ROBE} between the two women: the woman in wine-red grips one shoulder of it with her right hand and the "
     "young woman in moon-white grips the other shoulder with her bare right hand, so the robe hangs open between them above the round stone table; neither "
     "woman is wearing it. Two: remove the hanging lanterns; the corridor walls keep only a warm yellow glow; no lanterns, lamps or candles anywhere.")
edit("c04", ["ST:c04-b.png", "prop-shouyi-t1.png"],
     "Edit image 1. Exactly two changes. One: the young woman turns her head into three-quarter profile toward screen left, eyes on the blurred woman at the "
     "left edge, never looking at the camera, brows level, lips closed, not smiling. Two: the flat white board in her hands becomes the off-white cotton robe "
     "of image 2 folded into a soft neat square, its high stand collar and one fabric frog button showing on top. No earrings.")
edit("c07", ["ST:c07-b.png", "prop-shouyi-t1.png"],
     "Edit image 1. Exactly two changes. One: she turns her head into three-quarter profile toward screen left, eyes on someone far beyond the left edge, never "
     "looking at the camera, chin slightly lifted, lips closed, not smiling. Two: the flat white board in her arms becomes the off-white cotton robe of image 2 "
     "folded into a soft neat square, its high stand collar and one fabric frog button showing on top.")
edit("c08", ["ST:c08-b.png"],
     "Edit image 1. Exactly two changes. One: the blurred person at the RIGHT edge becomes the back of a young woman's head with straight glossy BLACK hair and "
     "her left shoulder in a MOON-WHITE high stand-up collar, soft and out of focus; no face, no ear, no earring; no chestnut curls and no wine-red at the right "
     "edge. Two: the woman in wine-red turns her face into three-quarter profile toward screen right, eyes on that blurred young woman, never looking at the "
     "camera, one corner of her red lips curled up in a sneer, no teeth, chin raised.")
edit("c13", ["ST:c13-a.png"],
     "Edit image 1. Exactly two changes. One: the hair of the young woman seen from behind at the right becomes glossy jet-BLACK (not grey, not white), keeping "
     "her one black braid and moon-white collar; only the back of her head, no face, no ear. Two: the old woman in the wheelchair turns her face slightly toward "
     "screen right, eyes on the young woman's back, never looking at the camera, brows pushed up and together, eyes glistening with clear tears, no redness, "
     "mouth open in a cry.")
edit("c14", ["ST:c14-b.png"],
     "Edit image 1. Exactly two changes. One: the old woman in the wheelchair wraps both arms around the young woman's waist, her face lifted toward her; the "
     "young woman's bare right hand rests on the old woman's back. Two: the old woman is crying: brows pushed up and together, eyes glistening with clear tears, "
     "no redness, no red marks, mouth corners pulled down, lips closed, not smiling.")
edit("c21", ["ST:c21-b.png"],
     "Edit image 1. Exactly two changes. One: she turns her head into three-quarter profile toward screen LEFT, eyes clearly to the left on someone far beyond "
     "the left edge, never looking at the camera, lips closed, not smiling. Two: her bare right hand gently cups the little brass bells on the bag's flap, her "
     "left hand holds the bag's handle at chest height.")
edit("c25", ["ST:c25-b.png"],
     "Edit image 1. Only change: her bare right hand is closed tight around the little brass bells on the flap, the bells hidden inside her fist; her left hand "
     "holds the bag's handle up at her chest.")
edit("c26", ["ST:c26-a.png"],
     "Edit image 1. Exactly two changes. One: the phone is completely hidden in front of her body; no glowing screen shows beside her head or anywhere; only a "
     "faint cool glow on the wall in front of her. Two: the bright glow around the empty wall hook is removed; the hook is a plain dark metal hook on a dim wall, "
     "not a lamp.")
edit("c05", ["set-shenjia-yuanzi-t1.png", "meifeng-portrait-t1.png", "jianye-portrait-t1.png"],
     "Edit image 1: keep the courtyard exactly as it is and put ONLY TWO people into it: by the left side of the round stone table the woman from image 2 "
     "(wine-red knit dress, pearl necklace, chestnut curls, hands empty), and just stepping in from the left corridor the man from image 3 (brown double-breasted "
     "suit); both faces in three-quarter profile turned toward screen right, eyes toward the lower right corner, never looking at the camera, not smiling, no "
     "teeth. Warm yellow wall glow only, no lanterns.")
edit("c19", ["set-shenjia-chufang-t1.png", "yuetang-18-portrait-t1.png", "prop-shubao-t1.png"],
     "Edit image 1: keep the kitchen exactly as it is and put ONLY ONE young woman (from image 2, moon-white stand-collar shirt, black braid on her right "
     "shoulder, navy skirt, sleeves folded to the wrists, no earrings) side-on at the white sink on screen right, holding the wet navy flap school bag of image 3 "
     "(big round brass clasp, red cord with three brass bells) above the sink with both hands, eyes down on the bag, never looking at the camera, lips closed. "
     "No lanterns or hanging lamps other than the bare bulb.")
S.append({"shot": "c27", "shares_with": BASE["c27"]["shares_with"], "refs": BASE["c27"]["refs"], "prompt": BASE["c27"]["prompt"],
          **({"latent": BASE["c27"]["latent"]} if BASE["c27"].get("latent") else {})})

if __name__ == "__main__":
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(OUT, len(S))
