#!/usr/bin/env python3
"""screen-test-e007.py OUT_DIR : the two live-action references e007 r2 needs (owner 2026-11-11: 兩張都畫，每張兩個種子):
Sun Zhanggui's head-and-shoulders portrait and the lane behind the county silk shop. Same templates, style, negative
prompt, grey canvas and seeds as screen-test.py; writes OUT_DIR/e007.json for `h3.sh images-check` / `images` on Colab."""
import json, re, runpy, subprocess, sys
from pathlib import Path
out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True); (out / "base").mkdir(exist_ok=True)
here = Path(__file__).resolve().parent
st = runpy.run_path(str(here / "screen-test.py"), run_name="screen_test_lib", init_globals={"sys": type("S", (), {"argv": ["x", str(out / "_full")]})})
# Sun Zhanggui: cast.json's "narrow smiling eyes that are always half closed" would draw a smile on every shot
sun = st["appearance"]("sunzhanggui").replace("narrow smiling eyes that are always half closed", "narrow heavy-lidded eyes and a calm, shrewd look") \
    .replace("a green satin robe with a jade belt hook", "an ancient Chinese Song-dynasty silk merchant's green satin cross-collared robe with a jade belt hook")
lane = ("the narrow flagstone back lane behind a silk shop in an ancient Chinese Song-dynasty county town: bamboo poles across the lane "
        "hung with lengths of dyed silk in soft colours, one red-painted wooden back door half open, grey brick walls and tiled eaves, "
        "a wooden tub and a stone well, a stone mounting block at the lane mouth and a simple thatched tea shed beyond it, "
        "late-morning sunlight; every door lintel and signboard plain and blank")
items = [("sunzhanggui", st["HEAD"].format(desc=re.sub(st["FEET"], "", sun)), 864, 1152, st["canvas"]("grey-portrait.png", 864, 1152)),
         ("set-chouduan", st["PLACE"].format(desc=lane), 1312, 736, st["canvas"]("grey-set.png", 1312, 736))]
(out / "prompts" / "negative.txt").write_text(st["NEG"], encoding="utf-8")
jobs = []
for jid, body, w, h, base in items:
    (out / "prompts" / f"{jid}.txt").write_text(st["BLANK"] + body + " " + st["STYLE"], encoding="utf-8")
    jobs += [{"id": f"{jid}-{s}", "reference_images": [str(out / base)], "prompt_file": str(out / "prompts" / f"{jid}.txt"),
              "negative_file": str(out / "prompts" / "negative.txt"), "width": w, "height": h, "seed": s, "latent": "empty"} for s in st["SEEDS"]]
(out / "e007.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / "e007.json")
