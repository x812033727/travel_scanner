import os, subprocess
A = os.path.dirname(os.path.abspath(__file__)); O = f"{A}/retake/out"; S = f"{A}/retake/review"; os.makedirs(S, exist_ok=True)
shots = ["s01", "s13", "s14", "s19", "s30", "s36", "s47", "s50", "s53", "s54"]
for k in range(0, 10, 5):
    args, rows = [], []
    n = 0
    for sid in shots[k:k + 5]:
        for seed in (400000, 400001):
            args += ["-i", f"{O}/{sid}-{seed}.mp4"]
            rows.append(f"[{n}:v]select='eq(n,3)+eq(n,60)+eq(n,110)+eq(n,155)',scale=360:-1,drawtext=text='{sid} {seed}':x=6:y=6:fontsize=24:fontcolor=yellow:box=1:boxcolor=black,tile=4x1[r{n}]")
            n += 1
    chain = ";".join(rows) + ";" + "".join(f"[r{i}]" for i in range(n)) + f"vstack={n}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", chain, "-frames:v", "1", "-q:v", "4", f"{S}/retake-{k // 5 + 1}.jpg"], check=True)
