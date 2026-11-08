#!/usr/bin/env bash
# bk-episode.sh 1..6 | cg N | old NNN | shared | cg-shared : back up EVERY file (owner 2026-11-07: 「檔案都要備份，不要漏備份某個你覺得沒用的檔案」;
# 「一集一個分支」; 「跨集共用可以共同放一個：音效庫、配樂、試鏡、參考圖各輪、我寫的腳本」).
#   N        -> transfer/zt-live-e00N : zhong-tian-qu-qi-e90N-dh (everything but music/), _live-e90N, zhong-tian-qu-qi-e00N-r2,
#                                       zhong-tian-qu-qi-import/zhong-tian-qu-qi-e00N-r2
#   old NNN  -> transfer/zt-live-eNNN : zhong-tian-qu-qi-eNNN, zhong-tian-qu-qi-import/zhong-tian-qu-qi-eNNN
#   shared   -> transfer/zt-shared    : _series, _live-pilot, every music/, compilations, the files at the top of the
#                                       work folder and of the import folder, and the whole scratchpad (as _scratchpad/)
# Nothing is skipped except one secret: the pod gate token (scratchpad/h3r-state) and this script's own temp repos.
# Each run adds a commit on top of the branch (fast-forward, never forced). Files over 95 MB are split into 90 MiB parts.
set -u
V=$HOME/mokaair-work/videos
S=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad
REMOTE=https://github.com/x812033727/travel_scanner
LIST=$(mktemp)   # lines: <absolute file>\t<path in the branch>
add_dir() { [ -e "$1" ] && find "$1" -type f "${@:3}" -print0 | while IFS= read -r -d '' f; do printf '%s\t%s\n' "$f" "$2${f#$1}"; done >> "$LIST"; }
case "$1" in
  shared)
    # live action and what both versions use; the 3D CG era goes to cg-shared (owner 2026-11-08: 拆分支, bk-shared-split.py)
    BR=zt-shared
    python3 "$S/bk-shared-split.py" live >> "$LIST" || exit 1 ;;
  cg-shared)
    BR=zt-cg-shared
    python3 "$S/bk-shared-split.py" cg >> "$LIST" || exit 1 ;;
  cg)
    # owner 2026-11-08: the 3D CG era files of a remade episode go on their own branch, not mixed with the live ones
    N=$2; EP=$(printf '%03d' "$N"); BR=zt-cg-e$EP
    python3 "$S/bk-cg-list.py" "$N" >> "$LIST" || exit 1 ;;
  old)
    EP=$2; BR=zt-live-e$EP
    add_dir "$V/zhong-tian-qu-qi-e$EP" "zhong-tian-qu-qi-e$EP"
    add_dir "$V/zhong-tian-qu-qi-import/zhong-tian-qu-qi-e$EP" "zhong-tian-qu-qi-import/zhong-tian-qu-qi-e$EP" ;;
  *)
    N=$1; EP=$(printf '%03d' "$N"); BR=zt-live-e$EP
    # owner 2026-11-08: 「只留重剪需要的 但不能漏」: the branch tip holds what a re-cut needs (bk-lean-list.py; a cut
    # rebuilt from it alone matched the delivered one bit for bit); the earlier full backups stay in the branch history.
    # FULL=1 lists every file of the episode folders as before.
    if [ "${FULL:-0}" != 1 ]; then python3 "$S/bk-lean-list.py" "$N" >> "$LIST" || exit 1; else
    add_dir "$V/zhong-tian-qu-qi-e90$N-dh" "zhong-tian-qu-qi-e90$N-dh" ! -path "$V/zhong-tian-qu-qi-e90$N-dh/music/*"
    add_dir "$V/zhong-tian-qu-qi-e$EP-r2" "zhong-tian-qu-qi-e$EP-r2"
    add_dir "$V/_live-e90$N" "_live-e90$N"   # the live-action refine/cut workdir (missed until 2026-11-08 coverage)
    add_dir "$V/zhong-tian-qu-qi-import/zhong-tian-qu-qi-e$EP-r2" "zhong-tian-qu-qi-import/zhong-tian-qu-qi-e$EP-r2"; fi ;;
