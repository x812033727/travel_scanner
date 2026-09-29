---
id: 2026-09-28-video-tool-import-a-finished-long
title: Video tool: import a finished long video made elsewhere into the admin review tab
status: done
priority: P2
area: tools
owner: claude-opus-5.5-shorts-missing
claimed_at: 2026-09-28T23:10:44Z
created_at: 2026-09-28T23:08:27Z
completed_at: 2026-09-29T00:09:05Z
branch:
depends_on: []
scope:
  - tools/video/import
  - tools/video/cli.mjs
---

# Video tool: import a finished long video made elsewhere into the admin review tab

## Why

`/admin/videos` lists only what the site's database knows, and the only way in for a long video
is `review-push`, which needs a `docs/videos/<slug>/video.json` project and the work directory the
slides or drama pipeline leaves. A long video finished by another tool has no such project, so it
never shows on the admin. On 2026-09-29 the owner found six of them missing: PR #880's season one
of 「AI 與真實世界」 (Codex's own builder, 1920×1080, Windows Hanhan narration), which sit only on
this machine. The Shorts pipeline already has `shorts/cli.mjs import` for the same case; long
videos had nothing.

The owner chose (2026-09-29) to write the import this time and send the six videos up.

## Definition of done

- [x] `node tools/video/cli.mjs import --from DIR` reports a long video to `/admin/videos`
      and submits its final cut for review, from a directory holding `final.mp4`, `meta.json`
      and optionally `zh-TW.srt` and a thumbnail.
- [x] The cut is measured, not trusted: duration, picture and sound are probed and anything off
      the long-video profile is listed as a problem on the review card.
- [x] Sending the same cut again is safe (the site answers with the review it has).
- [x] Tests cover `meta.json` validation, the checks from a probe, the project and review bodies.
- [x] The six season-one videos are on `/admin/videos` waiting for the owner.

## Steps

- [x] Write `tools/video/import/import.mjs` on the Shorts site client and upload helper.
- [x] Register `import` in `tools/video/cli.mjs` (the area `import`).
- [x] Tests.
- [x] Import the six videos and check the admin.

## How to verify

`node --test tools/video/import/import.test.mjs`; `/admin/videos` shows the six under 需要你.

## Notes

- An imported video has no `video.json`, so `package`, `languages` and `review-pull` do not
  apply to it: after the owner approves the cut, the upload is by hand in Studio and the YouTube
  address is recorded with the existing form on the video's page.
- It lives in `tools/video/import/`, not beside `review-push`: `tools/video/review` sits in the
  scope of `2026-09-26-video-dubs-worker`, which is still marked review. It uses
  `shorts/site.mjs` for the site and `shorts/push.mjs`'s `upload`, and `review/sync.mjs`'s
  `previewArgs` for the 720p copy, so the calls stay the ones the other tools make.
- A slug the site knows from somewhere else is refused unless `--force`; one this command put
  there (checklist key `imported`) is updated without asking.
- 2026-09-29, run from this branch against the live site: `ai-real-world-01-image-trust` …
  `ai-real-world-06-digital-yesman` (the local cuts in Codex's `travel_scanㄐ` checkout, captions
  from the repo, thumbnail A). Each card lists four differences from the profile: 24 fps, audio
  at 96 kHz, mono, about −17.6 LUFS. The owner decides on those; nothing was re-encoded.
- Their twelve Shorts went up the same day through `tools/video/shorts/cli.mjs import`, as
  `ai-real-world-0N-<name>-short-1|2`, line `cut`, series and source the long video's slug;
  they were re-encoded to the Shorts profile first (30 fps, 48 kHz, two-pass −14 LUFS), which
  that import requires.
