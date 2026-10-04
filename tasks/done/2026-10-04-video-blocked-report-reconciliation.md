---
id: 2026-10-04-video-blocked-report-reconciliation
title: Reconcile saved blocked video states to backend reports
status: done
priority: P2
area: tools
owner: codex-video-recovery-20261004
claimed_at: 2026-10-04T06:02:01Z
created_at: 2026-10-04T05:51:24Z
completed_at: 2026-10-04T07:16:37Z
branch: codex/video-pipeline-recovery-20261004
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
---

# Reconcile saved blocked video states to backend reports

## Why

The read-only production audit on 2026-10-04 found two videos stopped in their persisted
worker state while the backend still presented their earlier stages:

| Video | Persisted `auto.json` | Backend project |
| --- | --- | --- |
| `ai-term-temperature` | `status: blocked`, writer HTTP 504 / lost answer | `stage: retrying`, last synced 2026-10-03 16:55:55 UTC |
| `ai-term-knowledge-cutoff` | `status: blocked`, writer HTTP 504 / lost answer | `stage: outline approved`, last synced 2026-10-03 23:45:55 UTC |

Both stored reasons say the writer may have run on the server without its answer reaching
the worker and is not asked again until the owner retries. The UI cannot expose the real
stop through its normal blocked state; the backend retry endpoint also refuses a project
whose recorded stage is not `blocked`.

The source has a failure window: `Automation.block()` saves `auto.json` before awaiting
the backend report. A failed report leaves the local stop intact; later rounds skip blocked
states unless the owner has already requested a retry, and there is no reconciliation of
the missed report. The observed local/backend mismatch is confirmed. The exact original
reporting failure for these two videos is unconfirmed; the available capture does not
establish whether the report suffered transport failure, process interruption or another
error. Do not assert a particular cause without older logs/evidence.

## Definition of done

- [x] A persisted blocked state whose backend stage/checklist is stale is reconciled on a
      later worker round using a report only, without replaying any paid model/media call.
- [x] The backend receives the actual blocked reason and current checklist, so the normal
      retry action becomes available; repeated reconciliation is idempotent.
- [x] A reporting failure leaves durable evidence of the pending report and is retried with
      appropriate pacing. Failure for one blocked video does not indefinitely starve other
      videos or create a tight reporting loop.
- [x] Reconciliation respects owner drop/withdrawal, current one-shot retry identity and
      acknowledgement. An owner-requested resume must not be overwritten by a stale block.
- [x] Existing uncertainty safeguards remain intact: a writer response lost at HTTP 504
      is not paid for again merely to refresh the UI, including after a worker restart.
- [x] Focused tests cover save-before-report failure, restart, stale backend stages, repeated
      report failure, successful reconciliation, owner drop and a new retry request.

## Steps

- [x] Compare persisted states to current backend records without changing either.
- [x] Trace block persistence/report ordering and blocked-state filtering.
- [x] Search the shared queue for an existing exact reconciliation ticket.
- [x] Reproduce a missed report with the fake backend before modifying implementation.
- [x] Add durable report reconciliation preserving the existing retry/drop contract.
- [x] Validate reporting recovery without paid submissions or production changes.

## How to verify

Implemented save-before-report pending evidence, five-minute report backoff and
legacy stage/checklist reconciliation. Owner drops and one-shot retries take
priority, and a failed report can leave other videos progressing. Failing-first
fixtures proved the old exception/stale stage behavior; restart/reconciliation
fixtures pass with exactly one writer call. Existing owner retry/acknowledgement
tests remain passing. No live project or worker state was changed.

Use the existing automation fake site: let a writer request produce an uncertain outcome,
then fail the first blocked report after `auto.json` has been saved. Start another worker
round from that persisted file while the backend still says `retrying` or `outline approved`.
Assert the report eventually becomes `blocked` with the stored reason, model-run count
stays one, and the actual backend retry contract can accept a fresh owner request. Repeat
with reporting unavailable across rounds, a dropped project and a retry arriving during
reconciliation. Keep owner requests distinct from reporting attempts.

```bash
node --test tools/video/automation/automation.test.mjs tools/video/automation/client.test.mjs
npm run test:tools && npm run check:tasks
```

Any later production validation needs a separately authorized deploy and must compare
`auto.json`, backend `stage`/checklist, one-shot retry IDs and model-run counts. A recovered
report alone does not mean the writer answer or video has been recovered.

## Notes

- Diagnosis-only ticket, open and unclaimed. This audit did not edit source, change
  production settings/state, retry generation or submit paid requests.
- Source pointers in the audited checkout:
  - `tools/video/automation/flow.mjs:1204-1209`: block writes local state before `report()`.
  - `tools/video/automation/flow.mjs:429-448`: report derives stage/checklist for the backend.
  - `tools/video/automation/flow.mjs:625-645`: later rounds move only active/done states.
  - `tools/video/automation/flow.mjs:666-710`: bookkeeping handles drops, explicit retries,
    YouTube IDs and compilation completion, but not a missed blocked report.
  - `tools/video/automation/flow.mjs:672-693,715-720`: preserve exact retry identity and
    existing retry-acknowledgement recovery when adding report reconciliation.
  - `tools/video/automation/client.mjs:79-118`: report retry errors can still escape after
    the bounded client attempts; do not reuse the paid-run retry path for reconciliation.
  - `apps/api/app/video_reviews/admin_service.py:1822-1833`: the owner retry endpoint
    requires backend `stage == "blocked"`; it is a read-only source pointer, out of scope.
- Live capture outside git:
  `%TEMP%/mokaair-video-diagnosis-20261004/host-output.txt`, PROJECT rows 33/36 and AUTO
  rows 193/196 in this audit. Keep credentials, requests and capability URLs out of git.
- The coordinator verified SHA-256 equality for deployed worker `automation/flow.mjs`
  and this checkout, together with `core/state.mjs`, `review/sync.mjs`, `render/plan.mjs`,
  API `video_automation/settings.py` and the BFF automation-run route. Local HEAD was
  `7f2744a`, live repository HEAD `d038b035`; these relevant files were byte-identical.
  This confirms the save-before-report/skip-blocked mechanism exists in the audited live
  source, while the exact initial failure of the two reports remains unconfirmed.
- Related `2026-10-04-full-script-writer-timeout-result-recovery` handles writer deadlines
  and answer retrieval; this ticket handles truthful persisted status/report recovery.
  Coordinate overlapping scopes before implementation. The existing
  `2026-10-02-stop-repeating-lost-stage-answers-outside` covers other stage callers,
  not the saved blocked-video report mismatch.
- Initial transport/process cause remains unconfirmed. The defect can be reproduced
  independently by failing a report after local persistence; that is not proof which
  failure happened to the two live videos.

## PR handoff (2026-10-04)

Implementation and independent review are included in draft PR #1203. This task
records completed source work and validation, not a production deployment or a
recovered/published video. All four API shards passed 6695 tests with 22 skips;
API Ruff/Mypy, Web checks and all three Web unit shards passed on source head
dc2a4b194. The complete tools suite passed 1536 tests with 2 skips. Real PostgreSQL/Redis shard 4 passed 1352 tests
with 9 skips, including the saved-items lifecycle regression. Final aggregate CI
results are recorded in the PR. Existing media switches, caps, owner approvals
and disabled uploader were not changed.

Local API broad run: 6070 passed, 442 skipped; 28 Windows-only failures were
rechecked with UTF-8 mode. The relevant collection then passed 173 tests with
1 skip and only the unavailable Windows symlink privilege case remaining.
That test-platform gap is tracked separately as
2026-10-04-python-anime-planning-symlink-windows.
