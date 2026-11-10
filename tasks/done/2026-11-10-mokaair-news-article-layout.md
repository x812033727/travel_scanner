---
id: 2026-11-10-mokaair-news-article-layout
title: Implement approved Mokaair news and article layouts
status: done
priority: P1
area: web
owner: codex-news-layout
claimed_at: 2026-11-10T11:31:26Z
created_at: 2026-11-10T11:30:52Z
completed_at: 2026-11-10T12:05:41Z
branch: codex/mokaair-news-layout-20261110
depends_on: []
scope:
  - apps/web/components/guides/news-list.tsx
  - apps/web/components/guides/news-list.test.tsx
  - apps/web/components/guides/news-desk.tsx
  - apps/web/components/guides/news-desk.test.tsx
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/components/guides/topic-hub-page.tsx
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/app/[locale]/life/page.test.tsx
  - apps/web/e2e/guides-adsense.spec.ts
  - docs/mokaair-news-layout.md
---

# Implement approved Mokaair news and article layouts

## Why

The owner approved the Mokaair news-list and article preview after studying Kocpc's news hierarchy. The current list only shows dates and titles. Implement clearer article discovery and a comfortable reading layout using the site's existing content and five-language UI.

## Definition of done

- [x] News uses a lead story, thumbnails, descriptions and usable topic links, preserving event-date chronology and pagination.
- [x] Lifestyle articles provide readable typography, a desktop contents rail and a folded mobile contents list; travel and series behavior remains intact.
- [x] Relevant checks and desktop/mobile browser verification pass; a reviewable PR carries the implementation without merging or deploying.

## Steps

- [x] Check active branches, worktrees, remote heads and open PR file scopes; create isolated worktree from b5f713f57.
- [x] Implement news and article layouts with existing catalog strings and content.
- [x] Validate components, five-language catalogs, build and browser interactions.
- [x] Record evidence and open a PR with no-auto-merge.

## How to verify

Run web lint, i18n, TypeScript, unit tests, production build, task checks and the existing guides-adsense Playwright spec. Inspect news and article screenshots on desktop/mobile; test event dates, cross-topic deduplication, pagination, missing images, deliberate scrolling and contents targets.

## Notes

- Owner authorization: implement approved preview and prepare review. Merge/deployment are separate.
- Claim completed without force. The blocked reader-support ticket holds no active scope; its existing integration is preserved. No matching open PR changed the UI paths at the initial audit.
- Article layout delegated to article_layout (four article files); browser fixture/testing to news_layout_e2e (guides-adsense.spec.ts); root owns news integration and this record.
- No fabricated popularity, author, summary, dates, artwork or advertisement placeholders. Existing ads and contextual affiliate behavior remain intact.
- The life page test scope was added after existing assertions proved tied to the former date/title-only row; assertions will retain chronology and URL checks while accepting the approved descriptions.
- Validation: 123 distinct focused unit cases passed (73 article, 47 news/topic/life, 3 AI rails); final news-only rerun 8 passed. Full web ESLint passed, final changed-file lint passed, five locales/25 namespaces passed, TypeScript and 371-route webpack production build passed. Task validation passed for 2,389 files (existing unrelated stale/overlapping claim warnings remain).
- Full desktop/mobile browser suite: 34 passed, exit 0. Visual review then found clipped lead focus and cropped diagram edges; the correction uses an unclipped card and aspect-video/object-contain images, with mobile title first. The 6 affected browser cases passed again with explicit focus-clipping, image-fit and order checks.
- Final isolated capture: 16 pages and 18 PNGs across all five locales, desktop/mobile/320px/dark, zero page errors, keyboard focus clippedBy=[]. Root and independent layout_review both inspected final images; no blocking visual findings. Original captures are preserved in before-fix/.
- Local evidence: `<home>/.codex/tmp/mokaair-news-layout-20261110/` (build-final.log, before-fix/, final/e2e-results.json, final/visual-results.json and PNGs). All browser/fixture processes were closed.
- Pre-PR audit repeated: origin/main still b5f713f57; no matching open PR scope or competing news/layout branch. Initial parallel broad guide-test attempt was interrupted during memory pressure; it is not counted as a pass. All relevant focused cases were completed separately.
- PR: https://github.com/x812033727/travel_scanner/pull/2061, opened with no-auto-merge. CI is tracked on the PR; closing this implementation ticket does not authorize merge or deployment.
