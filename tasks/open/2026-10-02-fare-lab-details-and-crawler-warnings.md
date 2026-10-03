---
id: 2026-10-02-fare-lab-details-and-crawler-warnings
title: Fare lab comparison details and crawler warnings still reach readers as Chinese
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-02T17:06:47Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/crawlers/airlines.py
  - apps/api/app/crawlers/back_to_back.py
  - apps/api/app/providers/live_back_to_back.py
  - apps/api/tests/test_airline_crawlers.py
  - apps/api/tests/test_back_to_back_fares.py
  - apps/api/tests/test_live_back_to_back.py
  - apps/web/components/airline-fare-lab.tsx
  - apps/web/components/back-to-back-fare-search.tsx
  - apps/web/components/live-back-to-back-search.tsx
  - apps/web/lib/fare-lab-messages
---

# Fare lab comparison details and crawler warnings still reach readers as Chinese

## Why

`2026-09-11-fare-lab-warnings-and-copy` 把航班票價實驗室三個畫面改成五語系目錄
（`apps/web/lib/fare-lab-messages/`），倒買與即時倒買兩支 API 的 `warnings` 也都改成代碼。
但還有三種 API 寫好的繁中句子，原樣出現在每個語系的畫面上：

1. **比較卡的 `detail`**。`BackToBackFareService._comparison` 與 `search` 寫的
   「混搭航空公司的外站兩段票估算較省。」「…缺少第一趟一般票的公開快取票價，因此無法組成完整比較；
   這不是 0% 節省。」，以及 `LiveBackToBackService.search` 的「所有必要票價均來自同一次使用者主動即時比較。」。
   兩個元件都是 `<p>{comparison.detail}</p>`。
2. **一般來回分頁的警告**。`app/crawlers/airlines.py` 的 `AirlineFareCrawlerService` 寫
   `f"{adapter.name}：{detail}"`，`detail` 是 `CrawlerError.detail` 或 `disabled_reason`（繁中）。
   `test_warning_codes.py` 的 ratchet 抓不到它，因為漢字不在 append 那一行。
3. **來源卡的 `detail`**（`AirlineCrawlerSource.detail`）。目前畫面沒有顯示它，若之後要顯示，同樣要先改。

## Definition of done

- [ ] 英文、日文、韓文讀者在三個分頁都看不到 API 寫的中文句子（比較說明與警告）。
- [ ] `airlines.py` 的警告用 `app.warnings.warning_code`，airline 與失敗原因當參數；渲染端已經用
      `fareLabWarnings`，只要在 `lib/fare-lab-messages/*.json` 補 `warning.*` 鍵。
- [ ] 比較說明改成代碼（例如沿用 warning 的 `code?name=value` 形狀放進 `detail`，或新增欄位），
      缺哪幾張票用 role 值列出，讓前端用 `ticketRole.*` 說出名稱。

## Steps

- [ ] 先 grep 有沒有別的讀者讀 `detail`（2026-10-02 時只有倒買與即時倒買兩個元件顯示它；
      兩支 router 讀 `comparisons` 只為了決定扣不扣次，不看 `detail`）。
- [ ] 決定 `detail` 的形狀，舊的冪等重播結果仍是中文句子，前端要讓非代碼字串原樣通過。
- [ ] 補五語系文案與 `lib/fare-lab-copy.test.ts` 的案例。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_back_to_back_fares.py tests/test_live_back_to_back.py tests/test_airline_crawlers.py tests/test_warning_codes.py -q
cd apps/web && npx vitest run lib/fare-lab-copy.test.ts components/airline-fare-lab.test.tsx components/live-back-to-back-search.test.tsx
```

## Notes

- 從 `2026-09-11-fare-lab-warnings-and-copy` 拆出來：那張票的範圍是畫面上寫死的中文與 ratchet 抓到的警告。
- `airline_fares` 是站主刻意關閉的功能之一，不急。
