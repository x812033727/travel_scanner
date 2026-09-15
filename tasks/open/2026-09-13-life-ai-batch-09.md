---
id: 2026-09-13-life-ai-batch-09
title: 生活分享 AI 系列批次 09：工作流、效率與自動化（20 篇）
status: review
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-15T00:26:24Z
created_at: 2026-09-13T11:56:00Z
completed_at:
branch:
depends_on:
  - 2026-09-13-life-ai-series-tooling
  - 2026-09-13-life-ai-series-catalogue
  - 2026-09-13-life-ai-batch-01
scope:
  - apps/api/app/guides/content/ai-note-taking-workflow.json
  - apps/api/app/guides/content/notion-ai-guide.json
  - apps/api/app/guides/content/ai-meeting-notes-tools.json
  - apps/api/app/guides/content/n8n-ai-automation-guide.json
  - apps/api/app/guides/content/zapier-make-ai-automation.json
  - apps/api/app/guides/content/mcp-servers-for-everyone.json
  - apps/api/app/guides/content/ai-email-management.json
  - apps/api/app/guides/content/ai-calendar-scheduling.json
  - apps/api/app/guides/content/ai-pdf-tools-summarize-translate.json
  - apps/api/app/guides/content/ai-browsers-guide.json
  - apps/api/app/guides/content/ai-spreadsheet-automation.json
  - apps/api/app/guides/content/ai-second-brain-obsidian.json
  - apps/api/app/guides/content/ai-prompt-library-personal.json
  - apps/api/app/guides/content/ai-for-social-media-content.json
  - apps/api/app/guides/content/ai-for-youtube-creators.json
  - apps/api/app/guides/content/ai-for-small-business-taiwan.json
  - apps/api/app/guides/content/ai-customer-service-line-bot.json
  - apps/api/app/guides/content/ai-agent-frameworks-explained.json
  - apps/api/app/guides/content/ai-weekly-review-templates.json
  - apps/api/app/guides/content/ai-reading-list-books-2026.json
  - apps/web/public/guides/ai-note-taking-workflow
  - apps/web/public/guides/notion-ai-guide
  - apps/web/public/guides/ai-meeting-notes-tools
  - apps/web/public/guides/n8n-ai-automation-guide
  - apps/web/public/guides/zapier-make-ai-automation
  - apps/web/public/guides/mcp-servers-for-everyone
  - apps/web/public/guides/ai-email-management
  - apps/web/public/guides/ai-calendar-scheduling
  - apps/web/public/guides/ai-pdf-tools-summarize-translate
  - apps/web/public/guides/ai-browsers-guide
  - apps/web/public/guides/ai-spreadsheet-automation
  - apps/web/public/guides/ai-second-brain-obsidian
  - apps/web/public/guides/ai-prompt-library-personal
  - apps/web/public/guides/ai-for-social-media-content
  - apps/web/public/guides/ai-for-youtube-creators
  - apps/web/public/guides/ai-for-small-business-taiwan
  - apps/web/public/guides/ai-customer-service-line-bot
  - apps/web/public/guides/ai-agent-frameworks-explained
  - apps/web/public/guides/ai-weekly-review-templates
  - apps/web/public/guides/ai-reading-list-books-2026
---

# 生活分享 AI 系列批次 09：工作流、效率與自動化（20 篇）

## Why

`docs/life-ai-series.md` 的批次 09。生活分享專區今天是空的，站主要至少 200 篇 AI 工具的介紹與教學，
分十一批產出；這張票是其中一批，scope 精確到這二十篇的內容包與圖片目錄，和其他批次可以同時進行。

開工前先讀 `docs/life-ai-series.md` 的「經驗記錄」與批次 01 票的 Outcome。

## Definition of done

- [x] 二十個 `apps/api/app/guides/content/<slug>.json`（zh-TW），每篇：hero（自繪插圖渲染的 `hero.jpg` 或 Commons 照片）、
      至少一張自繪 `diagram-1.svg`、≥3 個 h2、一表、一 callout、sources 每筆有 `checked_on`、至少一個站內 `link`；
      合作連結只在總表標了的篇、只放文章真的用到的段落。
- [x] 沒有任何產品 logo、字標、圖示或介面截圖；照片只來自 Commons 的 CC0／PD／CC BY／CC BY-SA，授權由 Commons API 讀回。
- [x] 方案、價格、模型名、額度都在寫作當天查官網；查不到的寫「以官網為準」。
- [x] `guides-pack lint --kind life` 沒有 error；每張 hero 與圖解渲染成 PNG 後人工看過；`test_guides_content_pack.py` 全綠。

## Steps

這二十篇（slug · 標題 · topics · 圖 · 合作 · 易變）：

