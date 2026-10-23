---
id: 2026-10-15-dub-check-flags-a-line-whose
title: Dub check flags a line whose transcript opens with a leaked word (thought)
status: done
priority: P2
area: tools
owner: claude-opus-5-5-pr-tidy
claimed_at: 2026-10-16T13:44:13Z
created_at: 2026-10-15T04:05:37Z
completed_at: 2026-10-16T13:51:43Z
branch: claude/youthful-brahmagupta-1giys7
depends_on: []
scope:
  - tools/video/tts/check.mjs
  - tools/video/tts/check-leak.test.mjs
---

# Dub check flags a line whose transcript opens with a leaked word (thought)

## Why

On 2026-10-15 the English dubs of 奇聞檔案局 H05 and H06 had lines whose audio opens with the
spoken word "thought" before the sentence: Gemini TTS reading a stray token aloud. The server
transcript showed it (`"heard": "thoughtIt proves the ransom, not the man."`,
`"thought
Researchers did not name the children by sight alone."`), yet `check-audio` passed one
of them (H05 h5v109: Jev judged it fine) and the other survived both `dub --redo` rounds. A viewer
hears it. They were found only by scanning `review/check.en.json` by hand, and each took one more
targeted redo to clear.

## Definition of done

- [x] `check-audio` flags any line whose transcript starts with a word that is not in the script
      line's first words, at least the known leak `thought` (case-insensitive, glued or followed by
      a newline), whatever Jev says, with a note naming the leak.
- [x] A flagged leak goes into `check-flags.<locale>.json` so `dub --redo` re-records it.
- [x] Tests cover a glued leak, a newline leak and a line that really starts with "Thought".

## Notes

- Seen only in English so far (three lines across H05/H06 in two rounds, none in ja/ko).
- How it was cleared by hand: a one-id flags file (copy of check-flags.en.json with `flags` set to
  the id) passed to `dub --redo <file> --keep-fitting`, then `check-audio` again.

### 2026-10-16 fix (claude-opus-5-5-pr-tidy)

`tools/video/tts/check.mjs` adds `LEAKED_WORDS` (`["thought"]`) and `leakedWord(heard, line)`.
A transcript counts as a leak when it opens with one of those words, case-insensitive, and the
next character is nothing, whitespace, punctuation or a capital letter (glued: `thoughtIt`). The
script line's own first word, past any opening quote, must not be that word.

`check-audio` flags every leaked line whatever Jev or a second transcript says. The flags file
note reads `leaked word 「thought」 before the line (Jev 0.95): heard 「…」`. The summary line adds
`N of them for a leaked word`, and the `check-audio` run in `state.json` records `leaked: N`.
Leaked lines Jev passed are no longer counted as "judged fine", and a second transcript cannot
clear one.

The rule stays a list of known leaks, not "any first word not in the script". A plain transcript
difference at the start of a line is still Jev's to judge, so the check does not double-flag
every mishearing.

Scope changed from `check.test.mjs` to `check.mjs` plus a new
`tools/video/tts/check-leak.test.mjs`. `check.test.mjs` is bound by the long-form duration review
(`REVIEW_FILES`), and a new test file needs no receipt, as #1513 did. `check.mjs` is not bound.

Ran: `node --test tools/video/tts/check-leak.test.mjs` (3/3: glued, newline, punctuation and
leading-space leaks; a line that really starts with "Thought", one in quotes, and "Thoughtful"
are not leaks; an English dub where Jev passes both leaked lines still flags them in line order),
`check.test.mjs` plus `dubs/*.test.mjs` (56/56), `npm run test:tools` (2377/2377), and
`tools/video/long-form/cli.mjs check` (PASS).
