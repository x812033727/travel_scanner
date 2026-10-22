---
id: 2026-10-22-preflight-c07-dr-martens-final-visual
title: Preflight C07 Dr Martens final visual plan
status: done
priority: P1
area: docs
owner: codex-c07-visual-preflight
claimed_at: 2026-10-22T15:00:46Z
created_at: 2026-10-22T15:00:38Z
completed_at: 2026-10-22T15:02:50Z
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/visual-plan.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/visual-preflight-v12.md
---

# Preflight C07 Dr Martens final visual plan

## Why

The final C07 visual-plan header still said 62 shots and 11 cards, while the current 73-row table contained 63 shots and 10 cards. Recheck every row against the final script before submitting it to the owner.

## Definition of done

- [x] Correct counts and a SHA-bound 73-row visual preflight receipt.

## Steps

- [x] Match script and visual IDs in order; count shots/cards and longest card run.
- [x] Review visual text for one-focus, illustrative-only, source-bound treatment and record remaining timed-media gates.

## How to verify

PowerShell parse of both Markdown tables: 73/73 unique IDs, same order, 63 shots, 10 cards, longest card run 2, 86.3% by count. `Get-FileHash` binds script and visual-plan SHA-256 in `visual-preflight-v12.md`; `git diff` confirms header-only visual change.

## Notes

All 73 visual rows were unchanged from the independent source v12 receipt; only stale header counts changed. Time-based illustration share, actual TTS duration and image quality remain unproved. No paid media generated.
