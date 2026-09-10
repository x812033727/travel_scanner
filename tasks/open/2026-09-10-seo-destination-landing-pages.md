---
id: 2026-09-10-seo-destination-landing-pages
title: 目的地索引頁與城市指南落地頁
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
  - 2026-09-10-seo-robots-sitemap
  - 2026-09-10-seo-structured-data
scope:
  - apps/web/app/[locale]/destinations/page.tsx
  - apps/web/app/[locale]/destinations/[destinationId]/page.tsx
  - apps/web/components/destination-guide.tsx
  - apps/web/components/destination-guide.test.tsx
  - apps/web/lib/destinations.server.ts
  - apps/web/lib/destinations.server.test.ts
  - apps/web/lib/destinations-copy.ts
  - apps/web/lib/destinations-copy.test.ts
  - apps/web/messages/en/metadata.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ko/metadata.json
  - apps/web/messages/zh-TW/metadata.json
  - apps/web/messages/zh-CN/metadata.json
---

# 目的地索引頁與城市指南落地頁

## Why

站台完全沒有可被索引的目的地內容頁。`/{locale}/destinations` 與 `/{locale}/destinations/{id}` 都不存在；
唯一帶目的地的路徑是 `/{locale}/destinations/{id}/services`（住宿聯盟頁）。景點與美食只能透過
`/{locale}/hotspots?destination_id=tokyo` 這種 query string 到達——搜尋引擎不會把 query 組合當成獨立
內容頁，站內也沒有任何 hub 頁把它們連起來。

結果是：一個以亞洲城市旅遊為主題的站台，沒有一頁在講「東京」。

而資料其實早就備齊，而且品質比預期好。`apps/api/app/destinations/catalog.py` 有 33 筆
`DestinationProfile`，slug 是人類可讀的 `tokyo`、`osaka-kyoto`、`seoul`、`busan`、`bangkok`、`taipei`…；
`apps/api/app/destinations/localized.py` 有 `CITY_NAMES`、`COUNTRY_LABELS`、`REASONS` 與
`area_labels()`，**33 個目的地 × 5 語系全部齊備，而且有 `validate_localized_catalog()` 把關**。
`GET /api/v1/destinations`（`apps/api/app/places/router.py:292`）依 `X-Travel-Locale` 一次回齊
`city`、`local_name`、`english_name`、`country`、`country_code`、`areas`、`reason`、
`recommended_days.{min,max}`、`timezone`、`currency`、`center.{latitude,longitude}`、`role`、
`parent_destination_id`、`extension_ids`。

33 個目的地 × 5 語系 = 166 個新的可索引網址（含索引頁），全部有真實內容，全部能往既有的
hotspots / foods / 行程規劃導流。

## Definition of done

- [ ] `/{locale}/destinations` 依國家分組列出所有目的地，每筆連到自己的指南頁。
- [ ] `/{locale}/destinations/{id}` 伺服器端渲染出：在地化城市名的 `<h1>`、為什麼去、區域清單、
      建議天數、時區與貨幣、熱門景點、代表店家。
- [ ] 景點與店家**出現在原始 HTML 裡**（關掉 JS 也看得到），不是 hydration 後才 fetch。
- [ ] 兩頁都有正確的 canonical、五語系 hreflang 與 `x-default`（沿用 `lib/seo.ts`）。
- [ ] 兩頁都有 `BreadcrumbList`；指南頁另有 `TouristDestination`（`geo` 用 `center`）與景點 `ItemList`。
- [ ] `role: "extension"` 的目的地 canonical 指向其 `parent_destination_id` 的指南頁，不與母目的地互相競爭。
- [ ] 未知的 `destinationId` 回 404（`notFound()`），不是空白頁。
- [ ] 後端不可用時頁面仍可渲染核心目錄內容，景點／店家區塊優雅缺席。
- [ ] `npm run check:i18n` 與未經修改的 `metadata.test.ts` 都通過。
- [ ] `npm run build:web` 通過，與既有的 `/{locale}/destinations/{id}/services` 沒有路由衝突。

## Steps

- [ ] **第一步先驗證路由能共存**：放一個空的 `app/[locale]/destinations/[destinationId]/page.tsx`
      跑一次 `npm run build:web`，確認沒有跟 route group 底下的 `/services` 衝突，再開始寫內容。
- [ ] `apps/web/lib/destinations.server.ts`：照 `lib/hotspots.server.ts` 的既有形態
      （`API_INTERNAL_URL` + `X-Travel-Locale` header + `try/catch` 回 `null` + React `cache()` 去重），
      加上 `next: { revalidate: 3600 }`（目錄大約一季才變一次）。
      指南頁另外取 `GET /api/v1/hotspots/rankings?destination_id={id}&limit=12`（`revalidate: 900`）
      與 `GET /api/v1/foods/merchants?destination_id={id}&limit=12`。
      目錄查詢失敗時 fallback 到 `apps/web/lib/destinations.ts` 的離線副本。
- [ ] `apps/web/lib/destinations-copy.ts`：區塊標題等版面文案，locale-keyed TS 物件，
      形態比照既有的 `lib/discovery-copy.ts` / `lib/stay22-script-copy.ts` / `lib/frontend-flow-copy.ts`。
      **不要新增 `messages/` namespace**（理由見 Notes）。
