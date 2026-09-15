---
id: 2026-09-10-seo-open-content-pages
title: 讓 pet-friendly 與社群內容頁先 SSR 再開放索引
status: review
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-14T13:01:17Z
created_at: 2026-09-10T16:43:42Z
completed_at:
branch: claude/gifted-archimedes-1zfznf
depends_on:
  - 2026-09-10-seo-index-directives
scope:
  - apps/web/components/community/page.tsx
  - apps/web/components/community/page.test.tsx
  - apps/web/components/community/pets.tsx
  - apps/web/components/community/post.tsx
  - apps/web/components/community/profile.tsx
  - apps/web/components/community/use-resource.ts
  - apps/web/app/[locale]/pet-friendly/page.tsx
  - apps/web/app/[locale]/pet-friendly/[id]/page.tsx
  - apps/web/app/[locale]/community/posts/[id]/page.tsx
  - apps/web/app/[locale]/community/profiles/[handle]/page.tsx
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
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

- [x] 四條路由的主要內容都在伺服器端 HTML 裡（關掉 JS 也看得到）。
- [x] 每頁的 `<title>` 與 meta description 反映該筆內容本身（文章標題、地點名稱、使用者顯示名），
      不再是共用字串。
- [x] `communityMetadata()` 接受 `index` 選項且**預設 `false`**，`admin/community` 與
      `admin/pet-friendly` 兩個呼叫端不必修改就維持 `noindex`。
- [x] 社群功能開關關閉（`COMMUNITY_ENABLED=false`）時，這些頁仍然 `noindex`。
- [x] 開放索引的路由 append 進 `app/sitemap.ts` 的 `SITEMAP_ROUTES`。

## Steps

- [x] 新增 `apps/web/lib/community/public.server.ts`，照 `lib/hotspots.server.ts` 的既有形態，
      在伺服器端取 `GET /api/v1/pet-friendly/places`、`/pet-friendly/places/{uuid}`、
      `/community/posts/{uuid}`、`/community/profiles/{handle}`（四支都是公開端點）。
- [x] 把結果當 initial props 傳進既有的 client component，維持 hydration 後的互動不變。
- [x] `communityMetadata(title, { index = false } = {})`，並讓四條路由依實際內容組出標題與描述。
- [x] `robots` 綁 `getCommunityState()`：功能關閉時仍回 `index: false`。
- [x] 補測試（新檔）。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web && npm run check:tasks && npm run build:web
npm --workspace @travel-scanner/web run start
curl -s localhost:3000/en/pet-friendly | grep -c 'noindex'   # 必須是 0
curl -s localhost:3000/en/pet-friendly | head -c 4000        # 必須看得到地點名稱
```

再取一篇實際貼文的 UUID，確認 `<title>` 是那篇的標題而不是「貼文 | Mokaair」。

## Notes

### 收尾紀錄（claude-opus-5, 2026-09-14）

- **`CommunityGate` 本來就擋不住伺服器端渲染。** 原本擔心 gate 會讓 SSR 內容出不來，實測不會：
  沒有 `travel_access` cookie 的訪客（爬蟲就是）在 layout 拿到 `hasSession=false`，
  `HeaderSessionProvider` 的初始 status 直接是 `signed_out` 而不是 `loading`，
  `member={false}` 的 gate 於是直接放行 children。真正的空殼成因只有一個：
  內容元件在 `useEffect` 裡才發請求。所以這次沒有動 `shell.tsx`。
- **`robots.index` 綁的是「伺服器端這次真的拿到內容了嗎」，不只是開關。**
  開關關閉、API 連不上、404（草稿／隱藏貼文）三種情況都回 `null`，四條路由一律維持
  `noindex, follow`，標題退回區段共用字串。這比只看 `getCommunityState()` 嚴格，
  也讓「可索引」與「HTML 裡有內容」永遠是同一個答案。
- **`/community/posts/{id}` 不必自己判斷草稿。** API 的 `published_post()` 對所有人
  （含作者）強制 `state == "published"`，其餘一律 404；而這裡的伺服器端讀取不帶 cookie，
  拿到的必然是公開版本。草稿與隱藏貼文因此自動落在 `null` 分支。
- **`useResource` 的 seed 綁在「第一次的 path」上。** 直接用 `initial` 當 fallback 會有個
  實際的 bug：讀者在 `/pet-friendly` 送出篩選後 `path` 變了，舊的未篩選第一頁會在新請求
  飛行中被當成結果顯示，等於把他剛篩掉的清單又貼回去。改成只有 `path` 仍等於首次算繪的
  path 時才套用 seed。用 `useState` 而不是 `useRef` 記那個 path：算繪期間讀 ref 會被
  `react-hooks/refs` 擋下（lint 已抓到一次）。
- **順手修掉重複 `<h1>`。** 三條詳情路由的 `CommunityPage` 會先印一個區段標題 `<h1>`，
  底下的元件又印一個記錄名稱 `<h1>`，等於每頁兩個、而且第一個在整個區段裡都一樣。
  新增 `heading` 選項，詳情頁傳 `false`，目錄頁維持原樣。
- **canonical / hreflang 不用動。** layout 的 `generateMetadata` 已經用
  `x-travel-pathname` 算出真實路徑，四條路由自動拿到 self-canonical 與五語言 + x-default，
  實測確認過。
- 詳情頁（place / post / profile）尚未進 sitemap，另開
  `2026-09-14-sitemap-lists-pet-friendly-places`（P3）。`/pet-friendly` 目錄頁有連到每一筆
  地點，所以在那之前不是孤島。

### 實測（`next start` + stub API）

`API_INTERNAL_URL` 指向一支假 API，量到的結果：

| 狀態 | robots | `<title>` |
| --- | --- | --- |
| 社群開啟、有內容 | `index, follow` | 記錄自己的名字 |
| 社群關閉 | `noindex, follow` | 區段共用字串 |
| API 連不上 | `noindex, follow` | 區段共用字串 |

四條路由關掉 JS 都看得到主要內容（地點名、地址、貼文標題與內文、顯示名與自介），
每頁剛好一個 `<h1>`；社群關閉時 `sitemap.xml` 不含 `/pet-friendly`，開啟時五個語言各一筆。

### 動到的檔案比原本 scope 多

原 scope 少了 `pets.tsx` / `post.tsx` / `profile.tsx` / `use-resource.ts`，但 Steps 寫的
「把結果當 initial props 傳進既有的 client component」本來就得改它們；`app/sitemap.ts`
也是 DoD 要求卻不在清單裡。已把六個檔案補進 scope，確認過沒有任何 active 任務認領它們
（`2026-09-07-mokaair-community-web` 是 `open`，不鎖 scope；`2026-09-09-site-experience-settings`
認的是 `community/home.tsx` 與 `ui.tsx`，沒有重疊）。

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
