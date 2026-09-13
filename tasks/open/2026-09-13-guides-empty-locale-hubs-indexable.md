---
id: 2026-09-13-guides-empty-locale-hubs-indexable
title: 非 zh-TW 的空文章 hub 可被索引又列在 sitemap
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-13T05:16:19Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/[locale]/guides/page.tsx
  - apps/web/app/[locale]/guides/[kind]/page.tsx
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

- [ ] 某語系、某個 hub **確定沒有已發布文章**時，該頁輸出 `robots: { index: false, follow: true }`，sitemap 也不列它。
- [ ] **API 失敗不等於空**：現在 `loadGuideList`（`lib/guides.server.ts:66-76`）和 `guideSitemapEntries`（`:160-164`）
      失敗時都回空陣列。直接拿「空」當判斷，一次 API 故障就會把 zh-TW 的 hub 全部 noindex、從 sitemap 拿掉。
      要先讓兩者能分辨「失敗」與「確定是空的」；失敗時維持現狀，也就是照常可索引、照常列入 sitemap。
- [ ] 有文章的語系（目前是 zh-TW）行為完全不變。
- [ ] `docs/seo.md` 的表格補上 hub 在空語系的規則。

## Steps

- [ ] `guides.server.ts`：清單與 sitemap 載入器回傳可分辨失敗的結果，更新呼叫端與測試。
- [ ] 三個 hub 頁的 `generateMetadata` 依結果決定 robots（React `cache()` 讓同一請求不會重打 API）。
- [ ] `sitemap.ts`：hub 路徑只列給有文章的語系，而且 intel、howto、life 分開算；載入失敗時退回列出全部。
- [ ] `sitemap.test.ts`、`e2e/seo.spec.ts`（`:54` 起會數 sitemap 的 URL 數）跟著改。

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
