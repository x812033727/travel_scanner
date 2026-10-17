# A01 round 12 driver: independent code review, revision 4

Date: 2026-10-17. This review compares the fourth local candidate with the revision-3 finding. It is not an A01 production run, narrative PASS, script-review receipt, or media approval.

## Frozen bytes

| File | SHA-256 |
| --- | --- |
| `review-round12-104.mjs` | `f0712d5bc5722cc6b6d0f7c220e815e8ed280b3a70805dafa5fa51fb976db363` |
| `review-round12-core.mjs` | `07b9a216da6753e77e8624a3bd30d3ece5e85cdca2831683643c5192554acdeb` |
| `inspect-review-progress.mjs` | `3d4fa7a891244a7e0c0ca620fb6a01d9e967b4fc3b4c6c8cee3cf0e156b3415d` |
| `review-round12-core.test.mjs` | `e8daae93acb0c2018646e528e0e30cb9bfc4e29cee37e0972f5e84904de6e614` |
| `review-round12-donor.test.mjs` | `f9278fd12adae78964eabd7201d873dc88b276368f4fad39441664f19a44a8ef` |
| `review-round12-preflight.test.mjs` | `b878506ac79b808ed82c7e3c07bb48342a054a695f801c3398784932605f3f12` |

The author summary is `round12-driver-local-review.md` SHA-256 `da70b86d0a5f1a8656b41cffe9e6336e4e3924e129150a186553586a99ff0b67`.

## Verdict

**Revision-3 canonical LEASE finding is fixed.** The `--preflight` branch now returns at lines 136–140 before `acquireProjectLease` at line 142. It cannot create, release, or take over A01's canonical `LEASE` through this path. Each production phase acquires the lease before its own fresh source capture and inspector pass (lines 141–149); it verifies the lease and current source again before lifting STOP (lines 175–177). I found no new driver code blocker in this revised path.

**`--preflight` remains a scoped temporary host write, not a strictly read-only operation.** It creates `/tmp/a01-round12-preflight-*` and copies source/audit bytes there (lines 120–124). These captures are retained by this code rather than deleted at exit. The direct snapshot currently measures 254 files, 7.18 MiB; future sizes can differ. A host caller must classify and authorize the temporary write, keep the directory private, and check free space. Any prior approval for read-only host inspection alone does not imply approval for this write.

The exact host STOP recovery guard and phase caller still require independent review, action-time checks, and applicable owner approval. The driver's `round12-restore-stop.pending.json` boolean is an assertion, not proof of installed guard wiring. Production phase execution remains **NO-GO** until that external gate passes.

## Evidence

- Re-read the complete control path around `--preflight`, lease acquisition, recapture, source comparison, and STOP removal. No canonical A01 writes occur in the preflight branch. The phase branch's `inspectCandidate` runs under the held project lease.
- The new preflight test runs a transformed copy of the actual driver branch with a lease mock that would rename an existing `LEASE` and throw if called. It confirms exit 0, original LEASE bytes unchanged, no `LEASE.dead.json`, STOP unchanged, and the explicit `canonical_lease_acquired:false` report. Its inspector/capture imports are stubbed, so it does not independently prove full live capture behavior or the phase branch; the full 104-chain inspector and donor tests cover those pieces separately.
- With the verified `snapshot-104` and exact pinned runtime donor, `node --test review-round12-core.test.mjs review-round12-donor.test.mjs review-round12-preflight.test.mjs` passed **16/16**. The donor success probe reached a synthetic 108-link `pilot_script_review` state with no media; pending and uncertain probes retained one request key or held the previous source and restored STOP, as applicable.
- The unchanged source inspector was separately rerun against the local direct snapshot and returned `ACTUAL_REVIEW_PROGRESS_CHAIN_PASS`, 104 links, tip `e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7`. This does not replace a fresh action-time production readback.

No production or provider call was made in this review.
