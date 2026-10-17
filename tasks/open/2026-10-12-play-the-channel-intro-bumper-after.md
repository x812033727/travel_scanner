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
branch: claude/bumper-after-condensation
depends_on: []
scope:
  - tools/video/assemble/branding.mjs
  - tools/video/assemble/branding.test.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/core/branding.mjs
  - tools/video/core/branding.test.mjs
  - tools/video/core/compilation.mjs
  - tools/video/core/compilation.test.mjs
  - tools/video/core/stages.mjs
  - tools/video/core/stages.test.mjs
  - tools/video/compile
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
  - tools/video/tts/cli.mjs
  - tools/video/cli.mjs
  - tools/video/review/renewal.mjs
  - tools/video/review/renewal-handoff.mjs
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

- [x] A new long video built by `assemble` has its first spoken line at 0:00 and the intro
      bumper between the end of the first chapter and the start of the second. (`compile` builds
      compilations only, which keep the intro first: see the decision below.)
- [x] Captions (every language), YouTube chapters and the dub packages are offset only after
      the bumper's position, not from 0:00; chapter 1 starts at 00:00 and chapter 2 starts
      after the bumper.
- [x] Videos already pinned to a branding (approved, uploaded, packaged, or with a pin) keep
      their bumper where it was: the new placement applies only to new builds, like the
      existing pin rules in BRANDING.md.
- [x] Dramas with a cast, compilations and Shorts are decided explicitly (ask the owner if
      unclear; the default is to leave them as they are).
- [x] BRANDING.md describes the new placement and the offset rule.

## Steps

- [x] Start only after PR #1467 has merged (it adds the condensation this task builds on).

- [x] Read docs/videos/BRANDING.md and tools/video/assemble/branding.mjs, core/branding.mjs,
      core/duration.mjs, compile/ to find every place that adds `intro_frames` from frame 0.
- [x] Choose where the bumper goes: at the first chapter boundary of the timeline
      (`chapterList` in core/timeline.mjs), so it never cuts into a sentence.
- [x] Move the offset: everything before the boundary keeps its time, everything after it
      moves by `intro_frames`.
- [x] Decide the pin/version field so old cuts rebuild unchanged.
- [x] Tests for the boundary placement, caption and chapter offsets, and old pinned builds.

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

### What was built (claude-opus-5-5-bumper, 2026-10-13)

- **Pin field** `intro_at: "start" | "after_first_chapter"` in `branding.json`. A pin without it
  (every cut before 2026-10-13) reads as `"start"` and keeps its original `branding_hash`, so it
  rebuilds byte-identically; pins written from now on always record the field. An intro after the
  first chapter hashes as `channel-bookends-v2`, so captions, dubs, packages and approvals timed
  for the other placement are never reused. `checks.branding` gains `intro_at_frame` (the body
  frame the intro is inserted before) only when it is not 0.
- **Who moves** (`narratedLong` in core/branding.mjs): slides, screencasts, explainer dramas
  (including the 357-frame 「原來如此」 intro) and brand stories, even with a cast. Dramas with a
  cast, compilations and Shorts keep `start`; that is the task's default and was not re-asked.
- **Where**: the second chapter's `start_frame`, which is a scene start; every scene is its own
  segment opening on a keyframe, so `wrapVideo` copies the body's segments before and after the
  intro, and `brandingJoinArgs` cuts the body's sound at the same sample (`atrim=start_sample`).
- **Offsets**: `presentationTimeline` and `shiftBrandingCues` move only what starts at or after
  the intro; an end exactly at the intro stays before it. Captions in every language, YouTube
  chapters (ch1 at 00:00 holds condensation + intro, ch2 after it), dub tracks and dub-timed
  captions (`captionTimelineOf` caps a line before the intro at the intro), and compilation
  caption merging (`mergeCaptions` `introAtMs`) all follow. `dub` refuses a dubbed line that
  would run across the intro instead of cutting it.
- **Re-placing a not-uploaded cut**: `assemble --intro-after-condensation` takes the pin's assets
  (or current when there is no pin), places the intro after chapter 1 and rewrites the pin only
  after a successful build. The new final.mp4 has new bytes, so the old final/publish approvals
  and upload package stop matching, as after any re-assembly. It refuses uploaded or finished
  videos, dramas with a cast, compilations and Shorts. The renewal tools (review/renewal*.mjs)
  join a retained body after the intro and so refuse a pin placed after the first chapter.
- Totals, duration floors and the end-screen time do not change with the placement, so
  core/duration.mjs, qa, package and flow needed no change.
- Real media check (2026-10-13, scratchpad, installed 「原來如此」 series intro 357 frames):
  final 747 frames; frame 119 is the condensation, frame 120 the intro's first frame, frame 477
  chapter 2; the WAV wrapper matches condensation | intro | chapter 2 | outro sample for sample
  (seams at 0, 4.0, 15.9, 21.9 s); the first 100 ms of the final are the body's voice level;
  chapter 2's first cue is at 15.900 s and chapters read `00:00 開場` / `00:15 第二章`.
- Follow-up not done here: the 奇聞檔案局 v2 recuts (curio-*-v2) are new slugs not in the repo
  yet; a first build of them gets the new placement by default, and an existing pinned workdir
  needs `--intro-after-condensation`.
