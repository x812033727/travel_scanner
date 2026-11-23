---
id: 2026-11-11-thumbnail-qa-resolved-drama-layout
title: Thumbnail QA measures the layout a drama takes by default (layout f), not only data.layout
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-11-11T23:00:10Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/qa/cli.mjs
  - tools/video/qa/thumbnail.test.mjs
  - tools/video/long-form
---

# Thumbnail QA measures the layout a drama takes by default (layout f), not only data.layout

## Why

PR #2078 (task `2026-11-11-bright-explainer-and-drama-thumbnails`) gave AI dramas their own thumbnail
layout `f`: an AI drama (`isDramaThumbDoc` in `tools/video/templates/templates.mjs`) takes it whenever
`thumbnail.data.layout` is not written. `tools/video/qa/thumbnail.mjs` already has the rule for it
(`HEADLINE_DRAMA`: one line across the frame, at most `DRAMA_HEADLINE_MAX` 8 characters), but
`tools/video/qa/cli.mjs` `thumbnailItem` still passes only `doc.thumbnail.data?.layout`. So a drama
drawn in layout `f` by default is measured with the channel's 40% column and its six-character rule,
as before #2078: a 7–8 character drama headline fails qa although it fits the drawn thumbnail.

`qa/cli.mjs` is bound by the independent duration review (`tools/video/long-form/review.test.mjs`
fails with "stale duration review binding: tools/video/qa/cli.mjs" once it changes), which is why
#2078 left it alone.

## Definition of done

- [ ] `thumbnailItem` passes the layout as drawn: `data.layout ?? (isDramaThumbDoc(doc) ? THUMB_DRAMA_LAYOUT : null)`, for the video's thumbnail and every locale's.
- [ ] A test in `tools/video/qa/thumbnail.test.mjs` shows a drama without `data.layout` measured with `HEADLINE_DRAMA`.
- [ ] The duration review binding for `qa/cli.mjs` is renewed the way `tools/video/long-form` documents (an independent reviewer, not the author), and `review.test.mjs` passes.

## Steps

- [ ] Read `tools/video/long-form/` for how a binding is renewed (PR #2004 did the same for `qa/cli.mjs`: "時長收據增量", reviewed by a separate agent).
- [ ] Make the two-line change and the test.
- [ ] Get the review and update the receipt.

## How to verify

```bash
node --test tools/video/qa/thumbnail.test.mjs tools/video/long-form/review.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

PR #2004 also edits `qa/cli.mjs` and `qa/thumbnail.mjs`; whichever lands second resolves the overlap.
