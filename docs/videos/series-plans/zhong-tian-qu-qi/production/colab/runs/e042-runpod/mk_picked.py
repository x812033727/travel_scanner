"""Picked drafts for e042, then stage-2 manifests through route_a_st2.py."""
import glob, os, shutil, subprocess, sys
repo = sys.argv[1]
A = os.path.dirname(os.path.abspath(__file__))
H = f"{repo}/docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo"
ST2 = f"{repo}/.agents/skills/minimax-h3-runpod/scripts/route_a_st2.py"
P = {"s02": 420101, "s06": 420101, "s09": 420100, "s13": 420101, "s16": 420100, "s18": 420101, "s19": 420100, "s20": 420100,
     "s29": 420101, "s31": 420101, "s32": 420100, "s33": 420101, "s34": 420100, "s35": 420100}
out = f"{A}/picked/st1/out"; os.makedirs(out, exist_ok=True)
for path in glob.glob(f"{A}/st1/out/*.mp4"):
    shutil.copy2(path, out)
for sid, seed in P.items():
    shutil.copy2(f"{A}/retake/out/{sid}-{seed}.mp4", f"{out}/{sid}.mp4")
subprocess.run([sys.executable, "-I", ST2, f"{H}/clips-dh-e042.json", f"{A}/picked", "420000", *[f"{k}:{v}" for k, v in P.items()]], check=True)
# The refine text must not bring back the owner of a hands-only shot.
for sid, old, new in (("s16", "Tang Xiaotang", "the woman"),):
    path = f"{A}/picked/st2/prompts/{sid}.txt"
    text = open(path, encoding="utf8").read()
    print(sid, text.count(old), "swapped")
    open(path, "w", encoding="utf8", newline="\n").write(text.replace(old, new))
print(len(glob.glob(f"{out}/*.mp4")), "drafts")
