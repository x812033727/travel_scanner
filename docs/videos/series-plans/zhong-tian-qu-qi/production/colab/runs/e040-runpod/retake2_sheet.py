import os, subprocess
A = os.path.dirname(os.path.abspath(__file__)); O = f"{A}/retake2/out"
args, rows = [], []
n = 0
for sid in ("s13", "s14", "s36", "s47"):
    for seed in (400000, 400001):
        args += ["-i", f"{O}/{sid}-{seed}.mp4"]
        rows.append(f"[{n}:v]select='eq(n,3)+eq(n,40)+eq(n,80)+eq(n,110)',scale=360:-1,drawtext=text='{sid} {seed}':x=6:y=6:fontsize=24:fontcolor=yellow:box=1:boxcolor=black,tile=4x1[r{n}]")
        n += 1
chain = ";".join(rows) + ";" + "".join(f"[r{i}]" for i in range(n)) + f"vstack={n}"
subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", chain, "-frames:v", "1", "-q:v", "4", f"{A}/retake2/review.jpg"], check=True)
