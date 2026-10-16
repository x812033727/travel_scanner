# A01 81st lexicon audit: host adapter HOLD

**Decision (2026-10-16): do not build or run a production append command yet.** The
80→81 proposal and transaction fixture can validate exact bytes, but the current
production writers do not share a lock that would make the live source, audit tip,
and new event atomic. A new adapter that checked files, took its own lock, and
renamed the two directories would present a false safety guarantee. This folder
contains the missing coordination contract and acceptance criteria; it contains
no SSH, host-write, paid, retry, deployment, or installer program.

## What the existing controls actually fence

| Control | Current behavior | Limit for this append |
| --- | --- | --- |
| A01 `STOP` and global work-base `STOP` | `tools/video/core/paths.mjs:85-88` only tests file existence. `tools/video/automation/cli.mjs:135-178` stops the automatic loop between units; `apps/api/app/video_automation/ai.py:253-260` checks before a queued model request. | Cooperative pause, not an exclusive lock. An already active unit or a direct host writer can outlive the check. The 06:26 UTC host readback documented in `../A01-live-readback-20261016.md` found neither STOP; it is historical, not a current preflight. Creating/removing STOP on production is a separate owner-authorized write. |
| A01 `LEASE` | `tools/video/core/project-lease.mjs:99-158` uses exclusive creation and process identity. `tools/video/automation/flow.mjs:1438-1460` takes it for the A01 worker unit, and media/TTS commands use it before their own writes. | Per video, not a lock on `docs/videos/lexicon.json`. An absent `LEASE` is only a momentary observation. The host command would need to acquire and verify the *same* lease in the `video-worker` container, never a `docker compose run` container (see `docs/videos/AUTOMATION.md:79`); this still would not cover all source or audit writers. |
| Shared lexicon | `tools/video/automation/flow.mjs:401-412` reads, merges, and atomically writes the worker-owned shared lexicon. `saveAndLint()` calls it after the caller's per-slug `fence` at `flow.mjs:2916-2925`. | A different video's valid `LEASE` and unit can change A01's source composite while A01 holds its own lease. There is no shared lexicon mutex or per-story frozen lexicon in this path. The open immutable-binding task is `tasks/open/2026-10-16-bind-story-audits-and-narration-to.md`. |
| Audit event / manual receipt | The `../A01-lexicon-apply-candidate/apply-fixture.mjs` transaction lock is a private `story/lexicon-rebaseline-transactions/<event-id>` directory under a marked OS Temp fixture; it is not used by other writers. The older `../A01-round11-offline-install/installer.mjs:303-342` writes a differently shaped audit file with `wx`, also only in a fixture. | No current production `recheck-audit` writer was found in `tools/video`, `ops`, or `apps/api`, and no common audit lock contract is declared for manual host corrections. This does **not** prove there are no external host scripts or operators. A lock invented by the new adapter would not be respected by them. |
| Worker mount | `docker-compose.prod.yml:256-314` mounts `video_work` read-only into `video-ai-worker` and writable into `video-worker`; `video_docs` is writable in `video-worker`. `ops/video/README.md:17-22` says the shared lexicon is worker-owned. | The API-side worker cannot normally append an audit file through its mount, but the video worker and host-level maintenance can. Mount layout alone gives no exclusive writer window. |

The offline fixture's `safety` object and reviewer/approval strings are supplied
by its caller. Its independent review explicitly states that those values do not
authenticate host state, a reviewer, or an owner. The saved 06:24 UTC source
capture is historical. It found no real A01 independent review or record-only
receipt, and the 80-link source tip was already behind the mounted lexicon.

## Could a short maintenance window close this race?

**Conditionally for worker-origin writes, yes; currently not as a proven live
guarantee.** In this Compose file only `video-worker` mounts both `video_docs`
and `video_work` writable; the API and `video-ai-worker` have `video_work:ro`
(`docker-compose.prod.yml:72,271,312-314`). An owner-approved window that
creates global and A01 STOP, allows in-flight work to finish, gracefully drains
the sole `video-ai-worker`, stops the sole `video-worker`, verifies both remain
stopped and no paid call or queued/running job, A01 lease, or run receipt remains
unresolved, and then keeps the deployment/autodeploy lock through append and
readback would exclude the known automatic writers. The stage worker must be
drained with a reviewed warm-drain procedure: checking `running=0` and then
stopping it has already proved racy during deployment. The host lock must also
prevent an automatic container recreation throughout the window; a point-in-time
`docker ps` check cannot do that.

