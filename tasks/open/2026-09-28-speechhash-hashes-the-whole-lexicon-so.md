---
id: 2026-09-28-speechhash-hashes-the-whole-lexicon-so
title: speechHash hashes the whole lexicon, so a term added for one video marks every video's narration stale
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-29T02:58:51Z
created_at: 2026-09-28T15:00:53Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core
---

# speechHash hashes the whole lexicon, so a term added for one video marks every video's narration stale

## Why

`speechHash(doc, lexicon)` in `tools/video/core/timeline.mjs` feeds the whole of
`lexicon.terms` into the hash that `timeline.json` carries as `speech_hash`. The dictionary is
one file shared by every video (`docs/videos/lexicon.json`), so adding a term for one video
changes the hash of every other video, even when none of their lines contains the term.
`status`, `qa` (`narration`), `render`, `assemble`, `clips` and `music` then call those
timelines stale and ask for `tts` again.

Seen on 2026-09-28: the writers of the season's videos 5 and 6 added terms, and videos 1–4
(already narrated, and 1–3 packaged and approved) went to "narration synthesized: timeline.json
was built for an older script" with every dub track "stale". `tts --dry-run` showed 0 lines to
synthesize for all four, because the clip keys in `tools/video/tts/requests.mjs` already use
only each line's own spoken parts (`spokenParts(spokenText(line), lexicon)`). Re-running `tts`
would be free but rewrites `timeline.json`, and the audio approval is bound to that file's
hash, so a finished video would need its audio approved again for no change in sound.
`docs/videos/SERIES.md` already warns about this for dramas ("之後才加詞會讓進行中的集重錄旁白").

## Definition of done

- [ ] Adding a lexicon term that no line of a video uses leaves that video's `speech_hash`
      unchanged; adding one that a line uses changes it.
- [ ] Existing timelines built with the old hash are handled deliberately (accepted once, or
      the change documented with the one-time `tts` re-run it needs); `docs/videos/DESIGN.md`
      and `SERIES.md` describe the new rule.

## Steps

- [ ] Hash each line's spoken parts (what the clip key already uses) instead of the whole
      `lexicon.terms`, or hash only the terms that some line's spoken text matches.
- [ ] Decide how old timelines are treated: a second accepted hash, or a note that every
      in-progress video needs one free `tts` re-run (and the audio approval again).
- [ ] Tests in `tools/video` for both cases above.

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs status --slug <slug> --workdir <VIDEO_WORKDIR>   # before and after adding an unrelated term
```

## Notes

- The host worker's in-progress videos go stale the same way whenever a term is merged into
  its copy of the dictionary, so an automated video between the audio and final gates can
  stall on "run tts first".
