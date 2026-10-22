---
id: 2026-10-22-independently-review-c12-pyrex-treatment
title: Independently review C12 Pyrex Treatment sources
status: done
priority: P2
area: docs
owner: codex-c12-independent-review
claimed_at: 2026-10-22T14:12:47Z
created_at: 2026-10-22T14:11:43Z
completed_at: 2026-10-22T14:16:22Z
branch: codex/brand-story-pyrex-c12-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-review
---

# Independently review C12 Pyrex Treatment sources

## Why

The C12 Treatment was authored separately and needs a reviewer who directly reads each cited publisher page. The series slate's older laboratory-to-kitchen shorthand risks collapsing railway Nonex, 1915 consumer ovenware, current U.S. and French consumer glass, and Corning laboratory PYREX into one formula.

## Definition of done

- [x] A source-by-source M01–M17 verdict and six-chapter Treatment review are recorded with exact input SHA-256 hashes in a separate review folder.

## Steps

- [x] Reopen S1–S7 directly, including the Corning laboratory PDF and current European product page.
- [x] Distinguish museum retrospectives, brand marketing, product specification, and the museum's FAQ; identify any unsupported Treatment language.

## How to verify

Re-run `Get-FileHash docs/videos/story-everyday-pyrex-c12/treatment.md,docs/videos/story-everyday-pyrex-c12/source-matrix.md -Algorithm SHA256` and open the seven direct links in the receipt. `git diff --check` checks the review changes. No paid generation or script is part of this task.

## Notes

The direct S1 museum text records Bessie's cake as evenly cooked, easy to remove from the glass, and quicker than usual for metal or ceramic; it does not say her trial showed easy cleaning or observation through the glass. Thus M09 and the engine beat need a narrow author revision. The rain image in the cold open is supported by European brand source S4, but the local citation currently lists S1–S3 only. All other 16 M claims stayed within their source limits. No original Bessie diary, per-object assay, or universal glass safety rule was found or claimed.
