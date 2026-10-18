---
id: 2026-10-11-host-explainer-writer-image-cards
title: Host explainer writer: screenshot and photo cards need a way to supply and credit an image file
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T04:02:22Z
completed_at:
branch:
depends_on:
  - 2026-10-11-cute-explainers-own-series-prompts
scope:
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/explainer-series.test.mjs
  - tools/video/core/drama.mjs
  - tools/video/automation/flow.mjs
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Host explainer writer: screenshot and photo cards need a way to supply and credit an image file

## Why

`2026-10-10-explainer-route-takes-a-series-look` asked that `EXPLAINER_CARD_TEMPLATES` gain `screenshot` and `photo` so a real
photograph may sit between an explainer's stills (the owner allows public-domain and stock
photographs in 奇聞檔案局 and So That's Why; the `photo` card shipped as #1425). The design
moved that out ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 1 and `DECISIONS.md`, engineering defaults): the automated
route has no way to supply and credit an image file. `settle()` empties `assets[]` on every
save, the worker has no step that fetches a file into the work directory, and render refuses a
`photo` or `screenshot` scene whose file is missing or not in `assets[]`, after the narration
and pictures were paid for. The cute presets therefore get the six explainer cards plus `steps`
and `table` only. The local pilots did use more (`bullets`, `quote`, `screenshot`), so the host's
episodes are poorer in cards than the approved pilots; whether `quote` should be offered to the
奇聞檔案局 writer was left open too.

Related, not the same: `2026-10-10-host-writer-prompt-forbids-photo` tells the host's *slides*
writer not to use `photo`; this ticket is about letting the *explainer* writer use it properly.

## Definition of done

- [ ] A decided way for an automated explainer to obtain an image file with its credit (for
      example the writer names a stock query or a Commons file and a worker step fetches it with
      `stock fetch` and registers `assets[]`), written down with its cost and licence rules
      (docs/videos/history-curiosity/README.md §照片).
- [ ] `settle()` keeps the registered `assets[]` for such a video; lint refuses an image card
      whose file was not supplied before any paid step.
- [ ] The cute writers' card list and prompt texts offer `screenshot` and `photo` (and `quote`
      for 奇聞檔案局 if decided); `flat-explainer`'s prompt bytes do not move.
- [ ] Tests; the new prompt digests pinned; the receipt re-issued by an independent agent.

## Steps

- [ ] Design first and show the owner; this is not a one-line change.
- [ ] Any prompt change stops unfinished cute runs: deploy with none unfinished.

## How to verify

A host `cute-mystery` episode with one `photo` scene renders, and its description lists the
photograph under 📷 圖片來源.

## Notes

- 2026-10-11 filed from the design's section 7, item 2.
