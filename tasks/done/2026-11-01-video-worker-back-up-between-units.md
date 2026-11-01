---
id: 2026-11-01-video-worker-back-up-between-units
title: Video worker: back up between units of a long auto round, not only at its end
status: done
priority: P2
area: tools
owner: claude-opus-5-5-backup-0801
claimed_at: 2026-11-01T08:07:11Z
created_at: 2026-11-01T08:06:33Z
completed_at: 2026-11-01T08:07:12Z
branch: claude/video-backup-between-units
depends_on: []
scope:
  - tools/video/automation/cli.mjs
  - tools/video/automation/backup-between-units.test.mjs
  - docs/videos/BACKUP.md
---

# Video worker: back up between units of a long auto round, not only at its end

## Why

`auto` (tools/video/automation/cli.mjs) ran the backup, and with it the download of an imported video's
upload package (review-package.mjs, at most 40 files a backup), only once a round had ended. A round with a
daily brief's eight languages runs for hours (seven on 2026-10-30). On 2026-11-01 the worker restarted at
04:43 UTC with a deploy and its first round was still running at 07:51; the log had no `backup:` line since,
and `zhong-tian-qu-qi-e031`, `e032`, `e034`, `e035` (approved packages, 60-75 files each) had no work
directory yet, so /admin/videos showed them as not queued. `e033` had been fetched and backed up at 03:15-03:16
in the round before the restart. No STOP file, 132 GB free, no 429 from the review store.

## Definition of done

- [x] In a round longer than `BACKUP_EVERY_MS` (10 min) the first lane runs the backup between units and
      between durable waits, never two at once, and not after a STOP; the round-end backup and the tidy are unchanged.
- [x] `--once` backs up only at its end, as before.
- [x] docs/videos/BACKUP.md says so, with a troubleshooting row for "imported video never queued".

## Steps

- [x] `backupBetweenUnits` in cli.mjs, called by lane 0 before each unit.
- [x] tools/video/automation/backup-between-units.test.mjs (new file; automation.test.mjs is bound by
      docs/videos/long-form/review.json).
- [ ] After merge and deploy: the four episodes become 已備份 and `AI/備份/drama/zhong-tian-qu-qi-e03N/` holds `final.mp4` and `clips/`.

## How to verify

```bash
node --test tools/video/automation/backup-between-units.test.mjs tools/video/automation/backup.test.mjs tools/video/automation/review-package.test.mjs
node --test tools/video/automation/*.test.mjs
```

Removing the `backupNow()` call makes the second test in backup-between-units.test.mjs fail.

## Notes

- Claimed with `--force`: the overlapping tickets 2026-10-23-video-backup-when-ready-to-upload,
  2026-10-29-daily-brief-on-the-host-worker and 2026-10-31-zhong-tian-clip-backup are in-progress, but their
  work on these paths has landed on main (#1785, #1949, #1957) and no open PR touches cli.mjs; this change only
  adds lines (a new function, one call, a doc paragraph and a table row).
- A single unit still runs to its end before a backup can start (one language's dub is about 20 minutes).
- Safe beside another lane: a video a lane is moving is off the site's backup list, and backup.mjs keeps its own
  record in backup-state.json, not auto.json.
