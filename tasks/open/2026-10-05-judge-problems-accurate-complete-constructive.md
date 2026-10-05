---
id: 2026-10-05-judge-problems-accurate-complete-constructive
title: Judge problems that are accurate, complete and constructive: key, fault, and one prompt-level fix
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-05T16:08:25Z
completed_at:
branch:
depends_on:
  - 2026-10-04-fault-checks-for-the-drama-judges
  - 2026-10-05-media-budget-estimate-reserve-reconcile
scope:
  - apps/api/app/video_media/judge.py
  - apps/api/tests/test_video_media_judge.py
  - tools/video/media/keyframes.mjs
  - tools/video/media/clips.mjs
  - tools/video/media/look.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/media/clips.test.mjs
  - docs/videos/ILLUSTRATED.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Judge problems that are accurate, complete and constructive: key, fault, and one prompt-level fix

## Why

The judge's `problems` are free text: a take can fail a criterion with no problem naming it,
or carry a problem that names no failed criterion, and the retake prompt gets nothing it can
act on. The reviewer rules of the CHAI study (accurate: point at the place; complete: scan for
the same fault elsewhere; constructive: every critical finding proposes a fix), used by
OpenMontage's reviewer skill (AGPL — idea only), are the contract to enforce.

## Definition of done

- [ ] Every `problems[]` string is `"<criterion key>: <what is wrong and where> → <one
      prompt-level change>"`; the server drops a problem naming no failed criterion and
      synthesises one for a failed criterion without a problem; the instructions ask for the
      fix clause. `JudgeOut`'s shape and the review payload keys
      (`shots[].judge.overall/problems/passed`) are unchanged.
- [ ] The tool's retake loops put the fix clause into `needs_review` hints and the next take's prompt.
- [ ] Measured on the 163 recorded takes of the fault-checks ticket: the share of failed takes
      whose problem names the failing criterion, before and after, in this ticket.

## Steps

- [ ] `judge.py`: instructions, post-processing, tests with fake answers.
- [ ] `keyframes.mjs`, `clips.mjs`, `look.mjs`: carry the fix clause; tests.
- [ ] `ILLUSTRATED.md` §judge; receipt increment for the two bound test files.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_media_judge.py -q
node --test tools/video/media/look-keyframes.test.mjs tools/video/media/clips.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

- Bound: `media/look-keyframes.test.mjs`, `media/clips.test.mjs`.
- Depends on the fault-checks ticket (the questions) and the budget gate (judge calls count).