esac
cp "$LIST" "$S/bk-list-$BR.tsv"   # verify-episode.py checks exactly this list
G=$S/bk-$BR.git; rm -rf "${G:?}"; git init -q --bare "$G"; export GIT_DIR=$G GIT_INDEX_FILE=$G/index
PARENT=$(git ls-remote $REMOTE "refs/heads/transfer/$BR" | cut -f1)
[ -n "$PARENT" ] && git fetch -q --depth=1 --filter=blob:none $REMOTE "+refs/heads/transfer/$BR:refs/heads/prev"
n=0; bytes=0; parts=0
while IFS=$'\t' read -r f rel; do
  sz=$(stat -c %s "$f")
  if [ "$sz" -gt 95000000 ]; then
    tmp=$S/bk-split-$BR; mkdir -p "$tmp"; rm -f "${tmp:?}"/*; split -b 90m -d -a 2 "$f" "$tmp/p"
    for p in "$tmp"/p*; do h=$(git hash-object -w "$p"); printf '100644 %s\t%s\n' "$h" "$rel.part${p##*/p}" | git update-index --add --index-info; parts=$((parts+1)); done
    rm -rf "${tmp:?}"
  else
    h=$(git hash-object -w "$f"); printf '100644 %s\t%s\n' "$h" "$rel" | git update-index --add --index-info
  fi
  n=$((n+1)); bytes=$((bytes+sz))
done < "$LIST"
readme=$(mktemp); cat > "$readme" <<R
# 種田娶妻打天下 $BR：全部檔案

$(date -u +%F\ %T) UTC，$n 個檔，$((bytes/1000000)) MB，$parts 個分割檔。站主 2026-11-07：所有檔案都要備份，一集一條分支，跨集共用的放 transfer/zt-shared。
還原：每個資料夾複製回 ~/mokaair-work/videos/（_scratchpad/ 是當時的 Claude scratchpad）。X.part00、X.part01… 是超過 95 MB 的檔案分割：\`cat X.part* > X\`。
沒有放的只有 pod 的登入憑證（scratchpad/h3r-state，是密碼，重開 pod 時會重新產生）。
每一集的分支（站主 2026-11-08：「只留重剪需要的 但不能漏」）：最新這一版只放重剪需要的檔（選中的草稿與精修、錄音、picks.json、精修提示詞、成片、後台匯入資料夾；清單見 _scratchpad/bk-lean-list.py），只用這些加上 transfer/zt-shared 的配樂與音效重剪，成片與交出去的逐位元相同。沒選中的草稿、被換掉的精修、CG 時期的檔、剪片中間檔在這條分支較早的 commit 裡（git log，一版都沒刪）。
R
h=$(git hash-object -w "$readme"); printf '100644 %s\t%s\n' "$h" "README-backup.md" | git update-index --add --index-info; rm -f "$readme" "$LIST"
T=$(git write-tree)
MSG=$(printf 'zhong-tian %s backup %s\n\n%s files, %s MB, %s split parts, nothing skipped but the pod token.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_018EYovKNmSMKVnfFFMhZJH2\n' "$BR" "$(date -u +%F)" "$n" "$((bytes/1000000))" "$parts")
if [ -n "$PARENT" ]; then C=$(echo "$MSG" | git commit-tree "$T" -p "$PARENT"); else C=$(echo "$MSG" | git commit-tree "$T"); fi
ok=0; for w in 2 4 8 16 0; do git push -q $REMOTE "$C:refs/heads/transfer/$BR" 2>&1 && { ok=1; break; }; [ "$w" = 0 ] || sleep "$w"; done
got=$(git ls-remote $REMOTE "refs/heads/transfer/$BR" | cut -f1)
unset GIT_DIR GIT_INDEX_FILE; rm -rf "${G:?}"
[ "$ok" = 1 ] && [ "$got" = "$C" ] && echo "OK transfer/$BR $C $n files $((bytes/1000000)) MB parts=$parts" || echo "FAIL transfer/$BR (pushed=$ok remote=$got local=$C)"
