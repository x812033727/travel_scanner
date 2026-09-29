---
id: 2026-09-29-correct-current-shorts-scripts-and-resubmit
title: Correct current Shorts scripts and resubmit final review evidence
status: done
priority: P1
area: docs
owner: codex-shorts-pr
claimed_at: 2026-09-29T02:20:17Z
created_at: 2026-09-29T01:36:57Z
completed_at: 2026-09-29T02:24:40Z
branch: codex/shorts-backend-audit
depends_on: []
scope:
  - docs/videos/ai-shorts/corrections-20260929
---

# Correct current Shorts scripts and resubmit final review evidence

## Why

The 2026-09-29 live audit found misleading single-variable framing in the prompt pilot, two flagged narration phrases, missing script-bound independent verification, and incomplete QA evidence on 15 pending Shorts. The user requested corrections after the audit. Preserve the original experiments and publish no videos.

## Definition of done

- [x] Three lab scripts describe the actual bundled A/B method and its limits; corrected narration and captions match.
- [x] All 15 final cuts have current independent fact receipts and automated narration/technical checks; unresolved gates remain explicit.
- [x] Corrected versions and their evidence are visible in the existing backend final-review records with matching reloaded hashes.

## Steps

- [x] Preserve historical experiments and create dated lab corrections outside the pilot fixture directories.
- [x] Coordinate the 12 cut fixes under the separately claimed season-one ticket.
- [x] Rebuild, independently verify, run QA, and submit only the final review gate.
- [x] Save a receipt separating authored, validated, submitted, owner accepted and published states.
- [x] Include these local source changes in the source PR, with independent review completed and this ticket closed inside the PR under the repository's in-PR closure protocol.

## How to verify

Run the existing Shorts schema/evidence validator, check-audio and QA against the corrected builds; decode and measure the final video bytes, inspect safe-area frames, then reload each final-review record and compare its hash. The dated operations/review.mjs accepts an external build manifest and records per-step receipts. It never submits a publish gate.

## Notes

- Generated media and authenticated response receipts stay outside the public repository in the dated shorts-fixes work directory.
- Scope is isolated from the original experiment/protocol fixtures and active Shorts tool development.
- The existing pilot-launch ticket only owns release receipts; this separate ticket owns revised scripts and the dated resubmission helper.
- Channel stance was empty at the start of correction. A concrete proposed editorial stance has been presented to the owner; do not change it without their answer. Parent-video public links cannot be invented or obtained by publishing without authorization.
- Delivery: all 15 corrected videos were submitted to existing final-review records and remain pending. Automated narration passed 112 phrases; independent facts passed 69 claims. Lab QA is 11/12 (policy remains); cut QA is 9/12 (policy and missing parent URL metadata/links remain). See `docs/videos/ai-shorts/releases/2026-09-29-corrections.json` and the external `shorts-fixes-20260929` package.
- The final-only helper rejects stale script/QA/check/verify/layout receipts and verifies the reloaded backend QA plus attachment hashes. The equivalent gaps in shared CLI commands were separately filed as `2026-09-29-bind-shared-shorts-narration-and-qa`; no active shared-tool work was overwritten.
- The correction and resubmission stage performed no manual approval, publish gate, YouTube upload/publication, setting change, PR, merge or deployment. Human listening and phone playback remain owner acceptance. Browser review playback was not verified because browser control timed out; backend API records were reloaded instead.
- Source PR preparation was separately authorized by the owner. The branch was fast-forwarded to main at `a14d45f8`; independent review found no draft-PR blocker, private user paths, credentials or binary media in the candidate files. The Node 24.19 tools suite passed 659 tests with 2 skips and no failures; all three lab schema/evidence validators and helper syntax checks passed. Owner-acceptance tickets remain open.
