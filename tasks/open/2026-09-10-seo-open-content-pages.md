---
id: 2026-09-10-seo-open-content-pages
title: 讓 pet-friendly 與社群內容頁先 SSR 再開放索引
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-10T16:43:42Z
completed_at:
branch:
depends_on:
  - 2026-09-10-seo-index-directives
scope:
  - apps/web/components/community/page.tsx
  - apps/web/components/community/page.test.tsx
  - apps/web/app/[locale]/pet-friendly/page.tsx
  - apps/web/app/[locale]/pet-friendly/[id]/page.tsx
  - apps/web/app/[locale]/community/posts/[id]/page.tsx
  - apps/web/app/[locale]/community/profiles/[handle]/page.tsx
  - apps/web/lib/community/public.server.ts
  - apps/web/lib/community/public.server.test.ts
---

# 讓 pet-friendly 與社群內容頁可被索引

## Why

`/{locale}/pet-friendly`、`/{locale}/pet-friendly/{id}`、`/{locale}/community/posts/{id}`、
`/{locale}/community/profiles/{handle}` 是站台僅有的原創長文內容——經查證的寵物規定、旅人遊記、
公開個人檔案——目前全部掛著 `robots: { index: false }`。

但**單純把 `noindex` 拿掉會讓情況更糟**，因為這些頁面根本沒有伺服器端內容。
`components/community/` 底下 29 個檔案有 19 個是 `"use client"`，其中包含 `pets.tsx`、`post.tsx`、
`profile.tsx`、`shell.tsx`。以寵物詳情頁為例，整頁就是：

```tsx
export const generateMetadata = () => communityMetadata("pets");
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <CommunityPage title="pets" member={false}><PetDetails id={id} /></CommunityPage>;
}
```

`PetDetails` 在 `useEffect` 裡才打 `/pet-friendly/places/{id}`。伺服器送出去的是一個標題加一層 gate。
先拿掉 `noindex` 只會把一批空頁塞進索引，換來 Search Console 的「軟性 404」與薄內容評價。

另外 `communityMetadata()` 的標題也全是固定字串（`"貼文 | Mokaair"`），每篇文章的標題都一樣，
即使被索引也無法區分。

## Definition of done

- [ ] 四條路由的主要內容都在伺服器端 HTML 裡（關掉 JS 也看得到）。
- [ ] 每頁的 `<title>` 與 meta description 反映該筆內容本身（文章標題、地點名稱、使用者顯示名），
      不再是共用字串。
- [ ] `communityMetadata()` 接受 `index` 選項且**預設 `false`**，`admin/community` 與
      `admin/pet-friendly` 兩個呼叫端不必修改就維持 `noindex`。
- [ ] 社群功能開關關閉（`COMMUNITY_ENABLED=false`）時，這些頁仍然 `noindex`。
- [ ] 開放索引的路由 append 進 `app/sitemap.ts` 的 `SITEMAP_ROUTES`。

## Steps

- [ ] 新增 `apps/web/lib/community/public.server.ts`，照 `lib/hotspots.server.ts` 的既有形態，
      在伺服器端取 `GET /api/v1/pet-friendly/places`、`/pet-friendly/places/{uuid}`、
      `/community/posts/{uuid}`、`/community/profiles/{handle}`（四支都是公開端點）。
- [ ] 把結果當 initial props 傳進既有的 client component，維持 hydration 後的互動不變。
- [ ] `communityMetadata(title, { index = false } = {})`，並讓四條路由依實際內容組出標題與描述。
- [ ] `robots` 綁 `getCommunityState()`：功能關閉時仍回 `index: false`。
- [ ] 補測試（新檔）。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web && npm run check:tasks && npm run build:web
npm --workspace @travel-scanner/web run start
curl -s localhost:3000/en/pet-friendly | grep -c 'noindex'   # 必須是 0
curl -s localhost:3000/en/pet-friendly | head -c 4000        # 必須看得到地點名稱
```

再取一篇實際貼文的 UUID，確認 `<title>` 是那篇的標題而不是「貼文 | Mokaair」。

## Notes

- **順序是硬性的：先 SSR，再拿掉 `noindex`。** 兩件事必須在同一次變更裡完成，
  中間不要有「已可索引但還沒 SSR」的狀態上線。
- 社群目前是 `COMMUNITY_ENABLED=false` 的私有 rollout。README 也載明公開社群啟用前要先完成
  驗收清單、審核人力與法律頁面。**本任務不得順手打開任何功能開關**，只負責讓開關打開時
  這些頁面是可被正確索引的。
- `apps/web/components/community`（整個目錄）與 `apps/web/app/[locale]/pet-friendly`、
  `apps/web/app/[locale]/community` 被 `2026-09-07-mokaair-community-web`（open）以前綴認領。
  open 不鎖 scope，但認領前請先確認它沒有動起來。
- `/explore` 與 `/explore/collections` 有一模一樣的問題，但成因在 discovery store 的
  `getServerSnapshot`，已獨立成 `2026-09-10-seo-server-render-home-and-explore`，不在本任務範圍。
