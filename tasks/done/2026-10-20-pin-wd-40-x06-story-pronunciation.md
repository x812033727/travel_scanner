---
id: 2026-10-20-pin-wd-40-x06-story-pronunciation
title: Pin WD-40 X06 story pronunciation before local audio
status: done
priority: P1
area: docs
owner: codex-x06-lexicon
claimed_at: 2026-10-20T17:43:25Z
created_at: 2026-10-20T17:43:22Z
completed_at: 2026-10-20T17:46:10Z
branch: codex/brand-story-wd40-x06
depends_on: []
scope:
  - docs/videos/story-everyday-wd40-x06
---

# Pin WD-40 X06 story pronunciation before local audio

## Why

The X06 script and `video.json` were composed locally after the story had effectively
started. The paid speech gate therefore returns `STORY_LEXICON_MIGRATION_REQUIRED`:
there is no per-story pronunciation snapshot. This task pins the current shared
lexicon to the **unspoken** exact X06 draft before any Sulafat synthesis. It does
not authorize or run paid media.

## Definition of done

- [x] An independently reviewed, immutable story lexicon snapshot exists for the
      reviewed X06 `video.json` and `series.json` bytes.
- [x] The corresponding work-volume transaction is committed, strict read-back
      succeeds, and `tts --dry-run` lists the X06 requests without media charges.

## Steps

- [x] Confirm the exact script/source/blind receipt hashes, no X06 audio or
      timeline, no prior lexicon snapshot, and the current shared lexicon bytes.
- [x] Obtain independent root review of the manual bootstrap evidence and terms.
- [x] Publish the genesis snapshot and its audit artifact using the reviewed plan.
- [x] Run `lint`, strict lexicon read-back, TTS dry-run, and task validation.

## How to verify

From the X06 worktree, run `node tools/video/cli.mjs lint --slug
story-everyday-wd40-x06`, `npm run check:tasks`, and a paired
`tts --slug story-everyday-wd40-x06 --dry-run --workdir
/workspace/.brand-video-workdir` (with the paired home passed to `main`). Verify
`/workspace/.brand-video-workdir/story-everyday-wd40-x06` contains no audio
files after the dry run and the media ledger remains US$0.

## Notes

At 2026-10-20 17:44 UTC, `video.json` SHA-256 was
`4c9215b06364b3fb96cd9249054c6e7c15de381b4e8717a39a11fb9ad62bf1ba`,
`series.json` was `6f93b8b56662724200902260ea87f693faed0c21830587552698afbd2eeb3866`,
and the shared `docs/videos/lexicon.json` was
`95abdb67972cac70fe7c16b51faf4d94fe671e55aba9a1c3114fddb5a6cc613a`.
The source review and both blind reviews bind the X06 video SHA and PASS. No X06
directory exists in either local media work base. Built-in
`initializeStoryLexicon` refuses a started story with an existing `video.json`,
so the manual bootstrap follows the reviewed X05 format instead of invoking
the general migration command against an unproven worker workspace. The pure
plan seeds `WD-40`, `IN-ONE`, `Lava`, `Solvol`, `Spot`, and `Shot` as null terms;
version SHA is `3b4da9b2e82c5a69ca31c1f5af5832530bcf0cc02434c53da2b4458c606e9fc7`,
event SHA is `f1ce03e5ba8c2106d86fcdb54b4e5329ffe147ccc265798f69d7a0231f40f77c`.

`/root` independently rechecked and approved these exact preconditions before the
snapshot write, then performed a second read-back after the transaction. Committed
work-volume transaction ID is `8b2c20ac-2e8e-4177-bc74-198f934b6bc8`. Review
receipt SHA-256 is `3950abd2af30fac7796523feab8292418a8ef5cff68df818334aa82f8d013eaa`;
the manual bootstrap artifact SHA-256 is
`37a12b49f375371d8b845b2e52885475ab0b463ba18505ab3cb909b702ae2c75`.
Strict read-back returned snapshot mode, sequence 1 and the planned version/event
hashes. A pinned `tts --dry-run` returned 95 Sulafat requests and 2,337 billable
characters in the free tier. `lint` was 0 errors/0 warnings, `test:docs-videos`
236/236, and `check:tasks` exited 0 with existing queue warnings. The X06 work
volume contains only the lexicon transaction: no TTS audio, timeline or paid ledger.
Future media commands must use `--workdir /workspace/.brand-video-workdir`;
the paired token home remains `/workspace/.video-tool-home` and is never stored
in the repository.
