# 保留中的 AI 寫程式內容：批次 04、Claude Code 教學中心（#485）、Claude Code 深入教學（#501）

- 對應票：`tasks/open/2026-09-15-publish-held-ai-coding-content.md`
- 本文件狀態：**2026-09-19 準備完成（claude-fable-5-1）**。不需要正式站權限的部分都做完了：三批 slug 清單、本機檢查、正式站現況、站內連結重算、主機指令。
  剩下的是站主的兩個決定（第 1 節）與主機上的執行（第 7 節），執行結果請回填第 8 節。
- 沒有修改任何內容包；三批的內容以目前 `main`（本分支同步到 `3f5c8ad6`，#556）的 `apps/api/app/guides/content/` 為準。

## 1. 站主要做的兩個決定（請直接勾選並簽日期）

### 決定一：接受 #501 的 36 篇照文章目前寫明的限制發布

相依票 `2026-09-14-claude-advanced-live-validation` 仍然 `open`，20 項裡還有 4 項沒完成：

- 第 81 篇（`claude-code-mcp-http-auth-workshop`）：沒有真實的遠端 MCP HTTP／OAuth 測試服務，授權、撤銷與恢復沒有實機做過。
- 第 90 篇（`claude-code-cross-device-recovery-workshop`）：沒有在真實手機與電腦之間做接續、斷線、休眠與恢復。
- 第 92 篇（`claude-code-github-actions-review-workshop`）：GitHub Actions 只跑過 `run_model=false` 的 baseline，付費模型 job 與 review artifact 沒有跑（需要 `ANTHROPIC_API_KEY`）。
- 發布前重查高變動功能與來源日期：19 個官方來源的核對日期是 2026-09-14。

文章本身已寫明哪些是「依官方文件核對、未由作者實機操作」（見 `docs/claude-code-series/advanced/README.md` 的「驗證狀態」與 `source-review.md`）。
#501 與 #485 互相大量連結（#485→#501 12 條、#501→#485 85 條），批次 04 又連到 #485，所以 **不接受決定一就整批 111 篇都不能發**。

- [x] 接受：照目前寫明的限制發布 36 篇；`2026-09-14-claude-advanced-live-validation` 繼續獨立進行，補完後再更新文章。（日期：2026-09-20　簽名：站主於 AskUserQuestion 選定，claude-fable-5-1 代填）
- [ ] 不接受：本票維持 open，等實測票完成。

### 決定二：`codex-cli-getting-started` 與 `codex-cloud-tasks-github` 怎麼處理

這兩篇屬於批次 04，但被 #525（`ecf6fbc5`，2026-09-15）改過：多了 en、ja、ko、zh-CN 四個語系，內文連進 Codex 學習中心。
學習中心的票 `2026-09-14-codex-learning-series` 現在是 `blocked`，那 58 篇都還沒發布（正式站 sitemap 只有 `codex-beginner-guide` 一篇 codex 文章）。
兩篇 zh-TW 內文指向、而且現在沒上線的目標：

- `codex-cli-getting-started` → `codex-account-usage`、`codex-agents-md`、`codex-cli-linux-wsl`、`codex-cli-macos`、`codex-cli-windows`、`codex-commands`、`codex-learning-hub`、`codex-permissions`、`codex-sessions-resume`、`codex-terminal-paths`（另有 `ai-term-token`，已上線）。
- `codex-cloud-tasks-github` → `codex-first-project`、`codex-learning-hub`、`codex-mobile-guide`、`codex-testing-review`。

三個選項的實際影響：

| 選項 | 做法 | 影響 |
|---|---|---|
| (a) 等 Codex 學習中心一起發 | 從 slug 清單拿掉兩篇，這次發 **109 篇** | 批次 04 有 4 篇（`ai-coding-agents-compared`, `ai-coding-git-basics`, `ai-coding-prompt-patterns`, `ai-coding-tools-overview-2026`）內文引用 `codex-cli-getting-started`，加上已上線的 `codex-beginner-guide` 引用這兩篇，這些 article 行內引用在目標未發布時只顯示純文字（不是壞連結）；學習中心發布時再一起匯入即可 |
| (b) 只發 zh-TW，暫時接受連進學習中心的引用還不能點 | 兩篇留在清單，指令本來就帶 `--locale zh-TW`，所以只會建立 zh-TW；四個外語版本留到學習中心發布時再匯入（屆時會是 `create`） | 兩篇裡指向學習中心的 article 引用顯示為純文字；`guides-links-check --locale zh-TW` 會把它們列成 `unpublished`（票面 DoD 允許的唯一例外，第 8.7 節要記下來） |
| (c) 先拿掉兩篇連進學習中心的引用再發 | 要改兩個內容包（不在本票 scope；而且這兩個檔案也在 blocked 票 `2026-09-14-codex-learning-series` 的 scope 裡，另開票時 claim 會被 overlap 擋，需要 `--force` 並在票裡說明）、合併、**重新部署映像**，然後才能匯入 | 最慢；學習中心發布時還要再把引用加回去 |

- [ ] (a)　- [x] (b)　- [ ] (c)　（日期：2026-09-20　簽名：站主於 AskUserQuestion 選定，claude-fable-5-1 代填）

## 2. 正式站現況（2026-09-19 06:47–06:50 UTC 實測）

共 9 個請求，User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，間隔 1.5 秒，未登入，沒有送任何個人資料。

### 2.1 三批一篇都還沒上線

- `https://mokaair.com/sitemap.xml` 是 sitemap index，11 個子檔：`static`、`travel-{en,ja,ko,zh-TW,zh-CN}`、`life-{en,ja,ko,zh-TW,zh-CN}`；沒有編號的第二片。
- `sitemaps/sitemap/life-zh-TW.xml`：737 個 URL ＝ 705 篇文章 ＋ 32 個主題頁；最新 `lastmod` 2026-09-19T03:35Z（當天上午發布的多模型 AI 工作流系列）。**111 個 slug 沒有一個在裡面。**
- `sitemaps/sitemap/life-en.xml`：90 篇，沒有任何 `codex-*`（學習中心在外語版也沒發）。
- 抽查三頁（各批一篇）都還是保留狀態：

| 頁面 | HTTP | robots | `<title>` / h1 | canonical |
|---|---|---|---|---|
| `/zh-TW/life/ai-coding-cost-tokens-explained`（批次 04） | 200 | `<meta name="robots" content="noindex"/>` | 這篇文章目前看不到 | 指向自己 |
| `/zh-TW/life/claude-code-project-rules-workshop`（#501） | 200 | 同上 | 同上 | 同上 |
| `/zh-TW/life/codex-cli-getting-started`（批次 04／Codex） | 200 | 同上 | 同上 | 同上 |

- 兩張 hero 已經回 200：`/guides/ai-coding-cost-tokens-explained/hero.jpg`（50,756 bytes）、`/guides/claude-code-project-rules-workshop/hero.jpg`（54,146 bytes）。
  表示目前部署的 web 映像已經含這三批的素材；111 篇的 hero 都是 `/guides/<slug>/hero.jpg`。

