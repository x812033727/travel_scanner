---
id: 2026-11-03-shorts-import-zero-dialogue
title: Shorts import: accept a zero-dialogue cut (no captions) and an original Short with no long-form source
status: done
priority: P2
area: tools
owner: claude-opus-5.5
claimed_at: 2026-11-03T13:59:09Z
created_at: 2026-11-03T13:50:24Z
completed_at: 2026-11-03T14:27:25Z
branch: claude/shorts-import-zero-dialogue-491331
depends_on: []
scope:
  - tools/video/shorts/import.mjs
  - tools/video/shorts/import.test.mjs
  - tools/video/shorts/core.mjs
  - tools/video/shorts/qa.mjs
  - tools/video/shorts/package.mjs
  - tools/video/shorts/pipeline.test.mjs
  - docs/videos/SHORTS.md
  - apps/api/app/video_youtube/requests.py
  - apps/api/app/video_youtube/sync.py
  - apps/api/app/video_youtube/vps.py
  - apps/api/tests/test_video_youtube_requests.py
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
- Done 2026-11-03 (claude-opus-5.5): `silent: true` (drama only) takes headlines and no
  captions, writes no `upload/zh-TW.srt`, and `metadata.json` says `captions: false`, so the site
  sends no track and no 「｜CC字幕」 title tag (`requests.has_captions`). `original: true` (drama,
  no `source`) lists the cut itself as evidence. The owner also asked for English titles and
  descriptions for the global market: scripts take `localizations: { en: { title, description,
  hashtags? } }` and `package` writes them into `metadata.json`, which the site already sends as
  YouTube localizations. Tests: `tools/video/shorts/import.test.mjs` (a real 17 s ffmpeg cut
  through import, qa and package) and `apps/api/tests/test_video_youtube_requests.py`.
- Still open: a 13–18 s cut fails `profile` against the default 25–55 s range (the owner's
  `seconds_min` setting), and `layout`, `grammar` and `facts` stay with the owner as for any
  imported cut. The localizations reach YouTube only while the owner has not decided the video's
  languages on the panel (`language_package.compose` then keeps only the approved batch's).
