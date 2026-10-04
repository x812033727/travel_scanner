---
id: 2026-10-03-narration-homophone-misses-ni-variant
title: Narration homophone rule misses the 妳/你 pair
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-03T17:48:47Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
---

# Narration homophone rule misses the 妳/你 pair

## Why

The narration check treats a same-sound mismatch as acceptable before it asks Jev
(`tools/video/tts/check.mjs`, `reading()` at :143-145). pinyin-pro 3.29.4, the installed
version, reads 妳 as `nai3` and 你 as `ni3`, so a line whose script says 妳 and whose
transcript says 你 is not recognised as the same sound and goes to Jev. Two real lines on
2026-10-02 went that way and got different answers: one passed at 0.66
(`docs/videos/series-plans/competition-20261002/pilot/review.md:55`), one was flagged at 0.38
(`docs/videos/series-plans/competition-20261002/episodes/audio-check-summary.json`,
WR-E01-L026). The exported `matchKind("棠棠，你連我也信不過？", {text: "棠棠，妳連我也信不過？"}, {}, "zh-TW")`
returns `null`, while 她 heard as 他 returns `"sound"`.

## Definition of done

- [ ] 妳 heard as 你 is matched as the same sound, like 她／他.
- [ ] A test beside the existing 它／他 case in `tools/video/tts/check.test.mjs` pins it.

## Steps

- [ ] Smallest fix: fold the variant before reading, e.g. `pinyin(comparable(text).replace(/妳/gu, "你"), {...})`.
      Avoid pinyin-pro's global `customPinyin`, which would change every other importer.

## How to verify

```bash
node --test tools/video/tts/check.test.mjs
```

## Notes

- `docs/videos/ai-term-system-one-model/demo/demo_pinyin.cjs` reproduces the readings.
