---
id: 2026-10-23-reconcile-c-series-prior-charges-and
title: Reconcile C-series prior charges and activate per-film pilot accounts
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-23T11:25:15Z
completed_at:
branch:
depends_on:
  - 2026-10-23-consolidate-c-series-budget-holds-and
scope:
  - apps/api/migrations/versions/0138_everyday_story_budget.py
  - apps/api/tests/test_migration_0138_everyday_story_budget.py
  - apps/api/app/video_budget/models.py
  - apps/api/app/video_budget/service.py
  - apps/api/app/video_budget/RECONCILE.md
  - apps/api/app/video_budget/PENDING_EVERYDAY.md
  - apps/api/app/migration_guard.py
  - apps/api/app/schema.py
  - apps/api/tests/test_video_pilot_budget.py
  - apps/api/tests/test_migration_guard.py
  - tools/video/core/pending-pilot-budget.mjs
  - tools/video/tts/client.mjs
  - tools/video/media/client.mjs
  - tools/video/automation/client.mjs
---

# Reconcile C-series prior charges and activate per-film pilot accounts

## Why

C03–C06 used paid TTS/transcription/Jev and C03 used media before any per-film
USD ledger existed. Their owner-approved USD 25 ceilings do not become a new
USD 25 allowance after those calls. C07, C10 and C15 have approved ceilings
but no verified paid route. The fail-closed guard in the dependency task is a
safe review-only release; it deliberately creates no account or migration.
Drafts #1684/#1743/#1749 preserve prior implementation and evidence, but
#1749's immediately spendable C07/C10/C15 accounts and unprepared 0138
rollback path are unsafe to deploy as written.

## Definition of done

- [ ] Provider billing establishes each C03–C06 actual charge or an evidence
      backed upper bound. Every unresolved film receives a full USD 25
      `pre-ledger-history` uncertain operation before a balance can appear.
- [ ] Separate per-film accounts enforce the owner-approved USD 25 all-in
      ceiling and retain old operations on repeated migration/rollback.
- [ ] Exact supplier account, narration voice/model/region, billable units,
      published and account-specific prices, retake allowance and all paid
      TTS/ASR/Jev/image/music/text routes are verified before lifting any
      admission hold.
- [ ] The previous application image can safely serve the new database head
      after rollback. Real PostgreSQL and Compose upgrade/rollback tests and
      production readback pass before paid work resumes.
- [ ] Actual narration after the intro measures at least 480 seconds before
      buying illustrations; final illustration time share is checked later.

## Steps

- [ ] Read provider invoices/usage at least 48 hours after the last historical
      call, retaining ambiguous charges at full exposure. Preserve private
      evidence references outside the repository.
- [ ] Stage and deploy the rollback-compatible application image before any
      additive migration; verify exact schema/account behavior in both images.
- [ ] Add an idempotent migration at the then-current Alembic head. Refuse
      mismatched pre-existing accounts/holds; do not silently reopen a settled
      hold. Keep C07/C10/C15 held until the route audit completes.
- [ ] Read back all account limits, operations and remaining balances on host;
      dry-run and apply evidence-bound reconciliation only after that readback.
- [ ] Remove the seven client/API holds only in a reviewed activation change
      after all conditions are met. Preserve local STOP owner decisions.

## How to verify

Run `uv run alembic heads` and focused budget/migration/schema tests; exercise
the real PostgreSQL upgrade, repeat, mismatched-row refusal and Compose
application rollback in CI. On host, inspect Alembic current, `/ready`, media
status and `python -m app.video_budget.reconcile_cli --slug SLUG` for each exact
slug. Test no vendor POST before activation and one budgeted operation per
request after it. Measure actual body audio, excluding the intro, with the
video tooling duration receipt before purchasing images.

## Notes

The 2026-10-23 local inventory in `apps/api/app/video_budget/RECONCILE.md`
records C03 94 TTS / 94 ASR / Jev 27 lines / media USD 1.713; C04 a
429-refused TTS; C05 79 TTS / 79 ASR / Jev once; C06 94 TTS / 71 ASR.
Worst-case request bounds for C03/C05/C06 exceed USD 25, so the request count
cannot clear the exposure. Shared provider totals must be used only as
conservative upper bounds, never allocated by guesswork. Empty local speech
journals do not establish no charge. C03–C06 each need a full hold until
billing evidence proves otherwise.

The proposed migration in #1749 was numbered 0138 from 0137 and included
C07/C10/C15 as immediately spendable accounts. Recheck the current Alembic
head before writing a new migration; do not copy its FRESH set. The current
0137 application recognizes only the 0132→0133 rollback exception. A new
head without a prior compatibility release would break rollback `/ready` and
the migrate container. No paid provider request, STOP removal, upload or
publication is included in this ticket's initial safety release.
