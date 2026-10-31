---
id: 2026-10-31-zhong-tian-e041-e042-brief-script
title: Zhong-tian e041-e042: brief, script, storyboard, video.json and clip lists (no generation)
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e033
claimed_at: 2026-10-31T08:03:03Z
created_at: 2026-10-31T08:03:03Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/ref2manifest.mjs
---

# Zhong-tian e041-e042: brief, script, storyboard, video.json and clip lists (no generation)

## Why

The owner confirmed (2026-10-31) that nobody had written episodes 41-60 and asked for 41 and 42 first, from the
season-01.json outline, authoring.md and production/storyboard-rules.md, in the e033-e040 format, as a PR to review
before any clip is made.

## Definition of done

- [x] docs/videos/zhong-tian-qu-qi-e041 and e042: brief, script, storyboard, video.json, overlays.
- [x] hailuo/ff-dh-e041/e042 and clips-dh-e041/e042 from gen-dh.mjs.
- [x] e042's new characters (xudalang, zhouyuanwai) and sets (zhou-kezhan, gongyuan) registered in cast.json,
      gen-dh.mjs, ref2manifest.mjs and dub-glossary.json.
- [ ] The owner reviews the PR.
- [ ] Before e042 can be made: paint refs-dh/xudalang-portrait-t1.png, zhouyuanwai-portrait-t1.png,
      set-zhou-kezhan-t1.png, set-gongyuan-t1.png (26 of its 35 shots need one of them).

## How to verify

```bash
node tools/video/cli.mjs lint --slug zhong-tian-qu-qi-e041
node tools/video/cli.mjs lint --slug zhong-tian-qu-qi-e042
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/zhong-tian-qu-qi-e041/video.json
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/zhong-tian-qu-qi-e042/video.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/zhong-tian-qu-qi-e04N/video.json
node --test docs/videos/series-plans/zhong-tian-qu-qi/production/colab/manifests.test.mjs
```

## Notes

- e041: 36 shots, ~99 s, 50 lines; sets gucang, shiji, xujia-wu, all pictures exist. The fan-waving master stays
  unnamed (A-ling's 「他認得我」 points back to e030); the 秦 seal is not drawn (no text in pictures), Xu Yan reads it off
  screen; the listener is only a shadow on the window paper.
- e042: 35 shots, ~96 s, 47 lines. Xu Dalang says he arranged the guarantor (s13); who withdrew it is not shown; the
  only m05 hint is the cord mark on his hat (s22). Minor speakers zhanggui (innkeeper) and shuli (registrar) live in
  video.json and dub-glossary only, like e038's guards.
- Voices: every male Gemini voice is already taken by a cast member. Xu Dalang got Puck (used once by an e038 guard);
  Zhou Yuanwai got Gacrux, a mature voice that is probably female, with a 「低沉的男聲」 style line. Needs an audition or the
  owner's choice of a voice to share before dubbing.
- ref2manifest EXTRAS gained innkeepers/thief/thieves/scholars so crowd shots are not told "only person in the frame".
