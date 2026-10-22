---
id: 2026-10-22-recheck-c07-narrative-source-delta
title: Recheck C07 narrative source delta
status: done
priority: P2
area: docs
owner: codex-c07-delta-source-review
claimed_at: 2026-10-22T12:08:20Z
created_at: 2026-10-22T12:08:10Z
completed_at: 2026-10-22T12:09:19Z
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review-v5.md
  - tasks/open/2026-10-22-recheck-c07-narrative-source-delta.md
  - tasks/done/2026-10-22-recheck-c07-narrative-source-delta.md
---

# Recheck C07 narrative source delta

## Why

The C07 author rewrote eight source-sensitive narration lines after a narrative blind reader wanted a more concrete account of clothing, music and political ambiguity. Four matching visual rows and source notes changed too. The v4 source PASS is hash-bound to the previous text and cannot approve this new version.

## Definition of done

- [x] Independently check the eight changed narration claims, four changed visual rows and revised source note against direct sources.
- [x] Publish an exact-hash PASS/HOLD delta receipt to draft PR #1680 without altering the script or visuals.

## Steps

- [x] Compare current files to the v4-reviewed head and verify all 77 script/visual IDs still align.
- [x] Reopen Crucq's research and the official brand history, with care not to present company retrospective as independent social history.
- [x] Document limited political claims and pending blind reader/owner gates.

## How to verify

Recompute SHA-256 of `script.md`, `visual-plan.md` and `script-source-notes.md`; compare with the v5 receipt. Review `git diff 37d8db01d..1dd3fb18e` and count one-to-one IDs, 64 shots and 13 stats. Run `git diff --cached --check`. Local `check:tasks` is limited by four untracked duplicate open tickets from interrupted `done` removals; do not call it green or bypass their removal.

## Notes

2026-10-22: Crucq's article directly supports bricolage and work boot/clothing combinations, West Indian ska/rocksteady influence, later punk adoption, and separate racist and anti-racist skinhead responses. Official Dr. Martens brand history puts punk and Two Tone into its 1970s retrospective. The new narration keeps these as a researcher's analysis, a company retrospective or questions; it does not claim that music caused purchases. The visual changes are anonymous concept scenes with no extremist symbols or instructive political color code. Source gate PASS is limited to this hash; blind readers and owner approval remain.

`tasks done` wrote this finished copy but reported the open copy remained. It is untracked alongside three earlier duplicate open tickets. No deletion workaround was attempted; the review receipt and this done copy are the only staged output.