This still depends on an **operator-wide exclusion** for direct host or manual
container writers. The repository has no shared lock that every manual audit
writer honors. A host `flock` only blocks callers that take that very lock;
`STOP`, zero jobs and a missing `LEASE` cannot prove that an external root
session will not write a moment later. The present evidence does not establish
an exclusive operator window, a review of all manual writer paths, or authority
to place STOP files and stop services. Therefore this is a possible controlled
maintenance design, **not** a ready adapter or an authorization to use it.

A per-story immutable lexicon is the durable fix for unrelated-video drift:
make A01 narration and audit hashes read its frozen snapshot, keep the old
80-event shared-file binding verifiable, and bridge the observed change with
one explicit audited migration event. This removes the need to pause all other
videos whenever their shared lexicon grows. It does **not** by itself serialize
manual `recheck-audit` appends or authenticate human approval, so the audit
writer protocol and readback requirements still apply.

## Missing contract before a host adapter can be reviewed

1. **One writer protocol:** enumerate every production path that can mutate
   A01 docs, its work directory, `story/recheck-audit`, manual receipts, and the
   shared lexicon. Make each path honor the same exclusive mutation protocol,
   including manual host correction tools. A01 `LEASE` alone is insufficient:
   lexicon writers for every slug need a shared fence or A01 must read an
   immutable per-story lexicon. Document how a host administrator enforces a
   single maintenance window for external writers.
2. **Drain before a lock-bound snapshot:** after separately authorized STOP
   creation, wait for existing worker units and durable jobs to finish or enter
   a resolved state. Capture an immutable, complete 80-event source and audit
   snapshot; independently pin its tar hash, every old index, original tip,
   install receipt, source map, release and mounted worker/rules bytes. Re-read
   project retry, stage/media jobs, budget, unfinished run receipts, media,
   STOP, and lease under the same coordination window. A check for zero running
   jobs before acquiring the lock does not close a later enqueue race.
3. **Real human evidence:** obtain an independent review of the exact proposed
   source delta and raw `independent-review.json` bytes, then bind a genuine
   owner approval to the exact *two* record-only paths and STOP maintenance
   action. A syntactically valid `reviewer` or `owner_approval_ref` field is not
   authentication. Recompute the plan and four output-file hashes from the
   fresh capture; reject any additional lexicon or history drift.
4. **Two-mount durable transaction:** adapt the fixture only after the lock
   contract exists. Its docs source is under `/opt/mokaair/docs/videos`; its
   event and receipt are under `/var/lib/mokaair/video-work`. Stage both new
   directories on the **work** volume, flush files and parent directories,
   publish the receipt first and audit directory last, then recheck all source
   and historical pins while the coordinated lock still holds. Publish a
   separately reviewed 81-link read-only inspector; the old inspector is
   intentionally pinned to 80 and must continue to reject 81.
5. **Crash reconciliation:** retain a durable intent. No automatic retry or
   deletion after receipt-only publication. A post-crash full publication may
   be recognized only after exact 81-link and external-evidence readback; a
   partial state or changed file requires a new reviewed recovery decision.
   An ordinary exception may remove only exact new bytes; it must never
   rewrite the original 80 events or shared lexicon.

## Acceptance tests required for any later implementation

- Hold A01's real project lease in one process and prove an adapter waits or
  refuses; also prove a second A01 producer cannot enter between the adapter's
  last precommit check and readback.
- Run a different slug's `mergeLexicon()` during the attempted append and prove
  the adapter either excludes it through a *shared* mechanism or refuses
  without publishing the audit tip. Test a manual audit writer with the same
  protocol, rather than only two copies of the proposed adapter.
- Change STOP contents, source bytes, one historical index, reviewer bytes,
  receipt bytes, approval binding, a DB job/retry, and one budget operation at
  each relevant boundary; every case must refuse before a valid 81st tip.
- Inject process death after intent, after receipt rename, and after audit
  rename. Prove exact readback, refusal of partial retry, and no double append.
  The before and after capture roots must be distinct and immutable.
- Verify that no branch from this adapter calls a provider, clears STOP/LEASE,
  retries A01, installs the script review, or enables B18/five-film work.

The existing fixture's synthetic 80→81 tests are useful for byte mechanics;
they do not exercise a production writer or establish this missing lock.
Until the coordination contract, live evidence and separate narrow owner
authorization exist, the operational result is **HOLD**.
