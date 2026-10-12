---
id: 2026-10-12-play-the-channel-intro-bumper-after
title: Play the channel intro bumper after the opening condensation, not before the first line
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-12T07:44:57Z
completed_at:
branch:
depends_on:
  - 2026-10-12-narrated-videos-open-on-a-30
scope:
  - tools/video/assemble/branding.mjs
  - tools/video/core/branding.mjs
  - tools/video/core/duration.mjs
  - tools/video/compile
  - docs/videos/BRANDING.md
---

# Play the channel intro bumper after the opening condensation, not before the first line

## Why

Since PR #1467 (task 2026-10-12-narrated-videos-open-on-a-30) a narrated video's first chapter
is a 30-60 s curiosity condensation: the hook, then two or three of the video's strongest moments
left without their answers, so the viewer stays. The owner (2026-10-12) asked for the channel
intro bumper to move after that condensation. Today `assemble`/`compile` put the bumper in front
of everything (docs/videos/BRANDING.md): the channel's 5 s / 150-frame intro, or the
「原來如此」 series' 11.9 s / 357-frame intro, plays before the first spoken line, and the
captions, chapters and dub packages are all shifted by `checks.branding.intro_frames`. A viewer
who opens the video sees 5-12 s of bumper before the hook, which is when most leave (D07 in
docs/videos/channel-review-20261007/README.md).

Wanted order: condensation (chapter 1) -> bumper -> chapter 2 onward -> outro.

## Definition of done

- [ ] A new long video built by `assemble` or `compile` has its first spoken line at 0:00 and
      the intro bumper between the end of the first chapter and the start of the second.
- [ ] Captions (every language), YouTube chapters and the dub packages are offset only after
      the bumper's position, not from 0:00; chapter 1 starts at 00:00 and chapter 2 starts
      after the bumper.
- [ ] Videos already pinned to a branding (approved, uploaded, packaged, or with a pin) keep
      their bumper where it was: the new placement applies only to new builds, like the
      existing pin rules in BRANDING.md.
- [ ] Dramas with a cast, compilations and Shorts are decided explicitly (ask the owner if
      unclear; the default is to leave them as they are).
- [ ] BRANDING.md describes the new placement and the offset rule.

## Steps

- [ ] Read docs/videos/BRANDING.md and tools/video/assemble/branding.mjs, core/branding.mjs,
      core/duration.mjs, compile/ to find every place that adds `intro_frames` from frame 0.
- [ ] Choose where the bumper goes: at the first chapter boundary of the timeline
      (`chapterList` in core/timeline.mjs), so it never cuts into a sentence.
- [ ] Move the offset: everything before the boundary keeps its time, everything after it
      moves by `intro_frames`.
- [ ] Decide the pin/version field so old cuts rebuild unchanged.
- [ ] Tests for the boundary placement, caption and chapter offsets, and old pinned builds.

## How to verify

```bash
node --test tools/video/assemble/*.test.mjs tools/video/core/*.test.mjs tools/video/compile/*.test.mjs
npm run test:docs-videos   # needs ffmpeg
```

Then build one real illustrated video and check with ffprobe that the first audio is speech at
0:00, the bumper starts at chapter 2's old start, and the CC lines stay in sync after it.

## Notes

- Do not deploy while a video is being assembled on the host; a rebuild of an approved cut
  must not move its bumper (pin rules).
- The series READMEs (so-thats-why, history-curiosity) already list the series bumper after
  the hook in their episode tables, so this matches the plan they describe.
