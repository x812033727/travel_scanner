---
id: 2026-10-23-independently-recheck-c19-seven-bank-five
title: Independently recheck C19 Seven Bank five-ID delta
status: in-progress
priority: P2
area: docs
owner: codex-c19-seven-bank-delta-reviewer
claimed_at: 2026-10-23T06:40:04Z
created_at: 2026-10-23T06:39:43Z
completed_at:
branch: codex/c19-seven-bank-delta-review-20261023
depends_on: []
scope:
  - docs/videos/story-everyday-seven-bank-c19/reviews/independent-delta-review-20261023.md
---

# Independently recheck C19 Seven Bank five-ID delta

## Why

Author PR #1742 narrowed five holds from independent full review PR #1745. The new exact head needs a separate source and paired-visual delta verdict without changing the author script.

## Definition of done

- [x] The five changed IDs have explicit PASS/HOLD reasoning tied to original Seven Bank sources.
- [x] A separate receipt binds all four author files to the new Git blob SHA-256 and checks 79/79 parity.
- [ ] A draft, no-auto-merge PR contains only this receipt and task handoff, based on the new author head.

## Steps

- [x] Create an isolated sparse review worktree and branch at f45d93dd263a06f582a2ebc06441b3f924bad381.
- [x] Compare a33b270..f45d93d and verify only five IDs and author receipt changed.
- [x] Reopen S3 PDF P14, S4 PDF P17–P18, S6 PDF P2 and S7 2001 notice.
- [x] Recompute four file hashes from both Git blobs and worktree bytes; parse all four files for parity and visual counts.
- [ ] Run task and diff checks, push the review branch, open a draft PR, and record its URL.

## How to verify

Read docs/videos/story-everyday-seven-bank-c19/reviews/independent-delta-review-20261023.md. Run Get-FileHash -Algorithm SHA256 on the four author files and compare with the receipt. Parse the Markdown tables and JSON shots for 79 unique same-order IDs, identical narration/source/prompt, 67 shots, 12 cards, maximum card streak 2. Run npm run check:tasks and git diff --check. Compare this PR with exact author head f45d93dd to confirm only the delta receipt and this task handoff changed.

## Notes

All five old HOLDs now PASS at exact f45d93dd: c190313 no imagined partner hesitation; c190409 restricted to S3 maintenance/funding costs; c190410 no fixed amount symbol; c190501 includes points beyond the initial corner; c190607 represents already offered document-reading functions without universal availability. Prior 74 PASS rows remain unchanged in the author four files. Blind readers, owner approval, measured TTS and illustration time, paid media, import, upload and publication remain separate.