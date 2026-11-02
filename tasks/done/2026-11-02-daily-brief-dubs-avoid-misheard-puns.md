---
id: 2026-11-02-daily-brief-dubs-avoid-misheard-puns
title: Daily brief dubs: avoid misheard puns, keep ja under budget, Whisper in session runs
status: done
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-02T13:39:29Z
completed_at: 2026-11-02T15:32:12Z
branch:
depends_on: []
scope:
  - .agents/skills/youtube-video/references/daily-brief.md
---

# Daily brief dubs: avoid misheard puns, keep ja under budget, Whisper in session runs

## Why

The owner now has the daily AI brief made by a scheduled Claude Code cloud session (weekdays 09:00
Taipei, all eight dubs before upload), not the host worker. The first session-made episode,
`daily-ai-20261101`, had its eight dub tracks flagged 53 times on the first listen (en 6, es 4, pt 5,
id 6, vi 6, th 8, ko 10, ja 12), and 21 lines were still flagged after one retake round. Reading the
flags showed three causes:

1. **No second transcriber in the session.** The host sets `VIDEO_SECOND_OPINION` (Whisper medium,
   `docs/videos/DUBS.md`), a cloud session does not, so every Gemini mishearing stood: brake heard as
   break, Thai บิล (bill) as บิน (fly), Portuguese Taiwan as Caiobá.
2. **The script invited mishearing.** A pun (en `wtmi`: "Your bill has a brake now; someone's braking
   on AI money too") was garbled twice. "Gemma 4" lost its 4 in zh, id, th, ko and ja.
3. **Japanese ran tight.** 40 of 72 windows had to be sped up, to at most 1.21×, and three lines did
   not fit at all until they were shortened by hand.

## Definition of done

- [x] `daily-brief.md` tells a session-made brief to install Whisper (`python3 -m venv ~/whisper &&
      ~/whisper/bin/pip install faster-whisper`, `WHISPER_MODEL=medium`) and to set
      `VIDEO_SECOND_OPINION` before the first `check-audio`.
- [x] Its writing rules say: no puns or homophone wordplay in the narration, and a model name
      ending in a digit is said so the digit is clearly heard.
- [x] The translator brief for ja (and ko) aims at about 85% of each line's `max_chars`, so that
      most windows need no speed-up.

## Steps

- [x] Add the three rules to `.agents/skills/youtube-video/references/daily-brief.md` (§四 or a new
      section for session-made episodes).
- [ ] Note the results of the next session-made episode in this file.

## How to verify

On the next session-made brief, count the first-listen flags per locale and the ja speed-ups in
`dubs/ja/fit.json` and compare with the figures above.

## Notes

- 2026-11-02: the three rules are in `daily-brief.md` §三 (旁白與配音的規矩), written together with the switch to the Tech Signal podcast format. Comparing the next episode's first-listen flags is left to the weekly review in §五.

- The host worker's daily brief was switched off by the owner on 2026-11-02 (`daily_brief_enabled`).
- In a session, a wait loop using `pgrep -f "<pattern>"` matches its own shell and never ends. Wait
  on the background task's notification instead.
- A line the TTS garbled into a much longer take (id `5qw9` came back 72 s long) shows up in
  `dubs/<locale>/fit.json` under `over`. Retaking it with `dub --redo` fixes it; shortening the
  translation does not.
