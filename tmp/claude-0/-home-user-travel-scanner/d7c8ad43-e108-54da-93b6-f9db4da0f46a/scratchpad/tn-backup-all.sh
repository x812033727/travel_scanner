#!/usr/bin/env bash
# 《恁祖媽今年18》這台容器裡的全部工作檔 → transfer/tn-all-work（站主 2026-11-07：怕漏備份又要重做）
# 收：scratchpad 的 e0*、e0*-post、own、pilot、refs-r*、所有 *.sh／*.py 腳本；~/mokaair-work/videos 的 _series/tai-nainai、
#     _series/zhong-tian-qu-qi/sfx（post/sfx.sh 從它複製）、tai-nainai-import。
# 不收（可重建）：segments-v4/（assemble 重建）、*/refs/（repo 的 production/assets/refs 有一樣的圖）、*.git 暫存庫。
# > 95 MB 的檔切成 .partNN。每次推一個接在前一次之後的提交（不覆蓋）。驗證交給獨立代理：verify-backup.py。
set -uo pipefail
S=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad
V=$HOME/mokaair-work/videos
REMOTE=$(git -C /home/user/travel_scanner remote get-url origin)
G=$S/tnall.git; P=$S/tnall-parts; rm -rf $G $P; mkdir -p $P
export GIT_DIR=$G GIT_WORK_TREE=/
git init -q; git config user.name Claude; git config user.email noreply@anthropic.com; git config core.bigFileThreshold 50m
printf '%s\n' 'segments-v4/' '/'"${S#/}"'/*/refs/' '*.git/' 'tnall-parts/' 'tnbk*-parts/' '*.part[0-9][0-9]' > $G/info/exclude
paths=(); for p in $S/e0* $S/own $S/pilot $S/refs-r* $S/*.sh $S/*.py $V/_series/tai-nainai $V/_series/zhong-tian-qu-qi/sfx $V/tai-nainai-import; do [ -e "$p" ] && paths+=("${p#/}"); done
big=$(cd / && find "${paths[@]}" -type f -size +95M -not -path "*/segments-v4/*" -not -path "*/refs/*" 2>/dev/null)
for f in $big; do echo "/$f" >> $G/info/exclude; done
cd /
git add --ignore-errors -- "${paths[@]}" 2>&1 | grep -v "^warning" | head -5  # 正在跑的批次會刪暫存檔：單一檔案錯誤略過，其餘照加
for f in $big; do mkdir -p "$P/$(dirname $f)"; split -b 90m -d "/$f" "$P/$f.part"; GIT_WORK_TREE=$P git add -f -- "$f".part*; done
n=$(git ls-files | wc -l)
[ "$n" -ge "${MIN_FILES:-1000}" ] || { echo "ABORT: only $n files staged (expected >= ${MIN_FILES:-1000}); nothing pushed"; exit 1; }
git fetch -q "$REMOTE" refs/heads/transfer/tn-all-work:refs/remotes/bk/prev 2>/dev/null && PARENT=$(git rev-parse refs/remotes/bk/prev) || PARENT=
tree=$(git write-tree); sha=$(git commit-tree $tree ${PARENT:+-p $PARENT} -m "tai-nainai all work $(date -u '+%F %T') ($n files)")
for i in 1 2 3 4; do git push -q "$REMOTE" $sha:refs/heads/transfer/tn-all-work 2>&1 | grep -v "^remote:" | tail -1; r=$(git ls-remote "$REMOTE" refs/heads/transfer/tn-all-work | cut -f1); [ "$r" = "$sha" ] && break; sleep $((2**i)); done
echo "files $n local $sha remote $r"
git ls-tree -r $sha > $S/tnall-last.tree
rm -rf $P
