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

### 2026-10-06：提前做了一次（票 2026-10-05-multi-vendor-ai-price-pages-late）

各家換代（GPT-6 家族、Claude 5.5、grok-4.7）讓這一輪提前。做法、讀數與網址都在
`docs/content-research/ai-model-comparison-table-2026/notes.md` 的 2026-10-06 段落，重點：

- `sources` 現在是 20 筆（不是上面寫的 18 筆），10/06 全部重開，`checked_on` 都是 2026-10-06。
  換掉兩筆：Opus 5 發布頁 → Opus 5.5 發布頁，grok-4.6 發布頁 → grok-4.7 發布頁；Mistral 改成轉址後的
  `docs.mistral.ai/inference/pricing`。
- 分級規則寫進 notes.md：跟各家自己的命名走，被標 legacy 或上一代的型號出表。
- 分數欄只留在旗艦表，中階與輕量兩張表拿掉這一欄（9/16 版那兩張表的「官網未公布」有幾格其實錯了）。
- 「官網有沒有列跑分」表改成 GPQA Diamond／Terminal-Bench 4.0 兩欄的對照：這兩項各有四家列，
  沒有一項六家都有。Anthropic 現在有數字、DeepSeek 的更新紀錄有 GPQA、Qwen 的測試條件寫法更正。
- 更正兩筆：MiniMax-M3 上下文是 100 萬（51.2 萬是計價分段），grok-4.7 寫「無輸出上限」。
- 開放權重表十二列的授權與參數用 HF API 重讀，全部不變；各家 9/16 之後沒有新的通用語言模型權重。
- `reingest.sh` 不再需要拿掉 `ai-plans`；`build_pack.py` 會把圖解 `<desc>` 帶進 `image.description`。

這張票照舊開著：下一次是 2026-12 或 2027-01，必改的是 `gemini-3.8-flash`（0.75／3.75 標到
2026-12-31，之後 1.50／7.50），以及 `gpt-5.6-sol` 的促銷價（至少到 2026-11-21）是否還在定價頁上。

同一天的獨立查核第二輪再補兩件（讀數在 notes.md 的「獨立查核第二輪的更正」）：

- Mistral Large 4（10/06 公開預覽）的 0.68／2.09 是上市兩週的五折價，更新紀錄寫「Launch pricing: 50% off for
  2 weeks.」，原價 1.36／4.18；大約 10/20 結束。旗艦表下面那段與 `ai-api-pricing-comparison-2026` 第 15 段、
  第 22 段的提醒框都寫了。下次重查時看 Large 4 是否已正式上線、`mistral-large-latest` 是否改指 Large 4，
  是的話旗艦表那一列要換。
- `sources` 仍是 20 筆，但 Meta Muse Glimmer 30B 權重頁換成 Mistral 更新紀錄；上下文與最大輸出改在旗艦表
  caption 寫明「在定價頁沒寫的，照各家的模型說明頁」，模型頁網址都在 notes.md。
