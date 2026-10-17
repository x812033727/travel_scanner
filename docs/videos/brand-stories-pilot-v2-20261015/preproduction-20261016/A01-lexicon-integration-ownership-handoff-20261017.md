# A01 詞典綁定整合：認領與路徑核對（2026-10-17）

**狀態：唯讀交接，HOLD。** 這份紀錄沒有認領 `2026-10-16-bind-story-audits-and-narration-to`、改動 `tools/`、寫入正式機、啟動模型或媒體製作。

## 認領障礙

- 整合票 `tasks/open/2026-10-16-bind-story-audits-and-narration-to.md` 目前是 `open`、無 owner。它宣告 `tools/video/automation/story.mjs`、`flow.mjs`、`state.mjs`、TTS 和測試等路徑。
- `node .agents/skills/task-board/scripts/who-is-on-it.mjs --scope tools/video/automation/story.mjs` 回報另一張 `review` 票 `2026-10-14-support-10-minute-minimax-cute-brand`，owner `codex-8a78-story-route`。該票同時涵蓋 `story.mjs`、`story.test.mjs` 和 `flow.mjs`。它的 branch `codex/brand-stories-five-20261014` 對應 **已合併** PR #1499（merge commit `a1b6b1149c9086478e2d3954f5d19aab7eb5301a`）；票仍留在 `tasks/open/` 的 `review` 狀態。應由原 owner 按 task-board 規則核對並結案，不能把「已合併 PR」當成可擅自接管該票的證明。
- 另一個真正尚開的 **草稿** PR #1518（head `b8695951d8f3de44416c589848013747f95378e8`，`DIRTY`）也修改 `story.mjs`、`story.test.mjs`，處理 hash-pinned author chapters。整合前要與它的 owner 排序或協調；不能在它尚未收斂時平行改同檔。
- 草稿 PR #1528（head `1eeb5f48fa5ede9498dd23818788af88afb22691`，`BEHIND`）只加入 `tools/video/core/story-lexicon.mjs` 與測試。它定義版本／事件／current 指標的唯讀格式，尚無 writer、worker 或 TTS 綁定，也沒有 A01 歷史 80 筆稽核事件的過渡。它不是已可上線的修復。

## 必須同時接通的程式路徑

- 兩個共用字典寫入點：`story.mjs` 的 `addTerms()` 約第 671 行；`flow.mjs` 的 `mergeLexicon()` 約第 421 行。每支影片的 lease 無法排除別支影片寫同一個 `docs/videos/lexicon.json`。兩條寫入路徑都需要同一個跨影片 writer admission；只改 A01 路線仍會再漂移。
- 故事撰稿與聽稿直接讀共用詞典：`story.mjs` 的 `draftContext()`、`writerPayload()`、`listenChapter()` 約第 795、1104、1348 行。一般 flow 另在約第 2857、3411、3617 行讀取。
- `core/state.mjs` 的 `loadProject()` 約第 193–218 行把共用詞典放進 `project.lexicon`，接著 `speechHash()` 綁定旁白與後續狀態。`tts/cli.mjs` 的 TTS 使用它；`tts/check.mjs` 約第 276 行又自行重讀共用檔。因此單改來源稽核或單改 TTS 都不足以保證語音、審查與重啟後的 hash 一致。
- 正式機的 `video_docs` 與 `video_work` 是分開的 volume。不可假設跨兩個 volume 的字典版本、A01 稽核追加和 work 收據可由單一 rename 原子完成；需要 durable intent、讀回和崩潰後 fail-closed 恢復規則。

## 建議順序

1. 先由 #1499／舊 `review` 票 owner 核對結案，與 #1518 owner 排定 `story.mjs` 整合；將 #1528 的純格式 reader 重整到當時 main 並獨立審查，再認領整合票。不要用 `--force` 蓋掉活躍 scope。
2. 做單一跨影片 writer admission，讓 `story.addTerms()` 和 `flow.mergeLexicon()` 都走它；鎖住期間確認字典的原始 bytes/hash，避免讀—改—寫競態。
3. 以不可變 per-story version/event/current 實作明確提交與恢復狀態。對舊故事維持唯讀相容；對已開始的 A01，必須以**新的正式機擷取**先核對原 80 筆、`ebfa590a…` 舊詞典和當前實際詞典（2026-10-17 擷取為 `e6403c82…`），再由獨立審查的 append-only 過渡綁定，不能默默把當前 shared 檔複製為已核准版本。
4. 讓 story writer/listener/lint、`loadProject()`/speech hash、TTS 與 check-audio 讀同一份釘選版本；缺檔、hash 不符、未完成的雙 volume intent 都要阻斷付費呼叫。真正修改 A01 詞典時，記錄前後 hash 並令相依審查失效。
5. 用併發寫入、重啟／部分提交、舊 80-link 稽核、無快照新故事及獨立審稿夾具驗證，再做 release 規劃和正式機前檢；本交接沒有授權任何 A01 寫入或付費續跑。

核對命令：`npm run tasks -- list`；`node .agents/skills/task-board/scripts/who-is-on-it.mjs --scope tools/video/automation/story.mjs`；`gh pr view 1499 --json state,headRefName,mergedAt,mergeCommit,files`；`gh pr view 1518 --json state,isDraft,headRefOid,mergeStateStatus,files`；`gh pr view 1528 --json state,isDraft,headRefOid,mergeStateStatus,files`；`git ls-remote origin refs/heads/main`。這些是 2026-10-17 的唯讀觀測，執行前須重查。
