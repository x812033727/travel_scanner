---
id: 2026-11-01-zhong-tian-the-line-recordings-travel
title: Zhong-tian: the line recordings travel with the upload package to the Drive backup
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-zt-e033
claimed_at: 2026-11-01T14:23:25Z
created_at: 2026-11-01T14:23:11Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/import
  - tools/video/automation/review-package.mjs
  - tools/video/automation/review-package.test.mjs
  - tools/video/automation/backup.mjs
  - tools/video/automation/backup.test.mjs
  - docs/videos/BACKUP.md
  - docs/videos/COMPILATIONS.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/README.md
---

# Zhong-tian: the line recordings travel with the upload package to the Drive backup

## Why

站主 2026-11-01：原始錄音也要備份。An imported episode's line-by-line voice takes (the workdir's `audio/` for zh-TW and
`audio-<locale>/` for each dub, with each dub line's `.json` naming the text, style and voice) lived only in the cloud
session's workdir. Changing one line later needs them: a new recording does not sound the same. About 75 MB an episode.

## Definition of done

- [x] `tools/video/import/recordings.mjs`: pack the folders into one playable wav a locale plus `manifest.json` (each
      line's offset, header bytes, hash and sidecar); `unpack` cuts them back byte for byte (checked on e035: 748 files).
- [x] `import --publish` carries them as `recording_<locale>` (audio/wav) and `recordings_manifest` (application/json),
      from `--recordings DIR` or the `--clips` folder's parent; metadata.json names the manifest (`recordings_sha256`).
      Content types the site already takes, so `apps/api` is unchanged (`schemas.py` is hash-bound by the long-form receipt).
- [x] The worker places them at `recordings/` (`review-package.mjs placeOf`) and the full tier copies `recordings/`
      (`backup.mjs FULL_DIRS`). Tests for all three.
- [x] Docs: BACKUP.md, COMPILATIONS.md, the zhong-tian production README.
- [ ] After merge and deploy: e031-e039 sent again with their recordings (a new upload package each; the owner approves),
      and each `AI/備份/drama/zhong-tian-qu-qi-eNNN/recordings/` holds a manifest and nine wavs.

## How to verify

`node --test tools/video/import/*.test.mjs tools/video/automation/review-package.test.mjs tools/video/automation/backup.test.mjs`
