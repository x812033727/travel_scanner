---
id: 2026-10-23-show-brand-story-preproduction-intake-progress
title: Show brand story planning and script intake beside finished-video progress
status: done
priority: P2
area: web
owner: codex-c-series-integration
claimed_at: 2026-10-23T18:29:02Z
created_at: 2026-10-23T12:15:47Z
completed_at: 2026-10-23T23:43:42Z
branch: codex/brand-story-preproduction-progress-20261024
depends_on: []
scope:
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/story_progress.py
  - apps/api/tests/test_video_story_progress.py
  - apps/web/components/admin-video-stories.tsx
  - apps/web/components/admin-video-stories.test.tsx
  - apps/web/lib/admin-video-story-progress-copy.ts
---

# Show brand story planning and script intake beside finished-video progress

## Why

The C01–C20 planning intake and eleven live script cards have been saved to the
video backend. This `kind=story` series renders in `admin-video-stories.tsx`:
its list card shows status and quota without preproduction intake, and its
detail counts episodes with `status=done` as finished films. The generic
`0/20` progress in `admin-video-series.tsx` belongs to a different series
view. The story UI needs separate persisted plan and script-card signals.

## Definition of done

- [x] The actual C-series story list and detail show separately labeled counts
      for full persisted plans, live script cards by review state, source Markdown,
      and finished films, from backend readback rather than repository constants.
- [x] `episodes_done / planned_episodes` and the story detail `done` count
      continue to mean finished films; preproduction counts never advance them.
- [x] The labels distinguish imported source, script review and completed film,
      including missing or partial intake, without implying upload or publication.

## Steps

- [x] Read the full stored story plans and only count episodes with valid plan
      identity, chapters and sources. Match each live script-review card to its
      exact series, episode number and project slug; exclude dropped, rejected,
      superseded or mismatched cards. Count original source Markdown separately:
      C03 has an approved legacy card without `source_md`.
- [x] Add one read-only preproduction summary endpoint and render its counters
      on the `kind=story` list/detail with localized labels. Keep the response
      model and copy in separate, unclaimed modules.
- [x] Test full, partial and absent intake and retain the finished-video progress
      assertion. Coordinate existing claims before editing any scoped file.

## How to verify

Run focused story UI/API tests, `admin-video-stories.test.tsx`, i18n checks,
and read back the C-series card in admin. For current persisted state it should
show 20 full plans, ten approved and one pending script card (ten source
Markdown plus one C03 legacy card), and zero finished films. A failed backend read must be shown as
unavailable rather than silently counted as zero.

## Notes

Filed 2026-10-23 during C-series closeout; corrected after readback of the
`kind=story` route. The story list is in `admin-video-stories.tsx`, and its
detail computes `done` from episode status. The generic series progress label
does not render this story card. This ticket does not authorize changing the
finished-video metric, uploading, publishing or paid generation.

2026-10-24 scope narrowed after collision check. The original `schemas.py` and
five `messages/*/admin.json` paths have active claims from other work lines;
`admin_api.py`, the story component/test and the proposed new modules have no
active task or open-PR path owner. The endpoint and local copy module satisfy
the same definition of done without editing those claimed files.

2026-10-24 implementation complete in the shared checkout: backend endpoint
tests 5/5, story UI tests 28/28, web typecheck, Ruff and focused mypy pass.
The definition of done remains open until the merged release is deployed and
the live admin card is read back. No new worktree was created.

2026-10-24 production closeout: PR #1796 was squash merged as
`a0ea214b5aaba535006b02ab6de393dc38cae359` and deployed by the standard
background host script (`DEPLOY_EXIT=0`, health 3/3). The independent host
verifier reported `TOTAL pass=13 fail=0`, including the live read-only service
computation: 20 full plans, 11 approved scripts, 0 pending scripts, 10
verifiable source Markdown files and 0 finished films. C19 was approved in the
backend and remains unfinished. Both API and web proxy rejected unauthenticated
requests to the new route with HTTP 401. The owner then refreshed the
Traditional Chinese `/admin/videos` C-series card and replied
"顯示正確" to the 20/11/10/0 visual acceptance question. This is an owner
reported UI readback; Chrome automation itself returned `Debugger unattached`.
The finished-film `0/20` remains accurate and does not count preproduction as
completed video. Deployment and verification receipt is on PR #1796.
