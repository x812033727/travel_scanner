---
id: 2026-09-28-video-english-narration-locale
title: Slides pipeline: per-video narration locale so English-first videos can be produced
status: in-progress
priority: P1
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-28T02:47:47Z
created_at: 2026-09-28T02:13:09Z
completed_at:
branch: claude/ai-video-planning-l43qas
depends_on: []
scope:
  - tools/video/core/schema.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/stages.mjs
  - tools/video/core/state.mjs
  - tools/video/core/metadata.mjs
  - tools/video/core/captions.mjs
  - tools/video/i18n
  - tools/video/tts/check.mjs
  - tools/video/tts/requests.mjs
  - apps/api/app/video_speech/checking.py
  - apps/api/app/video_speech/schemas.py
  - .agents/skills/youtube-video/references/automated.md
---

# Slides pipeline: per-video narration locale so English-first videos can be produced

## Why

The slides pipeline can only narrate in zh-TW: `NARRATION_LOCALE` is a constant in `tools/video/core/schema.mjs`, `voice.lang` and `youtube.default_language` must equal it, lint demands every Latin word be in `docs/videos/lexicon.json`, and the server's `check-audio` transcription prompt (`apps/api/app/video_speech/checking.py`, `NARRATION_LANGUAGE`) is hard-wired to Mandarin. The English season planned in `docs/ai-video-en-season-01/` needs English narration with English slides; the multi-language audio route (`docs/videos/DUBS.md`) keeps the picture in Chinese and is only a fallback.

## Definition of done

- [ ] `video.json` accepts `narration_locale` (default `zh-TW`, so every existing video and fixture lints unchanged); with `en`, `voice.lang` and `youtube.default_language` must be `en`.
- [ ] `lint`: English pace (about 150 words a minute instead of 250 characters) for chapter and total length; the lexicon rule for `en` checks only all-caps abbreviations and terms listed in the lexicon, not every Latin word; brief section headings stay zh-TW.
- [ ] `tts`: the Gemini voice gets an English `voice.style` default; lexicon aliases apply only when all-Latin (as `dub` already does).
- [ ] `check-audio`: transcription and Jev run with `language: en` (the server's `TrackLanguage` already accepts it for dubs); the pinyin homophone and particle rules are skipped for `en`.
- [ ] `i18n-sheet`/`i18n-merge`/`captions`: the source locale is the narration locale; translations go to the other four; `metadata` uses the English labels and `default_language: en`; the description's article link picks the `en` locale first.
- [ ] `stages`/`state`/`qa` treat the narration locale as the base track; the `dubs` item excludes it.
- [ ] Tests in `tools/video/**/*.test.mjs` cover an `en` fixture end to end through lint, timeline and captions; `npm run test:tools` passes; `.agents/skills/youtube-video/references/automated.md` documents the field.

## Steps

- [ ] Replace the constant with `narrationLocale(doc)` in `schema.mjs` and thread it through `lint.mjs`, `stages.mjs`, `state.mjs`, `metadata.mjs`, `captions.mjs`, `tools/video/i18n`, `tools/video/tts/check.mjs` and `tools/video/tts/requests.mjs`.
- [ ] Add the `en` fixture (a short showcase) and the tests.
- [ ] API: `checking.py` reads the language from the request (already a field for dubs) and drops the Mandarin-only prompt when it is not zh-TW; `schemas.py` unchanged unless a default needs moving.
- [ ] Document in `automated.md`; note that Jev's outline and policy judges are language-agnostic prompts but the channel stance is written in zh-TW.

## How to verify

```bash
node tools/video/cli.mjs lint --file tools/video/core/fixtures/minimal/video.json      # unchanged videos still pass
node tools/video/cli.mjs lint --file <the new en fixture>
npm run test:tools
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_speech*.py
```

## Notes

- 2026-09-28 (claude-fable-5-1): filed from the English season plan. `grep -rn "zh-TW\|NARRATION_LOCALE" tools/video --include=*.mjs` (non-test) finds 132 lines in 29 files, but most are the locale list; the places that assume the narration is zh-TW are the ones in scope here. `apps/api/app/video_speech/ssml.py` has its own `NARRATION_LOCALE` for Azure only; the channel voice is Gemini, so it can stay.
- Estimated one to two days. Until it lands, an English video can only be a zh-TW master with an English dub track (DUBS.md), which the plan treats as a fallback.
