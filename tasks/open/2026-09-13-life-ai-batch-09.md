---
id: 2026-09-13-life-ai-batch-09
title: 生活分享 AI 系列批次 09：工作流、效率與自動化（20 篇）
status: in-progress
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

- [ ] 二十個 `apps/api/app/guides/content/<slug>.json`（zh-TW），每篇：hero（自繪插圖渲染的 `hero.jpg` 或 Commons 照片）、
      至少一張自繪 `diagram-1.svg`、≥3 個 h2、一表、一 callout、sources 每筆有 `checked_on`、至少一個站內 `link`；
      合作連結只在總表標了的篇、只放文章真的用到的段落。
- [ ] 沒有任何產品 logo、字標、圖示或介面截圖；照片只來自 Commons 的 CC0／PD／CC BY／CC BY-SA，授權由 Commons API 讀回。
- [ ] 方案、價格、模型名、額度都在寫作當天查官網；查不到的寫「以官網為準」。
- [ ] `guides-pack lint --kind life` 沒有 error；每張 hero 與圖解渲染成 PNG 後人工看過；`test_guides_content_pack.py` 全綠。

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

- [ ] 認領後從總表抄出指派，一篇一個撰稿代理、每波最多七個，代理照 `docs/life-ai-series-brief.md` 產出工作區。
- [ ] 每篇落地就 `guides-pack ingest`；被拒的退回修。
- [ ] `guides-pack lint --render-dir` 逐張看圖；跑測試；更新這張票；commit。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --render-dir /tmp/renders --catalogue ../../docs/life-ai-series.md
cd apps/api && uv run pytest tests/test_guides_content_pack.py tests/test_guide_partner_links.py -q
npm run check:tasks
```

部署後在主機：`python -m app.cli guides-import --actor-email <admin> --dry-run`，再 `--publish`。

## Notes

- 前三批旅遊文章的經驗：兩篇一個代理會在半小時左右撞到額度，一篇一個代理、先寫檔再寫報告最穩。
