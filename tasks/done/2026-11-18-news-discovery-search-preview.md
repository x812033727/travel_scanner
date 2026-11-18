---
id: 2026-11-18-news-discovery-search-preview
title: Improve news discovery and AI news search and share previews
status: done
priority: P2
area: web
owner: codex-news-discovery
claimed_at: 2026-11-18T06:29:03Z
created_at: 2026-11-18T06:28:12Z
completed_at: 2026-11-18T06:50:03Z
branch: codex/news-discovery-seo-20261118
depends_on: []
scope:
  - apps/web/app/[locale]/page.tsx
  - apps/web/components/discovery/explorer.tsx
  - apps/web/components/discovery/home-gate.test.tsx
  - apps/web/e2e/frontend-flow.spec.ts
  - apps/web/components/home-guides.tsx
  - apps/web/components/home-portal-tabs.tsx
  - apps/web/components/home-guides.test.tsx
  - apps/web/app/[locale]/page.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/app/(ads-public)/[locale]/guides/[kind]/[slug]/page.test.tsx
  - apps/web/components/guides/topic-hub-page.tsx
  - apps/web/components/guides/topic-hub-page.test.tsx
  - apps/web/messages/zh-TW/metadata.json
  - apps/web/messages/zh-CN/metadata.json
  - apps/web/messages/en/metadata.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ko/metadata.json
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/app/[locale]/life/page.test.tsx
  - apps/web/components/guides/ai-hub-rails.tsx
  - apps/web/components/guides/ai-hub-rails.test.tsx
  - apps/web/components/guides/news-list.tsx
  - apps/web/components/guides/news-list.test.tsx
  - apps/web/lib/structured-data.ts
---

# Improve news discovery and AI news search and share previews

## Why

The homepage could hide a current headline when the editor also featured it elsewhere. The news desk linked to the top of the lifestyle section, and news channels shared the same generic guide title in search. Stories without editorial photography inherited the website share card.

## Definition of done

- [x] The latest dated stories and links to populated channels appear in the homepage HTML. A reader can follow a headline to its article with JavaScript disabled.
- [x] News channel search titles describe their beat in all five languages. A published story has its own share title, summary, URL, dates, and language alternatives.

## Steps

- [x] Reserve overview positions for dated news before deduplicating other sections. Keep the complete editorial selections on the individual tabs.
- [x] Provide one main landmark and one page heading for the homepage across both discovery states. Show the first dated story with its summary on the lifestyle and AI hubs.
- [x] Describe the visible news sequence in the lifestyle page's JSON-LD and retain the existing availability checks for feeds, indexing and translations.

## How to verify

Run the web tests, type check, lint, production build, and `npm run check:i18n`. From the homepage follow a news channel and an article, then follow the lifestyle and AI hub leads. Inspect the canonical and share metadata with and without an article image.

## Notes

Local Chrome testing used published-content fixtures at 1440, 390 and 320 CSS pixels. The narrowest viewport was tested with JavaScript disabled. The mobile channel's first headline was visible before scrolling. Search CTR and readership require post-release data.
The two video-worker claims cover the entire messages directory for admin text. This branch edits only the public metadata catalogues, which are separate files.
