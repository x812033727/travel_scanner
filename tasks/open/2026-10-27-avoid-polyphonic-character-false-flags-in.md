---
id: 2026-10-27-avoid-polyphonic-character-false-flags-in
title: Avoid polyphonic-character false flags in Mandarin audio comparison
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-10-27T09:46:03Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
---

# Avoid polyphonic-character false flags in Mandarin audio comparison

## Why

Curio S31 v2 retains two official narration flags even though whole, SHA-bound independent transcripts contain the intended sounds. The offline `reading()` comparison defaults 吳曾 to `wu2 ceng2`, while the historical author's name is Wu Zeng and Whisper wrote 無憎 (`wu2 zeng1`). It also defaults 麗芝 to `li2 zhi1`, whereas 荔枝 and the usual 麗 reading are `li4 zhi1`; the simplified control 丽芝 already matches. Jev's original low scores and actual transcripts remain intact in `docs/videos/curio-s31-v2/audio-qa-listener-rw1-official.json`.

The comparator should not force producers to purchase repeated unchanged narration or alter correct caption spelling merely because a polyphonic character's default differs. A fix must remain bounded and avoid accepting a real tone/word error.

## Definition of done

- [ ] Correct same-sound Mandarin variants can be compared without globally changing pinyin behavior or accepting arbitrary alternate tones.
- [ ] The real tone difference 荔枝 (`li4 zhi1`) versus 立志 (`li4 zhi4`) remains a doubt; ASR evidence and Jev scores are never rewritten.
- [ ] Existing wrong-word, leaked-word, non-Chinese and pronunciation-dictionary safeguards retain their behavior.

## Steps

- [ ] Reproduce the four current readings plus simplified-character controls using pure offline fixtures.
- [ ] Design a narrow contextual/polyphonic comparison and add positive and negative regression cases before any shared change.

## How to verify

Run `node --test tools/video/tts/check.test.mjs` and relevant tools checks with the supported bundled runtime. Use fixture transcripts only, with zero paid requests and no modification of existing production caches or approvals.

## Notes

- Filed as an unclaimed follow-up; the episode task does not change shared tools, the lexicon, cached ASR or official flags.
- `matchKind()` currently returns null for both examples. Adding a complete episode-local `.say` with 吳增 proves a pure-memory sound match against 無憎, but changes a production speech key and would require new synthesis; it was a diagnostic, not an adopted audio fix.
- The existing shared lexicon accepts Latin-start terms, so adding Chinese proper names there is not an appropriate workaround. Do not weaken all Mandarin tone comparisons or use global `customPinyin()` state.
