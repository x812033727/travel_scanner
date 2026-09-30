---
id: 2026-09-30-video-review-list-category-and-state
title: Video review list: category and state filters, search and paging
status: done
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-30T10:00:16Z
created_at: 2026-09-30T09:59:08Z
completed_at: 2026-09-30T10:34:07Z
branch: claude/nifty-heisenberg-0ldw0i
depends_on:
  - 2026-09-30-video-review-categories-column-browse-endpoint
scope:
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-browser.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/components/admin-guides-list.tsx
  - apps/web/lib/admin-workspace-navigation.ts
  - apps/web/messages
  - apps/web/e2e/admin-operations.spec.ts
  - apps/web/e2e/admin-video-manual-upload.spec.ts
  - tools/e2e-runtime-api.mjs
  - apps/web/components/admin-video-shorts.test.tsx
  - apps/web/components/admin-video-youtube.test.tsx
---

# Video review list: category and state filters, search and paging

## Why

The reviews tab of `/admin/videos` showed every tutorial as a large card in five fixed groups, with
no filter, search or paging, so once there are dozens of videos finding one and reading its state
takes scrolling. The API half (`2026-09-30-video-review-categories-column-browse-endpoint`) gives
each video a category and a paged catalog endpoint; this is the page.

## Definition of done

- [x] "需要你" and "可以上架" stay at the top as they were (cards, ReadyCard).
- [x] Under them, every tutorial is one line of a table (title, category, state, to decide,
      progress, YouTube, last synced) read from `GET /admin/videos/browse`.
- [x] Category pills (eight + 未分類) and state pills (進行中／已上架／已放棄) carry the server's
      counts; a title/slug search submits on Enter; previous/next paging; all in the URL
      (`category`, `state`, `q`, `page`), a page past the end falls back to the last.
- [x] The video's page has a category select; a content manager saves it
      (`PUT /admin/videos/{slug}/category`), a reader sees it disabled.
- [x] Five locales have the new `videoReviews` keys; no Chinese in `.tsx`.

## Steps

- [x] `VIDEO_CATEGORIES`, `category`, `VideoPage` types and `PublishPill` in admin-video-review-card.tsx.
- [x] `updateAdminQuery` moved to lib/admin-workspace-navigation.ts (guides list re-exports it).
- [x] New components/admin-video-browser.tsx: `VideoBrowser`, `CategoryPanel`, `CategoryPill`.
- [x] `ProjectList` keeps the two groups and renders the browser; `ProjectDetail` gets the panel.
- [x] Messages in en, zh-TW, ja, ko, zh-CN; vitest (29 cases in admin-video-reviews.test.tsx);
      browse mocks in the Shorts and YouTube tests, the two e2e specs and tools/e2e-runtime-api.mjs.

## How to verify

```bash
git add -A && npm run check:i18n && npm run lint:web && npm run typecheck:web && npm run test:web
```
Open `/zh-TW/admin/videos`: the two groups, then 全部影片 with pills, search and paging; the
URL follows the filters; on a video's page change 分類 and save, the row's pill changes.

## Notes

- The catalog reads again every 60 s like the groups, for the same query, and once more when a
  video is sent or linked from its card (`revision`); the search box keeps what is typed until Enter.
- The browser only lists `format = slides` without a Shorts line: dramas and Shorts have their tabs.
- The two top groups still come from `GET /admin/videos?shorts=exclude` (cap 200): a video that
  needs the owner is by construction recently reported, so the cap is not a problem today; revisit
  past ~150 tutorials.
- An API older than `/browse` shows the catalog's error state and leaves the groups working, so the
  API PR deploys first.
