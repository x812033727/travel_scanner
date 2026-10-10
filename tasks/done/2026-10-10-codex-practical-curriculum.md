---
id: 2026-10-10-codex-practical-curriculum
title: Build the Codex practical 18-lesson curriculum and reproducible materials
status: done
priority: P1
area: docs
owner: codex-gpt6-practical-series
claimed_at: 2026-10-10T17:12:41Z
created_at: 2026-10-10T17:12:28Z
completed_at: 2026-10-10T18:17:02Z
branch: codex/codex-practical-series-20261011
depends_on: []
scope:
  - docs/videos/codex-practical-series
  - tools/codex-practical
  - tools/codex-practical.test.mjs
---

# Build the Codex practical 18-lesson curriculum and reproducible materials

## Why

Implement the approved Traditional Chinese Codex course: 18 lessons, paired independent App/CLI versions, and a useful task/weekly-report project. Existing product articles and authored reference code cannot substitute for real product-operation evidence.

## Definition of done

- [x] All 18 lesson specifications and 36 independent episode briefs are complete.
- [x] Every lesson has a self-contained start/reference/challenge learner package with prompts, acceptance and separate answers.
- [x] Reference behavior passes meaningful tests, including duplicate titles, preservation, invalid data, unknown dates, truthful reports and backup/restore.
- [x] Reproducible ZIPs, manifests, independent learner reproduction and accurate stage status are saved.
- [x] First CLI baseline invocation and its original evidence are preserved; missing App/media/owner gates have separate continuation tickets.

## Steps

- [x] Check local worktrees, remote branches, open PRs and landed main; claim this narrow scope.
- [x] Author specs and paired runbooks with current official sources.
- [x] Build runnable incremental materials and package/check tools.
- [x] Record baseline, run independent checks, and prepare a reviewable draft PR.

## How to verify

Run `node tools/codex-practical/course.mjs check`, `node --test tools/codex-practical/labs.test.mjs`, the source tests and `npm run check:tasks`. Rebuild twice into new external output directories and compare all 18 ZIP SHA-256 values. Read `docs/videos/codex-practical-series/VALIDATION.md` and its hash-bound evidence for the recorded source/integration/browser/replay results. Repository-wide `npm run test:docs-videos` passed; the Windows `npm run test:tools` attempt is failed/incomplete and tracked separately, not reported as green. Review actual App, media and owner gates in the production tickets; pending assets do not count as this curriculum's product-operation or publication evidence.

## Notes

User approved on 2026-10-11 Asia/Taipei. The task CLI uses UTC for its ID (2026-10-10). Branch begins at origin/main 6a26eff42707603d8f80586ae0efb7c85a13fe15. Untracked .codex/environments is pre-existing and preserved. Normal text computer tools have no native App surface, so original App UI capture is an explicit pending production gate. No external upload, public publication, merge or production deploy is authorized by this task.

2026-10-11 curriculum completion evidence:

- `docs/videos/codex-practical-series/curriculum.json`, `lessons/01.md` through `18.md`, and `episodes/codex-practical-NN-{app,cli}/brief.md` provide 18 lessons and 36 independent entrance runbooks. Fresh completeness check reports 18/36 with no errors. Each entrance has its own start copy, prompt, verification, failure/repair and transfer exercise; author reference code, model results and native App capture remain distinct. Official Codex sources were opened on 2026-10-11; recording-day version checks remain in the briefs.
- `tools/codex-practical/course.mjs` and `labs.mjs` rebuild the 54 start/reference/challenge snapshots from tracked source. `materials/lessons/NN` saves all 18 sets of README, prompts, acceptance, answers and lesson metadata. Full runnable snapshots and media stay outside Git. `evidence/packages.json` indexes all 18 archives; external `<home>/mokaair-work/codex-practical-series/build-05/delivery` and `build-06/delivery` have identical ZIP bytes and canonical LF content. Prior builds are retained as history.
- `docs/videos/codex-practical-series/evidence/validation.json` preserves hashes for source 23/23 PASS, canonical course integration 11/11 PASS, and docs-videos 219/219 PASS. Coverage includes stable IDs for duplicate titles, input preservation, JSON/CSV validation, Taipei date boundaries and unknown completion dates, read-only MCP, actual Git worktree integration/conflict/revert, and archive preview/backup/byte-exact restore. Intentional start/challenge failures are retained; lessons 06 and 07 deliberately begin with green weak tests, so a green baseline is not treated as feature correctness.
- Independent replay report: `<home>/mokaair-work/codex-practical-series/runs/independent-learner/20261011-012806/REPLAY-REPORT.md`. Lesson 01 preserved 2 PASS/1 FAIL and unchanged source; lessons 03/05 main and challenge fixes passed with only core changes and unchanged supplied tests. Actual learner-website checks total 35: 34 PASS, one expected baseline failure, zero unexpected failures. This is an independent coding-agent reproduction, not human learning acceptance or native Codex App evidence. Owned HTTP servers were stopped; one timed-out empty Chrome tab has explicitly unconfirmed cleanup in that report.
- `evidence/independent-final-review.json` records independent lesson 07 actual DOM checks, lesson 11 invalid-calendar behavior preservation, lesson 17 configurable next-week/missing-input receipts and final lesson 18 scope reread. The final 18 prompt correctly implements `core.mjs/archiveTasks` TODO, allows only core/archive/restore/`practice.yml` plus a new boundary test, and identifies author-provided IO/CI scaffolds. No remaining identified consistency defect is recorded; actual model, App and CI runs remain separately gated.
- `evidence/lesson-01-cli-session.json` and `lesson-01-input-hashes.json` retain the actual read-only Codex CLI baseline session, original event/output hashes and unchanged five-file input. The inner project tests were 2 PASS/1 FAIL; successful outer exec does not mean all project tests passed. `lesson-01-browser.json`, `lesson-01-http-preview.json` and `advanced-browser.json` are learner-website/HTTP evidence, not native Codex App captures.
- Broad Windows tools validation is failed/incomplete. Existing ffmpeg empty-frame-range and automation fixture import/wait failures are retained and filed as `2026-10-10-windows-ffmpeg-empty-reference-range` and `2026-10-10-windows-automation-fixture-import`; their active scopes were not changed. See VALIDATION and `validation.json` for the precise limits.

Continuation audit: all 17 production tickets 02..18 remain `open`, unowned and unchecked. Each depends on this curriculum and lesson 01 production; lessons 03/05 form the next pilot pair, and the other production tickets also depend on both pilots. They retain native App, real App/CLI execution, full independent production review, media QA and owner learning gates. The partial independent learner replay above does not complete those paired-video tickets. Lesson 01 production is being updated by the parent from its latest media receipts and was not changed by this closeout.

This `done` marks the approved curriculum/materials scope complete for submission with the current draft PR. It does not claim that a PR was merged, a release was deployed, 36 videos were produced, the owner accepted the course, or YouTube content was uploaded/published. Draft PR creation, commit and push are handled by the parent; this closeout performs none of them. Current media status is read from STATUS and the production receipts rather than copied into this frozen curriculum evidence.

公開定位說明：`<home>` 與 `<repo>` 是去識別佔位，不供直接執行。精確路徑與未遮罩原始收據保存在 repo 外；既有收據 SHA-256 仍綁定原始位元組。
