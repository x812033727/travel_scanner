import glob, os, subprocess
A = os.path.dirname(os.path.abspath(__file__)); F = f"{A}/picked/final"; S = f"{A}/picked/review"; os.makedirs(S, exist_ok=True)
clips = sorted(glob.glob(f"{F}/*_1080.mp4"))
for k in range(0, len(clips), 9):
    args, rows = [], []
    for n, path in enumerate(clips[k:k + 9]):
        sid = os.path.basename(path).split("_")[0]
        args += ["-i", path]
        rows.append(f"[{n}:v]select='eq(n,3)+eq(n,40)+eq(n,80)+eq(n,110)',scale=400:-1,drawtext=text='{sid}':x=6:y=6:fontsize=26:fontcolor=yellow:box=1:boxcolor=black,tile=4x1[r{n}]")
    count = len(rows)
    chain = ";".join(rows) + ";" + "".join(f"[r{i}]" for i in range(count)) + f"vstack={count}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", chain, "-frames:v", "1", "-q:v", "4", f"{S}/final-{k // 9 + 1}.jpg"], check=True)
