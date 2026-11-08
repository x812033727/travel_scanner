#!/usr/bin/env python3
"""Back up an episode's work directory (and everything a remake needs) to a git branch, verify every file by hash.

usage: backup.py <slug> <message> [extra_src:dest ...]
- copies /root/mokaair-work/videos/<slug>/ to workdir/ on branch claude/backup-<slug> (never deletes anything already backed up)
- extra files or directories go to <dest>
- always adds shared/ (series sheets, music, branding), review-packs/, tools/, the scratchpad files for the episode, and
  _repo/ (the episode's script folder as it is in this checkout, uncommitted edits included, and the checkout's commit)
- files over 90 MB are split into <name>.partNN (90 MiB each); MANIFEST.tsv keeps path, size, sha256, parts
- no checkout: blobs go straight into the object store through a private index, commits are pushed in batches
  of at most 900 MB (GitHub refuses a push over 2 GiB), then the branch is fetched back and every file re-hashed
  from the remote tree; finally the pushed objects are pruned from the local store so the disk does not fill up
"""
import hashlib, os, subprocess, sys, time

REPO = "/home/user/travel_scanner"
LIMIT = 90 * 1024 * 1024
BATCH = 900 * 1024 * 1024
slug, message, extras = sys.argv[1], sys.argv[2], sys.argv[3:]
branch = f"claude/backup-{slug}"
src = f"/root/mokaair-work/videos/{slug}"
SCRATCH = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(SCRATCH, f".index-{slug}")
ENV = {**os.environ, "GIT_INDEX_FILE": INDEX}
TRAILER = "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_018EYovHhG7uMki2Ri6NGbqt"

def git(*a, data=None, env=None, check=True):
    r = subprocess.run(["git", *a], cwd=REPO, input=data, capture_output=True, env=env or os.environ)
    if check and r.returncode: sys.exit(f"git {' '.join(a)} failed: {r.stderr.decode(errors='replace')}")
    return r.stdout

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def blob_file(path): return git("hash-object", "-w", "--", path).decode().strip()
def blob_bytes(data): return git("hash-object", "-w", "--stdin", data=data).decode().strip()

# base: the branch as it is on the remote
exists = subprocess.run(["git", "ls-remote", "--exit-code", "--heads", "origin", branch], cwd=REPO, capture_output=True).returncode == 0
parent = None
if os.path.exists(INDEX): os.remove(INDEX)
FETCH = ["-c", "remote.origin.promisor=true", "-c", "remote.origin.partialclonefilter=blob:none", "fetch", "-q", "--filter=blob:none", "origin", branch]
if exists:
    git(*FETCH)
    parent = git("rev-parse", "FETCH_HEAD").decode().strip()
    git("read-tree", parent, env=ENV)
else:
    git("read-tree", "--empty", env=ENV)

manifest = {}
if parent:
    text = git("show", f"{parent}:MANIFEST.tsv", check=False).decode()
    for line in text.splitlines()[1:]:
        p, size, h, parts = line.split("\t"); manifest[p] = (int(size), h, int(parts))
indexed = set(git("ls-files", env=ENV).decode().splitlines())

pending = 0
def commit_batch(label):
    global parent, pending
    tree = git("write-tree", "--missing-ok", env=ENV).decode().strip()
    args = ["commit-tree", tree, "-m", f"backup: {slug} {message}{label}{TRAILER}"]
    if parent: args[2:2] = ["-p", parent]
    commit = git(*args).decode().strip()
    for attempt in range(5):
        if subprocess.run(["git", "-c", "remote.origin.promisor=true", "-c", "remote.origin.partialclonefilter=blob:none", "push", "-q", "origin", f"{commit}:refs/heads/{branch}"], cwd=REPO).returncode == 0: break
        time.sleep(2 ** (attempt + 1))
    else: sys.exit("push failed")
    parent, pending = commit, 0

batches = 0
def add(path, blob):
    git("update-index", "--add", "--cacheinfo", f"100644,{blob},{path}", env=ENV)
    indexed.add(path)

SOURCES = []
def place(srcfile, rel):
    global pending, batches
    if os.path.basename(srcfile).startswith("LEASE"): return
    SOURCES.append((rel, srcfile))
    size, h = os.path.getsize(srcfile), sha(srcfile)
    if manifest.get(rel, (None, None))[1] == h: return
    stale = [p for p in indexed if p == rel or p.startswith(rel + ".part")]
    if stale: git("update-index", "--force-remove", "--", *stale, env=ENV); indexed.difference_update(stale)
    if size > LIMIT:
        n = 0
        with open(srcfile, "rb") as f:
            while True:
                b = f.read(LIMIT)
                if not b: break
                add(f"{rel}.part{n:02d}", blob_bytes(b)); n += 1
        manifest[rel] = (size, h, n)
    else:
        add(rel, blob_file(srcfile)); manifest[rel] = (size, h, 0)
    pending += size
    if pending >= BATCH:
        batches += 1; commit_batch(f" (part {batches})")

def place_any(s, d):
    if os.path.isdir(s):
        for root, dirs, files in os.walk(s):
            for f in sorted(files):
                full = os.path.join(root, f)
                place(full, os.path.join(d, os.path.relpath(full, s)))
    elif os.path.isfile(s):
        place(s, d)

