---
id: 2026-10-31-imported-video-whose-review-package-is
title: Imported video whose review package is gone stops retrying its backup
status: done
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-31T13:09:40Z
completed_at: 2026-10-31T13:11:19Z
branch:
depends_on: []
scope:
  - tools/video/automation/backup.mjs
  - tools/video/automation/review-package.test.mjs
  - docs/videos/BACKUP.md
---

# Imported video whose review package is gone stops retrying its backup

## Why

#1957 fetches an imported video's upload package from the review store before the Drive backup.
When the store has let go of the whole package (old episodes, `zhong-tian-qu-qi-e001-005` and
`e006-010` on 2026-10-31), the fetch finishes with 0 files and the backup then reports
`has no upload package to back up` as a failure: three attempts, then again every six hours,
forever, with nothing that could ever succeed. The lines also fail the deploy verifier's
`video-worker-started` check on every deploy.

## Definition of done

- [x] Such a video tells the site once why nothing was backed up, and is not tried again.
- [x] It is not read as backed up: the tidy's verdict stays not ok.
- [x] A renewed package with files is fetched and backed up as usual.

## How to verify

`node --test tools/video/automation/review-package.test.mjs`

## Notes

The site refuses a partial report with 0 files (`_refuse_incomplete`), so this reports `failed`
once with the reason and keeps a local `package_gone` state, with no API change. The three
failures in `backup.test.mjs` on Windows are there on main as well.
