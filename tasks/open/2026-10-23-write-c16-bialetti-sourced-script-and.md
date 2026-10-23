---
id: 2026-10-23-write-c16-bialetti-sourced-script-and
title: Write C16 Bialetti sourced script and Curio visual plan
status: in-progress
priority: P1
area: docs
owner: codex-c16-script
claimed_at: 2026-10-23T03:26:56Z
created_at: 2026-10-23T03:26:50Z
completed_at:
branch: codex/brand-story-bialetti-c16-script
depends_on: []
scope:
  - docs/videos/story-everyday-bialetti-c16/script.md
  - docs/videos/story-everyday-bialetti-c16/script-source-notes.md
  - docs/videos/story-everyday-bialetti-c16/visual-plan.md
  - docs/videos/story-everyday-bialetti-c16/visual-plan.json
  - docs/videos/story-everyday-bialetti-c16/reviews/author-script-receipt.md
---

# Write C16 Bialetti sourced script and Curio visual plan

## Why

C16's Treatment and direct-source matrix were independently checked and adopted by the owner on PR #1698, but there is no approved script or shot plan. The episode needs a chronological, source-bound Traditional Chinese narration and a Curio-style one-to-one visual plan before a script approval or paid-media quote is possible. The original Treatment task claims only its three existing author files; this ticket claims only five new script-author files.

## Definition of done

- [ ] Six connected chapters with stable line IDs, per-line source anchors, a 30–60 second hook, chapter-end questions, and an outro with answer, comment prompt, and subscription reason.
- [ ] A one-to-one Curio visual plan with original illustration prompts, post-produced cards, exact cute-mystery look, 5-second intro placement, 21-second v4 outro, and no resolved portrayal of M16 or M17 HOLD claims.
- [ ] An independent reviewer rechecks every narration claim and paired visual meaning against the direct sources, recording hashes; two fresh readers assess narration alone and author repairs any common failure.
- [ ] A draft stacked PR carries the authored files and review receipts, with no-auto-merge. No paid generation, import, upload, merge, deployment, or claim of measured TTS duration.

## Steps

- [x] Verify PR #1698 adoption hashes, narrowed Treatment claim, open PRs, branches, and absence of a C16 script claim; branch at `e32a2b5f05b38e4fe25ba7db5738e5b2e48aa2f4` without force.
- [x] Draft narration, source notes, and 1:1 visual plan in separate C16 script worktree.
- [ ] Run mechanical checks; record author hash and limitations.
- [ ] Obtain independent source/paired-visual review and two narration-only blind reads; apply any required author repairs and re-review changed hashes.
- [ ] Open draft stacked PR and hand off owner script/visual approval gate.

## How to verify

`npm run check:tasks`; compare `script.md` IDs with `visual-plan.json` IDs in order, count illustration/cards and max consecutive cards, inspect image prompts for banned brand/person names, compute SHA-256, `git diff --check`, and verify PR base/head/draft/`no-auto-merge` via `gh pr view`.

## Notes

2026-10-23 UTC: The managed `create_worktree` request failed because this chat's default cwd is not the Git repository (`Git ref lookup failed`). A separate ordinary Git worktree was created from the exact owner-adopted Treatment head; `attach_worktree` reports it is not managed. This does not affect Git isolation. The policy-blocked untracked ghost approval task remains only in the Treatment worktree and is untouched here.

The 1933 date is a retrospective design attribution; the visible utility-model dates are 1950/1951. The laundry inspiration is a legend. M16 identity and M17 invention, ownership, and litigation stay unresolved and out of definitive narration or art. Script length and illustration share are paper plans until real TTS and timing are measured after later owner/cost gates.
