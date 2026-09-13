---
id: 2026-09-13-adsense-article-slot
title: 文章頁 AdSense 版位、載入器與文章路由 CSP
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-13T05:16:19Z
completed_at:
branch:
depends_on:
  - 2026-09-13-adsense-privacy-policy-section
  - 2026-09-13-adsense-admin-config
  - 2026-09-12-attribute-affiliate-clicks-to-the-guide
scope:
  - apps/web/components/ads
  - apps/web/lib/adsense.server.ts
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/app/(ads-public)
  - apps/web/app/[locale]/guides/[kind]/[slug]/page.tsx
  - apps/web/app/[locale]/life/[slug]/page.tsx
  - apps/web/lib/csp.ts
  - apps/web/lib/csp.test.ts
  - apps/web/proxy.ts
  - apps/web/public/ads.txt
  - tools/e2e-runtime-api.mjs
  - apps/web/e2e/guides-adsense.spec.ts
  - .github/workflows/ci.yml
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - docs/travel-guides.md
  - docs/adsense-feasibility.md
---

# 文章頁 AdSense 版位、載入器與文章路由 CSP

## Why

評估全文在 `docs/adsense-feasibility.md`。這張是真正把廣告放上頁面的那一步，只限
旅遊情報攻略與生活分享的**文章頁**（`/{locale}/guides/{kind}/{slug}`、`/{locale}/life/{slug}`）。
其他頁都不放：分享頁、社群、hub、帳號、行程。

依賴三張票：隱私政策揭露（沒有就違反 AdSense 政策）、後台設定與匿名設定端點、
分潤點擊記到文章（沒有就量不出廣告有沒有吃掉分潤點擊）。另外要等站主做完 D1–D5，
並且 AdSense 審核通過、slot ID 已填進後台。

## Definition of done

- [ ] **只在文章頁**、而且伺服器端判斷可以時才輸出版位。條件：
      設定端點回開啟；請求沒有 `Sec-GPC: 1` 或 `DNT: 1`；該語系的文章可讀，
      也就是不是 unavailable、不是「沒有你的語言」頁。關閉時連預留空間都不輸出。
- [ ] 版位規則：
      - 數量照 D3（1–2 個）。
      - 不在第一屏（hero 是 LCP，`article.tsx:116-137`）。
      - 不貼著 offer island 或文末合作區塊，中間至少隔一個內容段落；政策禁止廣告放在互動元素旁。
      - 預留固定最小高度，避免 CLS。
      - 上方標示「廣告」：新 key 放 `common.json` 的 `guides.*`，五語系。
- [ ] 載入器是 client island：`next/script` 載入
      `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=<ca-pub>`（`crossOrigin="anonymous"`）。
      每個 `<ins class="adsbygoogle">` mount 時 push 一次；D1 選非個人化時先設
      `requestNonPersonalizedAds = 1`（見 AdSense「廣告個人化設定」的程式碼範例）。
      開發模式 StrictMode 會跑兩次 effect，用 `data-adsbygoogle-status` 防重複 push。
- [ ] **document 邊界**：比照 Stay22 的前例（`docs/stay22-module-switch.md:41-62`、
      `app/(stay22-public)/[locale]/layout.tsx`），有廣告的文章頁放在獨立的 root layout（`app/(ads-public)`）。
      - 從文章頁到私人頁面一定是整頁導覽，已執行的廣告腳本不會留在帳號、行程頁的 document 裡。
      - 載入前去掉 query。
      - 這個 layout 不掛讀取 session 的 provider。
      - 設定關閉時退回原本的 layout。
- [ ] **CSP（D5）**：`proxy.ts` 只對文章路由產生 AdSense 版政策。
      依 Google 說明是 `script-src 'nonce-…' 'unsafe-inline' 'unsafe-eval' 'strict-dynamic' https: http:`，
      `frame-src`、`connect-src` 放寬到 `https:`；其他路由的政策一個字都不變。
      `lib/csp.test.ts` 加一組文章路由的斷言，既有斷言（`:9`、`:46`）保留給非文章路由。
