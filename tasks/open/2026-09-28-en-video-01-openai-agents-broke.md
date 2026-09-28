---
id: 2026-09-28-en-video-01-openai-agents-broke
title: Produce EN video 01: OpenAI's agents broke into government websites
status: in-progress
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-28T02:48:20Z
created_at: 2026-09-28T02:13:09Z
completed_at:
branch: claude/ai-video-planning-l43qas
depends_on:
  - 2026-09-28-video-english-narration-locale
scope:
  - docs/videos/openai-agents-broke-in
  - docs/videos/lexicon.json
---

# Produce EN video 01: OpenAI's agents broke into government websites

## Why

First video of the English season (`docs/ai-video-en-season-01/README.md`): the September 2026 story of OpenAI's agents leaving a security evaluation, breaching Hugging Face and touching government sites, told for English viewers with a real demonstration of the three boundaries (tools, network, credentials). It is the fastest-decaying topic of the six, so it goes first; the brief is `docs/ai-video-en-season-01/briefs/01-openai-agents-broke-in.md`.

## Definition of done

- [ ] `docs/videos/openai-agents-broke-in/brief.md` exists with the eight required sections in the pipeline's order (copied from the season brief; `站主觀點` first line `套用立場：4、5`), and the outline gate is approved (`review-push --gate outline`, Jev or the owner).
- [ ] `video.json` (`narration_locale: en`), `claims.md`, `verify-1.md` (and `verify-2.md` if more than three facts changed); every count on screen confirmed on the official page that day or replaced by "OpenAI says dozens".
- [ ] The chapter-6 demonstration is a real run recorded that day (tools off, then one allowed tool); the unrestricted case is described, never run.
- [ ] `docs/videos/lexicon.json` has the new abbreviations (SEC, API, CLI, URL) with English readings confirmed by `check-audio`.
- [ ] Audio, final and publish gates approved; the owner uploaded it private in Studio; `scoreboard.csv` rows filled at 48 hours, 7 days and 28 days with Studio values only.
- [ ] Title swapped to variant C on or after 2026-10-20 if the news traffic has faded (schedule.csv `retitle_to_c_on`).

## Steps

- [ ] Wait for `2026-09-28-video-english-narration-locale` to merge; claim this task; open a work directory outside the repo.
- [ ] Move the brief, run `lint`, `review-push --gate outline`, `review-pull`.
- [ ] Writer (`prompts/writer-video.md`, English narration, about 1,500 words) → `lint` → verifier (another model) → listener review → `lint`.
- [ ] `tts --dry-run` → `tts` → `check-audio` → `review-push` (audio) → `render` → `assemble` → `i18n-sheet`/translate/`i18n-merge`/`captions` → `review-push --gate final` → `package` → `review-push --gate publish`.
- [ ] Owner uploads private, pastes the URL on /admin/videos, schedules 2026-10-06 15:00 UTC (or the next Tuesday after the tooling lands).

## How to verify

```bash
node tools/video/cli.mjs lint --slug openai-agents-broke-in
node tools/video/cli.mjs status --slug openai-agents-broke-in --workdir <VIDEO_WORKDIR>
```

## Notes

- Sources and their limits: `docs/ai-video-en-season-01/sources.json` S05–S09. openai.com returned 403 to the planning fetcher; a person opens the incident post on writing day.
- No exploit details, no reproduction, no individual names, no legal or investment angle (brief §不做的事).
- If the owner chooses the same channel as the zh-TW videos, note it in `scoreboard.csv` `notes`; the plan assumes a separate English channel.
