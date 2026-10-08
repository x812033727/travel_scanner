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

The replacement content draft supplies original starting files, full prompts, missing-deliverable repair, empty-file and wrong-name contrasts, and a course-material transfer exercise. An earlier independent read-only review by `review_own_video` resolved the working-directory/absolute-path gap and passed draft SHA-256 `8dec95ed57d8744c23a9d7a81120c2416a3e19fd0dc3ef3d154ba84687492c5d`; that is historical draft acceptance, not approval of subsequent source changes or media. Shared writing guidance was corrected under `2026-10-08-video-teaching-outcomes-and-examples`. Earlier local checks: prompt/register 27/27, skill parity 7/7, document/hygiene 5/5, docs/videos 199/199. Later CI at `4514d80596729895714819211ebbef0e423aa350` caught a machine-specific research path introduced into the draft after the earlier hygiene check. It is now a `<home>` placeholder; include new files in the index before rerunning the tracked-file hygiene check.

Continued on 2026-10-09: candidate source now exists in `demo/delivery-check`, with complete reusable inputs in `demo/delivery-fixtures` and an ordinary Node harness `demo/verify-delivery-logic.mjs`. It checks actual missing/add/refresh files, empty and wrong-name contrasts, path parsing, injected error classification and original-input hashes. Author verification passed 9/9 at `demo-evidence/delivery-logic-20261009.json` in the external evidence directory. It imports only pure data helpers; no Mod adapter or Claude runtime is executed. The teaching draft and `demo/delivery-verification.md` distinguish this evidence from native compatibility, first-use learning and actual footage. The adapter uses stat rather than exists, marks only explicit ENOENT as missing, and keeps unknown serialization as unable to check. Native errno shape remains unverified.

Independent source review found a real API mismatch before execution: the live interface guide described placement data from ui.open, but pinned official type commit `684800b206824dfd0cc8a876e8604b20f72c3617` declares Promise<void>. The candidate now awaits open without dereferencing its result. It also discards stale asynchronous refresh/open results. These are source corrections, not proof that the native static analyzer, command, buttons or panel work. No first-use execution, new narration, audio review or video review has occurred; production checkboxes remain open.

Final source-only independent review passed register SHA-256 `a584d7ba0f6256f59e631709814002ad44866138192ae1fac65820cfa7023dca` and logic SHA-256 `d62fe38bae54c329bece9dfdaa37a02bbcb820553892d7677947b089deb78f74`. The independent ordinary Node run passed 9/9 without importing the adapter. Its source-review receipt is `demo-evidence/independent-delivery-source-review-20261009-01.json`, SHA-256 `378cea59544b584db868101e8d31bf0e5fe9700e2a8839d72cd49d82ad9de0ad`. No full Windows pass or native Claude success is implied by these results. Release the claim with the concrete candidate and review evidence until permitted runtime verification, source handoff and actual media production can continue.

After staging all new candidate/material files, the combined video-document and repository-hygiene run passed 202/202 with no skips (66.3 seconds), saved as `delivery-package-docs-hygiene.log` outside Git. This includes the new paths that the earlier unstaged-file hygiene run missed. Repository checks do not satisfy the remaining native-demo or production acceptance steps.

Handoff from local branch `codex/mods-clarity-20261009`. Evidence and generated assets are under `<home>/mokaair-work/mods-clarity-20261009/`; the static review is `preview/storyboard/index.html`. The original source snapshot is SHA-256 `bd703aad6591a898ecbb46a824b76cfa2a5cdab05a856a857b8dbb50fad6103c`. A separate English-dub producer lease was present, but read-only process verification timed out; liveness is unknown. No production source was overwritten.

Automatic approval review rejected the isolated CLI version/validate/test command with only `blocked by policy`. This action has not been retried; the repo's counter test is a `.test.ts.example` source template, not a test run. Keep this limitation explicit and resolve the refusal before any equivalent attempt. No paid speech or image generation was started for the revision in the source/preview work.
