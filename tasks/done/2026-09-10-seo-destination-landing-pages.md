---
id: 2026-09-10-seo-destination-landing-pages
title: 目的地索引頁與城市指南落地頁
status: done
priority: P1
area: web
owner: claude-opus-5-seo
claimed_at: 2026-09-10T17:50:09Z
created_at: 2026-09-10T16:43:42Z
completed_at: 2026-09-11T15:54:06Z
branch: claude/seo-optimization-planning-xq1vjl
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

- [x] `/{locale}/destinations` 依國家分組列出所有目的地，每筆連到自己的指南頁。
- [x] `/{locale}/destinations/{id}` 伺服器端渲染出：在地化城市名的 `<h1>`、為什麼去、區域清單、
      建議天數、時區與貨幣、熱門景點、代表店家。
- [x] 景點與店家**出現在原始 HTML 裡**（關掉 JS 也看得到），不是 hydration 後才 fetch。
- [x] 兩頁都有正確的 canonical、五語系 hreflang 與 `x-default`（沿用 `lib/seo.ts`）。
- [x] 兩頁都有 `BreadcrumbList`；指南頁另有 `TouristDestination`（`geo` 用 `center`）與景點 `ItemList`。
- [x] ~~`role: "extension"` 的目的地 canonical 指向其 `parent_destination_id`~~ —— **這一條做到一半推翻了，改成每個目的地都 canonical 指向自己**，理由見 Notes。母子關係改用雙向內部連結表達。
- [x] 未知的 `destinationId` 回 404（`notFound()`），不是空白頁。
- [x] 後端不可用時頁面仍可渲染核心目錄內容，景點／店家區塊優雅缺席。
- [x] `npm run check:i18n` 與未經修改的 `metadata.test.ts` 都通過。
- [x] `npm run build:web` 通過，與既有的 `/{locale}/destinations/{id}/services` 沒有路由衝突。

## Steps

- [x] **第一步先驗證路由能共存**：放一個空的 `app/[locale]/destinations/[destinationId]/page.tsx`
      跑一次 `npm run build:web`，確認沒有跟 route group 底下的 `/services` 衝突，再開始寫內容。
- [x] `apps/web/lib/destinations.server.ts`：照 `lib/hotspots.server.ts` 的既有形態
      （`API_INTERNAL_URL` + `X-Travel-Locale` header + `try/catch` 回 `null` + React `cache()` 去重），
      加上 `next: { revalidate: 3600 }`（目錄大約一季才變一次）。
      指南頁另外取 `GET /api/v1/hotspots/rankings?destination_id={id}&limit=12`（`revalidate: 900`）
      與 `GET /api/v1/foods/merchants?destination_id={id}&limit=12`。
      目錄查詢失敗時 fallback 到 `apps/web/lib/destinations.ts` 的離線副本。
- [x] `apps/web/lib/destinations-copy.ts`：區塊標題等版面文案，locale-keyed TS 物件，
      形態比照既有的 `lib/discovery-copy.ts` / `lib/stay22-script-copy.ts` / `lib/frontend-flow-copy.ts`。
      **不要新增 `messages/` namespace**（理由見 Notes）。
- [x] `apps/web/components/destination-guide.tsx`：純呈現，一個 `<h1>` + 數個 `<h2>` 分區
      （住哪裡 / 看什麼 / 吃什麼 / 規劃行程 / 鄰近延伸），內部連結指向
      `/{locale}/hotspots?destination_id={id}&area=…`、`/{locale}/foods`、
      既有的 `/{locale}/destinations/{id}/services`、以及 `/search/new`。
      母目的地用 `extension_ids` 連向延伸目的地，延伸目的地反向連回母目的地。
- [x] 兩個 `page.tsx`。指南頁用 `if (!PUBLIC_DESTINATIONS.includes(destinationId)) notFound();` 驗證，
      形態與既有的 services 頁一致。
- [x] 五個 `messages/*/metadata.json` 補 `destinationsTitle`、`destinationsDescription` **兩個 key**。
- [x] 把 `/destinations` 與 33 筆指南頁 append 進 `app/sitemap.ts` 的 `SITEMAP_ROUTES`。
- [x] 掛上 `2026-09-10-seo-structured-data` 建好的 `StructuredData` 與 builder。

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

### 實作結果（2026-09-10, claude-opus-5-seo）

