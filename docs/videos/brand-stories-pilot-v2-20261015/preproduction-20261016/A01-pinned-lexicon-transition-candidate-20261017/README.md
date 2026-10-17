# A01 historical pronunciation pin — offline candidate

Status: **HOLD, not deployed**. This directory contains a local planner, read-only inspector and a separately reviewed guarded adoption API. The adoption API writes only when explicitly invoked by an authorized host caller with the external gates below satisfied. There is no apply CLI, provider call, database write, retry reset or release command. No actual 81st event has been written.

## Why this transition exists

A01's 80-event audit tip used the historical ebfa590a dictionary. The morning captured shared dictionary is e6403c82 with 23 additions; the afternoon capture is 4d3e995b with four more exact additions. supported-baseline.mjs accepts only these two captured versions, their exact 23/27-term deltas, unchanged old values and the immutable historical 80-link pins. Unknown hashes still refuse. Runtime draft PR #1548 requires an immutable dictionary per story and refuses to initialize legacy A01 automatically. This candidate preserves the historical dictionary bytes instead of adopting those additions.

The planner authenticates the captured chain through the existing e640 rebaseline validator, then creates the exact immutable version/event/current format consumed by #1548. Only two state fields are added: story.lexicon_sha256 and story.lexicon_head_event_sha256. Retry counters, chapter states, narrative decisions and every historical audit byte remain unchanged. The state metadata makes the new audit source distinct; an unchanged source would create a self-edge in the old equality-based audit graph.

## Evidence and boundaries

- Five synthetic tests pass: intact transition, old-file mutation/addition rejection, partial publication/shared drift/extra approval rejection, and evidence identity/state mutation rejection. Synthetic owner/review strings are test data only. The read-only inspector CLI rejects incomplete or write-like arguments with exit 2; even an exact local readback keeps release_allowed:false.
- local-plan-summary.json records a read-only plan against the captured 80-event source; 185 historical evidence files were hashed. This is a plan, not a persisted migration or permission to publish it.
- snapshot-format.mjs is the #1548 format module with only its two relative imports adjusted. Restoring those import paths gives SHA-256 66e11923b9de4a0ac065a1f4f9b38819c665ee7fa53a32957490069286434982.
- preparePinnedEvent requires separately supplied review and owner-record bytes, bound to this plan and source hashes. Matching strings cannot authenticate a person or create authorization; the future caller must verify authority separately.
- verifyPinnedTransition checks complete historical file sets and bytes, exactly one new audit event/revision, exactly three snapshot files, unchanged shared dictionary, strict runtime readback and the complete resulting source tuple. It continues to return HOLD and paid_work_allowed:false.

## Local use

Run transition.test.mjs with Node 24.19 or later using --test. The planning CLI accepts only --snapshot <local-capture-root> --old-lexicon <historical-json>. It prints a plan and never writes outputs.

## Still required

Independent host-caller review and deployment of the required runtime; current host locks and DB/job/budget preflight; a fresh matching production export and explicit host action authorization; resolution of the uncertain legacy job; and guarded application of the reviewed 81-to-82 narrative transition bound to the pinned dictionary. The older e640 round20 bridge does not validate this new source. A01 must pass factual, listening and storytelling gates before paid media. The adoption API can append the held 81st event after its external gates are met; it cannot approve a script, reset retries, change the shared dictionary, release a HOLD, deploy #1548, or complete a film.

## Read-only pinned inspection entry

inspect-pinned.mjs --before <local-80-capture> --after <local-81-capture> --old-lexicon <historical-json> reuses the complete transition verifier and emits a compact JSON report. Exit 0 means only the exact captured transition passed integrity checks; production_status remains HOLD and release/installation/paid flags remain false. Exit 2 means inspection failed. It does not inspect or settle SQL jobs, acquire production locks, verify human authority, adopt data, or validate later narrative events. The original historical 80-link inspector is unchanged. A same-root check of the actual 80-event capture correctly returned HOLD/ENOENT because a real 81st event is absent.