- [ ] `apps/web/components/destination-guide.tsx`：純呈現，一個 `<h1>` + 數個 `<h2>` 分區
      （住哪裡 / 看什麼 / 吃什麼 / 規劃行程 / 鄰近延伸），內部連結指向
      `/{locale}/hotspots?destination_id={id}&area=…`、`/{locale}/foods`、
      既有的 `/{locale}/destinations/{id}/services`、以及 `/search/new`。
      母目的地用 `extension_ids` 連向延伸目的地，延伸目的地反向連回母目的地。
- [ ] 兩個 `page.tsx`。指南頁用 `if (!PUBLIC_DESTINATIONS.includes(destinationId)) notFound();` 驗證，
      形態與既有的 services 頁一致。
- [ ] 五個 `messages/*/metadata.json` 補 `destinationsTitle`、`destinationsDescription` **兩個 key**。
- [ ] 把 `/destinations` 與 33 筆指南頁 append 進 `app/sitemap.ts` 的 `SITEMAP_ROUTES`。
- [ ] 掛上 `2026-09-10-seo-structured-data` 建好的 `StructuredData` 與 builder。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web && npm run check:tasks
npm run build:web && npm --workspace @travel-scanner/web run start
curl -s localhost:3000/zh-TW/destinations | grep -c 'destinations/'
curl -s localhost:3000/zh-TW/destinations/tokyo | grep -E '<h1|rel="canonical"|TouristDestination'
curl -s localhost:3000/ja/destinations/kanazawa | grep -c 'application/ld+json'
curl -s -o /dev/null -w '%{http_code}\n' localhost:3000/zh-TW/destinations/not-a-city   # 期望 404
```

五個語系各抓一次指南頁，確認城市名、區域名與「為什麼去」都跟著語系變。
再把 `/zh-TW/destinations/tokyo` 的 JSON-LD 貼進 Google Rich Results Test，`TouristDestination` 與
`BreadcrumbList` 都要零錯誤。

## Notes

- **`apps/web/app/(stay22-public)` 整個目錄被 `2026-09-09-isolate-public-stay22-script`（review）鎖住，
  不可觸碰。** 新增的 `app/[locale]/destinations/[destinationId]/page.tsx` 與該 route group 底下的
  `.../services/page.tsx` 解析成不同 URL，不構成路由衝突；兩個 root layout 並存本來就是現況
  （`app/` 下沒有 root `layout.tsx`，這個形態今天就在 CI 裡 build 得過）。
- **動態 segment 必須叫 `[destinationId]`**，跟既有的 services 路徑一致。寫成 `[id]` 或 `[destination]`
  會讓 Next 報 "You cannot use different slug names for the same dynamic path"。
- scope 也不重疊：`tools/tasks.mjs` 的 `scopesOverlap` 是路徑前綴比對，
  `.../[destinationId]/page.tsx` 與 `.../[destinationId]/services/page.tsx` 互不為前綴。
  但**目錄形式的 `apps/web/app/[locale]/destinations` 會被拒絕**（它是被鎖住那條路徑的前綴），
  所以 scope 一定要逐檔列。
- **不要用 `generateStaticParams` + `dynamicParams: false`**：root layout 在 body 裡 `await cookies()`
  與 `headers()`，這棵樹下沒有任何東西會被預先產生，加了只是讓語意變模糊。
- `apps/web/app/[locale]/metadata.test.ts`（被 `2026-09-09-site-experience-settings` 認領，**不要改**）
  會自動走訪 `app/[locale]` 找出所有非動態路由並要求它們有自己的 metadata key。
  所以 `destinations/page.tsx` 必須在五個語系都補上唯一、且與其他頁不重複的 title/description，
  而且該檔的原始碼裡要留下 `title: t("destinationsTitle")` 這個字面
  （regex 是 `/title:\s*t\("([A-Za-z]+)"\)/`），否則會報 "has no generateMetadata"。
  `[destinationId]/page.tsx` 是動態 segment，被該測試的 `startsWith("[")` 判斷略過。
- **版面文案不要開新的 `messages/` namespace。** `tools/check-i18n.mjs` 會交叉比對
  `apps/web/lib/ui-text.ts` 的 `EDITABLE_NAMESPACES` 與 `apps/api/app/ui_text/schemas.py` 的
  `UI_TEXT_NAMESPACES`，新增 namespace 得同步改那兩個檔，等於把一個 api-area 的變更和兩個
  被別人認領的檔拉進這個 web 任務。只有 `metadata.json` 那兩個 key 非進 `messages/` 不可，
  因為 `metadata.test.ts` 只認它。
- `messages/` 整個目錄被 `2026-09-09-site-experience-settings`（blocked）與
  `2026-09-07-mokaair-community-web`（open）以前綴認領，兩者都不鎖 scope；
  `2026-09-07-merchant-style-discovery` 已明確把 `metadata.json` 排除在自己的 scope 之外。
  儘管如此還是盡快落地，那兩個任務隨時可能動起來。
- `apps/web/lib/destinations.ts` 的離線副本只有 19 個城市，比 API 的 33 個少。
  正常路徑一律用 API，離線副本只當降級用。
- `GET /api/v1/hotspots/{id}/place` 與 `/guides` 需要登入，**不能**用在公開頁；
  `/hotspots/{id}/intro` 與 `/hotspots/{id}/source` 是公開的。
- 導覽列或頁尾的入口刻意不做：那需要五個 `navigation.json`，正好是看板上第一順位的
  `2026-09-06-legal-content-from-owner` 的 scope。首頁的城市 chip 改指目的地頁則屬於
  `2026-09-10-seo-server-render-home-and-explore`（它持有 `app/[locale]/page.tsx`）。
