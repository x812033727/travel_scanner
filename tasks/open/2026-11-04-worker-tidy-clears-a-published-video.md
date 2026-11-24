---
id: 2026-11-04-worker-tidy-clears-a-published-video
title: Worker tidy clears a published video's work folder before the owner has uploaded its dubs
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-04T01:03:38Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/tidy.mjs
---

# Worker tidy clears a published video's work folder before the owner has uploaded its dubs

## Why

Since 2026-11-04 (#2008) the site's review store keeps a done-with video's files for PREVIEW_RETENTION
(7 days) after the last of "on YouTube, Drive backup done, languages made" holds, because the owner
approves the languages batch (which the site reads as "dubs uploaded in Studio") *before* downloading
the package to upload those dubs. The worker's `tools/video/automation/tidy.mjs` still purges
`video_work/<slug>/` the moment the same three conditions hold (docs/videos/BACKUP.md §跟 tidy 的關係).
The review store no longer depends on it, but on 2026-11-04 the only on-host copy that let the
daily-ai-20261103 package be put back was the worker's `upload/` folder, which tidy had not yet reached.

## Definition of done

- [ ] tidy keeps a done-with video's work folder at least as long as the review store does (or the
      owner decides explicitly that the worker copy may go at once), and BACKUP.md says which.

## Steps

- [ ] Ask the owner whether the worker copy should follow the review store's 7-day wait.
- [ ] Change tidy's purge rule accordingly, with a test in a new test file (editing a file bound in
      docs/videos/long-form/review.json needs an independent DURATION_ONLY rebind).

## How to verify

`npm run test:tools`; on the host, a video that became done-with today still has `video_work/<slug>/upload/`
after the next tidy round.

## Notes

- Background: tasks/done/2026-11-03-admin-upload-zip-fails-to-download.md.
