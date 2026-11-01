"""Picked drafts for e041 and the four e040 retakes, then stage-2 manifests through route_a_st2.py."""
import glob, json, os, re, shutil, subprocess, sys
repo = sys.argv[1]
V = "C:/Users/x8120/mokaair-work/videos"
A41 = f"{V}/zhong-tian-qu-qi-e041-dh/runpod/a"
A40 = f"{V}/zhong-tian-qu-qi-e040-dh/runpod/a"
H = f"{repo}/docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo"
ST2 = f"{repo}/.agents/skills/minimax-h3-runpod/scripts/route_a_st2.py"
P41 = {"s01": 410101, "s02": 410100, "s05": 410101, "s07": 410100, "s09": 410101, "s13": 410101, "s23": 410101,
       "s24": 410100, "s27": 410100, "s30": 410100, "s32": 410100, "s33": 410100, "s35": 410101}
P40 = {"s14": 400001, "s24": 400001, "s50": 400000, "s54": 400001}
out = f"{A41}/picked/st1/out"; os.makedirs(out, exist_ok=True)
for path in glob.glob(f"{A41}/st1/out/*.mp4"):
    shutil.copy2(path, out)
for sid, seed in P41.items():
    shutil.copy2(f"{A41}/retake/out/{sid}-{seed}.mp4", f"{out}/{sid}.mp4")
shutil.copy2(f"{A41}/retake/out26/s26-410102.mp4", f"{out}/s26.mp4")
seeds41 = [f"{k}:{v}" for k, v in {**P41, "s26": 410102}.items()]
subprocess.run([sys.executable, "-I", ST2, f"{H}/clips-dh-e041.json", f"{A41}/picked", "410000", *seeds41], check=True)
root = f"{A40}/picked3"; out = f"{root}/st1/out"; os.makedirs(out, exist_ok=True); os.makedirs(f"{root}/st2", exist_ok=True)
for sid, seed in P40.items():
    shutil.copy2(f"{A40}/retake3/out/{sid}-{seed}.mp4", f"{out}/{sid}.mp4")
clips = json.load(open(f"{H}/clips-dh-e040.json", encoding="utf8"))
skip = [k.split("-")[1] for k in clips if k.split("-")[1] not in P40]
open(f"{root}/st2/skip.txt", "w").write("\n".join(skip))
subprocess.run([sys.executable, "-I", ST2, f"{H}/clips-dh-e040.json", root, "400000", *[f"{k}:{v}" for k, v in P40.items()]], check=True)
# The refine text must not bring back the owner of a hands-only shot.
for path, old, new in ((f"{A41}/picked/st2/prompts/s32.txt", "Xu Yan", "the man"), (f"{root}/st2/prompts/s54.txt", "A-ling", "the woman")):
    text = open(path, encoding="utf8").read()
    print(path[-8:], text.count(old), "swapped")
    open(path, "w", encoding="utf8", newline="\n").write(text.replace(old, new))
print(re.sub(r"\s+", " ", open(f"{root}/st2/prompts/s54.txt", encoding="utf8").read())[:300])
