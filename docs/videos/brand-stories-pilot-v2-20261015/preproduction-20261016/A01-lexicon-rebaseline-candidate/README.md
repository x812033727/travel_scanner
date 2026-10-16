# A01 lexicon rebaseline candidate — offline only, HOLD

This package proposes one append-only **81st** A01 source audit event after the independently pinned 80-event history. It reads local snapshots and prints a plan or transition check. It has no SSH, database, deploy, model, media, installer, retry, STOP/LEASE or paid path. `LOCAL_81_EVENT_TRANSITION_PASS` still reports `production_status: HOLD`, `installation_allowed: false` and `paid_work_allowed: false`.

The 2026-10-16 readback in [`A01-live-readback-20261016.md`](../A01-live-readback-20261016.md) found the intact 80-link tip `c7ddb6b5…`, source composite `cf39296d…`, and only the shared mounted `docs/videos/lexicon.json` changed from `ebfa590a…` to `835e09df…`. The two added entries are `pull: null` and `request: null`. The old bytes are preserved in `A01-round10-candidate/evidence/round9-lexicon.json`; the current worker-mounted file must come from a **fresh, complete, immutable local capture**. The repository checkout's lexicon hash is a third value and must not substitute for the mounted file. The code pins both real hashes and the historical 80-event pins in its CLI. It refuses other source drift and any occurrence of the new terms in spoken lines from all six chapter JSON files **and** `video.json`, using the real TTS choice `line.say ?? line.text`. Camera and image prompts are outside that narration check.

**Systemic limit:** the source composite currently binds the entire shared mutable lexicon. Another unrelated video adding even one term will drift A01's live source composite again. This 81st event handles only the observed `ebfa590a…` → `835e09df…` change; it does not stabilize future A01 reads. A separate narrowly scoped task should design a per-story immutable lexicon snapshot (or equivalently stable source binding), the worker read path, hash migration, and backward compatibility for existing audit links. This candidate does not edit the shared worker or rebind other videos.

## Offline proposal

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-lexicon-rebaseline-candidate/rebaseline.mjs `
  --snapshot C:\path\to\complete-80-event-local-capture `
  --old-lexicon C:\path\to\round9-lexicon.json
