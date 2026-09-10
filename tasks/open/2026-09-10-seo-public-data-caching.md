---
id: 2026-09-10-seo-public-data-caching
title: 公開資料改用 revalidate 快取，並把 /foods 店家列表放進 SSR
status: review
priority: P2
area: web
owner: claude-opus-5-seo
claimed_at: 2026-09-10T18:08:12Z
created_at: 2026-09-10T16:43:50Z
completed_at:
branch: claude/seo-optimization-planning-xq1vjl
depends_on: []
scope:
  - apps/web/lib/hotspots.server.ts
  - apps/web/lib/hotspots.server.test.ts
  - apps/web/lib/foods.server.ts
  - apps/web/lib/foods.server.test.ts
  - apps/web/components/food-browser.tsx
  - apps/web/components/food-browser-seed.test.tsx
  - apps/web/app/[locale]/foods/page.tsx
---

# 公開資料改用 revalidate 快取，並把 /foods 的店家列表放進 SSR

## Why

兩個問題，同一個成因：伺服器端資料取用一律 `cache: "no-store"`，而且只取一半。

**一、每次請求都回源。** `lib/hotspots.server.ts`、`lib/foods.server.ts`、
`lib/site-visibility.server.ts`、`lib/site-pages.server.ts` 全部帶 `cache: "no-store"`。
這些是公開、非個人化、變動極慢的資料（景點排行一天變幾次、店家目錄一週變幾次），卻每一次頁面請求
都同步等後端回應。這是 TTFB 的主要來源，而 TTFB 直接進 LCP。

站台其餘部分是 per-request SSR 的設計選擇（root layout 讀 session cookie、`proxy.ts` 每次請求
產生 CSP nonce），**不建議為了 SEO 去拆**。但「不能快取 HTML」不等於「不能快取資料」。

**二、`/foods` 的實際內容不在 HTML 裡。** `lib/foods.server.ts` 只餵了
`/foods/cities` 與 `/foods/categories`，真正的店家列表是 `components/food-browser.tsx` 在
`useEffect` 裡打 `/foods/merchants` 拿的。所以 `/{locale}/foods` 對爬蟲來說是一個只有篩選器的空殼——
而它是站台目前少數幾個可索引且有內容的頁面之一。`lib/hotspots.server.ts` 已經用
`initialRanking` 做對了同一件事，照抄即可。

## Definition of done

- [x] 公開資料取用改成 `fetch(url, { next: { revalidate: N } })`，不再是 `cache: "no-store"`。
- [x] `/{locale}/foods` 的伺服器端 HTML 含店家列表第一頁。
- [x] 個人化或帶登入身分的請求**維持** `no-store`，不得被快取污染。
- [x] 後端不可用時各頁的降級行為不變（回 null、頁面照樣渲染）。

## Steps

- [x] `lib/foods.server.ts` 加第三支 server fetch（`/foods/merchants?limit=20`），
      以 `initialMerchants` 傳進 `FoodBrowser`，比照 `HotspotExplorer` 收 `initialRanking` 的形狀。
- [x] `FoodBrowser` 接受 `initialMerchants` 當首屏資料，掛載後仍照舊依篩選條件重新查詢。
- [x] 為每一支公開端點挑一個合理的 `revalidate`：目的地目錄約一季才動一次（3600s 以上），
      景點排行 900s，店家目錄 900s。`site-visibility` 是功能開關，維持 `no-store`。
