---
id: 2026-09-28-review-batch041-keyword-and-title-summary
title: Review Batch041 keyword and title summary blocks
status: done
priority: P2
area: docs
owner: codex-batch041-summary
claimed_at: 2026-09-29T05:25:17Z
created_at: 2026-09-28T17:31:06Z
completed_at: 2026-09-29T05:37:53Z
branch: codex/batch041-summary-correction
depends_on:
  - 2026-09-28-localize-seo-keyword-and-title-guides
scope:
  - apps/api/app/guides/content/seo-keyword-research.json
  - apps/api/app/guides/content/seo-title-writing.json
  - docs/article-localization/batch041-summary-correction.md
---

# Review Batch041 keyword and title summary blocks

## Why

Strict intake reports one inherited source failure in each of seo-keyword-research
and seo-title-writing: their first block is paragraph instead of summary.
Localization preserves the published source and has not silently rewritten it.

## Definition of done

- [x] Review the source correction and make a separate versioned change if accepted.
- [x] Keep all five editions consistent without deleting details or altering facts.
- [x] Re-run strict intake, locale checks and exact review/source hash binding.

## How to verify

Run intake_check.py --from-content for each slug and scoped pack lint. Internal
article targets and SVG numeric checks already passed. All five locales will be
checked; the Japanese title document has a separately tracked intake matcher
false positive, fixed under 2026-09-29-intake-japanese-self-reference.

## Notes

Leave unclaimed until localization scope is released. Any source change requires
the guarded reconciliation path before production import.

Claimed after localization #940 merged and its ticket moved to done. The remaining
#959 overlap is an unchanged aggregate CI train containing #940; its two pack
bytes match main, and the original author's content worktree is clean. No active
claim covers either pack. New work uses a separate branch from main `8be1cf9b`.

The accepted correction promotes the original second paragraph's three verbatim
sentences to the first summary block and retains the original first paragraph
immediately afterward. The other 30 blocks, all metadata and all assets remain
unchanged. Two independent reviews accepted all ten locale documents. The old
T2 frozen candidate remains immutable; changed source and target hashes require
explicit source reconciliation and newly bound release evidence before publishing.

## Completion evidence

See `docs/article-localization/batch041-summary-correction.md` for before/after
source and locale hashes, two independent content review receipts, preserved
asset hashes, strict-intake results and the formal-release handoff.

- Applied ten three-sentence summaries; no facts, dates, assets or later blocks changed.
- Real strict intake: 10/10 pass without disabled checks or higher limits.
- New matcher regression: old tool 9 failed/12 passed; corrected tool 21 passed.
- Installed targeted pytest (intake, content pack, content links): 33 passed,
  5 isolated-PostgreSQL skips. Scoped Ruff/mypy and six skill contract tests pass.
- Independent code review passed. Twenty standalone desktop/mobile previews
  pass DOM checks and changed-region visual review; forty image loads succeed.
- Original T2 freeze is immutable. The new two-source/eight-target hashes require
  separately approved source reconciliation, release rebinding and PostgreSQL
  rehearsal before publication. The original release task remains open.

This ticket closes the reviewed local correction only, within a draft PR;
it does not mark source publication or the original localization release done.
