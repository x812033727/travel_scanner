# Worktree：介面與報表分開交付

本課 start 尚無新提示或 --compact；reference 是作者完整實作，不是工作樹或模型執行紀錄。從 start 複製全部檔案到全新的 practice-worktree，開終端機在其根目錄操作。下列 ../ 路徑必須尚不存在；若已有練習請換新名稱，不覆寫。不要在正式 repository 照做。

```text
git init -b main
git config user.name Practice
git config user.email practice@example.test
git add .
git commit -m "practice baseline"
git worktree add ../practice-ui -b codex/filter-hint
git worktree add ../practice-report -b codex/report-compact
git worktree list
git -C ../practice-ui status --short
git -C ../practice-report status --short
```

在原 practice-worktree 的 style.css 手動加 /* KEEP-MY-NOTE */，保持未提交。兩個工作樹的 style.css 不應有此字，原檔仍有；先用 Get-Location/pwd、git branch --show-current、git status --short 核對自己在哪一份。

路線 A 的 Codex 任務：只改 index.html，在搜尋與狀態工具列下方加入可見文字「搜尋會與目前狀態篩選一起套用。」。作者使用 p#filter-hint。維持既有 label、搜尋接線、窄螢幕與資料行為。用真正 HTTP 畫面核對文字及390px；Node測試不證明文字可見。

路線 B 的 Codex 任務：只改 report.mjs，並新增 tests/report-compact.test.mjs。加入無值的 --compact 旗標；stdout 及 --out 都是單行 JSON，加一個尾端 LF。沒有此旗標時維持原兩空格 pretty JSON。固定資料仍 total5/completedInWeek2/pending1/unknownCompleted1；來源不變，既有輸出仍拒絕覆寫。新測試先證明 compact 未實作，再驗預設與 compact 等值、行數、來源保留、重複旗標拒絕。

各路完成後在自己的資料夾跑 node --test，再只暫存授權檔案。以下仍從主 practice-worktree 執行：

```text
git -C ../practice-ui diff
git -C ../practice-ui add index.html
git -C ../practice-ui diff --cached --name-only
git -C ../practice-ui commit -m "add filter explanation"
git -C ../practice-report diff
git -C ../practice-report add report.mjs tests/report-compact.test.mjs
git -C ../practice-report diff --cached --name-only
git -C ../practice-report commit -m "add compact weekly report"
git cherry-pick codex/filter-hint
git cherry-pick codex/report-compact
git diff --name-only
git show --stat HEAD
node --test
node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11
node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11 --compact
```

成功條件：A commit 只有 index.html；B commit 只有 report.mjs 及新測試；main 有可見提示與兩種格式，數字相同，未提交的 style.css 註記仍在原工作樹。以 HTTP 真正檢查整合頁面；未跑記 NOT RUN。把整合 commit hashes 與原文輸出另記，不把作者 reference 當這次代理結果。

挑戰：從完成主任務的 main 建兩個新分支，故意改相同的 p#filter-hint 文字：

```text
git worktree add ../practice-conflict-a -b codex/conflict-a
git worktree add ../practice-conflict-b -b codex/conflict-b
```

A 改為「搜尋會與目前狀態篩選一起套用；首尾空白會被忽略。」；B 改為「搜尋會與目前狀態篩選一起套用；搜尋不會刪除任務。」。兩路各只 git add index.html，提交後：

```text
git -C ../practice-conflict-a add index.html
git -C ../practice-conflict-a commit -m "explain trimmed search"
git -C ../practice-conflict-b add index.html
git -C ../practice-conflict-b commit -m "explain retained tasks"
git cherry-pick codex/conflict-a
git cherry-pick codex/conflict-b
git status --short
```

第二次應停止於 index.html 內容衝突，這是預期失敗。先保存輸出，再讀雙方需求，把衝突標記改成一句保留兩項意思的提示：「搜尋會與目前狀態篩選一起套用；首尾空白會被忽略，搜尋不會刪除任務。」。只 git add index.html，再 git cherry-pick --continue。重新 node --test、兩格式與HTTP驗收；style.css 註記仍不提交。若決定停止未完成的這次挑選，用 git cherry-pick --abort；不要 reset --hard。

還原：若只完成主任務且尚未做文案挑戰，可在主練習庫 git revert --no-edit codex/report-compact，再 git revert --no-edit codex/filter-hint；核對逆向提交與原 CSS 註記保留。若有後續文案改動，先讀歷史及 diff 再選回復範圍，或保留整份成果、從本包 start 複製全新副本。

清理：先 git worktree list 核對絕對路徑，保存成果並確認各支工作樹 git status --short 是空。只對本課明確路徑執行 git worktree remove ../practice-ui、../practice-report、../practice-conflict-a、../practice-conflict-b；沒有做挑戰就不執行其兩條。原 main 的註記保留。是否刪分支依成果是否仍需要決定。
