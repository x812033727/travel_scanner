# A01 104 → 105 guarded adoption core — OFFLINE HOLD

This directory is a reviewable transaction library and synthetic test suite. It
has **no production CLI, SSH call, Docker call, database client, provider call,
or host release wrapper**. Do not copy the old 25-public-source r23 proposal
onto the host. A01 is already imported; these nine source files would revise
the existing episode after the owner separately authorizes their exact paths.

## Inputs and checks

`verify-fresh-104.mjs` calls the fixed sibling
`../a01-capture/verify-archive.mjs`, then checks the complete 104-event chain
and current source tuple in a private extraction of the hash-pinned archive.
It issues a create-only receipt with `status: PASS`,
`verification_scope: ARCHIVE_MEMBERSHIP_AND_IMMUTABLE_104_ONLY` and
`production_adoption_allowed: false`. An unrelated queued media job can leave
the capture operationally on HOLD while this **source-only** verification
passes. The capture helper currently lives on a separate branch; until it is
independently reviewed and integrated at that fixed path, the verifier and
prepare step fail closed. The old `-02` capture lacks the helper's current
runtime/completeness pins and cannot receive this receipt. Use a new complete
capture such as `-03`.

Independent source verification is separate from historical/editorial review.
The r23 manuscript failed the latter on 2026-10-19: two spoken claims exceed
their cited sources, one claim attribution needs correction, and the opening
image prompt fixes an unsupported decade. `prepareAdoption()` and
`applyAdoption()` both reject the pinned r23 manifest in code. A revised r24
must receive new source, editorial and narrative review before these pins and
the readback expectation can be updated. The production transaction also has
an unconditional `R24_EDITORIAL_REVIEW_GATE_NOT_CONFIGURED` stop until a future
reviewed receipt binds its manifest and exact nine target hashes. Synthetic
fault tests alone bypass that stop through a test-runner-only pin override.
Source-only PASS cannot unlock r23 or an arbitrary changed manifest SHA.

`prepareAdoption()` takes a safe-extracted **fresh** 104-event capture, the
pinned r23 editorial inputs, the actual deployed worker checkout, and that
source-only receipt. It **recomputes** the archive, full chain and receipt
before using it. It requires the independently verified
104 source (`e1499cd6…`), tip index (`f2628d89…`), and 222-file audit
inventory (`0e51a4fa…`) to match. It regenerates six chapters from r23 scene
and claim rows, replacing all six old section titles and stale chapter hook
loops with the reviewed 11 r23 setup/payoff pairs. It resets each claim to
`UNCHECKED` and calls the pinned
`composeStory()` to regenerate the filtered public `video.json`. It rejects
any difference from the complete reviewed r23 `video.json`, including the
18 ordered public URLs, `[7,8]`, thumbnail and `source_guide`. The internal
series retains 25 research sources and scalar `target_minutes: 10`.
The r23 editorial manifest is pinned to SHA-256 `a5978f83…`, and all ten
listed outputs must match an exact relative path allowlist and manifest hash.

The local checkout HEAD, clean `tools/video` tree, host-reported tree SHA,
full container `tools/video` file inventory SHA/count, worker image ID, and
worker `story.mjs` SHA must agree. The inventory sorts relative POSIX paths
and hashes each UTF-8 relative path, one NUL byte, the lowercase file SHA-256,
then one LF byte, concatenated across every regular file. It rejects symlinks
and special files. The currently deployed release lacks the final A01 duration
and public-source filter. No real plan can be prepared by pretending a future
checkout is the deployed worker. A generated plan is data, not permission.

`applyAdoption()` is available only to a future reviewed **host wrapper** that
passes all of these held, verifiable handles:

- exact owner grant for the plan hash and every derived write path (including
  temporary sidecars, both intent/backup copies, audit, receipt and LEASE);
- root-owned release hold and **all four** release locks, verified by the
  wrapper on every probe/write; an unrelated hold is a refusal;
