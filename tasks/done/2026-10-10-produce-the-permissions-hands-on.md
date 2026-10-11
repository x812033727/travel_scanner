---
id: 2026-10-10-produce-the-permissions-hands-on
title: Produce the permission-rules hands-on tutorial under the content-value rules
status: done
priority: P1
area: docs
owner: claude-opus-5-5-video-reference-comparison
claimed_at: 2026-10-10T07:25:58Z
created_at: 2026-10-10T07:25:55Z
completed_at: 2026-10-10T11:12:45Z
branch: claude/permissions-hands-on-video
depends_on: []
scope:
  - docs/videos/claude-code-permissions-hands-on
  - docs/videos/lexicon.json
  - docs/videos/claude-code-headless-hands-on/video.json
  - docs/videos/claude-code-claude-md-hands-on/video.json
  - docs/videos/claude-code-skills-hands-on/video.json
  - docs/videos/claude-code-subagents-hands-on/video.json
  - docs/videos/claude-code-mcp-hands-on/video.json
---

# Produce the permission-rules hands-on tutorial under the content-value rules

## Why

The owner asked to keep making AI tutorials. Several earlier ones ended on the same sentence, a
rule that must hold every time belongs in a permission rule or a hook and not in CLAUDE.md, and
the MCP one showed a call refused for lack of an allow rule. This is the tutorial those pointed
at: writing allow, ask and deny rules in a project's settings, and checking that each rule
matches what its author thinks it matches. Same order as the last six: plan, run, write. It goes
as far as the publish gate on `/admin/videos`; uploading stays the owner's.

The five `video.json` files of earlier tutorials are in scope for one field each: their
thumbnails (see Notes).

## Definition of done

- [x] A brief by a planner with the rules and no run evidence; outline A, as the owner delegated.
- [x] The listed runs made and logged: twelve headless sessions and the model-free checks.
- [x] `video.json` and `claims.md` by a writer; `lint` 0 errors, 0 warnings; the layout check run
  before narration.
- [x] Two independent fact checks (`verify-1.md`, `verify-2.md`), their findings applied.
- [x] Narration synthesized and checked until no line was flagged; the audio gate approved it.
- [x] Its files in the repository.
- [x] The thumbnails of five earlier tutorials given a subject; their packages rebuilt.
- [x] The cut, and the final and publish gates: an 11:09 cut, final 11 of 11, publish 4 of 4; the
  package is in the work directory's `upload/`.
- [ ] Uploading to YouTube, which is the owner's.

## Steps

- [x] Plan, run, write, verify twice, narrate.
- [x] `render`, `assemble`, `captions`, `review-push --gate final`, `package`,
  `review-push --gate publish`; languages: zh-TW only (the owner, in chat).

## How to verify

```bash
node tools/video/cli.mjs lint --slug claude-code-permissions-hands-on
node tools/video/cli.mjs status --slug claude-code-permissions-hands-on
```

`docs/videos/claude-code-permissions-hands-on/runlog.txt` holds every run a card quotes, with
each session's tool calls and their outcome, and `demo/` the practice project, each rules file
and the scripts.

## Notes

- Produced on 2026-10-10 with Claude Code 2.1.295 on Windows, Git Bash; twelve sessions on
  sonnet, none with `--force`. This is the first of these tutorials whose sessions were offered
  Bash. The project lived in a temporary folder outside any repository; its "deploy script" only
  appends a line to a file inside the project and its `.env` holds plainly fake values; every
  arm passed `--permission-mode default` and none used a mode that skips permission checks; no
  rules file allows bare Bash. After every session the folder above the project was compared by
  name and hash and every Bash command the model issued was read: nothing outside the project
  changed and no command, run or refused, pointed outside it, used the network or installed
  anything. The sandbox was not used; the official page says it does not run on native Windows.
- What only the runs showed: without rules the model did not read the secrets file or run the
  deploy; it stopped when its first edit was refused, so the difference between the arms is that
  routine work got done (fixed and tested 3 of 3 against 0 of 3), not that secrets leaked.
  With the rules file, the deploy and the read of `.env` were each sent three times and blocked
  by a deny rule three times, and the model tried no other route afterwards.
- Where a rule did not reach, one run each, every one a command the request named line by line:
  `bash scripts/../scripts/deploy.sh` ran past the deny on the deploy script; `grep -r` printed
  the denied file's content; a project script wrote into the denied folder. The official page
  lists the last two as things Read rules do not cover and says a Bash rule is not a security
  boundary; the video says so and does not say the model found a way round.
- A refusal by a deny rule and an ask nobody could answer look alike in the result line's
  `permission_denials`; the tool result's text and the hook record tell them apart, and a file
  tool blocked by a deny rule leaves no hook line at all. A deny on reading a file also removed
  it from the file listing, and once the model answered that the project had no such file.
- Project-file allow rules are ignored under `-p` in an untrusted folder, with a warning on
  stderr; the same rules passed by flag, or placed in `settings.local.json`, took effect.
- The first fact check caught "no retries after a refusal" said without its scope, and the
  permission mode called "the default" when the built-in default may be `auto`. The second caught
  the description losing the instruction to copy the project outside the clone.
- In `demo/`, the rules files and the fake secrets keep neutral file names and `session.sh`
  places them, so this repository gains no live settings file and no file named `.env`.
- Narration: 23 of 120 lines flagged on the first audio check, then 3, then none
  (`narration-rewrites-1.json`, `-2.json`). 禁止 was heard as 進去, 靜止, 禁手 and 指令; 金鑰 as
  金耀; 那一次 as 每一次, which changes the meaning. Longest card state measured from
  `timeline.json`: 13.5 s.
- Thumbnails: since the headless tutorial these were "text only", which left the thumb template's
  right 60% an empty panel, and two had a sub-line clipped at three lines. The final gate checks
  the file's size and the headline's height, so it passed five times before anyone opened the
  image. Each now carries the capture of the docs page its video cites; the two long sub-lines
  were shortened. No cut changed (same hashes), and all five packages were rebuilt and their
  publish gates resubmitted. While doing it, a batch script stopped with TaskStop kept running
  beside its replacement and two assembles collided on one video; nothing wrong was packaged, and
  that video was redone alone.
