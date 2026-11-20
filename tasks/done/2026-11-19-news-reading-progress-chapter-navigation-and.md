---
id: 2026-11-19-news-reading-progress-chapter-navigation-and
title: News reading progress, chapter navigation and mobile tables
status: done
priority: P2
area: web
owner: codex-news-reading
claimed_at: 2026-11-19T00:04:12Z
created_at: 2026-11-19T00:03:57Z
completed_at: 2026-11-19T00:17:13Z
branch: codex/news-reading-controls-20261119
depends_on: []
scope:
  - apps/web/components/guides/article-toc-rail.tsx
  - apps/web/components/guides/article-toc-rail.test.tsx
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/components/guides/news-reading.module.css
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
  - apps/web/components/nav-menu.tsx
  - apps/web/components/nav-menu.test.tsx
---

# News reading progress, chapter navigation and mobile tables

## Why

On small screens, the chapter sheet lets keyboard focus move behind it and the floating controls cover the next stories. Reading progress counts the footer as part of the story. Long comparison tables introduce themselves after their data. The desktop header prefetches routes from collapsed menus while the reader is opening a story.

## Definition of done

- [x] Readers can finish the story at 100%, choose a chapter by keyboard and continue to another article without a floating control covering the recommendations.
- [x] Small-screen tables identify their subject first, fit two columns comfortably, and keep wider tables readable.
- [x] Collapsed desktop submenus generate no viewport prefetch. Opening one still exposes its links to the reader and to the router.

## Steps

- [x] Implement article-bound progress, chapter navigation, mobile tables and closed-menu layout.
- [x] Verify real article fixtures at phone and desktop widths, the five site locales, and keyboard navigation.

## How to verify

Run the web unit suite, lint, typecheck, production build and i18n parity. In the Dynamo and MDASH stories, read the table at 320px, open and dismiss the chapter list by keyboard, jump to a heading, and scroll to related stories. At desktop width check reading progress, submenu keyboard interaction and network activity with the header idle.

## Notes

Use the published article payloads in a local production build for repeatable viewport and network comparisons.

At 390px, the MDASH table shortened from 597px to 487px. At 320px it shortened from 759px to 628px. The three-column Dynamo table keeps its first column while panning. Both stories reached 100% at the end of the body and removed the floating control before related reading. Tab, Shift+Tab, Escape, backdrop and heading focus were checked in Chrome. Rotating into the desktop layout releases the modal.

Desktop cold-load prefetch in the replay went from 48 requests to 24. The eight AI submenu destinations prefetched on opening. This sample measures browser requests, not a live rate-limit outcome.

The older discovery draft #2061 touches the article components for editorial links. This branch is based on main and changes article bounds and reader controls independently.
