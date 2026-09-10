---
id: 2026-09-10-seo-structured-data
title: JSON-LD 結構化資料基礎與列表頁標記
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-10T16:43:42Z
completed_at:
branch:
depends_on:
  - 2026-09-10-seo-canonical-hreflang
scope:
  - apps/web/components/structured-data.tsx
  - apps/web/components/structured-data.test.tsx
  - apps/web/lib/structured-data.ts
  - apps/web/lib/structured-data.test.ts
  - apps/web/app/[locale]/hotspots/page.tsx
  - apps/web/app/[locale]/foods/page.tsx
---

# JSON-LD 結構化資料基礎與列表頁標記

## Why

整個 `apps/web` 沒有任何一行結構化資料：搜尋 `application/ld+json`、`schema.org`、`@context`、`@type`
在 `app/`、`components/`、`lib/` 全都是零筆。站台有品牌、站內搜尋、景點排行、城市美食這些天生適合
標記的內容，卻完全沒有告訴搜尋引擎它們是什麼。

沒有 `Organization` 就沒有品牌識別；沒有 `WebSite` + `SearchAction` 就拿不到站內搜尋框；
列表頁沒有 `ItemList`、內頁沒有 `BreadcrumbList`，搜尋結果裡也不會出現麵包屑。

本任務只做**共用元件、builder 與兩個列表頁**。首頁的 `Organization` / `WebSite` 標記留給
`2026-09-10-seo-server-render-home-and-explore`，因為首頁目前的伺服器端輸出是骨架，那個任務會一併處理；
目的地頁的 `TouristDestination` 留給 `2026-09-10-seo-destination-landing-pages`。兩者都會沿用這裡建好的東西。

## Definition of done

- [ ] 有一個共用的 `StructuredData` server component，會逸出 `</script>`。
- [ ] `lib/structured-data.ts` 提供 `organization`、`webSite`、`breadcrumbs`、`touristDestination`、
      `itemList`、`faqPage` 六個純函式 builder，每個都輸出 `@context` 與 `@type`。
- [ ] `/{locale}/hotspots` 與 `/{locale}/foods` 輸出 `BreadcrumbList` + `ItemList`。
- [ ] 輸出的 `inLanguage` 與該頁語系一致，`url` 是含語系前綴的絕對網址（沿用 `lib/seo.ts` 的 `localeUrl`）。
- [ ] Google Rich Results Test 與 Schema.org Validator 對兩個列表頁都零錯誤。

## Steps

- [ ] `apps/web/components/structured-data.tsx`：

      ```tsx
      export function StructuredData({ data }: { data: object | object[] }) {
        return (
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(data).replace(/</g, "\\u003c") }}
          />
        );
      }
      ```

- [ ] `apps/web/lib/structured-data.ts`：純函式、不讀 `headers()`、好測試，網址一律走
      `lib/seo.ts` 的 `siteUrl` / `localeUrl`。
- [ ] 在兩個列表頁掛上。`ItemList` 用伺服器端已經取得的初始資料（`getInitialHotspots` /
      `getInitialFoods`），**不要**為了標記多打一次 API。
- [ ] 測試：`</script>` 有逸出、輸出可被 `JSON.parse` 還原、`inLanguage` 隨語系變動、builder 形狀正確。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web && npm run check:tasks && npm run build:web
npm --workspace @travel-scanner/web run start
curl -s localhost:3000/zh-TW/hotspots | grep -c 'application/ld+json'
```

把輸出的 JSON 貼進 Google Rich Results Test 與 Schema.org Validator，兩邊都要零錯誤。

## Notes

- `JSON.stringify` 之後把每個 `<` 換成 JSON 逸出序列 `\u003c`（在 JSON 字串裡等價於 `<`）。
  這不是可有可無的：店家名稱、景點名稱、貼文標題都會流進這些圖譜，其中任何一個含 `</script>`
  都會提早關閉標籤。
- **nonce：不需要，也刻意不加。** `type="application/ld+json"` 在 HTML 規格裡是 data block，
  瀏覽器不會執行它，CSP 的 `script-src` 因此不適用（本站的 CSP 目前還是 Report-Only）。
  更重要的是，加 nonce 就得在元件裡呼叫 `headers()`，會讓每個引用它的頁面失去靜態渲染的可能。
  如果日後在真實瀏覽器裡確實看到 CSP 報告，再改成從 `x-nonce` 取值並接受那個代價。
- **`/{locale}/pricing` 不要掛 `Product` / `Offer`**：那是用量方案不是商品，標錯結構化資料會在
  Search Console 被判定為違規。
- `FAQPage` 只在頁面上真的有問答區塊時才輸出，不要為了 rich result 憑空捏造問答。
- 社群的 `Article` / `Person` 等到那些頁面真的有伺服器端內容再說
  （見 `2026-09-10-seo-open-content-pages`）。