判讀時注意：每一頁的 HTML 都內嵌 `這篇文章目前看不到` 這個字串（`guides.unavailableTitle`，發布與否都在），所以 grep 這句話證明不了什麼；
要看 `<title>`、h1 與 `<meta name="robots">`。

### 2.2 sitemap 列數：票面「925 → 1,036」已過時

`GET https://mokaair.com/api/travel/guides/sitemap/summary`（BFF 轉到 `GET /api/v1/guides/sitemap/summary`）現在的已發布 (kind, locale) 列數：

| kind | zh-TW | en | ja | ko | zh-CN | 小計 |
|---|---|---|---|---|---|---|
| intel | 19 | 2 | 2 | 2 | 2 | 27 |
| howto | 106 | 18 | 18 | 18 | 18 | 178 |
| life | 705 | 90 | 90 | 90 | 90 | 1065 |
| **合計** | | | | | | **1,270** |

- 票面的 925 是 2026-09-15 單一 sitemap 時代的數字；之後 sitemap 已拆成 index（`2026-09-14-sitemap-split-before-1000-rows`，done），子檔上限 5,000（`SITEMAP_CHILD_LIMIT`，`apps/web/lib/guides.server.ts`），超過會自動出現 `life-zh-TW-2`。**1,000 列的上限已經不存在。**
- 這次發布 111 篇全是 zh-TW：合計 1,270 → **1,381**，`life-zh-TW` 子檔 705 → **816** 篇（加 32 個主題頁共 848 個 URL）。選項 (a) 是 109 篇：1,379／814 篇。離 5,000 還很遠。

### 2.3 主機映像應已包含目前的內容包（仍要在主機核對）

- 三批合併後，內容包又被改過三次：#513（`c23c87a3`，`ai-build-line-bot-tutorial`、`ai-coding-tools-overview-2026`、`vibe-coding-first-website` 的 description）、#525（`ecf6fbc5`，兩篇 Codex）、#531（`88cfde04`，2026-09-16，**111 篇全部**：完整網址改成 article 行內引用、主題、摘要工具等）。
- 最近一次正式部署 `deploy_20260919_032927`（#553，`a69763b5`；見 `tasks/done/2026-09-18-ai-workflow-tutorial-series-12-zh.md`）在這三次之後；#554–#556 沒有動任何內容包或 `apps/web/public/guides/`。
- 所以這次**不需要為了發布再部署**，但第 7.0 節要用 sha256 核對容器裡的 111 個檔案就是本分支這一版。
- 本分支的 git 是 shallow clone（54 個 commit），看不到 #485／#501／#499／#502 原始 commit；slug 清單改由下列檔案交叉比對得出，與 `docs/claude-code-series/evidence/content-validation.json`（61 頁）、`advanced/evidence/content-validation.json`（97 頁）一致。

## 3. 三批 slug 清單（111 篇，全部有內容包）

來源與扣除方式：

- 批次 04：`docs/life-ai-series.md`「批次 04」表 20 篇，扣掉轉入 Claude Code 系列、網址沿用的 5 篇（`claude-code-getting-started`、`claude-code-claude-md-guide`、`claude-code-mcp-servers`、`claude-code-hooks-and-skills`、`claude-code-on-the-web`，它們算在 #485 的 61 篇裡），再扣掉 `gemini-cli-getting-started`（轉入 Gemini 系列，已上線）＝ 14 篇 ＝ 12 篇一般文章 ＋ 2 篇 Codex。
- #485：`apps/api/app/guides/series_data/claude-code.json` 的 `hub`（`claude-code-tutorials`）＋ entries 1–60 ＝ 61 篇。
- #501：同一檔 entries 61–96 ＝ 36 篇，與 `docs/claude-code-series/advanced/curriculum.json` 的 36 篇逐一相同。
- 檢查：111 個 slug 都有 `apps/api/app/guides/content/<slug>.json`，`kind` 都是 `life`；目錄裡 `claude-code-*.json` 恰好 97 個，沒有多餘、沒有缺少；除兩篇 Codex 外都只有 zh-TW。

### 3.1 批次 04（14）

| 總表 # | slug | 標題 | 內容包語系 | 備註 |
|---|---|---|---|---|
| 61 | `ai-coding-tools-overview-2026` | AI 寫程式工具總覽：Claude Code、Codex、Gemini CLI、Cursor、Copilot | zh-TW |  |
| 67 | `codex-cli-getting-started` | Codex CLI 安裝與入門 | en、ja、ko、zh-CN、zh-TW | #525 改過：多 en/ja/ko/zh-CN、連進 Codex 學習中心；本票只匯 zh-TW |
| 68 | `codex-cloud-tasks-github` | 雲端任務與 GitHub | en、ja、ko、zh-CN、zh-TW | #525 改過：多 en/ja/ko/zh-CN、連進 Codex 學習中心；本票只匯 zh-TW |
| 70 | `cursor-editor-guide` | Cursor 編輯器入門：Tab 補全、Chat 與代理模式 | zh-TW |  |
| 71 | `github-copilot-guide` | GitHub Copilot 入門：VS Code 裡的補全、Chat 與代理 | zh-TW |  |
| 72 | `vibe-coding-first-website` | Vibe coding：不會寫程式也能做出第一個網站 | zh-TW |  |
| 73 | `ai-coding-agents-compared` | AI 寫程式代理操作步驟比較：同一個需求在三個工具怎麼做 | zh-TW |  |
| 74 | `deploy-ai-built-site-to-vps` | 把 AI 幫你寫的網站放上網：VPS、網域與 HTTPS 一次搞定 | zh-TW |  |
| 75 | `ai-coding-git-basics` | 用 AI 寫程式前該懂的 Git：分支、提交與還原 | zh-TW |  |
| 76 | `ai-code-review-safety` | AI 寫的程式能信嗎：審查、測試與安全檢查清單 | zh-TW |  |
| 77 | `ai-coding-cost-tokens-explained` | AI 寫程式的費用怎麼算：token、訂閱與 API 額度 | zh-TW |  |
| 78 | `ai-coding-prompt-patterns` | 給程式代理的提示模式：先規劃、再實作、最後驗證 | zh-TW |  |
| 79 | `ai-build-line-bot-tutorial` | 用 AI 幫你做 LINE 機器人：從零到上線 | zh-TW |  |
| 80 | `ai-build-personal-blog-tutorial` | 用 AI 做個人部落格：靜態網站產生器與部署 | zh-TW |  |

### 3.2 Claude Code 教學中心 #485（61 ＝ 總目錄 ＋ 第 01–60 篇）

