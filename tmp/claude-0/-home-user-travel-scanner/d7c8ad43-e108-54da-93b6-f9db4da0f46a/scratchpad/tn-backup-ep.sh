#!/usr/bin/env bash
# 《恁祖媽今年18》一集一個分支（站主 2026-11-07）：tn-backup-ep.sh 001 → transfer/tn-e001-work
# 收：scratchpad 的 e001、e001-post、own/e001（模型原聲重拍）、（第 1 集另收 pilot）、~/mokaair-work/videos/tai-nainai-import/tai-nainai-e001
# 全部都收（站主 2026-11-07：檔案都要備份，不要漏掉任何你覺得沒用的檔）；只排除備份自己的暫存庫 tn*.git、tn*-parts。> 95 MB 切 .partNN。每次推接在前一次之後（不覆蓋）。
# 檔數少於 MIN_FILES 就不推；推完一定要另外跑 verify-backup.py（獨立代理）。
set -uo pipefail
EP=$1
S=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad
V=$HOME/mokaair-work/videos
BR=transfer/tn-e$EP-work
REMOTE=$(git -C /home/user/travel_scanner remote get-url origin)
G=$S/tnep$EP.git; P=$S/tnep$EP-parts; rm -rf $G $P; mkdir -p $P
export GIT_DIR=$G GIT_WORK_TREE=/
git init -q; git config user.name Claude; git config user.email noreply@anthropic.com; git config core.bigFileThreshold 50m
printf '%s\n' '/'"${S#/}"'/tn*.git/' '/'"${S#/}"'/tn*-parts/' > $G/info/exclude
paths=(); for p in $S/e$EP $S/e$EP-* $S/own/e$EP $V/tai-nainai-import/tai-nainai-e$EP; do [ -e "$p" ] && paths+=("${p#/}"); done
[ "$EP" = 001 ] && [ -e $S/pilot ] && paths+=("${S#/}/pilot")
# 那集用到的共用素材也放一份（站主 2026-11-07：每集分開分支放，單拿一條就能重做那一集）：音效庫、配樂、種田音效（sfx.sh 從它複製）、腳本與審片工具
for p in $V/_series/tai-nainai/sfx $V/_series/tai-nainai/music $V/_series/zhong-tian-qu-qi/sfx $S/asm2038 $S/*.sh $S/*.py; do [ -e "$p" ] && paths+=("${p#/}"); done
big=$(cd / && find "${paths[@]}" -type f -size +95M 2>/dev/null)
for f in $big; do echo "/$f" >> $G/info/exclude; done
cd /
git add --ignore-errors -- "${paths[@]}" 2>&1 | grep -v "^warning" | head -5
for f in $big; do mkdir -p "$P/$(dirname $f)"; split -b 90m -d "/$f" "$P/$f.part"; GIT_WORK_TREE=$P git add -f -- "$f".part*; done
n=$(git ls-files | wc -l)
[ "$n" -ge "${MIN_FILES:-200}" ] || { echo "ABORT: only $n files staged; nothing pushed"; exit 1; }
git fetch -q "$REMOTE" refs/heads/$BR:refs/remotes/bk/prev 2>/dev/null && PARENT=$(git rev-parse refs/remotes/bk/prev) || PARENT=
tree=$(git write-tree); sha=$(git commit-tree $tree ${PARENT:+-p $PARENT} -m "tai-nainai e$EP work $(date -u '+%F %T') ($n files)")
for i in 1 2 3 4; do git push -q "$REMOTE" $sha:refs/heads/$BR 2>&1 | grep -v "^remote:" | tail -1; r=$(git ls-remote "$REMOTE" refs/heads/$BR | cut -f1); [ "$r" = "$sha" ] && break; sleep $((2**i)); done
echo "$BR files $n local $sha remote $r"
rm -rf $P $G  # 暫存庫推完就清（內容都在原資料夾與遠端）
