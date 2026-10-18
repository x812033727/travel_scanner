---
id: 2026-10-11-make-a-dub-again-on-a
title: Make a dub again on a video whose work files were tidied
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T00:00:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/package
  - tools/video/automation
  - tools/video/review
---

# Make a dub again on a video whose work files were tidied

## Why

The worker clears a published video's work files seven days after publication
(`tools/video/automation/tidy.mjs`). The owner's 再做一次 for a skipped dub
(`2026-10-10-let-the-owner-re-request-a`) is refused there in three places, with the
reason in the cell. Most of the 49 dubs skipped by 2026-10-09 belong to videos already
past that point, so the button does not help them; the owner is arranging those by hand.

`dub` and `check-audio` could still run on a tidied video: they need `video.json`,
`timeline.json`, the translations and a Gemini voice, not `final.mp4` or the narration
takes; the whole track is bought again (about 6,000 to 10,000 characters). What cannot be
built is the batch: `package` needs `final.mp4` (`tools/video/package/cli.mjs`), the tidy
deleted the other locales' track files, and YouTube sync refuses a batch that does not
name the whole choice (`apps/api/app/video_youtube/language_package.py`).

## Definition of done

- [ ] A languages batch for one re-made dub can be sent for a tidied video, re-attaching
      the other locales' files from the review store by hash instead of from disk, and
      YouTube sync accepts it.
- [ ] The cell offers 再做一次 on a tidied video and says the whole track is bought again.

## Steps

- [ ] A dub-only package path that does not read `final.mp4`.
- [ ] By-reference files in `review-push --gate languages` and in the manifest contract
      (`docs/videos/APPROVED-LANGUAGE-PACKAGE.md`).
- [ ] Lift the tidied refusal in the API, the worker and the cell together.

## How to verify

Automation test: a tidied video with a skipped ja dub asked again ends with a pending
languages card carrying `dub_ja` and the other locales' files unchanged.

## Notes

- Decided out of scope in the spec of the retry (section 5); this is that follow-up.
