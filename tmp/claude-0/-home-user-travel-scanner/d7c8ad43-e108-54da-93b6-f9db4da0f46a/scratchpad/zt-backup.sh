#!/usr/bin/env bash
# 《種田》工作資料夾備份到 transfer/zt-eNNN-media，驗證後才刪本機（站主 2026-11-07：「種田如果有備份後就可以刪除」）。
# 每集一個暫存 git 庫（GIT_DIR 在 scratchpad，工作樹直接指 ~/mokaair-work/videos，不複製檔案）；> 95 MB 的檔切成 .partNN。
# 備份：<集>-dh/ 與 <集>/ 底下全部，只有 segments-v4/（assemble 重建）與 review/（匯入預覽）不放。
# 驗證：遠端分支的 sha = 本機提交；`git status` 對這些路徑是空的（檔案從提交後沒變）。都過才 rm -rf。
set -uo pipefail
V=$HOME/mokaair-work/videos
S=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad/zt-backup
REMOTE=$(git -C /home/user/travel_scanner remote get-url origin)
mkdir -p $S
for ep in "$@"; do
  dirs=(); for d in zhong-tian-qu-qi-$ep-dh zhong-tian-qu-qi-$ep zhong-tian-qu-qi-$ep-site; do [ -d "$V/$d" ] && dirs+=("$d"); done
  [ ${#dirs[@]} -eq 0 ] && { echo "== $ep: nothing"; continue; }
  need=$(du -sk --exclude=segments-v4 --exclude=review "${dirs[@]/#/$V/}" | awk '{s+=$1} END {print int(s/1024)}')
  free=$(df -k --output=avail $V | tail -1 | awk '{print int($1/1024)}')
  echo "== $ep: ${dirs[*]} need ${need} MB, free ${free} MB"
  if [ $((free - need)) -lt 400 ]; then echo "== $ep: not enough disk, skipped"; continue; fi
  G=$S/$ep.git; P=$S/$ep-parts; rm -rf $G $P; mkdir -p $P
  export GIT_DIR=$G GIT_WORK_TREE=$V
  git init -q && git config user.name "Claude" && git config user.email "noreply@anthropic.com" && git config core.bigFileThreshold 50m
  printf '%s\n' segments-v4/ review/ > $G/info/exclude
  big=$(find "${dirs[@]/#/$V/}" -type f -size +95M -not -path "*/segments-v4/*" -not -path "*/review/*")
  for f in $big; do echo "/${f#$V/}" >> $G/info/exclude; done
  git add -- "${dirs[@]}" || { echo "== $ep: add failed"; continue; }
  # 大檔切片放在暫存的 parts 工作樹，另加
  for f in $big; do
    rel=${f#$V/}; mkdir -p "$P/$(dirname $rel)"; split -b 90m -d "$f" "$P/$rel.part"
    GIT_WORK_TREE=$P git add -- "$rel".part*
  done
  files=$(git ls-files | wc -l); mb=$(du -sm $G | cut -f1)
  printf '# 種田娶妻打天下 work-folder backup: %s\n\nMade %s from ~/mokaair-work/videos (%s files, objects %s MB).\nRestore: copy each folder back to ~/mokaair-work/videos/. A file named X.part00, X.part01 ... is one file over 95 MB split for GitHub: `cat X.part* > X`.\nLeft out (the tools rebuild them): segments-v4/ (assemble-v4 / dub.sh), review/ (the import preview).\n' \
    "${dirs[*]}" "$(date -u +%F)" "$files" "$mb" > $P/README-backup.md
  GIT_WORK_TREE=$P git add README-backup.md
  git commit -q -m "zhong-tian work-folder backup $(date -u +%F): ${dirs[*]}" || { echo "== $ep: commit failed"; continue; }
  sha=$(git rev-parse HEAD)
  ok=0; for i in 1 2 3 4; do git push -q "$REMOTE" HEAD:refs/heads/transfer/zt-$ep-media 2>&1 | tail -2 && ok=1 && break; sleep $((2**i)); done
  remote=$(git ls-remote "$REMOTE" refs/heads/transfer/zt-$ep-media | cut -f1)
  changed=$(git status --porcelain -- "${dirs[@]}" | wc -l)
  if [ "$remote" = "$sha" ] && [ "$changed" -eq 0 ]; then
    echo "== $ep: verified ($files files, $sha); deleting ${dirs[*]}"
    unset GIT_DIR GIT_WORK_TREE
    for d in "${dirs[@]}"; do rm -rf "$V/$d"; done
  else
    echo "== $ep: NOT verified (remote ${remote:-none} vs $sha, changed $changed); kept"
    unset GIT_DIR GIT_WORK_TREE
  fi
  rm -rf $G $P
  df -h $V | tail -1
done
echo "== done"
