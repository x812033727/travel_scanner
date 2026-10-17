# A01 round 12 independent code review — 2026-10-17

**Decision: do not run `review-round12-104.mjs --run` on production yet.** This is an independent, adversarial review of the frozen candidate, based on the actual 104-link A01 snapshot. No production write, model request, media request, merge or deployment was made in this review.

## Reviewed bytes and evidence

| File | SHA-256 |
| --- | --- |
| `review-round12-104.mjs` | `d9738b0a2388bd8c48999020a68504455cb328d026fb2b39262b34c530c7bd5e` |
| `review-round12-core.mjs` | `b1166c6195c0bd663373081efeece632e5122bf296c106373165d74ce5a89759` |
| `inspect-review-progress.mjs` | `7c03874cbe33a0f309cde243bcc63d25c1abe4cf4960c240f5ec1c5145dca231` |
| `review-round12-core.test.mjs` | `468d0bdc7233a66f318e5cd8484246660334da98d89dd4b125c902264d1f8735` |

The read-only `verify-progress104.mjs` returned `ACTUAL_REVIEW_PROGRESS_CHAIN_PASS`, 104 links, source SHA `e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7`. Snapshot `auto.json` has `status=blocked`, `blocked_kind=prompt_fixes:narrative`, `narrative.rounds=11`, and no approved pilot script receipt. I inspected the actual `turn.json`, installed `story.mjs`, `flow.mjs`, and `project-lease.mjs` paths used by the driver.

## Findings

### P1 — Verifier allows duplicate claim IDs and silently loses another claim

`review-round12-104.mjs:137-140` checks the response claim count and that each row matches *some* existing ID. It does not require each existing ID exactly once. Against the actual 104-link chapter, a response replacing the last row `t13` with a duplicate `t1` passes this guard; I ran that adversarial predicate and got `guard_accepts_duplicate=true`. Installed `story.mjs:653-667` then renumbers the duplicate, so the saved claims can lose `t13` and gain a new ID even though the driver intends to allow only verdict and note updates. This changes the fact record outside the reviewed `t19` retirement.

Require the response ID sequence to equal the current ID sequence exactly, rejecting duplicates, omissions and reordering; compare every persisted claim's `id/claim/scene/source/fact` after the verifier. Test a duplicate ID with one omitted ID using actual snapshot 104.

### P1 — Scope validation runs after audit success and journal settlement

The listener, chapter verifier and panel each call `commitModelEvent` before checking unchanged source fields (`review-round12-104.mjs:161-163`, `191-193`, `204-205`). `commitModelEvent` writes the saved audit event and committed receipt, adopts the model run, and settles its journal (`:60-77`). If an unexpected series, lexicon, pilot receipt, other chapter, or narrative field changes, the process reports the scope failure only **after** it records the step as saved and clears the journal. The reader at `inspect-review-progress.mjs:47-56` checks round-12 stage order but does not independently enforce each event's allowed field changes.

Validate the complete before/after tuple and exact allowed changes before adoption, audit write or settlement. Mirror those restrictions in the read-only chain inspector, including partial chains after step one, two or three. Keep an unexpected result pending for investigation instead of recording it as a successful reviewed edge.

### P1 — A forced stop can leave the A01 STOP file absent

`review-round12-104.mjs:149` removes the persistent project `STOP`; restoration is only in its JS `finally` and SIGTERM/SIGINT handlers (`:109-110`, `:209`). SIGKILL, a container restart, or a host crash bypasses both. The project lease deliberately permits takeover of a certainly dead holder (`project-lease.mjs:82-116`), so it does not preserve the hold after a crash.

**Risk boundary:** A01's current `status=blocked` means the ordinary auto loop skips it (`flow.mjs:1436-1465`), and the missing pilot script receipt still blocks the normal media path. Thus STOP loss alone does not prove immediate paid media. But `flow.mjs:1532-1537`, `1584-1610` can accept a site `retry_request_id` when STOP is absent and make a blocked video active. A deployment hold does not participate in this check. A persistent external recovery guard must recreate STOP after a killed container and before the video worker can process a retry after host reboot; alternatively keep the video worker stopped until recovery. Verify this with a simulated killed child and reboot/start ordering before running on production. A host shell `trap` alone covers normal exit and child death, not host reboot.

### P2 — A completed partial phase cannot resume with this driver

`review-round12-104.mjs:114-119` insists on exactly 104 links and the round-11 state. After one legitimate listener event, the chain has 105 links; after manual amendment or verifier it has 106 or 107. Reinvoking this same driver then refuses at preflight, even if the last event is valid and no journal is pending. This is safe against blind duplicate calls, but a normal interruption leaves A01 requiring a new phase-specific recovery driver and review. Add phase-specific, source-pinned resume with exact event/tuple checks, or explicitly execute and inspect one phase per invocation.

### P2 — Manual audit does not prove derived story files came from the exact amendment

`inspect-review-progress.mjs:14-33` verifies the exact `turn.json` and `auto.json` manual changes, but does not verify `video.json`, `claims.md` or `script.md` content or allowed deltas. The event index hashes these files and the chain connects the hashes, yet a rehashed unexpected derivative edit would still satisfy the manual scope check. Recompute or structurally verify the merged scene list, claims table and screenplay from the six chapter files, and test a rehashed tampered derivative, not only a changed file with a stale hash. The runtime currently calls installed `relint`, which reduces ordinary execution risk, but the independent audit is weaker than its stated scope.

### P2 — Listener response guard accepts nonempty `edits`

`review-round12-core.mjs:20-25` accepts any array in `answer.edits`. Installed `story.mjs:1357-1364` ignores this field, and the saved chapter comparison prevents its instructions from landing, but it weakens the intended exact response contract. Accept only absent or empty `edits` and add a test with one nonempty edit.

## Checks and positive boundaries

- `node --check` passed for all three reviewed `.mjs` implementation files.
- With `A01_SNAPSHOT104_ROOT` set to the actual verified snapshot, `node --test review-round12-core.test.mjs` passed **8/8**. It tests the target line, exact listener cut, `t19` retirement, a manual audit tamper with stale hashes, pending same-source polling, STOP restoration on an ordinary thrown error, and a lint probe.
- The adversarial duplicate-ID probe above demonstrated an untested accepted response; the existing 8 tests do not cover it.
- The driver itself calls only `advanceStory(..., 'verified')` and `advanceStory(..., 'script passes lint')`; it does not call `flow.media`, TTS, upload, or foreign-language stages. The missing pilot receipt is a downstream gate. I found no path that labels a pending/uncertain model result successful: `commitModelEvent` requires one adopted journal with a `succeeded` receipt, while `RUN_PENDING` polls the same source and a failure exits without settling. The preflight's runtime hashes cover installed `story.mjs`, `flow.mjs` and `lexicon-store.mjs`.
- Budget, paid-job quiet state, host deployment locks/hold, site retry status, and the A01 STOP file must be verified again by the host wrapper immediately before any production run; this driver does not enforce the US$25 ledger itself.

This report approves neither the current production run nor an A01 script-review PASS. After code and host recovery fixes, rehash the new candidate, repeat independent review, and rerun the actual 104-link preflight.
