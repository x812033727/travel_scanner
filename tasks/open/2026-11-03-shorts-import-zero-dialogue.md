---
id: 2026-11-03-shorts-import-zero-dialogue
title: Shorts import: accept a zero-dialogue cut (no captions) and an original Short with no long-form source
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-wangwang
claimed_at: 2026-11-05T00:18:19Z
created_at: 2026-11-03T13:50:24Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts/import.mjs
  - tools/video/shorts/import.test.mjs
  - tools/video/shorts/core.mjs
  - tools/video/shorts/qa.mjs
  - docs/videos/SHORTS.md
---

# Shorts import: accept a zero-dialogue cut (no captions) and an original Short with no long-form source

## Why

The zero-dialogue series (`docs/videos/wangjia-couple/README.md`, `docs/videos/raccoon-mischief/README.md`, `docs/videos/influencer-piglet/README.md`, `docs/videos/shechu-hell/README.md`) are original 13–18 s vertical Shorts made outside the drama pipeline (Colab H3 clips, ffmpeg cut). `node tools/video/shorts/cli.mjs import --from DIR` is the only way in, and it cannot take them:

- An empty `zh-TW.srt` crashes it: `Cannot read properties of undefined (reading 'text')` (`tools/video/shorts/import.mjs` around line 49 builds each scene's headline from `cues[...]`).
- `line` must be `lab`, `cut` or `drama`; `drama` means a crop of an approved long-form episode, so `evidence` in `qa` wants a source video on the site. These Shorts have none.

## Definition of done

- [x] `import` accepts a cut with no captions (no CC track, headlines from `meta.json`), and `qa` passes `captions` and `narration` for it with a stated reason.
- [x] A line (or a `source`-less `drama`) for an original Short, with `evidence` bound to the cut itself instead of a long-form source.
- [x] Test with a 17 s silent-dialogue fixture.

## How to verify

```bash
node --test tools/video/shorts/*.test.mjs
node tools/video/shorts/cli.mjs import --from <dir with final.mp4, empty zh-TW.srt, meta.json> --workdir <outside repo>
```

## Notes

- First cut waiting on this: `<VIDEO_WORKDIR>/wangjia-couple-e01/edit/final.mp4` (17.8 s, 1080x1920, 30 fps, -14 LUFS).
- 2026-11-05 (claude-opus-5-5-wangwang): done as two explicit meta fields instead of a new line.
  An empty or missing `zh-TW.srt` makes the script `dialogue: false` with `narration: []` per
  scene, the cards from `meta.json` `headlines` (required; refused before anything is made
  without them), zero cues, no phrase audio, and `checks.json` `dialogue: false`. An original
  Short is `line: "drama"` + `original: true` and no `source`; `validate(doc, { imported: true })`
  is the only way those two fields pass, so authored scripts are unchanged. `qa`: `narration`
  and `captions` pass with "no spoken words: zero-dialogue cut" when script, timeline and
  checks.json all agree there is no dialogue (a stray caption still fails); `evidence` for an
  original Short passes only when `checks.json.final_sha256` is the hash of `upload/final.mp4`.
  Not done here: nothing measures that the cut really has no speech (that stays with the owner
  and the policy check); the 9–18 s length needs the site's `seconds_min`, otherwise `profile`
  fails; whether YouTube accepts an empty `zh-TW.srt` in `push`/`package` was not tried (offline).
  Tests: `tools/video/shorts/import.test.mjs` (17 s colour-and-tone cut made with ffmpeg in the
  test; skips without ffmpeg).
