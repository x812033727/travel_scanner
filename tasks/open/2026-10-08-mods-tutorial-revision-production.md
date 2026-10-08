---
id: 2026-10-08-mods-tutorial-revision-production
title: Produce and review the revised Mods tutorial after original-source handoff
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-08T16:35:11Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/claude-code-mods-no-sandbox-before-install
---

# Produce and review the revised Mods tutorial after original-source handoff

## Why

The owner requested a clearer Mods video. The source rewrite, single-case diagrams and static storyboard now exist, but they are not new narration or a finished video. Production must continue against this revision without replacing the original while its separate language work is unresolved.

## Definition of done

- [ ] The original-source/dub handoff is resolved and the new revision has its own source-bound production state.
- [ ] New narration retains the selected voice; both spoken body and final cut meet the 8-minute minimum without padding.
- [ ] Real ASR/audio review, visual/video QA, captions, package checks and backend hash readback pass for the new source.
- [ ] Owner review, upload and publication are recorded as separate states; no original approvals are reused.

## Steps

- [ ] Review `docs/videos/claude-code-mods-no-sandbox-before-install/revision-review.md` and the static preview.
- [ ] Resolve source handoff and confirm the applicable production budget before provider calls; retain unknown provider outcomes without retries.
- [ ] Either obtain permitted runtime evidence or preserve every official/illustrative/expected-result label; do not fabricate a demonstrated installation.
- [ ] Produce narration and cut, inspect the actual player/audio, and complete the source-bound reviews and packaging.

## How to verify

Follow the current youtube-video skill and existing pipeline in a fresh work directory. Verify measured narration/body/final durations, speech/visual/source hashes, review receipts, actual exported captions and backend readback. A static preview and passing repository tests do not establish acceptance or publication.

## Notes

Handoff from local branch `codex/mods-clarity-20261009`. Evidence and generated assets are under `C:/Users/x8120/mokaair-work/mods-clarity-20261009/`; the static review is `preview/storyboard/index.html`. The original source snapshot is SHA-256 `bd703aad6591a898ecbb46a824b76cfa2a5cdab05a856a857b8dbb50fad6103c`. A separate English-dub producer lease was present, but read-only process verification timed out; liveness is unknown. No production source was overwritten.

Automatic approval review rejected the isolated CLI version/validate/test command with only `blocked by policy`. This action has not been retried; the repo's counter test is a `.test.ts.example` source template, not a test run. Keep this limitation explicit and resolve the refusal before any equivalent attempt. No paid speech or image generation was started for the revision in the source/preview work.
