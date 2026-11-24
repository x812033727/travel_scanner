# Independent review of the read-only production observation

Reviewer: `brand_resume_review`, independent of the capture author. Date: 2026-10-20.

**PASS for read-only capture scope, export minimization and the bounded status interpretation.** This is a review of stored observations and code. The reviewer made no network request and did not read credentials, perform pairing, change settings, retry a project, generate media or upload anything.

## Exact reviewed files

Paths are relative to this directory.

| File | SHA-256 |
| --- | --- |
| `capture-live.mjs` | `aff9f7a68c84d371e048821b05e287bf1ee59899b009abe72cc5878fc55e45bd` |
| `live-status.json` | `b739859a6db97bbf22c2ac215d8d64c69719a9d6f6edc5ec9a13b69f764cae54` |

The exported observation window is **2026-10-20 00:39:40.327–00:39:47.813 UTC** (08:39 in Taiwan). Requests are sequential; the result is not an atomic snapshot or a guarantee of the present state. A later refresh invalidates this report's file binding until that output is reviewed again.

## Read-only request paths and data handling

Read the capture script and the relevant implementations in `tools/video/automation/client.mjs` and `tools/video/media/client.mjs`. The capture uses only:

- `client.settings()` → GET `automation/settings`.
- `mediaStatus(...)` → GET media `status`.
- `client.videos()` → GET `automation/videos?shorts=exclude`.
- `client.reviews(slug)` → GET `reviews/<exact slug>`; its existing client normalizes only HTTP 404 to a missing result.

The invoked methods do not submit model jobs or other mutations. `attempts: 1` is set. Credentials are obtained internally through the existing paired client and are not printed or included in the exported object. This reviewer inspected the credential **call sites only**, not credential files or values.

The output retains selected settings flags, provider/model configuration status, two relevant pilot budget summaries, selected project state fields, locale part state/reason, final content hash and timestamps, stored duration, failed QA summaries, and review gate/status timestamps. It does not export raw settings, full review payloads, administrator identities, tokens or media. An independent recursive scan of this exact output found no credential/identity/payload keys, Bearer authorization strings, URL userinfo or email addresses. This scan is supplementary to inspecting the actual export allowlists; it is not a claim about arbitrary future server text.

## Stored observation comparison

Compared only the allowed existing private readback files `videos.json`, `settings.json`, `media-status.json` and the six `story-*.json` snapshots. No other file in the private directory was read. An independent Python comparison returned exit code 0; `node --check .../capture-live.mjs` also returned exit code 0 without executing the capture.

The six exported project slugs agree with the story rows found in the earlier list snapshot. The exported stage, series, ready flag, synchronization timestamp, worker-state label, download flag, YouTube ID, locale state/reason, review history subset, final hash/timestamps, stored final duration and failed QA items agree with the earlier per-story snapshots. The one dynamic discrepancy is B26's `media_usd`, which differs between observations. It is therefore not described as a byte-identical raw-snapshot reconstruction; the field is explicitly labeled a media subtotal, not an all-in cost ledger. Selected settings and the two pilot budget summaries agree with the allowed snapshots.

The exported state supports these limited observations:

- Six projects were observed. A01 is `retrying`, B26 is `narration approved`, and Dolby is `languages`.
- A4, Michelin and Seiko have `ready_to_upload: true`; all three nevertheless report **skipped en/ja/ko dubs**. The ready flag is not evidence that those audio tracks exist.
- Four projects retain an approved final record whose submitted QA says `ok: false`. The export preserves the failed item details and the approval together. It neither revokes the owner decision nor claims a fresh all-green media check.
- The duration values are stored submitted **final** durations. They are not new ffprobe results or body-only narration measurements.
- `worker_state: unavailable` means the API could not read producer state. It does not establish that the producer stopped.
- The generic media cap is US$200. The captured A01 pilot summary has a US$25 limit and B18 has US$5. None of these values establishes vendor cash balance, a complete historical spend ledger or authorization to spend.

## Inventory bound and remaining limitations

The initial list response has 200 rows. During this review the author added `catalog_scope` to retain that limit, set `exhaustive: false`, and probe known pilot/five-series slugs exactly. The final export records 12 exact probes and six 404/missing-project results (B18 and the five `story-five-*` slugs). This reviewer verified the handling in code and the recorded scope; it did not independently repeat those requests. A missing project response is not evidence that host media/workspaces do not exist, and the capped list is not a full production inventory.

The exported limitations correctly leave host files, release/worker SHA, locks, actual producer liveness, original chapter/timeline/speech artifacts and provider cash balances unverified. No unresolved capture/export defect was found in the exact reviewed files. This review adds no production, payment or publication approval and does not supersede the user's instructions or existing owner decisions.
