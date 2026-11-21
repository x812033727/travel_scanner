---
id: 2026-11-21-shorts-import-silent-zero-dialogue-vertical
title: Shorts import: silent (zero-dialogue) vertical dramas through import, qa, package and push
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-silent-shorts
claimed_at: 2026-11-21T13:44:19Z
created_at: 2026-11-21T13:43:09Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts
  - docs/videos/SHORTS.md
  - docs/videos/shorts-drama/README.md
  - docs/videos/shorts-drama/REVIEW.md
---

# Shorts import: silent (zero-dialogue) vertical dramas through import, qa, package and push

## Why

The zero-dialogue Shorts dramas (`docs/videos/shorts-drama/`: no dialogue, no narration, no
caption cards, 9–20 s, not cut from any long video) are meant to reach the site through
`node tools/video/shorts/cli.mjs import` (REVIEW.md §6), but the import was built for narrated
Shorts cut from a long video: it required `zh-TW.srt` (an empty one crashed with
`Cannot read properties of undefined (reading 'text')`), `validateV2` required narration in every
scene and a `source.slug`, and qa held every Short to 25–55 s or the owner's setting. Found
2026-11-21 when the owner asked to "備份並匯入" 《社畜地獄》e06 (10.8 s, made in Google Flow); the
20 silent dramas of 2026-11-04 never went through the tool either.

## Definition of done

- [x] A drama-line Short with `"silent": true` validates with no scenes, no narration and no source.
- [x] `import` takes `final.mp4`, `meta.json` and an optional chosen `cover.png`, refuses a
      `zh-TW.srt` beside a silent meta, and gives a clear error for a talking cut without captions.
- [x] `check-audio` needs no site and pays for nothing; `qa` holds the cut to 9–20 s and reads
      narration/facts/captions/grammar for what a silent drama is; `package` and `push` carry no
      caption track, and `metadata.json` says `"silent": true`.
- [x] `meta.json` `localizations` (the eight languages of `youtube-meta.json`) reach `metadata.json`.
- [x] Tests (`tools/video/shorts/silent.test.mjs`); SHORTS.md, shorts-drama README and REVIEW §6.
- [x] Verified on `shechu-hell-e06` locally (import, check-audio, qa --offline, package); not pushed.

## How to verify

```bash
node --test tools/video/shorts/silent.test.mjs
node tools/video/shorts/cli.mjs import --from <dir with final.mp4, cover.png, meta.json> --workdir <work base>
node tools/video/shorts/cli.mjs check-audio --dir <build dir>
node tools/video/shorts/cli.mjs qa --dir <build dir> --offline
```

## Notes

- The format: `line: "drama"`, `silent: true` on the script (and on `metadata.json`). Chosen over a
  fourth line so the site's `shorts_line` CHECK, the Shorts tab filters and the category (24) stay
  as they are.
- `qa` uses `SILENT_RANGE` (9–20 s, the drama's own hard range), not the owner's
  `seconds_min`/`seconds_max`. The site's settings cannot go below 10 anyway
  (`video_shorts/schemas.py` `ge=10`, DB CHECK `BETWEEN 10 AND 180`), so a 9-second drama could never
  pass under the setting. Whether the owner wants the setting to govern silent dramas too is theirs.
- `layout` stays failed for every import (no safe-area measurement of a finished file): the owner
  looks once. A hand push makes the owner decide both gates anyway.
- `grammar`: a silent drama loops by its story (the twist frozen on its last beat), so the cover
  being the chosen frame and the last frame not returning to the first are `warnings`, not failures.
  e06 measured cover 12.9 dB, loop 9.1 dB.
- The site adds `｜CC字幕` to every title on the way to YouTube; for a silent drama that is false.
  The fix is in `apps/api/app/video_youtube` (`requests.py`, `sync.py` were claimed by two stale
  October tasks), so it is its own task: `2026-11-21-silent-shorts-leave-the-cc-captions`.
- `2026-10-14-shorts-carry-translated-titles-descriptions-and` (open) is the general translation
  flow; this only passes through the translations a maker already wrote.
- On this machine the site token was revoked on 2026-11-21 (`package` exits 3), so `package` was
  verified with `packageBuild` and explicit settings.
