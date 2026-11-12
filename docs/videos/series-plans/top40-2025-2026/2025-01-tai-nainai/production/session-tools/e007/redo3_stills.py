#!/usr/bin/env python3
"""第 7 集首格第三輪（2026-11-10，站主同意超過首格檢查點約 1.5 CU）：剩下 10 鏡全部用修圖 -> stills-redo3.json。

第二輪結論：整張重生的鏡（c01、c09、c12、c25–c29）幾乎全失敗，修圖鏡大多成功；所以這輪每鏡都拿最接近的一張改。
refs：`ST:` 是 $TN_WORK/e007ff/st/，`ST2:` 是 st2/，其他在 refs/。c25 分兩步（這輪先放人與疊好的長袍，前景背影下一步）；
c29 等 c27 定了再從它改，這輪不畫。
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "stills-redo3.json"
NOTEXT = "No subtitles, no captions, no text, numbers, signs, LED displays or screens anywhere in the picture."
KEEP = "Keep everything else exactly the same: the place, the light, the camera angle, faces, hair and clothes. No other change. "
NOLANTERN = "No lanterns anywhere."
S = []


def edit(shot, refs, prompt):
    S.append({"shot": shot, "shares_with": [], "refs": refs, "prompt": prompt + " " + KEEP + NOTEXT, "latent": "image1"})


edit("c01", ["ST:c01-a.png"], "Edit image 1. Remove every seated or standing passenger except the schoolgirl walking in the aisle and the young woman at the "
     "front door, leaving the seats empty. The young woman at the front: long sleeves down to the wrist, a navy ankle-length skirt, her face clearly visible "
     "in three-quarter profile toward screen left. The schoolgirl wears white ankle socks and a navy pleated skirt below the knee.")
edit("c07", ["ST2:c07-c.png"], "Edit image 1. His mouth is CLOSED in a wide excited grin, lips together, no teeth showing; his head turned to a three-quarter "
     "profile toward the upper left, eyes fixed on the black phone on the selfie stick. Remove the dark display frame behind his head, leaving plain bus wall.")
edit("c09", ["ST2:c09-d.png"], "Edit image 1. Remove the yellow LED display and the yellow strip behind him, leaving plain bus wall. A selfie stick rises from "
     "his right hand out of the top of the frame. The person in the foreground shrinks to only a thin blurred sliver of a right shoulder in a MOON-WHITE high "
     "collar with one black braid over it at the far LEFT edge, no ear, no cheek, no face.")
edit("c12", ["ST2:c12-c.png"], "Edit image 1. The girl on the RIGHT has long straight LIGHT-BROWN hair worn down, NO bangs, a navy necktie; in her right hand "
     "an unzipped navy school bag, in her left hand a clear plastic cup with NO lid and one straw. The two girls look at each other, not at the camera.")
edit("c15", ["ST2:c15-d.png"], "Edit image 1. Nothing is pouring: the cup is held upright and still just above the open mouth of the bag; the cup is fully "
     "clear plastic with no lid, pale milk tea inside, one straw. Her expression: one corner of the mouth lifted in a sneer, one eyebrow raised, eyes half "
     "closed, looking to screen left, no teeth.")
edit("c22", ["ST2:c22-d.png"], "Edit image 1. Her mouth corners turned down, one eyebrow raised, chin lifted, eyes looking down at the person in front of her, "
     "not smiling. At the bottom edge she holds an empty clear plastic cup with no lid and one straw. The small booth behind her becomes a white guard booth "
     "with a rounded roof, out of focus.")
edit("c25", ["set-shenjia-yuanzi-t1.png", "meifeng-portrait-t1.png", "prop-shouyi-t1.png"],
     "Edit image 1, keeping the courtyard exactly the same: add ONLY ONE woman, the woman from image 2 in her wine-red knit dress, pearl necklace and big "
     "glossy dark chestnut curls, standing beside the round stone table, her face in three-quarter profile turned toward screen right, not looking at the "
     "camera, holding against her chest the off-white robe of image 3 folded flat into a neat rectangle, its high stand-up collar and frog buttons visible on "
     "top; she is NOT wearing it. Dusk, the veranda lamps lit. " + NOLANTERN)
edit("c26", ["ST2:c26-d.png"], "Edit image 1. Remove the red lanterns, leaving a dark eave with warm yellow wall light. The blurred person in the foreground has "
     "plain black hair pulled back into one braid, no bun, no earring. The woman in wine-red has a cold thin fake smile with closed lips, eyes cold.")
edit("c27", ["ST2:c29-c.png"], "Edit image 1. Her head turns to a three-quarter profile toward screen right, eyes to the right; her red lips pulled to one side "
     "in a cold smile, closed; she holds the robe up by its shoulders, held out toward screen right. The background darkens to just after dusk: the wooden "
     "veranda posts, warm yellow light from the left. She is NOT wearing the robe. " + NOLANTERN)


if __name__ == "__main__":
    OUT.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(OUT, len(S))