| # | slug | 標題 |
|---|---|---|
| 00 | `claude-code-tutorials` | Claude Code 完整教學目錄：從入門到自動化 |
| 01 | `claude-code-getting-started` | Claude Code 入門：認識工具與第一條學習路線 |
| 02 | `claude-code-accounts-and-access` | Claude Code｜帳號、登入與使用資格 |
| 03 | `claude-code-platforms-guide` | Claude Code｜桌面、CLI、網頁、手機怎麼選 |
| 04 | `claude-code-terminal-git-basics` | Claude Code｜終端機、路徑與 Git 基礎 |
| 05 | `claude-code-practice-project-setup` | Claude Code｜準備第一個練習專案 |
| 06 | `claude-code-task-prompts` | Claude Code｜如何把需求交代清楚 |
| 07 | `claude-code-install-windows` | Claude Code｜Windows CLI 安裝教學 |
| 08 | `claude-code-install-macos` | Claude Code｜macOS CLI 安裝教學 |
| 09 | `claude-code-install-linux-wsl` | Claude Code｜Linux 與 WSL 安裝教學 |
| 10 | `claude-code-desktop-setup` | Claude Code｜桌面版安裝與第一個任務 |
| 11 | `claude-code-desktop-workflow` | Claude Code｜桌面版日常工作流程 |
| 12 | `claude-code-ide-integration` | Claude Code｜VS Code 與 JetBrains 整合 |
| 13 | `claude-code-on-the-web` | Claude Code 網頁版教學 |
| 14 | `claude-code-mobile-ios` | Claude Code｜iPhone 與 iPad 使用教學 |
| 15 | `claude-code-mobile-android` | Claude Code｜Android 使用教學 |
| 16 | `claude-code-remote-control` | Claude Code｜Remote Control：接續電腦上的工作 |
| 17 | `claude-code-desktop-dispatch` | Claude Code｜Dispatch：從手機派送桌面任務 |
| 18 | `claude-code-cross-device-workflow` | Claude Code｜跨裝置接續工作的完整流程 |
| 19 | `claude-code-markdown-basics` | Claude Code｜Markdown 零基礎 |
| 20 | `claude-code-claude-md-guide` | Claude Code｜CLAUDE.md 完整教學 |
| 21 | `claude-code-claude-md-scopes` | Claude Code｜個人、專案與子目錄規則 |
| 22 | `claude-code-rules-and-imports` | Claude Code｜拆分規則與引用其他 MD |
| 23 | `claude-code-auto-memory` | Claude Code｜自動記憶與 /memory |
| 24 | `claude-code-settings-json` | Claude Code｜settings.json 設定教學 |
| 25 | `claude-code-cli-command-guide` | Claude Code｜CLI 指令入門與分類索引 |
| 26 | `claude-code-help-status-doctor` | Claude Code｜說明、狀態與診斷 |
| 27 | `claude-code-sessions-resume` | Claude Code｜繼續、找回與管理對話 |
| 28 | `claude-code-context-compact-clear` | Claude Code｜上下文整理：context、compact 與 clear |
| 29 | `claude-code-models-usage-config` | Claude Code｜模型、用量與偏好設定 |
| 30 | `claude-code-permissions-plan-mode` | Claude Code｜Plan Mode 與權限模式 |
| 31 | `claude-code-files-and-context` | Claude Code｜提供檔案與專案上下文 |
| 32 | `claude-code-understand-codebase` | Claude Code｜快速讀懂陌生專案 |
| 33 | `claude-code-implement-feature` | Claude Code｜新增一個小功能 |
| 34 | `claude-code-debug-and-test` | Claude Code｜除錯與補測試 |
| 35 | `claude-code-git-review-pr` | Claude Code｜Git、差異審查與 PR |
| 36 | `claude-code-checkpoints-rewind` | Claude Code｜Checkpoint 與 /rewind |
| 37 | `claude-code-hooks-and-skills` | Claude Code｜Hooks 與 Skills 怎麼選 |
| 38 | `claude-code-skills-skill-md` | Claude Code｜建立第一個 SKILL.md |
| 39 | `claude-code-skill-arguments-resources` | Claude Code｜Skill 參數與附屬材料 |
| 40 | `claude-code-custom-commands` | Claude Code｜自訂斜線指令與舊格式移轉 |
| 41 | `claude-code-hooks-getting-started` | Claude Code｜建立第一個 Hook |
| 42 | `claude-code-hooks-recipes` | Claude Code｜Hooks 實用案例 |
| 43 | `claude-code-mcp-servers` | Claude Code 接 MCP 入門 |
| 44 | `claude-code-mcp-setup-troubleshooting` | Claude Code｜MCP 安裝、設定與排錯 |
| 45 | `claude-code-plugins-guide` | Claude Code｜Plugins 安裝與管理 |
| 46 | `claude-code-subagents-guide` | Claude Code｜Subagents 與代理 MD 設定 |
| 47 | `claude-code-worktrees-parallel` | Claude Code｜Git Worktree 平行工作 |
| 48 | `claude-code-agent-teams` | Claude Code｜Agent Teams 協作 |
| 49 | `claude-code-chrome-browser` | Claude Code｜Chrome 瀏覽器整合 |
| 50 | `claude-code-computer-use` | Claude Code｜Computer Use 教學 |
| 51 | `claude-code-headless-json` | Claude Code｜非互動執行與 JSON 輸出 |
| 52 | `claude-code-scheduled-tasks` | Claude Code｜排程與重複任務 |
| 53 | `claude-code-github-actions` | Claude Code｜GitHub Actions 整合 |
| 54 | `claude-code-agent-sdk` | Claude Agent SDK 入門 |
| 55 | `claude-code-build-todo-app` | Claude Code｜完整實作：待辦清單網站 |
| 56 | `claude-code-maintain-existing-project` | Claude Code｜接手舊專案與逐步重構 |
| 57 | `claude-code-project-data-safety` | Claude Code｜專案資料與操作安全 |
| 58 | `claude-code-usage-cost-optimization` | Claude Code｜用量、成本與效率調整 |
| 59 | `claude-code-troubleshooting` | Claude Code｜常見問題排除大全 |
| 60 | `claude-code-templates-cheatsheet` | Claude Code｜指令速查與設定範本庫 |

### 3.3 Claude Code 深入教學 #501（36 ＝ 第 61–96 篇）

