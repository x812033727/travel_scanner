---
id: 2026-09-11-guide-lastmod-republication
title: Sitemap lastmod should move when a guide translation is republished
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-12T17:42:17Z
created_at: 2026-09-11T16:08:54Z
completed_at: 2026-09-12T17:55:02Z
branch: claude/travel-guide-10-posts-56a1a9
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

- [x] `GET /api/v1/guides/sitemap` 的每一筆多一個欄位，記錄目前公開版本上線的時間：重新發布會前進，撤下不會。
- [x] 網頁端 sitemap 的攻略條目 `lastmod` 改用這個時間；`published_at` 仍是首次發布日，列表與文章頁顯示的
      發布日期不受影響。
- [x] API 測試涵蓋「重新發布後這個時間前進、`published_at` 不變」；`sitemap.test.ts` 涵蓋網頁端用的是新欄位。

## Steps

- [x] `service.sitemap_entries` outer join `GuideArticleRevision`（`version == published_version`、
      `action == "published"`），`SitemapEntry.modified_at = coalesce(revision.created_at, published_at)`。
- [x] `schemas.SitemapEntry` 新增 optional 欄位；網頁端 `guideSitemapEntries()` 只在字串可解析時帶上
      `modified_at`，`sitemap.ts` 用 `modified_at ?? published_at`，API 與網頁哪個先部署都不掉條目。
- [x] `PublishedDocument.modified_at` 同一個時間，文章頁顯示「更新日期」、`Article` JSON-LD 帶 `dateModified`
      （與 rich-blocks 任務同一個 PR，scope 在該任務）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides.py -k "sitemap or modified_at"
cd apps/web && npx vitest run app/sitemap.test.ts lib/guides.server.test.ts
```

## Notes

- 目前公開版本的 revision 在 `service._published_document` 已經有現成查法
  （`GuideArticleRevision.version == row.published_version` 且 `action == "published"`），
  它的 `created_at` 就是這一版上線的時間。
- 只改 sitemap 的 `lastmod`，不要改 `published_at` 的語意：列表的排序與分頁游標
  （`service.py:140-226`）都依賴它是首次發布日。
- 2026-09-13 做完：`modified_at` 也進了 `PublishedDocument`，所以文章頁與 JSON-LD 一起拿到；
  sitemap 用 outer join 而不是子查詢，指標壞掉的列只失去 lastmod、不失去網址。
