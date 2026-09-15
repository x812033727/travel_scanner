---
id: 2026-09-14-life-finance-series-hub
title: 財經教學中心：系列目錄與 hub
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-14T11:45:57Z
completed_at:
branch:
depends_on:
  - 2026-09-14-life-finance-batch-01
  - 2026-09-14-life-finance-batch-02
  - 2026-09-14-life-finance-batch-03
  - 2026-09-14-life-finance-batch-04
  - 2026-09-14-life-finance-batch-05
  - 2026-09-14-life-finance-batch-06
scope:
  - apps/api/app/guides/series_data
  - apps/api/tests/test_guide_series.py
---

# 財經教學中心：系列目錄與 hub

## Why

站主要的是「財經文章**與教學**」。文章由六張批次票產出，教學中心（hub）是把其中操作型的那些
串成有先修順序與學習路線的入口——就像 `claude-code-tutorials`（60 課）和 Gemini 系列（50 篇）。

**這件事不能和內容票一起做**，所以獨立成票，`depends_on` 六個批次：

1. `series.Catalogue.consistent` 要求編號從 1 連續、每個 `prerequisites`／`related` 都指到
   系列內存在的條目、hub 本身不在條目裡。為 120 篇還沒寫的文章先寫 catalogue，
   等於在寫作定案前凍結編號與標題；AI 系列的經驗記錄裡標題中途改過兩次。
2. `public_series` 在 hub 文章發布前一律回 `None`，所以今天寫的 catalogue 什麼都做不到。
3. 機制還沒選定（見下）。
4. `series_data/` 與 `test_guide_series.py` 現在都在
   `tasks/open/2026-09-14-claude-code-tutorial-center.md` 的 scope 裡。

## Definition of done

- [ ] 選定機制並寫下理由（見 Steps）。
- [ ] hub 文章 `personal-finance-tutorials` 的內容包（或所選機制對應的檔案）落地。
- [ ] catalogue 通過 `Catalogue.consistent`：編號連續、參照都解析得出來、hub 不在條目裡。
- [ ] **`apps/api/tests/test_guide_series.py` 改成不再假設只有一個 catalogue**（見下）。
- [ ] `GET /guides/series/personal-finance-tutorials` 在 hub 發布後回得出內容。

## Steps

### 1. 選機制

站上有兩套，各有前例：

| 機制 | 檔案 | 前例 |
| --- | --- | --- |
| API 端 | `apps/api/app/guides/series_data/<slug>.json` ＋ `app/guides/series.py`，路由 `GET /guides/series/{slug}` | Claude Code 教學中心，60 課、10 群組、5 條學習路線 |
| Web 端 | `apps/web/lib/guide-series.json` ＋ `apps/web/lib/gemini-series.ts` | Gemini 系列，50 篇，前端自帶搜尋 |

- [ ] 建議走 **API 端**：財經要的是學習路線與先修順序（「剛開始工作」「準備報稅」「第一次投資」），
      不是 Gemini 那種純搜尋。但這是一個決定，做的時候重新評估，理由寫進票。

### 2. 會壞掉的那個測試（重點）

`apps/api/tests/test_guide_series.py` 的 `test_catalogue_is_complete_and_references_are_valid`
第一行是：

```python
(catalogue,) = catalogues()
```

**解構成「剛好一個」。** 在 `series_data/` 放第二個 JSON 會讓它直接 `ValueError`。

- [ ] 改成依 `slug` 取出要斷言的那一個，並為財經 catalogue 加對應的斷言。

### 3. catalogue 的內容

- [ ] 進 catalogue 的是**操作型**那些（記帳 App、開戶、載具設定、報稅 App、下單、零股、
      網路投保、W-8BEN、聯徵查詢…），約 30–40 篇，**不是全部 120 篇**。
      觀念型與制度說明型的留在一般列表。
- [ ] 群組按批次切；學習路線至少三條：「剛開始工作」「準備報稅」「第一次投資」。
- [ ] 條目編號在這張票做的時候，從總表的 1–120 挑出實際要收的那些重新連續編號。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guide_series.py tests/test_gemini_series.py -q
cd apps/api && uv run ruff check . && uv run mypy app
```

## Notes

- hub slug 預定 `personal-finance-tutorials`，已在 `docs/life-finance-series.md` 保留。
- 開工前確認 `2026-09-14-claude-code-tutorial-center` 已經合併，否則 scope 卡住。