| # | slug | 標題 |
|---|---|---|
| 61 | `claude-code-project-rules-workshop` | Claude Code｜替真實專案設計 CLAUDE.md |
| 62 | `claude-code-monorepo-rules-workshop` | Claude Code｜Monorepo 的分層 MD 與路徑規則 |
| 63 | `claude-code-rules-loading-diagnostics` | Claude 沒照 MD 做：找出載入與規則衝突 |
| 64 | `claude-code-permissions-sandbox-lab` | Claude Code｜權限與 Sandbox 邊界實驗 |
| 65 | `claude-code-context-handoff-workshop` | Claude Code｜長任務的上下文整理與交接文件 |
| 66 | `claude-code-team-config-maintenance` | Claude Code｜把個人設定整理成團隊可維護的設定包 |
| 67 | `claude-code-skill-sop-workshop` | Claude Code｜把一套工作 SOP 做成可重用 Skill |
| 68 | `claude-code-skill-input-validation` | Claude Code｜Skill 參數驗證：缺值、錯誤與危險字元 |
| 69 | `claude-code-skill-resource-design` | Claude Code｜拆分大型 Skill 的範本、參考文件與腳本 |
| 70 | `claude-code-skill-invocation-control` | Claude Code｜Skill 何時啟動：手動呼叫與自動選用 |
| 71 | `claude-code-skill-regression-testing` | Claude Code｜替 Skills 建立回歸案例與評分表 |
| 72 | `claude-code-plugin-team-distribution` | Claude Code｜把 Skills 與 Hooks 包成可版本管理的 Plugin |
| 73 | `claude-code-hook-event-test-lab` | Claude Code｜讀懂 Hook 事件：輸入、輸出與退出碼 |
| 74 | `claude-code-hook-scoped-formatting` | Claude Code｜只處理變更檔案的格式化 Hook |
| 75 | `claude-code-hook-quality-gates` | Claude Code｜建立可停止的品質檢查 Hook |
| 76 | `claude-code-hook-file-boundaries` | Claude Code｜用 Hook 保護指定檔案並測試路徑邊界 |
| 77 | `claude-code-hook-notifications-audit` | Claude Code｜任務通知與事件紀錄：有用而不洗版 |
| 78 | `claude-code-hook-portability-recovery` | Claude Code｜跨平台 Hooks：中文路徑、逾時與遞迴排錯 |
| 79 | `claude-code-mcp-local-server-workshop` | Claude Code｜建立自己的唯讀 MCP 工具 |
| 80 | `claude-code-mcp-tool-contracts` | Claude Code｜設計 MCP 工具名稱、輸入 Schema 與分頁 |
| 81 | `claude-code-mcp-http-auth-workshop` | Claude Code｜遠端 MCP 登入、授權範圍與重新認證 |
| 82 | `claude-code-mcp-failure-contract-tests` | Claude Code｜MCP 排錯實驗室：斷線、逾時與格式錯誤 |
| 83 | `claude-code-mcp-untrusted-output` | Claude Code｜MCP 回傳含有指令時：資料與操作權限分開 |
| 84 | `claude-code-issue-to-draft-pr-workshop` | Claude Code｜從 Issue 到變更草稿：串起工具與程式碼 |
| 85 | `claude-code-tdd-debugging-workshop` | Claude Code｜真正走完一次重現、失敗測試與修正 |
| 86 | `claude-code-legacy-refactoring-workshop` | Claude Code｜接手缺測試舊專案：先留住行為再重構 |
| 87 | `claude-code-subagent-review-workshop` | Claude Code｜讓 Subagent 提出可核對的審查發現 |
| 88 | `claude-code-worktree-integration-workshop` | Claude Code｜雙 Worktree 實作與衝突整合 |
| 89 | `claude-code-agent-teams-integration-lab` | Claude Code｜Agent Teams 的分工、阻塞與成果整合 |
| 90 | `claude-code-cross-device-recovery-workshop` | Claude Code｜桌面到手機：離線、中斷與返回工作現場 |
| 91 | `claude-code-structured-cli-pipeline` | Claude Code｜把 claude -p 接進有驗證的 JSON 流程 |
| 92 | `claude-code-github-actions-review-workshop` | Claude Code｜CI 審查助手：權限、fork 與結果附件 |
| 93 | `claude-code-scheduled-workflow-reliability` | Claude Code｜排程失敗怎麼辦：重複執行、漏跑與停止 |
| 94 | `claude-code-agent-sdk-stateful-runner` | Claude Code｜Agent SDK：保存狀態、取消與重新接續 |
| 95 | `claude-code-workflow-evaluation-cost` | Claude Code｜比較流程品質、用量與執行時間 |
| 96 | `claude-code-advanced-capstone` | Claude Code｜期末實作：可維護的待辦專案工作流程 |

### 3.4 可直接貼的 `--slug` 參數（每批一段，每行 4 個，行尾反斜線接續）

`guides-import` 的 `--slug` 是 `action="append"`，一個 slug 一個 `--slug`；111 個合計約 4.2 KB，一條指令放得下。建議還是用第 7.1 節的 slug 檔組參數，比較不會漏。

批次 04（14）：

```text
  --slug ai-coding-tools-overview-2026 --slug codex-cli-getting-started --slug codex-cloud-tasks-github --slug cursor-editor-guide \
  --slug github-copilot-guide --slug vibe-coding-first-website --slug ai-coding-agents-compared --slug deploy-ai-built-site-to-vps \
  --slug ai-coding-git-basics --slug ai-code-review-safety --slug ai-coding-cost-tokens-explained --slug ai-coding-prompt-patterns \
  --slug ai-build-line-bot-tutorial --slug ai-build-personal-blog-tutorial \
```

#485（61）：

```text
  --slug claude-code-tutorials --slug claude-code-getting-started --slug claude-code-accounts-and-access --slug claude-code-platforms-guide \
  --slug claude-code-terminal-git-basics --slug claude-code-practice-project-setup --slug claude-code-task-prompts --slug claude-code-install-windows \
  --slug claude-code-install-macos --slug claude-code-install-linux-wsl --slug claude-code-desktop-setup --slug claude-code-desktop-workflow \
  --slug claude-code-ide-integration --slug claude-code-on-the-web --slug claude-code-mobile-ios --slug claude-code-mobile-android \
  --slug claude-code-remote-control --slug claude-code-desktop-dispatch --slug claude-code-cross-device-workflow --slug claude-code-markdown-basics \
  --slug claude-code-claude-md-guide --slug claude-code-claude-md-scopes --slug claude-code-rules-and-imports --slug claude-code-auto-memory \
  --slug claude-code-settings-json --slug claude-code-cli-command-guide --slug claude-code-help-status-doctor --slug claude-code-sessions-resume \
  --slug claude-code-context-compact-clear --slug claude-code-models-usage-config --slug claude-code-permissions-plan-mode --slug claude-code-files-and-context \
  --slug claude-code-understand-codebase --slug claude-code-implement-feature --slug claude-code-debug-and-test --slug claude-code-git-review-pr \
  --slug claude-code-checkpoints-rewind --slug claude-code-hooks-and-skills --slug claude-code-skills-skill-md --slug claude-code-skill-arguments-resources \
  --slug claude-code-custom-commands --slug claude-code-hooks-getting-started --slug claude-code-hooks-recipes --slug claude-code-mcp-servers \
  --slug claude-code-mcp-setup-troubleshooting --slug claude-code-plugins-guide --slug claude-code-subagents-guide --slug claude-code-worktrees-parallel \
  --slug claude-code-agent-teams --slug claude-code-chrome-browser --slug claude-code-computer-use --slug claude-code-headless-json \
  --slug claude-code-scheduled-tasks --slug claude-code-github-actions --slug claude-code-agent-sdk --slug claude-code-build-todo-app \
  --slug claude-code-maintain-existing-project --slug claude-code-project-data-safety --slug claude-code-usage-cost-optimization --slug claude-code-troubleshooting \
  --slug claude-code-templates-cheatsheet \
```

#501（36）：

