---
id: 2026-09-13-adsense-admin-config
title: AdSense 後台設定與匿名公開設定端點（預設關閉）
status: blocked
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-13T05:16:04Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/ads
  - apps/api/app/main.py
  - apps/api/app/admin/service.py
  - apps/api/app/config.py
  - apps/api/tests/test_ads_config.py
  - apps/api/tests/test_admin_readiness.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - .env.example
---

# AdSense 後台設定與匿名公開設定端點（預設關閉）

## Why

評估全文在 `docs/adsense-feasibility.md`。要在文章頁放 AdSense，站主需要從後台控制幾件事，而且不用重新部署：

- 開關
- 發布商 ID（`ca-pub-` 加 16 位數字）
- 1–2 個廣告單元的 slot ID
- 是否只放非個人化廣告

文章頁也要能**匿名**讀到「現在有沒有開、ID 是什麼」。

**先別動手**：這張票等站主決定評估文件第六節的 D1–D3（隱私立場、申請時機、版位），
而且要先有 AdSense 帳號拿到發布商 ID。沒有這些，做出來的只是一個沒人用的開關。

## Definition of done

- [ ] `PROVIDER_DEFINITIONS`（`apps/api/app/admin/service.py:108` 起）新增獨立的 `adsense` provider：
      `enabled_field` 是 `adsense_enabled`；設定欄位有 `adsense_publisher_id`、`adsense_in_article_slot_id`、
      `adsense_end_slot_id`、`adsense_non_personalized_only`（預設 true）。全部是明文 config，不是 secret，
      因為這些值本來就公開寫在頁面上。
- [ ] 驗證：`ca-pub-\d{16}`、slot 是 10 位數字、布林欄位加進 `boolean_fields`（`service.py:1246`），格式不對回 422。
- [ ] 匿名端點（例如 `GET /api/v1/ads/config`）比照 `GET /travel-services/stay22-script-config`：
      匿名、`Cache-Control: no-store`、收到 `DNT: 1` 或 `Sec-GPC: 1` 就回「關閉」、
      只回有效狀態（開啟**且**ID 驗證通過）與驗證過的 ID。
- [ ] `.env.example` 與 `config.py` 預設全關；沒有設定時端點回關閉。
- [ ] 後台「設定」頁出現 AdSense 卡片，欄位標籤放 `admin.providerFields.*`（五語系）。

## Steps

- [ ] 在本檔 Notes 記下 D1–D3 的答案與發布商 ID。
- [ ] `config.py` 欄位、`PROVIDER_DEFINITIONS`、驗證、`_configured` 的分支。
- [ ] 把 `adsense` 加進 `LOCAL_ONLY_PROVIDERS`（`service.py:976`）。
- [ ] 新模組 `apps/api/app/ads/`（router＋service），在 `main.py` 掛 router。
- [ ] 後台面板的分類（`admin-settings-panel.tsx:97-132`）與欄位中繼資料，五語系標籤。
- [ ] 測試：驗證、DNT／GPC、預設關、provider 分類。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_ads_config.py tests/test_admin_readiness.py -q
cd apps/api && uv run ruff check . && uv run mypy app
npm run lint:web && npm run check:i18n && npm run typecheck:web
```

本機起 API 後：`curl -s localhost:8000/api/v1/ads/config` 回關閉；後台開啟並填 ID 後回開啟；
帶 `-H "Sec-GPC: 1"` 回關閉。

## Notes

- **不要塞進既有的 `analytics` provider。** 它的 `enabled_field` 是 `analytics_enabled`（`service.py:130-144`），
  關掉流量分析會連帶關掉廣告，而且兩者的隱私條件不一樣。
- 新增 provider 有三個坑：
  - `_configured`（`service.py:590` 起）沒有對應分支時會掉到最後的 NAVITIME 判斷（約 `:920`），卡片會顯示 NAVITIME 的狀態。
  - `tests/test_admin_readiness.py:21-23` 要求每個 provider 都歸類到 `CONNECTION_TESTED_PROVIDERS` 或 `LOCAL_ONLY_PROVIDERS`。
  - 新布林欄位沒加進 `boolean_fields`，就不會被型別檢查。
- `GET /runtime/public-config` 需要登入，文章讀者拿不到，不能用。
- web 端怎麼讀、要不要輸出版位，是 `2026-09-13-adsense-article-slot` 的事，這張不碰 `apps/web/lib` 或文章元件。
