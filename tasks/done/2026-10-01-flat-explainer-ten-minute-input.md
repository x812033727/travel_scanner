---
id: 2026-10-01-flat-explainer-ten-minute-input
title: Allow ten-minute flat explainers without changing drama episode limits
status: done
priority: P1
area: api
owner: codex-longform-input
claimed_at: 2026-10-01T16:00:43Z
created_at: 2026-10-01T15:59:52Z
completed_at: 2026-10-01T16:44:05Z
branch: codex/sothatswhy-season2-complete
depends_on: []
scope:
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/series.py
  - apps/api/tests/test_video_explainer_duration.py
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-explainer-duration.test.tsx
---

# Allow ten-minute flat explainers without changing drama episode limits

## Why

The owner extended the video catalog's long-form plans to a ten-minute production target
with an eight-minute finished-video minimum. The illustrated explainer was still capped at
eight minutes and defaulted to three in both the request API and the admin form, so those
plans could not be submitted. Normal drama episodes retain their existing short format.

## Definition of done

- [x] Flat-explainer one-offs and requests accept 8–20 whole minutes and default to 10
  when the length is omitted. Other dramas retain the 1–8 range and default of 3.
- [x] Patches use the resulting kind/style, allow an existing short explainer to be
  corrected, and preserve the ability to pause or rename it while it is being revised.
- [x] The admin request form follows the API's defaults and bounds when changing style;
  switching between normal drama styles keeps the owner's chosen short duration.
- [x] Independent API and UI regression files cover the valid endpoints and defaults,
  under/overlength input, fractional/boolean input, and style-only patch persistence.

## Steps

- [x] Confirm the existing database columns and constraints accept the new input range.
- [x] Implement API creation/patch validation and the corresponding admin form behavior.
- [x] Run targeted new and existing regression suites, ruff, mypy, eslint and web typecheck.

## How to verify

From `apps/api`:

```text
uv run ruff check app/video_automation/schemas.py app/video_automation/series.py tests/test_video_explainer_duration.py
uv run mypy app/video_automation/schemas.py app/video_automation/series.py tests/test_video_explainer_duration.py
uv run pytest tests/test_video_explainer_duration.py tests/test_video_drama_requests.py tests/test_video_series.py tests/test_video_series_binge.py tests/test_video_story.py -q
```

From `apps/web`, with the bundled Node 24.19 runtime:

```text
node ../../node_modules/vitest/vitest.mjs run components/admin-video-explainer-duration.test.tsx components/admin-video-series.test.tsx
node ../../node_modules/eslint/bin/eslint.js components/admin-video-series.tsx components/admin-video-explainer-duration.test.tsx
node ../../node_modules/typescript/bin/tsc --noEmit
```

## Notes

- Collision audit before claiming: the overlapping 2026-09-27/28 claims are older than 24
  hours, their former branches have no active checkout, and the relevant document-edit
  implementation already landed in #978 (`9656d0d9`). Root forced this narrow new claim;
  no other owner's task is released or completed. Open #1097 changes Shorts fields in the
  same schema file and #1085 changes character-look validation in the same service; these
  submitted changes are outside the duration hunks here. Before final delivery, the newly
  pushed `claude/video-min-8-minutes` branch was also found; its general duration work is
  complete but unmerged, and the draft PR must retain this overlap as an integration note.

- The existing `ck_video_drama_series_numbers` already accepts 1–20 minutes, and
  `video_drama_requests` has no minute-range CHECK. This change needs no migration or backfill.
- Style-only changes into the explainer choose 10 minutes; changes out choose 3. Re-selecting
  the explainer style repairs an older short target to 10. Explicit lengths are validated.
  A written bible still prevents crossing the explainer/drama boundary.
- An unrelated pause/title patch on a legacy short explainer remains available; it does not
  certify a short finished video. The final media minimum belongs to the separate QA gate.
- The explainer field label reuses the existing translated `minutes` message, showing
  `8–20` without adding message keys or changing normal drama copy.
- Local validation on 2026-10-02: API regression suite **84 passed, 3 skipped**, exit 0.
  The skips require the PostgreSQL integration environment. UI regression suite **30 passed**,
  exit 0. Ruff, scoped mypy, eslint and full web typecheck also exited 0. No production
  settings, jobs, media or database rows changed.

- After rebase onto `abbc276d`, frozen dependency sync installed urllib3 2.8.0;
  the same affected API suites again passed 84 tests with three database skips,
  the two UI suites again passed 30 tests, and scoped ruff/full web typecheck passed.
  Future shared-branch duration integration is tracked by
  `2026-10-01-longform-duration-merge-integration`, separate from this completed input change.

- The final rebase onto `eda3b60f` incorporated #1085 character-look validation.
  The affected API suite then passed 105 tests with three skips; four-file ruff/mypy
  exited 0. Independent incremental review confirmed the minute-patch blocks are
  byte-identical; the genuine report and refreshed receipt were installed and checked.
