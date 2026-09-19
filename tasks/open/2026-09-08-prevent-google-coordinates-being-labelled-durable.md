---
id: 2026-09-08-prevent-google-coordinates-being-labelled-durable
title: Prevent Google coordinates being labelled durable by merchant review
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-08T08:53:20Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/coordinate_queue.py
  - apps/api/tests/test_food_coordinate_queue.py
---

# Prevent Google coordinates being labelled durable by merchant review

## Why

Production coordinate_queue.apply_approval copies Google match.latitude/longitude to
catalog rows, labels them admin_verified and uses a Google Maps URL as permanent
provenance. This contradicts coordinate_fill's explicit rule excluding embedded
Google data and allows incomplete candidates to pass durable-coordinate gates.

## Definition of done

- [ ] Accepting a Google identity candidate never turns provider coordinates into durable catalog data.
- [ ] Preserve separately verified permanent coordinates and require independent provenance for publication.
- [ ] Add regression tests for missing coordinates, preserved genuine coordinates and Korean exact-map behavior.
- [ ] Define a separately authorized review of affected historical data; no blanket relabel or deletion.

## Steps

- [ ] Confirm current main and normal map approval flows before selecting the smallest fix.
- [ ] Fix and test queue approval without bypassing existing publication guards.

## How to verify

Run apps/api/tests/test_food_coordinate_queue.py and affected integration tests,
Ruff and mypy; verify new Google candidates remain non-public until independent
durable coordinate evidence exists.

## Notes

Confirmed in the running API container 2026-09-08 08:54 UTC: coordinate_queue.py
around lines 298-305 assigns Google match coordinates, admin_verified, Google URL
and fresh verification timestamp. No app code was changed by the editorial task.
Only its own prior four approvals were withdrawn with full audits; five pending
source repairs also cleared unsupported stamps. See
docs/catalog-review-followup-2026-09-08.md for exact operational scope.
Other administrators' previously published rows were not silently changed.

### 2026-09-19 補註

claude-opus-5 應站主「整理目前所有工作狀態」處理，盤點見 `docs/work-status-2026-09-19.md`。

在 main `161687ad` 重新確認問題仍在：`apps/api/app/foods/coordinate_queue.py` 的 `apply_approval`（第 298–303 行）把 Google 候選的 `latitude`／`longitude` 寫進店家、標成 `admin_verified`，來源寫 Google Maps 網址。每核准一筆就多一筆。
