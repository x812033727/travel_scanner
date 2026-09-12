---
id: 2026-09-11-guide-lastmod-republication
title: Sitemap lastmod should move when a guide translation is republished
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-11T16:08:54Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/service.py
  - apps/api/app/guides/schemas.py
  - apps/api/tests/test_guides.py
  - apps/web/lib/guides.server.ts
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
---

# Sitemap lastmod should move when a guide translation is republished

## Why

sitemap 的攻略條目用 API 的 `published_at` 當 `lastmod`（見 `2026-09-11-guides-sitemap`）。但 `published_at`
是該語系**第一次**發布的時間：`apps/api/app/guides/admin_service.py:208-210` 重新發布時保留原值，
`apps/api/tests/test_guides.py:289-290` 也斷言撤下後再發布會沿用原日期。

所以編輯修訂一篇已發布的文章（例如情報的票價更新）之後，`lastmod` 不會前進，Google 沒有理由提早重新抓取。
而時效性正是情報區存在的理由。

## Definition of done

- [ ] `GET /api/v1/guides/sitemap` 的每一筆多一個欄位，記錄目前公開版本上線的時間：重新發布會前進，撤下不會。
- [ ] 網頁端 sitemap 的攻略條目 `lastmod` 改用這個時間；`published_at` 仍是首次發布日，列表與文章頁顯示的
      發布日期不受影響。
- [ ] API 測試涵蓋「重新發布後這個時間前進、`published_at` 不變」；`sitemap.test.ts` 涵蓋網頁端用的是新欄位。

## Steps

- [ ] `service.sitemap_entries` 一併取出目前 `published_version` 對應的 `GuideArticleRevision.created_at`
      （`action == "published"`），加進 `SitemapEntry`。
- [ ] `schemas.SitemapEntry` 新增欄位；網頁端 `guideSitemapEntries()` 的驗證與型別跟著改，欄位缺席時退回
      `published_at`，這樣 API 與網頁哪個先部署都不會讓 sitemap 掉條目。
- [ ] 需要的話，文章頁的 `Article` JSON-LD 可以用同一個時間補上 `dateModified`
      （`app/[locale]/guides/[kind]/[slug]/page.tsx`，不在本票 scope，要做先擴 scope）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides.py -k sitemap
cd apps/web && npx vitest run app/sitemap.test.ts lib/guides.server.test.ts
```

## Notes

- 目前公開版本的 revision 在 `service._published_document` 已經有現成查法
  （`GuideArticleRevision.version == row.published_version` 且 `action == "published"`），
  它的 `created_at` 就是這一版上線的時間。
- 只改 sitemap 的 `lastmod`，不要改 `published_at` 的語意：列表的排序與分頁游標
  （`service.py:140-226`）都依賴它是首次發布日。
