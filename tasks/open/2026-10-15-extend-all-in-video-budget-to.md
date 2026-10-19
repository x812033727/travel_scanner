---
id: 2026-10-15-extend-all-in-video-budget-to
title: Enforce US$5 all-in limits for B18 v2 and five brand stories
status: in-progress
priority: P1
area: api
owner: codex-gpt6-budget-six
claimed_at: 2026-10-16T00:03:23Z
created_at: 2026-10-15T18:38:21Z
completed_at:
branch: codex/a01-pilot-deploy-evidence-20261015
depends_on:
  - 2026-10-14-enforce-usd-25-all-in-cap
scope:
  - apps/api/app/video_budget/recovery.py
  - apps/api/app/video_budget/RECONCILE.md
  - apps/api/app/video_media/admin_api.py
  - apps/api/migrations/versions/0133_story_followon_budget.py
  - apps/api/tests/test_migration_0133_story_followon_budget.py
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/media/client.mjs
  - tools/video/media/client.test.mjs
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - tools/video/tts/cli.mjs
  - tasks/open/2026-10-15-extend-all-in-video-budget-to.md
---

# Enforce US$5 all-in limits for B18 v2 and five brand stories

## Why

The owner requested five brand-story follow-ons after the A01/B18 pilots. The existing all-in budget mechanism covers only the four original/v2 pilot slugs. The five `story-five-*` slugs are not in `PILOT_SLUGS`; the ordinary media estimate cap does not cover TTS, transcription, Jev and all other paid stages. The prepared quote proposes US$5 for B18 v2 and each of five follow-ons, US$30 total. A concrete whole-film quote must not be described as an enforceable per-film ceiling until these exact productions share equivalent reserve/settle/uncertain protection.

## Definition of done

- [ ] B18 v2 and the five exact follow-on slugs each have an independent US$5 all-in limit, including every attributed paid route and unresolved reservations.
- [ ] Existing pilot limits and unrelated slugs retain their behavior; one film cannot borrow beyond its own approved cap.
- [ ] Fresh per-slug ledger readback and boundary/concurrency tests prove the limit before paid import/continuation. No production is started merely by merging the code.

## Steps

- [ ] Coordinate with the existing pilot-budget task owner and inspect current merged/deployed code before claiming the overlapping scope; extend this task's scope only if the chosen implementation requires it.
- [ ] Implement the exact five-slug coverage using the existing budget mechanism or an equivalent configurable mechanism, then prove cross-stage, unknown-price, retry and exact-boundary behavior.
- [ ] Record the approved quote and deployment separately; preflight each slug and retain per-film plus batch totals before any paid production.

## How to verify

Run focused `apps/api/tests/test_video_pilot_budget.py` coverage for all five slugs, original pilots and an unrelated control. Include accumulated settled/reserved/uncertain costs and next-call refusal at the cap. After separately approved deployment, use the existing read-only reconcile CLI for each exact slug; a local test is not production enforcement.

## Notes

2026-10-19 owner-approved narrow scope transfer: the owner authorized releasing
only `apps/api/app/video_budget/models.py`,
`apps/api/app/video_budget/service.py`, and
`apps/api/tests/test_video_pilot_budget.py` to a separate A01 database-admission
fence task. This does not change any budget implementation in this PR. The
`0133_story_followon_budget` migration, recovery, clients, other tests and this
task's remaining scope stay with `codex-gpt6-budget-six`; its draft PR and
untracked work are preserved. Coordinate any future edits to the three
transferred files with the A01 fence task.

Exact follow-on slugs: `story-five-lego-legoland`, `story-five-costco-hot-dog`, `story-five-adidas-puma-brothers`, `story-five-ajinomoto-chip-film`, `story-five-pringles-vat-case`. The 2026-10-16 quote proposes US$5 per film for B18 v2 and the five, US$30 total. The owner waived subscription/balance proof; do not ask for it again. A01/B18 pilot completion and owner viewing remain ahead of the five. This claim prepares fail-closed code and tests; it does not deploy, generate, upload or publish.

2026-10-16 claim exception: `2026-10-14-enforce-usd-25-all-in-cap` remains marked in-progress by `codex-story-budget-cap` in this chat's attached, clean old worktree, but its #1508 was merged to main as `42fbfb40d` and its remote head was deleted. The task tool refused this follow-up only because that completed predecessor has not yet been moved to done; `--force` was used for this follow-up claim without modifying the old task or its worktree. The follow-up scope is expanded from two files to the exact service, migration, client, audition, documentation and test paths required by the existing handoff. Keep the PR draft/no-auto-merge until explicit release authorization.

Local implementation: one exact slug-to-limit policy gives A01 original/v2 and B18 original US$25, while B18 v2 and each of the five `story-five-*` titles get US$5. Migration `0133_story_followon_budget` preserves B18 v2 operation rows, narrows that account only when it is the old US$25 value, and seeds five independent accounts without replacing existing rows. A downgrade intentionally refuses to expand a cap or discard paid-operation context automatically. All three protected client families attribute the five slugs, and audition rejects absent/mismatched exact slugs. The normal reserve/settle/uncertain ledger still blocks any film at its own limit; no account borrows from another.

2026-10-16 read-only formal-host evidence at live `9fe80417c07684305f1e710e027b2cc2f2b5c22d`: `reconcile_cli --slug story-conveyor-belt-sushi-v2` returned old `limit_usd=25.000000`, `operations=[]`, reserved/settled/uncertain zero. This is safe input for the proposed narrowing but does **not** mean migration or new accounts are live. Local focused tests: budget/migration 16 passed/3 skipped; migration/schema/dialect 10 passed/1 skipped; three Node client suites 66/66 passed; Ruff passed; `mypy app` passed on 478 files and `mypy tests` on 397 files. The final integration fixture now creates the old 0132 schema transactionally before testing 0133, preserving its seed and prior operation rows; that PostgreSQL case is skipped locally and must run in CI (`RUN_INTEGRATION_TESTS=1`). Its offline test passes, and targeted Ruff/mypy pass after this fixture repair. No paid work, host write, deployment or owner approval is implied by these checks.

Independent rollback review found a hard release dependency: the currently deployed
0132 application rejects B18 v2 at USD 5 and rejects revision 0133 at `/ready`.
Migration-first deployment followed by application-only rollback would break the
video status endpoint. Draft PR #1521 stages exact-version/read-only/settlement
compatibility and blocks new B18 v2 spend while its stored cap is still USD 25.
It must be separately merged, deployed and read back before this PR's 0133 can ship.
The audition path fix in this branch also prevents an unrelated `a01-*` ancestor
from vetoing a valid A29 file, while a true B18 workdir mismatch still stops.
After rebasing, Windows Node 24's fixture `sandbox()` exited with native code
`-1073740791` before CLI execution; syntax checks passed and hosted CI is required
for the new regression cases. No full-film US$30 paid authorization is inferred.