```

The snapshot uses the exact layout required by `A01-host-inspect-candidate`. The planner reruns its 80-event verifier. That verifier must reject the current capture for **exactly** `SOURCE_DRIFT_FROM_TIP`; its validated anchor, all 80 indexes, all bound journals/reviews/receipts, original tip and index manifest must match the historical pins. This tool then checks that every other source hash equals the tip, the old and current lexicon bytes have the pinned hashes, the JSON delta is exactly the two null terms, and neither term occurs in `line.say ?? line.text` for chapter or video scenes. It also hashes every historical audit file and installation receipt to make the before/after comparison exact. The output plan includes the before and after source maps, composite, event ID, prior pins, full historical file digest, and a deterministic `plan_sha256`. This is a proposal, not a production approval.

The saved **06:24 UTC local snapshot** documented in `A01-live-readback-20261016.md` passed this offline proposal on 2026-10-16 with `plan_sha256=3ca62cfa4386c43dd0d45a6554fa3df63ddceb51f23bd48e9a9de9c2ab693f58`, after-source composite `2a54ed212c1d876664e17f73fc39f8a20b1ddddccb6c877de54c694c5634501a`, 295 → 297 terms and zero chapter narration hits. That snapshot is historical evidence; it does not establish the host's state after the capture.

The proposed event ID is `lexicon-rebaseline-835e09df378d0c1b`; its revision directory has the same suffix. The event's `before_source_sha256` is the original `cf39296d…` tip; its `after_source_sha256` is SHA-256 of `JSON.stringify(after_source_hashes)` in the existing source-key order. The old 80 index bytes and pins are never rewritten. The candidate's exact new tip and 81-index manifest hashes cannot be finalized until independently authored review and record receipt bytes are supplied, because the event index binds both by SHA-256. Do not fill those with fabricated PASS or owner approval text to make the tool green.

## Review and receipt contract

`prepareProposedEvent()` is a pure exported function for a separately reviewed local adapter. It takes the immutable before snapshot, archived old lexicon, and **external** raw bytes for:

- `independent-review.json`: `schema_version: 1`, `kind: "a01_lexicon_rebaseline_independent_review"`, A01 `slug`, `verdict: "PASS"`, `independent: true`, a nonempty `reviewer`, exact `plan_sha256`, old/new lexicon SHA, before/after source composite SHA, and the exact `delta` from the plan.
- `manual-revisions/<event-id>/installation-receipt.json`: `schema_version: 1`, `kind: "a01_lexicon_rebaseline_record_receipt"`, A01 `slug`, exact plan/event/revision and before/after hashes, the review-byte SHA, `record_only: true`, `lexicon_file_writes: 0`, a nonempty `operator` distinct from the reviewer, and a nonempty `owner_approval_ref`.

The function rejects missing or mismatched fields, then returns the exact proposed `index.json`, `author-manifest.json`, review and receipt bytes, and all five fields of a new 81-link pinset. It writes nothing. A string naming a reviewer or approval is **not authentication**: the owner approval and independent reviewer identity/content must be checked outside this tool. The actual shared lexicon mutation's provenance is still unresolved; this record-only event must not claim that the rebaseline writer added the terms.

With those independently supplied local files, `--prepare` prints the exact SHA-256 of each proposed file and the new pins without printing their contents or writing to disk:

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-lexicon-rebaseline-candidate/rebaseline.mjs `
  --prepare C:\path\to\complete-80-event-local-capture `
  --old-lexicon C:\path\to\round9-lexicon.json `
  --review C:\path\to\independent-review.json `
  --receipt C:\path\to\installation-receipt.json
```

## Exact transition verification

After an independently authorized and reviewed append procedure has produced a **separate immutable after snapshot**, the CLI can compare it with the original 80-event capture:

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-lexicon-rebaseline-candidate/rebaseline.mjs `
  --before C:\path\to\original-80-event-capture `
  --after C:\path\to\new-81-event-capture `
  --old-lexicon C:\path\to\round9-lexicon.json
```

The verifier revalidates the original 80 events, recomputes the plan, parses and binds the externally supplied review/receipt, then demands exactly the old 80 event IDs plus the proposed event. Every prior audit file and installation receipt must retain its original bytes. The after snapshot's source map must equal the proposed map; the new event and revision directories may contain only their expected files, with exact canonical bytes. Finally it recomputes the 81-index manifest and new tip pin. Missing files, an extra/duplicate event, a changed old link, altered review/receipt, different A01 source, concurrent lexicon change, or a partial append all reject. The before and after roots must differ. A caller must retain both snapshots and their independently recorded capture hashes; this tool cannot prove their host origin or freshness.

An operational adapter would need a new task, independent code and evidence review, exact owner authorization for the A01 audit/receipt write, a fresh no-drift host preflight including STOP/LEASE/jobs/budget, a crash and rollback plan, and a second host readback. It must then update the production inspector from exactly 80 to exactly 81 events under reviewed pins. This candidate makes **no** change to that inspector and no production write. The missing real narrative PASS, exact-file script review receipt, A01 media QA, and deploy worker race remain separate HOLD gates; no B18/five-film production or YouTube upload is authorized here.

## Synthetic verification

```powershell
node --check docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-lexicon-rebaseline-candidate/rebaseline.mjs
node --test docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-lexicon-rebaseline-candidate/rebaseline.test.mjs
```

The tests build disposable synthetic 80-link archives under the OS temp directory. Their PASS is about this candidate's behavior and is not evidence that the formal host readback, reviewer, owner authorization, or post-append transition happened.
