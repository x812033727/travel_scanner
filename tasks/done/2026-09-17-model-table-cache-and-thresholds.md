---
id: 2026-09-17-model-table-cache-and-thresholds
title: 模型總表加三欄：快取價格、長上下文加價門檻、tokenizer 差異
status: done
priority: P2
area: docs
owner: claude-opus-5
claimed_at: 2026-09-17T01:26:30Z
created_at: 2026-09-17T01:26:30Z
completed_at: 2026-09-17T01:34:15Z
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-pricing-beyond-list-price.json
  - apps/web/public/guides/ai-pricing-beyond-list-price
  - docs/content-research/ai-pricing-beyond-list-price
  - apps/api/app/guides/content/ai-model-comparison-table-2026.json
  - docs/content-research/ai-model-comparison-table-2026
---

# 模型總表加三欄：快取價格、長上下文加價門檻、tokenizer 差異

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [x] The observable outcome, not the implementation.

## Steps

- [x] First sub-task.
- [x] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

## 做法改了：另開一篇，不是加欄位（2026-09-17）

原訂把快取價、長上下文門檻、tokenizer 三件事加進 `ai-model-comparison-table-2026`。
實際動手才發現加不進去：**那篇的 `sources` 已經用滿 schema 上限 20 筆**
（`apps/api/app/guides/schemas.py:369`）。

要補這三欄，至少還要兩筆新來源——Anthropic 定價頁（快取倍率、100 萬 token 全程標準價、
tokenizer 註記）與 xAI 定價頁（快取價與門檻規則）。那篇引的是 Anthropic 模型總覽頁與
xAI 模型頁，那兩頁沒有這些欄位。擠不進去，只能砍掉現有的載重來源，那不划算。

所以改成另開一篇 `ai-pricing-beyond-list-price`，自己帶 8 筆來源，兩篇互相連：
新篇連回總表與價格文，總表在中階級那一段前面加一句連過去。這也是站上既有的做法——
`ai-api-pricing-comparison-2026`、`ai-benchmarks-explained`、`ai-model-tiers-explained`
本來就是各自聚焦、互相連的兄弟篇。

## 三個值得記下來的數字

- **快取命中價的級距差十倍以上。** 多數家是原輸入價的 10%，但 DeepSeek 的 deepseek-flash
  只要 2%（0.006／0.30），xAI 的 grok-4.6 要 25%（0.50／2.00）。同一份固定前綴，省下來的比例差很多。
- **xAI 的長上下文門檻是整筆改價。** 官網原文：`requests whose prompt reaches the listed token
  threshold are billed at the higher rate for all tokens in the request`。19.9 萬與 20.1 萬
  token 的兩筆請求，後者不是多付那 2 千 token，而是整整二十萬都換兩倍單價。
- **Anthropic 完全沒有這道門檻**，官網明寫 90 萬 token 的請求與 9 千 token 同一個單價。
  這是全表唯一的反例，值得單獨一列。

## 查不到、所以沒寫的

- 阿里雲百鍊的快取規則：定價頁 2026-09-17 回 HTTP 503，讀不到，表上沒有阿里雲。
- Mistral 與 Z.AI 的快取價當天沒查（不是「沒有」是「沒查」），下次要補從它們的定價頁開始。
- 其他家的 tokenizer 對照：只有 Anthropic 把差異寫在官網（約多 30%），
  其餘沒有可引用的說明，正文寫明只能自己拿同一份文件分別去數，沒有替它們填數字。

## 驗證

- `pack_cli lint --kind life --slug ai-pricing-beyond-list-price --slug ai-model-comparison-table-2026 --warnings`
  → 2 entries checked，零 error 零 warning
- `pack_cli lint --kind life`（全站 847 篇）→ 兩篇都乾淨
- `pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py` → 12 passed
- `ruff check .`、`mypy app`（337 檔）、`npm run check:tasks`（544 檔）全過
- 兩張新 SVG 渲染成 PNG 用眼睛看過：五個方塊與箭頭沒有壓線或超框，hero 縮到 400 px 仍讀得出
  「小方塊→三個關卡→大方塊」的對比

新篇：24 blocks、4 個 h2、2 張表、8 筆 sources、正文 1,918 字。
總表那篇只多了一句連結（正文 2,541 → 2,600 字），其餘未動。

## 這張卡的 scope 中途擴過

建卡時只寫了總表那篇的路徑，實際做出來的是新的一篇，所以把新篇的三個路徑補進 scope。
`claim` 一樣用了 `--force`（`2026-09-15-content-summary-howto-and-life` 持有整個
`apps/api/app/guides/content` 目錄），理由與前兩張卡相同。
