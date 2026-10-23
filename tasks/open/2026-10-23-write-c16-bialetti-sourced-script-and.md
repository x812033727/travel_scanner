---
id: 2026-10-23-write-c16-bialetti-sourced-script-and
title: Write C16 Bialetti sourced script and Curio visual plan
status: review
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

- [x] Six connected chapters with stable line IDs, per-line source anchors, a 30–60 second hook, chapter-end questions, and an outro with answer, comment prompt, and subscription reason.
- [x] A one-to-one Curio visual plan with original illustration prompts, post-produced cards, exact cute-mystery look, 5-second intro placement, 21-second v4 outro, and no resolved portrayal of M16 or M17 HOLD claims.
- [ ] An independent reviewer rechecks every narration claim and paired visual meaning against the direct sources, recording hashes; two fresh readers assess narration alone and author repairs any common failure.
- [x] A draft stacked PR carries the authored files and author precheck receipt, with no-auto-merge. No paid generation, import, upload, merge, deployment, or claim of measured TTS duration.

## Steps

- [x] Verify PR #1698 adoption hashes, narrowed Treatment claim, open PRs, branches, and absence of a C16 script claim; branch at `e32a2b5f05b38e4fe25ba7db5738e5b2e48aa2f4` without force.
- [x] Draft narration, source notes, and 1:1 visual plan in separate C16 script worktree.
- [x] Run mechanical checks; record author hash and limitations.
- [ ] Obtain independent source/paired-visual review and two narration-only blind reads; apply any required author repairs and re-review changed hashes.
- [x] Open draft stacked PR and hand off independent review, blind-read, and owner script/visual approval gates.

## How to verify

`npm run check:tasks`; compare `script.md` IDs with `visual-plan.json` IDs in order, count illustration/cards and max consecutive cards, inspect image prompts for banned brand/person names, compute SHA-256, `git diff --check`, and verify PR base/head/draft/`no-auto-merge` via `gh pr view`.

## Notes

2026-10-23 UTC: The managed `create_worktree` request failed because this chat's default cwd is not the Git repository (`Git ref lookup failed`). A separate ordinary Git worktree was created from the exact owner-adopted Treatment head; `attach_worktree` reports it is not managed. This does not affect Git isolation. The policy-blocked untracked ghost approval task remains only in the Treatment worktree and is untouched here.

The 1933 date is a retrospective design attribution; the visible utility-model dates are 1950/1951. The laundry inspiration is a legend. M16 identity and M17 invention, ownership, and litigation stay unresolved and out of definitive narration or art. Script length and illustration share are paper plans until real TTS and timing are measured after later owner/cost gates.

Author draft pushed as [draft PR #1704](https://github.com/x812033727/travel_scanner/pull/1704), initially at `0149597e39136cb3aea08b50c181cb640710c592`, stacked on `codex/brand-story-bialetti-c16-treatment`; `no-auto-merge` and draft state were read back. Script SHA-256 `1F92C7016D71488D4553E9D3AF246A41B2CC8435CC1A19468BED0106212CE22F`, visual JSON `1238039373D123C1461BFE3AE4E9020C1F7BB3B7D0BC8B1217DEBBAC2D9BA364`, visual Markdown `748B551F18E1FA93184B643D14734BD83F17E34EC7DD943D38D77E16C7E1E548`, source notes `A650E4B7A4A7BA0FBCE2C279242C7B447DC5ED6C656168C98045EE96E7978C0A`. Mechanical check: 85/85 unique ordered IDs, 74 shots, 11 cards, max consecutive cards 1, no banned names in shot prompts, `npm run check:tasks` exit 0 in this script worktree, `git diff --cached --check` exit 0 before first commit. Independent review and two fresh narration-only blind reads remain pending; this author task is in review and not done.

2026-10-23 UTC: Independent first review on PR head `2013aa26bfe7642a4c0e5e8660608da69db39507` found 85/85 narration claims PASS but overall HOLD for seven visual rows. The author changed only `c160106`, `c160508`, `c160510`, `c160511`, `c160602`, `c160604`, `c160605` in both visual files: the 1957 source is a magazine print page, and MoMA/Omero have separate object records rather than a current shared display. Current visual JSON SHA-256 `573D4A485E4611B475558C83D0A3CC0BE5A20D672E37F700919BCEFD128DE91B`, visual Markdown `8BFECB74AA53597E9ABF099B497E3F124C056F3AA617BD356DE149005A9B935A`; script and source-note bytes/hashes unchanged. Delta review by the same independent reviewer remains required. The Treatment-worktree policy-blocked ghost open approval task is untouched.
