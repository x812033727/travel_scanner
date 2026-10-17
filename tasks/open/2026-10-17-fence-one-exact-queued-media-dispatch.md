---
id: 2026-10-17-fence-one-exact-queued-media-dispatch
title: Fence one exact queued media dispatch for A01 host drain
status: in-progress
priority: P1
area: api
owner: codex-gpt6-a01-media-fence
claimed_at: 2026-10-17T15:43:49Z
created_at: 2026-10-17T15:43:40Z
completed_at:
branch: codex/a01-exact-media-dispatch-fence-20261017
depends_on: []
scope:
  - apps/api/app/video_media/jobs.py
  - apps/api/app/video_media/admin_api.py
  - apps/api/app/video_media/cutover_intake.py
  - apps/api/app/video_media/dispatch_fence.py
  - apps/api/app/video_media/dispatch_fence_cli.py
  - apps/api/app/video_media/dispatch_fence_cutover.py
  - apps/api/tests/test_video_media_jobs.py
  - apps/api/tests/test_video_media_api.py
  - apps/api/tests/test_video_media_cutover_intake.py
  - apps/api/tests/test_video_media_dispatch_fence.py
  - docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-media-dispatch-fence-20261017
  - tasks/open/2026-10-17-fence-one-exact-queued-media-dispatch.md
---

# Fence one exact queued media dispatch for A01 host drain

## Why

An unrelated historical image job remains queued on the production media API. Its ID is
`b721a65d-8c8d-4ae8-834c-391cfc267a6f`, slug
`google-project-suncatcher-prototype-what-it-tests`, request hash
`52b39c04a45f39b4101bcd7e401c31cd0e6083f3c8390b729afd2a83569379e6`,
kind `image`, provider `minimax`, model `image-01`. At the 2026-10-17 15:45:32Z
read-only snapshot it was `queued`, attempts 1, polls 0, with no vendor reference or
submission time. The existing GET and repeated POST paths can advance such a row and
call the provider. A01 needs a host-drain proof without changing, retrying or paying
for this unrelated job. A queued row alone does not prove that no old API provider
call is currently in flight or that there was never a historical charge.

## Definition of done

- [x] New API code refuses every dispatch path for this compiled exact ID even when
  the on-volume marker is absent, malformed or mismatched, leaving its DB row intact.
- [x] Valid exact marker returns an inspectable read-only CLI receipt with row identity,
  active-media count, Redis lock state, marker SHA and source hashes. Other IDs retain
  their existing behavior.
- [x] Local tests cover GET, repeated POST, direct advance, malformed/missing marker,
  non-target job and the Redis nonce helper without a vendor call.
- [x] Proposed new API refuses direct B25 image/clip/music POST, live-job GET,
  judge and locate before quota, budget or vendor work; the read-only receipt
  pins the API route source hash. This does not fence the deployed old API.
- [ ] Independently review the bounded old-API stop, durable Redis hold, marker
  installation, deploy and held-mode CLI plus exact nonce-owner receipt; obtain site-owner approval
  before any production write or transient API outage.
- [ ] On the exact production image and volume, verify the new API receipt and A01
  drain guard before claiming A01 may continue. No A01 vendor work is part of this task.

## Steps

- [x] Verify #1508 merged and its task is ownerless; check active board and PR scopes.
- [x] Add incident-specific API fence, strict marker parser, read-only CLI and tests.
- [x] Prepare a no-clobber marker candidate/installer and Redis cutover helper.
- [ ] Finish independent review, CI, PR and owner-approved production cutover.
- [ ] Read back exact production row, container/image, marker, Redis lock and guard
  receipt after deploy; only then decide whether A01 production can resume.

## How to verify

Locally, from `apps/api`: `uv run pytest tests/test_video_media_cutover_intake.py
tests/test_video_media_dispatch_fence.py tests/test_video_media_jobs.py
tests/test_video_media_api.py -q`, plus Ruff and Mypy.
Run `bash -n` on the two shell helpers and inspect `manifest.json` SHA-256. Production
commands and strict stop conditions are in the task's `README.md`; its held-mode CLI
`check --expect-operator-lock` must return `enforced=true`, `media_lock_absent=false`,
`active_media_count=1` and the exact pinned tuple from the exact deployed API
container, paired with a fresh private exact-nonce/TTL and supervised watcher
receipt. A dry run, green CI or a marker file by itself is not the done receipt.

