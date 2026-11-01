"""The inn set without the modern-looking bottles, edited from itself so the room stays the same room as e042's shots."""
import json, os
A = os.path.dirname(os.path.abspath(__file__))
PROMPT = ("Edit image 1 and keep its exact layout, camera angle, lighting, staircase, tables, lanterns, windows, abacus, ledger and red-sealed jars unchanged. "
          "At the far end of the long counter, where the row of tall dark bottles stands, there is now one squat round brown clay jar with a red cloth tied over its mouth, the same kind as the other jars. "
          "The wood of the counter, tables and floor is old and worn, with scuffs, ring stains and rubbed edges. 3D Chinese donghua CG, Unreal Engine 5 cinematic render.")
jobs = [{"id": f"set-zhou-kezhan-t2-{seed}", "reference_images": [f"{A}/refs-dh/set-zhou-kezhan-t1.png"], "prompt": PROMPT, "width": 1312, "height": 736, "seed": seed, "output_name": f"set-zhou-kezhan-t2-{seed}.png"} for seed in (420020, 420021, 420022)]
json.dump({"jobs": jobs}, open(f"{A}/refs4.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(len(jobs))
