---
id: 2026-09-29-keep-compilation-chapter-titles-from-giving
title: Keep compilation chapter titles from giving away mid-series answers
status: done
priority: P2
area: tools
owner: codex-gpt6-compilation-spoilers
claimed_at: 2026-09-30T05:58:31Z
created_at: 2026-09-29T02:27:23Z
completed_at: 2026-09-30T06:24:18Z
branch: codex/compilation-spoilers
depends_on: []
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/series.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/automation/compilation.mjs
  - tools/video/automation/compilation.test.mjs
  - tools/video/automation/compilation-spoilers.test.mjs
  - tools/video/core/compilation-review.mjs
  - tools/video/core/compilation-review.test.mjs
  - tools/video/compile/fixture.mjs
  - tools/video/package/metadata.mjs
  - tools/video/package/metadata.test.mjs
  - tools/video/package/cli.mjs
  - tools/video/package/package.test.mjs
  - .agents/skills/youtube-video/references/prompts/planner-compilation.md
---

# Keep compilation chapter titles from giving away mid-series answers

## Why

A binge compilation is one YouTube video with one chapter per episode, named
`第 N 集 〈集名〉` (`chapterTitle` and `chapterList` in
tools/video/core/compilation.mjs). All forty names sit in the description, so a
viewer reads every episode title before pressing play.

The 2026-09-29 read of the ten drama plans (docs/videos/series-plans) found 47
places where public text gave away an answer the story holds back: episode
titles such as 「第七次開服」 or 「她還活著」 on the episode-20 world flip,
title candidates naming the ending, pinned comments that promise what episode
40 does. The plans were rewritten and both AUTHORING.md now forbid it, but
nothing in the pipeline checks it:

- `planner:compilation` (prompts.mjs, the description prompt) only asks not to
  spoil the end, and it is handed the premise, which states the answers.
- The writer drafts each episode title with no view of which mysteries are
  still open, and a title becomes a chapter name word for word.

## Definition of done

- [x] The prompts that write episode titles, compilation descriptions and
  pinned comments say that public text must not give a mystery's answer, the
  mid-series flip or the ending, and they receive the mystery schedule (or the
  answers to avoid) rather than only the premise.
- [x] A reviewer or judge step for the compilation package looks at the chapter
  list and the description against the mystery schedule, and a hit sends the
  text back instead of publishing it.
- [x] A series without mysteries behaves as now.

## Steps

- [x] Find where episode titles are written for a series episode and what the
  model is shown then.
- [x] Extend the compilation description prompt and its input.
- [x] Add the check and a test with a fixture whose episode 20 title names the
  answer of a mystery revealed at 20.

## How to verify

`npm run test:tools`; with the fixture, the compilation package is sent back
until the spoiling title is changed.

## Notes

- 2026-09-30 preclaim audit on main `b9edf178`: PRs #999/#1000 are merged; 26 live PRs,
  58 remote heads and 176 accessible worktrees have no competing changes in this scope.
  `claim --force` bypasses only the obsolete `sothatswhy-shorts-from-episode` claim on
  prompts.mjs: its work landed in #904 and its remote branch is gone. That other task was
  not edited or released. flow.mjs remains owned by #1021 and is outside this scope.
  The series.test.mjs allowlist also needs the new verifier variant; its stale overlapping
  claim was completed in #978, and the file is clean in the other worktrees.
- The actual episode-title authors are the outline/chapter planners; they now receive the
  raw mystery answers and reveal schedule. Compilation context is retained at start and
  restored for legacy work, with missing context distinguished from an explicit empty list.
- An independent verifier reviews the actual composed source and translated public text.
  Rejected or malformed verdicts trigger bounded rewrites before documents are saved.
  Context/text hashes bind per-locale receipts; edits invalidate them. The worker checks
  resumed work before shared final/package/publish steps, and direct packaging refuses
  stale or missing receipts before touching the previous upload directory.
- Package chapter names now come from the current document, including title-only edits
  to a compilation without cards. A resumed worker rebuilds stale upload metadata before
  passing it to the shared publishing step. The shared flow itself was not modified.
- The plan-side sweep and the rewrites are recorded in
  docs/videos/series-plans/binge-five-20260928/AUDIT-REPAIR-20260929.md.
- Correction to the original note: compilation `chapter_cards` defaults to true. Public
  chapter-card/outro text, thumbnail text, title alternatives and any stored pinned-comment
  copy are included in the source review, alongside descriptions and chapter labels.
- Validation on bundled Node 24.19: full `npm run test:tools` completed with 964 passed,
  0 failed and 2 environment skips. After the final strict-verdict/counter changes, focused
  automation regressions passed 27/27 and helper/metadata/package tests passed 20/20.
  Prompt and series tests passed 47/47. The 40-episode fixture rejects episode 20's
  `她還活著` and accepts `門後的腳步`; tests also cover translated spoilers, legacy resume,
  context/text/timeline invalidation, package preservation and explicit no-mystery series.
- Final collision audit: 26 open PRs, 58 remote heads and 175 other accessible worktrees
  had no competing changes in the expanded scope at main `b9edf178`.
  Before push, rebased onto `b16d902f` (unrelated video pilot documents, #1006); all scoped
  implementation files were unchanged, all 94 focused tests passed again, and task checks
  validated 1,193 files. `git diff --check` passed.
  Validation used fixtures and mocked model stages, with no paid model calls, production
  actions or actual uploads. Merge and deployment remain separate from this draft PR.
