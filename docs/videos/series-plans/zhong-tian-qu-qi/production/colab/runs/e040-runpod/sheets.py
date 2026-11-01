import json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
A = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(A, "st1", "out"); S = os.path.join(A, "review"); os.makedirs(S, exist_ok=True)
ids = [f"s{i:02d}" for i in range(1, 55)]
missing = [i for i in ids if not os.path.exists(f"{OUT}/{i}.mp4")]
print("missing", missing)
for k in range(0, len(ids), 9):
    group = [i for i in ids[k:k + 9] if i not in missing]
    rows = []
    args = []
    for n, sid in enumerate(group):
        args += ["-i", f"{OUT}/{sid}.mp4"]
        rows.append(f"[{n}:v]select='eq(n,3)+eq(n,60)+eq(n,110)+eq(n,155)',scale=360:-1,drawtext=text='{sid}':x=6:y=6:fontsize=28:fontcolor=yellow:box=1:boxcolor=black,tile=4x1[r{n}]")
    chain = ";".join(rows) + ";" + "".join(f"[r{n}]" for n in range(len(group))) + f"vstack={len(group)}" if len(group) > 1 else ";".join(rows)
    target = f"{S}/sheet-{k // 9 + 1}.jpg"
    cmd = ["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", chain, "-frames:v", "1", "-q:v", "4", target]
    subprocess.run(cmd, check=True)
    print(target)
