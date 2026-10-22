---
id: 2026-10-22-plan-oxo-c10-everyday-reversal-treatment
title: Plan OXO C10 everyday reversal treatment and sources
status: in-progress
priority: P2
area: docs
owner: codex-root-oxo-c10
claimed_at: 2026-10-22T13:14:26Z
created_at: 2026-10-22T13:14:19Z
completed_at:
branch: codex/brand-story-oxo-c10-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-oxo-c10
---

# Plan OXO C10 everyday reversal treatment and sources

## Why

The approved everyday-reversal series assigns C10 to OXO. Its working title says a peeler designed for grip difficulty became broadly used, but "everyone bought it" is not a measured claim. First establish what Sam Farber, Smart Design, museums and independent interviews actually support; distinguish the 1989 design from 1990 sale and the later universal-design interpretation from sales proof.

## Definition of done

- [x] Six-chapter Treatment and claim-level source matrix have an independent source review bound to final SHA-256 and can be shown to the owner.
- [ ] Owner chooses whether to adopt this Treatment before a full script is written.

## Steps

- [x] Check for an existing C10 task, branch or PR; use an isolated managed worktree and claim narrow scope.
- [x] Read brand-story, youtube-video story and curio rules; directly read OXO, MoMA, Cooper Hewitt, Design Council, Smart Design and the 2000 LA Times interview.
- [x] Draft a Treatment with an actual product and business sequence, not a list of grip benefits; revise unsupported "everyone bought" title.
- [x] Obtain independent M01–M10 review and repair any HOLD on exact file hashes.
- [ ] Obtain owner Treatment decision; no script or paid media beforehand.

## How to verify

Review each direct source URL in source-matrix.md, especially the 1989 design versus 1990 launch, the contradictory initial 15/20 item counts, and the retrospective nature of early retailer reception. Run npm run check:tasks, git diff --check, and targeted documentation checks. Reviewer must not use the author's assertions as independent evidence.

## Notes

MoMA's peeler object is dated 1989, while the commercial launch is documented as 1990. OXO's 2017 history says 15 initial pieces, while Smart Design and a 2000 Los Angeles Times interview say 20; the Treatment avoids a count. The 2000 interview attributes initial retailer hesitation to Farber's later recollection. Design Council's business numbers have no linked contemporaneous ledger; this treatment uses the qualitative universal-design story and does not forecast viewing or sales. The approved 20-topic plan is in draft PR #1652 and is not present on this origin/main-based branch, so this document does not use a broken relative link to it.

Independent review on 2026-10-22 directly reread S1–S7 and marked M01–M10 10/10 PASS. It corrected S7's unsupported "1989 commissioned" wording to the directly stated 1989 Farber insight / 1990 partnership. Receipt: `docs/videos/story-everyday-oxo-c10/reviews/independent-treatment-source-review.md`, bound to Treatment SHA `CD541D96E66042CA9A5EDE0C4017355C536D16FC7092249C9CCB15D266F4D550` and matrix SHA `4DEEB89A2028184E73F681FCFD3C9B7FB44463B364BF0D26AC9941F557F156A6`. Next gate is the owner's Treatment choice.

No full script, TTS, image, music, import, upload, publish, or merge is authorized by this task. Other episodes' US$25 media approvals do not transfer.
