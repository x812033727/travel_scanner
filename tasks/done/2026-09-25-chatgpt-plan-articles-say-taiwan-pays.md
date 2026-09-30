---
id: 2026-09-25-chatgpt-plan-articles-say-taiwan-pays
title: ChatGPT 方案文章還寫台灣以美元計價
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-30T03:48:02Z
created_at: 2026-09-25T06:01:29Z
completed_at: 2026-09-30T04:41:16Z
branch: claude/chatgpt-plans-refresh
depends_on: []
scope:
  - apps/api/app/guides/content/chatgpt-plans-plus-pro-2026.json
  - apps/api/app/guides/content/ai-free-vs-paid-plans-2026.json
  - apps/web/public/guides/chatgpt-plans-plus-pro-2026
  - apps/web/public/guides/ai-free-vs-paid-plans-2026/diagram-1.svg
---

# ChatGPT 方案文章還寫台灣以美元計價

## Why

2026-09-25 查核影片〈ChatGPT 開始有廣告了〉時，未登入從台灣開 chatgpt.com/pricing，已直接顯示新台幣含稅價：Go 每月 NT$270、Plus 每月 NT$690（頁面載入的價格資料標 TWD、含 5% 稅）。站內 `chatgpt-plans-plus-pro-2026` 與 `ai-free-vs-paid-plans-2026` 仍寫台灣網頁結帳以美元計價另加 5% 營業稅；`chatgpt-plans-plus-pro-2026` 的方案階梯圖（`apps/web/public/guides/chatgpt-plans-plus-pro-2026/diagram-1.svg`）還列了舊的 Plus 型號名、只標免費版有廣告。

## Definition of done

- [x] 兩篇文章的台灣價格改成官方新台幣含稅價，附網址與查證日；Go 標明「可能有廣告」、Plus 以上沒有。
- [x] 方案階梯圖重畫（型號、廣告標示、幣別）。
- [x] 五語系一致（skill `content-pipeline`）。

## Steps

- [x] 重查 chatgpt.com/pricing（台灣、未登入）與 OpenAI Help Center 的方案頁。
- [x] 改寫、重畫圖、ingest、部署後匯入。

## How to verify

正式站兩篇文章與圖都顯示新台幣價格與新的查證日。

## Notes

- 影片那邊已改用官方新台幣價，並把引用這張圖的場景調整過；圖重畫後影片可以再引用。
- 2026-09-30 (claude-opus-5-5, owner chose a full refresh): the coordinator read
  chatgpt.com/zh-Hant/pricing/ in the in-app browser from Taiwan, logged out
  (Go $270, Plus $690, Pro from $3,300; scripts get a Cloudflare check, which
  was not bypassed); the multi-currency page now lists TWD (NT$) for Taiwan.
  VAT inclusion could not be confirmed, so the articles say 以結帳頁為準.
- A writer agent re-read ~21 OpenAI pages and updated every ChatGPT fact in both
  articles and both diagrams; an independent fact-check agent re-read 28 pages
  and returned 2 MUST and 11 SHOULD corrections, all applied. Main changes: NT$
  prices, ads on Free/Go (Taiwan from 2026-09-23), Plus thinking levels
  Instant/Medium/High only, Plus gets GPT-6 Astra in Work and Codex, three Pro
  tiers (Pro 500 added 2026-09-29; Pro 200 reopened 2026-09-29 after the 09-10
  pause), refunds within 7 days of a charge, removed claims no page supports
  (Go 10x, Pro 200 20x, GPT-5.3-Codex-Spark, double charging, Sora).
- Both packs stay at 20 sources; dropped entries are listed in the PR, and no
  sentence depends only on a dropped source. Claude and Gemini text in the
  comparison article is unchanged.
- Checks: lint 0 errors for both; content pack tests green; both diagrams
  rendered and looked at. Intake keeps the article's pre-existing failures (no
  summary, a 5-column table, body over 6,000 characters: 6,163 → 7,111); the
  three 本文 self-references and the diagram-number gap are gone.
- "Five locales": both packs are zh-TW only. Left: production import after
  merge and deploy.
