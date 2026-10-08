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
branch: codex/mods-clarity-20261009
depends_on: []
scope:
  - docs/videos/claude-code-mods-no-sandbox-before-install
---

# Produce and review the revised Mods tutorial after original-source handoff

## Why

The owner requested a clearer Mods video. The source rewrite, single-case diagrams and static storyboard now exist, but they are not new narration or a finished video. Production must continue against this revision without replacing the original while its separate language work is unresolved.

## Definition of done

- [ ] The lesson solves a concrete viewer problem with a complete worked example, a contrast and a transfer exercise; an independent first-use review verifies the learner can reproduce and explain the result.
- [ ] The original-source/dub handoff is resolved and the new revision has its own source-bound production state.
- [ ] New narration retains the selected voice; both spoken body and final cut meet the 8-minute minimum without padding.
- [ ] Real ASR/audio review, visual/video QA, captions, package checks and backend hash readback pass for the new source.
- [ ] Owner review, upload and publication are recorded as separate states; no original approvals are reused.

## Steps

- [x] Review `docs/videos/claude-code-mods-no-sandbox-before-install/revision-review.md` and the static preview; record the failed teaching-value review in `teaching-review.md`.
- [ ] Complete the substantive rewrite, provide starting materials and actual demonstrations, then synchronize the final script/video source and renew its source bindings.
- [ ] Resolve source handoff and confirm the applicable production budget before provider calls; retain unknown provider outcomes without retries.
- [ ] Obtain permitted runtime evidence for the core practical promise. Official/illustrative/expected-result labels remain mandatory where relevant, but labels alone do not satisfy a claim that viewers can reproduce a demonstrated installation.
- [ ] Produce narration and cut, inspect the actual player/audio, and complete the source-bound reviews and packaging.

## How to verify

Follow the current youtube-video skill and existing pipeline in a fresh work directory. Verify measured narration/body/final durations, speech/visual/source hashes, review receipts, actual exported captions and backend readback. A static preview and passing repository tests do not establish acceptance or publication.

## Notes

The owner's follow-up explicitly rejected presentation-only improvements: the reference videos teach useful decisions and include practical examples. Both full reference transcripts were read on 2026-10-09. The present counter-only script is not approved for production on educational grounds; preserve its source and preview as comparison evidence. `teaching-review.md` records specific failures and `teaching-rewrite.md` carries the replacement content draft. Runtime demonstrations, first-use learning verification, source synchronization and media production remain incomplete. Windows validation is a separate workstream and cannot explain or excuse these editorial gaps.

The replacement content draft now supplies original starting files, full prompts, missing-deliverable repair, empty-file and wrong-name contrasts, and a course-material transfer exercise. Independent read-only review by `review_own_video` found and resolved the working-directory/absolute-path gap, then passed draft SHA-256 `8dec95ed57d8744c23a9d7a81120c2416a3e19fd0dc3ef3d154ba84687492c5d`. This is draft acceptance only: the proposed `delivery-check` Mod is unimplemented, the custom command/UI unverified, and no first-use execution or audio/video review has occurred. Shared writing guidance was also corrected under `2026-10-08-video-teaching-outcomes-and-examples`. Local checks: prompt/register 27/27, skill parity 7/7, document/hygiene 5/5, docs/videos 199/199. Release this claim with these handoff notes until the remaining runtime/source/media work resumes.

Handoff from local branch `codex/mods-clarity-20261009`. Evidence and generated assets are under `<home>/mokaair-work/mods-clarity-20261009/`; the static review is `preview/storyboard/index.html`. The original source snapshot is SHA-256 `bd703aad6591a898ecbb46a824b76cfa2a5cdab05a856a857b8dbb50fad6103c`. A separate English-dub producer lease was present, but read-only process verification timed out; liveness is unknown. No production source was overwritten.

Automatic approval review rejected the isolated CLI version/validate/test command with only `blocked by policy`. This action has not been retried; the repo's counter test is a `.test.ts.example` source template, not a test run. Keep this limitation explicit and resolve the refusal before any equivalent attempt. No paid speech or image generation was started for the revision in the source/preview work.
