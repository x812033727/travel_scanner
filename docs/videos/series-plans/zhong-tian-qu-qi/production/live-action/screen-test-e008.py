#!/usr/bin/env python3
"""screen-test-e008.py OUT_DIR : the three live-action set pictures e008 r2 needs (owner 2026-11-12: 三張都畫，每張兩個種子):
the escort agency yard, the Qian mansion gate (with its white outer wall and side door) and the Qian mansion hall.
Same place template, style, negative prompt, grey canvas and seeds as screen-test.py; writes OUT_DIR/e008.json."""
import json, runpy, sys
from pathlib import Path
out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True); (out / "base").mkdir(exist_ok=True)
st = runpy.run_path(str(Path(__file__).resolve().parent / "screen-test.py"), run_name="screen_test_lib",
                    init_globals={"sys": type("S", (), {"argv": ["x", str(out / "_full")]})})
SETS = {
 "set-biaoju": ("the yard of a small escort agency outside an ancient Chinese Song-dynasty county town: a packed-earth yard, a stone well and a "
   "stone washing trough on the right, a wooden rack of furled escort banners in the near left (the banners rolled up, no writing), "
   "the yard gate at the back left, low tiled buildings with timber posts, the lintel board over the gate plain and blank; "
   "late-afternoon sun low from the left, long shadows; no weapons anywhere"),
 "set-qianfu-men": ("the front gate of a rich landlord's mansion in an ancient Chinese Song-dynasty county: stone steps up to a vermilion double gate "
   "with brass studs, one stone lion on each side, the board over the gate plain and blank; to the side a long white-washed outer wall "
   "with grey tiles on top, a small side door and a wooden hitching post, plain paper lanterns on the wall with no writing; "
   "sunset light low from the left"),
 "set-qianfu-ting": ("the main hall of a rich landlord's mansion in an ancient Chinese Song-dynasty county: a rosewood table on the right with one "
   "carved armchair behind it, a plain wooden screen behind the chair with no painting and no writing, polished wooden floor, "
   "the open doorway on the left with one shaft of low sunset light slanting in across the floor"),
}
base = st["canvas"]("grey-set.png", 1312, 736)
(out / "prompts" / "negative.txt").write_text(st["NEG"], encoding="utf-8")
jobs = []
for jid, desc in SETS.items():
    (out / "prompts" / f"{jid}.txt").write_text(st["BLANK"] + st["PLACE"].format(desc=desc) + " " + st["STYLE"], encoding="utf-8")
    jobs += [{"id": f"{jid}-{s}", "reference_images": [str(out / base)], "prompt_file": str(out / "prompts" / f"{jid}.txt"),
              "negative_file": str(out / "prompts" / "negative.txt"), "width": 1312, "height": 736, "seed": s, "latent": "empty"} for s in st["SEEDS"]]
(out / "e008.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "e008.json")