- [x] 補測試涵蓋「初始資料有渲染出來」與「快取選項正確」。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web && npm run check:tasks && npm run build:web
npm --workspace @travel-scanner/web run start
curl -s localhost:3000/zh-TW/foods | head -c 4000     # 必須看得到店家名稱
```

用 `curl -w '%{time_starttransfer}\n' -o /dev/null` 對 `/zh-TW/hotspots` 連打幾次，
第二次之後的 TTFB 應該明顯下降。

## Notes

- **只快取公開資料。** 任何帶 `travel_access` cookie、`Authorization` 或使用者身分的請求都必須
  維持 `no-store`；`revalidate` 的快取是跨使用者共享的。
- `apps/web/components/food-browser.tsx` 被 `2026-09-07-merchant-style-discovery`（open）認領。
  open 不鎖 scope，但認領前請確認它沒有動起來。
- 這個任務不依賴其他 SEO 任務，可以最先做，也可以跟 canonical 那條平行進行。
- 本任務**刻意不碰** `next.config.ts` 的 `images` 設定。所有 `next/image` 呼叫端
  （`hotel-offer-card.tsx`、`search-experience.tsx`、`account-list.tsx`、`trip-editor.tsx`、
  `shared-trip-view.tsx`）都已明確帶 `unoptimized`，而且五個全在登入後、掛 `noindex` 的頁面上，
  加 `remotePatterns` 既不會生效也不會改善任何可索引頁的 CWV。

### 實作結果（2026-09-10, claude-opus-5-seo）

- `lib/hotspots.server.ts` 與 `lib/foods.server.ts` 的 `cache: "no-store"` 換成
  `next: { revalidate }`：分類與城市清單 3600 秒（很少變），排行與店家清單 900 秒（每天變）。
  `site-visibility` 與 `site-pages` 不動——前者是功能開關，後者本來就 `no-store` 且有自己的理由。
- `/foods` 的伺服器端多取一支 `/foods/merchants?limit=20`（**只取無篩選的第一頁**），
  以 `initialMerchants` 傳進 `FoodBrowser`，形態比照既有的 `initialRanking` 餵 `HotspotExplorer`。
  客戶端只在「這位讀者也沒有帶篩選條件」時才重用它，判斷方式是
  `merchantsQuery(initialFilters) === merchantsQuery(readFoodBrowserFilters(""))`；
  網址帶了篩選就照舊自己查。爬蟲一律是無篩選進來，所以它拿到的是有內容的頁面而不是一排空篩選器。
- 客戶端測試另開 `components/food-browser-seed.test.tsx`，因為既有的
  `components/food-browser.test.tsx` 屬於 `2026-09-07-merchant-style-discovery` 的 scope。

### 驗證時踩到的兩個坑（都值得記下來）

1. **Next 的 fetch cache 存在 `.next/cache/fetch-cache`，重啟 server 也不會清掉。**
   第一次驗證時 stub API 完全沒收到 `/foods/merchants` 請求，但 HTML 裡卻有店家名稱——
   因為那是更早一輪跑出來、寫進磁碟的快取。要驗「冷啟動會不會真的去取」必須先
   `rm -rf .next/cache/fetch-cache`。
2. **舊的 `next start` 佔著 3000 埠時，新的啟動會失敗但 curl 照樣有回應**，量到的是舊 build。
   這一輪又中了一次。另外 `pgrep -f 'next-server'` 會匹配到執行這行指令的 shell 自己，
   把自己殺掉；用 `PAT=$(printf 'next-%s' server)` 之類在執行期才組出字串的寫法可以避開。

### 驗證紀錄

`npm run lint:web`、`npm run typecheck:web` 通過；`npm run test:web` 206 個檔案 1791 個測試全綠。
新增 12 個測試（foods.server 5、hotspots.server 3、food-browser 種子 4）。

清空 `.next/cache/fetch-cache` 後對 production build 實測：

- 冷啟動載入 `/ko/foods`，stub 收到三支請求，全部帶 `locale=ko`：
  `/foods/cities`、`/foods/categories`、`/foods/merchants?limit=20`，
  而店家名稱出現在伺服器輸出的 HTML 裡。
- 同一頁再載入兩次，stub 收到 **0** 支 `/api/v1/foods` 請求。
- **快取有依語系分開**：`/zh-TW/foods` 顯示「一蘭 新宿」、`/en/foods` 顯示 "Ichiran Shinjuku"，
  `/zh-TW/hotspots` 顯示「淺草寺」、`/en/hotspots` 顯示 "Sensoji"，`locale=ko` 也是獨立取一次。
  這一點特別確認過——共用快取若只用 URL 當 key，就會把某個語系的資料餵給其他語系的讀者。