```text
  --slug claude-code-project-rules-workshop --slug claude-code-monorepo-rules-workshop --slug claude-code-rules-loading-diagnostics --slug claude-code-permissions-sandbox-lab \
  --slug claude-code-context-handoff-workshop --slug claude-code-team-config-maintenance --slug claude-code-skill-sop-workshop --slug claude-code-skill-input-validation \
  --slug claude-code-skill-resource-design --slug claude-code-skill-invocation-control --slug claude-code-skill-regression-testing --slug claude-code-plugin-team-distribution \
  --slug claude-code-hook-event-test-lab --slug claude-code-hook-scoped-formatting --slug claude-code-hook-quality-gates --slug claude-code-hook-file-boundaries \
  --slug claude-code-hook-notifications-audit --slug claude-code-hook-portability-recovery --slug claude-code-mcp-local-server-workshop --slug claude-code-mcp-tool-contracts \
  --slug claude-code-mcp-http-auth-workshop --slug claude-code-mcp-failure-contract-tests --slug claude-code-mcp-untrusted-output --slug claude-code-issue-to-draft-pr-workshop \
  --slug claude-code-tdd-debugging-workshop --slug claude-code-legacy-refactoring-workshop --slug claude-code-subagent-review-workshop --slug claude-code-worktree-integration-workshop \
  --slug claude-code-agent-teams-integration-lab --slug claude-code-cross-device-recovery-workshop --slug claude-code-structured-cli-pipeline --slug claude-code-github-actions-review-workshop \
  --slug claude-code-scheduled-workflow-reliability --slug claude-code-agent-sdk-stateful-runner --slug claude-code-workflow-evaluation-cost --slug claude-code-advanced-capstone \
```

## 4. 本機檢查（不需要資料庫，2026-09-19）

| 檢查 | 指令 | 結果 |
|---|---|---|
| 編輯規則 lint，只看 111 篇 | `cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --slug … ×111` | `111 entries checked`，**0 error**，exit 0；121 個 warning：`no_summary` 119（每篇一個，兩篇 Codex 五個語系各一個）、`text_length` 2（`claude-code-tutorials`、`claude-code-templates-cheatsheet`，兩篇本來就是縮短的目錄與速查表） |
| 整個 life 專區 | `uv run python -m app.guides.pack_cli lint --kind life` | `911 entries checked`，0 error |
| 全部內容包 | `uv run python -m app.guides.pack_cli lint` | `1056 entries checked`，35 個 error 全在 5 個旅遊包（`japan-autumn-leaves-2026`、`korea-winter-events-2026`、`kyoto-bus-subway-guide`、`tokyo-transit-passes`、`usj-guide`），不在本票範圍 |
| 內容包測試 | `uv run pytest tests/test_guides_content_pack.py -q` | **9 passed, 5 skipped**（跳過的是 PostgreSQL leg），含 `test_the_packaged_content_validates_and_its_images_exist` 與 `test_the_packaged_life_content_passes_lint` |

`no_summary` 是警告不是錯誤（`--warnings` 才會讓 exit 變 1）；補摘要屬於內容修改，不在本票 scope，發布後可另開票用 `pack_cli summarize` 處理。

## 5. 站內連結重算（repo 內容包 × 正式站 sitemap）

方法：走訪全部 1,056 個內容包每個語系文件的整個 JSON 結構（不是正規表示式比對整份檔案），收集 `{"type": "article", …}` 行內引用，以及任何字串裡的完整站內網址（`https://mokaair.com/<locale>/life/<slug>`、`/guides/<kind>/<slug>`）；再用 2.1 節的 `life-zh-TW.xml` 判斷來源頁有沒有上線。腳本與原始結果在本次工作階段的 scratchpad，不進 repo。

- 指向 111 個 slug 的引用共 690 個，**全部是 article 行內引用，沒有任何完整網址**（#531 已把完整網址轉成行內引用）。
- **已上線的 zh-TW 頁面指向保留中文章：29 條、21 篇來源**；扣掉票面排除的 `codex-beginner-guide`（2 條）是 **27 條、20 篇**，比票面的 25 條多 2 條：
  - `ai-tools-choose-by-task` → `ai-coding-tools-overview-2026`
  - `ai-workflow-coding-agents-division` → `claude-code-headless-json`（#553 的多模型 AI 工作流系列，2026-09-19 上午發布）

| 批 | 保留中的目標 | 已上線的來源（zh-TW） | 條數 |
|---|---|---|---|
| 批次 04 | `ai-build-line-bot-tutorial` | `ai-customer-service-line-bot`, `line-ai-features-taiwan`, `n8n-ai-automation-guide` | 3 |
| 批次 04 | `ai-code-review-safety` | `ai-at-work-policy-checklist` | 1 |
| 批次 04 | `ai-coding-cost-tokens-explained` | `ai-api-pricing-comparison-2026`, `ai-token-cost-estimation`, `local-vs-cloud-ai-cost`, `ollama-with-code-editors`, `openrouter-multi-model-api` | 5 |
| 批次 04 | `ai-coding-tools-overview-2026` | `ai-benchmarks-explained`, `ai-tools-choose-by-task`, `ollama-with-code-editors` | 3 |
| 批次 04 | `codex-cli-getting-started` | `codex-beginner-guide` | 1 |
| 批次 04 | `codex-cloud-tasks-github` | `codex-beginner-guide` | 1 |
| 批次 04 | `cursor-editor-guide` | `ollama-with-code-editors` | 1 |
| 批次 04 | `deploy-ai-built-site-to-vps` | `self-host-ai-on-vps` | 1 |
| 批次 04 | `github-copilot-guide` | `microsoft-copilot-windows-office`, `ollama-with-code-editors` | 2 |
| #485 | `claude-code-agent-sdk` | `ai-agent-frameworks-explained` | 1 |
| #485 | `claude-code-claude-md-guide` | `ai-second-brain-obsidian` | 1 |
| #485 | `claude-code-files-and-context` | `ai-second-brain-obsidian` | 1 |
| #485 | `claude-code-headless-json` | `ai-workflow-coding-agents-division` | 1 |
| #485 | `claude-code-mcp-setup-troubleshooting` | `mcp-servers-for-everyone` | 1 |
| #485 | `claude-code-scheduled-tasks` | `ai-calendar-scheduling`, `ai-weekly-review-templates` | 2 |
| #501 | `claude-code-agent-sdk-stateful-runner` | `ai-agent-frameworks-explained` | 1 |
| #501 | `claude-code-mcp-untrusted-output` | `ai-customer-service-line-bot`, `ai-prompt-injection-explained`, `mcp-servers-for-everyone` | 3 |

- 其他 16 篇指向兩篇 Codex 的來源（`codex-account-usage`、`codex-cli-windows`…）都是 #525 的學習中心文章，五個語系都沒上線，現在不算。
- 三批之間（distinct 來源→目標對）：批次 04→#485 22、批次 04→批次 04 42、#485→#485 264、#485→#501 12、#501→#485 85、#501→#501 126。與票面的 12／85 一致。
- 批次 04 另有 `ai-coding-tools-overview-2026` → `codex-beginner-guide`（已上線，會正常成為連結）。

**這個重算有一個限制**：它用 repo 內容包代表「上線頁面的內容」。正式站資料庫裡已發布的版本如果在 #531 之前匯入、之後沒重匯，內文可能還是完整網址——那才是讀者真的會點進「這篇文章目前看不到」的壞連結；
而 article 行內引用在目標未發布時，前端只顯示純文字、不產生連結（`docs/claude-code-series/README.md`「無法解析時呈現純文字」；`apps/api/tests/test_guide_series.py::test_unavailable_targets_leave_no_public_navigation_or_inline_link`）。
所以權威的重算要在主機上跑 `guides-links-check --locale zh-TW`（讀資料庫的已發布版本，列出 `missing`／`unpublished`／`raw_url`），發布前、後各一次（第 7.5 節）。

