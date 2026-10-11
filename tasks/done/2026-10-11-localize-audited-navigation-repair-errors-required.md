---
id: 2026-10-11-localize-audited-navigation-repair-errors-required
title: Localize audited navigation repair errors required by CI
status: done
priority: P1
area: api
owner: codex-news-recovery-6f71
claimed_at: 2026-10-11T11:06:25Z
created_at: 2026-10-11T11:06:13Z
completed_at: 2026-10-11T11:17:48Z
branch: codex/news-recovery-followup-20261011
depends_on: []
scope:
  - apps/api/app/i18n.py
---

# Localize audited navigation repair errors required by CI

## Why

PR #1444 introduces eleven audited navigation-repair error codes. CI run
38133738581 failed only `test_every_public_error_code_has_a_sentence_in_every_locale`
in API shard 2 because these codes lack English, Japanese, Korean and Simplified
Chinese messages. The errors must explain the actual refusal rather than fall
back to a generic sentence.

## Definition of done

- [x] All eleven new codes have accurate, nonempty messages in every locale.
- [x] Existing localization coverage and locale key parity pass.
- [x] Fix and verification are recorded for PR #1444; conditional merge still requires all four green CI checks.

## Steps

- [x] Check active claims, worktrees, remote heads and open PRs for the exact i18n file.
- [x] Add only the missing navigation-repair messages to the existing news error table.
- [x] Run localization tests, Ruff, mypy and task validation, then close this ticket in PR #1444.

## How to verify

`apps/api/.venv/Scripts/python.exe -m pytest tests/test_error_localization.py`
from apps/api, Ruff for app/i18n.py, mypy app and tests, and
`node tools/tasks.mjs check`. Requery all four required checks on the new PR head.

## Notes

The exact-file ownership survey found no active claim or other open PR touching
apps/api/app/i18n.py. This task was claimed without a scope exception. CI log
SHA256 d9695f1b9450ddd63df3d8695640c417e7b4b255dd38be44f8cfe427b4f18251
records one failed test, 2036 passed, five skipped in the affected shard.
No test exemption or weakened assertion is planned.

Added eleven messages to each existing news locale map. Actual i18n SHA256
1b7187049202646a01a1e3047fa4a66512747540eeb50ca22fa96dc3326f228c;
non-author peer a9be0f006a4520560bb86f62ebbced1d263bf0e75805701fdb4a8ac2806d1e8b
read every Japanese/Korean sentence and confirmed all 55 values match the
immutable proposal. Removing only those entries restores the original file
byte-for-byte; every old AST node and sentence is unchanged. Unicode display
width was fixed only in the new entries after Ruff identified long lines.
Localization tests: 3 passed; Ruff: passed; mypy app/tests: 860 files passed;
task validation: 1779 files passed with unchanged foreign stale-claim warnings.
The original failed CI is preserved. New-head CI, conditional merge and production
deployment remain release gates and are not claimed complete by this ticket.
