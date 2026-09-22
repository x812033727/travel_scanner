---
id: 2026-09-22-fix-desktop-global-search-placeholder-icon
title: Fix desktop global search placeholder icon overlap
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-22T08:19:52Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/site-search/site-search.tsx
  - apps/web/components/site-search/site-search.test.tsx
---

# Fix desktop global search placeholder icon overlap

## Why

At the desktop viewport, the global article search magnifier overlaps the start
of the placeholder. This was observed in all five languages during the batch015
published-article and batch016 private-page visual checks on 2026-09-22. It is a
shared header issue; the article body and private draft protection passed.

## Definition of done

- [ ] The search icon and placeholder have clear separation in all five locales.
- [ ] Typed search text and focus styles remain readable on desktop and mobile.

## Steps

- [ ] Reproduce against the current header and inspect icon/input spacing.
- [ ] Make the narrow layout correction and check existing search interactions.

## How to verify

Render the signed-out global header at 1440px and 390px in zh-TW, zh-CN, en,
ja and ko. Check the empty field, entered text and keyboard focus. Run scoped
web lint/type checking and the existing site-search tests if touched.

## Notes

Observed deployed revision: d5f03e679bef2102e843426c42f045aef4ae08c0.
Evidence: `C:/Users/x8120/.codex/article-localization-release/batch015/public-qa-after-publish-20260922T0808`
and `batch016-llms/privacy-after-import-20260922T0808` under the same release root.
The private-page visual receipt SHA256 is
`e30c223090b26b8f46a76b1325cab76d8b017c73c1fee81bee910e072e67cb6b`.
No shared header implementation was changed during those content releases.
