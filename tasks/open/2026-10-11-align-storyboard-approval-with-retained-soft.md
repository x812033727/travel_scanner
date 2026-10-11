---
id: 2026-10-11-align-storyboard-approval-with-retained-soft
title: Align storyboard approval with retained soft judge notes
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-11T20:56:01Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - apps/api/app/video_automation/settings.py
  - apps/api/tests/test_video_automation_settings.py
---

# Align storyboard approval with retained soft judge notes

## Why

H02's native keyframes process reuses 68 complete pictures: 64 passed their native judge and four are explicitly kept for owner final review. The submitted storyboard nevertheless stays pending because 52 of the 64 passed pictures carry retained soft remarks in each shot's `judge.problems`. The official server `storyboard_check_passed` requires that list to be empty for every non-accepted picture, even when its native verdict passed and its score clears the threshold. Resolve the producer/consumer contract without erasing remarks, weakening hard defects or confusing an owner decision with automatic approval.

## Definition of done

- [ ] A complete storyboard with native passed pictures and permitted soft remarks has a documented, consistent approval decision at producer and consumer.
- [ ] Hard failed pictures, missing/changed file hashes, partial coverage and unmarked rejected pictures still cannot auto-approve.
- [ ] Original per-take verdicts and all retained remarks remain available to the reviewer; accepted exceptions still force the owner's final review.

## Steps

- [ ] Reproduce the current H02 payload against the official checker before choosing a contract change.
- [ ] Define an explicit distinction between soft remarks and blocking defects, with independent review of the policy.
- [ ] Add meaningful producer/consumer coverage for passed-with-remarks, hard failure, accepted exception and incomplete/changed evidence.

## How to verify

Run the relevant API automation-settings tests and `node --test tools/video/review/sync.test.mjs`. Use source-bound retained H02 evidence as an integration fixture, without new paid generation or changing historical reviews. Production deployment and any new review submission remain separate tasks.

## Notes

- 2026-10-12 Asia/Taipei: H02 storyboard review `e8cbd0f9-bf91-4a9b-b8f9-8fff70d9a946`, manifest/content SHA `92961cfc19a1109001fdc82e1f2b4cde66042580d41eb898c67930acdfc67055`, current source SHA `4dfe4d73dd458323949542ba5c22cd68a7838cbdc237b36543b07ea18620322e`. The actual 68 selected file hashes match, `keyframeProblems=[]`, expected coverage is complete, top-level judge has score7.18/problems[], and four accepted shots are correctly skipped by the server.
- Independent reviewer extracted the official pure checker from `settings.py` and evaluated the saved actual payload at threshold7: False, due to nonempty per-shot problems. This is not a score-shortfall or a missing-image issue. Example: `hook-white-happy` score9.29 has the soft remark about hands at the edge.
- Saved evidence lives outside the repository at `C:/Users/x8120/mokaair-work/videos/curio-h02/_audit/backend-readback.json`; native keyframe and review-push receipts are retained. Preserve the original remarks and keep the review pending until an explicit valid decision. Do not delete `problems`, change thresholds, falsely mark all shots accepted, or blindly repeat paid judging to make this instance pass.
- Existing 2026-10-07 illustrated-spec and 2026-10-08 kept-shot payload-size tickets address different cases. This ticket is filed for shared-code work later; H02 production does not claim or modify that code.
