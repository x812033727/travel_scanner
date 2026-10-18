---
id: 2026-10-09-produce-the-settings-hooks-hands-on
title: Produce the settings-hooks hands-on tutorial under the content-value rules
status: done
priority: P1
area: docs
owner: claude-opus-5-5-video-reference-comparison
claimed_at: 2026-10-09T10:01:30Z
created_at: 2026-10-09T10:01:12Z
completed_at: 2026-10-09T13:27:30Z
branch: claude/hooks-hands-on-video
depends_on: []
scope:
  - docs/videos/claude-code-hooks-hands-on
  - docs/videos/lexicon.json
---

# Produce the settings-hooks hands-on tutorial under the content-value rules

## Why

The Mods tutorial told its viewer to reach for a settings hook first and did not teach how. The
owner chose this topic for the next video made by hand under the content-value rules, in the
order the rules had not yet been used in: plan, run, write.

## Definition of done

- [x] A brief by a planner who had the rules and no run evidence; its 「要先實作」 list made the
  runs mechanical. Outline A chosen as the owner delegated.
- [x] The listed runs made and logged: model-free checks of both hook scripts, the Windows
  portability checks, and eight headless sessions. All matched what the brief expected.
- [x] `video.json` and `claims.md` by a writer; `lint` 0 errors, 0 warnings.
- [x] Two independent fact checks (`verify-1.md`, `verify-2.md`).
- [x] Narration, the cut, and the audio, final and publish gates on `/admin/videos`.
- [ ] Uploading to YouTube, which is the owner's.

## Steps

- [x] Plan, run, write, verify twice.
- [x] `tts`, three audio checks, `render`, `assemble`, `captions`, `review-push --gate final`.
- [x] `package`, `review-push --gate publish`; languages: zh-TW only (the owner, in chat).

## How to verify

```bash
node tools/video/cli.mjs lint --slug claude-code-hooks-hands-on
node tools/video/cli.mjs status --slug claude-code-hooks-hands-on
```

`docs/videos/claude-code-hooks-hands-on/runlog.txt` holds every run a card quotes, and `demo/`
the practice project and its settings variants as they were used.

## Notes

- Produced on 2026-10-09 with Claude Code 2.1.295 on Windows. Narration 14:01 after three audio
  checks (19 lines flagged, all reworded and re-recorded; 3 more reworded; then none; the
  records are `narration-rewrites-1.json` and `-2.json`). Cut 14:09, 124 slide states, zh-TW
  captions only.
- Gates, each approved by the server: audio; final, 11 of 11 with the judge's demonstration
  score at 0.95; publish, 4 of 4. The first final submission failed its captions check because
  the zh-TW-only choice had not been written to `languages.json` yet; it passed once it was.
- What only the runs showed, and the video now teaches: a Stop hook does fire in a headless
  session and sends Claude back; "hook error" is the wording of a successful block; exit code 1
  lets the edit through, and Claude then rewrote the test to expect the wrong answer; the
  stream's `outcome` reads `error` for exit codes 2 and 1 alike; a permission rule's refusal
  carries no reason of the owner's.
- Never observed, and not shown or told as seen: any interactive screen, the hook's stdin in a
  session, macOS or Linux, a second stop let through with the tests still red in a session.
- `--allowedTools "Read,Edit,Write"` did not remove Bash in these sessions; one read-only Bash
  command ran in the throwaway project. The video does not claim the flag limits the tools.
- The title card and the thumbnail first said 「不准收工」; the gate sends Claude back once a turn,
  so both now say 「先擋回去」, as do the closing card, the description and the title.
- 22 cards use the `source` line added in PR 1396; this was its first render.
- The demo's test is red on purpose, so the project sits in a folder named `demo`.
- Words the audio check mishears, beyond the Mods tutorial's list: 餵, 印出, 放行, 無介面, 那一欄.
