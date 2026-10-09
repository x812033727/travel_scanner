---
id: 2026-10-09-produce-the-skills-hands-on
title: Produce the Skills hands-on tutorial under the content-value rules
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-video-reference-comparison
claimed_at: 2026-10-09T16:17:40Z
created_at: 2026-10-09T16:16:21Z
completed_at:
branch: claude/skills-hands-on-video
depends_on: []
scope:
  - docs/videos/claude-code-skills-hands-on
  - docs/videos/lexicon.json
---

# Produce the Skills hands-on tutorial under the content-value rules

## Why

The owner asked to keep making AI tutorials. The CLAUDE.md tutorial ended by sorting what belongs
in CLAUDE.md and what belongs in a hook; this one takes the case it left: a procedure too long
for CLAUDE.md that is needed only sometimes. Same order as the last three: plan, run, write. It
goes as far as the publish gate on `/admin/videos`; uploading stays the owner's.

## Definition of done

- [x] A brief by a planner with the rules and no run evidence; outline A, as the owner delegated.
- [x] The listed runs made and logged: twelve headless sessions and the model-free checks.
- [x] `video.json` and `claims.md` by a writer; `lint` 0 errors, 0 warnings.
- [x] Two independent fact checks (`verify-1.md`, `verify-2.md`), their findings applied.
- [x] Narration synthesized and checked until no line was flagged; the audio gate approved it.
- [x] Its files in the repository.
- [ ] The cut, and the final and publish gates.
- [ ] Uploading to YouTube, which is the owner's.

## Steps

- [x] Plan, run, write, verify twice, narrate.
- [ ] `render`, `assemble`, `captions`, `review-push --gate final`, `package`,
  `review-push --gate publish`; languages: zh-TW only (the owner, in chat).

## How to verify

```bash
node tools/video/cli.mjs lint --slug claude-code-skills-hands-on
node tools/video/cli.mjs status --slug claude-code-skills-hands-on
```

`docs/videos/claude-code-skills-hands-on/runlog.txt` holds every run a card quotes, and `demo/`
the practice project, each way of writing the Skill, and the scripts.

## Notes

- Produced on 2026-10-09 with Claude Code 2.1.295 on Windows, Git Bash; twelve sessions on
  sonnet, none repeated. The runner script refuses to overwrite a named run and its dry run
  builds elsewhere, after the CLAUDE.md tutorial lost one run's raw files.
- What only the runs showed: without the Skill, three of the five steps were still done (version
  and README 3 of 3, CHANGELOG 2 of 3); the Skill's visible effect is the release note and the
  last line, 0 of 3 against 3 of 3. Under `-p` Claude called the Skill by itself every time, as
  its first tool call; the body arrives in the next stream line, a synthetic user message, not in
  the tool result. A vague description was called 3 of 3 as well. The slash form leaves nothing
  in the stream, only a hook log line. Listing cost +58 tokens against +486 for the same
  procedure in CLAUDE.md (one run).
- Never observed, and not told as seen: a present Skill being ignored, any pick-up rate, the
  effect of `when_to_use` or of the name alone, the interactive screen, personal or plugin
  Skills, other models.
- In `demo/`, the Skill and CLAUDE.md variants keep neutral file names and `session.sh` places
  them in the throwaway project, so this repository gains no live SKILL.md; the demo copies of
  the scripts keep their run folders under a temporary directory.
- The files go in before the cut is approved, as with the two tutorials before: the description
  links to `demo/` and the final gate checks that the link opens.
- Narration: 13 of 118 lines flagged on the first audio check, none on the second
  (`narration-rewrites-1.json`). Longest card state measured from `timeline.json` before
  assembling: 14.4 s.
- New mishearings: 被叫到 as 被照到／被抓到 (被呼叫 passed), 含糊 at the start of a sentence as 韓湖,
  指到 as 只到, 搬去 as 抽取.