## Notes

PR #1508 was verified merged at `42fbfb40d`; its older task was already ownerless
and still open for live readback, so no claim was removed or task closed. The
incident fence deliberately does not mark the row failed, clear the old record,
call MiniMax, modify A01 or re-enable dispatch. Removing the marker cannot
re-enable this compiled ID. A separately reviewed code change and owner decision
are required to remove the fence. Production cutover is blocked until the graceful
old-API stop, site-owner approval and independent runbook review are satisfied.

The isolated single-host cutover driver and patched stock-deploy guard are now
prepared in the task's documentation directory. Two independent reviews found
and then rechecked the under-lock preflight, effective API/worker Redis DB0
identity, and helper readability before the old API stops. Linux driver tests
passed 19/19 and deploy-guard tests 5/5; the final README describes one
continuous hold and `--no-rollback`. These are local candidate checks, not
production receipts. The driver's `--apply` path still stops at
`b25_producer_proof_missing` before any host write until the unrelated B25
producer is authoritatively completed or durably paused. No installation,
deployment, API stop, nonce, marker, A01 paid stage or vendor call occurred.

Independent read-only producer audit on 2026-10-18 found no safe snapshot-only
condition that can remove this hard STOP. B25 is made by `video-worker`, while
the cutover candidate pins only `video-ai-worker`; B25's producer can release
and reacquire its project LEASE between image units. A moment with no LEASE,
queued DB row or media process, or an `auto.json` done/blocked value, cannot
prove it will not send again. The four deployment locks do not fence that
producer. Before any proposed apply, a separately reviewed, durable B25
producer pause or terminal mechanism must be established with its own host
authorization, then rechecked under the release locks and throughout deploy
and A01 handoff alongside actual `video-worker` identity, work volume,
pending media jobs and ledger state. Do not clear or rewrite B25 records to
manufacture quiescence; retain `b25_producer_proof_missing` until the contract
exists.

The isolated B25 producer-pause helper in
`A01-media-dispatch-fence-20261017/` is now a **LOCAL HOLD candidate only**.
It checks the original video-worker/project identity, requests a per-project
STOP under the original LEASE without clearing jobs or the ledger, and repeats
the four-lock verification without creating absent lock files. Independent
review caught and then verified fixes for the real `{runs:[]}` state-journal
shape and a formerly write-capable `--verify`; disposable Linux tests pass
12/12. The host candidate explicitly returns `production_ready=false` because
a project STOP does not fence direct media API clients. It is not imported by
the cutover driver, installed, approved for a host write or a reason to lift
`b25_producer_proof_missing`. The separate direct-intake and full-window
cutover proof remains open.

On 2026-10-18, `admin_api.py` had no active task or open PR touching it under
the task-board scope audit, so this ticket's scope was extended to that exact
file. The proposed new API now compiles a B25 slug refusal in `jobs.py` and
applies it before direct `/judge` and `/locate` booking in `admin_api.py`.
Focused tests verify all five POST routes plus live GET and direct job calls
without a quota, database write, Redis reservation or vendor call. The CLI
reports the B25 guard and `admin_api.py` hash; the driver requires both pins.
This is a local, unmerged candidate. The old API can still take direct B25
requests before graceful exit; keep the driver's hard STOP until the B25
worker pause and complete old/new API transition have independent proof.

The follow-up local candidate adds a global, all-slug API paid-media gate on
the existing read-only `video_work` mount. A bootstrap marker is required even
before the first gate-aware deployment; absent/invalid files fail closed.
Installing the separate durable `armed.json` first immediately invalidates
`BOOTSTRAP_ALLOW`, and `PAUSED_ALL` rejects media POSTs, judge/locate and live
GET advancement. `ALLOW_A01_ONLY` checks the exact A01 slug plus the durable
Suncatcher Redis nonce hash and TTL. Route tests cover the 423 code before
quota/context; active GET now checks before its poll quota. The read-only CLI
and target source list include `cutover_intake.py`. The stock deploy does not
bind `RELEASE_SHA` to Git HEAD, so the marker cannot on its own prove a running
API binary is the target. The root-only transition, initial bootstrap marker
installer, old/new live ingress checks and repeated image/source proof are
still missing. Do not deploy or use `ALLOW_A01_ONLY` from this candidate;
`b25_producer_proof_missing` remains an unconditional apply STOP.
