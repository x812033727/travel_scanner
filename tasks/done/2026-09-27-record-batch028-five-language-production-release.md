---
id: 2026-09-27-record-batch028-five-language-production-release
title: Record Batch028 five-language production release
status: done
priority: P1
area: docs
owner: codex-batch028-release-record
claimed_at: 2026-09-27T20:25:41Z
created_at: 2026-09-27T20:25:36Z
completed_at: 2026-09-27T20:27:47Z
branch: codex/article-localization-028-release-record
depends_on: []
scope:
  - docs/article-localization/releases/batch028
---

# Record Batch028 five-language production release

## Why

The four WordPress presentation guides were published in five languages, then their English and Japanese page-builder diagrams needed narrow visual repairs. The guarded publication and the independent post-clear acceptance need a durable repository record that distinguishes merged content, published locales, deployed images, and browser verification.

## Definition of done

- [x] Record the four exact articles, their 16 new draft and published locales, and protection of the four original zh-TW documents.
- [x] Bind the content, diagram fixes, backup, journal, public/visual QA, hold clearance, and independent post-clear result to reviewed hashes.
- [x] State remaining limits and keep Batch029/030 separate from Batch028's completed release.

## Steps

- [x] Check the merged PR states and the v14 publisher journal/backup pins.
- [x] Read the sealed v17 rev4 raw, visual, clear, and independent post-clear receipts.
- [x] Write `docs/article-localization/releases/batch028/README.md` and run task/document checks.

## How to verify

Run `npm run check:tasks` and `git diff --check`. Verify the referenced local receipts' SHA-256 values and the merged state of PRs #852, #863, and #869. The independent post-clear receipt SHA-256 is `a1564df8111701c2bc466d3b47041d30beda6067155787c7482007d507ce4610`.

## Notes

Batch028 content v14 selected 16 target locales only; the original zh-TW rows stayed unchanged. The first English diagram audit and a later Japanese margin audit failed, and both failures remain preserved. PRs #863 and #869 repaired only the affected SVGs. A v17 rev3 contract had four impossible predicates, then rev4 passed against the original raw evidence. The first v17 privacy recheck used the wrong `/news/` path, then the correct `/life/` path passed. Clear helper v1 had the wrong English unavailable marker; v2 fixed it but did not bind dry-run versus real-clear gate mode; v3 added the mode binding and passed its guarded dry-run. Only a new clear-mode gate was used for the single real hold clearance. Independent post-clear review passed all checks; no physical device was used.
