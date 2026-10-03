# 長片時長審查收據（duration receipt）

`docs/videos/long-form/review.json` 用 SHA-256 綁住約 108 個檔（清單是 `tools/video/long-form/review.mjs` 的 `REVIEW_FILES`），
`review.md` 是它的報告、`report_sha256` 綁報告本身。綁住的檔一改，`node tools/video/long-form/cli.mjs check` 與
`tools/video/long-form/review.test.mjs` 就紅：CI 的 `web`（`test:tools`）和 Video tooling 的 `smoke` 兩個 job 都會帶著它。
規則在 `review.mjs` 的 `durationReviewProblems`：**作者不能自己重綁**，`reviewer_agent` 必須不同於 `author_agent`。

## 什麼時候會碰到

- 改到任何綁住的檔：`apps/api/app/video_automation/{models,settings,schemas,series}.py`、`tools/video/automation/{flow,prompts,series}.mjs`、
  `tools/video/core/{drama,lint,schema}.mjs`、`automation.test.mjs`、`tts.test.mjs`、`admin-video-reviews.test.tsx`、
  `docs/videos/README.md`、`DESIGN.md`、`.agents/skills/youtube-video/SKILL.md`（連 `.claude` 複本）……完整清單只看 `REVIEW_FILES`。
  改之前先 `grep -n "<路徑>" tools/video/long-form/review.mjs`，知道自己會不會踩到。
- **把 main 併進分支**：main 和分支都動過 `review.md`／`review.json`（每個碰到綁住檔的 PR 都會），兩個檔一定衝突；
  就算沒衝突（main 只改了綁住的檔、沒補收據），合併後的樹也會有一條 stale 綁定。
- **PR 的 CI 跑的是「head 併 main」的結果**：main 上有人改了綁住的檔卻沒補收據（2026-10-03 的 #1169），
  你的 PR 會紅在 `smoke`／`web` 的 `review.test.mjs`，錯誤訊息點名的檔不是你改的。先 `git fetch` 看 main 是不是已經壞了，
  再決定是把 main 併進來一起補，還是等補 main 的 PR（10-03 是 #1170）先合。

## 怎麼補（增量）

1. 作者把程式改完、提交。**不要**自己動 `review.md`／`review.json`。
2. 另開一個**獨立審查代理**，身分像 `claude-pr-review-<PR 號>`；還沒有 PR 號就用分支名（`claude-pr-review-<分支短名>`，review.md 的「Branch illustration-polish increment」就是這樣），段落標題寫 `## Branch <名字> increment: <k> files (<日期>)`。規則只要求 `reviewer_agent` 非空且不等於 `author_agent`。給它：綁住的檔的 diff 範圍
   （`git diff <merge-base>..HEAD` 交集 `REVIEW_FILES`）、要寫的段落標題格式、要用的 commit 訊息。它只能改那兩個收據檔、不推。
3. 它要做的事：讀 `review.mjs` 與 `review.test.mjs` 知道規則；先做 Baseline：對每個要重綁的檔，`git show <merge-base>:<路徑> | sha256sum`
   要等於 `review.json` 現綁的值（不等＝merge-base 那一側已有沒補的綁定，先照上面「把 main 併進分支」處理，否則這次 diff 不是全部沒審過的改動），
   段落的 Baseline 那一行就寫這件事（merge-base 的 SHA、幾個檔對上）；再逐檔讀 diff，確認**沒有改到時長規則**
   （600／780 秒目標、480 秒實測下限、8 分鐘下限、`target_minutes`、`MIN_EPISODE`、`VIDEO_MIN_EPISODE_MINUTES`、
   `runtime_spec`、`action_seconds`、來源雜湊、covered 狀態）；在 `review.md` 的 `## Reviewed SHA256 bindings` 之前加一節
   `## PR #<n> <名字> increment: <k> files (<日期>)`（照前幾節的格式：Reviewer／Author／Scope／Baseline／Findings／Ran／Non-claims／Verdict），
   更新表格裡那幾列；`review.json` 改 `checked_on`、`author_agent`、`reviewer_agent`、那幾個雜湊（每個是工作樹檔案 bytes 的 SHA-256，
   和 `review.mjs` 的 `readFileSync` 一樣：`sha256sum <路徑>`，Git Bash 與 Linux 都有；不是 `git hash-object`，`cli.mjs check` 也只印路徑不印值；
   `.gitattributes` 釘 LF，所以 Windows 上的 bytes 等於 repo 的），表格那幾列填同一個值，最後算 `report_sha256`
   （`sha256sum docs/videos/long-form/review.md`；`review.md` 要 LF、無 BOM、結尾換行不要動）；跑 `cli.mjs check` 要 `PASS`、`review.test.mjs` 要綠；只提交兩個收據檔。
4. 併 main 之後再來一次，段落叫 `## PR #<n> merge with #<m> follow-up`：兩邊的段落都留、表格列取合併後樹的雜湊
   （兩邊都改同一檔時，合併後的檔要等於哪一邊就綁那一邊；像 #1168 把測試檔改回 main 的版本，再綁 main 的雜湊）。
5. 一支分支多次增量很正常（#1168 做了四次：原始改動、併 main、修測試、再併 main）。每次都重跑 `cli.mjs check`。

同一個審查代理可以用 `SendMessage` 續用（它記得規則與格式），比每次重開省很多；它的回報要含跑過的指令與結果、commit 雜湊。
Workflow 版（提案／反駁）也行，但收據增量是循序的一件事，一個代理就夠。

## 開 PR 前後

- 推之前本機 `node tools/video/long-form/cli.mjs check`；紅就照上面補，不要推一個會在 CI 才紅的分支。
- 開收據 follow-up 之前先看開著的 PR：別人可能已經在他的分支綁了同一個檔（10-03 #1169 的綁定是 #1168 順帶補的、#1170 也補了），
  兩個都合就是下一個衝突。
- 收據衝突不是程式衝突：`git merge` 把兩邊段落都留、雜湊取合併後的檔、重算 `report_sha256`。永遠由審查代理做，作者只負責把樹準備好。

## 來源

2026-10-02 起的做法（#1105、#1107、#1108、#1112 的段落格式）；10-03 的 #1168 走了四次增量、#1169 漏補讓 main 紅、#1170 代補。
