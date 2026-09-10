---
id: 2026-09-10-seo-robots-sitemap
title: 公開 robots.txt 與五語系 sitemap
status: review
priority: P1
area: web
owner: claude-opus-5-seo
claimed_at: 2026-09-10T17:17:34Z
created_at: 2026-09-10T16:43:33Z
completed_at:
branch: claude/seo-optimization-planning-xq1vjl
depends_on:
  - 2026-09-10-seo-canonical-hreflang
scope:
  - apps/web/app/robots.ts
  - apps/web/app/robots.test.ts
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
---

# 公開 robots.txt 與五語系 sitemap

## Why

`apps/web` 從來沒有 `robots.txt` 也沒有 `sitemap.xml`：`app/robots.ts`、`app/sitemap.ts`、
`public/robots.txt` 三個位置都不存在（repo 全域搜尋確認）。搜尋引擎沒有任何抓取指引，也沒有一份
可提交到 Search Console 的網址清單。

站台有五個語系、每個語系一整棵路徑樹，靠爬蟲自己從首頁連結挖出全部內容既慢又不完整——尤其目前
內容多半藏在 query string 後面，內部連結稀疏。

同時有一些路徑本來就不該被抓：`/api/*` 是 BFF 反向代理、`/{locale}/out/*` 是聯盟外連轉址、
`/{locale}/share/{token}` 與 `/{locale}/account/confirm` 是一次性 token 網址、`/{locale}/admin/*` 是後台。

## Definition of done

- [x] production build 下 `/robots.txt` 與 `/sitemap.xml` 都回 200。
- [x] sitemap 每一筆都帶五個 `hreflang` 加一個 `x-default`（Google 要求互指，Next 不會自動補自指連結）。
- [x] sitemap 裡的每一條路徑都對應到實際存在的 `page.tsx`，不會列出 404。
- [x] robots.txt 指向 sitemap 絕對網址。
- [x] 掛了 `noindex` 的頁面**沒有**同時被 `Disallow`。

## Steps

- [x] `apps/web/lib/seo.ts` 已由 `2026-09-10-seo-canonical-hreflang` 建好，這裡沿用它的
      `siteUrl`、`localeUrl()` 與 `HREFLANG_DEFAULT`，不要另外讀一次 `NEXT_PUBLIC_SITE_URL`，
      否則 layout 與 sitemap 有機會對不起來。
- [x] `apps/web/app/robots.ts` 回 `MetadataRoute.Robots`。`disallow` 只放機器端點與 token 網址：
      `/api/`、`/*/out/`、`/*/share/`、`/*/share-target`、`/*/line/`、`/*/account/confirm`、`/*/admin`。
      因為 `localePrefix: "always"`，沒有不帶語系前綴的形式，pattern 必須寫成 `/*/…`。
- [x] `apps/web/app/sitemap.ts` 匯出一份 `SITEMAP_ROUTES` 常數（path + priority + changeFrequency），
      再對五個語系展開，每筆帶完整的 `alternates.languages`。
- [x] **第一版只列現在就存在且可索引的路由**：`/`、`/hotspots`、`/foods`、`/flights/status`、
      `/pricing`、`/labs/airlines`，以及 33 筆 `/destinations/{id}/services`。
      後續任務（目的地落地頁、explore、社群內容）各自把自己的路由 append 進 `SITEMAP_ROUTES`。
- [x] `app/robots.test.ts`、`app/sitemap.test.ts`。sitemap 測試要包含一個「每條路徑都存在」的守門測試：
      走訪 `app/[locale]/` 確認對應的 `page.tsx` 真的在，這是防止 sitemap 列出 404 的唯一保險。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web && npm run check:tasks && npm run build:web
