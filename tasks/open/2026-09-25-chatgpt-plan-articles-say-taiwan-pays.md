---
id: 2026-09-25-chatgpt-plan-articles-say-taiwan-pays
title: ChatGPT 方案文章還寫台灣以美元計價
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-25T06:01:29Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/chatgpt-plans-plus-pro-2026.json
  - apps/api/app/guides/content/ai-free-vs-paid-plans-2026.json
  - apps/web/public/guides/chatgpt-plans-plus-pro-2026
---

# ChatGPT 方案文章還寫台灣以美元計價

## Why

2026-09-25 查核影片〈ChatGPT 開始有廣告了〉時，未登入從台灣開 chatgpt.com/pricing，已直接顯示新台幣含稅價：Go 每月 NT$270、Plus 每月 NT$690（頁面載入的價格資料標 TWD、含 5% 稅）。站內 `chatgpt-plans-plus-pro-2026` 與 `ai-free-vs-paid-plans-2026` 仍寫台灣網頁結帳以美元計價另加 5% 營業稅；`chatgpt-plans-plus-pro-2026` 的方案階梯圖（`apps/web/public/guides/chatgpt-plans-plus-pro-2026/diagram-1.svg`）還列了舊的 Plus 型號名、只標免費版有廣告。

## Definition of done

- [ ] 兩篇文章的台灣價格改成官方新台幣含稅價，附網址與查證日；Go 標明「可能有廣告」、Plus 以上沒有。
- [ ] 方案階梯圖重畫（型號、廣告標示、幣別）。
- [ ] 五語系一致（skill `content-pipeline`）。

## Steps

- [ ] 重查 chatgpt.com/pricing（台灣、未登入）與 OpenAI Help Center 的方案頁。
- [ ] 改寫、重畫圖、ingest、部署後匯入。

## How to verify

正式站兩篇文章與圖都顯示新台幣價格與新的查證日。

## Notes

- 影片那邊已改用官方新台幣價，並把引用這張圖的場景調整過；圖重畫後影片可以再引用。
