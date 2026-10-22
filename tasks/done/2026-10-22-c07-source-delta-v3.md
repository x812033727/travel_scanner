---
id: 2026-10-22-c07-source-delta-v3
title: Recheck C07 source review delta v3
status: done
priority: P2
area: docs
owner: codex-c07-source-reviewer
claimed_at: 2026-10-22T11:54:02Z
created_at: 2026-10-22T11:53:56Z
completed_at: 2026-10-22T11:55:28Z
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review-v3.md
  - tasks/open/2026-10-22-c07-source-delta-v3.md
  - tasks/done/2026-10-22-c07-source-delta-v3.md
---

# Recheck C07 source review delta v3

## Why

After the v2 source review held three sentences, the author made a narrow repair. The new script hash needs an independent, direct-source delta receipt before anyone can treat the source gate as passed.

## Definition of done

- [x] Verify current script, source-note and visual SHA-256 values and exact 77-ID diff from the v2-reviewed files.
- [x] Reopen the affected company, product archive, museum and independent research pages.
- [x] Write a hash-bound verdict for c070105, c070310, c070609 and affected c070610, including the remaining gates.
- [x] Commit and push the receipt to draft PR #1680.

## Steps

- [x] Compare 619a245ef with fe924e629 and verify 73 narration rows unchanged, four changed, and 77 matching visual IDs.
- [x] Check the changed claims and source registration against direct pages.
- [x] Write docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review-v3.md.
- [x] Run available local checks, commit and push.

## How to verify

Recompute SHA-256 of script.md, script-source-notes.md and visual-plan.md against the receipt. Count and compare all 77 narration and 77 visual IDs. Read the four delta rows and source URLs. Run git diff --cached --check. npm run check:tasks is locally limited by the old policy-blocked duplicate open ticket noted below; in the pushed commit, only the finished ticket is tracked.

## Notes

2026-10-22: The four changed narration rows all pass direct-source scope review. The other 73 are byte-identical to v2-reviewed narration rows; visual-plan is unchanged. This yields 77/77 source PASS only, with narrative blind readers, owner script approval, TTS duration, actual illustration time and paid authorization still pending. Script SHA 5264D383C8E1CA8787DAD68F24989B774E53233813D4F6DEE00764B31B6E6F60; notes SHA C42E10CEE8B3F922479459E3AE5A345EBB7969A09DDB4FC5508AFA8384F7240F; visual SHA 32B854AE849421F14B39B81CC612745B522E9EBFDFEC1FF62AA09EEAE43984CA. The prior done command left untracked tasks/open/2026-10-22-c07-revised-script-source-review.md and exact Remove-Item was blocked by policy; this task does not touch it. No script/visual edit or paid work.
