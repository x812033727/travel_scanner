---
id: 2026-10-03-skills-accent-deploy-receipt
title: Skills: duration receipt procedure, dated-fixture triage, post-deploy verify script, voice wording audition
status: in-progress
priority: P2
area: docs
owner: claude-fable-accent-a1
claimed_at: 2026-10-03T09:22:28Z
created_at: 2026-10-03T09:22:26Z
completed_at:
branch: claude/skills-accent-deploy-receipt
depends_on: []
scope:
  - .agents/skills/dev-and-ci/SKILL.md
  - .claude/skills/dev-and-ci/SKILL.md
  - .agents/skills/dev-and-ci/references/ci-triage.md
  - .agents/skills/dev-and-ci/references/duration-receipt.md
  - .agents/skills/deploy/SKILL.md
  - .claude/skills/deploy/SKILL.md
  - .agents/skills/deploy/references/post-deploy.md
  - .agents/skills/deploy/scripts/host-verify.sh
  - .agents/skills/youtube-video/references/script-writing.md
  - .agents/skills/youtube-video/references/voice-audition.md
---

# Skills: duration receipt procedure, dated-fixture triage, post-deploy verify script, voice wording audition

## Why

The 2026-10-03 voice-accent change (PR #1168) and its deploy produced four procedures that lived only in a chat
log and in memory files: how a receipt-bound file gets its independent review increment (four times on one
branch, once after merging main), how to tell a dated-fixture time bomb from a flake (main was red from 06:14Z
until #1169), how to verify a deploy with one read-only script designed by a propose/refute workflow (15/15 on
5af4ffebf), and how to audition voice-style wordings before changing them. Skills are where the next agent
looks, so they go there.

## Definition of done

- [x] `dev-and-ci`: `references/duration-receipt.md` (what is bound, the increment, the merge follow-up, the
      head-merged-with-main CI effect), a rule and an index row in SKILL.md, two new triage rows in `ci-triage.md`.
- [x] `deploy`: `scripts/host-verify.sh` (the shared checks, EXPECTED_SHA/ALEMBIC_HEAD/UP_COUNT at the top, an EXTRA
      CHECKS section with the three container patterns), `post-deploy.md` section on using and extending it, SKILL.md
      row 4, command and file list.
- [x] `youtube-video`: `references/voice-audition.md` and a pointer from `script-writing.md`. SKILL.md (receipt-bound)
      left alone on purpose while #1170/#1172 carry their own receipt increments.
- [x] `.claude/skills/*/SKILL.md` copies byte-identical (`tools/skills.test.mjs`).

## How to verify

```bash
node --test tools/skills.test.mjs
bash -n .agents/skills/deploy/scripts/host-verify.sh
npm run check:tasks
```

## Notes

- `host-verify.sh` is the generic half of the 15-check script that verified 5af4ffebf; the five #1168/#1160/#1164
  checks were dropped and their shapes kept as the EXTRA CHECKS patterns.
- None of the changed files is in `REVIEW_FILES`, so no receipt increment is needed for this PR.
