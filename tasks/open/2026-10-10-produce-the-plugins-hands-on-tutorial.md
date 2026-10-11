---
id: 2026-10-10-produce-the-plugins-hands-on-tutorial
title: Produce the plugins hands-on tutorial under the content-value rules
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-video-reference-comparison
claimed_at: 2026-10-10T11:13:16Z
created_at: 2026-10-10T11:12:55Z
completed_at:
branch: claude/plugins-hands-on-video
depends_on: []
scope:
  - docs/videos/claude-code-plugins-hands-on
  - docs/videos/lexicon.json
---

# Produce the plugins hands-on tutorial under the content-value rules

## Why

The owner asked to keep making AI tutorials and picked plugins as the next subject. The earlier
ones each built one part in a project's `.claude` folder: a Skill, a subagent, a hook. This one
is what comes after: packing those three into a plugin, loading it into a second project, and
checking that all three arrived, because a plugin that passes `claude plugin validate` can still
lose a part. Same order as the last seven: plan, run, write. It goes as far as the publish gate
on `/admin/videos`; uploading stays the owner's.

## Definition of done

- [x] A brief by a planner with the rules and no run evidence; outline A, chosen by the owner.
- [x] The listed runs made and logged: twelve headless sessions and the model-free checks.
- [x] `video.json` and `claims.md` by a writer; `lint` 0 errors, 0 warnings; the layout check run
  before narration.
- [x] Two independent fact checks (`verify-1.md`, `verify-2.md`), their findings applied.
- [x] Narration synthesized and checked until no line was flagged; the audio gate approved it.
- [x] Its files in the repository.
- [ ] The cut, and the final and publish gates.
- [ ] Uploading to YouTube, which is the owner's.

## Steps

- [x] Plan, run, write.
- [x] Verify twice, narrate.
- [ ] `render`, `assemble`, `captions`, `review-push --gate final`, `package`,
  `review-push --gate publish`; languages: zh-TW only (the owner, in chat).

## How to verify

```bash
node tools/video/cli.mjs lint --slug claude-code-plugins-hands-on
node tools/video/cli.mjs status --slug claude-code-plugins-hands-on
```

`docs/videos/claude-code-plugins-hands-on/runlog.txt` holds every run a card quotes, with each
session's tool calls and their outcome, and `demo/` the seeds of the plugin and the two
projects, the scripts that assemble them, and each run's results.

## Notes

- Produced on 2026-10-10 with Claude Code 2.1.295 on Windows, Git Bash; twelve sessions on
  sonnet (k1 to k3 with the plugin, n1 to n3 without, and one each of b1, g1, s1, r1, x1, o1),
  none rerun, none with `--force`, every one with `--permission-mode default` and no Bash. The
  plugin was loaded with `--plugin-dir` only; `claude plugin validate` was the only
  `claude plugin` subcommand run, and only on the seeds' folders. The three places outside the
  project were hashed after every session and did not change.
- In `demo/`, the plugin's manifest, hooks file, `SKILL.md`, agent file and the projects'
  settings keep neutral file names, and `kit.sh` and `session.sh` assemble the plugin and the
  two projects outside the repository, so this repository gains no live plugin, skill, agent,
  hook or settings file. The scripts refuse to run when the run folder is inside a git
  repository.
- What only the runs showed: under `-p` with `--plugin-dir` all three parts loaded with no trust
  step; the model wrote the prefixed names (`ship-kit:release-prep`, `ship-kit:log-scout`) by
  itself; a plugin whose hook still pointed at the old project's path passed validate, loaded
  without an error and edited the file its hook should have stopped, and only the stream's hook
  events and the debug record showed it; a skill's template outside the project needed a read
  permission the main runs had pre-approved.
- The first fact check recounted all 121 tool calls from the raw streams (119 ran, 1 stopped by
  the hook, 1 asked with nobody to answer) and found every number right. Its one must-fix: the
  script called eleven variants "broken", and two of them are valid by the official page (the
  manifest is optional). It also found that the run record's "the backslashes differ from the
  official page" compared the run with one sentence of one page; the troubleshooting page says a
  hook written as a command with a separate args array keeps native paths, which is what was
  seen. `runlog.txt` ends with a coordinator note saying so.
- The second passed it with six should-fixes, among them: "no manifest also passes" read as if
  validate had checked that folder's parts, and "Node.js with arguments" named the wrong thing as
  the cause of the backslashes (it is the args array being separate from the command).
- Narration: 11 of 105 lines flagged on the first audio check, then none
  (`narration-rewrites-1.json`). 同一句 was heard as 同一局, 同事也要 as 同時也要, 怎麼搬 as 怎麼辦,
  旗標 as 起標 and 指標, 這支 hook as 只是 hook, 拿一句 as 拿依據. Narration 10:37; longest card
  state measured from `timeline.json`: 12.1 s; the second chapter starts at 29.7 s.
- The session that ran the first audio check ended mid-run and left one transcription request
  (a single clip) marked as sent with no answer. The process was gone, so the entry was cleared
  with `tools/video/tts/speech-journal.mjs forget` and the check run again; at worst that one
  clip was transcribed twice.
