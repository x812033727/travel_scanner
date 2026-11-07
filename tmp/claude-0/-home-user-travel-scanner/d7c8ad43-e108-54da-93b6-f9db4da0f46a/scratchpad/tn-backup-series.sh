#!/usr/bin/env bash
# 《恁祖媽今年18》系列分支 transfer/tn-series-assets：scratchpad 裡不屬於任何一集的全部檔案（腳本、log、試鏡與參考圖各輪、測試、審片工具…），
# 加上 ~/mokaair-work/videos 的 _series/tai-nainai（音效庫、配樂、試鏡）、_series/zhong-tian-qu-qi/sfx（post/sfx.sh 從它複製）、tai-nainai-import。
# 全部都收（站主 2026-11-07）；只排除備份自己的暫存庫 tn*.git、tn*-parts。路徑照絕對路徑存（去掉開頭的 /）。每次推接在前一次之後。
set -uo pipefail
S=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad
V=$HOME/mokaair-work/videos
REMOTE=$(git -C /home/user/travel_scanner remote get-url origin)
BR=transfer/tn-series-assets
G=$S/tnser.git; P=$S/tnser-parts; rm -rf $G $P; mkdir -p $P
export GIT_DIR=$G GIT_WORK_TREE=/
git init -q; git config user.name Claude; git config user.email noreply@anthropic.com; git config core.bigFileThreshold 50m
printf '%s\n' '/'"${S#/}"'/tn*.git/' '/'"${S#/}"'/tn*-parts/' > $G/info/exclude
# 含 .git 檔的資料夾（git worktree）git add 只會存成提交連結、裡面的檔不會進來（2026-11-07 全面驗證抓到 wt2038）：打包成 tar 放進去
mkdir -p $S/_backup-archives
for w in $(find $S -mindepth 1 -maxdepth 3 -name .git -not -path "$S/tn*" -printf '%h\n'); do
  tar cf $S/_backup-archives/$(basename $w).tar -C $(dirname $w) $(basename $w); echo "/${w#/}/" >> $G/info/exclude; done
paths=()
for p in $S/* $S/.[!.]*; do b=$(basename $p); case $b in e0[0-9][0-9]|e0[0-9][0-9]-*|pilot|own|tn*.git|tn*-parts) continue;; esac; [ -e "$p" ] && paths+=("${p#/}"); done
for p in $S/own/*; do case $(basename $p) in e0[0-9][0-9]) continue;; esac; paths+=("${p#/}"); done
for p in $V/_series/tai-nainai $V/_series/zhong-tian-qu-qi/sfx $V/tai-nainai-import; do [ -e "$p" ] && paths+=("${p#/}"); done
big=$(cd / && find "${paths[@]}" -type f -size +95M 2>/dev/null)
for f in $big; do echo "/$f" >> $G/info/exclude; done
cd /
git add --ignore-errors -- "${paths[@]}" 2>&1 | grep -v "^warning" | head -5
for f in $big; do mkdir -p "$P/$(dirname $f)"; split -b 90m -d "/$f" "$P/$f.part"; GIT_WORK_TREE=$P git add -f -- "$f".part*; done
n=$(git ls-files | wc -l)
[ "$n" -ge 500 ] || { echo "ABORT: only $n files staged; nothing pushed"; exit 1; }
git fetch -q "$REMOTE" refs/heads/$BR:refs/remotes/bk/prev 2>/dev/null && PARENT=$(git rev-parse refs/remotes/bk/prev) || PARENT=
tree=$(git write-tree); sha=$(git commit-tree $tree ${PARENT:+-p $PARENT} -m "tai-nainai series and everything else $(date -u '+%F %T') ($n files)")
for i in 1 2 3 4; do git push -q "$REMOTE" $sha:refs/heads/$BR 2>&1 | grep -v "^remote:" | tail -1; r=$(git ls-remote "$REMOTE" refs/heads/$BR | cut -f1); [ "$r" = "$sha" ] && break; sleep $((2**i)); done
echo "$BR files $n local $sha remote $r"
rm -rf $P $G  # 暫存庫推完就清（內容都在原資料夾與遠端）
