#!/usr/bin/env python3
"""Back up an episode's work directory (and extra files) to an orphan git branch, verify every file by hash.

usage: backup.py <slug> <message> [extra_src:dest ...]
- copies /root/mokaair-work/videos/<slug>/ to <wt>/workdir/ (never deletes anything already backed up)
- extra files go to <wt>/<dest>
- files over 90 MB are split into <name>.partNN (90 MB each); MANIFEST.tsv keeps path, size, sha256, parts
- commits, pushes to origin claude/backup-<slug>, fetches it back and re-hashes every file from the remote tree
"""
import hashlib, os, shutil, subprocess, sys, time

REPO = "/home/user/travel_scanner"
LIMIT = 90 * 1024 * 1024
slug, message, extras = sys.argv[1], sys.argv[2], sys.argv[3:]
branch = f"claude/backup-{slug}"
wt = f"/root/backup-wt/{slug}"
src = f"/root/mokaair-work/videos/{slug}"

def run(*a, cwd=wt, check=True, capture=False):
    r = subprocess.run(a, cwd=cwd, check=check, text=not capture, capture_output=capture)
    return r.stdout if capture else r

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

if not os.path.isdir(wt):
    os.makedirs(os.path.dirname(wt), exist_ok=True)
    exists = subprocess.run(["git", "ls-remote", "--exit-code", "--heads", "origin", branch], cwd=REPO, capture_output=True).returncode == 0
    if exists:
        run("git", "fetch", "-q", "origin", f"{branch}:{branch}", cwd=REPO)
        run("git", "worktree", "add", "-q", wt, branch, cwd=REPO)
    else:
        run("git", "worktree", "add", "-q", "--detach", wt, cwd=REPO)
        run("git", "checkout", "-q", "--orphan", branch)
        run("git", "rm", "-rq", "--cached", ".", check=False)
        for name in os.listdir(wt):
            if name != ".git": shutil.rmtree(os.path.join(wt, name)) if os.path.isdir(os.path.join(wt, name)) else os.remove(os.path.join(wt, name))

# manifest: path -> (size, sha, parts)
mpath = os.path.join(wt, "MANIFEST.tsv")
manifest = {}
if os.path.exists(mpath):
    for line in open(mpath, encoding="utf-8").read().splitlines()[1:]:
        p, size, h, parts = line.split("\t"); manifest[p] = (int(size), h, int(parts))

def place(srcfile, rel):
    if os.path.basename(srcfile).startswith("LEASE"): return
    size, h = os.path.getsize(srcfile), sha(srcfile)
    if manifest.get(rel, (None, None))[1] == h: return
    dest = os.path.join(wt, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for old in [f for f in os.listdir(os.path.dirname(dest)) if f.startswith(os.path.basename(dest) + ".part")]:
        os.remove(os.path.join(os.path.dirname(dest), old))
    if size > LIMIT:
        if os.path.exists(dest): os.remove(dest)
        n = 0
        with open(srcfile, "rb") as f:
            while True:
                b = f.read(LIMIT)
                if not b: break
                open(f"{dest}.part{n:02d}", "wb").write(b); n += 1
        manifest[rel] = (size, h, n)
    else:
        shutil.copy2(srcfile, dest); manifest[rel] = (size, h, 0)

if os.path.isdir(src):
    for root, dirs, files in os.walk(src):
        for f in files:
            full = os.path.join(root, f)
            place(full, os.path.join("workdir", os.path.relpath(full, src)))
for e in extras:
    s, d = e.split(":", 1)
    place(s, d)

with open(mpath, "w", encoding="utf-8") as f:
    f.write("path\tsize\tsha256\tparts\n")
    for p in sorted(manifest): f.write(f"{p}\t{manifest[p][0]}\t{manifest[p][1]}\t{manifest[p][2]}\n")
readme = os.path.join(wt, "README.md")
if not os.path.exists(readme):
    open(readme, "w", encoding="utf-8").write(
        f"# {slug} 備份\n\n站主 2026-11-07：每過一關就把整個工作目錄（重製要用的所有檔案）加上 upload/ 裡全部上傳的檔案推到這個分支，超過 90 MB 切塊，逐檔核對雜湊。\n\n"
        f"- `workdir/` 是 `/root/mokaair-work/videos/{slug}/` 的副本（不含 LEASE）。\n- `music/` 是系列配樂床與它的付費原檔。\n"
        f"- `MANIFEST.tsv`：每個檔案的原始大小、sha256 與切塊數；切塊的檔案是 `<name>.part00`、`.part01`…，還原時依序 `cat` 接回再核對 sha256。\n"
        f"- 稿子與 `build_scenes.py` 在工作分支的 `docs/videos/{slug}/`。\n\n## 紀錄\n\n")
open(readme, "a", encoding="utf-8").write(f"- {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}：{message}（{len(manifest)} 個檔案）\n")

run("git", "add", "-A")
if run("git", "status", "--porcelain", capture=True).decode().strip():
    run("git", "commit", "-q", "-m", f"backup: {slug} {message}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_018EYovHhG7uMki2Ri6NGbqt")
for attempt in range(5):
    if subprocess.run(["git", "push", "-q", "-u", "origin", branch], cwd=wt).returncode == 0: break
    time.sleep(2 ** (attempt + 1))
else:
    sys.exit("push failed")

# verify from the remote
run("git", "fetch", "-q", "origin", branch)
remote = run("git", "rev-parse", "FETCH_HEAD", capture=True).decode().strip()
bad = 0
for p, (size, h, parts) in manifest.items():
    names = [p] if parts == 0 else [f"{p}.part{i:02d}" for i in range(parts)]
    d = hashlib.sha256(); total = 0
    for n in names:
        blob = subprocess.run(["git", "cat-file", "blob", f"{remote}:{n}"], cwd=wt, capture_output=True, check=True).stdout
        d.update(blob); total += len(blob)
    if d.hexdigest() != h or total != size:
        bad += 1; print("MISMATCH", p)
print(f"{branch} @ {remote[:10]}: {len(manifest)} files verified, {bad} mismatches")
sys.exit(1 if bad else 0)