1. `ai-note-taking-workflow` · 用 AI 做筆記：Notion AI、Obsidian 與 NotebookLM · productivity, ai · 圖：插
2. `notion-ai-guide` · Notion AI 入門 · productivity, software · 圖：插 · 易變
3. `ai-meeting-notes-tools` · AI 會議記錄：Otter、Google Meet、Teams 摘要 · productivity, ai · 圖：照 · 易變
4. `n8n-ai-automation-guide` · n8n 入門：用 AI 節點做自動化 · tutorial, productivity · 圖：插 · 合作：H
5. `zapier-make-ai-automation` · Zapier 與 Make 的 AI 自動化 · productivity, software · 圖：插 · 易變
6. `mcp-servers-for-everyone` · MCP 伺服器實用清單：檔案、Google、Notion、瀏覽器 · ai, tutorial · 圖：插 · 易變
7. `ai-email-management` · 用 AI 管理 Email：分類、摘要與草稿 · productivity, ai · 圖：插
8. `ai-calendar-scheduling` · AI 排程與行事曆助手 · productivity, ai · 圖：插 · 易變
9. `ai-pdf-tools-summarize-translate` · AI PDF 工具：摘要、翻譯、問答 · productivity, software · 圖：插
10. `ai-browsers-guide` · AI 瀏覽器：Comet、Atlas、Dia 與 Chrome 的 AI · ai, software · 圖：插 · 易變
11. `ai-spreadsheet-automation` · 試算表 AI 自動化：Sheets、Excel Copilot · productivity, ai · 圖：插
12. `ai-second-brain-obsidian` · Obsidian＋AI：打造第二大腦 · productivity, software · 圖：插
13. `ai-prompt-library-personal` · 建立自己的提示詞庫 · productivity, ai · 圖：插
14. `ai-for-social-media-content` · 用 AI 做社群貼文：IG、Threads、FB 排程 · ai, daily · 圖：插
15. `ai-for-youtube-creators` · YouTuber 的 AI 工作流：腳本、字幕、縮圖 · ai, productivity · 圖：插
16. `ai-for-small-business-taiwan` · 台灣小店的 AI 應用：客服、菜單、廣告 · ai, daily · 圖：照
17. `ai-customer-service-line-bot` · 用 AI 做客服機器人：LINE 官方帳號接 AI · tutorial, software · 圖：插 · 合作：H
18. `ai-agent-frameworks-explained` · Agent 框架入門：OpenAI Agents SDK、Claude Agent SDK、LangGraph · ai, tutorial · 圖：插 · 易變
19. `ai-weekly-review-templates` · AI 週回顧與目標管理範本 · productivity, daily · 圖：插
20. `ai-reading-list-books-2026` · AI 入門書單：十本值得讀的書 · ai, misc · 圖：照 · 合作：B · 易變

