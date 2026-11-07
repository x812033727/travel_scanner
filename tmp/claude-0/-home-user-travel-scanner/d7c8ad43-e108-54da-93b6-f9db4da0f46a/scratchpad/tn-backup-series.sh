#!/usr/bin/env bash
# 《恁祖媽今年18》系列共用素材 → transfer/tn-series-assets（音效庫、配樂、試鏡與參考圖各輪）；每次推一個接在前一次之後的提交
set -uo pipefail
S=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad
REMOTE=$(git -C /home/user/travel_scanner remote get-url origin)
V=$HOME/mokaair-work/videos
G=$S/tnser.git; rm -rf $G
export GIT_DIR=$G GIT_WORK_TREE=$V
git init -q; git config user.name Claude; git config user.email noreply@anthropic.com
big=$(find $V/_series/tai-nainai $V/_series/zhong-tian-qu-qi/sfx -type f -size +95M)
[ -n "$big" ] && { echo "big files: $big"; exit 1; }
# 種田的音效庫也放：post/sfx.sh 從它複製一部分，沒有它就重建不出來
git add -- _series/tai-nainai _series/zhong-tian-qu-qi/sfx
n=$(git ls-files | wc -l)
git fetch -q "$REMOTE" refs/heads/transfer/tn-series-assets:refs/remotes/bk/prev 2>/dev/null && PARENT=$(git rev-parse refs/remotes/bk/prev) || PARENT=
tree=$(git write-tree); sha=$(git commit-tree $tree ${PARENT:+-p $PARENT} -m "tai-nainai series assets $(date -u +%F %T) ($n files): sfx library, music cues, screen-test and reference rounds; zhong-tian sfx that post/sfx.sh copies from")
for i in 1 2 3 4; do git push -q "$REMOTE" $sha:refs/heads/transfer/tn-series-assets 2>&1 | grep -v "^remote:" | tail -1 && break; sleep $((2**i)); done
r=$(git ls-remote "$REMOTE" refs/heads/transfer/tn-series-assets | cut -f1)
echo "files $n local $sha remote $r"
