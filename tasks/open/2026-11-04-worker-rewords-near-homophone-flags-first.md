---
id: 2026-11-04-worker-rewords-near-homophone-flags-first
title: Worker rewords near-homophone flags first instead of spending retake rounds on them
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-tts-retakes
claimed_at: 2026-11-04T16:50:59Z
created_at: 2026-11-04T16:48:18Z
completed_at:
branch: claude/tender-einstein-ss8r5w
depends_on: []
scope:
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
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

- [x] `review/check-flags.json` carries `reword: [ids]`: the flagged zh lines whose every
      transcript (Gemini's, and the second transcriber's when it ran) reads the same as the
      script once tones are ignored. Leaked-word flags are never in it. Other locales: empty.
- [x] The worker's retake rounds redo only the flagged lines not in `reword`; when every
      flagged line is in `reword`, no retake round is spent and the lines go straight to the
      listener rewrite. The rewrite rounds still take every line still flagged.
- [x] `tts --redo review/check-flags.json` by hand still redoes every flagged line (the file's
      `flags` is unchanged), and `check-audio`'s output names the reword lines.
- [x] `automated.md` and `docs/videos/HANDS-OFF.md` §旁白 describe the order.

## Steps

- [x] `tts/check.mjs`: `tonelessReading`, `soundsAlikeTonelessly(heard, line, lexicon)`;
      write `reword` into the flags file; print it.
- [x] `automation/flow.mjs` `narration()`: filter the retake flags file; skip the loop when
      nothing is left to retake.
- [x] Tests: `tts/check.test.mjs` for the classification, a worker test for the order.
- [x] Docs.

## How to verify

```bash
node --test tools/video/tts/check.test.mjs tools/video/automation/automation.test.mjs
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
- 2026-11-04 (claude-opus-5.5-tts-retakes, claimed with `--force` on the owner's go-ahead):
  done on branch `claude/tender-einstein-ss8r5w`.
  - `tts/check.mjs`: `tonelessReading`, `soundsAlikeTonelessly`; `reword` is written only
    when non-empty, so every other flags file is byte-for-byte what it was.
  - `flow.mjs`: `retakeFlags(workdir, { rewordFirst })` writes `check-flags.retake.json`
    without the reword lines, or returns null (no retake round spent) when nothing is left.
    Pilot story slugs (`PILOT_SCRIPT_REFERENCES`) cannot be rewritten, so they retake all.
  - Limit found while testing: pinyin-pro reads 九行 as jiu háng, so 九行→就行 is not caught;
    j/q/x confusions (本機→本期) are deliberately not caught either.
  - The test of the order is in `automation.test.mjs` (`narrationGate` gained `reword`), not a
    new file: the harness is not exported.
  - `flow.mjs`, `automation.test.mjs`, `check.test.mjs` and `automated.md` are bound by the
    long-form duration receipt; rebound by an independent reviewer agent.
  - Dub retakes are unchanged.
- 2026-11-04 feasibility check: of the 80 single-phrase rows of the script-writing.md table,
  `soundsAlikeTonelessly` puts 25 under `reword` (擋→當, 怎麼搬→怎麼辦, 只多→至多, 推回→退回,
  …), 2 already pass `matchKind`, 55 still go to a retake first. All 25 read as true
  near-homophones. Resuming a stopped retake is unaffected: `retakeExplains` checks takes, not
  the flags file name. If a video's rewrite rounds are already spent, its reword lines are no
  longer retaken and wait for the owner; a retake would have been heard the same way anyway.
