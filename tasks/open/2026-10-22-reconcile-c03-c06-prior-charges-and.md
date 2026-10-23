---
id: 2026-10-22-reconcile-c03-c06-prior-charges-and
title: Reconcile C03-C06 prior charges and activate the USD 25 all-in route
status: review
priority: P1
area: api
owner: claude-opus-5.5-everyday-budget
claimed_at: 2026-10-23T05:51:17Z
created_at: 2026-10-22T12:29:48Z
completed_at:
branch: claude/everyday-story-budget-route
depends_on:
  - 2026-10-22-hold-c03-c06-everyday-story-paid
scope:
  - apps/api/migrations/versions/0138_everyday_story_budget.py
  - apps/api/tests/test_migration_0138_everyday_story_budget.py
  - apps/api/app/video_budget/models.py
  - apps/api/app/video_budget/service.py
  - apps/api/app/video_budget/RECONCILE.md
  - apps/api/tests/test_video_pilot_budget.py
  - apps/api/tests/test_video_media_api.py
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - tools/video/tts/cli.mjs
  - tools/video/media/client.mjs
  - tools/video/media/client.test.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
---

# Reconcile C03-C06 prior charges and activate the USD 25 all-in route

## Why

C03–C06 were approved for USD 25 all-in local pilots before their slugs entered
the per-video budget route. C05 made 79 TTS and 79 ASR requests, and C06 made
94 TTS and at least 71 ASR requests outside that ledger. Some earlier C03/C04
media may also need attribution. Google AI Studio currently shows only a shared
project aggregate with delayed billing, so it cannot establish any film's actual
historical charge. Task `2026-10-22-hold-c03-c06-everyday-story-paid` guards
attributed server/media calls but deliberately keeps the four slugs unactivated.
The local TTS client still omits `video_slug` for these slugs, so its existing
requests cannot yet be protected by that server guard.

## Definition of done

- [x] Each film has an evidence-backed historical exposure ledger or a full USD 25
      uncertain hold; no migration creates a fresh spendable USD 25 balance.
- [x] The TTS/ASR client sends exact slug and stable operation IDs, including audition
      calls, and tests show ambiguous responses do not retry or consume money twice.
- [ ] The deployed account, migration guard, status, and local readback all prove
      remaining USD cannot exceed USD 25 minus all historical and new exposure.

## Steps

- [x] Wait for the migration scope holder `2026-10-19-a01-0133-story-budget-migration`
      (review, PR #1510) and TTS scope holder `2026-10-19-worker-video-languages-five`
      (review) to release or finish; inspect the current migration head again.
- [ ] Collect final provider billing evidence with per-film attribution for C03–C06;
      record ambiguous charges as fully held, never as zero.
- [x] Stage an additive migration with one USD 25 account and a USD 25 uncertain
      historical hold for each exact slug. Verify real PostgreSQL upgrade and repeat,
      and plan rollback compatibility before deployment.
- [x] Activate the four slugs in the server account set and the TTS client's exact
      allowlist, updating CLI audition slug/path checks and targeted tests.
- [ ] Inspect `python -m app.video_budget.reconcile_cli --slug SLUG` and use its
      evidence-bound settle action only when the full historical charge is attributable.
      Keep any unresolved film fully held and stopped.

## How to verify

Run budget/migration/TTS tests including real PostgreSQL migration integration,
then read back each account's operations and `remaining_usd` on the host before
allowing a single new paid request. Verify STOP handling separately; this task
does not authorize removing STOP or calling providers.

## Notes

Owner approved each C03–C06 local pilot up to USD 25, not a second USD 25 after
unrecorded calls. The project-wide AI Studio bar is partial and can lag more
than 24 hours; it cannot allocate cost to C05/C06. C05 and C06 have STOP files.
No upload, publication, merge, deployment, or paid provider action is authorized
by this ticket alone.

2026-10-23 (claude-opus-5.5-everyday-budget): Both scope holders were stale. 0133 is on
main (its PR #1510 closed after the file landed), and the five-language TTS work shipped
on 2026-10-20. The branch carries #1684's guard commit and replaces its "no account"
stance with migration 0138. That migration opens USD 25 accounts for C03–C07, C10 and C15;
C03–C06 each start with one `uncertain` USD 25 `pre-ledger-history` hold. The server also
treats every `story-everyday-` slug as budgeted, so a film without an account fails closed.
The TTS, media and automation clients attribute the whole series accordingly.
`PILOT_LIMITS_USD` stays the reviewed 0133 set for the migration guard, and the service
reads `BUDGET_LIMITS_USD`. The local workdir readback (request counts, C03's USD 1.713
media ledger, empty speech journals) and the settle procedure are in `RECONCILE.md`.
Every worst-case bound is above USD 25, so only provider billing can settle a hold.
Still open: an owner-run deploy and host readback, and provider evidence per film. No paid
call, STOP removal or deployment was made.
