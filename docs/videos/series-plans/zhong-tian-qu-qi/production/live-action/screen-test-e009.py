#!/usr/bin/env python3
"""screen-test-e009.py OUT_DIR : the four night interiors e009 r2 needs, which have no picture in any version: the Xu house
corridor with its three doors, Tang Xiaotang's room, Qin Shuang's room and A-ling's room (script.md 場頭; all at night).
Same place template, style, negative prompt, grey canvas and seeds as screen-test.py; writes OUT_DIR/e008.json."""
import json, runpy, sys
from pathlib import Path
out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True); (out / "base").mkdir(exist_ok=True)
st = runpy.run_path(str(Path(__file__).resolve().parent / "screen-test.py"), run_name="screen_test_lib",
                    init_globals={"sys": type("S", (), {"argv": ["x", str(out / "_full")]})})
SETS = {
 "set-xujia-zoulang": ("the inside corridor of a poor ancient Chinese Song-dynasty farmhouse at night: packed-earth walls and rough timber posts, "
   "three plain wooden doors in a row along the right-hand wall with no writing on them, warm candlelight glowing through the cracks around them, "
   "the open end of the corridor on the left letting in a little cold blue moonlight, at the near end a low woodshed doorway; "
   "dark, lit only by the glow from the door cracks and the moonlight"),
 "set-xujia-tangfang": ("a small bedroom in a poor ancient Chinese Song-dynasty farmhouse at night, made neat by a young woman: a plain wooden table "
   "on the right with three thin cloth-bound account books on it and one lit candle, a simple wooden bed with a pale pink quilt behind the table, "
   "a paper window with plain blank paper, the wooden door on the left, packed-earth walls; warm yellow light from the one candle only"),
 "set-xujia-qinfang": ("a small plain bedroom in a poor ancient Chinese Song-dynasty farmhouse at night, its owner gone: an empty wooden bed with "
   "the quilt folded square and neat, the paper window flung wide open to the night, an empty wooden wall rack beside the window with nothing on it, "
   "a small table with one candle whose flame leans in the night wind; cold blue moonlight through the open window and a little warm candlelight"),
 "set-xujia-lingfang": ("a very small, very dark bedroom in a poor ancient Chinese Song-dynasty farmhouse at night: the wooden door on the left, "
   "a narrow wooden bed on the right with a thick grey quilt, a small low side table beside the bed with one lit candle, packed-earth walls; "
   "the one candle is the only light, warm and dim, deep shadows in the corners"),
}
base = st["canvas"]("grey-set.png", 1312, 736)
(out / "prompts" / "negative.txt").write_text(st["NEG"], encoding="utf-8")
jobs = []
for jid, desc in SETS.items():
    (out / "prompts" / f"{jid}.txt").write_text(st["BLANK"] + st["PLACE"].format(desc=desc) + " " + st["STYLE"], encoding="utf-8")
    jobs += [{"id": f"{jid}-{s}", "reference_images": [str(out / base)], "prompt_file": str(out / "prompts" / f"{jid}.txt"),
              "negative_file": str(out / "prompts" / "negative.txt"), "width": 1312, "height": 736, "seed": s, "latent": "empty"} for s in st["SEEDS"]]
(out / "e009.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "e009.json")
