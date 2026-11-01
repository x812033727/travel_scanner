---
id: 2026-11-01-video-backup-an-imported-video-s
title: Video backup: an imported video's PNG thumbnail is never copied to Drive
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-01T03:47:17Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/backup.test.mjs
---

# Video backup: an imported video's PNG thumbnail is never copied to Drive

## Why

zhong-tian-qu-qi-e033 (imported, upload package approved) was backed up 2026-11-01 03:16 UTC to
`AI/備份/drama/zhong-tian-qu-qi-e033/`: 70 files, 41 clips, every caption, description and dub, but
the worker's report says `thumbnail: false`. The imported package's thumbnail is a PNG:
`tools/video/automation/review-package.mjs` writes it as `upload/thumbnail.png`, while
`tools/video/automation/backup.mjs` only plans and counts `thumbnail.jpg` (around lines 153 and 238).
Every imported episode (the zhong-tian route-A episodes ship `thumbnail.png`) loses its thumbnail in the backup.

## Definition of done

- [ ] `backup.mjs` copies `upload/thumbnail.<png|jpg|webp>` (and `thumbnail-b.*` variants) and reports `thumbnail: true` for it.
- [ ] A test in `tools/video/automation/backup.test.mjs` with a PNG-thumbnail package.
- [ ] After deploy, the next backup round fills in e033's thumbnail (check `/admin/videos?tab=settings#video-backup-settings`).

## How to verify

`node --test tools/video/automation/backup.test.mjs`
