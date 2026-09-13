---
id: 2026-09-13-adsense-cmp-consent
title: AdSense certified CMP and consent-gated personalised ads
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-13T08:53:12Z
created_at: 2026-09-13T08:52:35Z
completed_at: 2026-09-13T09:09:49Z
branch: claude/google-adsense-integration-plan-650u03
depends_on: []
scope:
  - apps/api/app/config.py
  - apps/api/app/ads
  - apps/api/app/admin/service.py
  - apps/api/tests/test_ads_config.py
  - apps/api/app/site_pages/drafts
  - apps/api/tests/test_site_pages_drafts.py
  - apps/web/lib/adsense.ts
  - apps/web/lib/adsense.test.ts
  - apps/web/components/ads
  - apps/web/app/[locale]/layout.tsx
  - apps/web/app/(ads-public)
  - apps/web/e2e/guides-adsense.spec.ts
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - docs/adsense-feasibility.md
  - docs/travel-guides.md
  - docs/privacy-data-map.md
  - .env.example
---

# AdSense certified CMP and consent-gated personalised ads

## Why

站主在 `2026-09-13-adsense-article-slot` 落地後改了主意：要加 CMP。
這推翻了評估文件第六節的 D1（原本是「只投非個人化廣告、不裝 CMP」）。

新的決定：

- 用 **Google 的「隱私權與訊息」**（Funding Choices，Google 自家的認證 CMP，已整合 IAB TCF）。
  訊息由 AdSense 後台設定、由廣告標籤自己載入，不需要再裝一支第三方腳本。
- 同意訊息**只對 EEA／英國／瑞士**顯示（Google 的預設，也是它唯一強制的範圍）。
  台灣讀者——目前 30 篇 zh-TW 文章的主要來源——不會看到彈窗。
- **DNT／GPC 的做法不變**：廣告完全不載入，連同意訊息都不會出現。
  這跟站上每一支第三方腳本一致，也是 GPC 在部分法域的法律意義。

程式面要改的只有三件事，其餘都在 AdSense 後台。

## Definition of done

- [x] 後台多一個 `adsense_cmp_enabled` 布林欄位（預設 false），意思是「AdSense 後台已經啟用
      Google 認證的同意訊息」。這是站主陳述的事實，行為由程式推導。
- [x] 載入器**只在 `adsense_cmp_enabled` 是 false 時**才設 `requestNonPersonalizedAds = 1`。
      有 CMP 時強制非個人化等於蓋掉同意結果，CMP 就白裝了。
- [x] 五語系隱私權政策改寫：現在那段寫「本站沒有同意橫幅」，加了 CMP 之後這句話是錯的。
      新文字要同時對「CMP 關閉」與「CMP 開啟」兩種狀態都成立。
- [x] `docs/adsense-feasibility.md` 第六節的 D1 改成新答案，舊答案保留備查。
- [x] `docs/privacy-data-map.md`「整個 repo 沒有 gtag consent update」那段要補：CMP 開啟後
      Google 的同意訊息會自己更新 Consent Mode。

## Steps

- [x] `config.py`、`PROVIDER_DEFINITIONS`、`boolean_fields`、`_configured` 的文案。
- [x] `app/ads/service.py` 的回應多一個 `cmp_enabled`。
- [x] `lib/adsense.ts` 的型別與驗證、載入器、版位元件。
- [x] 五語系隱私權文字與後台欄位標籤。
- [x] 測試：API、`lib/adsense.test.ts`、e2e 兩種狀態。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_ads_config.py tests/test_site_pages_drafts.py -q
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
cd apps/web && npm run build && PLAYWRIGHT_SERVE_BUILD=true npx playwright test e2e/guides-adsense.spec.ts
```

## Notes

- 實作後的行為摘要：`adsense_cmp_enabled` 關閉（預設）＝ 今天的行為，載入器設
  `requestNonPersonalizedAds = 1`；開啟＝ 不設那個旗標，由 Google 的同意訊息結果決定。
  旗標是站主陳述「AdSense 後台已發布認證同意訊息」這個事實，不是行為開關。
- `validAdsenseConfig` 現在要求 `cmp_enabled` 必須是布林值。舊版 API 少了這個欄位時
  會被判為無效而整個關閉——比起讓 `undefined` 靜靜地被當成「沒有 CMP」，寧可關掉。
- **站主還要在 AdSense 後台做完**才把開關打開：在「隱私權與訊息」建立並發布 GDPR 訊息、
  確認顯示區域是 EEA／英國／瑞士、檢視廣告夥伴清單。後台沒發布就打開開關，
  等於在沒有 CMP 的情況下投個人化廣告，這正是政策禁止的。

- **CSP 不用改。** CMP 的腳本（`fundingchoicesmessages.google.com`）是由廣告標籤載入的，
  在 `'strict-dynamic'` 下自動繼承信任；而且文章路由開啟廣告時 `script-src`／`frame-src`／
  `connect-src` 已經放寬到 `https:`。
- **`analytics-provider.tsx` 不動。** Consent Mode 的四項預設維持 denied，那正是 Consent Mode
  預設值該有的樣子；CMP 會在讀者做出選擇後自己呼叫 `gtag("consent","update")`。
  這支檔案也不在本票 scope 內。
- 站主還要在 AdSense 後台做的：在「隱私權與訊息」建立並發布一則 GDPR 訊息、選擇顯示區域
  （EEA／英國／瑞士）、確認廣告夥伴清單，然後才把後台的 `adsense_cmp_enabled` 打開。
