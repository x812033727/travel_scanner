---
id: 2026-09-16-model-table-quarterly-recheck
title: 模型總表定期重查：價格與上下文每季對一次官網
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-16T13:32:10Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-model-comparison-table-2026.json
---
# 模型總表定期重查：價格與上下文每季對一次官網

## Why

`ai-model-comparison-table-2026` 是一篇資料表，它的三張分級表寫的是 2026-09-16 當天
十家官網的價格與規格。這種內容會過期，而且過期的方式不明顯：頁面看起來一樣，數字已經不對。

當天就有兩個會在幾個月內動的例子：

- `gemini-3.8-flash` 的 0.75 美元與 3.75 美元，官網標到 2026-12-31，之後回到 1.50 與 7.50。
  **這一筆有明確到期日，2027-01 那次重查一定要改。**
- `deepseek-v4-pro` 與 `deepseek-flash` 用尖峰價，DeepSeek 隨時可以調整尖峰時段的定義。

另外 `ai-model-release-timeline-2026` 記錄 2026 年 1 到 9 月各家發了三十次以上的模型；
以這個節奏，一季不看就會有整列該換掉。

刻意不設 `valid_until`：同類的四篇（`ai-api-pricing-comparison-2026`、`ai-benchmarks-explained`、
`ai-model-tiers-explained`、`ai-model-release-timeline-2026`）都是 `null`，日期寫在表格 caption 裡，
過期用這張卡處理而不是讓文章自己消失。

## Definition of done

- [ ] 每季重跑一次，`sources` 的 18 筆逐一重開，`checked_on` 全部換成當次日期。
- [ ] 三張分級表的價格、上下文與最大輸出逐格對過；官網改欄位就跟著改，查不到就寫「官網未公布」。
- [ ] 第四張「官網有沒有列跑分」表也要重看：這一欄是本篇的論點，某家開始公布分數就要改。
- [ ] 每次更新後 `notes.md` 追加一段當次的查證記錄，不要覆蓋上一次的。

## Steps

- [ ] 下次重查：2026-12 或 2027-01（`gemini-3.8-flash` 的促銷價到 2026-12-31）。
- [ ] 用 `docs/content-research/ai-model-comparison-table-2026/build_pack.py` 改數字再重跑，
      不要手改 `apps/api/app/guides/content/` 底下的 JSON——那份是產出的。
- [ ] 順手看一下有沒有新廠商該進表，或表上哪一家已經退場。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind life --slug ai-model-comparison-table-2026 --warnings
uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py -q
```

## Notes

Meta Llama 2026-09-16 當天查不到現行版本（llama.com 轉 developer.meta.com、模型頁 404、
官方 blog 沒提），所以沒有列進表。下次重查時再試一次，查得到就補一列。
