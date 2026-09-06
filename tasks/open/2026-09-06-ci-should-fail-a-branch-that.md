---
id: 2026-09-06-ci-should-fail-a-branch-that
title: CI should fail a branch that adds a second alembic head
status: in-progress
priority: P1
area: ops
owner: claude-fable-5-1
claimed_at: 2026-09-06T02:29:36Z
created_at: 2026-09-06T00:55:40Z
completed_at:
branch: claude/ci-guards
depends_on: []
scope:
  - .github/workflows/ci.yml
  - apps/api/tests/test_schema.py
---

# CI should fail a branch that adds a second alembic head

## Why

Migration numbers are chosen when a branch is cut and the collision is only discovered
when it merges. That has now happened three times in three days:

- `0035_food_taxonomy` vs `0035_hotspot_area_code`
- `0039_ai_itinerary_refine_cost` vs `0039_repair_dead_food_sources`
- `0040_ai_itinerary_refine_cost` vs `0040_localized_names` vs `0040_trip_notes` — three at once

Each time the second branch to merge gives alembic two heads, `expected_schema_revision()`
raises `RuntimeError`, and every API test fails at import. Each time it was found by a human
mid-merge, and cost a renumber plus a round of CI.

`test_schema.py` already asserts the head by name, so a double head does fail the suite —
but only *after* the merge, on main, where a red `api` blocks nothing. Nobody notices until
the next branch merges on top of it.

## Definition of done

- [ ] A pull request whose branch would introduce a second alembic head fails CI on that
      pull request, naming both colliding revisions.
- [ ] The check runs against the merge result, not the branch in isolation — a branch is
      only in collision relative to the base it is merging into.

## Steps

- [ ] Add a check that walks `apps/api/migrations/versions/`, builds the revision graph and
      fails when more than one revision is never used as a `down_revision`.
- [ ] Wire it into the `api` job in `.github/workflows/ci.yml` so it runs on `pull_request`.
- [ ] Make the failure message name the colliding revisions and their `down_revision`, so
      the fix is obvious without reading the graph by hand.
- [ ] Consider whether `test_schema.py`'s hardcoded head assertion should stay. It catches
      the same class of problem but has to be edited by every migration, which is friction
      that produced at least one of the incidents above.

## How to verify

Create a throwaway branch with a second migration chained off the current head, open a
pull request, and confirm CI fails with a message naming both revisions.

## Notes

The pattern is always the same and always found late: two branches are cut on the same day,
both take the next number, both are green in isolation, and the second one to merge breaks
main for everyone. A pre-merge check is the only place this can be caught cheaply.

Worth pairing with a branch-protection decision: a red `api` on main currently blocks
nothing, which is why main stayed red across two commits on 2026-09-05 with nobody noticing.
That part is a repository setting rather than code, so it is not in this task's scope.
