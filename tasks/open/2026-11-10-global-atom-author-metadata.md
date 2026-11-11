---
id: 2026-11-10-global-atom-author-metadata
title: Global Atom feed is missing required author metadata
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-11-10T13:05:54Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/feed.xml/route.ts
  - apps/web/app/feed.xml/route.test.ts
---

# Global Atom feed is missing required author metadata

## Why

The existing global `/feed.xml` emits non-empty feeds without an `atom:author` at feed or entry level. RFC 4287 section 4.1.1 requires a feed author unless every entry supplies one. This can fail strict Atom validation even though current tests pass. The new topic feed includes an author; this separate task preserves the global endpoint's narrow scope.

## Definition of done

- [ ] A non-empty global Atom feed supplies valid author metadata while preserving existing URLs, locale, publication dates, ordering and failure behavior.
- [ ] A parsed-XML test checks the required metadata instead of only matching fragments.

## Steps

- [ ] Audit ownership and claim before changing the global route.
- [ ] Add the appropriate publisher author and a regression test.

## How to verify

From `apps/web`, run `npx vitest run app/feed.xml/route.test.ts` and validate an emitted non-empty feed as Atom XML. Confirm all existing four regression cases remain green and 503 is retained on upstream failure.

## Notes

Discovered on 2026-11-10 while adding localized topic subscriptions. Read [RFC 4287 section 4.1.1](https://www.rfc-editor.org/rfc/rfc4287#section-4.1.1) directly that day. The old global route and tests were read but not edited. This is open/unclaimed work, not evidence that production was changed or that a strict reader failure has been observed in production.
