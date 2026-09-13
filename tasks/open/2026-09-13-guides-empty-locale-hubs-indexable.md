---
id: 2026-09-13-guides-empty-locale-hubs-indexable
title: 非 zh-TW 的空文章 hub 可被索引又列在 sitemap
status: review
priority: P3
area: web
owner: claude-opus-5-seo
claimed_at: 2026-09-13T15:13:26Z
created_at: 2026-09-13T05:16:19Z
completed_at:
branch: claude/guides-empty-locale-hubs
depends_on: []
scope:
  - apps/web/app/[locale]/guides/page.tsx
  - apps/web/app/[locale]/guides/page.test.tsx
  - apps/web/app/[locale]/guides/[kind]/page.tsx
  - apps/web/app/[locale]/guides/[kind]/page.test.tsx
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/app/[locale]/life/page.test.tsx
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
  - apps/web/e2e/seo.spec.ts
  - tools/e2e-runtime-api.mjs
  - docs/seo.md
---

# 非 zh-TW 的空文章 hub 可被索引又列在 sitemap

## Why

做 AdSense 評估（`docs/adsense-feasibility.md`）時順帶發現的。2026-09-13 正式站的狀況：

- 30 篇文章全部只有 zh-TW。
- `https://mokaair.com/en/guides` 回 200，內容只有一句「Nothing is published here yet.」，
  沒有 robots meta，canonical 指向自己，而且 `app/sitemap.ts:47-53` 把 `/guides`、`/guides/intel`、
  `/guides/howto`、`/life` 列給五個語系。
- `/life` 在所有語系都是空的（生活分享 0 篇）。

對搜尋引擎，這是一批被主動送去索引的空頁（soft 404、薄內容）。對 AdSense，這是「無內容畫面」，不能放廣告。
`docs/seo.md:30-31` 只寫了文章「只在已發布的語系可索引」，沒有交代 hub 空了該怎麼辦。

## Definition of done

- [x] 某語系、某個 hub **確定沒有已發布文章**時，該頁輸出 `robots: { index: false, follow: true }`，sitemap 也不列它。
- [x] **API 失敗不等於空**：現在 `loadGuideList`（`lib/guides.server.ts:66-76`）和 `guideSitemapEntries`（`:160-164`）
      失敗時都回空陣列。直接拿「空」當判斷，一次 API 故障就會把 zh-TW 的 hub 全部 noindex、從 sitemap 拿掉。
      要先讓兩者能分辨「失敗」與「確定是空的」；失敗時維持現狀，也就是照常可索引、照常列入 sitemap。
- [x] 有文章的語系（目前是 zh-TW）行為完全不變。
- [x] `docs/seo.md` 的表格補上 hub 在空語系的規則。

## Steps

- [x] `guides.server.ts`：清單與 sitemap 載入器回傳可分辨失敗的結果，更新呼叫端與測試。
- [x] 三個 hub 頁的 `generateMetadata` 依結果決定 robots（React `cache()` 讓同一請求不會重打 API）。
- [x] `sitemap.ts`：hub 路徑只列給有文章的語系，而且 intel、howto、life 分開算；載入失敗時退回列出全部。
- [x] `sitemap.test.ts`、`e2e/seo.spec.ts`（`:54` 起會數 sitemap 的 URL 數）跟著改。

## How to verify

```bash
cd apps/web && npx vitest run lib/guides.server.test.ts app/sitemap.test.ts "app/[locale]/life/page.test.tsx"
npm run lint:web && npm run typecheck:web
```

部署後：`curl -s https://mokaair.com/en/guides | grep -o '<meta name="robots"[^>]*>'` 出現 noindex；
`curl -s https://mokaair.com/zh-TW/guides` 沒有；`curl -s https://mokaair.com/sitemap.xml | grep -c '/en/guides'` 為 0。

## Notes

- `/guides` 總 hub 同時列 intel 與 howto，兩者都空才算空。
- `seo.spec.ts` 在停用 JavaScript 下跑，e2e fixture API 的文章清單要能各給出一個空、一個有內容的語系。

### 做法與決定（2026-09-13, claude-opus-5-seo）

- `loadGuideList` 多回一個 `available`，`guideSitemapEntries` 改回 `{ entries, complete }`。
  只有「API 真的答了」才算數：`hubIsEmpty(...lists)` 要求每一份清單都 `available` 且為空，
  所以 `/guides` 這種跨兩個 kind 的 hub，只要有一邊讀不到就維持可索引。
- `complete` 除了失敗，**被 1000 筆上限截斷時也是 false**。被丟掉的是最舊的那些，
  而某語系唯一一篇文章完全可能就在裡面；截斷的答案不能當成「這個語系沒有」。
- sitemap 的 hub 改成「每語系」而不是「每路由」列出，`SitemapRoute.hub` 寫出這個 hub 靠哪些 kind
  才算有東西（`/guides` 是 intel + howto）。同時 hub 的 hreflang 只列出真的被列出的語系，
  `x-default` 只在英文也在裡面時才給——否則等於在 sitemap 裡推薦一個自己剛判定 noindex 的頁。
- e2e fixture 本來沒有 `/api/v1/guides` 清單端點（hub 頁一律讀失敗），所以補了一個，
  而且刻意讓它跟既有的 `/api/v1/guides/sitemap` fixture 完全一致：intel 在 zh-TW 與 ja、
  howto 在 en、life 在 zh-TW。兩個端點若各說各話，頁面與 sitemap 會互相矛盾。
- 兩個測試檔（`guides/page.test.tsx` 新開、`guides/[kind]/page.test.tsx`）加進 scope：
  前者原本不存在，`/guides` hub 的 robots 規則否則沒有任何測試；後者的 `vi.mock` 把整個
  `guides.server` 換掉，`hubIsEmpty` 會變成 undefined，非改不可。兩個檔都改成
  `...await original()` 只蓋掉兩個讀取函式，讓 `hubIsEmpty` 用真的那一份。

### 還沒做的

- 本機 `npm run typecheck:web` 另有一個與本任務無關的既有錯誤：`components/shared-trip-view.tsx`
  找不到 `qrcode`。`apps/web/package.json` 有這個相依，是本機安裝過舊，不是這次改動造成的。
- Playwright 沒有在本機跑（需要起 production build 與 fixture API）。`e2e/seo.spec.ts` 的
  URL 總數已按 fixture 重算為 `5 * (7 + 33 + 33) + 7 + 4`，但要等 CI 的瀏覽器套件確認。
