---
id: 2026-11-11-video-tool-reads-a-video-s
title: Video tool reads a video's audience retention curve from the YouTube Analytics API
status: in-progress
priority: P2
area: api
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T02:17:12Z
created_at: 2026-11-11T01:22:56Z
completed_at:
branch: claude/youthful-albattani-m1ih5z
depends_on: []
scope:
  - apps/api/app/video_youtube
  - apps/api/tests/test_video_youtube_retention.py
  - tools/video/youtube-reports
  - docs/videos/YOUTUBE-REPORTS.md
  - .agents/skills/youtube-channel-reports/SKILL.md
  - .claude/skills/youtube-channel-reports/SKILL.md
---

# Video tool reads a video's audience retention curve from the YouTube Analytics API

## Why

The owner asked on 2026-11-11 for the weekly channel review to see where viewers leave an
episode. The site's daily YouTube Reporting API downloads (`docs/videos/YOUTUBE-REPORTS.md`) carry
no per-second retention, so the review can only see averages: 奇聞檔案局's organic viewers leave
after about 52 s of 13-minute episodes, and nobody can say which line loses them without Studio.

The channel link already holds `yt-analytics.readonly`
(`apps/api/app/video_youtube/client.py` `ANALYTICS_SCOPE`), which is what the YouTube Analytics
API v2 needs for an audience retention report: `reports.query` with `dimensions=elapsedVideoTimeRatio`,
`metrics=audienceWatchRatio,relativeRetentionPerformance`, `filters=video==<id>` (and optionally
`audienceType==ORGANIC`), over a date range. No new Google consent should be needed; verify that
against the API docs before building.

## Definition of done

- [ ] A video tool token can ask the site for one video's retention curve (100 points of elapsed
      ratio with audience watch ratio, and relative performance where YouTube returns it) for a date
      range, organic only or all traffic, without any Google credential leaving the site.
- [ ] `node tools/video/youtube-reports/cli.mjs retention --video <id> [--from --to] [--organic]`
      prints the curve, the first big drop (largest fall between neighbouring points in the first
      30%) mapped to seconds with the video's duration, and can write CSV.
- [ ] A missing scope, a disabled Analytics API, too few views for YouTube to answer, and a
      video of another channel each give a clear message (the reports CLI's exit codes).
- [ ] `docs/videos/YOUTUBE-REPORTS.md` and the `youtube-channel-reports` skill say how to read it,
      and that computed figures stay private (derived-metrics policy).
- [ ] The weekly review (`docs/videos/channel-changes/README.md`) can use it to map the first drop
      to a script line (`docs/videos/<slug>/video.json` timeline).

## Steps

- [ ] Read the Analytics API v2 audience retention docs (dimension/metric combination, quota,
      minimum view thresholds) and check the scope.
- [ ] API: an admin-or-video-token endpoint next to `admin_reports_api.py`, calling Google with the
      stored token (`client.py`), with tests that mock Google.
- [ ] Tool: the `retention` subcommand in `tools/video/youtube-reports/cli.mjs` with tests.
- [ ] Docs and skill (both skill copies stay byte-identical; `npm run test:tools` checks).

## How to verify

`cd apps/api && uv run pytest tests/test_video_youtube_retention.py`, `npm run test:tools`, then on the
host after deploy: `node tools/video/youtube-reports/cli.mjs retention --video gkl0vABh1_c --organic`.

## Notes

- Filed from the 2026-11-11 channel review session (draft PR #2069). Not started.
- Owner context: viewers of the curio v2 batch leave in the first minute; the curve is what tells
  whether it is the hook, the promise line or a padded stretch.
