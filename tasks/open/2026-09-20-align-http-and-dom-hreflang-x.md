---
id: 2026-09-20-align-http-and-dom-hreflang-x
title: Align HTTP and DOM hreflang x-default
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-20T05:49:02Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/i18n/routing.ts
  - apps/web/proxy.ts
  - apps/web/e2e/seo.spec.ts
---

# Align HTTP and DOM hreflang x-default

## Why

Production article QA found two different `x-default` targets on the same localized
guide response. The DOM metadata points to the published English article, while the
HTTP `Link` header emitted by locale middleware points to the unprefixed guide path.
Search crawlers must receive one consistent reciprocal alternate set, and article
alternates must remain publication-aware rather than advertising drafts.

## Definition of done

- [ ] HTTP and DOM alternate declarations use the same English `x-default` URL.
- [ ] Article responses advertise only locales that are actually published.
- [ ] Static fully localized pages retain their complete reciprocal alternate set.

## Steps

- [ ] Reproduce the mismatch in a request-level test for a localized guide article.
- [ ] Configure the locale proxy so its response header cannot contradict page metadata.
- [ ] Cover guide, life and static-page behavior in SEO tests.

## How to verify

Run the focused web tests and inspect the production-style response `Link` header and
rendered `<link rel="alternate">` elements for one five-language article and one
partially published article.

## Notes

Observed during batch 001 production QA on 2026-09-20. For
`/zh-TW/guides/howto/taichung-sun-moon-lake-2-day`, the DOM `x-default` was
`/en/guides/howto/taichung-sun-moon-lake-2-day`, while the HTTP `Link` header used
the unprefixed `/guides/howto/taichung-sun-moon-lake-2-day`. The five requested
locale alternates were otherwise complete and correct, so this did not block that
content batch.
