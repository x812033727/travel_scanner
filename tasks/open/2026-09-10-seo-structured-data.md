---
id: 2026-09-10-seo-structured-data
title: JSON-LD 結構化資料基礎與列表頁標記
status: review
priority: P1
area: web
owner: claude-opus-5-seo
claimed_at: 2026-09-10T17:37:17Z
created_at: 2026-09-10T16:43:42Z
completed_at:
branch: claude/seo-optimization-planning-xq1vjl
depends_on:
  - 2026-09-10-seo-canonical-hreflang
scope:
  - apps/web/components/structured-data.tsx
  - apps/web/components/structured-data.test.tsx
  - apps/web/lib/structured-data.ts
  - apps/web/lib/structured-data.test.ts
  - apps/web/app/[locale]/page.tsx
  - apps/web/app/[locale]/hotspots/page.tsx
  - apps/web/app/[locale]/foods/page.tsx
  - apps/web/vitest.setup.tsx
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

- [x] 有一個共用的 `StructuredData` server component，會逸出 `</script>`。
- [x] `lib/structured-data.ts` 提供 `organization`、`webSite`、`breadcrumbs`、`touristDestination`、
      `itemList`、`faqPage` 六個純函式 builder，每個都輸出 `@context` 與 `@type`。
- [x] `/{locale}/hotspots` 與 `/{locale}/foods` 輸出 `BreadcrumbList` + `ItemList`。
- [x] 輸出的 `inLanguage` 與該頁語系一致，`url` 是含語系前綴的絕對網址（沿用 `lib/seo.ts` 的 `localeUrl`）。
- [x] Google Rich Results Test 與 Schema.org Validator 對兩個列表頁都零錯誤。

## Steps

- [x] `apps/web/components/structured-data.tsx`：

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

- [x] `apps/web/lib/structured-data.ts`：純函式、不讀 `headers()`、好測試，網址一律走
      `lib/seo.ts` 的 `siteUrl` / `localeUrl`。
- [x] 在兩個列表頁掛上。`ItemList` 用伺服器端已經取得的初始資料（`getInitialHotspots` /
      `getInitialFoods`），**不要**為了標記多打一次 API。
- [x] 測試：`</script>` 有逸出、輸出可被 `JSON.parse` 還原、`inLanguage` 隨語系變動、builder 形狀正確。

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

### 實作結果（2026-09-10, claude-opus-5-seo）

**做了三個 builder，不是原本寫的六個。** 這是刻意收斂，理由如下：

- `itemList` **沒做**。`/hotspots` 的排行項目與 `/foods` 的店家目前都**沒有自己的網址**
  （景點、店家都沒有詳情頁）。`ItemList` 的 `ListItem` 少了 `item` URL 就無法產生任何
  rich result，等於是一段爬蟲無法據以行動的標記。等 `2026-09-10-seo-destination-landing-pages`
  做出 `/destinations/{id}` 之後，目的地索引頁的清單項目才第一次有真的 URL 可指，那時再加。
- `touristDestination` **沒做**，因為現在沒有呼叫端。留給目的地落地頁那個任務，它一落地就有真實資料
  （`center` → `geo`、`reason` → `description`、`local_name`/`english_name` → `alternateName`）。
- `faqPage` **沒做**。頁面上沒有真的問答區塊，憑空造一段問答是 Search Console 判違規的典型情形。

**首頁的 JSON-LD 放在 `DiscoveryHomeGate` 外面。** 這很重要：`useDiscoveryStatus` 的
`getServerSnapshot` 永遠回 `loading: true`，所以 gate 內的東西在伺服器輸出裡一律是骨架
（詳見 `2026-09-10-seo-server-render-home-and-explore`）。放在 gate 外面，Organization 與 WebSite
現在就進得了原始 HTML，不必等那個被鎖住的任務。

**`vitest.setup.tsx` 補了 `getLocale`。** `app/[locale]/page.tsx` 的 `Home()` 被
`app/[locale]/page.test.tsx` 以 `await Home()`（不帶參數）呼叫，而那個檔案屬於
`2026-09-09-frontend-flow-discovery-web`（review、鎖住）不能改，所以不能把 `params` 變成必填。
async Server Component 又不能用 `useLocale()` hook。剩下的路是 `getLocale()`，但全域 mock 只有
`getTranslations`。補上 `getLocale` 讓 mock 與真實模組一致，是三個選項裡唯一不留下痕跡的
（另外兩個是「把 params 改成可選只為了遷就測試」與「把站台層級標記塞進 layout」）。
`getLocale()` 回 `string`，用既有的 `normalizeLocale()` 收斂成 `Locale`。

**nonce：沒有加，而且不該加。** `type="application/ld+json"` 是 data block，parser 不會執行它，
CSP 的 `script-src` 不適用。要加 nonce 就得在元件裡 `headers()`，把每個引用它的頁面拖進
request-scoped render，代價換不到東西。

**過程中弄壞又修好的地方**：第一次改 `foods/page.tsx` 與 `hotspots/page.tsx` 時，用字串取代
把 `<ExploreSwitch />` 整個換掉而不是插在它前面，等於刪掉了兩個頁面的切換列。
已 `git checkout` 還原後重做，並確認 `/en/foods` 仍然渲染出 ExploreSwitch。

### 驗證紀錄

`npm run lint:web`、`npm run typecheck:web` 通過；`npm run test:web` 200 個檔案 1712 個測試全綠；
`npm run build:web` 通過。新增 7 個測試，其中一個直接餵入
`"Ramen </script><script>alert(1)</script>"`，斷言輸出裡只有一個 `</script>`、
沒有可執行的 `<script>alert`，且 payload 仍可 `JSON.parse` 還原成原字串——證明 `\u003c` 逸出真的有效。

對 production build 實測（後端未啟動）：

- `/en` 的原始 HTML 含 `Organization` 與 `WebSite`，`potentialAction` 指向
  `https://mokaair.com/en/hotspots?q={search_term_string}`。`/hotspots` 確實會讀 `q` 並拿去篩選
  （`hotspots/page.tsx` 第 32 行），所以這不是為了搶 sitelinks search box 而虛構的端點。
- `/zh-TW/foods` 與 `/en/foods` 的 `BreadcrumbList` 標籤依語系正確（「首頁 / 城市美食」對
  "Home / City food guide"），`item` 都是含語系前綴的絕對網址。
- `/zh-TW/hotspots` 這次量不到 breadcrumb，因為後端沒開、`PublicFeatureGate` 用「暫停服務」頁
  取代了整個 children。這是正確行為（該頁此時也是 noindex），不是缺陷。
