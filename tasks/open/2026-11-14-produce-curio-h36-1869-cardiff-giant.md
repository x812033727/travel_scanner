---
id: 2026-11-14-produce-curio-h36-1869-cardiff-giant
title: Produce Curio H36 (1869 Cardiff Giant)
status: in-progress
priority: P2
area: docs
owner: antigravity
claimed_at: 2026-11-14T06:57:19Z
created_at: 2026-11-14T06:57:07Z
completed_at:
branch: antigravity/curio-h36
depends_on: []
scope:
  - docs/videos/curio-h36
  - tools/video/core/drama.mjs
  - docs/videos/lessons/curio.md
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
---

# Produce Curio H36 (1869 Cardiff Giant)

## Why

Produce 奇聞檔案局 episode H36 (`curio-h36`, 1869 Cardiff Giant hoax — why after scientists and newspapers exposed the gypsum statue as a fake, two competing giants collected admission simultaneously on Broadway in New York) from `docs/videos/history-curiosity/pool/batches/wave2-legacy-20261101.json`, following all series rules with owner overrides: built-in `generate_image` illustrations (`cute-mystery` look, imported via `keyframes import --provider external --usd 0`, no MiniMax `image-01`), Gemini `Sulafat` (`zh-TW`) narration, and 8 foreign-language dubs (`en`, `ja`, `ko`, `es`, `pt`, `id`, `vi`, `th`) synthesized via MiniMax Speech.

## Definition of done

- [ ] `docs/videos/curio-h36/` contains verified `brief.md`, `claims.md`, `verify-1.md`, `video.json`, `script.md`, `NOTES.md`, `story-lexicon/`, `review/narrative.json`, `i18n/{en,ja,ko,es,pt,id,vi,th}.json`, and `prompts/keyframes.md`.
- [ ] `node tools/video/cli.mjs lint --slug curio-h36` passes with `0 errors, 0 warnings`.
- [ ] All scene keyframes are generated via `generate_image` (`16:9` `cute-mystery` style), checked at 2x zoom, and imported with `--provider external --usd 0`.
- [ ] `zh-TW` TTS via Gemini `Sulafat` (`>= 4.4` chars/s bare speech rate) and 8 foreign dubs via MiniMax Speech pass `check-audio`, `qa` (11/11), and `package` (4/4), with all review gates pushed (`review-push`) and full workdir backed up to Google Drive (`AI/備份/AI劇/奇聞檔案局/H36/製作檔/`) and verified via `todrive.sh --check`.

## Steps

- [ ] Install channel branding package (`mokaair-brand-package-v4-endscreen`) and initialize per-episode `story-lexicon`.
- [ ] Research HTTP-200 historical sources, write `brief.md`, `claims.md`, `video.json`, `script.md`, pass `lint` (0 errors, 0 warnings), run independent `verify-1.md` fact-check and 2-reader blind `narrative` panel (`14/14 PASS`).
- [ ] Synthesize `zh-TW` narration via Gemini `Sulafat`, verify speech rate and `check-audio`, generate and inspect all `cute-mystery` scene keyframes via `generate_image`, and import them into the workdir.
- [ ] Generate background music, translate and independently review 8 locales (`en,ja,ko,es,pt,id,vi,th`), synthesize 8 dubs via MiniMax Speech (`--provider minimax`), assemble final video + localized packages, pass `qa` (11/11) and `package` (4/4), push review gates, and back up to Google Drive (`todrive.sh` + `--check`).

## How to verify

```bash
node tools/video/cli.mjs lint --slug curio-h36
node tools/video/cli.mjs qa --slug curio-h36
node tools/video/cli.mjs package --slug curio-h36
bash docs/videos/ai-drama-drive/todrive.sh --check curio-h36 "AI/備份/AI劇/奇聞檔案局/H36/製作檔"
npm run test:docs-videos && npm run check:tasks
```

## Notes

- Paired video tool token as `antigravity-curio`.
- Uses per-episode lexicon (`docs/videos/curio-h36/story-lexicon/`) so `docs/videos/lexicon.json` stays untouched.
