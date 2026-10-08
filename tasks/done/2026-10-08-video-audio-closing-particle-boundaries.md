---
id: 2026-10-08-video-audio-closing-particle-boundaries
title: Mandarin closing particles at clause boundaries
status: done
priority: P1
area: tools
owner: codex-video-audio-matcher
claimed_at: 2026-10-08T07:38:25Z
created_at: 2026-10-08T07:37:48Z
completed_at: 2026-10-08T07:46:25Z
branch: codex/stalled-videos-completion-20261008
depends_on: []
scope:
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
---

# Mandarin closing particles at clause boundaries

## Why

Mandarin narration legitimately adds a closing 耶 before a comma. The audio matcher
removed punctuation before its end-only particle rule, so two agreeing transcripts
of line tgby were flagged despite matching the spoken words and tones.

## Definition of done

- [x] Both independently cached tgby transcripts match as same sound without a new provider request.
- [x] Intended words and meaningful numeral, negation and noun differences stay significant.
- [x] Existing raw/end-only candidates and non-Chinese behavior remain unchanged.
- [x] Targeted regressions pass; the unchanged full-test Windows filesystem limitation is recorded.
- [x] Independent duration receipt review and parent commit are complete.

## Steps

- [x] Check current claims, active worktrees and open PRs for scope conflicts.
- [x] Reproduce the real tgby failure against the previous matcher.
- [x] Add a heard-only particle candidate while punctuation boundaries still exist.
- [x] Verify real existing transcripts offline and reject meaningful changes.

## How to verify

Using the bundled Node 24 runtime:

`node --test --test-name-pattern='comparison|same-sound|Taiwanese particles|closing particles|outside Chinese|zh-CN keeps' tools/video/tts/check.test.mjs`

`node tools/tasks.mjs check` and `git diff --check`.

## Notes

- No active claim or open PR touched check.mjs at the ownership check.
- The new real-transcript regression failed on the original matcher (exit 1), then
  all six selected matcher tests passed on the correction (exit 0). Tests cover
  Chinese/ASCII punctuation, added particles after intended 氣餒/好耶, missing
  intended characters, unexpected leading/interior 耶, numeral/negation/noun
  changes, Simplified Chinese, and unchanged en/ja/ko behavior.
- Full check.test.mjs ran twice; mock speech-journal writes encountered Windows
  EPERM atomic rename failures. The first run passed 21 of 23 tests, with no
  matcher assertion failures. Do not change paths.mjs under this scope; that
  separate filesystem fix is already in PR #1379.
- Existing remaining6-after-fresh8.json was evaluated entirely offline: only
  tgby changes from null to sound in both primary and secondary transcripts.
  htb5, ew6e, kr2g, yqpn and bc5q remain null in both. No cache, flags, audio
  approval, provider call or production file was changed by this code task.
- Logs and offline result: C:/Users/x8120/mokaair-work/stalled-video-completion-20261008/embedding-audio/particle-*.log and particle-offline-recheck.json.
- Independent review caught a new semantic false pass when lexical 氣餒 or
  好耶 appeared before a comma. New negative tests reproduced it (exit 1), then
  the candidate was narrowed to retain 氣餒/气馁 and 好耶 while allowing a
  further added particle in 氣餒耶/好耶餒. All six focused tests still pass and
  the offline six-flag outcomes are unchanged. Parent and independent peer are
  reviewing the revised source. Duration receipt changes remain reserved for
  an independent reviewer. No commit has been made by the implementation subagent.

- Parent review completed after the lexical correction: source commit eccafa3c7;
  independent duration receipt b9940f18c, baseline 52cfd7eea. All108 baseline
  bindings matched raw Git blobs; only check.test.mjs was rebound. Six matcher
  regressions, eight duration/review regressions and all473 duration plans pass.
  A separate peer confirmed the real six-line outcomes without provider calls.
