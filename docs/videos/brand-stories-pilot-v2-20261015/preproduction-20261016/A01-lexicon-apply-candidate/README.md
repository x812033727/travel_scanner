# A01 81st lexicon event: offline append transaction candidate

**Status: HOLD.** `apply-fixture.mjs` can write only a marked directory under the operating system's temporary directory. It has no CLI, SSH, Docker, database, admin API, provider, retry, deploy, or paid path. Its success values keep `installation_allowed: false` and `paid_work_allowed: false`. The synthetic reviewer and approval strings in `apply-fixture.test.mjs` are test data, not A01 evidence.

The independently reviewed [rebaseline proposal](../A01-lexicon-rebaseline-candidate/README.md) is unchanged. It establishes the original 80-link pins, the single observed shared-lexicon delta (`pull: null`, `request: null`), the exact current source map, and four proposed bytes: one record-only installation receipt and three audit files. This package models how those bytes could be appended without rewriting any of the old 80 events. It does **not** authorize or perform that append on the host.

## Preconditions modeled by the fixture

`beforeRoot` is a separate immutable 80-event snapshot. `liveRoot` is a copy of that snapshot with an exact fixture marker. Both must be real paths under the OS temp directory with no root aliases; path traversal and symlinked source parents are rejected. The A01 and global `STOP` files must already exist as regular files, and A01 `LEASE` must be absent. The candidate never creates, clears, or removes either STOP.

The pure `prepareProposedEvent()` call binds **external** raw review and record-only receipt bytes to an exact `plan_sha256`, old/new lexicon hashes, source composites and the resulting 81-link pinset. This package additionally requires independently supplied hashes of those two files, the plan and the 81-link pins. String fields such as `reviewer` and `owner_approval_ref` do not authenticate a person; an operator must check real approvals outside this code.

A fresh (at most 60 seconds old) fixture safety object must match the plan and an explicitly supplied 40-hex deployed Git commit and 64-hex panel-rules hash. It reports a clean checkout, live worker, A01 project `blocked`, no retry ID, no queued/running stage or media jobs, no in-flight paid calls, unarchived run journals, unresolved run receipts or media files, plus the unchanged US$25 ledger with zero operations/reserved/settled. It must report both STOPs present and no lease. The module also checks the two STOP files and lease on disk. The fixture object is **not** a live database or provider reading. A future host adapter must collect and recheck this state itself while holding a lock respected by all A01 writers.

The original 80-link inspector must reject both **pre-append** snapshots solely for `SOURCE_DRIFT_FROM_TIP`, with its historical pins, anchor, all indexes and bound evidence intact. The live and immutable snapshot proposals must match byte for byte. Any additional source drift, historical evidence change, modified review/receipt, mismatched 81 pins, changed STOP, or changed safety object stops before a final audit file is published.

## Transaction and crash behavior

The transaction creates one exclusive directory at `story/lexicon-rebaseline-transactions/<event-id>` in the fixture, with a durable intent and exact staged files. It rechecks the proposal and STOP bytes, then atomically renames the new record-only receipt directory into `manual-revisions/<event-id>` and the new audit directory into `story/recheck-audit/<event-id>`. Only these two new final directories are published; the shared lexicon, original 80 audit files, existing receipts, A01 source, STOP and lease are never written. The audit directory is renamed last so an incomplete receipt publication cannot look like an 81-link chain. File contents are flushed; Linux directory fsync is present for a future adaptation, while Windows tests skip directory fsync.

After both renames, `inspect81Fixture()` calls the independently reviewed exact 80→81 transition verifier, checks the externally pinned 81 values, reads the new files back, and writes a local transaction readback. It is a two-snapshot inspector, not a replacement for the existing hard-coded 80-link production inspector. A host-facing 81-link inspector still needs a reviewed implementation and deployment plan before any operational promotion.

An exception during a running transaction removes **only** the two just-published directories, and only if every contained file still has its proposed bytes and no extra file appeared. It then revalidates the 80-link source/history. If another actor touched a proposed file, the rollback refuses deletion and reports `MANUAL_RECOVERY_REQUIRED`. A process death after publishing only the receipt leaves a partial state and a transaction journal; automatic retry is refused. A death after both directories are published can only return `ALREADY_APPLIED_LOCAL_FIXTURE` after the exact 81-link inspection passes. It never creates a second event. Recovering a partial live append would require a separate reviewed, owner-authorized recovery decision; this candidate does not silently delete it.

## Tests

```powershell
node --check docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-lexicon-apply-candidate/apply-fixture.mjs
node --test docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-lexicon-apply-candidate/apply-fixture.test.mjs
```

The tests construct disposable 80-link chains and cover exact append/readback, idempotent retry, hard-coded old-inspector refusal, missing STOP, present LEASE, stale/busy safety and nonempty budget, altered review/receipt/pins/source/history, rollback after either rename, interrupted receipt-only or complete append, and refusal to delete a concurrently changed receipt. They prove only the local transaction mechanics.

## Operational HOLD and next review

The last documented host readback at 2026-10-16 06:26 UTC had **no global or A01 STOP**, no real `independent-review.json` or record-only receipt, and no station-owner authorization for these two audit paths or STOP writes. It also found a blocked A01 project with one uncertain historical stage job and the shared lexicon drift. The readback is no longer a fresh preflight. The #1517 narrative-rule merge alone does not deploy the new worker rules; the separate deploy-worker race remains unresolved.

Before adapting this module to the actual split docs/work mounts, an independent reviewer must inspect this exact code and tests; the operator must make a fresh immutable source capture, revalidate the historical pins and lexicon delta, verify the independent human review and exact owner-approved path list, and obtain fresh DB, job, budget, STOP, LEASE and run-receipt readings. The worker must be paused and all A01 writers quiescent through the final readback. The host adapter needs its own crash/recovery exercise and must publish a new, separately reviewed 81-link inspector. Any mismatch leaves A01 at HOLD. This event does not create narrative PASS, script-review approval, TTS, media, B18/five-film production, or YouTube publication.