**路由共存已由 build 證實。** `npm run build:web` 同時列出三條：

```
├ ƒ /[locale]/destinations
├ ƒ /[locale]/destinations/[destinationId]
├ ƒ /[locale]/destinations/[destinationId]/services
```

新的指南頁在 `app/[locale]/`，`/services` 在 `app/(stay22-public)/[locale]/` route group，兩個 root layout
並存沒有衝突。實測 `/zh-TW/destinations/tokyo/services` 仍回 200。動態 segment 必須叫
`[destinationId]`（與既有那條一致），否則 Next 會報 "different slug names for the same dynamic path"。

**推翻了原本的 extension canonical 設計。** 原訂 `role: "extension"` 的目的地 canonical 指向母目的地。
實作完、驗證通過之後才想清楚這是錯的：rel=canonical 是給**重複或近乎重複**的頁面用的，而橫濱和東京
是兩個不同城市——名稱、座標、內容都不同。把橫濱 canonical 到東京，若 Google 採信就等於主動讓一個
合法頁面消失；若不採信（更可能，因為兩頁並不重複）則是一段無效標記。extension 真正的風險是
**內容單薄**，而單薄的解法是補內容或 noindex，不是跨頁 canonical。

改成每一頁都 canonical 指向自己，母子關係用雙向內部連結（指南頁的「鄰近目的地」區塊）表達。
這也讓 sitemap 保持誠實：列進去的每一條都是自己的 canonical。

**站台文案沒有開新的 `messages/` namespace。** 區塊標題放在 `lib/destinations-copy.ts`，形態比照
`lib/stay22-script-copy.ts`。只有 `destinationsTitle` / `destinationsDescription` 兩個 key 進
`messages/metadata.json`，因為 `metadata.test.ts` 只認那裡——而它會自動走訪找到新的
`destinations/page.tsx` 並要求五語系都有唯一的 title/description，這次 1775 個測試全綠代表它滿意了。

**跨任務落地的兩處**（兩個任務都仍由本人持有，同一個分支）：

- `lib/structured-data.ts` 補上 `itemList` 與 `touristDestination` 兩個 builder（含測試）。
  `2026-09-10-seo-structured-data` 當時刻意沒做，理由是「沒有帶 URL 的清單項目就不值得標記」；
  目的地索引頁正是第一個項目真的有自己網址的清單，條件成立了。
- `app/sitemap.ts` 補上 `/destinations` 與 33 條 `/destinations/{id}`。指南頁 priority 0.7、
  `/services` 維持 0.4——後者是同一座城市的聯盟住宿目錄，該排在自己的指南頁下面。

**API 契約逐欄確認過**：`GET /api/v1/destinations`（`apps/api/app/places/router.py:292`）依
`X-Travel-Locale` 一次回齊 city / local_name / english_name / country / areas / reason /
recommended_days / timezone / currency / center / role / parent_destination_id / extension_ids，
而 `apps/api/app/destinations/localized.py` 有 `validate_localized_catalog()` 保證 33 個目的地
× 5 語系齊備。所以這兩頁不需要自己的城市名翻譯表。

**降級行為分三種，不是兩種。** 第一版把「目錄整個讀不到」和「目錄讀到了但沒有這個 slug」混成同一條
路徑，兩者都丟例外。做完整份 sitemap 的逐條 HTTP 稽核時才發現這是錯的：33 條指南頁裡有 29 條回 500，
因為驗證用的 stub 目錄只有 4 個目的地。正式環境的 API 有全部 33 個所以不會發生，但這暴露一個真實風險
——`PUBLIC_DESTINATIONS`（前端的 33 個 slug）和 API 目錄一旦漂移，我卻正在用 sitemap 叫 Google
去爬那些網址，它們會回 500。

兩種失敗是可以區分的，因為 `loadDestinations()` 回 `null` 代表整份目錄讀不到，回陣列但找不到 id
代表漂移。現在：

| 情況 | 回應 | 理由 |
| --- | --- | --- |
| 目錄讀不到（冷快取 + API 掛掉） | 5xx | 「稍後再來」。404 會邀請 Google 移除一個真實頁面 |
| 目錄讀到了但沒有這個 slug | 404 | 這個目的地是真的不存在，誠實回答 |
| slug 根本不在 `PUBLIC_DESTINATIONS` | 404 | 同上，而且更早就擋掉 |
| 索引頁遇到目錄讀不到 | 200 + 離線副本 19 個城市 | 少幾個城市好過一片空白 |

