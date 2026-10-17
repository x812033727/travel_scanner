# B25 producer pause and quiet proof: local candidate

**Status: LOCAL HOLD.** These files have not been installed or run on the
production host. Their `--apply-stop` mode needs a separate site-owner
approval. Even a successful quiet survey reports `production_ready=false`:
the B25 project `STOP` is read by the existing video-worker, but a direct
client can call the media API without consulting that file. Do not replace
`host-cutover-driver.py`'s `b25_producer_proof_missing` stop with a single
database count or with this candidate alone.

## Exact scope

- Slug: `story-adapt-seiko-quartz-astron` (B25 only).
- Work path inside the **existing** `video-worker` container and its existing
  `travel_scanner_video_work` volume:
  `/var/lib/mokaair/video-work/story-adapt-seiko-quartz-astron/STOP`.
- The host candidate pins that original container's full ID, image digest,
  Compose labels and hostname, UID, `VIDEO_WORKDIR`, writable named volume and
  mount source. It uses `docker exec -i <pinned-id> python3 - ...` as the
  container's default user. It never uses `docker compose run`, starts another
  container or kills a producer.
- The worker helper accepts only `inspect` and `pause`. `pause` verifies the
  slug and story state in `auto.json`, the real `state.json` journal shape
  (`runs`, which has no slug), and all six keyed `story/chapters/*.json`
  files inside the pinned B25 project path. It then creates only `STOP` with
  `O_EXCL|O_NOFOLLOW`, mode 0600, file and directory fsync, exact readback. A
  pre-existing/foreign STOP is not overwritten. There is no clear/delete mode.
- `LEASE`, `media/jobs.json` and `media/ledger.json` are read only. Any LEASE
  remains a hold even if its PID seems stale. Pending jobs or reserved ledger
  entries block quiet proof; the candidate never reconciles or clears them.

The worker may finish an in-flight paid image after STOP arrives; subsequent
media stage sends check STOP. Therefore the first STOP receipt means only
**pause requested**. It is not producer completion, no-charge proof, or an
approval to deploy.

## Action-time sequence, not executed

1. Freshly inspect the original worker and volume and prepare a root-private
   plan with the exact fields validated by `load_plan()`. Pin its SHA-256 and
   the worker helper SHA-256. The current local helper SHA-256 is
   `3808a3a2e0d2196918551edce4fef71c3b23a6d57e6f6c29eb175dddd1a4c042`;
   the host candidate SHA-256 is
   `3fdd45c30c1f7cdc00c11f7f358cfeb022fffdcb6f7903f22bd45cbfb218ff7c`.
   These are review identifiers, not host-readback evidence.
2. After explicit site-owner approval for **B25 pause only**, the candidate
   must hold the four release flocks, find no deployment hold and use the
   pinned original container to create the exact B25 STOP. It returns its
   STOP SHA-256. Any ambiguous result requires read-only inspection of that
   exact path; do not retry `pause` blindly or remove an existing file.
3. Let the original worker finish naturally. Repeated read-only checks must
   find the same STOP SHA-256, no `LEASE`, no pending `media/jobs.json` entry,
   no reserved ledger row, only the pinned old Suncatcher media job in
   `queued` status among active media jobs, and no queued/running stage job.
   The host survey opens **four existing release lock files read-only**,
   takes their flocks without creating files, and makes two samples five
   seconds apart. A missing lock file is a hard STOP. It checks the worker
   source-file hashes are unchanged. It can also compare an exact deploy-hold SHA when
   called during a held cutover. A missing/malformed file or drift is STOP.
4. Before A01 cutover, close the **direct API intake race** by a separately
   reviewed server-side mechanism or an equivalent sequence: the existing
   driver's graceful drain of the **sole** old API, followed by an exact DB and
   in-flight readback before any new API starts, may provide that boundary.
   The current exact-job dispatch fence protects only the old Suncatcher job;
   it does not reject a new B25 media request while the old API is running.
   Re-run the full B25 quiet proof under the driver-held four locks immediately
   before old API drain and after acquiring the continuous hold. Repeat the
   general paid-work, worker, Redis and release preflight. Keep the B25 STOP
   through cutover. Do not disable the `b25_producer_proof_missing` hard stop
   until that integration and direct-client boundary have independent review
   and named owner approval.

The four release flocks do not lock the media API's request path. A database
snapshot can be empty between B25 image jobs, and two snapshots cannot prove
future intake is disabled. If the direct-client gap remains, A01 cutover stays
blocked even if this candidate's worker survey is clean.

## Offline checks

Run only on a disposable Linux environment:

```text
python3 b25-pause-candidate.test.py -v
```

Twelve tests cover exact-path STOP creation, no overwrite, LEASE/pending/reserve
refusals, real stage-journal shape and six-chapter proof, container and volume
pin drift, exact active job, four-lock repeated survey, hold hash and STOP hash,
and read-only `--verify` refusal when a lock is absent. They do not exercise a
production worker, vendor or deployment.
