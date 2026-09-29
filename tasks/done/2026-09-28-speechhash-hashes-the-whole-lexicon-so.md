---
id: 2026-09-28-speechhash-hashes-the-whole-lexicon-so
title: speechHash hashes the whole lexicon, so a term added for one video marks every video's narration stale
status: done
priority: P3
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-29T02:58:51Z
created_at: 2026-09-28T15:00:53Z
completed_at: 2026-09-29T03:02:11Z
branch:
depends_on: []
scope:
  - tools/video/core
  - tools/video/tts/requests.mjs
  - docs/videos/DESIGN.md
  - docs/videos/SERIES.md
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

- [x] Adding a lexicon term that no line of a video uses leaves that video's `speech_hash`
      unchanged; adding one that a line uses changes it.
- [x] Existing timelines built with the old hash are handled deliberately (accepted once, or
      the change documented with the one-time `tts` re-run it needs); `docs/videos/DESIGN.md`
      and `SERIES.md` describe the new rule.

## Steps

- [x] Hash each line's spoken parts (what the clip key already uses) instead of the whole
      `lexicon.terms`, or hash only the terms that some line's spoken text matches.
- [x] Decide how old timelines are treated: a second accepted hash, or a note that every
      in-progress video needs one free `tts` re-run (and the audio approval again).
- [x] Tests in `tools/video` for both cases above.

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs status --slug <slug> --workdir <VIDEO_WORKDIR>   # before and after adding an unrelated term
```

## Notes

- The host worker's in-progress videos go stale the same way whenever a term is merged into
  its copy of the dictionary, so an automated video between the audio and final gates can
  stall on "run tts first".
- 2026-09-29 (claude-opus-5-5): done. `speechHash` now hashes `termsUsed(...)`, which is the dictionary
  entries the script's spoken lines use. They are matched by `termPattern`, which `spokenParts` now
  shares, so the hash and the speech request apply the same rule: whole words, longest term first.
  Old timelines are accepted once rather than kept valid. Keeping them valid would have meant
  accepting a legacy hash at every comparison (about twenty call sites, several of them manifests),
  and it would only help a video whose dictionary had not changed since its last `tts`. So every
  timeline from before this change reads as stale once. `tts` re-records nothing (checked:
  `openai-agents-broke-in` 0 of 28 requests, `rtx-spark-local-ai` 0 of 36) and rewrites
  `timeline.json`, whose hash the audio approval is bound to. A video between the audio and final
  gates therefore needs its audio approved again; Jev does that on its own when `check-audio` is
  clean. Season videos 1, 2, 3, 5 and 6 are packaged, and nothing needs redoing for them. Out of
  93 dictionary terms, video 1 uses 4 and video 5 uses 12.
