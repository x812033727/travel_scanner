---
id: 2026-10-15-dub-check-flags-a-line-whose
title: Dub check flags a line whose transcript opens with a leaked word (thought)
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-15T04:05:37Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/check.test.mjs
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

- [ ] `check-audio` flags any line whose transcript starts with a word that is not in the script
      line's first words, at least the known leak `thought` (case-insensitive, glued or followed by
      a newline), whatever Jev says, with a note naming the leak.
- [ ] A flagged leak goes into `check-flags.<locale>.json` so `dub --redo` re-records it.
- [ ] Tests cover a glued leak, a newline leak and a line that really starts with "Thought".

## Notes

- Seen only in English so far (three lines across H05/H06 in two rounds, none in ja/ko).
- How it was cleared by hand: a one-id flags file (copy of check-flags.en.json with `flags` set to
  the id) passed to `dub --redo <file> --keep-fitting`, then `check-audio` again.
