---
id: 2026-10-20-produce-the-agent-skills-one-year
title: Produce the Agent Skills one-year tutorial video (skills-one-year-monthly-report)
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1-ai-videos
claimed_at: 2026-10-20T16:04:38Z
created_at: 2026-10-20T16:04:14Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/skills-one-year-monthly-report
---

# Produce the Agent Skills one-year tutorial video (skills-one-year-monthly-report)

## Why

The owner asked on 2026-10-20 for AI videos that match or beat two reference films, the first being
《志說 AI｜Skill 出來滿一年了還有人不會嗎？7 分鐘完全理解 Skill》. Agent Skills were announced on
2025-10-16, so the one-year hook is exact. The channel's content-value rules want a tutorial with a
recurring example, real runs, a measured contrast with the simple way, and an unpredicted result.

## Definition of done

- [x] A brief under `docs/videos/skills-one-year-monthly-report/` with the main example, the simple way
      it beats, the runs, the record and two outline options (選項 A recommended).
- [x] Real runs on record: a practice folder, three arms × 3 headless `claude -p` sessions, a vague
      description × 3, one slash call, `claude plugin validate` on four versions (`runlog.txt`,
      `demo/`).
- [x] `video.json` and `claims.md` written from the record; `lint` shows 0 errors, 0 warnings;
      estimate 8.4 minutes, 94 lines, 33 scenes.
- [ ] Independent fact-check (`verify-1.md`) and the blind storytelling panel; findings applied.
- [ ] Outline gate, speech, audio check, render, assemble, captions, QA, package, gates on the site
      (needs the paired video-tool token or the host worker; the owner decides).
- [ ] Nothing uploaded to YouTube by an agent.

## Steps

- [x] Design and run the experiment (pilot, then the formal round; see Notes for why there were three).
- [x] Brief, run log, demo folder, claims, video.json, lexicon terms.
- [ ] Apply verify-1 and panel findings, re-lint, commit.
- [ ] Owner: pair the token (`node tools/video/cli.mjs login`), choose outline A on `/admin/videos`
      (or `approve --gate outline`), then `tts --dry-run`, `tts`, `check-audio`, `review-push`.

## How to verify

```bash
node tools/video/cli.mjs lint --slug skills-one-year-monthly-report
node tools/video/cli.mjs status --slug skills-one-year-monthly-report
```

## Notes

- Three rounds were run on 2026-10-20 (all in `runlog*.txt`): the pilot put the script and template in
  the project, and the "nothing given" arm found them by listing the folder (5/6), so the design
  changed; round 2 used the final design but its SKILL.md, sum.mjs and the pasted rules had lines
  longer than a code card's 64 characters, so the files were re-wrapped (no rule changed) and the
  whole batch was run again as round 3, the one the film uses. Round 2 scored identically.
- Headless flags are in `runlog.txt`; `node` is pre-approved and `python3` is not, which is why the
  skill's bundled script ran and the models' own Python did not. The film says this plainly and
  cites `allowed-tools` as the fix it did not use.
- `description` replaced by 「專案維護用的說明。」 was still invoked 3/3: the name matched. The film
  marks 「名字就對上了」 as the owner's reading; proving it needs the name changed too (not run).
- Every `claude -p` session cost 0.024–0.068 USD; the thirteen cost 0.449 in total.
- The Codex companion film is planned in `docs/videos/codex-first-task-no-code/brief.md` and waits
  for the owner's runs (task 2026-10-20-plan-the-codex-beginner-guide-video).
