---
id: 2026-09-14-ai-suffix-keywords-catalogue
title: AI 字尾關鍵字總表與批次 12 名單
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-14T23:06:58Z
created_at: 2026-09-14T23:06:57Z
completed_at: 2026-09-15T00:45:58Z
branch: claude/ai-suffix-keyword-planning-76gn21
depends_on: []
scope:
  - docs/ai-suffix-keywords.md
  - docs/life-ai-series.md
  - docs/life-ai-series-brief.md
---

# AI 字尾關鍵字總表與批次 12 名單

## Why

台灣使用者找 AI 工具常把 AI 放字尾打：「翻譯 AI」「簡報 AI」「去背 AI」。生活分享 573 篇 life 文章的標題與描述
幾乎全用字首型（「AI 翻譯」），字尾型只在「生成式 AI」「開源 AI」這幾個概念詞裡出現。要有一份對照表把字尾詞
對到文章：已寫的補描述與導言、總表排了還沒寫的由該批次帶入、哪裡都沒有的排成批次 12，撰稿指令也要知道
拿到字尾詞該怎麼寫。沒有搜尋量資料，候選詞是編輯判斷，文件要寫明並留欄位給 Search Console 回填。

## Definition of done

- [x] `docs/ai-suffix-keywords.md`：目的、資料來源聲明（無搜尋量）、寫法規則、關鍵字→slug 對照總表（狀態：已寫／已寫（系列外）／待批次 NN／批次 12）、批次 12 名單、不做的詞、驗證、經驗記錄。
- [x] `docs/life-ai-series.md`：H1 篇數 249→260、政策段指向總表、「批次與任務票」表加第 12 列（並修掉表頭下那個空行）、文末加批次 12 的 7 欄表（250–260）。
- [x] `docs/life-ai-series-brief.md` 第 4 節：指派給了字尾關鍵字時的寫法（標題開頭、description 第一句、導言各一次，h2 不重複）。
- [x] 批次 12 的 11 個 slug 不存在於內容包、總表與 two-site catalogue；`guides-pack lint --catalogue` 多出 11 個 `catalogue_missing_pack`、沒有 error。

## Steps

- [x] 寫總表與批次 12 名單。
- [x] 改 `docs/life-ai-series.md` 與 brief。
- [x] 立票：`2026-09-14-ai-suffix-keywords-backfill`（61 篇補強）、`2026-09-14-life-ai-batch-12-suffix-keywords`（新文章）、`2026-09-14-sitemap-split-before-1000-rows`（926 列已過警戒線）。

## How to verify

```bash
npm run check:tasks
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --catalogue ../../docs/life-ai-series.md
```

lint 基準（改前，exit 0）：120 `catalogue_missing_pack`、`sitemap_budget` 886；同日批次 06、07 併入 main 後基準變成 80 與 926。改後應是 91 個 `catalogue_missing_pack`，其餘不變。

## Notes

- 不改既有標題：h1、站內 `link` 文字與兩個系列目錄（`guide-series.json`、`series_data/claude-code.json`）都抄自標題，沒有工具會同步。
- 257–260（算命、投資、法律、健康）是敏感／YMYL 題，先列著等站主拍板；不寫就從兩份總表刪掉。
- 「旅遊 AI」一組直接對到站的核心產品，總表標 P1；批次 11 的 `ai-travel-planning-tools` 指派要加必寫「站內規劃器入口」。

## Outcome (2026-09-14)

- `docs/ai-suffix-keywords.md`：五組共 90 個字尾詞對到 slug，狀態四種（已寫／已寫（系列外）／待批次 NN／批次 12），
  含資料來源聲明、寫法規則、檢查腳本、批次 12 名單與不做的詞。
- `docs/life-ai-series.md` 260 篇、批次 12 表（250–260）與第 12 列；brief 第 4 節加字尾詞規則。
- `guides-pack lint --catalogue`：`catalogue_missing_pack` 從 80（批次 06、07 併入後）變 91，沒有 error。
- 立了 `2026-09-14-ai-suffix-keywords-backfill`（本次一起做完）、`2026-09-14-life-ai-batch-12-suffix-keywords`、`2026-09-14-sitemap-split-before-1000-rows`。
