---
id: 2026-09-10-seo-server-render-home-and-explore
title: 首頁與 explore 要在伺服器端渲染出真正的內容
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-10T16:49:04Z
completed_at:
branch:
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

- [ ] `curl -s localhost:3000/zh-TW` 的輸出含 hero `<h1>` 與目的地連結列（關掉 JS 也看得到）。
- [ ] `curl -s localhost:3000/en/explore` 的輸出含 feed 第一頁的實際項目，不是骨架。
- [ ] 功能開關關閉時，伺服器端直接渲染「關閉」狀態，不再先送骨架再切換。
- [ ] `/explore` 與 `/explore/collections` 移除 `noindex`，並加進 `SITEMAP_ROUTES`。
- [ ] 首頁輸出 `Organization` 與 `WebSite`（含 `potentialAction: SearchAction`）JSON-LD。
- [ ] 首頁的城市 chip 從 `/hotspots?destination_id={id}` 改指 `/destinations/{id}`（若目的地頁已上線）。
- [ ] 首屏不再出現骨架 → 內容的整頁位移。

## Steps

- [ ] 新增 `apps/web/lib/discovery.server.ts`，照 `lib/site-visibility.server.ts` 的既有形態
      （`API_INTERNAL_URL` + `try/catch` + React `cache()`）在伺服器端解析 discovery 開關。
- [ ] 把解析結果當成初始值餵進 store，讓 `getServerSnapshot` 回傳真實狀態而不是寫死的 `loading: true`。
      現成範本是 root layout 已經在做的 `<SiteVisibilityProvider state={siteVisibility}>`。
- [ ] `/explore` 比照 `getInitialHotspots` 餵 `/hotspots` 的做法，在伺服器端先取
      `GET /api/v1/discovery/feed?mode=latest` 的第一頁當初始資料。
- [ ] 移除兩個 explore 頁的 `robots: { index: false }`，並 append 進 `app/sitemap.ts` 的 `SITEMAP_ROUTES`。
- [ ] 首頁掛上 `2026-09-10-seo-structured-data` 建好的 JSON-LD builder。
- [ ] 更新／新增測試。**不要動 `app/[locale]/page.test.tsx`**（見 Notes）。

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
