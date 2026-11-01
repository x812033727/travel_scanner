"""Second pass: what the first drew wrong is written as what should be there (Qwen paints negatives as text)."""
import json, os
A = os.path.dirname(os.path.abspath(__file__))
jobs = json.load(open(f"{A}/refs.json", encoding="utf8"))["jobs"]
EXTRA = {
 "xudalang-portrait-t1": "His face is mild and bookish with narrow eyes and level brows, skin with fine CG pores. The old straw hat is grey and weathered, a round shallow brim sitting low. The robe is plain smooth blue cotton, half worn. Framed from the waist up.",
 "zhouyuanwai-portrait-t1": "His long narrow face has a high hooked nose, hollow cheeks and small sly eyes, a look of sour contempt. On his head a small round black six-panel melon-skin skullcap fitted close to the skull. Framed from the waist up.",
 "set-zhou-kezhan-t1": "Along the back of the counter stand fat brown clay wine jars with red cloth seals. The beams are plain dark wood.",
 "set-gongyuan-t1": "The lintel over the gate is a plain bare dark timber beam. The table stands under its own small tiled roof at the left of the square.",
}
out = []
seen = set()
for job in jobs:
    name = job["id"].rsplit("-", 1)[0]
    if name in seen:
        continue
    seen.add(name)
    for seed in (420010, 420011, 420012):
        item = dict(job)
        item.update(id=f"{name}-{seed}", seed=seed, output_name=f"{name}-{seed}.png", prompt=job["prompt"].replace(" 3D Chinese donghua", " " + EXTRA[name] + " 3D Chinese donghua", 1))
        out.append(item)
json.dump({"jobs": out}, open(f"{A}/refs2.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(len(out))
