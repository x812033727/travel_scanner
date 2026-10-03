---
id: 2026-10-03-video-voice-accent-a1
title: Video voice accent: retire 「台灣國語」 in Gemini styles for the owner's A1 wording
status: done
priority: P1
area: tools
owner: claude-fable-accent-a1
claimed_at: 2026-10-03T06:40:55Z
created_at: 2026-10-03T06:39:10Z
completed_at: 2026-10-03T07:44:40Z
branch:
depends_on: []
scope:
  - tools/video/core/accent.mjs
  - tools/video/core/accent.test.mjs
  - tools/video/tts/requests.mjs
  - tools/video/tts/tts.test.mjs
  - tools/video/automation/register.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/production/design.mjs
  - tools/video/production/design.test.mjs
  - tools/video/production/voice-audit.mjs
  - tools/video/production/voice-audit.test.mjs
  - tools/video/dubs/plan.mjs
  - apps/api/app/video_automation/models.py
  - docs/videos/README.md
  - docs/videos/ILLUSTRATED.md
  - docs/videos/DUBS.md
  - docs/videos/DESIGN.md
  - docs/videos/DRAMA.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
  - .agents/skills/youtube-video/references/script-writing.md
  - .agents/skills/youtube-video/references/prompts/writer-drama.md
  - .claude/skills/youtube-video/references/prompts/writer-drama.md
---

# Video voice accent: retire 「台灣國語」 in Gemini styles for the owner's A1 wording

## Why

2026-10-03 the owner said the videos' narration sounded 「台灣國語太嚴重」. Every Gemini voice style the
pipeline writes carried 「台灣國語」 or "a natural Taiwanese accent" (`STORY_VOICE_STYLE`, `DEFAULT_VOICE`,
the production narrator and character styles, the zh-TW dub style, the writer prompts), and in Taiwan
「台灣國語」 names the heavy Hokkien-coloured accent, which the model played. Spectral measurement of the
same text under five wordings put 「台灣國語」 last every take; the owner listened to eleven auditions
(`mokaair-work/videos/_audition/accent-20261003/`) and chose A1: 「標準國語，咬字清楚，台北人平常說話的語調」.

## Definition of done

- [x] No style the tools write names 「台灣國語」, 「台灣腔」 or a "Taiwanese accent"; the wording is one
      constant (`tools/video/core/accent.mjs`) in Chinese and English.
- [x] A stored style that still carries the retired wording (the production settings row, a series
      setting book, an older `video.json`) is rewritten when the request is built, once, within 400
      characters, so no stored document or hash has to move.
- [x] Docs and the shared skill say the wording and why.

## Steps

- [x] `core/accent.mjs`: `CHANNEL_ACCENT`, `CHANNEL_ACCENT_EN`, `channelAccent()` with tests.
- [x] `tts/requests.mjs` `voiceFields()` applies it (so Shorts clip keys and dub requests go through it too).
- [x] Constants: `register.mjs`, `models.py`, `flow.mjs`, `production/design.mjs`, `voice-audit.mjs`,
      `dubs/plan.mjs`; writer prompts in `prompts.mjs` ask for the channel wording.
- [x] Docs: `docs/videos/README.md` (「口音」 row), `ILLUSTRATED.md`, `DUBS.md`, `DESIGN.md`, `DRAMA.md`,
      skill `script-writing.md` and `writer-drama.md`.
- [x] Long-form duration receipt rebound by an independent review agent (`claude-pr-review-1168`, commits 261e9d9f and merge 21d69d74) (bound files changed:
      `models.py`, `flow.mjs`, `prompts.mjs`, `automation.test.mjs`, `tts.test.mjs`, `README.md`, `DESIGN.md`).

## How to verify

```bash
node --test tools/video/core/accent.test.mjs tools/video/tts/tts.test.mjs tools/video/automation/automation.test.mjs tools/video/production/*.test.mjs tools/video/dubs/*.test.mjs
node tools/video/long-form/cli.mjs check
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_automation_settings.py
```

On the host after deploy: a video whose `video.json` style still says 「台灣國語」 re-records all clips on
its next `tts` run (the clip keys changed); `speechHash` is unchanged, so approved narration is not
invalidated. The production settings row may keep its English wording: the request rewrites it.

## Notes

- Claimed with `--force`: the overlapping claims on `flow.mjs`/`prompts.mjs`/`automation.test.mjs` are
  September branches already merged; `2026-10-03-drama-craft-spec-check-and-probe` overlaps only on the
  receipt files and `writer-drama.md`/`DRAMA.md`, which every video PR touches to rebind the receipt.
- Fixtures under `tools/video/core/fixtures/` keep the retired wording on purpose: they stand for the
  documents already stored, and the TTS tests prove the rewrite on them.
- Not changed: `check-audio`'s transcription prompt 「台灣國語、繁體字」 (tells the transcriber the
  language, not a performance), Azure help text in `admin.json`, and English prose that names the
  language "Taiwanese Mandarin" (planner and story prompts, docs).
