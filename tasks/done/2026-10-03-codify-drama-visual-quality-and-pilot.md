---
id: 2026-10-03-codify-drama-visual-quality-and-pilot
title: Codify drama visual quality and pilot revision workflow
status: done
priority: P1
area: docs
owner: codex-skill-creator
claimed_at: 2026-10-03T01:38:32Z
created_at: 2026-10-03T01:38:20Z
completed_at: 2026-10-03T02:00:11Z
branch: codex/wedding-visual-revision-20261003
depends_on: []
scope:
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
  - .agents/skills/youtube-video/references/visual-quality.md
  - .agents/skills/youtube-video/references/drama.md
  - .claude/skills/youtube-video/references/drama.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Codify drama visual quality and pilot revision workflow

## Why

The wedding pilot was technically traceable but the owner rated its production
craft around 60/100 and said the rough visuals would not hold attention. Existing
instructions emphasize source, props and mechanical checks without enough
guidance for art direction, acting and editorial appeal. The owner requested a
reusable skill and a 90/100 quality target, not a lower automated pass threshold.

## Definition of done

- [x] The existing youtube-video skill routes animation development and rough-visual feedback to a usable visual-quality workflow.
- [x] Art, acting, storytelling and sound/edit review remain distinct from technical validity and automatic scores.
- [x] The workflow preserves current authorization, production review bindings, bounded retakes and existing audio reuse.
- [x] The user target of 90/100 is treated as a subjective quality goal with actual comparison evidence, not a self-awarded result or universal scoring threshold.
- [x] Skill mirrors and references validate, and an independent realistic scenario review finds no scope or approval inflation.
- [x] Research actual reference videos in the in-app browser, preserve observed timestamps and limits, and use the findings in reusable craft guidance.

## Steps

- [x] Add a focused reference and route it from the existing entrypoint and drama workflow.
- [x] Check skill discovery, mirrors, links and behavior; record validation and close this skill-only task in the PR.

## How to verify

Run `node --test tools/skills.test.mjs`, the skill-creator quick validator and
`npm run check:tasks`; inspect a realistic independent forward-test without paid
generation or production writes. Run the repository tools checks before push.

## Notes

PR #1132 already changes animation-production.md, so this change avoids that
file. The active worker-concurrency task changes automated.md only; neither its
files nor owner state is touched. SKILL.md and the existing drama.md mirror stay
byte-identical; the new reference lives at the canonical .agents path.

The duration guard binds both SKILL.md files. Scope was extended to the two shared
duration review artifacts only after collision inspection: no active task claims
them, but PRs #1132 and #1139 also carry their own increments. Preserve historical
review text and all 68 unchanged bindings; add only this independently reviewed
two-file increment. This is an integration receipt overlap, not implementation of
either PR. Reconcile bindings after any later rebase rather than copying another
branch's receipt or treating its review as coverage of these bytes.

Validation on 2026-10-03:
- Actual in-app reference sampling and primary creator notes are recorded in
  episodes/visual-reference-study-20261003.md under the production task's scope.
- Independent forward review /root/skill_forward_review: PASS after explicit
  source-meaning, narrow-repair, locked-audio and not-checked evidence fixes.
- Independent duration increment /root/verify_local: PASS—DURATION_ONLY for both
  SKILL.md files, hash 37b4d8539b058120886eb7de0cd57d65a1900cde175bd78cab4893e7afa9f0a3.
- node --test tools/skills.test.mjs: 6/6 pass. Skill-creator quick_validate with
  Python -X utf8: valid. Long-form CLI check: all 473 plans pass.
- Full tools suite using bundled Node 24.19.0: 1,259 pass, 3 skip, 0 fail.
  The initial system Node 24.13.0 run had native Windows failures plus the stale
  duration bindings; the refresh and compatible-runtime rerun resolved these.
- check:tasks passes with existing unrelated stale/overlap warnings.
  git diff --check passes. No production settings, jobs, TTS or publication changed.
- This closes only the reusable skill work. The first two episodes remain open
  under 2026-10-02-wedding-competition-pilot-four-languages.
