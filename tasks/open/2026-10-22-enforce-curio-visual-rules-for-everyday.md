---
id: 2026-10-22-enforce-curio-visual-rules-for-everyday
title: Enforce Curio visual rules for everyday brand stories
status: in-progress
priority: P1
area: tools
owner: codex-gpt6-everyday-curio-guard
claimed_at: 2026-10-22T02:06:15Z
created_at: 2026-10-22T01:58:23Z
completed_at:
branch: codex/everyday-curio-guard
depends_on: []
scope:
  - tools/video/core/story.mjs
  - tools/video/core/story.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - .agents/skills/brand-story/SKILL.md
  - .claude/skills/brand-story/SKILL.md
---

# Enforce Curio visual rules for everyday brand stories

## Why

The owner decided that the `story-everyday-*` series follows the Curio visual rules; C02's task and `docs/videos/brand-stories-everyday-reversals-20261020/README.md` already record this. C03 needed a manual recut because its first accepted plan had 67 illustrations and 27 cards, several of them conceptual lists or questions. Its corrected 73/21 plan passes a manual Curio check, but `curioProblems` runs only for `curio-*` slugs, while `cuteStoryVisualProblems` in the story worker covers `story-five-*` and two named v2 pilots. A future `story-everyday-*` episode can pass ordinary lint without the series' illustration ratio or card-run guard.

## Definition of done

- [x] `story-everyday-*` episodes with `series.kind: story` fail local lint and the host pre-keyframes gate if the look differs from the exact `cute-mystery` preset, illustrated body scenes are below 70%, or more than three cards run together.
- [x] The rule applies to C04–C20 and does not change legacy story routes or `curio-*` behavior.
- [x] The shared brand-story skill states the same Curio illustration acceptance and one-number/name/quote/source card guidance; card meaning still receives editorial review.

## Steps

- [x] Reuse a shared visual-rule predicate in core lint and the story worker preflight, scoped to the everyday series, without reclassifying a story as Curio.
- [x] Add positive and negative tests for look, illustrated share, card runs, C03 passing, and unrelated story slugs staying unchanged.
- [x] Update byte-identical `.agents` and `.claude` brand-story skills.

## How to verify

Run `node tools/video/cli.mjs lint --slug story-everyday-moleskine-c03`, the focused core lint and story worker tests, `npm run test:tools`, and `npm run check:tasks`. Use a temporary test fixture to show that an everyday story at 69% illustrations or four consecutive cards fails before paid keyframes; verify a legacy story does not acquire the new gate.

## Notes

Filed during the C03 Curio-rules recut on 2026-10-22. C03's visual rule audit is recorded at `docs/videos/story-everyday-moleskine-c03/reviews/curio-rules-recut.md`; this ticket is an enforcement follow-up, not authorization for new paid media or changes to the C03 task's scope.

Claimed with `--force` on 2026-10-22 because the board still marks two overlapping historical tickets in progress: `2026-10-17-story-narrative-panel-asks-two-independent` and `2026-10-18-story-thumbnail-brand`. Their PRs #1562 and #1568 merged on 2026-10-18, their named remote branches are gone, and both changes are in `origin/main`; no open PR owns the visual-rule function. This ticket changes only the listed visual-rule files and mirrored skill.

Implementation: `storyCuteVisualProblems` is the shared check. Local lint applies it only when the slug starts `story-everyday-` and `series.json.kind` is `story`; the host worker uses the same check before keyframes, with the existing five-story and two v2 pilot routes unchanged. The semantic purpose of each card stays an editorial review, not an automated text classifier.

Verification: core story/lint tests **59/59 pass** (including a 69/100 direct-rule fixture and local-lint four-card/60% negative cases); host visual-gate focused test **1/1 pass** for C03, C04, C20 and non-story exclusions; Curio core tests **6/6 pass**; real C03 lint **0 errors, 0 warnings**; `npm run check:tasks` passed before the partial task move, with unrelated stale-claim warnings. `npm run test:tools` was attempted but is not green in this Windows checkout: several test-file subprocesses exit without diagnostics, including the full `automation/story.test.mjs` which also does so on the unmodified C03 branch. The separately isolated host visual-gate test passes. That full run also flagged two C03 profile paths outside this ticket's scope; the C03 branch then replaced them with portable placeholders, this branch was rebased on that commit, and `node --test tools/repo-hygiene.test.mjs` now passes **3/3**. No media service was called.

Administrative close remains open: `npm run tasks -- done` wrote a second, untracked `tasks/done/` copy but could not remove this original open file because Windows reported it was still present/held open. A single exact `Remove-Item -LiteralPath` attempt was rejected by automatic approval review as `blocked by policy`; no alternate deletion was attempted. The draft PR deliberately includes this open/in-progress task and excludes the untracked done copy. The earlier `check:tasks` success was before this partial move; local validation now sees both copies until the administrative block is resolved.
