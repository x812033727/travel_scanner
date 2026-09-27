---
id: 2026-09-27-localize-wordpress-500-error-and-comment
title: Localize WordPress 500 error and comment moderation Batch032 Pair A
status: done
priority: P2
area: api
owner: codex-batch032-pair-a
claimed_at: 2026-09-27T13:43:13Z
created_at: 2026-09-27T13:42:51Z
completed_at: 2026-09-27T14:05:58Z
branch: codex/article-localization-032-pair-a
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-500-error.json
  - apps/api/app/guides/content/wordpress-comment-spam.json
  - apps/web/public/guides/wordpress-500-error
  - apps/web/public/guides/wordpress-comment-spam
---

# Localize WordPress 500 error and comment moderation Batch032 Pair A

## Why

Both articles are published only in zh-TW v4. Readers in en, ja, ko and zh-CN
need full articles and localized text-bearing diagrams/covers. This branch
starts from local source-link correction `a4d3cc5070f43cf6d6133dbd3f464727dfbc22da`;
its `wordpress-comment-spam` zh-TW plain-text marker is a provisional source
because the corrected revision is not yet published on production.

## Definition of done

- [x] Eight complete locale documents preserve source structure, audience,
      eligibility, code literals, source URLs/check dates and conditional links.
- [x] Twenty-four new localized assets render without clipping or missing
      glyphs; the six original assets and both zh-TW documents stay unchanged.
- [x] Pack lint, targeted API tests, exact source/asset comparisons, link policy
      and image renders pass. Commit locally without push, PR or production write.

## Steps

- [x] Translate all fields of `wordpress-500-error` and `wordpress-comment-spam`
      into en, ja, ko and zh-CN.
- [x] Localize each hero SVG, hero JPG and diagram SVG and visually review.
- [x] Record the unpublished comment-spam source-fix prerequisite and hashes.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --slug wordpress-500-error
--slug wordpress-comment-spam` and targeted guide pack/link/ingest tests from
`apps/api`; run `npm run check:tasks` from the repo root. Compare source pack
and original image hashes to the Batch032 inventory and corrected parent
commit, then render SVGs and review every locale image.

## Notes

Read-only Batch032 inventory:
`C:\Users\x8120\.codex\article-localization-release\batch032-inventory\batch032-candidate-inventory.json`,
SHA-256 `fa3262b33c0948c125f4a46b93caeade730723d1428ffed0ee8d5d6ccd3a4d73`.
Published source models at that snapshot: 500-error zh-TW v4
`e378eec5e25ecaf20a325f248adff3b805ea53fdc87ffc764a11fda157942c83`;
comment-spam zh-TW v4
`ef124872b2da725961846d3bb941f65a51b953f8a2c6ed9ac8f0df88467da98d`.
The latter is deliberately superseded in this local branch by the single
TextInline correction at block 9; publish that corrected zh-TW revision and
recapture its new version/hash before Batch032 translations can publish.
The 500-error links to already five-language backup and maintenance articles.
Comment-spam links to `wordpress-member-registration` and
`wordpress-contact-forms`, currently zh-TW-only, so target-locale links must
render as plain text until those destinations publish in that locale.

Local validation receipt: `C:\Users\x8120\.codex\article-localization-release\batch032-pair-a\validation.json`,
SHA-256 `6955df72ae1d5216f3dfabb45a2c8e82fd025ce50ef931d7ae2d46a378dd0e75`.
It confirms eight documents, 24 new assets, six unchanged originals, equal
block type/order, preserved source URL/check dates and credits, and link policy.
All six four-locale contact sheets were visually reviewed at full resolution;
no clipping, overlap or missing glyphs were observed. Pack lint returned zero
errors; its no-summary and one English length messages are advisory warnings.
Targeted API pack/link/ingest tests: 67 passed, 5 skipped. Task check: 929
files validated, with pre-existing stale-claim warnings. The local `uv run`
venv setup hit a Windows PE resource access-denied error; the same commands
ran from this worktree using the already initialized Batch031 API venv's
Python, with `PYTHONPATH=.` so imports resolved to this worktree.
