---
id: 2026-09-10-seo-server-render-home-and-explore
title: 首頁與 explore 要在伺服器端渲染出真正的內容
status: done
priority: P1
area: web
owner: claude-opus-5-seo
claimed_at: 2026-09-13T15:10:18Z
created_at: 2026-09-10T16:49:04Z
completed_at: 2026-09-13T22:53:43Z
branch: claude/explore-server-render
depends_on:
  - 2026-09-09-frontend-flow-discovery-web
  - 2026-09-09-discovery-card-details
  - 2026-09-10-seo-structured-data
scope:
  - apps/web/lib/discovery.ts
  - apps/web/lib/discovery.server.ts
  - apps/web/lib/discovery.server.test.ts
  - apps/web/components/discovery/explorer.tsx
  - apps/web/app/[locale]/explore/page.tsx
  - apps/web/app/[locale]/explore/collections/page.tsx
  - apps/web/components/discovery/explore-ssr.test.tsx
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
---

# 首頁與 explore 要在伺服器端渲染出真正的內容

## Why

首頁的伺服器端 HTML **永遠**是一塊骨架，不分功能開關狀態。

`apps/web/lib/discovery.ts`：

```ts
const closed = { enabled: false, loading: true };
export function useDiscoveryStatus() {
  return useSyncExternalStore(subscribe, () => status, () => closed);
}
```

第三個參數是 `getServerSnapshot`，它回傳的 `closed` 帶著 `loading: true`。所以在伺服器上
`DiscoveryHomeGate`（`components/discovery/explorer.tsx:29`）永遠走 `loading` 分支：

```tsx
return loading ? <main className={styles.page}><DiscoverySkeleton /></main> : enabled ? <DiscoveryExplorer home /> : children;
```

`app/[locale]/page.tsx` 裡的 `<h1>`、hero 文案、七國十九城的連結列——全部不在回應內容裡。
`DiscoveryExplorer` 有同樣的判斷，所以 `/explore` 與 `/explore/collections` 也一樣。
現有測試之所以綠燈，是因為 `app/[locale]/page.test.tsx:7` 直接 mock 掉那個 hook。

後果有三層，而且互相加乘：

1. **SEO**：站台首頁沒有任何可索引內容。所有內部連結的起點也一起消失，爬蟲從首頁挖不到 `/hotspots`、
   `/foods` 或任何城市頁。這比 canonical 的問題更根本。
2. **LCP**：讀者先看到骨架，等 `/discovery/status` 回來才換成真內容。
3. **CLS**：骨架換成真內容是一次整頁位移。

`/explore` 與 `/explore/collections` 目前掛著 `robots: { index: false }`。在伺服器端真的渲染得出內容
之前，那個 `noindex` 是對的——先解決 SSR，再談索引。

## Definition of done

- [x] ~~`curl -s localhost:3000/zh-TW` 的輸出含 hero `<h1>` 與目的地連結列~~ —— **已由
      `2026-09-10-seo-home-ssr-and-internal-links` 的繞道解決**（discovery 關閉時不再包 gate）。
- [x] `curl -s localhost:3000/en/explore` 的輸出含 feed 第一頁的實際項目，不是骨架。
- [x] 功能開關關閉時，伺服器端直接渲染「關閉」狀態，不再先送骨架再切換。
- [x] `/explore` 移除 `noindex` 並加進 `SITEMAP_ROUTES`（都綁 discovery 開關）。
      **`/explore/collections` 刻意不改**，理由見下方「與 DoD 不同的地方」。
- [x] ~~首頁輸出 `Organization` 與 `WebSite` JSON-LD~~ —— 已由 `2026-09-10-seo-structured-data` 完成（放在 gate 外面）。
- [x] ~~首頁的城市 chip 改指 `/destinations/{id}`~~ —— 已由 `2026-09-10-seo-home-ssr-and-internal-links` 完成。
- [x] 首屏不再出現骨架 → 內容的整頁位移。

## Steps

- [x] 開關的伺服器端解析沿用既有的 `lib/discovery-status.server.ts`（繞道那次已經建好），
      新的 `lib/discovery.server.ts` 只負責 feed 的第一頁。
- [x] 解析結果以 prop 傳入（不是餵進 store，理由見下），讓伺服器端輸出真實狀態。

