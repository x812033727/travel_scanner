#!/usr/bin/env python3
"""《恁祖媽今年18》備份到 transfer/tn-e<NNN> 與 transfer/tn-shared（docs/videos/drama/BACKUP-BRANCHES.md，站主 2026-11-08）。

  tn-bk.py plan                 每個檔案歸哪條分支（不推）；列出歸不到的 → 涵蓋檢查
  tn-bk.py push e001|…|shared   推一條分支（暫存 git 庫建在 scratchpad，推完刪掉）
  （verify 沒有實作：推完請獨立代理自己抓分支逐檔比對 blob；2026-11-09 第 4 集是這樣驗的）

路徑在分支裡相對於 ~/mokaair-work/videos/；scratchpad 放在 _scratchpad/（不存含 session id 的絕對路徑）。
歸屬：路徑前兩層名字裡有 e00N（e001、e001-post、own/e001、expr/e001、e003r、review-expr-e001、picks-e001.txt…）
與 tai-nainai-import/tai-nainai-e00N → 那一集；pilot 與第 1 集小樣 → e001；其他 → shared。
不放：segments-v4/*.mkv（站主 2026-11-08 同意，合成腳本重建）、備份暫存庫 tn*.git / tn*-parts / tnbk-*、
git worktree（wt2038 打包成 _backup-archives/wt2038.tar 放 shared；wt2047 是本 repo 的 PR 分支，內容就在 GitHub）。
每個 commit 附 README-backup.md 與 MANIFEST.tsv（路徑、大小、git blob 雜湊、本機原路徑）。
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

S = Path(os.environ.get("TN_WORK", str(Path.home() / "mokaair-work/videos/_tn-work")))
V = Path.home() / "mokaair-work" / "videos"
REPO = "/home/user/travel_scanner"
ROOTS = [(S, "_scratchpad"), (V / "_series" / "tai-nainai", "_series/tai-nainai"), (V / "tai-nainai-import", "tai-nainai-import")]
# 2026-11-08 audit5：~/mokaair-work/videos/tai-nainai-eNNN/（站台預覽）與 _audition/（試鏡聲音樣本）原本沒進任何分支
ROOTS += [(d, d.name) for d in sorted(V.glob("tai-nainai-e[0-9][0-9][0-9]")) if d.is_dir()] + [(V / "_audition", "_audition")]
PART = 90 * 1024 * 1024
BIG = 95 * 1000 * 1000
EP = re.compile(r"(?:^|[^0-9a-z])e(00\d)(?![0-9])")
SKIP_TOP = re.compile(r"^(tn[^/]*\.git|tn[^/]*-parts|tnbk-[^/]*|wt2038|wt2047)$")


MULTI = re.compile(r"^_scratchpad/pick-expr\d*/")  # 三集一起挑的表情重拍：分不清屬於哪一集，三集與 shared 都放（GitHub 只存一次）


def branches_of(rel: str) -> set[str]:
    if MULTI.match(rel):
        return {"e001", "e002", "e003", "shared"}
    return {branch_of(rel)}


def branch_of(rel: str) -> str:
    parts = rel.split("/")
    head = "/".join(parts[:3]) if parts[0] == "_scratchpad" else "/".join(parts[:2])
    if rel.startswith("_scratchpad/pilot/") or "e001-pilot" in head:
        return "e001"
    eps = set(EP.findall(head.replace("_scratchpad/", "/")))
    return f"e{eps.pop()}" if len(eps) == 1 else "shared"


def walk():
    """(local path, branch path, is_link) for every file we keep; plus the skipped ones."""
    keep, skipped = [], []
    for root, prefix in ROOTS:
        for dirpath, dirnames, filenames in os.walk(root):
            rel_dir = os.path.relpath(dirpath, root)
            if rel_dir == ".":
                dirnames[:] = [d for d in dirnames if not SKIP_TOP.match(d)]
            names = list(filenames) + [d for d in dirnames if os.path.islink(os.path.join(dirpath, d))]
            dirnames[:] = [d for d in dirnames if not os.path.islink(os.path.join(dirpath, d))]
            for n in names:
                full = os.path.join(dirpath, n)
                rel = os.path.normpath(os.path.join(prefix, rel_dir, n))
                if "/segments-v4/" in f"/{rel}" and n.endswith(".mkv"):
                    skipped.append(rel)
                    continue
                if not os.path.islink(full) and not os.path.isfile(full):
                    continue
                keep.append((full, rel, os.path.islink(full)))
    return keep, skipped


def git(gd: str, *args: str, inp: bytes | None = None) -> str:
    env = dict(os.environ, GIT_DIR=gd)
    return subprocess.run(["git", *args], env=env, input=inp, capture_output=True, check=True).stdout.decode()


CHUNK = 1_200_000_000  # 2026-11-09：容器磁碟只剩幾 GB，一次建整條分支的暫存庫（第 1 集 5 GB）會塞爆；改成每 1.2 GB 推一次、推完刪暫存


def hobj(data_or_path, write_gd=None, stdin=False):
    # --no-filters：在 travel_scanner 裡跑會套用它的 .gitattributes（eol=lf），CRLF 檔的雜湊就跟存進去的原始內容不一樣（audit7，2026-11-09）
    args = ["git", "hash-object", "--no-filters"] + (["-w"] if write_gd else []) + (["--stdin"] if stdin else [data_or_path])
    env = dict(os.environ, GIT_DIR=write_gd) if write_gd else None
    return subprocess.run(args, input=data_or_path if stdin else None, capture_output=True, check=True, env=env).stdout.decode().strip()


def push(name: str) -> int:
    keep, skipped = walk()
    mine = [k for k in keep if name in branches_of(k[1])]
    br = f"transfer/tn-{name}"
    # 2026-11-09 站主：祖媽的備份另開 repo（x812033727/drama-backup-tn），travel_scanner 快到容量上限
    remote = os.environ.get("TN_BACKUP_REMOTE", "https://github.com/x812033727/drama-backup-tn")
    if len(mine) < 30:
        print(f"ABORT {br}: only {len(mine)} files", file=sys.stderr)
        return 1
    # 先算好每一筆（不寫物件）：(mode, sha, path, size, source) source = ("file", full) | ("part", full, k) | ("data", bytes)
    entries, manifest, total = [], [], 0
    for full, rel, link in sorted(mine, key=lambda k: k[1]):
        if link:
            target = os.readlink(full)
            # 連結指到 scratchpad 或 ~/mokaair-work/videos 的，改成分支裡的相對路徑（不存含 session id 的絕對路徑；audit4 2026-11-08）
            for root, prefix in ROOTS + [(V, "")]:
                if target.startswith(str(root) + "/"):
                    dest = os.path.normpath(os.path.join(prefix, os.path.relpath(target, root)))
                    target = os.path.relpath(dest, os.path.dirname(rel) or ".")
                    break
            sha = hobj(target.encode(), stdin=True)
            entries.append(("120000", sha, rel, 0, ("data", target.encode())))
            manifest.append(f"{rel}\tlink\t{sha}\t{full}")
            continue
        size = os.path.getsize(full)
        total += size
        if size > BIG:
            k = 0
            with open(full, "rb") as fh:
                while chunk := fh.read(PART):
                    entries.append(("100644", hobj(chunk, stdin=True), f"{rel}.part{k:02d}", len(chunk), ("part", full, k)))
                    k += 1
            manifest.append(f"{rel}\t{size}\t{hobj(full)}\t{full}\tparts={k}")
        else:
            sha = hobj(full)
            mode = "100755" if os.access(full, os.X_OK) else "100644"
            entries.append((mode, sha, rel, size, ("file", full)))
            manifest.append(f"{rel}\t{size}\t{sha}\t{full}")
    stamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    readme = f"""# {br}

