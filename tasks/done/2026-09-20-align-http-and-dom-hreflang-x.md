---
id: 2026-09-20-align-http-and-dom-hreflang-x
title: Align HTTP and DOM hreflang x-default
status: done
priority: P2
area: web
owner: claude-opus-5-5
claimed_at: 2026-09-30T00:29:45Z
created_at: 2026-09-20T05:49:02Z
completed_at: 2026-09-30T00:48:30Z
branch: claude/hreflang-single-source
depends_on: []
scope:
  - apps/web/i18n/routing.ts
  - apps/web/e2e/hreflang-header.spec.ts
---

# Align HTTP and DOM hreflang x-default

## Why

Production article QA found two different `x-default` targets on the same localized
guide response. The DOM metadata points to the published English article, while the
HTTP `Link` header emitted by locale middleware points to the unprefixed guide path.
Search crawlers must receive one consistent reciprocal alternate set, and article
alternates must remain publication-aware rather than advertising drafts.

## Definition of done

- [x] HTTP and DOM alternate declarations use the same English `x-default` URL.
- [x] Article responses advertise only locales that are actually published.
- [x] Static fully localized pages retain their complete reciprocal alternate set.

## Steps

- [x] Reproduce the mismatch in a request-level test for a localized guide article.
- [x] Configure the locale proxy so its response header cannot contradict page metadata.
- [x] Cover guide, life and static-page behavior in SEO tests.

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
- 2026-09-30 (claude-opus-5-5): still reproduced on production before the fix,
  and worse than first reported: a zh-TW-only article's `Link` header listed
  all five locales, advertising four unpublished translations. The fix sets
  next-intl's `alternateLinks: false`, so the middleware emits no hreflang
  header; page metadata (publication-aware, x-default on English, unit-tested
  in the guides and life `page.test.tsx`) and the sitemap are the only sets.
- Scope narrowed from `proxy.ts` + `seo.spec.ts` to `routing.ts` + a new
  `e2e/hreflang-header.spec.ts`: `seo.spec.ts` sits in the active scope of
  `2026-09-22-destination-services-pages-differ-only-by`, and `proxy.ts`
  needed no change. The e2e fixture API has no article documents, so the
  article DOM sets stay covered by the unit tests; the spec checks the header
  on a static, a how-to, an intel and a life route plus the static page's DOM.
- Verified: new spec 10/10 on a served build (desktop and mobile); the header
  case fails against production as expected; related vitest 60/60; lint and
  typecheck clean. After deploy, recheck `curl -sI` for no hreflang `Link`.
