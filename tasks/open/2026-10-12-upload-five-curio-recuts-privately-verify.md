---
id: 2026-10-12-upload-five-curio-recuts-privately-verify
title: Upload five Curio recuts privately, verify Studio, back up and clear local batch
status: in-progress
priority: P1
area: docs
owner: codex-curio-studio-8bc3
claimed_at: 2026-10-12T16:22:35Z
created_at: 2026-10-12T16:22:26Z
completed_at:
branch: codex/curio-five-recuts-20261012
depends_on: []
scope:
  - docs/videos/curio-five-recuts-20261012
---

# Upload five Curio recuts privately, verify Studio, back up and clear local batch

## Why

Five complete Curio remasters were delivered locally for reupload, but no new
YouTube videos existed when the owner asked to update Studio before deleting
the C: delivery copy. YouTube cannot replace media under the five original
video IDs. The owner explicitly authorized five new **private** uploads and
wants to decide whether and when they become public after language/end-screen
verification. The local batch needs a verified VPS copy before exact-root
cleanup; its existing transfer began before that clarification, but deletion
must remain gated on both Studio and VPS readback.

## Definition of done

- [ ] Five distinct new private YouTube video IDs, each with the exact recut,
      corrected four-language titles/descriptions, four CC tracks, three
      supplemental audio tracks, thumbnail and three clickable elements in
      the final 16 seconds; verify persisted Studio state per video.
- [x] The isolated VPS backup contains all 2,697 manifest-listed files,
      with exact SHA-256 and byte-count verification after extraction.
- [ ] After Studio, backend and VPS verification, preserve the corrected
      staging metadata and remove only
      `<home>/mokaair-work/curio-five-recuts-20261012`, the exact
      hardlink staging directory and temporary archive; retain a receipt and
      independently verify local absence and freed space.
- [ ] Record new IDs, package exceptions, VPS restore instructions, and
      publication/owner-playback status in the delivery docs. Existing original
      video IDs and separate source directories remain intact.
- [ ] Reconcile the five new Studio IDs with the video admin backend through
      separate version records or another supported path, without replacing
      the original projects' YouTube IDs; verify backend readback.

## Steps

- [x] Inventory original and recut IDs, local source hashes, and Studio status.
- [x] Stop the automatic deletion controller before Studio upload; add a
      five-video verification gate to the local cleanup script.
- [x] Obtain action-time permission for Studio's YouTube terms; owner chose
      private uploads and reserved public release.
- [ ] Complete each Studio upload and localized/end-screen readback.
- [ ] Inspect and apply a safe backend linkage for all five new private IDs.
- [x] Finish and independently verify the isolated VPS backup.
- [ ] Recheck source-root identity and safety, delete only the authorized
      local batch, hardlink staging directory and temporary archive, then
      verify absence.
- [ ] Update the draft delivery PR and run affected checks.

## How to verify

For each new ID, read Studio Content/Details/Languages/Editor after upload
processing and confirm private visibility, duration, corrected metadata,
thumbnail, four Published CC tracks, three Published audio tracks, and the
end-screen elements. Verify the VPS backup with its included `backup-verify.py`
against manifest SHA-256
`a71389c4be3bec7c20e3495eb2c8b3750093f568a714bdf217ab9026235565e7`
at `/var/backups/curio-video/20261012-five-recuts/curio-five-recuts-20261012`.
The receipt must show five Studio IDs, 2,697 remote files and local absence.
Run `npm run check:tasks` and `npm run test:docs-videos` for documentation edits.

## Notes

- Original private IDs: H02 `6hswTvAftUA`, U02 `uZ9TlblvrCw`, H03
  `b98IdS1MB78`, L08 `mLxCEB_wSLk` (another same-title private video
  `XSFNRORVuYo` also exists), H01 `efSy-Jxq-s8`. Do not delete/modify them.
- Live VPS Studio uploader is healthy but has no successful actual upload job;
  the five canonical projects already hold original IDs, so that uploader
  route would treat each as an existing video and cannot replace its MP4.
- The owner-confirmed Studio route uses the `upload/` package in the isolated
  local batch. Its `metadata.json` has a few CC-title suffix errors; normalized
  four-language titles are recorded outside the snapshot at
  `<home>/mokaair-work/backup-receipts/curio-five-recuts-20261012-studio-titles.json`.
- Backup transfer PID 33276 ended at 2026-10-12 17:29 UTC. Controller PID 39912
  matched the 3,349,714,868-byte archive and SHA-256, extracted and verified
  all 2,697 files, finalized
  `/var/backups/curio-video/20261012-five-recuts/curio-five-recuts-20261012`,
  and exited at 17:32 UTC **without deletion** because the Studio completion
  receipt was absent. Independent remote, local archive and local snapshot
  readbacks all matched at 17:33 UTC; receipt:
  `<home>/mokaair-work/backup-receipts/curio-five-recuts-20261012-backup-verified.json`.
  A separate cleanup run must check Studio and backend gates. The controller
  would not delete the hardlink staging directory, which retains about 1.135
  GB until separately removed.
- A 2026-10-12 17:03 UTC `videos.list` readback confirmed all five new IDs
  belong to the linked channel and are private. H02 is processed/succeeded
  with 12:02 duration; U02/H03/L08/H01 are uploaded but still processing, so
  these have not yet passed the upload-completion gate. `captions.list` found
  H02's four tracks serving, U02's zh-TW/en and one zh-TW track on each other
  upload. API metadata does not prove SRT content, alternate dubs or end screen.
- Five new backend projects are imported one at a time under distinct recut
  slugs. Until each video is processed and its new project is linked, original
  projects keep their prior IDs. The H01 staging `meta.json` contains the only
  4,961-byte corrected Chinese description; preserve the small staging
  metadata and hashes outside cleanup targets before deleting that directory.
- Do not edit the local batch during transfer: the tar snapshot and file
  manifest are immutable. Store Studio progress and title corrections beside
  the backup receipts, then retain them with the final backup.
- At 2026-10-12 17:43 UTC, an attempted exact-path removal of the verified
  local temporary archive was rejected by automatic approval review with only
  `blocked by policy`. No local archive, batch or hardlink staging deletion was
  performed; do not retry by disguising or weakening the removal command.
- At 17:54 UTC, Studio still showed all 15 English/Japanese/Korean WAV uploads
  processing. Five private full-length videos, four published caption sets and
  three end-screen elements per video had already been read back. Keep the
  cleanup gate pending until the audio tracks finish and backend IDs are linked.
