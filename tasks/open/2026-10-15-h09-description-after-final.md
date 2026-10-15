---
id: 2026-10-15-h09-description-after-final
title: Correct H09 description after final-cut approval
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-curio-h09
claimed_at: 2026-10-15T08:23:53Z
created_at: 2026-10-15T08:23:44Z
completed_at:
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09/video.json
---

# Correct H09 description after final-cut approval

## Why

After the owner approved H09's final cut, its YouTube description still promised to recheck any new expedition finding "before the final cut and upload." That timing is now false. The promise should refer to the remaining publication decision and the editable description.

## Definition of done

- [x] The H09 description states a time-bounded, accurate update promise before formal publication; no approved narration or media bytes change.

## Steps

- [x] Replace only the stale sentence in the zh-TW description of `video.json`.
- [x] Rebuild and merge the en, ja and ko worksheets against the new description; verify only metadata hashes change.

## How to verify

Compare `git diff -- docs/videos/curio-h09/video.json`; run `node tools/video/cli.mjs lint --slug curio-h09` and `npm run check:tasks`. Check the approved script, timeline, storyboard manifest and final.mp4 SHA-256 values remain E9404ADD…, 69E3FF3D…, 4E8D778D… and BE7FC714…. Regenerate each i18n worksheet and merge without stale-field errors.

## Notes

The final approval in `/admin/videos` was read back on 2026-10-15 and binds final.mp4 SHA-256 BE7FC714…. The October 14 official expedition update still has no aircraft identification. The change is metadata copy only; translators have been notified to refresh their description source hashes.

All three translations were independently reviewed and merged after the metadata correction. A fresh `i18n-sheet --parts metadata,captions` reports 0/100 lines, 0/8 chapters and no metadata todo for en, ja or ko; lint has 0 errors. The approved script, timeline, storyboard manifest and final.mp4 retain their original SHA-256 values. Keep this task in progress until PR #1503 is merged.