npm --workspace @travel-scanner/web run start
curl -s localhost:3000/robots.txt
curl -s localhost:3000/sitemap.xml | head -40
```

上線後在 Google Search Console 提交 `sitemap.xml`，確認「已探索的網址」數量接近 sitemap 筆數。

## Notes

- **不要在 sitemap 裡打 API。** 33 個目的地 slug 已經在前端 bundle 裡
  （`components/travel-services/options.ts` 的 `PUBLIC_DESTINATIONS`，實測 33 筆），sitemap 只需要網址不需要名稱，
  所以完全不需要在地化也不需要網路。這一點是硬性的：`API_INTERNAL_URL` 在
  `docker-compose.prod.yml` 只有 runtime 才有，而 Next 預設會在 build 期就把 `sitemap.ts` 預先產生，
  CI 的 web job 也沒有可連的 API——build 期 fetch 只會靜靜地產出一份殘缺的 sitemap。
- **`/privacy`、`/terms`、`/about`、`/contact` 第一版先不要列。**
  `components/site-information-page.tsx:12` 在管理文件尚未發布時就會回 `robots: { index: false }`，
  現在列進去只會在 Search Console 累積「已被 noindex 標記排除」。等
  `2026-09-06-legal-content-from-owner` 落地後再加。這四頁在 footer 有連結，不會漏爬。
- **robots.txt 的 `Disallow` 不等於 de-index。** 被 Disallow 的網址爬蟲讀不到 `noindex`，
  反而可能以「只有網址」的形式留在搜尋結果裡。所以 `/login`、`/register`、`/account`、`/trips`、
  `/alerts`、`/my`、`/search` 只掛 `noindex`（見 `2026-09-10-seo-index-directives`），**不要**寫進 `Disallow`。
  `/*/admin` 兩邊都做是刻意的：後台從來沒打算被收錄，也沒有既有索引要清，擋在門口最省爬取預算。
- `proxy.ts` 的 matcher 是 `/((?!api|_next|_vercel|.*\..*).*)`，含小數點的路徑被排除，
  所以 `/robots.txt` 與 `/sitemap.xml` 不會被 next-intl 加上語系前綴。`app/manifest.ts` 已經證明
  `app/` 根層的 metadata route 在沒有 root `layout.tsx` 的情況下可以正常運作。
- 約 200 個 URL 對上單檔 50,000 筆的上限，**不需要 sitemap index 也不需要 `generateSitemaps()`**。
  等景點、店家、文章有了各自的詳情網址再回頭評估。
- **測試用 vitest，不要用 Playwright。** `vitest.config.ts` 只排除 `e2e/**`，新的 `*.test.ts` 會自動被收；
  而 CI 的 Playwright spec 清單寫死在 `.github/workflows/ci.yml`，那個檔被
  `2026-09-09-clarify-stay22-module-switch`（review）鎖住，加不進去。

### 實作結果（2026-09-10, claude-opus-5-seo）

- **`robots.ts` 與 `sitemap.ts` 都必須是 `force-dynamic`，這不是可有可無的。**
  第一版讓它們維持預設的預先產生，實測結果是整份 sitemap 的網址都變成 `http://localhost:3000/…`——
  因為 `siteUrl` 在 build 期就被求值，而那次 build 沒有帶 `NEXT_PUBLIC_SITE_URL`。
  `docker-compose.prod.yml` 雖然同時以 build arg（第 168 行，有預設值）與 runtime（第 174 行，
  用 `:?` 強制必填）提供這個變數，但**只有 runtime 那個是強制的**。也就是說漏帶 build arg 的 build
  會安靜地產出一份跨網域的 sitemap，而 Google 會整份拒收。改成 per-request 之後實測 195 筆網址
  全部落在 `https://mokaair.com`，`localhost` 出現 0 次。重新產生這份檔案的成本可以忽略。
- 診斷時踩到一個坑值得記下來：舊的 `next start` 還佔著 3000 埠，新的啟動失敗但 `curl` 照樣有回應，
  於是量到的是上一版 build 的輸出。改設定後請確認舊 server 真的死了再驗證。
- **sitemap 不打 API 這件事後來看是對的。** 這個 route 會在 build 期被預先產生（改成 dynamic 之前），
  而 `API_INTERNAL_URL` 只有 runtime 才有，CI 的 web job 也沒有後端。33 個 slug 直接取自
  `components/travel-services/options.ts` 的 `PUBLIC_DESTINATIONS`（唯讀 import，該檔的 scope 屬於
  review 中的 stay22 任務，本任務沒有修改它）。
- `sitemap.test.ts` 的「每條路徑都對應到真的 `page.tsx`」守門測試會同時走訪 `app/[locale]` 與
  `app/(stay22-public)/[locale]` 兩棵樹，並讓 `[dynamic]` 目錄比對字面 segment，
  所以 `/destinations/tokyo/services` 解析得到。另外加了一個「守門的守門」測試
  （`/not-a-route` 必須回 false），避免走訪邏輯壞掉之後整組測試變成空轉——
  這個手法沿用 `metadata.test.ts` 既有的 "a guard on the guard"。
- `robots.test.ts` 有一條測試專門守「掛了 `noindex` 的頁面不可以同時被 `Disallow`」，
  刻意排除 `/admin`、`/share`、`/share-target`、`/line`、`/account/confirm` 這幾條兩邊都做的路徑。

### 驗證紀錄

`npm run lint:web`、`npm run typecheck:web`、`npm run build:web` 通過；
`app/robots.test.ts` 與 `app/sitemap.test.ts` 共 53 個測試通過。build 輸出顯示
`ƒ /robots.txt` 與 `ƒ /sitemap.xml`（dynamic）。

對 production build 實測：

```
Sitemap: https://mokaair.com/sitemap.xml
<loc>https://mokaair.com/en</loc>
urls: 195   localhost leaks: 0   xhtml:link: 1170
```

195 = 39 條路由 × 5 語系；1170 = 195 × 6（五語系 + `x-default`）。
