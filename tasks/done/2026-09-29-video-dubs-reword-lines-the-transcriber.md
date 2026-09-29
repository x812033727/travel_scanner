---
id: 2026-09-29-video-dubs-reword-lines-the-transcriber
title: Video dubs: reword lines the transcriber keeps mishearing instead of dropping the whole locale
status: done
priority: P1
area: tools
owner: claude-opus-5-5-dub-reword
claimed_at: 2026-09-29T11:43:36Z
created_at: 2026-09-29T11:41:51Z
completed_at: 2026-09-29T11:54:38Z
branch: claude/video-dub-reword
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/automation.test.mjs
  - .agents/skills/youtube-video/references/prompts/caption-translate.md
  - .claude/skills/youtube-video/references/prompts/caption-translate.md
  - docs/videos/AUTOMATION.md
---

# Video dubs: reword lines the transcriber keeps mishearing instead of dropping the whole locale

## Why

On 2026-09-29 the host worker gave up every dub it attempted: Academy en/ko, ENISA en/ja/ko,
GPT-6 en/ja (ja for Academy had no check file). Each locale costs 15–20 minutes of synthesis,
checks and two retakes, and the worker does one video at a time, oldest first, so the videos
behind wait while nothing comes out.

Each gave up over 1–5 lines of about 98, after both retakes. Most of those lines are homophones
or near-homophones that no retake can fix, because the voice says them right and the
transcriber hears the other word every time:

- ja 定価ではありません → heard 低下ではありません (both teika)
- en "Two: developers" → "to developers"; "your own bill" → "your own build"
- ko 두 표를 → 투표를; 계정 → 개정; 것 → 거
- ja 年で → 都市で／年収は; 行動2、→ コードに

The narration (zh-TW) already has the answer to this: lines still flagged after the retakes go to
the listener's rewrite pass and are reworded. Dubs have no such pass, so one misheard word drops
the whole locale's track.

A related case: ENISA en gave up with "the retake failed" because the retaken line no longer fit
its slide window (`dub --redo` exit 1); nothing tried to shorten it.

The check-audio second opinion (#968) does not help the worker: it runs only when
`VIDEO_SECOND_OPINION` is set, and the worker image has no Whisper.

## Definition of done

- [x] After the retakes, a dub's still-flagged lines go to the translator (variant `reword`) with
      what the transcriber heard; a reworded line that keeps every number, is non-empty, differs
      and stays within the window budget replaces the translation (captions follow), the dub is
      remade for those lines and checked again. Up to `MAX_DUB_REWORD_ROUNDS` rounds; only then is
      the locale given up, as today.
- [x] A retake whose line no longer fits its window gets the shortening pass instead of giving
      the locale up at once.
- [x] Tests in `automation.test.mjs` cover: reword clears the flag and the dub is made; a
      reword that changes a number is dropped; reword rounds exhausted gives up with the reason.
- [x] `docs/videos/AUTOMATION.md` and the skill's `caption-translate.md` describe the pass.

## Steps

- [x] `TRANSLATOR_REWORD` in prompts.mjs, registered as `translator:reword`.
- [x] `rewordDub` in flow.mjs, called from `makeDub` after the retake loop.
- [x] Tests, docs, `npm run test:tools`.

## How to verify

`node --test tools/video/automation/automation.test.mjs`; after deploy, the worker log shows
`<locale> dub made after … reword` for a video whose lines were flagged.

## Notes

- Evidence: `review/check.<locale>.json` and `check-flags.<locale>.json` in each workdir under
  `/var/lib/mokaair/video-work/` on the host (read-only diagnosis, 2026-09-29 11:35Z).
- Claimed with `--force`: the overlapping claims (`2026-09-26-video-dubs-worker`,
  `2026-09-27-video-languages-skill-docs`, `2026-09-27-video-drama-room-skill-docs`,
  `2026-09-28-sothatswhy-shorts-from-episode`) were all stale, a day or more old. Open PR #983
  also edits flow.mjs and prompts.mjs; the only shared line is `VARIANT_INSTRUCTIONS`, a one-line
  conflict for whichever merges second.
- Retakes are not reset after a rewording round: a reworded line gets one `dub` and one check,
  and if it is still flagged the next rewording round (or the give-up) follows. Retakes cannot fix
  a homophone, and every retake round re-checks the track.
- `dub` (without `--redo`) keeps a retaken clip because its cache key is the line's text, so the
  pass after a rewording synthesizes only the changed lines.
- Budget: `max_chars` from a fresh captions sheet, never less than the line's current length.
- Not done here: a Whisper second opinion on the worker (#968's `VIDEO_SECOND_OPINION`) would
  clear some lines without changing words; the image has no Whisper.
