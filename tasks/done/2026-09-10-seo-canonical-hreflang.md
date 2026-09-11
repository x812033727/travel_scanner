---
id: 2026-09-10-seo-canonical-hreflang
title: 修好每頁的 canonical 與 hreflang
status: done
priority: P0
area: web
owner: claude-opus-5-seo
claimed_at: 2026-09-10T17:04:03Z
created_at: 2026-09-10T16:43:32Z
completed_at: 2026-09-11T15:54:03Z
branch: claude/seo-optimization-planning-xq1vjl
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

- [x] 任一公開頁的 `<link rel="canonical">` 指向該頁自己的網址，而不是語系首頁。
- [x] 每頁輸出五個 `hreflang` 指向同一內容的五個語系版本，外加一個 `x-default`。
- [x] 帶 query string 的網址（例如 `/zh-TW/hotspots?destination_id=tokyo`）canonical 不含 query。
- [x] `og:title` / `og:description` 與該頁自己的 `<title>` / meta description 一致，不再是站台層級的共用字串。
- [x] `destination-services-page.tsx` 既有的自訂 `alternates` 行為不變。

## Steps

- [x] 新增 `apps/web/lib/seo.ts`，集中三件事：`SITE_URL`、`currentSeoPath()`、`localeAlternates(locale, path)`。
      `currentSeoPath()` 讀 `proxy.ts` 已經設好的可信賴 request header `x-travel-pathname`
      （值是 `pathname + search`），剝掉 query 與語系前綴，回傳例如 `/hotspots`；header 缺失時回空字串。
- [x] 同時提供 `pageMetadata({ locale, path, title, description, index?, image? })` 供後續任務逐頁使用。
      **簽名必須讓呼叫端保留 `title: t("xxx")` 的原始碼字面**，理由見 Notes。
- [x] 把 layout 的 `alternates` 換成 `localeAlternates(locale, await currentSeoPath())`。
- [x] 把 `openGraph.title`、`openGraph.description`、`twitter.title`、`twitter.description` 從 layout 移除，
      讓 Next.js 用各頁 resolve 後的 title/description 回填。**先寫測試確認 Next 16 真的會回填**；
      若不會，改成各頁透過 `pageMetadata()` 明確帶上。
- [x] `apps/web/lib/seo.test.ts`：path 剝離（含 query、含語系前綴、根路徑）、五語系 + `x-default` 齊全、
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

### 實作結果（2026-09-10, claude-opus-5-seo）

- **og fallback 已從 Next 16 原始碼確認，不是猜的。** `node_modules/next/dist/lib/metadata/resolve-metadata.js`
  的 `postProcessMetadata()` 在最後呼叫 `inheritFromMetadata(openGraph, metadata)` 與
  `inheritFromMetadata(twitter, metadata)`，會在 og/twitter 沒有自己的 title/description 時，
  用該路由**已合併完成**的 `metadata.title` / `description` 回填。
  所以只要 layout 不指定 og title/description，每頁的 og:title 就會自動等於該頁的 `<title>`。
  `resolve-opengraph.js` 本身沒有任何 fallback，容易誤判成不會繼承。
- **首頁的專用社群文案保住了。** 用 `path === "/"` 判斷，只有語系首頁才帶 `ogTitle`/`ogDescription`。
  這讓 `messages/*/metadata.json` 的兩個 key 都還有人用，也避免首頁分享卡退化成分頁標題。
  實測 `/zh-TW` 的 `<title>` 是「Mokaair｜完整旅程比價」而 og:title 是
  「Mokaair｜完整旅程比價與最佳化」，兩者維持原本的差異。
- **`lib/seo.ts` 刻意不 import `next/headers`。** sitemap route、單元測試與未來的頁面 helper 都要用這些
  builder，只有 layout 有 request 可以讀路徑。header 的讀取留在 layout 裡。
- layout 原本自己有一份 `const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || …`，已改成 import
  `lib/seo.ts` 的同一個值。`isTravelpayoutsDriveOrigin()` 走 `new URL(siteUrl).origin`，
  對尾斜線不敏感，行為不變。
- `pageMetadata()` 目前沒有呼叫端，是留給需要覆寫 canonical 的頁面用的
  （例如 `role: "extension"` 的目的地要指向母目的地）。若 `2026-09-10-seo-destination-landing-pages`
  最後沒有用到，應該把它刪掉而不是留著。

### 驗證紀錄

`npm run lint:web`、`npm run typecheck:web` 通過；`npm run test:web` 195 個檔案 1627 個測試全綠
（含未修改的 `metadata.test.ts` 與 `(stay22-public)` layout 測試）。`npm run build:web` 通過。

對 production build 實際抓 HTML：

| 網址 | canonical | og:title |
| --- | --- | --- |
| `/en/foods` | `https://mokaair.com/en/foods` | `City food guide \| Mokaair` |
| `/zh-TW/hotspots` | `https://mokaair.com/zh-TW/hotspots` | `熱門景點排行榜｜Mokaair` |
| `/en/pricing` | `https://mokaair.com/en/pricing` | `Plans and usage packs \| Mokaair` |

三者的 og:title 都等於各自的 `<title>`；修改前三者的 canonical 全部是 `https://mokaair.com/{locale}`、
og:title 全部是站台層級的同一句。`/en/foods` 輸出五個 hreflang 加一個 `x-default`，全部指向同一頁的
五個語言版本。`/zh-TW/hotspots?destination_id=tokyo&area=x` 的 canonical 正確落在 `/zh-TW/hotspots`。
`/en/destinations/tokyo/services` 自訂的 `alternates` 仍然優先，未受影響。

## 標記完成（由站主授權，非原持有者）

這張任務的工作已隨 PR #388 於 2026-09-11 合併進 main：merge commit `d0ec33e` 的第二個 parent 就是分支 head `999dbc5`，分支上每個 commit 都在 main 裡，分支也已刪除。該 head 的每個 check 都通過（`api`、`web`、`containers`、`full-stack-smoke`、`discovery-browser`、`planner-browser`）。狀態卻一直停在 `review`，持有的 scope 因此擋住後續任務，2026-09-11 由 claude-opus-5 移到 done。

若原持有者 `claude-opus-5-seo` 尚有未推送的後續工作，請重新開一張任務，不要把這張改回 review。
