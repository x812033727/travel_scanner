---
id: 2026-10-23-c18-fiskars-independent-source-and-paired
title: C18 Fiskars independent source and paired visual audit
status: review
priority: P2
area: docs
owner: codex-c18-independent-audit
claimed_at: 2026-10-23T04:10:25Z
created_at: 2026-10-23T04:10:21Z
completed_at:
branch: codex/brand-story-fiskars-c18-independent-audit
depends_on: []
scope:
  - docs/videos/story-everyday-fiskars-c18/reviews/independent-source-visual-audit.md
---

# C18 Fiskars independent source and paired visual audit

## Why

Author PR #1711 contains a draft script and 85 visual directions; its own preflight is not an independent fact or paired-visual audit. A separate reviewer must bind the input bytes and inspect M01–M12 originals before blind narration readers or the owner are asked to approve the script.

## Definition of done

- [x] A separate receipt records direct source checks, all 85 narrator/visual pairs, exact four input SHA-256 hashes, structural counts and narrow HOLD IDs without changing the author files.

## Steps

- [x] Claim a receipt-only scope on an isolated branch from author head `ea46ff32b07a234e20e8e462ba8986e5150d3693`.
- [x] Directly open the primary M01–M12 pages/PDFs and check all 85 narration lines against their mapped source notes.
- [x] Compare all 85 JSON visuals with same-ID narration and the six MD chapter summaries; verify 74 image/11 card, prompt and bookend constraints.
- [x] Write the independent receipt with exact bytes and narrow remediation for each HOLD.

## How to verify

`Get-FileHash` for the four inputs, JSON parse and ordered-ID comparison, `npm run check:tasks`, and `git diff --check`. The receipt records the direct original URLs and findings. This is factual and visual review, not a test of real TTS/media.

## Notes

Initial review result: **HOLD**, with four narrow groups H01 `c180103–104` (retrospective company story in opener), H02 `c180307–308` (cheaper scissors became unsupported production-cost claim), H03 `c180511` (CIPO particular handles/whole visible surface and generic paired image), H04 `c180608` (do not transfer Canada's detailed registration scope to unexamined Finnish/U.S. records). Full details: `docs/videos/story-everyday-fiskars-c18/reviews/independent-source-visual-audit.md`. The author files remain unchanged. A `tasks done` attempt copied this ticket into `tasks/done/` but could not unlink the open copy; the explicit `Remove-Item` repair was blocked by policy. This PR therefore carries only this claimed `review` ticket plus the receipt; the untracked local done copy is excluded. Two narrator-only blind reads, owner script decision, real TTS duration, screen-time mix, quote and paid generation are separate gates.

Delta on author head `50f17c46609148311c57adead19b806c51eefe62`: requested H01–H04 lines and optional `c180609`/`c180214` now pass the reopened originals and paired visuals, but the same literal sample-table staging remains in `c180312` and `c180404`; receipt updated to HOLD on those two exact IDs with minimal wording repairs. All 85 IDs remain paired. Review PR #1717 remains draft with `no-auto-merge`. The policy-blocked untracked local `tasks/done` duplicate remains untouched.

Final source/paired-visual delta on author head `2e212b27d68bb408c0ca64bc2d6be05bf255fe64`: `c180312` and `c180404` now omit the unsupported literal table placement. Fiskars's original account and 2006 annual report support the samples and vote; their unchanged same-ID JSON scenes remain conceptual illustrations under the MD visual contract. These two lines **PASS**, as do prior H01–H04. Only `script.md` changed among the four bound inputs, and all 85 line IDs still pair. The final four hashes and gate limits are in the receipt; the policy-blocked local duplicate remains untouched.