## Guarded adoption API (reviewed locally, not run on production)

adopt-pinned.mjs requires deployed runtime hashes in required-runtime.json, exact before-source/plan pins, separately authenticated owner authority and hash-bound independent evidence. The host caller must hold deployment locks and establish current SQL/job/budget safety; the API does not acquire host deployment locks or settle DB jobs. Do not invoke it from a different container hostname from the actual worker.

The API takes separate root and workBase volumes, uses the worker project lease and shared pronunciation-writer lease, creates or preserves A01 STOP, then publishes durable work/docs intents, immutable evidence and pronunciation bytes, auto metadata, and finally the current pointer. Fresh copied source readback must match the complete reviewed transition before a committed receipt is recorded and its own fences are cleared. STOP remains. No production-wide STOP is removed or created.

An interruption keeps STOP and pending intent evidence. Explicit recoverCommitted mode clears only a matching, fully committed receipt with exact source/STOP/fence readback; pre-commit partials refuse recovery and require separate review. Captures are retained in OS Temp for investigation. A valid integrity report still has release_allowed:false and paid_work_allowed:false.

Three portable adoption tests independently pass, covering seven checkpoint interruptions, both committed recovery cases, and runtime/source drift. These synchronous exception tests are not power-loss or cross-container consumer tests; see adoption-review.md. The synthetic runtime override is restricted to marked OS Temp fixtures. All three test/runtime reports and earlier review history are preserved.

## Current manuscript handoff

pinned-revision-plan.mjs now targets the isolated round22 spoken-callback package (manifest d7c321dfb9871511367fe748163d1d3e38f31d4c72d4281284ebaee603b96da6). Old round20/21 packages and their review reports remain historical. The chapter transition is a separate82nd event, invalidates checker/listener flags and starts a fresh checker/lint cycle: six check_rounds/lint_fixes become0 and changed tallies are removed, with previous counters retained in the81capture/plan/author record. A pin-only authorization does not cover that source revision; the actual authorized scope must include it. Narrative failure, rounds9 and narrative_fixes2 remain unchanged. There is no auto-retry or paid release here.

The real afternoon capture still has80events,109succeeded/1uncertain historical stage job,0media jobs and the fullUS$25 budget unused. Its199source files differ from the morning only in the shared dictionary;198others match. Fresh plan SHA3a08217137dabd3ca57256cb12f73ae6b9ced9e86cf66704b17fd4ea64f21220 was independently reproduced. This is read-only proof; not a real81/82append.

## 2026-10-17 actual host readback

- Runtime PR #1548 is merged/deployed at `4f02734769f683615d1ca8b641026ac8cf1f87b5`; full host verifier passed 12/12. No migration; database remains 0132.
- Historical dictionary pin adoption (80 -> 81) committed while held. The 206-file host export passed local verification; 185 original historical evidence files are byte-identical. See `actual-81-readback-20261017.json`.
- Round22 existing-chapter source adoption (81 -> 82) committed while held. The 210-file host export passed local verification, source `729a1c47e955448968908cd6ba2a0f8ff4257c0a7a1f951b0de744696c8d5a8d`. See `actual-82-readback-20261017.json`. Six chapter checks/listening and the new source check cycle are invalidated; prior counters and narrative failures remain preserved in immutable history.
- Both own global release holds were cleared only after verified export success. The project STOP remains; no paid request, media generation or YouTube upload was made during adoption.
- `adopt-revision.mjs` is the guarded production source-adoption API; the older `pinned-revision-plan.mjs` remains a read-only proposal/verification model. Production APIs reject fixture overrides.
- `review-batch.mjs` is a separate bounded real-worker review driver. Its first review found missing audit-before-settle, durable-mode and block detection protections. Initial findings are preserved; updated code requires independent no-model validation before any --run. Its --preflight passed against actual host source 82 with STOP preserved and zero paid calls. Formal verifier/listener/panel and the pilot script-review gate have not passed yet.
