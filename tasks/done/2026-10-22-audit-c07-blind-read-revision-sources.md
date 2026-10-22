---
id: 2026-10-22-audit-c07-blind-read-revision-sources
title: Audit C07 blind-read revision sources
status: done
priority: P2
area: docs
owner: codex-c07-v8-source-review
claimed_at: 2026-10-22T13:41:09Z
created_at: 2026-10-22T13:41:05Z
completed_at: 2026-10-22T13:44:37Z
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review-v8.md
  - tasks/open/2026-10-22-audit-c07-blind-read-revision-sources.md
  - tasks/done/2026-10-22-audit-c07-blind-read-revision-sources.md
---

# Audit C07 blind-read revision sources

## Why

The C07 author revised the script, visual plan, and source notes again after blind reading. The v7 source PASS is bound to different hashes. Review the new delta independently before anyone treats it as source approved.

## Definition of done

- [x] Compare all 48 changed narration rows, 32 changed visual rows, and revised source notes with v7 and direct primary sources.
- [x] Record exact PASS/HOLD IDs and SHA-256 hashes in a separate v8 receipt.
- [x] Keep the author's script, visual plan, and source notes unchanged and push the receipt to draft PR #1680.

## Steps

- [x] Claim a narrow review scope and compute exact changed ID lists and 77/77 alignment.
- [x] Read Crucq A1 directly, check the late-1980s Dutch anecdote and 1990s hypothetical, and cross-check brand/museum claims.
- [x] Persist the HOLD result with exact repair scope, verify staged diff, and push.

## How to verify

`Get-FileHash` on script, visual plan, and source notes; row-by-row comparison against commit `c0a891c54`; 77/77 ID and 64/13 count; `git diff --cached --check`; read PR #1680 head after push. Global docs-video test is not used as a source approval gate for a review-only receipt.

## Notes

HOLD is narrow: A1 explicitly says cut-off jeans or starched trousers, but changed narration `c070102` and `c070404` and visual `c070103` and `c070404` cite it for turned-up cuffs. Existing unchanged visual `c070102` also depicts a turned-up cuff. A direct 1969 Leeds student newspaper confirms some skinheads wore a half-inch turn-up but lists several boot types and does not identify Dr. Martens on the same wearer. The easiest correction is to use A1's cut-off wording consistently; alternatively add a stronger direct source for the precise combination. All other changed claims passed their source boundaries. A1's Dutch lace anecdote is limited to that place/time, with no color mapping in narration or imagery, and its 1990s outfit is explicitly hypothetical. Existing unrelated duplicate open task files are left untouched. `tasks.mjs done` wrote this done copy but left its untracked open copy; the previous identical-path cleanup attempt was automatically blocked by policy, so this copy will not be staged and no workaround will be attempted.
