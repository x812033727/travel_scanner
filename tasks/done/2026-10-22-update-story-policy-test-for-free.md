---
id: 2026-10-22-update-story-policy-test-for-free
title: Update story policy test for free channel CTA
status: done
priority: P2
area: api
owner: codex-s34-policy-ci-fix
claimed_at: 2026-10-22T03:54:40Z
created_at: 2026-10-22T03:54:35Z
completed_at: 2026-10-22T03:56:20Z
branch: codex/curio-s34-self-cta-policy-20261022
depends_on: []
scope:
  - apps/api/tests/test_video_story_policy.py
---

# Update story policy test for free channel CTA

## Why

PR #1664 clarified the shared Jev sponsorship question, but the brand-story API regression suite still expected the former tutorial question word for word. That deterministic assertion made `api-tests (2/4)` red; the new sponsorship rule itself was already covered by another test.

## Definition of done

- [x] The tutorial's full four-question contract test expects the current exact sponsored question, including the narrow free own-channel subscription exception and retained paid/external promotions.
- [x] Focused API regression tests and Ruff pass.

## Steps

- [x] Reproduce the old expected literal in `test_video_story_policy.py` and compare to `judge.py`.
- [x] Update only the stale expected sponsored literal and its comment; keep the whole-question equality assertion.
- [x] Run focused API checks.

## How to verify

From `apps/api`, run `uv run pytest -q tests/test_video_story_policy.py tests/test_video_automation_judge.py` and `uv run ruff check tests/test_video_story_policy.py`; both exited 0 (61 tests passed). CI shard should be reread after this PR push.

## Notes

The PR also has a separate `test:tools` failure because `apps/api/app/video_automation/judge.py` is covered by the independent long-form duration review hash. That binding must be reviewed and updated by someone other than this patch author. Direct GitHub Actions job logs return 403 in this environment; step metadata and local reproduction identified the failures.