- global video-work `STOP` owned by the wrapper as the queue fence, plus the
  pre-existing A01 scoped `STOP`, byte-identical throughout;
- a durable, self-owned A01 database admission fence whose token is read back
  from the A01 budget row. The API must reject **all** A01 vendor reservations
  and text-stage dispatch under that same row lock while the fence is held;
- live DB, budget, media, journal, deployed runtime and host-state probe
  repeated before each canonical replace. All global stage/media jobs must
  have drained, and A01's USD 25 ledger must still be unspent and unreserved.

Current global STOP is cooperative: direct API media jobs and subscription
text-stage dispatch can still enter. The required A01 database admission
fence does **not** exist yet. Thus this library currently has no valid
production caller. A future wrapper must prove the DB flag and row-lock
checks, acquire the A01 LEASE and perform all nine writes in one video-worker
process, hold all four release locks and its own release hold, and read back
the live drain state. It must retain the admission fence, STOP and hold after
any failure. This directory does **not** provide that wrapper; a callback
that merely returns `true` is insufficient evidence for real execution.

## Durable write order and recovery

1. Create and verify A01 `LEASE` with exclusive create; any existing lease or
   lease sidecar is refused, including a stale one. The transaction never
   renames an old lease or creates a `LEASE.*.dead.json` sidecar. Keep A01 and
   global STOP in place.
2. Create the same durable intent on docs and work mounts.
3. Back up the **original nine bytes twice**, one copy on each mount. Each
   create uses `wx`, file fsync and Linux directory fsync.
   Journals live at each mount's `.a01-adoption/<slug>/<event-id>/`, outside
   the captured A01 source subtree; the independent 105 verifier therefore
   sees only the nine canonical replacements, new event and receipt.
4. Recheck live gates and source tuple. Atomically replace only six chapters,
   `series.json`, filtered `video.json`, and `auto.json` with same-directory
   temporary files and directory fsync.
5. Create manual amendment, then installation receipt, then publish the new
   immutable 105 `index.json` **last** through a same-directory fsynced temp
   and atomic rename. The index binds the receipt SHA, old
   index SHA and before/after tuples. Amendment and receipt both bind the
   exact plan SHA, owner grant SHA and approval reference. The plan has no
   index SHA field: it is computed after the grant to avoid a hash cycle.
   Read back; return HOLD.

Any failure leaves STOP and intent/backups. `inspectRecovery()` is read-only:
it distinguishes unchanged, partial known, unknown drift and complete-index
states. `recoverBefore()` is a separate explicitly granted, fenced operation
that restores exact old bytes **only before an index exists**, keeps both
intents/backups and STOP, and writes a recovery receipt. It never blindly
retries the forward install. Once index exists, only independent readback may
decide whether 105 is valid. No script-review receipt is issued by adoption.

The separate `tools/video/a01-readback` verifier consumes a separately
approved expectation with nine target hashes, both source tuples, immutable
104 inventory, 105 event/receipt hashes and the ordered public 18 URLs. The
installer's own plan or return value is not an independent verdict.
`draftReadbackExpectation(plan, before, grant)` emits the exact hash and
authorization fields with a deliberately incompatible `..._draft` kind; an independent reviewer must approve the
bytes and issue the verifier's `a01_r23_105_readback_expectation` separately.

## Local verification

```bash
node tools/video/a01-adoption/verify-fresh-104.mjs --capture ABS_FRESH_CAPTURE_DIR --out ABS_NEW_RECEIPT.json
node --check tools/video/a01-adoption/prepare.mjs
node --check tools/video/a01-adoption/transaction.mjs
node --test tools/video/a01-adoption/*.test.mjs
```

Windows cannot fsync directory handles; synthetic tests skip that OS-specific
operation. On the Linux host, every new directory entry and rename requires
directory fsync. All tests use disposable OS Temp trees and synthetic grants,
locks, STOP files, receipts and failure injection; they neither touch the host
nor authorize A01 paid work. The production status remains **HOLD**.
