---
id: 2026-11-04-worker-rewords-near-homophone-flags-first
title: Worker rewords near-homophone flags first instead of spending retake rounds on them
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-04T16:48:18Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/reword-first.test.mjs
  - .agents/skills/youtube-video/references/automated.md
  - docs/videos/HANDS-OFF.md
---

# Worker rewords near-homophone flags first instead of spending retake rounds on them

## Why

When `check-audio` flags lines, the host worker (`tools/video/automation/flow.mjs`
`narration()`) first spends up to `max_retake_rounds` (drama default 2) on `tts --redo` of the
same text, and only then hands the still-flagged lines to the listener rewrite
(`prompts/listener-rewrite.md`, `MAX_REWRITE_ROUNDS`). For a line the transcriber hears as a
near-homophone — the voice said it right and the transcript only differs in tone
(擋呼叫→當呼叫, 九行→就行, 沒有量→沒有亮) — a retake is the same sound again: it is paid TTS
plus a full Jev round that cannot change the outcome. `script-writing.md` says it outright:
被標記的句子只重錄通常沒用，同音字會再被聽成一樣. Exact same-tone homophones are already
cleared locally by `matchKind(...) === "sound"`; the toneless case is the gap.

## Definition of done

- [ ] `review/check-flags.json` carries `reword: [ids]`: the flagged zh lines whose every
      transcript (Gemini's, and the second transcriber's when it ran) reads the same as the
      script once tones are ignored. Leaked-word flags are never in it. Other locales: empty.
- [ ] The worker's retake rounds redo only the flagged lines not in `reword`; when every
      flagged line is in `reword`, no retake round is spent and the lines go straight to the
      listener rewrite. The rewrite rounds still take every line still flagged.
- [ ] `tts --redo review/check-flags.json` by hand still redoes every flagged line (the file's
      `flags` is unchanged), and `check-audio`'s output names the reword lines.
- [ ] `automated.md` and `docs/videos/HANDS-OFF.md` §旁白 describe the order.

## Steps

- [ ] `tts/check.mjs`: `tonelessReading`, `soundsAlikeTonelessly(heard, line, lexicon)`;
      write `reword` into the flags file; print it.
- [ ] `automation/flow.mjs` `narration()`: filter the retake flags file; skip the loop when
      nothing is left to retake.
- [ ] Tests: `tts/check.test.mjs` for the classification, a worker test for the order.
- [ ] Docs.

## How to verify

```bash
node --test tools/video/tts/check.test.mjs tools/video/automation/reword-first.test.mjs
npm run test:tools
```

## Notes

- Filed from the 2026-11-04 cost conversation. Sister task:
  `2026-11-04-narration-lint-warns-known-mishearings` (stops the words before they are said).
- Kept deliberately narrow: only a whole-line toneless match counts. Wider confusions
  (j/q/x, 本機→本期, 實跑→食譜) stay on the retake path; widen only with measured data from
  `review/check.json` of finished videos.
- Overlap: `2026-10-09-dub-skipped-because-jev-still-hears` also touches `tts/check.mjs`; read
  its notes before changing the dub path. This task does not change dub retakes.
- Claim was refused on 2026-11-04: `flow.mjs`, `check.mjs`, `automated.md` and `HANDS-OFF.md`
  are in the scope of many in-progress tasks, all stale (>24 h) except
  `2026-11-04-curio-and-sothatswhy-stop-burning-subtitles`, which is in `review` and whose PR
  (#2011) is already merged. Taking it needs `claim --force`, which the session's permission
  mode did not allow without the owner's go-ahead.
