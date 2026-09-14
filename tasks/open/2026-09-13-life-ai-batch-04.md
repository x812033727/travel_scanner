---
id: 2026-09-13-life-ai-batch-04
title: 生活分享 AI 系列批次 04：AI 寫程式：Claude Code、Codex、Gemini CLI、Cursor、Copilot（20 篇）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-13T11:55:59Z
completed_at:
branch:
depends_on:
  - 2026-09-13-life-ai-series-tooling
  - 2026-09-13-life-ai-series-catalogue
  - 2026-09-13-life-ai-batch-01
scope:
  - apps/api/app/guides/content/ai-coding-tools-overview-2026.json
  - apps/api/app/guides/content/claude-code-getting-started.json
  - apps/api/app/guides/content/claude-code-claude-md-guide.json
  - apps/api/app/guides/content/claude-code-mcp-servers.json
  - apps/api/app/guides/content/claude-code-hooks-and-skills.json
  - apps/api/app/guides/content/claude-code-on-the-web.json
  - apps/api/app/guides/content/gemini-cli-getting-started.json
  - apps/api/app/guides/content/cursor-editor-guide.json
  - apps/api/app/guides/content/github-copilot-guide.json
  - apps/api/app/guides/content/vibe-coding-first-website.json
  - apps/api/app/guides/content/ai-coding-agents-compared.json
  - apps/api/app/guides/content/deploy-ai-built-site-to-vps.json
  - apps/api/app/guides/content/ai-coding-git-basics.json
  - apps/api/app/guides/content/ai-code-review-safety.json
  - apps/api/app/guides/content/ai-coding-cost-tokens-explained.json
  - apps/api/app/guides/content/ai-coding-prompt-patterns.json
  - apps/api/app/guides/content/ai-build-line-bot-tutorial.json
  - apps/api/app/guides/content/ai-build-personal-blog-tutorial.json
  - apps/web/public/guides/ai-coding-tools-overview-2026
  - apps/web/public/guides/claude-code-getting-started
  - apps/web/public/guides/claude-code-claude-md-guide
  - apps/web/public/guides/claude-code-mcp-servers
  - apps/web/public/guides/claude-code-hooks-and-skills
  - apps/web/public/guides/claude-code-on-the-web
  - apps/web/public/guides/gemini-cli-getting-started
  - apps/web/public/guides/cursor-editor-guide
  - apps/web/public/guides/github-copilot-guide
  - apps/web/public/guides/vibe-coding-first-website
  - apps/web/public/guides/ai-coding-agents-compared
  - apps/web/public/guides/deploy-ai-built-site-to-vps
  - apps/web/public/guides/ai-coding-git-basics
  - apps/web/public/guides/ai-code-review-safety
  - apps/web/public/guides/ai-coding-cost-tokens-explained
  - apps/web/public/guides/ai-coding-prompt-patterns
  - apps/web/public/guides/ai-build-line-bot-tutorial
  - apps/web/public/guides/ai-build-personal-blog-tutorial
---

# 生活分享 AI 系列批次 04：AI 寫程式：Claude Code、Codex、Gemini CLI、Cursor、Copilot（20 篇）

## Why

`docs/life-ai-series.md` 的批次 04。生活分享專區今天是空的，站主要至少 200 篇 AI 工具的介紹與教學，
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

1. `ai-coding-tools-overview-2026` · AI 寫程式工具總覽：Claude Code、Codex、Gemini CLI、Cursor、Copilot · ai, software · 圖：插 · 易變
2. `claude-code-getting-started` · Claude Code 入門：安裝、第一個專案與常用指令 · ai, tutorial · 圖：插 · 易變
3. `claude-code-claude-md-guide` · 寫好 CLAUDE.md：讓 Claude Code 記住專案規矩 · ai, tutorial · 圖：插
4. `claude-code-mcp-servers` · Claude Code 接 MCP：連 GitHub、資料庫與瀏覽器 · ai, tutorial · 圖：插
5. `claude-code-hooks-and-skills` · Claude Code 的 Hooks 與 Skills：自動化你的工作流 · ai, tutorial · 圖：插 · 易變
6. `claude-code-on-the-web` · Claude Code 網頁版與手機：在雲端跑任務、回來看結果 · ai, tutorial · 圖：插 · 易變
7. `codex-cli-getting-started` · Codex CLI 入門：在終端機裡讓 OpenAI 幫你改程式 · ai, tutorial · 圖：插 · 易變
8. `codex-cloud-tasks-github` · Codex 雲端任務：連 GitHub、平行跑多個任務、開 PR · ai, tutorial · 圖：插 · 易變
9. `gemini-cli-getting-started` · Gemini CLI 入門：免費額度、安裝與常用指令 · ai, tutorial · 圖：插 · 易變
10. `cursor-editor-guide` · Cursor 編輯器入門：Tab 補全、Chat 與代理模式 · ai, software · 圖：插 · 易變
11. `github-copilot-guide` · GitHub Copilot 入門：VS Code 裡的補全、Chat 與代理 · ai, software · 圖：插 · 易變
12. `vibe-coding-first-website` · Vibe coding：不會寫程式也能做出第一個網站 · ai, tutorial · 圖：插 · 合作：H
13. `ai-coding-agents-compared` · AI 寫程式代理實測比較：同一個需求三個工具怎麼做 · ai · 圖：插 · 易變
14. `deploy-ai-built-site-to-vps` · 把 AI 幫你寫的網站放上網：VPS、網域與 HTTPS 一次搞定 · tutorial, software · 圖：插 · 合作：H
15. `ai-coding-git-basics` · 用 AI 寫程式前該懂的 Git：分支、提交與還原 · tutorial, software · 圖：插
16. `ai-code-review-safety` · AI 寫的程式能信嗎：審查、測試與安全檢查清單 · ai, tutorial · 圖：插
17. `ai-coding-cost-tokens-explained` · AI 寫程式的費用怎麼算：token、訂閱與 API 額度 · ai, software · 圖：插 · 易變
18. `ai-coding-prompt-patterns` · 給程式代理的提示模式：先規劃、再實作、最後驗證 · ai, tutorial · 圖：插
19. `ai-build-line-bot-tutorial` · 用 AI 幫你做 LINE 機器人：從零到上線 · tutorial, software · 圖：插 · 合作：H
20. `ai-build-personal-blog-tutorial` · 用 AI 做個人部落格：靜態網站產生器與部署 · tutorial, software · 圖：插 · 合作：H

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

2026-09-14: The two Codex articles (codex-cli-getting-started and codex-cloud-tasks-github), including their public image directories, are transferred to 2026-09-14-codex-learning-series under the user's approved five-language Codex plan. This task was open and unowned at transfer; retain the other 18 articles here. Do not recreate the transferred files.
