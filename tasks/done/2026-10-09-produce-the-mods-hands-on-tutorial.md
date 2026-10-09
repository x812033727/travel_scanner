---
id: 2026-10-09-produce-the-mods-hands-on-tutorial
title: Produce the Mods hands-on tutorial under the content-value rules
status: done
priority: P1
area: docs
owner: claude-opus-5-5-video-reference-comparison
claimed_at: 2026-10-09T03:52:00Z
created_at: 2026-10-09T03:51:51Z
completed_at: 2026-10-09T05:23:49Z
branch: claude/mods-hands-on-video
depends_on: []
scope:
  - docs/videos/claude-code-mods-hands-on
  - docs/videos/lexicon.json
  - tools/docs-videos-tests.test.mjs
---

# Produce the Mods hands-on tutorial under the content-value rules

## Why

The owner rejected `claude-code-mods-no-sandbox-before-install` on 2026-10-09 for teaching
nothing, set the content-value rules (PR 1392), and asked for that video to be made again with
them. This is that video, under a new slug so the paused original and the rewrite package kept
under the old slug are not overwritten. It is also the first use of the rules.

## Definition of done

- [x] A brief written by a planner that was given the rules and the run evidence, not an
  earlier draft; outline A chosen as the owner delegated.
- [x] Two mods written for the video, validated, tested, and run in headless sessions; the logs
  kept beside them with no home directory's owner in any path.
- [x] `video.json` and `claims.md` by a writer; `lint` 0 errors, 0 warnings.
- [x] An independent fact check (`verify-1.md`) and a second round (`verify-2.md`).
- [x] Narration, the cut, and the final review pushed to `/admin/videos`.
- [x] The upload package at the publish gate. Uploading to YouTube is the owner's.

## Steps

- [x] Plan, run the 「要先實作」 items that a headless session can answer, write.
- [x] Verify, then `tts`, `check-audio`, `render`, `assemble`, `captions`, `review-push --gate final`.
- [x] `package`, `review-push --gate publish`; languages: zh-TW only (the owner, in chat).

## How to verify

```bash
node tools/video/cli.mjs lint --slug claude-code-mods-hands-on
node tools/video/cli.mjs status --slug claude-code-mods-hands-on
```

`docs/videos/claude-code-mods-hands-on/runlog-2.txt` holds every run a card quotes.

## Notes

- Observed in a session, headless (`claude -p --plugin-dir`, Claude Code 2.1.295): the same
  request with and without pipe-guard (the tool result goes from no error to `Exit code 1`), the
  same in auto permission mode, `/plink` answering, and the count reading 0 after `-c`.
- Never observed, and so not shown or told as seen: the status line, the toast, the `/plugin`
  screen, the hot-reload question, a 31st refusal in a live session. An interactive session is
  needed for those.
- The validator's two error messages on 2.1.295 differ from the examples on the official page.
- `handwritten-sample.md` is the first hand-written sample the owner read before the rules were
  written; `video.json` supersedes it.
- What the planner and the writer found unclear in the rules: `2026-10-09-fix-what-the-first-use-of`.
- CI first failed on two repository rules. `tools/docs-videos-tests.test.mjs` wants every test under docs/videos run by `npm run test:docs-videos`; a mod's `*.test.ts` runs only under `claude plugin test`, so tests under a `mods` folder are now named there as a second kind that is never selected. `tools/repo-hygiene.test.mjs` reads a name after `plink -load` as a host detail; the mod's test commands use `<saved-session>`.
- Produced on 2026-10-09, outside the repo as always. Narration 13:53 (three audio checks: 13
  lines flagged, 9 reworded and all 13 re-recorded; 3 still flagged and reworded; then none; the
  rewrites are `narration-rewrites-1.json` and `-2.json`). Cut 14:01, 127 slide states, zh-TW
  captions only (the owner's choice).
- Gates on `/admin/videos`, each approved by the server: audio, final (11 of 11 checks; the
  judge's demonstration score 0.90, where the rejected video had 0.45 against 0.6), publish
  (4 of 4). Landed as PR 1394.
- Left for the owner: upload `final.mp4` in Studio as private and paste the address on the
  video's page; the language panel may still want its 「只出繁體中文」 pressed.
- Not done: the brief's first-use trial by someone who took no part in the writing.
