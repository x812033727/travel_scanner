---
id: 2026-10-23-c20-zippo-v4-reader-b
title: C20 Zippo v4 independent narrator reader B
status: in-progress
priority: P1
area: docs
owner: codex-c20-reader-b
claimed_at: 2026-10-23T07:10:38Z
created_at: 2026-10-23T07:10:33Z
completed_at:
branch: codex/brand-story-zippo-c20-reader2-v4-blind
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20/reviews/reader2-v4-blind-lock.json
  - docs/videos/story-everyday-zippo-c20/reviews/reader2-v4-receipt.md
---

# C20 Zippo v4 independent narrator reader B

## Why

An independent narrator-only blind reading is required for C20's Zippo v4 text. The verdict must be locked before author material is read, then bound to the exact author PR head and preserved on a separate review branch.

## Definition of done

- [x] Reader B sees only the 64-line narration, records all twelve required PASS/HOLD answers with IDs, and locks a local read-only SHA-bound verdict before author context.
- [x] Exact author PR #1728 head and 64/64 narration parity are independently verified after the lock.
- [x] The byte-identical lock and a separate explanatory receipt are added to this isolated branch.
- [ ] Draft review PR is opened against the exact author branch and its base/head and checks are read back.

## Steps

- [x] Read blind narration and lock `HOLD` verdict (no_spoiler, no_detour, no_recap).
- [x] Create worktree/branch from author commit `3b27a5af392acfe88a168850aa57d2f27cb2f84d`.
- [x] Compare all 64 ID/text pairs against the author script with ordinal equality.
- [ ] Run focused checks, push branch, open draft PR, and record readback.

## How to verify

Read `docs/videos/story-everyday-zippo-c20/reviews/reader2-v4-blind-lock.json` and `reader2-v4-receipt.md`; verify the lock SHA-256 `DD5C0EE29C121D32BCDBE62B6EC302898AC474BE4BBF7444EF2C9FDDA7659BF5` and narration SHA-256 `0AB3EE39F253B19604618BDF70424DBEEDA51711561673B3120A06563697F761`. Check `git merge-base` against author head, `npm run check:tasks`, and `git diff --check`. Read PR metadata after creation.

## Notes

This is a text-only narrative HOLD. The score is independent from source/visual verification, paid voice runtime, owner acceptance, import, upload, and publication. Local read-only lock was created before author context; the copy in Git has the same SHA. The exact author script has 64 matching lines, no missing/extra/duplicate IDs, and no text mismatches. The draft PR stays open for author/editor review of the three HOLD points.