## 6. 匯入與發布會做什麼（讀指令輸出時用）

- `guides-import` 走後台寫入路徑（`apply_import` → `admin_service.create_article`／`start_translation`／`publish_locale`），發布時搜尋索引與連結圖會一起更新，不需要另外跑 `guides-search-reindex` 或 `guides-links-rebuild`。
- `--dry-run` 不需要 `--actor-email`，輸出 `{"dry_run": true, "articles": [{"slug", "taxonomy", "locales": [{"locale", "action", "publish"}]}]}`；`taxonomy`／`action` 是 `create`／`update`／`unchanged`，`publish` 是「`--publish` 有沒有事要做」。
- 正式跑輸出 `{"created", "updated", "unchanged", "published", "taxonomy_updated", "failed"}`，項目格式 `slug:locale`；`failed` 不是 `null` 時 exit 1。
- `--locale zh-TW` 讓五語系的兩篇 Codex 只建立 zh-TW；之後不帶 `--locale` 重匯，其餘四個語系會是 `create`。
- 不帶 `--slug` 的 dry-run 會列出全部 1,056 個包。預期除了這 111 篇之外還會看到：其他未發布的 life zh-TW 包 95 個 `create`（`codex-*` 58、`gemini-*` 29、`notebooklm-*` 5、`google-flow-*` 2、`llms-txt-evaluation` 1）、旅遊專區未發布的包、以及很多已上線文章的 `update`（#531 之後沒重匯的都會是 `update`，`codex-beginner-guide` 也是）。**這些都不能進 `--slug` 那一步。**
- 匯入不重建容器，不受 `ops/release/README.md` 的多段式發布規則管；但如果 `/root/travel-scanner-deploy.hold` 存在，表示有人正在做分段發布（`activate` 會停服務、換映像），先等它結束。

## 7. 主機執行順序（`/root/travel_scanner`，root；`<admin>` 換成站主的管理員 email）

### 7.0 前置核對

```bash
cd /root/travel_scanner
ls -l /root/travel-scanner-deploy.hold 2>/dev/null && cat /root/travel-scanner-deploy.hold || echo "no hold file"   # 有檔就先等
git log -1 --format='%h %ad %s' --date=short                                   # 應是 a69763b5（#553）或之後
docker compose -f docker-compose.prod.yml ps                                   # api、web 都 running
docker compose -f docker-compose.prod.yml exec -T api sh -c 'ls /app/app/guides/content | grep -c "^claude-code-"'   # 97
```

### 7.1 寫 slug 檔（三個檔，共 111 行）

```bash
mkdir -p /root/held-content-20260919 && cd /root/held-content-20260919
cat > b04.txt <<'EOF'
ai-coding-tools-overview-2026
codex-cli-getting-started
codex-cloud-tasks-github
cursor-editor-guide
github-copilot-guide
vibe-coding-first-website
ai-coding-agents-compared
deploy-ai-built-site-to-vps
ai-coding-git-basics
ai-code-review-safety
ai-coding-cost-tokens-explained
ai-coding-prompt-patterns
ai-build-line-bot-tutorial
ai-build-personal-blog-tutorial
EOF
cat > cc485.txt <<'EOF'
claude-code-tutorials
claude-code-getting-started
claude-code-accounts-and-access
claude-code-platforms-guide
claude-code-terminal-git-basics
claude-code-practice-project-setup
claude-code-task-prompts
claude-code-install-windows
claude-code-install-macos
claude-code-install-linux-wsl
claude-code-desktop-setup
claude-code-desktop-workflow
claude-code-ide-integration
claude-code-on-the-web
claude-code-mobile-ios
claude-code-mobile-android
claude-code-remote-control
claude-code-desktop-dispatch
claude-code-cross-device-workflow
claude-code-markdown-basics
claude-code-claude-md-guide
claude-code-claude-md-scopes
claude-code-rules-and-imports
claude-code-auto-memory
claude-code-settings-json
claude-code-cli-command-guide
claude-code-help-status-doctor
claude-code-sessions-resume
claude-code-context-compact-clear
claude-code-models-usage-config
claude-code-permissions-plan-mode
claude-code-files-and-context
claude-code-understand-codebase
claude-code-implement-feature
claude-code-debug-and-test
claude-code-git-review-pr
claude-code-checkpoints-rewind
claude-code-hooks-and-skills
claude-code-skills-skill-md
claude-code-skill-arguments-resources
claude-code-custom-commands
claude-code-hooks-getting-started
claude-code-hooks-recipes
claude-code-mcp-servers
claude-code-mcp-setup-troubleshooting
claude-code-plugins-guide
claude-code-subagents-guide
claude-code-worktrees-parallel
claude-code-agent-teams
claude-code-chrome-browser
claude-code-computer-use
claude-code-headless-json
claude-code-scheduled-tasks
claude-code-github-actions
claude-code-agent-sdk
claude-code-build-todo-app
claude-code-maintain-existing-project
claude-code-project-data-safety
claude-code-usage-cost-optimization
claude-code-troubleshooting
claude-code-templates-cheatsheet
EOF
cat > cc501.txt <<'EOF'
claude-code-project-rules-workshop
claude-code-monorepo-rules-workshop
claude-code-rules-loading-diagnostics
claude-code-permissions-sandbox-lab
claude-code-context-handoff-workshop
claude-code-team-config-maintenance
claude-code-skill-sop-workshop
claude-code-skill-input-validation
claude-code-skill-resource-design
claude-code-skill-invocation-control
claude-code-skill-regression-testing
claude-code-plugin-team-distribution
claude-code-hook-event-test-lab
claude-code-hook-scoped-formatting
claude-code-hook-quality-gates
claude-code-hook-file-boundaries
claude-code-hook-notifications-audit
claude-code-hook-portability-recovery
claude-code-mcp-local-server-workshop
claude-code-mcp-tool-contracts
claude-code-mcp-http-auth-workshop
claude-code-mcp-failure-contract-tests
claude-code-mcp-untrusted-output
claude-code-issue-to-draft-pr-workshop
claude-code-tdd-debugging-workshop
claude-code-legacy-refactoring-workshop
claude-code-subagent-review-workshop
claude-code-worktree-integration-workshop
claude-code-agent-teams-integration-lab
claude-code-cross-device-recovery-workshop
claude-code-structured-cli-pipeline
claude-code-github-actions-review-workshop
claude-code-scheduled-workflow-reliability
claude-code-agent-sdk-stateful-runner
claude-code-workflow-evaluation-cost
claude-code-advanced-capstone
EOF
wc -l b04.txt cc485.txt cc501.txt            # 14 61 36 → 111
cat b04.txt cc485.txt cc501.txt > all.txt   # 決定二選 (a) 時改用下一行
# grep -v -x -e codex-cli-getting-started -e codex-cloud-tasks-github b04.txt | cat - cc485.txt cc501.txt > all.txt   # (a)：109 行
sort all.txt | uniq -d                       # 應無輸出
SLUG_ARGS=$(sed 's/^/--slug /' all.txt | tr '\n' ' ')
echo "$SLUG_ARGS" | wc -w                    # 222（(a) 是 218）
```

