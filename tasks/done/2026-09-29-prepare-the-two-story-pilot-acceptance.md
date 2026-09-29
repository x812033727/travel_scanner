---
id: 2026-09-29-prepare-the-two-story-pilot-acceptance
title: Prepare the two story pilot acceptance plan
status: done
priority: P1
area: docs
owner: codex-story-pilot-plan
claimed_at: 2026-09-29T02:57:56Z
created_at: 2026-09-29T02:57:47Z
completed_at: 2026-09-29T03:03:16Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - docs/work-status-2026-09-29-story-pilot-plan.md
---

# Prepare the two story pilot acceptance plan

## Why

The owner requested a concrete two-story pilot plan once the dependencies were ready. PR #933 merged on 2026-09-29, so the earlier wait-only plan can now be expanded without starting production work.

## Definition of done

- [x] A01 and B18 have exact input hashes, slugs, release prerequisites, settings, bounded budgets, staged import, acceptance and recovery steps in the scoped document.
- [x] The plan preserves the original pilot ticket, production authorization and owner review; no jobs or media are created.

## Steps

- [x] Verify #933 merge and main ancestry including #938; read the newly merged story skill and original pilot criteria.
- [x] Validate the backlog offline and compare the seven input files to the exact Git commit.
- [x] Independently check budget/concurrency/final-review settings and document limits rather than claiming total-cost enforcement.
- [x] Run task validation and finish this plan-only ticket in the existing draft PR.

## How to verify

Bundled Node 24.21.0: `node tools/video/story-plans/validate.mjs` and `node tools/tasks.mjs check`. Read-only GitHub PR checks/compare plus raw Git blob and local SHA-256 parity for seven inputs. No live DB/model/host calls.

## Notes

- #933 merged `157cca889a169ebf9f0af4f609be69388b8f6d2e`; final head four required checks SUCCESS. GitHub compare to #938 reports ahead 1 / behind 0.
- Original pilot remains open; this ticket completes only `docs/work-status-2026-09-29-story-pilot-plan.md`.
- Scope collision helper found no active task or open PR touching this new document; work stays on the root-owned shared branch, no commit/push by this agent.
- Offline backlog check: 100 stories / 50 days / 0 problems, exit 0. Seven exact-commit blobs match local bytes.
- Independent settings inspection by audit_product: max_usd_per_video is only media estimate protection, judge is charged without spend precheck, TTS/text costs are separate. The plan keeps total-cost control/rehearsal and existing image-model-pricing work as prerequisites; no claim that 25 in settings guarantees total cost. The original pilot's cost acceptance remains incomplete.
- The original 720–900-second acceptance is stricter than worker narration 690–930 seconds; preserve it. `drama_auto_approve_final=false` is honored even for hands_off stories.
- Task validation: 1,093 files, exit 0 (pre-existing stale/overlap warnings); `git diff --check` exit 0. Completion means preparation only, not execution of the original pilot.
- audit_product independently reviewed the finished settings/budget/import/final-gate plan; no substantive issues. Clarified the actual `auto --once` command and that total cost requires combined provider receipts, not a single all-inclusive server ledger.