# Everything a remake needs that lives outside the episode's work directory goes in every backup (站主 2026-11-08:
# 之後如果要重製就可以不用重新做的都要備份到): series sheets, the music bed and its paid source, the branding pack,
# the zoom-review packs, this session's helper scripts, logs, prompts and answers, and the script folder.
short = slug.split("-")[1] if slug.startswith("sothatswhy-") else slug
extras_default = [
    ("/root/mokaair-work/videos/_series/sothatswhy", "shared/_series/sothatswhy"),
    ("/root/mokaair-work/videos/_music", "shared/_music"),
    ("/root/mokaair-work/videos/_branding", "shared/_branding"),
    (f"/root/review-packs/{slug}", "review-packs"),
    (os.path.join(REPO, "docs/videos", slug), f"_repo/docs/videos/{slug}"),
]
base = os.path.join(SCRATCH, f".base-{slug}.txt")
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
dirty = subprocess.run(["git", "status", "--porcelain", "--", f"docs/videos/{slug}"], cwd=REPO, capture_output=True, text=True).stdout
open(base, "w").write(f"{head}\nuncommitted changes in docs/videos/{slug}: {'yes' if dirty.strip() else 'no'}\n{dirty}")
extras_default.append((base, "_repo/BASE"))
for name in ("backup.py", "makepack.py", "overview.py", "dubloop.sh", "repin.py"):
    extras_default.append((os.path.join(SCRATCH, name), f"tools/{name}"))
for name in sorted(os.listdir(SCRATCH)):
    full = os.path.join(SCRATCH, name)
    if os.path.isfile(full) and name.startswith(short + "-"):
        extras_default.append((full, f"scratchpad/{name}"))

place_any(src, "workdir")
for s, d in extras_default: place_any(s, d)
for e in extras:
    s, d = e.split(":", 1); place_any(s, d)

# MANIFEST and README last
lines = ["path\tsize\tsha256\tparts"] + [f"{p}\t{v[0]}\t{v[1]}\t{v[2]}" for p, v in sorted(manifest.items())]
add("MANIFEST.tsv", blob_bytes(("\n".join(lines) + "\n").encode()))
readme = git("show", f"{parent}:README.md", check=False).decode() if parent else ""
if not readme:
    readme = (f"# {slug} 備份\n\n站主 2026-11-07：每過一關就把整個工作目錄（重製要用的所有檔案）加上 upload/ 裡全部上傳的檔案推到這個分支，超過 90 MB 切塊，逐檔核對雜湊。\n\n"
              f"- `workdir/` 是 `/root/mokaair-work/videos/{slug}/` 的副本（不含 LEASE）。\n- `shared/` 是系列設定圖、配樂床與片頭片尾素材包。\n"
              f"- `MANIFEST.tsv`：每個檔案的原始大小、sha256 與切塊數；切塊的檔案是 `<name>.part00`、`.part01`…，還原時依序 `cat` 接回再核對 sha256。\n"
              f"- `_repo/` 是當時這一集的稿子資料夾與 checkout 的 commit。\n\n## 紀錄\n\n")
readme += f"- {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}：{message}（{len(manifest)} 個檔案）\n"
add("README.md", blob_bytes(readme.encode()))
commit_batch(f" (part {batches + 1}, last)" if batches else "")

# verify from the remote: fetch the branch's commit and trees back, and check that every blob id on GitHub is the
# git id of the file's bytes here (git is content-addressed, so equal ids mean equal bytes; split files part by part)
git(*FETCH)
remote = git("rev-parse", "FETCH_HEAD").decode().strip()
assert remote == parent, (remote, parent)
tree = {}
for line in git("ls-tree", "-r", remote).decode("utf-8", "surrogateescape").splitlines():
    meta, path = line.split("\t", 1); tree[path] = meta.split()[2]
sources = dict(SOURCES)
bad = 0
for p, (size, h, parts) in manifest.items():
    srcfile = sources.get(p)
    if srcfile is None or not os.path.exists(srcfile) or sha(srcfile) != h:
        # backed up earlier and gone or changed here since: its id must still be on the branch
        names = [p] if parts == 0 else [f"{p}.part{i:02d}" for i in range(parts)]
        if not all(n in tree for n in names): bad += 1; print("MISSING", p)
        continue
    if parts == 0:
        ok = tree.get(p) == git("hash-object", "--", srcfile).decode().strip()
    else:
        ok = True
        with open(srcfile, "rb") as f:
            for i in range(parts):
                ok = ok and tree.get(f"{p}.part{i:02d}") == git("hash-object", "--stdin", data=f.read(LIMIT)).decode().strip()
    if not ok: bad += 1; print("MISMATCH", p)
print(f"{branch} @ {remote[:10]}: {len(manifest)} files verified, {bad} mismatches")
if not bad:
    # the branch is safe on the remote: drop the local copies of its objects so the disk does not fill up
    os.remove(INDEX)
    subprocess.run(["git", "update-ref", "-d", "FETCH_HEAD"], cwd=REPO)
    subprocess.run(["git", "update-ref", "-d", f"refs/remotes/origin/{branch}"], cwd=REPO)  # fetch's tracking ref keeps the objects alive
    subprocess.run(["git", "prune", "--expire=now"], cwd=REPO)
sys.exit(1 if bad else 0)
