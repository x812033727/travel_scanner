"""s26 again: both seeds of the first retake came out full body with the abacus out of the frame."""
import json, os
A = os.path.dirname(os.path.abspath(__file__)); R = f"{A}/retake"
OLD = "The shot opens directly on this medium close-up, her face and shoulders large in the frame from the waist up, and she keeps the proportions of a grown woman of eighteen. She rises fully off the stool to standing, and the abacus goes up over her head."
NEW = "From the first frame to the last the frame holds only her head, shoulders and chest, her face large and filling the upper middle of the frame on screen left; her waist, legs and the stool are never in the frame, and she keeps the proportions of a grown woman of eighteen. She rises a little and the frame rises with her; the small gold abacus comes up in one hand beside her head and stays inside the frame while she shakes it."
text = open(f"{R}/prompts/ref-s26.txt", encoding="utf8").read()
assert OLD in text
open(f"{R}/prompts/ref-s26b.txt", "w", encoding="utf8", newline="\n").write(text.replace(OLD, NEW))
base = next(j for j in json.load(open(f"{R}/retake.json", encoding="utf8"))["jobs"] if j["id"] == "s26-410100")
jobs = []
for seed in (410102, 410103):
    item = dict(base)
    item.update(id=f"s26-{seed}", seed=seed, output_name=f"s26-{seed}.mp4", prompt_file="prompts/ref-s26b.txt")
    jobs.append(item)
json.dump({"jobs": jobs}, open(f"{R}/retake26.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(len(jobs))
