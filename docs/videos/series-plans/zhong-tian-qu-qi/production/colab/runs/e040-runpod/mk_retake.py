"""Retake manifest: the listed e040 drafts with a fix written into the prompt, two seeds each."""
import glob, hashlib, json, os, sys
A = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(A, "retake"); os.makedirs(f"{R}/prompts", exist_ok=True)
BOUND = "He stays sitting against the grain sacks with both hands bound behind his back by the rope for the whole shot; he never leans onto the floor and never picks anything up."
FIX = {
 "s01": "Xu Yan wears plain cloth shoes on both feet. The crowd stays in the left third of the frame and nobody stands between the camera and Xu Yan.",
 "s13": BOUND + " The framing stays a close-up of his face from the first frame to the last; static shot.",
 "s14": "The framing stays a medium close-up of Qin Shuang from the waist up, large on screen right, from the first frame to the last; static shot.",
 "s19": "He has a realistic human face with natural proportions and the same detailed CG skin as every other character in this series.",
 "s30": "He stays upright with his mouth closed and never laughs or lies down; only his eyes move, wavering. Static close-up from the first frame to the last.",
 "s36": "These two grown women are the only people in the frame; the ridge around them is empty.",
 "s47": "The rice bowl stays on the straw floor in front of him. " + BOUND,
 "s50": "The rice bowl stays on the straw floor in front of him. " + BOUND,
 "s53": "The framing stays a close-up of her face, head and shoulders filling the frame, from the first frame to the last; static shot.",
 "s54": "From the first frame to the last the frame holds only her two hands and the tea bowl, very large; her face stays out of the frame.",
}
jobs = []
for path in sorted(glob.glob(f"{A}/st1/ref-e040-part*.json")):
    for job in json.load(open(path, encoding="utf8"))["jobs"]:
        if job["id"] not in FIX:
            continue
        text = open(f"{A}/st1/{job['prompt_file']}", encoding="utf8").read()
        at = text.find("overall_soundscape")
        if at < 0:
            sys.exit(f"{job['id']}: no soundscape line")
        head = text[:at].rstrip()
        text = head + " " + FIX[job["id"]] + text[len(head):]
        name = f"prompts/{job['id']}.txt"
        open(f"{R}/{name}", "w", encoding="utf8", newline="\n").write(text)
        for seed in (400000, 400001):
            item = {k: v for k, v in job.items() if k not in ("output_path", "output_name", "prompt_sha256", "prompt_file")}
            item.update(id=f"{job['id']}-{seed}", seed=seed, prompt_file=name, output_name=f"{job['id']}-{seed}.mp4")
            jobs.append(item)
json.dump({"jobs": jobs[:20]}, open(f"{R}/retake.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(len(jobs), "jobs")