《恁祖媽今年18》{'第 ' + str(int(name[1:])) + ' 集' if name != 'shared' else '跨集共用'}的備份，規則見 travel_scanner 的 `docs/videos/drama/BACKUP-BRANCHES.md`。備份放在 `x812033727/drama-backup-tn`（2026-11-09 起；之前在 travel_scanner 的同名分支）。

- 時間：{stamp}；{len(mine)} 個檔，{total / 1e9:.2f} GB（切塊前）。清單與雜湊在 `MANIFEST.tsv`（分支路徑、大小、git blob 雜湊、本機原路徑）。
- 路徑相對於 `~/mokaair-work/videos/`；Claude 的 scratchpad 放在 `_scratchpad/`。
- 大於 95 MB 的檔切成 `X.part00`、`X.part01`…（90 MiB），還原：`cat X.part* > X`；MANIFEST 記著整檔的雜湊。
- **沒放的**：`segments-v4/*.mkv`（合成的中間檔，站主 2026-11-08 同意不備份，`post/assemble-v4.mjs` 重建；較早的 `tn-*-work` 分支裡有）；
  git worktree `wt2047`（本 repo 的 PR 分支，內容就在 GitHub）；`wt2038` 打包在 shared 的 `_scratchpad/_backup-archives/wt2038.tar`。
  音效是從種田的音效庫複製來的（`_series/zhong-tian-qu-qi/sfx`，在種田的分支），複本在 tn-shared 的 `_series/tai-nainai/sfx/`。
- 舊的分支 `tn-e001-work`、`tn-e001-work-v2`、`tn-e002-work`、`tn-e003-work`、`tn-series-assets`、`tn-all-work` 保留不動（絕對路徑）。
- 還原一集要**這一集的分支加上 `transfer/tn-shared`**（音效、配樂、參考圖、腳本、`wt2038.tar` 都在 shared）：兩條都
  `git fetch https://github.com/x812033727/drama-backup-tn <分支>`、`git archive FETCH_HEAD | tar x -C ~/mokaair-work/videos`，再把 `_scratchpad/` 搬到新 session 的 scratchpad、
  `cat X.part* > X` 接回切塊（MANIFEST 有整檔雜湊可核對）。連結存成相對路徑，解開後就接得上。
