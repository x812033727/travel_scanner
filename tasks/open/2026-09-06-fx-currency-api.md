---
id: 2026-09-06-fx-currency-api
title: 匯率改由 Currency-api 供應，Frankfurter 退為備援；行程報價與記帳顯示換算
status: review
priority: P2
area: api
owner: claude-fable-5.1
claimed_at: 2026-09-06T06:43:11Z
created_at: 2026-09-06T06:28:55Z
completed_at:
branch: claude/fx-currency-api
depends_on: []
scope:
  - apps/api/app/crawlers/fx.py
  - apps/api/app/fx
  - apps/api/app/main.py
  - apps/api/app/config.py
  - apps/api/app/trips/pricing.py
  - apps/api/app/trips/router.py
  - apps/api/tests/test_back_to_back_fares.py
  - apps/api/tests/test_trip_pricing.py
  - apps/api/tests/test_fx_rates.py
  - apps/web/lib/currency.ts
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
  - .env.example
---

# 匯率改由 Currency-api 供應，Frankfurter 退為備援；行程報價與記帳顯示換算

## Why

站內唯一的匯率來源是 Frankfurter（歐洲央行），只在外站始發倒買票換算 TWD 時用到；行程報價
遇到外幣只列在 `unsummed_currencies`，前端沒有任何地方顯示，記帳面板也沒有匯率參考。
owner 2026-09-06 從 public-apis 清單挑了 Currency-api（fawazahmed0）：每日更新、339 種幣別
含 TWD、走 jsDelivr 與 pages.dev 兩個 CDN、免金鑰無限制；歐洲央行週末不更新，它照常更新。

## Definition of done

- [x] `FxRateProvider.rate(base, quote)` 支援任意幣別對；來源順序 Currency-api（jsDelivr）→
      Currency-api（pages.dev）→ Frankfurter；三個都失敗才用 stale 快取或報錯。
- [x] 外站倒買票的 `rate_to_twd` 行為不變。
- [x] 行程報價：外幣報價有匯率時另算 `converted_total` 與每筆 `converted_amount`，並附
      `conversions`（幣別、匯率、日期、來源）；`quoted_total` 仍只算同幣別，拿不到匯率的幣別
      留在 `unsummed_currencies`。
- [x] `GET /api/v1/fx/rate?base=JPY&quote=TWD` 給前端用，登入後每小時 120 次，查不到回 404。
- [x] 記帳面板：帳本幣別與目的地幣別不同時顯示「今日匯率 1 JPY ≈ 0.2028 TWD（日期）」，
      同幣別不打 API。五語系文案在 `trips.json` 的 `costRate`。
- [x] `apps/api` ruff／mypy／pytest 與 `apps/web` lint／typecheck／i18n／vitest 通過。

## Steps

- [x] `crawlers/fx.py`：來源鏈、兩個解析器、`rate()`；快取 key 改為 `fx:rates:{BASE}:{QUOTE}`。
- [x] `config.py`／`.env.example`：`fx_currency_api_base_url`、`fx_currency_api_fallback_url`。
- [x] `trips/pricing.py`：`trip_pricing(rates=...)` 與 `trip_pricing_with_rates()`；
      `serialize_trip` 只在有外幣報價時才查匯率。
- [x] `fx/router.py` + `main.py`：端點與註冊。
- [x] `lib/currency.ts`：`countryCurrency`；`trip-cost-panel.tsx`：匯率提示。
- [x] 測試：`test_back_to_back_fares.py` 改成 Currency-api 格式並補 fallback；`test_trip_pricing.py`
      補換算；`test_fx_rates.py`；`trip-cost-panel.test.tsx`。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_back_to_back_fares.py tests/test_trip_pricing.py tests/test_fx_rates.py
npm run lint:web && CI=1 npm run check:i18n && npm run typecheck:web && cd apps/web && npx vitest run components/trip-cost-panel.test.tsx
```

線上：開一趟日本行程的旅程工具，記帳幣別選 TWD，幣別欄下面會出現今日匯率；
`curl -b <cookie> https://mokaair.com/api/v1/fx/rate?base=JPY&quote=TWD` 回 `source_url` 是 jsDelivr。

## Notes

- 生產 `.env` 的 `FX_RATE_BASE_URL` 仍指向 Frankfurter，那只是第三順位，不用改。
- Currency-api 一天更新一次，快取 24 小時、stale 保留 7 天，跟原本一致。
- 報價換算的 `converted_total` 前端還沒顯示：`trip.pricing` 目前沒有任何元件在畫，
  之後做旅程總價卡片時直接拿來用。
