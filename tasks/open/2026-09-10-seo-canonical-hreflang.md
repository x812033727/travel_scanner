---
id: 2026-09-10-seo-canonical-hreflang
title: 修好每頁的 canonical 與 hreflang
status: open
priority: P0
area: web
owner:
claimed_at:
created_at: 2026-09-10T16:43:32Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/lib/seo.ts
  - apps/web/lib/seo.test.ts
  - apps/web/app/[locale]/layout.tsx
---

# 修好每頁的 canonical 與 hreflang

## Why

`apps/web/app/[locale]/layout.tsx` 的 `generateMetadata` 把 canonical 寫死成語系首頁：

```ts
alternates: { canonical: `${siteUrl}/${locale}`, languages },
```

Next.js 的 metadata 是 parent → child 淺層合併，`alternates` 是 top-level key，只有自己設定 `alternates`
的頁面才會覆寫它。全站四十餘個 `page.tsx` 裡只有
`components/travel-services/destination-services-page.tsx` 這麼做。結果是 `/en/hotspots`、`/en/foods`、
`/en/pricing`、`/zh-TW/flights/status` 等每一頁都輸出

```html
<link rel="canonical" href="https://mokaair.com/en" />
```

也就是對搜尋引擎宣告「我跟首頁是同一頁」。canonical 是強烈提示而非指令，但這種全站自我指向首頁的形態，
典型結果是 Search Console 出現大量「重複網頁，Google 選擇的標準網址與使用者指定的不同」，內頁被排除在
索引外。`alternates.languages` 有同樣的問題：五個 hreflang 全部指向各語系首頁，而不是同一篇內容的五個語言版本，
而且沒有 `x-default`。

站台的 URL 結構本身是對的（`localePrefix: "always"`，五語系各有自己的路徑，`<html lang>` 也正確），
所以這是一個純粹的 metadata 計算錯誤，不是架構問題。

## Definition of done

- [ ] 任一公開頁的 `<link rel="canonical">` 指向該頁自己的網址，而不是語系首頁。
- [ ] 每頁輸出五個 `hreflang` 指向同一內容的五個語系版本，外加一個 `x-default`。
- [ ] 帶 query string 的網址（例如 `/zh-TW/hotspots?destination_id=tokyo`）canonical 不含 query。
- [ ] `og:title` / `og:description` 與該頁自己的 `<title>` / meta description 一致，不再是站台層級的共用字串。
- [ ] `destination-services-page.tsx` 既有的自訂 `alternates` 行為不變。

## Steps

- [ ] 新增 `apps/web/lib/seo.ts`，集中三件事：`SITE_URL`、`currentSeoPath()`、`localeAlternates(locale, path)`。
      `currentSeoPath()` 讀 `proxy.ts` 已經設好的可信賴 request header `x-travel-pathname`
      （值是 `pathname + search`），剝掉 query 與語系前綴，回傳例如 `/hotspots`；header 缺失時回空字串。
- [ ] 同時提供 `pageMetadata({ locale, path, title, description, index?, image? })` 供後續任務逐頁使用。
      **簽名必須讓呼叫端保留 `title: t("xxx")` 的原始碼字面**，理由見 Notes。
- [ ] 把 layout 的 `alternates` 換成 `localeAlternates(locale, await currentSeoPath())`。
- [ ] 把 `openGraph.title`、`openGraph.description`、`twitter.title`、`twitter.description` 從 layout 移除，
      讓 Next.js 用各頁 resolve 後的 title/description 回填。**先寫測試確認 Next 16 真的會回填**；
      若不會，改成各頁透過 `pageMetadata()` 明確帶上。
- [ ] `apps/web/lib/seo.test.ts`：path 剝離（含 query、含語系前綴、根路徑）、五語系 + `x-default` 齊全、
      header 缺失時 fallback 回 `${SITE_URL}/${locale}`。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web && npm run check:tasks
```

再跑一次本機 production build 並直接看原始 HTML：

```bash
npm run build:web && npm run start --workspace @travel-scanner/web
curl -s http://localhost:3000/en/foods | grep -E 'rel="canonical"|hreflang|og:title'
```

`canonical` 必須是 `.../en/foods`，不是 `.../en`；`hreflang` 要有 en、ja、ko、zh-TW、zh-CN 與 x-default。

## Notes

- `headers()` 出現在 `generateMetadata` 會讓路由變成 dynamic，但這個 layout 本來就 `await cookies()`，
  全站早已是 per-request SSR，沒有額外成本。
- `apps/web/app/(stay22-public)/[locale]/layout.tsx` 是 `export { generateMetadata } from "@/app/[locale]/layout"`，
  會自動受惠。**該檔與整個 `apps/web/app/(stay22-public)` 被 `2026-09-09-isolate-public-stay22-script`（review）
  鎖住，不可觸碰**；改完請確認 `/zh-TW/destinations/tokyo/services` 的 canonical 仍是該頁既有的自訂值。
- `apps/web/app/[locale]/layout.tsx` 也被 `2026-09-09-site-experience-settings`（blocked）與
  `2026-09-07-mokaair-community-web`（open）列在 scope 裡。兩者都不是 active 狀態所以不鎖 scope，
  但認領前請先看一眼那兩個任務有沒有動起來。
- `x-default` 選 `en`，不要指向未加語系前綴的路徑：那會依賴 `localeDetection` 的轉址行為，對爬蟲不穩定。
- **不要改 `apps/web/app/[locale]/metadata.test.ts`**（被 blocked 任務認領）。它用
  `/title:\s*t\("([A-Za-z]+)"\)/` 直接比對 `page.tsx` 的原始碼字面，所以任何共用 helper 都必須設計成
  `pageMetadata({ ..., title: t("foodsTitle"), description: t("foodsDescription") })` 這種形式，
  把字面留在呼叫端；寫成 `pageMetadata(locale, "foods")` 會讓那個測試報 "has no generateMetadata"。
