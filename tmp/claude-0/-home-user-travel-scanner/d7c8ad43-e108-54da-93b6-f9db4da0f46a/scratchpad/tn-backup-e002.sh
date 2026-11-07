#!/usr/bin/env bash
# 《恁祖媽今年18》第 2 集重製所需的全部工作檔 → transfer/tn-e002-work（站主 2026-11-07：應該要重製的所有檔案都要備份到）
set -uo pipefail
S=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad
REMOTE=$(git -C /home/user/travel_scanner remote get-url origin)
G=$S/tnbk2.git; P=$S/tnbk2-parts; rm -rf $G $P; mkdir -p $P
export GIT_DIR=$G GIT_WORK_TREE=/
git init -q; git config user.name Claude; git config user.email noreply@anthropic.com; git config core.bigFileThreshold 50m
R=${S#/}
cat > $G/info/exclude <<EOF
/$R/e002/refs/
/$R/e002/st2-dry/
/$R/e002-post/cut-draft/
/$R/e002-post/draftwork/
/$R/e002-post/final/segments-v4/
segments-v4/
EOF
big=$(find $S/e002 $S/e002-post $HOME/mokaair-work/videos/_series/tai-nainai $HOME/mokaair-work/videos/tai-nainai-import -type f -size +95M -not -path "*/segments-v4/*" -not -path "*/cut-draft/*")
for f in $big; do echo "/${f#/}" >> $G/info/exclude; done
cd /
git add -- "$R/e002" "$R/e002-post" "$R/zt-backup.sh" "$R/tn-backup.sh" "${HOME#/}/mokaair-work/videos/_series/tai-nainai" "${HOME#/}/mokaair-work/videos/tai-nainai-import"
for f in $big; do rel=${f#/}; mkdir -p "$P/$(dirname $rel)"; split -b 90m -d "$f" "$P/$rel.part"; GIT_WORK_TREE=$P git add -- "$rel".part*; done
cat > $P/README-backup.md <<EOF
# 《恁祖媽今年18》第 2 集工作檔備份（$(date -u +%F)）

路徑照原本的絕對路徑存（scratchpad 與 ~/mokaair-work/videos）；還原：把各資料夾複製回同一個位置（或改 W=…）。
X.part00、X.part01… 是超過 95 MB 的單一檔案，\`cat X.part* > X\` 接回。
不放：e002/refs（repo 的 production/assets/refs 有）、segments-v4（assemble-v4 重建）。
內容：e002/（草稿 out、trimmed、manifest、提示詞、之後的重拍與精修）；e002-post/（台詞、連戲表與審片截圖、成片）；_series/tai-nainai（音效庫、四首配樂、試鏡與參考圖各輪）；tai-nainai-import（匯入用的檔）。每個階段做完推一次，分支只往前加。
EOF
GIT_WORK_TREE=$P git add README-backup.md
n=$(git ls-files | wc -l)
git fetch -q "$REMOTE" refs/heads/transfer/tn-e002-work:refs/remotes/bk/prev 2>/dev/null && PARENT=$(git rev-parse refs/remotes/bk/prev) || PARENT=
tree=$(git write-tree); sha=$(git commit-tree $tree ${PARENT:+-p $PARENT} -m "tai-nainai e002 work backup $(date -u +%F) ($n files)"); git update-ref HEAD $sha
: git commit -q -m "tai-nainai e002 work backup $(date -u +%F): everything a remake needs ($n files)"
sha=$(git rev-parse HEAD)
for i in 1 2 3 4; do git push -q "$REMOTE" HEAD:refs/heads/transfer/tn-e002-work 2>&1 | grep -v "^remote:" | tail -2 && break; sleep $((2**i)); done
r=$(git ls-remote "$REMOTE" refs/heads/transfer/tn-e002-work | cut -f1)
echo "files $n local $sha remote $r"
