---
id: 2026-10-22-repair-c11-ucc-v4-blind-read
title: Repair C11 UCC v4 blind-read holds
status: done
priority: P2
area: docs
owner: codex-c11-ucc-author
claimed_at: 2026-10-22T17:01:50Z
created_at: 2026-10-22T17:01:45Z
completed_at: 2026-10-22T17:07:31Z
branch: codex/brand-story-ucc-c11-script
depends_on: []
scope:
  - docs/videos/story-everyday-ucc-c11/script.md
  - docs/videos/story-everyday-ucc-c11/visual-plan.json
  - docs/videos/story-everyday-ucc-c11/visual-plan.md
  - docs/videos/story-everyday-ucc-c11/script-source-notes.md
  - docs/videos/story-everyday-ucc-c11/reviews/narrative-reader-v4-a-author-transcription.md
  - docs/videos/story-everyday-ucc-c11/reviews/narrative-reader-v4-b-author-transcription.md
---

# Repair C11 UCC v4 blind-read holds

## Why

C11 UCC v4 source/visual delta review PASS, but two new, narration-only blind readers independently HOLD on script SHA `BA6284B882ECED83D522A8B568141C62BA565B944AAEBEE1E8AC388543C78A73`: the separation and heat-flavor problems jump to launch without a supported development bridge. Both also hear repeated opening-tool beats; Reader A finds the opener list-like. Rework only those areas within U1/U2 evidence; do not invent a formula, experiment or result.

## Definition of done

- [x] A/B feedback is recorded separately as author transcriptions of coordinator reports, bound to the old exact SHA, with no false reader signature or PASS.
- [x] Script and paired visual/source notes make the trial-and-error evidence limit audible, and give each remaining line a distinct job.
- [x] Updated draft PR head/hashes, focused structural checks, and pending independent source/two fresh blind gates are recorded. No paid media or publication.

## Steps

- [x] Read v4 independent source/visual receipt and the same 83-line blind narration input used by both readers.
- [x] Reopen U1/U2 primary pages for actual evidence on trial-and-error, launch and package generations.
- [x] Write old-SHA A/B author transcriptions, repair script/visuals/notes, run checks and push.

## How to verify

Compare script and visual IDs one-to-one; parse JSON; compare visual Markdown rows to JSON; check counts, card streak, opener spoilers and forbidden prompt names; `git diff --cached --check`; compute SHA-256 from committed bytes; confirm draft PR head via GitHub readback. Independent source and blind results cannot be self-judged.

## Notes

The relevant UCC 2026 retrospective (U1) says experts helped with repeated trial-and-error for separation and heat flavor, but does not disclose recipe or ordered trials. Its concrete technical answer is special inner coating for blackening caused by metal contact. U2 independently as a second company retrospective also mentions persistent trial-and-error and distribution-quality aim, and lists 1978 as second package generation and 1981 third-generation detachable pull tab. These are not independent historical witnesses. `--force` claim was needed because this worktree still has stale untracked `tasks/open` copies of prior completed C11 tasks; do not add or silently delete them.

The revised draft has 78 unique narration/visual IDs (70 body lines), 69 illustrated candidates and 9 post-production cards, with a maximum two-card streak. Script, JSON and visual Markdown have matching ordered IDs and mirrored visual rows; JSON parses; prompt-name scan and `git diff --check` pass. A 1,500-Han-character body count is only a pacing proxy, not proof of 480 TTS seconds. The new source/visual review and two fresh narration-only blind reads remain pending and must bind the new exact hashes. The five deleted IDs are `c110309`, `c110310`, `c110604`, `c110609`, `c110612`; no ID was renumbered or reused.

`npm run check:tasks` exits 1 because eight older, untracked C11 `tasks/open` copies duplicate already-finished `tasks/done` files in this worktree. This task's own open copy was removed after `tasks done` wrote its done file. The other orphan files are outside this task's scope and are excluded from the PR.
