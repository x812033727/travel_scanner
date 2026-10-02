---
id: 2026-09-11-fare-lab-warnings-and-copy
title: 航班票價實驗室三個畫面的多語系與警告代碼
status: in-progress
priority: P3
area: web
owner: claude-opus-5-5-fare-lab
claimed_at: 2026-10-02T16:22:36Z
created_at: 2026-09-11T20:41:05Z
completed_at:
branch: claude/fare-lab-warning-codes
depends_on: []
scope:
  - apps/web/components/airline-fare-lab.tsx
  - apps/web/components/back-to-back-fare-search.tsx
  - apps/web/components/live-back-to-back-search.tsx
  - apps/api/app/crawlers/back_to_back.py
  - apps/api/app/providers/live_back_to_back.py
  - apps/api/tests/test_warning_codes.py
  - apps/api/tests/test_back_to_back_fares.py
  - apps/api/tests/test_live_back_to_back.py
  - apps/web/components/airline-fare-lab.test.tsx
  - apps/web/components/live-back-to-back-search.test.tsx
  - apps/web/lib/fare-lab-copy.ts
  - apps/web/lib/fare-lab-copy.test.ts
  - apps/web/lib/fare-lab-messages
---

# 航班票價實驗室三個畫面的多語系與警告代碼

## Why

`2026-09-11-remaining-api-warning-literals` 把後端所有送給前端的警告都改成代碼，讓讀者自己的
catalog 去說。**只留了三處沒改**，並在 `apps/api/tests/test_warning_codes.py` 的 allow-list
裡寫明理由：

| 位置 | 內容 |
| --- | --- |
| `crawlers/back_to_back.py:810` | 「{currency} 使用七日內的舊匯率估算 TWD。」 |
| `crawlers/back_to_back.py:812` | 「{currency}：目前無法取得 TWD 估算匯率。」 |
| `providers/live_back_to_back.py:274` | 「{role}：沒有可用即時票價」 |

理由是渲染端：`airline-fare-lab.tsx:337`、`back-to-back-fare-search.tsx:651`、
`live-back-to-back-search.tsx:183` 都是 `result.warnings.map((warning) => …{warning})`——
原樣印出，沒有 catalog 可查。送代碼過去只會把識別字印在畫面上，比現在更糟。

而那三個畫面本來就整頁寫死繁中（標題、空狀態、每一張比較卡），所以這不是補三個 key 就好，
是那三頁還沒做多語系。`airline_fares` 是站主刻意關閉的四個功能之一，目前線上回「尚未開放」，
所以不急——但要做就是一起做。

## Definition of done

- [x] 三個畫面改用 message catalog（五語系），不再有寫死的使用者可見中文。
- [x] 三處後端警告改用 `app.warnings.warning_code`，帶 `currency` / `role` 參數。
- [x] 三個渲染端改用 `apps/web/lib/warnings.ts` 的 `translateWarnings`。
- [x] `apps/api/tests/test_warning_codes.py` 的 allow-list 清空，那條 ratchet 變成無例外。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_warning_codes.py -q
cd apps/web && npm run check:i18n && npm run test:web -- airline-fare back-to-back live-back
```

## Notes

- 參數化警告的寫法已經有了：`code?name=value`，值做 percent-encode。
  後端 `app/warnings.py`，前端 `apps/web/lib/warnings.ts`，兩邊都有測試。
- 這三頁的漢字量不小，做之前先估一下 key 數；`lib/itinerary-messages/` 那種功能專屬的側
  catalog 是另一個選項，可以避開多人同時編輯 `messages/*/search.json` 的衝突。

### 2026-10-02 做了什麼（claude-opus-5-5-fare-lab）

- **文案放側 catalog**：`apps/web/lib/fare-lab-messages/<locale>.json` 加 `apps/web/lib/fare-lab-copy.ts`，
  約 200 個鍵。不放 `messages/` 的理由：新 namespace 要改五個 `admin.json`（綁在
  `docs/videos/long-form/review.json` 的檔），塞進 `search.json` 又是大家同時在改的檔。代價是站主不能在
  後台覆寫這三頁的文字，check:i18n 也不看它；鍵的齊全靠 typecheck，佔位符一致靠
  `lib/fare-lab-copy.test.ts`。zh-TW 的句子逐字保留，元件測試與 e2e 不用改字。
- **警告不只三處**。ratchet 掃的是「漢字行的前三行內有 append」，所以 `back_to_back.py` 的「指定日期前後
  N 天內沒有公開快取票價」（270–271 行）也在名單上，清空 allow-list 前一定要改；另外三種 ratchet 沒抓到的也一起改了：
  open-jaw 那句（用 `warnings.insert`，所以 ratchet 現在也看 `insert`／`extend`）、航空公司停用、爬蟲讀頁失敗
  （原本把 `exc.detail` 的中文接在後面）。現在的代碼：`fare_source_paused`、`fare_route_unsupported`、
  `fare_page_blocked`、`fare_page_unavailable`（帶 `reason=<CrawlerError.code>`，畫面不用，留給除錯）、
  `fare_not_cached`／`fare_not_cached_nearest`、`stale_exchange_rate`、`exchange_rate_unavailable`、
  `open_jaw_baseline_only`、`live_fare_failed`、`live_fare_missing`。
- **參數本身也要翻**：`airline=CI`、`role=reverse`、`page=reverse` 由 `fareLabWarnings` 先查 catalog 換成名稱
  再填進句子；即時比較的五張票名稱跟快取比較的四張不同，所以要傳 `"liveRole"` 或 `"ticketRole"`。
- **即時比較的例外**：原本把 provider 的例外字串直接當警告給讀者，現在寫進 log，讀者看到 `live_fare_failed`。
- **登入連結**：一般來回分頁原本用「訊息含 sign in 或登入」判斷要不要放登入連結，改看 `ApiError.status === 401`。
- **沒做的**：比較卡的 `detail` 與一般來回分頁的爬蟲警告（`airlines.py`）還是 API 寫好的繁中句子，
  拆成 `2026-10-02-fare-lab-details-and-crawler-warnings`。
- 驗證：API `ruff`、`mypy app`、`mypy tests`、`pytest` 五個相關檔（56 passed）；新加的 API 測試在舊程式上 8 個紅；
  web `typecheck:web`、`lint:web`、`check:i18n`、vitest 四個檔（31 passed），新的元件斷言在舊元件上紅。
