---
id: 2026-10-14-video-qa-truncates-source-urls-with
title: Video QA truncates source URLs with parentheses
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-14T07:36:59Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/qa/links.mjs
  - tools/video/qa/links.test.mjs
---

# Video QA truncates source URLs with parentheses

## Why

`descriptionUrls` in `tools/video/qa/links.mjs` stops at ASCII `(`, so an
otherwise live source URL such as Wikimedia Commons
`...Plane_Ticket_(28379315406).jpg` is checked as `...Plane_Ticket_` and
returns 404. H05-v2 encountered this in its 2026-10-14 final QA. Encoding the
parentheses as `%28` and `%29` in that episode's asset URL is a local workaround;
the shared parser still misreads ordinary source URLs that contain parentheses.

## Definition of done

- [ ] Video QA checks the full destination of a plain URL with balanced ASCII
      parentheses, while still removing Markdown link-closing punctuation.
- [ ] Existing URL extraction, duplicate elimination and link checking tests pass.

## Steps

- [ ] Add a regression case for a Wikimedia-style URL in `links.test.mjs`.
- [ ] Narrowly correct `descriptionUrls` without accepting trailing sentence or
      Markdown punctuation as part of the URL.

## How to verify

`node --test tools/video/qa/links.test.mjs` and
`node --test --test-name-pattern="links" tools/video/qa/qa.test.mjs`.

## Notes

H05's other QA link failures were HTTP 403 from the local editorial GET to FBI
and FAA URLs. Those primary pages were opened separately on 2026-10-14; they
are a different issue and must not be hidden by weakening the parser or
accepting 403 as a successful response.
