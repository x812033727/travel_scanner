---
id: 2026-10-31-zhong-tian-clip-backup
title: Zhong-tian: back up the per-shot 1080p clips of e031+ so a re-cut or season 2 does not need a re-render
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-31T09:25:51Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/README.md
  - tools/video/review/files.mjs
---

# Zhong-tian: back up the per-shot 1080p clips of e031+ so a re-cut or season 2 does not need a re-render

## Why

The owner (2026-10-31) wants everything a later conversation or a season-2 production would need kept in one known
place. From e031 the episodes are made on Colab in a cloud session; `node tools/video/cli.mjs import --from DIR` sends
only the cut (final.mp4, srt, dubs, thumbnail, meta.json) to the host, so the host's Google Drive backup
(docs/videos/BACKUP.md, `AI/備份/<series>/<episode>/`) holds the finished episode but not the per-shot 1080p clips
(`<workdir>/zhong-tian-qu-qi-eNNN-dh/clips/sNN-t1.mp4`, about 300 MB per episode). They disappear with the container;
a re-cut, a Short or a compilation would need stages 1-3 again (4-6 G4 hours per episode, different takes).

## Definition of done

- [ ] Every imported Colab episode's `clips/sNN-t1.mp4` ends up under the same `AI/備份/<series>/<episode>/clips/`
      folder the host already fills, checked by the backup's own `rclone check`.
- [ ] `production/README.md` section 2 no longer lists the clips as unbacked.

## Steps

- [ ] Decide the route with the owner: (a) let `import --from` carry an optional `clips/` folder to the host's
      `video_work/<slug>/clips/` so the full tier copies it, or (b) a separate upload.
- [ ] Back-fill e033-e039 while their workdirs still exist.

## How to verify

`/admin/videos?tab=settings#video-backup-settings` shows the episode as done with its clips listed.

## Notes

- e031/e032 were made by another account's session; their clips may already be gone.