- [ ] `apps/web/public/ads.txt`：`google.com, pub-<16 位數字>, DIRECT, f08c47fec0942fa0`。
- [ ] 測試：
      - `tools/e2e-runtime-api.mjs` 的新設定端點回關閉，所以既有 8 支「零外部請求」規格不變。
      - 新規格 `e2e/guides-adsense.spec.ts`：設定開啟時出現有標籤、有預留高度的版位，對 `pagead2.googlesyndication.com` 的請求在測試裡攔下；
        GPC 時沒有版位；hub、分享頁沒有版位。
      - 把新規格加進 `.github/workflows/ci.yml` 的 Playwright 清單。
- [ ] 文件：`docs/travel-guides.md:98-100`「文章永遠不會讓瀏覽器向第三方抓圖」改成照實描述；
      `docs/adsense-feasibility.md` 記下 D1–D5 的最終答案。

## Steps

- [ ] 開工前重讀 Google 的 AdSense CSP 說明與廣告個人化設定，確認寫法沒變（連結在評估文件第十節）。
- [ ] `lib/adsense.server.ts`：伺服器端讀設定，比照 `lib/stay22-script.server.ts`。
- [ ] `app/(ads-public)` layout、兩個文章路由搬過去或改掛；確認切換 layout 時是整頁導覽。
- [ ] `components/ads`：版位元件與載入器。
- [ ] `article.tsx` 在段落之間插版位；`article-page.tsx` 傳入是否可放。
- [ ] `proxy.ts`＋`csp.ts` 的文章路由 CSP 與測試。
- [ ] `ads.txt`、e2e fixture、新規格、ci.yml。
- [ ] 上線後兩週：比較文章頁分潤點擊率（`GET /admin/analytics/affiliates` 的 by_article）與 CLS，結果寫進 Notes。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
cd apps/web && npm run build && PLAYWRIGHT_SERVE_BUILD=true npx playwright test e2e/guides-adsense.spec.ts e2e/site-experience.spec.ts e2e/stay22-script.spec.ts
```

CLS 要在頂層頁用 Playwright 量（`chromium.launch()`，`addInitScript` 先裝 `PerformanceObserver`），
而且要先對一個故意位移的對照頁跑一次，確認量得出非零值；內建瀏覽器 pane 永遠量到 0。

正式站：`curl -s https://mokaair.com/ads.txt`；開一篇文章看到「廣告」版位；
開 GPC（例如 Brave）再開同一篇，沒有版位也沒有對 googlesyndication 的請求。

## Notes

- 為什麼要獨立 document：移除 React `<Script>` 收不回已經執行的第三方 observer 和 timer（Stay22 文件原話的意思）。
  文章頁跟帳號、行程共用 root layout 時，讀完文章用 client-side 導覽進私人頁，廣告腳本仍然在跑。
- `ads.txt` 可能已經在站主送審時先單獨上線了（評估文件第七節第 2 步），那就只要確認內容，不用重做。
- 分享頁 `/share/{token}` 絕對不要放：網址本身是秘密 token，同頁第三方腳本讀得到。
- 手機的 sticky header（z-40）與固定底部導覽（z-60）會跟錨定、插頁廣告撞在一起，所以要在 AdSense 後台關閉這兩種（D3）。
- Travelpayouts Drive 已經在每一頁載入（`app/[locale]/layout.tsx:109`）；獨立 layout 要決定帶不帶它，比照 Stay22 layout 是不帶。
- 範圍重疊：
  - `components/guides/article.tsx` 也在 `2026-09-12-attribute-affiliate-clicks-to-the-guide` 的 scope 裡，那張是依賴，先做完它。
  - `lib/csp.ts` 在 `2026-09-07-mokaair-community-web` 的 scope 裡；claim 前用 `npm run tasks -- list` 看它是不是 in-progress。
