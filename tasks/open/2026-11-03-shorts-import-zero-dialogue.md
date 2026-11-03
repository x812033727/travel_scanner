---
id: 2026-11-03-shorts-import-zero-dialogue
title: Shorts import: accept a zero-dialogue cut (no captions) and an original Short with no long-form source
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-03T13:50:24Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts/import.mjs
  - tools/video/shorts/import.test.mjs
---

# Shorts import: accept a zero-dialogue cut (no captions) and an original Short with no long-form source

## Why

The zero-dialogue series (`docs/videos/wangjia-couple/README.md`, `docs/videos/raccoon-mischief/README.md`, `docs/videos/influencer-piglet/README.md`, `docs/videos/shechu-hell/README.md`) are original 13–18 s vertical Shorts made outside the drama pipeline (Colab H3 clips, ffmpeg cut). `node tools/video/shorts/cli.mjs import --from DIR` is the only way in, and it cannot take them:

- An empty `zh-TW.srt` crashes it: `Cannot read properties of undefined (reading 'text')` (`tools/video/shorts/import.mjs` around line 49 builds each scene's headline from `cues[...]`).
- `line` must be `lab`, `cut` or `drama`; `drama` means a crop of an approved long-form episode, so `evidence` in `qa` wants a source video on the site. These Shorts have none.

## Definition of done

- [ ] `import` accepts a cut with no captions (no CC track, headlines from `meta.json`), and `qa` passes `captions` and `narration` for it with a stated reason.
- [ ] A line (or a `source`-less `drama`) for an original Short, with `evidence` bound to the cut itself instead of a long-form source.
- [ ] Test with a 17 s silent-dialogue fixture.

## How to verify

```bash
node --test tools/video/shorts/*.test.mjs
node tools/video/shorts/cli.mjs import --from <dir with final.mp4, empty zh-TW.srt, meta.json> --workdir <outside repo>
```

## Notes

- First cut waiting on this: `<VIDEO_WORKDIR>/wangjia-couple-e01/edit/final.mp4` (17.8 s, 1080x1920, 30 fps, -14 LUFS).
