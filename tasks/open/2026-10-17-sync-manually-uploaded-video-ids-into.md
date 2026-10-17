---
id: 2026-10-17-sync-manually-uploaded-video-ids-into
title: Sync manually uploaded video IDs into local projects
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-17T00:31:27Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/youtube
---

# Sync manually uploaded video IDs into local projects

## Why

Manually produced episodes can be approved and uploaded through `/admin/videos`, while
their local `video.json` and `state.json` still say they are not on YouTube. On
2026-10-17, authenticated review readback showed private YouTube IDs for H11 and
U09, but both local projects had blank IDs. `review-pull` only copies approval
decisions; `auto` reconciles IDs only for projects with `auto.json`. The advertised
`node tools/video/cli.mjs youtube-sync` delegates to `tools/video/youtube/cli.mjs`,
which does not exist in this checkout and exits with the missing-tool code.

## Definition of done

- [ ] A manually produced video's current YouTube ID and sync state can be read
  from the authenticated site record and reconciled locally without another upload.
- [ ] Reconciliation checks the exact slug and approved package identity, preserves
  script/final approval hashes, and refuses missing or contradictory site records.
- [ ] The command never treats a site `dub=uploaded` attestation as proof that an
  alternate audio track plays in Studio.
- [ ] A repeat run is idempotent and tests cover stale local state and mismatched IDs.

## Steps

- [ ] Inspect `review-pull`, `auto` ID recording, local state schemas, and the
  `youtube-sync` CLI stub before choosing the narrowest implementation.
- [ ] Implement the readback/reconciliation command under `tools/video/youtube`.
- [ ] Add focused tests with mock site responses; document manual-video usage.

## How to verify

Run the focused tool tests and `npm run test:tools`. Against an authorized
manual episode, compare the site's slug/ID with local state before and after a
dry run and one reconciliation; verify a second reconciliation changes nothing.

## Notes

H11 and U09 were private and unscheduled at readback. Do not put their live
video IDs or account credentials into the public repository or test fixtures.
Studio audio tracks cannot be independently verified through the current Data
API route.