- [x] `/explore` 比照 `getInitialHotspots` 餵 `/hotspots` 的做法，在伺服器端先取
      `GET /api/v1/discovery/feed` 的第一頁當初始資料（用該網址真正對應的 mode，不是寫死 latest）。
- [x] `/explore` 的 robots 與 sitemap 都綁 discovery 開關。
- [x] ~~首頁掛上 JSON-LD builder~~ —— 早已完成，見上方 DoD。
- [x] 更新／新增測試。沒有動 `app/[locale]/page.test.tsx`。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web && npm run check:tasks && npm run build:web
npm --workspace @travel-scanner/web run start
curl -s localhost:3000/zh-TW      | grep -c '<h1'          # 必須 >= 1
curl -s localhost:3000/zh-TW      | grep -c 'application/ld+json'
curl -s localhost:3000/en/explore | grep -c 'noindex'      # 必須是 0
```

再用瀏覽器停用 JavaScript 打開首頁，應該看得到完整的 hero 與連結，而不是灰色方塊。

## Notes

- 本任務 `depends_on` 兩個 review 中的任務。`apps/web/components/discovery/explorer.tsx` 被
  `2026-09-09-frontend-flow-discovery-web` 與 `2026-09-09-site-experience-settings` 認領、
  `apps/web/lib/discovery.ts` 被 `2026-09-09-discovery-card-details` 認領，前兩者中
  **`2026-09-09-frontend-flow-discovery-web` 與 `2026-09-09-discovery-card-details` 是 review 狀態、會鎖住 scope**，
  所以在它們合併之前 `npm run tasks -- claim` 會直接拒絕。這是預期行為，不要用 `--force` 繞過。
- `app/[locale]/page.test.tsx` 被 `2026-09-09-frontend-flow-discovery-web`（review）與
  `2026-09-09-site-experience-settings` 認領，不在本任務 scope 裡。新測試請開新檔。
  順帶一提，那個檔正是目前 mock 掉 `useDiscoveryStatus` 讓問題長期沒被發現的地方——
  合併後值得補一個「伺服器端輸出含 `<h1>`」的測試。
- 這是整份 SEO 規劃裡效益最高的一項，但也是唯一一項現在完全被別人的分支擋住的。
  其餘任務都可以先行，不需要等它。
- `2026-09-10-seo-open-content-pages`（社群與寵物友善內容頁）踩到同一個坑：那些頁面也是
  client component 進 `useEffect` 抓資料。兩個任務的處理原則一樣——**先做 SSR，再談索引**。

### 範圍收斂（2026-09-10, claude-opus-5-seo）

首頁那一半已經解決了，但**是繞過去的，不是修好的**。
`2026-09-10-seo-home-ssr-and-internal-links` 新增 `lib/discovery-status.server.ts`
在伺服器端解析開關，讓 `app/[locale]/page.tsx` 在 discovery 關閉時直接渲染行銷首頁，
不包 `DiscoveryHomeGate`。因為 `DISCOVERY_ENABLED` 預設 false，正式環境的首頁因此有了內容。

**本任務剩下的是繞不過去的那一半**，仍然要等
`2026-09-09-frontend-flow-discovery-web` 與 `2026-09-09-discovery-card-details` 合併：

1. **根治 `getServerSnapshot`。** `lib/discovery.ts` 回傳寫死的 `{ loading: true }`，
   所以 **discovery 開啟時**首頁與 explore 的伺服器輸出依舊是骨架。要把伺服器端解析出來的值
   餵進 store（現成範本是 root layout 的 `<SiteVisibilityProvider state={siteVisibility}>`）。
   繞道之後這件事只影響「開啟」狀態，優先度因此下降。
2. **`/explore` 與 `/explore/collections` 的 SSR。** 內容在 `DiscoveryExplorer` 裡，
   那個元件在被鎖住的 `explorer.tsx`，**沒有繞道空間**。這兩頁維持 `noindex`。
3. 上述完成後才把兩頁加進 `app/sitemap.ts` 的 `SITEMAP_ROUTES` 並移除 `noindex`。

`app/[locale]/page.tsx` 已不在本任務 scope（改動落在 `2026-09-10-seo-structured-data`
與 `2026-09-10-seo-home-ssr-and-internal-links`），scope 已相應收斂。

### 做法與決定（2026-09-13, claude-opus-5-seo）

**與 DoD 不同的地方：`/explore/collections` 維持 `noindex`，也不進 sitemap。**
這一頁不是「內容在 hydration 之後才抓」的空殼，它是**每位讀者自己的收藏工作區**
（`DiscoveryCollections` 未登入時只給一個登入按鈕，登入後是本人的 saved items）。
沒有公開版本可以在伺服器端渲染，也沒有任何匿名爬蟲該看到的東西。它屬於 `/account`、
`/trips` 那一類，跟開關無關。已在該檔與 `app/sitemap.ts` 寫下理由。

**開關用 prop 傳，不餵進 module store。** `lib/discovery.ts` 的 store 是 module 層級的，
在伺服器上由同一個容器裡**所有請求共用**；一次失敗的讀取會替其他請求回答。
所以 `getServerSnapshot` 維持寫死的 `loading: true`，改由 `resolveDiscoveryStatus(live, initialEnabled)`
在元件裡合併：store 還在 loading 且有伺服器值時用伺服器值。伺服器與 hydration 首次渲染
結果相同（那時 store 必定還在 loading），所以這只改回應內容，不改 hydration 後的樹。

**只預取 feed，不預取 search。** `GET /discovery/search` 的第一頁會記一筆 `discovery_search`；
已登入讀者的瀏覽器還會用自己的身分再送一次，兩邊都送等於同一次搜尋算兩次。
帶 `q=` 的網址 canonical 本來就指回 `/explore`，沒有東西要索引。`mode=following` 同理跳過：
伺服器不讀 cookie，那個排序渲染出來是登入提示。

**預取的是匿名排序，而且瀏覽器照樣會自己再要一次。**（2026-09-14 CI 之後改的：原本會跳過
那次請求。）`publicServerHeaders` 只轉發位址與 UA、不帶 cookie，所以伺服器渲染的是登出狀態的
排序；瀏覽器那次是走 BFF、帶著自己的 session，答案才是這個元件該顯示的東西。伺服器那份只負責
**第一次繪製**，不是替代品。`e2e/discovery.spec.ts` 用 `page.route` 攔瀏覽器的請求塞測試資料，
伺服器端那次攔不到——跳過瀏覽器請求等於讓那批測試看不到自己的 fixture，CI 的 discovery-browser
就是這樣紅的。順帶一提，**空的 feed 不傳過去**：拿「這裡還沒有內容」蓋掉骨架比骨架更糟。

**path 當快取鍵。** `discoveryFeedPath()` 與 fetch 分開，兩個呼叫端（`generateMetadata` 與頁面本體）
用同一個字串當 React `cache()` 的鍵，不必賭 `await searchParams` 兩次拿到同一個物件。
`lib/discovery.server.test.ts` 拿真的 `discoveryQuery()`（client 模組）逐字比對，
因為伺服器模組不能呼叫 `"use client"` 的函式，只能靠測試守住兩邊不飄移。

**`/explore` 的 robots**：discovery 開著**且**伺服器真的取到 feed 才可索引。開關關著時
這一頁是那張 fallback 連結格（連到的頁本來就各自在 sitemap 裡），沒有自己的內容可排名。
sitemap 那邊只看開關——讀不到 API 時照樣列出，與 guides hub 的降級方向一致。

### 還沒做的

- 本機 `npm run typecheck:web` 有一個與本任務無關的既有錯誤：`components/shared-trip-view.tsx`
  找不到 `qrcode`（本機安裝過舊）。
- 沒有實際跑起 `next start` 用 curl 驗證（需要可連到的 API）。SSR 輸出改由
  `components/discovery/explore-ssr.test.tsx` 以 `renderToString` 斷言。
- **首頁在 discovery 開啟時仍然只 SSR 出外框加骨架**：`DiscoveryHomeGate` 現在會在伺服器端
  渲染出 explorer 的標題與篩選列，但沒有 feed 第一頁，因為 `app/[locale]/page.tsx` 不在本任務
  scope 裡。要補的話就是照 `/explore` 的兩行：`discoveryFeedPath()` + `getInitialDiscoveryFeed()`
  傳進 `DiscoveryHomeGate`。開關關著時首頁本來就是行銷首頁，所以這件事今天沒有影響。
- 本分支疊在 `claude/guides-empty-locale-hubs`（PR #464）上，因為兩者都動 `app/sitemap.ts`。
  `npm run check:tasks` 因此會警告這兩張票的 scope 重疊——是預期的，兩張都在同一個人手上，
  #464 併入後這裡 rebase 就沒事了。