- `_scratchpad/e001-post/*/music` 這類指到 `_series/tai-nainai/music` 的連結存成相對路徑，`_scratchpad/` 搬離 `~/mokaair-work/videos/` 後會斷：還原後用 `find _scratchpad -xtype l` 列出斷掉的連結，再 `ln -sfn ~/mokaair-work/videos/_series/tai-nainai/music <連結>` 重做。
- 空資料夾 git 存不了：清單在 shared 的 `_scratchpad/_backup-archives/empty-dirs.txt`，還原後 `mkdir -p` 補回。
- `_scratchpad/pick-expr*`（三集一起挑的表情重拍）三集與 shared 都放，同一份檔 GitHub 只存一次。
"""
    for nm, content in (("README-backup.md", readme), ("MANIFEST.tsv", "path\tsize\tsha\tlocal\textra\n" + "\n".join(manifest) + "\n")):
        entries.append(("100644", hobj(content.encode(), stdin=True), nm, len(content), ("data", content.encode())))
    groups, cur, acc = [], [], 0
    for e in entries:
        if cur and acc + e[3] > CHUNK:
            groups.append(cur); cur, acc = [], 0
        cur.append(e); acc += e[3]
    groups.append(cur)
    env0 = dict(os.environ, GIT_AUTHOR_NAME="Claude", GIT_AUTHOR_EMAIL="noreply@anthropic.com", GIT_COMMITTER_NAME="Claude", GIT_COMMITTER_EMAIL="noreply@anthropic.com")
    last = None
    for gi, grp in enumerate(groups):
        gd = tempfile.mkdtemp(prefix=f"tnbk-{name}-", dir=S) + "/g.git"
        git(gd, "init", "-q", "--bare")
        env = dict(env0, GIT_DIR=gd, GIT_INDEX_FILE=gd + "/idx")
        parent = []
        if subprocess.run(["git", "--git-dir", gd, "fetch", "-q", "--filter=blob:none", remote, f"refs/heads/{br}:refs/remotes/prev"], capture_output=True).returncode == 0:
            prev = git(gd, "rev-parse", "refs/remotes/prev").strip()
            parent = ["-p", prev]
            if gi > 0:  # 第一塊從空的樹開始（本機已刪的檔不留下）；之後每塊接在剛推上去的那一塊上
                subprocess.run(["git", "read-tree", prev], env=env, check=True)
        for mode, sha, path, size, src in grp:
            if src[0] == "file":
                got = hobj(src[1], write_gd=gd)
            elif src[0] == "part":
                with open(src[1], "rb") as fh:
                    fh.seek(src[2] * PART); got = hobj(fh.read(PART), write_gd=gd, stdin=True)
            else:
                got = hobj(src[1], write_gd=gd, stdin=True)
            if got != sha:  # 正在跑的工作（進度檔）在備份中途改了：用新內容，記下來
                print(f"  note: {path} changed while backing up; stored the newer version", flush=True)
                grp[grp.index((mode, sha, path, size, src))] = (mode, got, path, size, src)
        subprocess.run(["git", "update-index", "--add", "--index-info"], env=env, input=("\n".join(f"{m} {h}\t{p}" for m, h, p, _, _ in grp) + "\n").encode(), check=True)
        tree = subprocess.run(["git", "write-tree", "--missing-ok"], env=env, capture_output=True, text=True, check=True).stdout.strip()
        msg = f"{br}: {len(mine)} files {stamp} (part {gi + 1}/{len(groups)})"
        last = subprocess.run(["git", "commit-tree", tree, *parent, "-m", msg], env=env, capture_output=True, text=True, check=True).stdout.strip()
        subprocess.run(["git", "--git-dir", gd, "push", "-q", remote, f"{last}:refs/heads/{br}"], check=True)
        subprocess.run(["rm", "-rf", os.path.dirname(gd)])
        print(f"  pushed part {gi + 1}/{len(groups)} {sum(e[3] for e in grp) / 1e9:.2f} GB", flush=True)
    got = subprocess.run(["git", "ls-remote", remote, f"refs/heads/{br}"], capture_output=True, text=True).stdout.split()[:1]
    print(f"{br} files {len(mine)} {total / 1e9:.2f} GB local {last} remote {got[0] if got else '-'}")
    return 0 if got and got[0] == last else 1


def main(argv: list[str]) -> int:
    if argv[:1] == ["plan"]:
        keep, skipped = walk()
        by = {}
        for _, rel, _ in keep:
            for b in branches_of(rel):
                by.setdefault(b, []).append(rel)
        for b, files in sorted(by.items()):
            print(f"tn-{b}: {len(files)} files")
        print(f"skipped (segments-v4 mkv): {len(skipped)}")
        return 0
    if argv[:1] == ["push"] and len(argv) == 2:
        return push(argv[1])
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