另外發現一個沒預期到但很有用的性質：**只要目錄曾經被快取過，API 掛掉不會讓目的地頁掛掉**——
`next: { revalidate }` 是 stale-while-revalidate，會繼續送上一份好的資料。5xx 只在「冷快取 + API 同時掛掉」
才會發生。對 SEO 來說這比每次後端抖動就一片 5xx 好得多。

### 驗證紀錄

`npm run lint:web`、`npm run check:i18n`、`npm run typecheck:web` 通過；
`npm run test:web` 203 個檔案 1775 個測試全綠；`npm run build:web` 通過。
新增 28 個測試（server loader 11、guide 元件 7、copy 10），其中 copy 測試有一條專門抓
「key 齊全但內容還是英文」的情形。

因為本機沒有後端，另外寫了一支 stub API（scratchpad，未進 repo）提供
`/destinations`、`/hotspots/rankings`、`/foods/merchants`、`/runtime/site-visibility`，
對 production build 實測：

- `/zh-TW/destinations/tokyo` 的原始 HTML 含 `<h1>東京</h1>` 與五個 `<h2>`（住哪一區／看什麼／
  吃什麼／規劃這趟行程／鄰近目的地），景點「淺草寺」「澀谷 Sky」、店家「一蘭 新宿」、
  以及 `Asia/Tokyo`、`JPY`、`4–6` 全部在伺服器輸出裡，不是 hydration 後才出現。
- canonical 指向自己，五語系 hreflang + `x-default` 齊全。
- `TouristDestination` 帶 description、`alternateName: ["東京"]`（英文頁上與 name 相同的
  `english_name` 被濾掉）、`containedInPlace`、`geo`。索引頁帶 `ItemList` 與 `BreadcrumbList`。
- `/zh-TW/destinations/not-a-city` 回 404；`/zh-TW/destinations/tokyo/services` 回 200。
- `/en`、`/ja` 的城市名與頁面標題都跟著語系變（`<title>旅行先ガイド｜Mokaair</title>`）。

### 追加驗證（2026-09-10，修正 404/500 之後）

把 stub 擴充成供應全部 33 個 slug 之後，對 production build 逐條稽核整份 sitemap：

```
checked 365 URLs, 0 non-200
```

365 = 73 條路由 × 5 語系。另外兩項交叉檢查也都乾淨：

- sitemap 裡沒有任何一條網址帶 `noindex`（0 contradictions）。
- sitemap 裡沒有混進 `/login`、`/register`、`/account`、`/trips`、`/alerts`、`/my`、`/admin`、
  `/search`、`/share` 任何一條。

冷快取 + API 關閉時實測：指南頁 500、索引頁 200 且列出 19 個離線城市、`/foods` 200。
API 開著但目錄沒有該 slug 時：404。

**殘留風險**：`PUBLIC_DESTINATIONS` 與 API 目錄的一致性目前沒有自動化守門，靠的是兩邊都源自
同一份 catalog。漂移的後果現在是 404 而不是 500，但 sitemap 仍會列出那條網址。
要根治得有一個跨語言的比對測試（讀 `apps/api/app/destinations/catalog.py` 的 id 與
`PUBLIC_DESTINATIONS` 對照），評估後認為那種 regex 解析 Python 的測試太脆，先記在這裡而不做。

**測試覆蓋的界線**：404 與 5xx 的分岔是三行內嵌在 page 裡的邏輯，用單元測試包起來需要 mock 掉整個
server component 的相依，代價不成比例。它的輸入（`loadDestinations` 回 `null` 還是陣列）有單元測試，
分岔本身則以上面對 production build 的實測為證。

## 標記完成（由站主授權，非原持有者）

這張任務的工作已隨 PR #388 於 2026-09-11 合併進 main：merge commit `d0ec33e` 的第二個 parent 就是分支 head `999dbc5`，分支上每個 commit 都在 main 裡，分支也已刪除。該 head 的每個 check 都通過（`api`、`web`、`containers`、`full-stack-smoke`、`discovery-browser`、`planner-browser`）。狀態卻一直停在 `review`，持有的 scope 因此擋住後續任務，2026-09-11 由 claude-opus-5 移到 done。

若原持有者 `claude-opus-5-seo` 尚有未推送的後續工作，請重新開一張任務，不要把這張改回 review。
