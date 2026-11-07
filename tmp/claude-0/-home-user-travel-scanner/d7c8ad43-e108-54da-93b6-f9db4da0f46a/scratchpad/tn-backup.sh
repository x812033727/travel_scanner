#!/usr/bin/env bash
# 《恁祖媽今年18》第 1 集重製所需的全部工作檔 → transfer/tn-e001-work-v2（站主 2026-11-07：應該要重製的所有檔案都要備份到）
set -uo pipefail
S=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad
REMOTE=$(git -C /home/user/travel_scanner remote get-url origin)
G=$S/tnbk.git; P=$S/tnbk-parts; rm -rf $G $P; mkdir -p $P
export GIT_DIR=$G GIT_WORK_TREE=/
git init -q; git config user.name Claude; git config user.email noreply@anthropic.com; git config core.bigFileThreshold 50m
R=${S#/}
cat > $G/info/exclude <<EOF
/$R/e001/refs/
/$R/e001/st2-dry/
/$R/e001-post/cut-draft/
/$R/e001-post/draftwork/
/$R/e001-post/final/segments-v4/
segments-v4/
EOF
big=$(find $S/e001 $S/e001-post $HOME/mokaair-work/videos/_series/tai-nainai $HOME/mokaair-work/videos/tai-nainai-import -type f -size +95M -not -path "*/segments-v4/*" -not -path "*/cut-draft/*")
for f in $big; do echo "/${f#/}" >> $G/info/exclude; done
cd /
git add -- "$R/e001" "$R/e001-post" "$R/zt-backup.sh" "$R/tn-backup.sh" "${HOME#/}/mokaair-work/videos/_series/tai-nainai" "${HOME#/}/mokaair-work/videos/tai-nainai-import"
for f in $big; do rel=${f#/}; mkdir -p "$P/$(dirname $rel)"; split -b 90m -d "$f" "$P/$rel.part"; GIT_WORK_TREE=$P git add -- "$rel".part*; done
cat > $P/README-backup.md <<EOF
# 《恁祖媽今年18》第 1 集工作檔備份（$(date -u +%F)）

路徑照原本的絕對路徑存（scratchpad 與 ~/mokaair-work/videos）；還原：把各資料夾複製回同一個位置（或改 W=…）。
X.part00、X.part01… 是超過 95 MB 的單一檔案，\`cat X.part* > X\` 接回。
不放：e001/refs（repo 的 production/assets/refs 有）、e001/st2-dry、e001-post/cut-draft（草稿試剪，已被成片取代）、segments-v4（assemble-v4 重建）。
內容：e001/（草稿 out、trimmed、retake/retake3/retake5–8 的 manifest、提示詞、草稿與挑選、st2/refined 28 鏡精修、RESUME.md）；
e001-post/（audio 19 句、music 兩首、final/clips（c27-t2 為精修後從 1.8 秒剪）、final/cut 成片與 final.log、lines.json、字幕、手機版、連戲表與審片截圖）；
_series/tai-nainai（音效庫、試鏡與參考圖各輪）；tai-nainai-import（匯入用的 meta.json、縮圖、字幕）。
EOF
GIT_WORK_TREE=$P git add README-backup.md
n=$(git ls-files | wc -l)
git commit -q -m "tai-nainai e001 work backup $(date -u +%F): everything a remake needs ($n files)"
sha=$(git rev-parse HEAD)
for i in 1 2 3 4; do git push -q "$REMOTE" HEAD:refs/heads/transfer/tn-e001-work-v2 2>&1 | grep -v "^remote:" | tail -2 && break; sleep $((2**i)); done
r=$(git ls-remote "$REMOTE" refs/heads/transfer/tn-e001-work-v2 | cut -f1)
echo "files $n local $sha remote $r"