- [x] 認領後從總表抄出指派，一篇一個撰稿代理、每波最多七個，代理照 `docs/life-ai-series-brief.md` 產出工作區。
- [x] 每篇落地就 `guides-pack ingest`；被拒的退回修。
- [x] `guides-pack lint --render-dir` 逐張看圖；跑測試；更新這張票；commit。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --render-dir /tmp/renders --catalogue ../../docs/life-ai-series.md
cd apps/api && uv run pytest tests/test_guides_content_pack.py tests/test_guide_partner_links.py -q
npm run check:tasks
```

部署後在主機：`python -m app.cli guides-import --actor-email <admin> --dry-run`，再 `--publish`。

## Notes

- 前三批旅遊文章的經驗：兩篇一個代理會在半小時左右撞到額度，一篇一個代理、先寫檔再寫報告最穩。

## Outcome (2026-09-15)

- 二十篇全部落地：`apps/api/app/guides/content/<slug>.json` 與 `apps/web/public/guides/<slug>/{hero.jpg,hero.svg,diagram-1.svg}`，slug 照 scope 清單；每篇一張自繪 hero（jpg 最大 61 KB）與一張 1600×900 自繪圖解，全部渲染成 PNG 人工看過。總表標「照」的三篇（會議記錄、小店、書單）一律改自繪，避免 Commons 授權與 429 問題。
- 檢查：`pack_cli lint --kind life --catalogue ../../docs/life-ai-series.md` 0 error（warning 只有既有的 `pack_not_in_catalogue`、尚未寫的批次 10–12 `catalogue_missing_pack`，以及 `sitemap_budget`：本批落地後 repo 內 (article, locale) 列數為 1,017（含同日合併的其他系列），已超過共用 sitemap 的 1,000 列上限——這是 repo 內容包的計數，不是已發布數；拆 sitemap 由 `tasks/open/2026-09-14-sitemap-split-before-1000-rows.md` 與 `2026-09-14-guide-sitemap-capacity.md` 處理，發布前請先完成其中一張）；`uv run pytest tests/test_guides_content_pack.py tests/test_guide_partner_links.py` 63 passed、28 skipped；`npm run check:tasks` 通過。
- 來源：每篇 12–20 筆，`checked_on` 全為 2026-09-15，只用官方頁、官方倉庫、法規資料庫、出版社官網與國家圖書館 ISBN 系統；沒有任何合作連結（總表的 H／B 標記沒有聯盟網址可用）。
- 審稿：每篇跑 `life_links`、dry-run、文字 dump、圖解與 hero 目視，並用 curl／WebFetch 逐篇抽查 8–15 個數字；十二篇經一輪修正（字數超限三篇、正文偏短一篇、hero 四角星 sparkle 兩篇、來源網址或缺漏五篇、Make 年繳價一篇），無二輪。審稿記錄在 session scratchpad 的 `life09/review-log.md`。
- 與指派不同、寫手照當天官網改寫的事實（重點）：NotebookLM 已改名 Gemini Notebook（說明中心搬到 support.google.com/gemininotebook，2026-09-02 起使用上限改為運算量制）；Notion AI 只在 Business／Enterprise、Notion Mail 2026-09-22 關閉；Zoom AI Companion 名稱退場、ZoomMate 另計；Google Meet「幫我做筆記」語言清單無中文、2026-09-21 起 Business Standard／Plus 預設開啟；Otter 中文只有簡體且標 beta；n8n npm 安裝自 3.0（2026 年 10 月）淘汰、Business 是自架方案、Line 節點已淘汰；Make 已把 operations 改名 credits、AI Agent (New) 2026-02-02；MCP 參考伺服器只剩七個、Google 有官方 Workspace 遠端 MCP（開發者預覽）、ChatGPT app 目錄 2026-07-09 併入 plugin 目錄；ChatGPT Atlas 2026-08-09 停止運作、Chrome auto browse 限美國、Dia 屬 Atlassian、Comet 免費；Excel 的 COPILOT 函式 2026-09-14 停用、Google 試算表 AI 函式語言清單只有 zh-CN；Clockwise 2026-03-27 收攤、Reclaim 屬 Dropbox；Obsidian 的 Local REST API 外掛已內建 MCP；ChatGPT 個人帳號已不能新建 GPT；YouTube 靈感分頁 2026 年 8 月起淘汰、自動配音對繁中只能配成英語；LINE 官方帳號 2026-11-01 起調價、AI 聊天機器人（β）屬聊天進階方案；Google 商家檔案與 Google Ads 的 AI 功能語言清單皆無中文；Empire of AI、The Alignment Problem、AI Snake Oil 查無繁中版。
- 官網自己前後不一致、正文擇一並註明的：Obsidian pricing 與 sync 頁的 Sync 價格（以 /sync 為準）；Ollama FAQ 預設上下文 4096 與 Obsidian Interpreter 頁 2048（兩者都寫）；Reclaim 頁首「from Dropbox」與定價頁頁尾版權（以關於頁為準）；Dia 首頁只寫 macOS 而方案頁提到 Windows（以官網為準）。
- 讀法：docs.claude.com 全站已轉到 platform.claude.com／code.claude.com，langchain-ai.github.io 轉到 docs.langchain.com，google.github.io/adk-docs 轉到 adk.dev，help.obsidian.md 轉到 obsidian.md/help（JS 頁，改讀 publish 後端 Markdown），sources 一律記轉址後網址；Meta Business 說明中心的內文藏在 JS payload（curl Safari UA + `--compressed` 後解碼）、transparency.meta.com 只有 WebFetch 讀得到；canva.com、make.com 定價頁、support.deepl.com、us.macmillan.com 對本環境 403（DeepL 走 Zendesk API，Make 用 Wayback 快照）；microsoft.com 台灣定價要 Safari UA；help.otter.ai 走 Zendesk API；support.zoom.com 用 WebFetch；Buffer 有機器可讀的 `/pricing.md`。
- 總表標題同步 15 列（`docs/life-ai-series.md`），連結文字收完後統一為目標文章標題。
- 撰稿代理：20 個 Opus 代理、一篇一個、同時最多七個；七個代理在 2026-09-15 約 03:00 UTC 撞到帳號的 session 額度被切斷，03:30 重置後用 SendMessage 接續同一個代理，查證不用重做，全部順利交件。
- 部署後在主機：`python -m app.cli guides-import --actor-email <admin> --dry-run`，確認後再 `--publish`；發布前先處理 sitemap 拆分。
