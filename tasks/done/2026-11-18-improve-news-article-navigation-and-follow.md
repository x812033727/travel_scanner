---
id: 2026-11-18-improve-news-article-navigation-and-follow
title: Improve news article navigation and follow-up reading
status: done
priority: P2
area: web
owner: codex-news-reader
claimed_at: 2026-11-18T09:36:05Z
created_at: 2026-11-18T09:35:22Z
completed_at: 2026-11-18T09:50:46Z
branch: codex/news-reader-followthrough-20261118
depends_on: []
scope:
  - apps/web/components/guides/news-list.tsx
  - apps/web/components/guides/news-list.test.tsx
  - apps/web/components/guides/channel-guide.tsx
  - apps/web/components/guides/topic-hub-page.test.tsx
  - apps/web/vitest.setup.tsx
  - apps/web/app/[locale]/life/page.test.tsx
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/api/app/guides/links.py
  - apps/api/tests/test_guides_links.py
---

# Improve news article navigation and follow-up reading

## Why

Scrolling a channel on a phone can fetch stories the reader never opens. The mobile news diagrams are hard to read in the article column. The GPT-6.2 launch and system-card articles also link to the same four broad recommendations and omit each other.

## Definition of done

- [x] List headlines expose their localized destinations in server HTML and only request those stories when opened.
- [x] Readers can open the large original body figure on a dated news story and return to the article.
- [x] Strongly matching recent coverage wins over broad topic matches. Editorial choices and language availability keep precedence.

## Steps

- [x] Exercise localized headline links and large body images in the production frontend build.
- [x] Exercise related-article ordering, availability and fallback on the backend.

## How to verify

Run the news list, life hub, content block and article page Vitest suites. Run the guides link/API tests, web lint, typecheck, build, i18n parity and task-board checks. In mobile Chrome, scroll an AI channel before clicking a headline. On each illustrated article, open the original PNG and use Back.

## Notes

The older video tasks claiming message directories work on video-admin copy. This change adds only the shared article image label. Existing news discovery drafts remain separate. The mobile comparisons use a local production build and captured public data to avoid sending test traffic through the public rate limiter.

On a 390 px Chrome viewport, scrolling the same 24-story channels and their illustrated guide before clicking generated 26 to 0 article requests for AI and 27 to 0 for tech. Clicking the lead in each fetched one HTML document. The 240 news URLs and ten guide URLs matched across five locales. Both 1600 by 900 PNG originals opened at 320 and 390 px, with JavaScript enabled and disabled. Back returned to the figure.

Replaying 48 published article identities and 240 translations from the two channel front pages against the local resolver produced 960 localized recommendations. The GPT launch and system-card stories ranked each other first in all five languages. A control run using topic fallback alone left each outside the other's four slots.
