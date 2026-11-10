---
id: 2026-10-16-deploy-can-interrupt-a-video-media
title: Deploy can interrupt a video media vendor call
status: in-progress
priority: P1
area: ops
owner: codex-media-deploy-barrier
claimed_at: 2026-10-16T08:25:15Z
created_at: 2026-10-16T08:25:06Z
completed_at:
branch: codex/video-media-deploy-barrier
depends_on: []
scope:
  - ops/release/video_media_drain.sh
  - ops/release/video_media_host_patch.py
  - ops/release/test_video_media_drain.py
  - ops/release/video-media-drain.md
---

# Deploy can interrupt a video media vendor call

## Why

The API commits a `video_media_jobs.status=queued` row before making a vendor
submission in the same HTTP request. A predeploy count of `queued` jobs is not
proof that no paid call is in flight: the row stays queued while `provider.submit`
runs. The Redis per-job lock lasts 240 seconds, while a configured submit/fetch
can wait up to 280 seconds. The 2026-10-16 production readback reported one
queued media row before and after the #1521 deployment; its exact operation
must be diagnosed, never erased or automatically resent to clear this gate.

#1527 guards the separate RQ video AI stage worker. It does not drain API
requests or the shell/Node `video-worker` which Compose also recreates.

## Definition of done

- [x] The normal and rollback host deployment paths refuse a media vendor call
      that is queued, or wait for an already accepted API request to finish,
      before replacing the API container.
- [x] A guard refusal before API shutdown leaves the API serving; an uncertain
      postshutdown result retains a marker and requires manual reconciliation.
- [ ] An incremental, pinned host-only install is independently reviewed and
      requires separate owner approval; no production script is changed here.
- [x] The independent `video-worker` paid-unit termination risk is recorded as
      an overall deployment HOLD in a separate precise ticket.

## Steps

- [x] Verify the actual API command/version and Uvicorn graceful shutdown
      default; inspect both compose replacement points and #1527 dependency.
- [x] Add an API media drain helper with a zero-queued precheck, indefinite
      graceful stop, command/version/exit checks, zero-queued postcheck, and a
      crash-persistent pending marker.
- [x] Add an incremental host-script patcher based on #1527's reviewed output;
      reject script drift, install only under deploy flock and pinned hashes.
- [x] Exercise refusal, arrival during drain, interruption, rollback and
      no-queued successful drain with offline fakes; run touched CI checks.

## How to verify

`bash -n ops/release/video_media_drain.sh`; focused
`python -m unittest ops.release.test_video_media_drain -v`; `python -m
unittest ops.release.test_video_stage_drain -v`; Ruff and `npm run
check:tasks`. Before any real install, read back the exact host-only script
hash/mode, API command/version, queued job IDs and worker paid-run receipts.

## Notes

Read-only live API on 2026-10-16: one `travel_scanner-api-1`, entrypoint null,
command `uvicorn app.main:app --host 0.0.0.0 --port 8000`, Uvicorn 0.52.4.
The same live API container used Docker `json-file` logs; a read-only
`docker logs --tail 1` succeeded. No signal was sent to that container.
Its local pinned source uses `timeout_graceful_shutdown=None`: SIGTERM closes
listeners then awaits in-flight tasks. An independent 0.52.4 reproduction
showed Uvicorn re-raises SIGTERM, so a clean container exit is 143. Exit 143
alone is insufficient proof: the guard requires same-container,
post-SIGTERM `Application shutdown complete.` then `Finished server process
[1]` logs. A Docker stop with `--timeout=-1` must not escalate to SIGKILL;
an interrupted stop retains a marker, blocking retry.
The dependency base is #1527 head `cebf987e1e5f253089872b103452557f47f65641`;
this task changes only newly named files and cannot install concurrently with
#1527's host patch. Overall deployment stays held until `video-worker` is
also safely drained and live queued media is reconciled.

Initial independent review found exit-143, log-proof, worker-setting and
new-helper hash gaps; this candidate now handles them. The revised media
suite passes 18/18 and the full release suite passes 40/40 tests.
`npm run check:tasks` validated 1915 task files (pre-existing stale-claim and
scope-overlap warnings); Ruff and `bash -n` passed. The live host script was
read-only copied with SHA-256
`c6e69658cd22351008a179389e807304cb284052136b3aaf1522ffb281a39370`.
The #1527 plus media host-only render passed `bash -n` and has SHA-256
`17a028c3f3f135db14e29bfaba4419b6d025d202613a79b071841dd4f0f94f6f`.
No host install or deployment occurred. Independent code review remains open.

The exact queued production row is `b721a65d-8c8d-4ae8-834c-391cfc267a6f`,
non-pilot `google-project-suncatcher-prototype-what-it-tests`, MiniMax
`image-01` keyframe `h-planet`, queued since 2026-10-12 04:17:49 UTC,
attempts=1/polls=0 and no vendor_ref, idempotency key or receipt. Redis media
lock absent at 08:26 UTC; this does not establish a no-charge result. The
separate task `2026-10-16-reconcile-suncatcher-queued-media-job-before`
tracks its evidence and owner decision. This PR must not clear or resend it.