核對容器裡的內容包就是本分支這一版（把 111 個檔案的 sha256 再做一次 sha256）：

```bash
docker compose -f /root/travel_scanner/docker-compose.prod.yml exec -T api sh -c \
  'cd /app/app/guides/content && while read -r s; do sha256sum "$s.json"; done' \
  < <(cat b04.txt cc485.txt cc501.txt) | sha256sum
# 預期 954a319af2dc626ecd88a3a959c4664ec27e40a733d9f7dfe16dff58844a93d1  -   （2026-09-20 起，= main 在 #563 之後）
# 2026-09-20 第一次執行時關卡擋下：映像算出 954a319a…，文件原寫 8674d468…（= #559 基準，已在 6a254971 重算驗證）。
# 查因：6a254971..main 之間只有 #563 `14ce467d` 碰過這 111 篇，+119 行／0 刪除，每篇加一行圖片 description
# （兩篇 Codex 五語各一行）。映像 = 現在的 main。純附加 metadata，不影響匯入，預期值改成上面那個。
# 單檔參考：codex-cli-getting-started.json 475c1a62…ecda6、codex-cloud-tasks-github.json 497085b1…104d7e、claude-code-tutorials.json 24b1ff9c…f46d
```

數字不同就表示映像不是這一版（或有人又改了內容包）：先 `git log -- apps/api/app/guides/content/` 查原因，再決定要不要部署，**不要**直接匯入。

### 7.2 不帶 slug 的 dry-run（確認 111 篇仍全是 create、看清楚其他人的內容）

```bash
cd /root/travel_scanner
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import \
  --locale zh-TW --dry-run > /root/held-content-20260919/dryrun-all.json 2> /root/held-content-20260919/dryrun-all.err
echo "exit=$?"; tail -3 /root/held-content-20260919/dryrun-all.err
cd /root/held-content-20260919 && python3 - <<'EOF'
import json
from collections import Counter
plan = json.load(open('dryrun-all.json'))
want = [l.strip() for l in open('all.txt') if l.strip()]
rows = {a['slug']: a for a in plan['articles']}
missing = [s for s in want if s not in rows]
not_create = [(s, rows[s]['taxonomy'], rows[s]['locales']) for s in want if s in rows and not (
    rows[s]['taxonomy'] == 'create' and [l['locale'] for l in rows[s]['locales']] == ['zh-TW']
    and rows[s]['locales'][0]['action'] == 'create' and rows[s]['locales'][0]['publish'])]
print('plan rows', len(rows), '| ours', len(want), '| missing', missing, '| not a plain zh-TW create', not_create)
others = Counter(a['taxonomy'] for s, a in rows.items() if s not in want)
print('other packs by taxonomy', dict(others))
print('other creates:', sorted(s for s, a in rows.items() if s not in want and a['taxonomy'] == 'create'))
EOF
```

要看到：`missing []`、`not a plain zh-TW create []`；`other creates` 大致是第 6 節列的那些。有任何一篇不是 create，先停下來查。

### 7.3 `--slug` 限定的 `--dry-run --publish`，核對計畫與清單完全一致

```bash
cd /root/travel_scanner
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import \
  --actor-email <admin> --locale zh-TW --publish --dry-run $SLUG_ARGS \
  > /root/held-content-20260919/dryrun-slugs.json 2> /root/held-content-20260919/dryrun-slugs.err
echo "exit=$?"
cd /root/held-content-20260919 && python3 - <<'EOF'
import json
plan = json.load(open('dryrun-slugs.json'))
want = set(l.strip() for l in open('all.txt') if l.strip())
got = {a['slug'] for a in plan['articles']}
bad = [(a['slug'], a['taxonomy'], a['locales']) for a in plan['articles']
       if a['taxonomy'] != 'create' or [ (l['locale'], l['action'], l['publish']) for l in a['locales'] ] != [('zh-TW', 'create', True)]]
print('plan', len(got), 'want', len(want), '| missing', sorted(want - got), '| extra', sorted(got - want), '| bad', bad)
EOF
```

要看到：`plan 111 want 111 | missing [] | extra [] | bad []`（(a) 是 109）。

### 7.4 正式 `--publish`（同一組參數去掉 `--dry-run`），再回放 dry-run

```bash
cd /root/travel_scanner
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import \
  --actor-email <admin> --locale zh-TW --publish $SLUG_ARGS \
  > /root/held-content-20260919/publish.json 2> /root/held-content-20260919/publish.err
echo "exit=$?"
python3 -c "import json; r=json.load(open('/root/held-content-20260919/publish.json')); print({k: (len(v) if isinstance(v, list) else v) for k, v in r.items()})"
# 預期 created 111、published 111、updated 0、unchanged 0、failed None（taxonomy_updated 依匯入時的主題差異而定）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import \
  --locale zh-TW --dry-run $SLUG_ARGS | python3 -c "import json,sys; p=json.load(sys.stdin); print(sorted({(a['taxonomy'], l['action'], l['publish']) for a in p['articles'] for l in a['locales']}))"
# 預期 [('unchanged', 'unchanged', False)]
```

### 7.5 驗證

逐頁與 hero（任何機器都能跑，未登入；nginx 每 IP 5 r/s，這裡每個請求後停 1.5 秒，111 篇約 6 分鐘）：

```bash
cd /root/held-content-20260919
UA='Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'
while read -r s; do
  code=$(curl -sS -A "$UA" -o page.html -w '%{http_code}' "https://mokaair.com/zh-TW/life/$s"); sleep 1.5
  hero=$(curl -sS -A "$UA" -o /dev/null -w '%{http_code}' "https://mokaair.com/guides/$s/hero.jpg"); sleep 1.5
  title=$(grep -o '<title>[^<]*</title>' page.html | head -1)
  robots=$(grep -o '<meta name="robots"[^>]*>' page.html | head -1)
  canon=$(grep -o '<link rel="canonical" href="[^"]*"' page.html | head -1)
  echo "$s page=$code hero=$hero robots=${robots:-none} $title $canon"
done < all.txt | tee page-checks.txt
grep -v 'page=200 hero=200 robots=none' page-checks.txt          # 應無輸出
grep -c '這篇文章目前看不到</title>' page-checks.txt               # 應為 0
```

sitemap、summary 與系列 API（各一個請求）：

```bash
curl -sS -A "$UA" https://mokaair.com/sitemaps/sitemap/life-zh-TW.xml -o life-zh-TW.xml; sleep 1.5
python3 -c "
import re; want=[l.strip() for l in open('all.txt') if l.strip()]
locs=set(re.findall(r'<loc>https://mokaair.com/zh-TW/life/([^<]+)</loc>', open('life-zh-TW.xml').read()))
print('article locs', len([l for l in locs if not l.startswith('topics/')]), 'ours present', sum(s in locs for s in want), 'missing', [s for s in want if s not in locs])"
# 預期 816（(a) 814），ours present 111，missing []
curl -sS -A "$UA" https://mokaair.com/api/travel/guides/sitemap/summary; echo; sleep 1.5      # life zh-TW 816、合計 1381
curl -sS -A "$UA" 'https://mokaair.com/api/travel/guides/series/claude-code?locale=zh-TW' | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('hub') or d.get('slug'), 'entries', len(d.get('entries', [])))"
# 預期 entries 96
```

