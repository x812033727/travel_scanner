---
id: 2026-09-13-adsense-admin-config
title: AdSense 後台設定與匿名公開設定端點（預設關閉）
status: done
priority: P3
area: api
owner: claude-opus-5
claimed_at: 2026-09-13T08:00:32Z
created_at: 2026-09-13T05:16:04Z
completed_at: 2026-09-13T08:06:13Z
branch: claude/google-adsense-integration-plan-650u03
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

- [x] `PROVIDER_DEFINITIONS`（`apps/api/app/admin/service.py:108` 起）新增獨立的 `adsense` provider：
      `enabled_field` 是 `adsense_enabled`；設定欄位有 `adsense_publisher_id`、`adsense_in_article_slot_id`、
      `adsense_end_slot_id`、`adsense_non_personalized_only`（預設 true）。全部是明文 config，不是 secret，
      因為這些值本來就公開寫在頁面上。
- [x] 驗證：`ca-pub-\d{16}`、slot 是 10 位數字、布林欄位加進 `boolean_fields`（`service.py:1246`），格式不對回 422。
- [x] 匿名端點（例如 `GET /api/v1/ads/config`）比照 `GET /travel-services/stay22-script-config`：
      匿名、`Cache-Control: no-store`、收到 `DNT: 1` 或 `Sec-GPC: 1` 就回「關閉」、
      只回有效狀態（開啟**且**ID 驗證通過）與驗證過的 ID。
- [x] `.env.example` 與 `config.py` 預設全關；沒有設定時端點回關閉。
- [x] 後台「設定」頁出現 AdSense 卡片，欄位標籤放 `admin.providerFields.*`（五語系）。

## Steps

- [x] 在本檔 Notes 記下 D1–D3 的答案與發布商 ID。
- [x] `config.py` 欄位、`PROVIDER_DEFINITIONS`、驗證、`_configured` 的分支。
- [x] 把 `adsense` 加進 `LOCAL_ONLY_PROVIDERS`（`service.py:976`）。
- [x] 新模組 `apps/api/app/ads/`（router＋service），在 `main.py` 掛 router。
- [x] 後台面板的分類（`admin-settings-panel.tsx:97-132`）與欄位中繼資料，五語系標籤。
- [x] 測試：驗證、DNT／GPC、預設關、provider 分類。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_ads_config.py tests/test_admin_readiness.py -q
cd apps/api && uv run ruff check . && uv run mypy app
npm run lint:web && npm run check:i18n && npm run typecheck:web
```

本機起 API 後：`curl -s localhost:8000/api/v1/ads/config` 回關閉；後台開啟並填 ID 後回開啟；
帶 `-H "Sec-GPC: 1"` 回關閉。

## Notes

- 站主的決定（`docs/adsense-feasibility.md` 第六節）：D1 只投非個人化廣告、不裝 CMP；
  D2 程式碼先就緒且預設關閉，審核通過後從後台開啟；D3 文中 1 個版位。
  發布商 ID `ca-pub-4140966684432854`（站主提供，公開識別碼）。
- **兩處刻意偏離原本的規格**：
  - 不做 `adsense_end_slot_id`。D3 只要 1 個文中版位，欄位改叫 `adsense_slot_id`；
    要加文末版位再開新票。
  - 不做 `adsense_non_personalized_only` 開關。D1 已定案只投非個人化廣告，而切成個人化在
    EEA／英國／瑞士需要認證 CMP 並且要改寫隱私政策——做成後台開關等於留一個一按就違反政策的
    按鈕。改成在載入器裡寫死（`components/ads/adsense-loader.tsx` 的 `requestNonPersonalizedAds`），
    要改必須改程式碼並同步更新政策。
- `_configured` 的 `adsense` 分支直接呼叫 `app.ads.service.adsense_config`，
  所以後台卡片的燈號跟讀者實際會拿到的答案永遠一致：開關開了但 ID 沒填，卡片說的是
  「已開啟但缺少…，讀者不會看到版位」，不是綠燈。

- **不要塞進既有的 `analytics` provider。** 它的 `enabled_field` 是 `analytics_enabled`（`service.py:130-144`），
  關掉流量分析會連帶關掉廣告，而且兩者的隱私條件不一樣。
- 新增 provider 有三個坑：
  - `_configured`（`service.py:590` 起）沒有對應分支時會掉到最後的 NAVITIME 判斷（約 `:920`），卡片會顯示 NAVITIME 的狀態。
  - `tests/test_admin_readiness.py:21-23` 要求每個 provider 都歸類到 `CONNECTION_TESTED_PROVIDERS` 或 `LOCAL_ONLY_PROVIDERS`。
  - 新布林欄位沒加進 `boolean_fields`，就不會被型別檢查。
- `GET /runtime/public-config` 需要登入，文章讀者拿不到，不能用。
- web 端怎麼讀、要不要輸出版位，是 `2026-09-13-adsense-article-slot` 的事，這張不碰 `apps/web/lib` 或文章元件。
