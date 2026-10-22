---
id: 2026-10-22-back-up-videos-even-when-an
title: Back up videos even when an automation round ends in an error
status: done
priority: P1
area: tools
owner: claude-opus-5-5-video-cloud-backup
claimed_at: 2026-10-22T00:30:50Z
created_at: 2026-10-22T00:30:32Z
completed_at: 2026-10-22T02:17:43Z
branch: claude/video-cloud-backup-issue-48a886
depends_on: []
scope:
  - tools/video/automation/cli.mjs
  - tools/video/automation/cli.test.mjs
  - tools/video/automation/client.test.mjs
---

# Back up videos even when an automation round ends in an error

## Why

The video worker copies the videos on YouTube to the owner's Google Drive once a round, after
the units (docs/videos/BACKUP.md). `auto` did that only on a round that finished: an
`AutomationError` from any lane went straight to the catch and the run exited, so the backup
never ran. From 2026-10-21 16:43Z the site refused the tutorial writer's prompt every round
("instructions：內容太長", PR #1657), every round exited with 4, and on 2026-10-22, with the
rclone remote freshly installed on the host, none of the 62 videos on YouTube was even queued:
the site still showed the lock reported at 2026-10-21 01:00 and the owner's test unanswered.

## Definition of done

- [x] A round that ends in an error still runs the backup (which reads its own settings,
      honours a STOP file and never throws), then exits with the same code as before.
- [x] The tidy still runs only after a round that finished.
- [x] Deployed, and the worker's log shows `backup:` lines on a round that ended in an error.

## Steps

- [x] `run()` in `cli.mjs` calls `backupAfterRound` in its catch, for an `AutomationError`
      and for any other error before it is thrown on.
- [x] Test: the site refuses the settings with the real 422 text; the backup client is asked
      for its config and told the lock, the exit code is still `external`, and the tidy, which
      backups being off would otherwise let clear the video, leaves it.

## How to verify

```bash
node --test tools/video/automation/cli.test.mjs
```

On the host after the deploy: `docker compose -f docker-compose.prod.yml logs --since 15m video-worker | grep backup:`.

## Notes

- `client.test.mjs` "auto exits for the owner … Claude Code needs updating" drives `auto` into
  an error with a fake site that fails on any request it does not expect; it now answers the
  backup config with a 404 (a site from before backups) and expects that request last.
- On Windows, two tests in `backup.test.mjs` fail on main as well ("a file added after the
  backup…", "a check that finds Drive's copy different…"); this change does not touch
  backup.mjs. CI runs them on Linux.
- Why the worker had not reported between 2026-10-21 01:00 and the 16:42Z restart is unknown:
  the old container's log went with it.
- 2026-10-22 02:02Z deployed as 53ad804a6. Every round since ends at the monthly draft cap
  (exit 3) and still backs up two videos: 02:03Z gpt-6-sol-luna-where-to-use and
  claude-opus-5-5-three-numbers, 02:09Z google-vids-omni-free-quota and
  openai-cursor-wind-down-nov-12. The deploy verifier lost the cap/exit pair across those lines;
  fixed under `2026-10-14-recognize-the-video-monthly-draft-cap`.
