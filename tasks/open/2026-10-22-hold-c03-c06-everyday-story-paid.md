---
id: 2026-10-22-hold-c03-c06-everyday-story-paid
title: Stage C03-C06 attributed-route budget holds before historical reconciliation
status: review
priority: P1
area: api
owner: codex-everyday-budget-guard
claimed_at: 2026-10-22T12:25:09Z
created_at: 2026-10-22T12:25:03Z
completed_at:
branch: codex/everyday-budget-preflight
depends_on: []
scope:
  - apps/api/app/video_budget/models.py
  - apps/api/app/video_budget/service.py
  - apps/api/tests/test_video_pilot_budget.py
  - tools/video/media/client.mjs
  - tools/video/media/client.test.mjs
---

# Stage C03-C06 attributed-route budget holds before historical reconciliation

## Why

The C03–C06 local story pilots already have approved USD 25 all-in ceilings, but their
slugs are absent from the server budget dispatch guard and the local media client's
one-send list. C05/C06 made nonpilot TTS/ASR calls before registration; those charges
cannot be attributed from the existing per-video ledger. A newly spendable USD 25
account would falsely ignore them.

## Definition of done

- [x] The four exact slugs use the server pilot dispatch guard when attributed, and local media one-send behavior.
- [x] With no reconciled budget account, attributed paid server calls fail before provider dispatch;
      the unrelated media status remains readable.
- [x] The remaining reconciliation and activation steps are explicit, with no invented spend.

## Steps

- [x] Register the four slugs as guarded but unactivated in the server and media client.
- [x] Test missing and accidental fresh accounts, plus one-send media calls.
- [x] Run targeted checks and record the blocked activation prerequisites.

## How to verify

`cd apps/api; uv run pytest tests/test_video_pilot_budget.py` and
`node --test tools/video/media/client.test.mjs` from the repository root.

## Notes

The migration directory is held by task 2026-10-19-a01-0133-story-budget-migration
(review, PR #1510), and tools/video/tts by task 2026-10-19-worker-video-languages-five
(review). This ticket avoids both scopes. A later migration must add each USD 25 account
with a full USD 25 uncertain historical-cost hold in the same transaction, then use
evidence-bound `video_budget` reconciliation to settle attributable historical charges
before any new paid call. If attribution is impossible, keep the full hold and stop.

Critical gap: the current local TTS client omits `video_slug` entirely for C03–C06,
so their TTS/ASR calls cannot be identified by the server guard in this PR. Do not
resume TTS, ASR, image, judging, music, or any other paid call from these four films.
Retain C05/C06 STOP files. Follow-up ticket:
`2026-10-22-reconcile-c03-c06-prior-charges-and`.

This is a partial safeguard in review, not a completed full-film cap. On 2026-10-22,
`npm run tasks -- done` wrote an untracked copy under `tasks/done/` but could not
remove this open copy. The exact `Remove-Item` attempt was `blocked by policy`;
the duplicate remains untracked locally and makes local `check:tasks` fail.

Verification: budget pytest 19 passed, 2 skipped; media client 8 passed; ruff
passed; `npm run check:tasks` exit 0. No provider call was made.
