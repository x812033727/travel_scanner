---
id: 2026-10-03-narration-homophone-misses-ni-variant
title: Narration homophone rule misses the 妳/你 pair
status: done
priority: P2
area: tools
owner: claude-opus-5-5-tts-ni-tempdirs
claimed_at: 2026-10-04T14:52:49Z
created_at: 2026-10-03T17:48:47Z
completed_at: 2026-10-04T15:32:13Z
branch: claude/tts-ni-variant-and-test-tempdirs
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

- [x] 妳 heard as 你 is matched as the same sound, like 她／他.
- [x] A test beside the existing 它／他 case in `tools/video/tts/check.test.mjs` pins it.

## Steps

- [x] Smallest fix: fold the variant before reading, e.g. `pinyin(comparable(text).replace(/妳/gu, "你"), {...})`.
      Avoid pinyin-pro's global `customPinyin`, which would change every other importer.

## How to verify

```bash
node --test tools/video/tts/check.test.mjs
```

## Notes

- `docs/videos/ai-term-system-one-model/demo/demo_pinyin.cjs` reproduces the readings.
- 2026-10-04 (claude-opus-5-5-tts-ni-tempdirs): `reading()` in `tools/video/tts/check.mjs` now
  replaces 妳 with 你 after `comparable()` and before pinyin-pro, as suggested; `customPinyin` is
  untouched, so other importers of pinyin-pro read as before. Only `reading()` changed, so the
  fold applies to the same-sound rule alone: "exact" and "filler" still compare the characters.
- The test sits beside 它／他 in "same-sound characters and added filler words pass without Jev"
  and uses the three transcripts competition-20261002 produced: L002 (`字簽了 你也就沒用了`) and
  WR-E01-L026 from both recognizers (`棠棠，你連我也信不過？`, and Whisper's `唐唐,你連我也信不過?`,
  whose 唐 for 棠 is already the same sound). With the fold removed the test fails with
  `actual: null, expected: 'sound'`; with it, it passes.
- `node --test tools/video/tts/check.test.mjs`: 19 of 20 pass; the one failure is the known
  Windows-only "a second transcript clears a line only Gemini misheard" test.
- `tools/video/tts/check.test.mjs` is bound by SHA-256 in `docs/videos/long-form/review.json`
  (`check.mjs` is not); the PR is a draft until an independent reviewer adds the
  duration-receipt increment.