站內連結重算（主機，讀資料庫的已發布版本）：

```bash
cd /root/travel_scanner
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-links-check --locale zh-TW \
  > /root/held-content-20260919/links-after.json; echo "exit=$?"
python3 - <<'EOF'
import json
want = set(l.strip() for l in open('/root/held-content-20260919/all.txt') if l.strip())
f = json.load(open('/root/held-content-20260919/links-after.json'))['findings']
print('findings', len(f))
print('still pointing at one of ours:', [x for x in f if x['target'] in want or x['target'].split('/')[-1] in want])
print('from the two Codex pages:', [x for x in f if x['source'] in ('codex-cli-getting-started', 'codex-cloud-tasks-github')])
EOF
```

要看到：`still pointing at one of ours: []`。選 (b) 時 `from the two Codex pages` 會列出指向學習中心的 `unpublished`，這是站主同意的例外，抄到第 8.7 節。
如果想留發布前的對照，在 7.4 之前先跑一次同樣的指令存成 `links-before.json`。

### 7.6 收尾

- 把 7.2–7.5 的輸出摘要抄進第 8 節（完整 JSON 留在主機 `/root/held-content-20260919/`）。
- 票：`npm run tasks -- claim 2026-09-15-publish-held-ai-coding-content --owner <你> --force`（相依票未完成要 `--force`，理由是站主已在第 1 節簽字），勾完 DoD，`npm run tasks -- done 2026-09-15-publish-held-ai-coding-content`，連同本文件一起提交。
- 選 (a) 時：在 `2026-09-14-codex-learning-series` 的票裡記一筆「兩篇 Codex 隨學習中心一起匯入」。

## 8. 主機執行紀錄（只有主機上的執行能填；留空表示還沒做）

### 8.1 站主決定

- 決定一：接受，照文章寫明的限制發布 36 篇（2026-09-20，站主於 AskUserQuestion 選定；claude-fable-5-1 代填）
- 決定二：(b) 111 篇 zh-TW 全發（2026-09-20，同上）

### 8.2 前置核對（7.0、7.1）

```text
執行時間（UTC）: 2026-09-19 ~17:0x（台北 09-20 凌晨），腳本 /root/held111-precheck.sh，跑了兩次
git log -1: 9af3511f 2026-09-20 ops(nginx): repo 補上已在主機的爬蟲允許清單，並修好 CI 的設定測試 (#568)
compose ps: travel_scanner-api-1 Up 2 hours、travel_scanner-web-1 Up 2 hours（映像為 #566 ecc6cbc0 部署）
claude-code-* 檔數: 97
111 檔 sha256 合成值: 954a319af2dc626ecd88a3a959c4664ec27e40a733d9f7dfe16dff58844a93d1
  第一次執行與文件原值 8674d468… 不符、關卡停止；查因見 §7.1 註解（#563 每篇加一行圖片 description，映像 = main）。
  在本機驗證：6a254971 算出 8674d468…（= 文件原值）、origin/main 算出 954a319a…（= 映像）。第二次執行以此值通過。
hold 檔: 無
slug 檔: b04 14 / cc485 61 / cc501 36 = 111，無重複；SLUG_ARGS 222 個字
actor: 由 api 容器的 ADMIN_EMAILS 第一個值取得，不寫進指令或文件
```

### 8.3 不帶 slug 的 dry-run（7.2）

```text
執行時間（UTC）: 2026-09-19 ~17:2x（第二次 precheck，關卡以更新後的 sha 通過）
plan rows / ours / missing / not a plain zh-TW create: 1036 / 111 / [] / []
other packs by taxonomy: {'unchanged': 829, 'create': 95, 'update': 1}
other creates: 95（codex-account-usage、codex-agents-md、codex-agents-md-scopes、codex-automation-recovery、codex-automations、codex-browser-images、codex-ci-workflows、codex-cli-linux-wsl、codex-cli-macos、codex-cli-windows、codex-commands、codex-config-toml …）= §6 預告的 codex／gemini／notebooklm／google-flow／llms-txt-evaluation，一篇都沒進 --slug
```

### 8.4 `--slug` dry-run `--publish`（7.3）

```text
執行時間（UTC）: 同上，緊接 7.2
plan / want / missing / extra / bad: 111 / 111 / [] / [] / []
actor: api 容器 ADMIN_EMAILS 第一個值（不寫進文件）
```

### 8.5 正式 `--publish` 與回放 dry-run（7.4）

```text
執行時間（UTC）: 2026-09-19T17:49:52Z → 17:50:18Z（26 秒），/root/held111-publish.sh 在 nohup 下執行，輸出在 /root/held-content-20260919/publish-run.log
publish.json 摘要: {'created': 111, 'updated': 0, 'unchanged': 0, 'published': 111, 'taxonomy_updated': 0, 'failed': None}
回放 dry-run（--slug 同組）: [('unchanged', 'unchanged', False)]
決定二 = (b)：兩篇 Codex 只建 zh-TW，四個外語版本留到學習中心發布時再匯（屆時為 create）
```

### 8.6 逐頁驗證、sitemap、summary、系列 API（7.5）

```text
執行時間（UTC）: 2026-09-19T17:51:03Z → 17:57:46Z，/root/held111-verify.sh（nohup），日誌 /root/held-content-20260919/verify-run.log
逐頁: 111/111 都是 page=200 hero=200 robots=none；「這篇文章目前看不到」標題 0；canonical 全部 = https://mokaair.com/zh-TW/life/<slug>
sitemap life-zh-TW.xml: article locs 816、ours present 111、missing []
summary: life zh-TW 816（intel 19、howto 106；四個外語各 life 90／howto 18／intel 2）→ 合計 1,381
系列 API /api/travel/guides/series/claude-code?locale=zh-TW: hub claude-code-tutorials、entries 96
```

### 8.7 `guides-links-check --locale zh-TW`（7.5）

```text
exit=1（有 findings 即非零，預期）；findings 19
still pointing at one of ours: []
from the two Codex pages: 14 —— codex-cli-getting-started → codex-commands／codex-agents-md／…（10）、codex-cloud-tasks-github → codex-learning-hub／codex-mobile-guide／codex-testing-review／codex-first-project（4），
  全部是決定二 (b) 同意暫留的 unpublished 引用（頁面上顯示純文字，學習中心發布時自動變連結）
其餘 5 筆 findings 不指向本批，屬發布前就存在的狀況；完整 JSON 在主機 /root/held-content-20260919/links-after.json
```

### 8.8 發布後注意到、但不屬本票的事

- `guides-links-check` 另有 5 筆不指向本批的 findings，發布前就在；沒有逐一判讀，留給 `2026-09-14-codex-learning-series`（blocked）或連結維護票。
- §7.1 的 sha256 預期值會隨每次動到這 111 篇內容包的 PR 過期（這次是 #563 加圖片 description）。關卡本身是對的，但下次照 runbook 跑之前先在本機用同一方法重算 origin/main。
- 111 篇全是 zh-TW；四個外語版本（兩篇 Codex 有）留到 Codex 學習中心發布時再匯，屆時為 create。

```text
```
