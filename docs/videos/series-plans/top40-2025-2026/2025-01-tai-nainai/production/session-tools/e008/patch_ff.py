"""e008 clip manifest patch (2026-11-11, owner approved cap 66): shorter clips and motion fixes for the three weak first frames."""
import hashlib, json, math
from pathlib import Path
H = Path(__file__).resolve().parent
m = json.load(open(H / "ff-clips.json"))
FIX = {
 "c14": [("in the first frame her arms are already wrapped around the young woman's waist and her face is lifted from her side toward her",
          "in the first second she lifts both arms from her lap and wraps them tight around the young woman's waist, lifting her face toward her"),
         ("mouth corners pulled down.", "mouth corners pulled down, not smiling at any moment.")],
 "c10": [("in the first frame she is already stooping a little like an old woman,",
          "in the first second she lets her back sag into a slight old-woman stoop,"),
         ("folded into a neat square folded in front of her waist.", "folded into a neat square, clearly soft folded cloth, held out a little in front of her waist.")],
 "c07": [("folded into a neat square against her chest;", "folded into a neat square of soft cloth against her chest, its stand-up collar on top;"),
         ("behind her only out-of-focus corridor pillars and dark eaves.", "behind her only out-of-focus corridor pillars and dark eaves; the sky above is dark, almost black.")],
}
for j in m["jobs"]:
    pf = H / j["prompt_file"]; t = pf.read_text(encoding="utf-8")
    for a, b in FIX.get(j["id"], []):
        assert a in t, (j["id"], a); t = t.replace(a, b)
    pf.write_text(t, encoding="utf-8"); j["prompt_sha256"] = hashlib.sha256(pf.read_bytes()).hexdigest()
    j["duration_seconds"] = min(j["duration_seconds"], max(5, math.ceil(j["min_seconds"] + 1.5)))
json.dump(m, open(H / "ff-clips.json", "w"), ensure_ascii=False, indent=1)
print(sum(j["duration_seconds"] for j in m["jobs"]), [(j["id"], j["duration_seconds"]) for j in m["jobs"]])
