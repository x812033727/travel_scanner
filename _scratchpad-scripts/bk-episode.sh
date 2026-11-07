#!/usr/bin/env bash
# bk-episode.sh N|shared : one backup branch per episode plus one shared branch (owner 2026-11-07: 「一集一個分支」,
# 「跨集共用可以共同放一個：音效庫、配樂、試鏡、參考圖各輪、我寫的腳本，其他每一集的全部放每一集的分支」).
#   N      -> transfer/zt-live-e00N : the episode's whole work folder (drafts, refines, the model's own voice, prompts,
#             manifests, cut logs, import folder) except its music/, plus its r2 publish folder;
#   shared -> transfer/zt-shared    : _series/zhong-tian-qu-qi (sound library, every reference round, screen tests),
#             _live-pilot, every episode's music/, and the scratchpad scripts (bk-*, verify-*, chains, builders).
# Each run adds a commit on top of the branch (fast-forward, never forced), so earlier versions stay in its history.
# Left out (rebuilt free): clips/, segments-v4/, cut/*.mp4, review/ previews and frames. Files over 95 MB are split.
set -u
N=$1
V=$HOME/mokaair-work/videos
S=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad
REMOTE=https://github.com/x812033727/travel_scanner
if [ "$N" = shared ]; then
  EP=shared; BR=zt-shared
  mkdir -p "$V/_scratchpad-scripts"; cp -p "$S"/*.sh "$S"/*.py "$V/_scratchpad-scripts/" 2>/dev/null
  DIRS=("_series/zhong-tian-qu-qi" "_live-pilot" "_scratchpad-scripts")
  for m in "$V"/zhong-tian-qu-qi-e9*-dh/music; do DIRS+=("${m#$V/}"); done
  NOMUSIC=()
else
  EP=$(printf '%03d' $N); BR=zt-live-e$EP
  DIRS=("zhong-tian-qu-qi-e90$N-dh")
  [ -d "$V/zhong-tian-qu-qi-e$EP-r2" ] && DIRS+=("zhong-tian-qu-qi-e$EP-r2")
  NOMUSIC=(! -path "*/music/*")
fi
G=$S/bk-ep-$EP.git; rm -rf "${G:?}"; git init -q --bare "$G"; export GIT_DIR=$G GIT_INDEX_FILE=$G/index
PARENT=$(git ls-remote $REMOTE "refs/heads/transfer/$BR" | cut -f1)
[ -n "$PARENT" ] && git fetch -q --depth=1 --filter=blob:none $REMOTE "+refs/heads/transfer/$BR:refs/heads/prev"
n=0; bytes=0; parts=0
for d in "${DIRS[@]}"; do
  while IFS= read -r -d '' f; do
    rel=${f#$V/}; sz=$(stat -c %s "$f")
    if [ "$sz" -gt 95000000 ]; then
      tmp=$S/bk-split-$EP; mkdir -p "$tmp"; rm -f "${tmp:?}"/*; split -b 90m -d -a 2 "$f" "$tmp/p"
      for p in "$tmp"/p*; do h=$(git hash-object -w "$p"); printf '100644 %s\t%s\n' "$h" "$rel.part${p##*/p}" | git update-index --add --index-info; parts=$((parts+1)); done
      rm -f "${tmp:?}"/*
    else
      h=$(git hash-object -w "$f"); printf '100644 %s\t%s\n' "$h" "$rel" | git update-index --add --index-info
    fi
    n=$((n+1)); bytes=$((bytes+sz))
  done < <(find "$V/$d" -type f ! -path "*/clips/*" ! -path "*/segments-v4/*" ! -path "*/cut/*.mp4" ! -path "*/review/*.mp4" ! -path "*/review/*.jpg" ! -path "*/review/*.png" ! -name "*.part??" "${NOMUSIC[@]}" -print0)
done
readme=$(mktemp); cat > "$readme" <<R
# 種田娶妻打天下 $BR：重做需要的檔案

一集一條分支，跨集共用的放 transfer/zt-shared（站主 2026-11-07）。$(date -u +%F\ %T) UTC，$n 個檔，$((bytes/1000000)) MB，$parts 個分割檔。
還原：把每個資料夾複製回 ~/mokaair-work/videos/。X.part00、X.part01… 是超過 95 MB 的檔案分割：\`cat X.part* > X\`。
包含：${DIRS[*]}。重做一集要這條分支加上 transfer/zt-shared（音效、配樂、參考圖、試鏡、腳本）。
不含（工具免費重建）：clips/、segments-v4/、cut/*.mp4、review/ 的預覽與格子圖。
R
h=$(git hash-object -w "$readme"); printf '100644 %s\t%s\n' "$h" "README-backup.md" | git update-index --add --index-info; rm -f "$readme"
T=$(git write-tree)
MSG=$(printf 'zhong-tian e%s backup %s\n\n%s files, %s MB, %s split parts.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_018EYovKNmSMKVnfFFMhZJH2\n' "$EP" "$(date -u +%F)" "$n" "$((bytes/1000000))" "$parts")
if [ -n "$PARENT" ]; then C=$(echo "$MSG" | git commit-tree "$T" -p "$PARENT"); else C=$(echo "$MSG" | git commit-tree "$T"); fi
ok=0; for w in 2 4 8 16 0; do git push -q $REMOTE "$C:refs/heads/transfer/$BR" 2>&1 && { ok=1; break; }; [ "$w" = 0 ] || sleep "$w"; done
got=$(git ls-remote $REMOTE "refs/heads/transfer/$BR" | cut -f1)
unset GIT_DIR GIT_INDEX_FILE; rm -rf "${G:?}"
[ "$ok" = 1 ] && [ "$got" = "$C" ] && echo "OK transfer/$BR $C $n files $((bytes/1000000)) MB parts=$parts" || echo "FAIL transfer/$BR (pushed=$ok remote=$got local=$C)"
