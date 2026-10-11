---
id: 2026-10-11-explainer-docs-that-are-payload-or
title: Explainer documentation that is payload or receipt-bound still describes one preset
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-11T04:03:54Z
completed_at:
branch:
depends_on:
  - 2026-10-11-cute-explainers-own-series-prompts
scope:
  - .agents/skills/youtube-video/references/drama.md
  - .claude/skills/youtube-video
  - .agents/skills/animation-camera/references/model-misreads.md
  - .claude/skills/animation-camera
  - docs/videos/so-thats-why/README.md
  - docs/videos/history-curiosity/look.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Explainer documentation that is payload or receipt-bound still describes one preset

## Why

The three explainer-route pull requests edit no file that `prompts.mjs references()` reads into
a payload, because one changed byte there moves the durable key of every unfinished
drama-format stage (`video_ai_receipt_input_changed`); their documentation went to
`docs/videos/DRAMA.md` and `DRAMA-FLOW.md` instead ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 1). Four texts are
therefore out of date once the cute presets exist (section 7 item 10):

1. `.agents/skills/youtube-video/references/drama.md`: the explainer paragraph and the preset
   list name `flat-explainer` only, and say nothing of the request's image model. This file is
   payload.
2. `docs/videos/so-thats-why/README.md`: the table row that says to use `preset: "custom"`
   until a named preset exists; it exists now (`cute-cartoon`). This file is bound by the
   duration receipt.
3. `.agents/skills/animation-camera/references/model-misreads.md`, about line 35: the list of
   each preset's `look.motion` stops at `flat-explainer`.
4. `docs/videos/history-curiosity/look.md` §縮圖: the tag is written `外星`, the prompt and the
   pilots use `外星與太空` (and the prompt shortens two others to `奇異現象` and `預言`).

## Definition of done

- [ ] The four texts say what the code does after `2026-10-11-cute-explainers-own-series-prompts`.
- [ ] Item 1 is deployed with **no drama-format journal unfinished** on the host (check before
      the deploy; say so in the pull request), all four in one deploy.
- [ ] The Claude Code copies of the two skills stay byte-identical (`npm run test:tools`), and
      the receipt is re-issued by an independent agent for the bound file.

## Steps

- [ ] Confirm which of the four are read by `references()` at that time (`prompts.mjs`), and
      which the receipt binds (`node tools/video/long-form/cli.mjs check` after the edit).

## How to verify

`node --test tools/skills.test.mjs`; `node tools/video/long-form/cli.mjs check`; the worker's
log has no `video_ai_receipt_input_changed` after the deploy.

## Notes

- 2026-10-11 filed from the design's section 7, item 10.
