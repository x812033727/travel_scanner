---
id: 2026-10-23-preflight-music-before-paid-dub-synthesis
title: Preflight music before paid dub synthesis
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-23T12:15:16Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
---

# Preflight music before paid dub synthesis

## Why

The #1669 generated-music guard reaches a dub through `musicInputs()` in `dubSound()`.
`dubLocale()` currently calls paid `synthesize()` for pending translation lines before
`dubSound()` checks that music. A legacy, missing, changed or short generated track can
therefore stop the final mix after dub speech has already been purchased. The C-series
safety port holds before dub *mixing*, not before dub speech spend. No C-series dub run is
authorized in that port.

## Definition of done

- [ ] A dub with invalid required music stops before the first paid speech request, with
      a clear owner action and no new speech journal, audio cache or TTS charge.
- [ ] The check uses the current source cut length, SHA and fully decoded generated-music
      evidence. Valid owner-supplied music and music-free videos keep their existing path.
- [ ] The later mix-time check remains, so a music file changed during speech work cannot
      enter a final dub.

## Steps

- [ ] Coordinate a narrow release of these dubs files from the active A01 lexicon and
      five-language task owners before claiming or editing; do not force their claims.
- [ ] Place the shared music preflight after current translation/timeline checks and before
      the `synthesize()` loop, passing `timeline.total_frames / FPS` explicitly.
- [ ] Test invalid legacy/short/missing/changed generated music with a zero-call speech stub,
      plus valid generated, owner track and no-music routes. Keep the mix-time race guard.

## How to verify

Run focused `node --test tools/video/dubs/dubs.test.mjs` with FFmpeg present and the
video tooling CI jobs. The failing music cases must make zero calls to the speech client.

## Notes

Filed 2026-10-23 from independent review of the C-series #1669 port. The new shared
`musicInputs()` guard is called near `tools/video/dubs/cli.mjs:194`; the current
`dubLocale()` paid speech loop is near line 251 and `dubSound()` near line 365. This
ticket is separate from the port and makes no change to the C-series dub route now.
