---
id: 2026-09-28-video-english-narration-locale
title: Slides pipeline: per-video narration locale so English-first videos can be produced
status: done
priority: P1
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-28T02:47:47Z
created_at: 2026-09-28T02:13:09Z
completed_at: 2026-09-29T02:58:50Z
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

- [x] `video.json` accepts `narration_locale` (default `zh-TW`, so every existing video and fixture lints unchanged); with `en`, `voice.lang` and `youtube.default_language` must be `en`.
- [x] `lint`: English pace (about 150 words a minute instead of 250 characters) for chapter and total length; the lexicon rule for `en` checks only all-caps abbreviations and terms listed in the lexicon, not every Latin word; brief section headings stay zh-TW.
- [x] `tts`: the loaded project's dictionary drops Chinese-character aliases for a non-Chinese narration (`speechLexicon`, as `dub` does); the English style is written in `video.json` (`DUB_STYLES.en` is the reference text).
- [x] `check-audio`: transcription and Jev run with `language: en` (the server's `TrackLanguage` already accepts it for dubs); the pinyin homophone and particle rules are skipped for `en`.
- [x] `i18n-sheet`/`i18n-merge`/`captions`: the source locale is the narration locale; translations go to the other four; `metadata` uses the English labels and `default_language: en`; the description's article link picks the `en` locale first.
- [x] `stages`/`state` treat the narration locale as the base track and list dub locales from it (`dubLocales(doc)`); `qa` needs no change (it reads the captions manifest and lint).
- [x] Tests in `tools/video/**/*.test.mjs` cover an `en` fixture end to end through lint, timeline and captions; `npm run test:tools` passes; `.agents/skills/youtube-video/references/automated.md` documents the field.

## Steps

- [x] Replace the constant with `narrationLocale(doc)` in `schema.mjs` and thread it through `lint.mjs`, `stages.mjs`, `state.mjs`, `metadata.mjs`, `captions.mjs`, `tools/video/i18n`, `tools/video/tts/check.mjs` and `tools/video/tts/requests.mjs`.
- [x] Add the `en` fixture and the tests (`tools/video/core/narration-locale.test.mjs`, 8 tests; 483 pass).
- [x] API: no change needed: `checking.py` already reads `language` from the request (the dubs added it) and `schemas.py` accepts every caption locale. Not edited: `checking.py` reads the language from the request (already a field for dubs) and drops the Mandarin-only prompt when it is not zh-TW; `schemas.py` unchanged unless a default needs moving.
- [x] Document in `automated.md`; note that Jev's outline and policy judges are language-agnostic prompts but the channel stance is written in zh-TW.

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
- 2026-09-28 (claude-fable-5-1): done on branch `claude/ai-video-planning-l43qas` (commit e7a9b8b3). Also: an English sentence warns at 25 words (`SENTENCE_WARN_EN`), English written-language and process phrases are checked, `parseDubLocale`/`trackFiles`/`checkFiles`/`lexiconFor` take the narration locale, `dub --locale` and `i18n-sheet --locale` are validated against the video's own dub locales, `defaultRate` scales from the fixed rates when the narration is not zh-TW, and `DUB_STYLES` gained a zh-TW style so a Chinese dub of an English video has a voice. Not done: the host worker's planner and writer prompts (`tools/video/automation/prompts.mjs`) still assume zh-TW; the English season is written by hand for now. Left `render/subtitles.mjs` (drama burn-in) and `automation/compilation.mjs` on `NARRATION_LOCALE`, since dramas and compilations stay zh-TW.
- 2026-09-29 (claude-opus-5-5, same session as the work above): closed. Every item in the definition of done was ticked on 2026-09-28 in commit e7a9b8b3; the season then moved to zh-TW narration with English dubs, so the English-narration prompts for the host worker's planner and writer stay a possible follow-up rather than part of this task. Closing it releases its scope for the check-audio and speechHash tasks.
