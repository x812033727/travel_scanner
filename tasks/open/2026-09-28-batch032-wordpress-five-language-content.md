---
id: 2026-09-28-batch032-wordpress-five-language-content
title: Integrate Batch032 four WordPress articles in five languages
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-28T01:06:01Z
completed_at:
branch: codex/article-localization-032-content
depends_on:
  - 2026-09-27-correct-three-wordpress-maintenance-glossary-links
scope:
  - apps/api/app/guides/content/wordpress-500-error.json
  - apps/api/app/guides/content/wordpress-comment-spam.json
  - apps/api/app/guides/content/wordpress-performance-plugins.json
  - apps/api/app/guides/content/wordpress-reset-safely.json
  - apps/web/public/guides/wordpress-500-error
  - apps/web/public/guides/wordpress-comment-spam
  - apps/web/public/guides/wordpress-performance-plugins
  - apps/web/public/guides/wordpress-reset-safely
  - tasks/done/2026-09-27-localize-wordpress-500-error-and-comment.md
  - tasks/done/2026-09-27-localize-wordpress-performance-plugins-and-safe.md
---

# Integrate Batch032 four WordPress articles in five languages

## Why

Four published WordPress maintenance articles have only zh-TW bodies. Batch032
adds complete en, ja, ko and zh-CN documents and language-specific covers and
diagrams. The three unrelated glossary links in the zh-TW originals were
corrected by #876 before this integration; the corrected originals must remain
byte-for-byte unchanged here.

## Definition of done

- [x] All 16 target documents and 48 language-specific assets are present; the
      four corrected zh-TW documents and original art match merged main.
- [x] Scoped pack lint, link/pack/ingest tests, image hash and layout checks pass.
- [ ] Open a narrow draft PR after #875 merges, without deploying or publishing.

## Steps

- [x] Integrate Pair A `ca9323df` and Pair B `3bde09e3` onto merged #876 main.
- [x] Refresh the link eligibility evidence in the Pair A/B handover notes.
- [x] Rebase onto main after #875 and verify the final PR file list.

## How to verify

From `apps/api`, run `python -m app.guides.pack_cli lint --slug
wordpress-500-error --slug wordpress-comment-spam --slug
wordpress-performance-plugins --slug wordpress-reset-safely`, then `python -m
pytest tests/test_guides_content_pack.py tests/test_guides_links.py
tests/test_guides_content_links.py tests/test_guides_pack_ingest.py -q`.
From the repository root run `npm run check:tasks`. Compare all four `zh-TW`
locale objects to `origin/main`; compare 48 files to the Pair A/B asset
manifests and inspect all 12 four-locale contact sheets.

## Notes

Base `origin/main` at integration: `4db43425` (includes merged source-fix
PR #876). Pair commits cherry-picked cleanly as `a35d9144` and `1af48443`.
The four `zh-TW` locale objects exactly equal this main. The Pair A/B branch
receipts are under `C:\Users\x8120\.codex\article-localization-release\batch032-pair-a`
and `batch032-pair-b`; their asset manifests contain 24 matching files each.
All non-locale root metadata also equals main. Integrated scoped pack lint
checked four entries with zero errors (only no-summary and three English
length advisories); targeted API tests passed `73 passed, 11 skipped`.
`npm run check:tasks` validated 947 task files with only pre-existing stale
claim/scope warnings. All 48 new assets match the recorded manifest SHA-256
values; 12 four-language contact sheets and 288 image text-fit entries were
independently reviewed with no observed clipping or overflow.

Independent read-only publication snapshot at 2026-09-28T00:03:32Z, SHA
`b7417d7b8f3ee636a2b50c58925f7b7e6b940764cb23a9ed3978c5a99bc3ac5a`:
28 of 40 ArticleInline references resolve to published same-locale targets;
12 remain plain text. `wordpress-contact-forms` and
`wordpress-theme-selection` now have five published locales, superseding the
older Pair A/B inventory prose. `wordpress-member-registration`,
`website-cache-cdn`, and `pagespeed-performance-review` remain zh-TW-only in
that snapshot. Recheck eligibility before publishing.

Merged code is not a published source revision. The three corrected zh-TW
originals still need a guarded source-only publication, followed by exact
production version/hash capture and translation source rebind before the 16
new locales may publish. Do not infer publication from this draft PR.

After #875 merged, this branch rebased onto exact main
`4b6c5cd99fa9eab3b658d5b6cf639cb001f8fc3e`. The final comparison has
55 files: four packs, 48 new assets and three task files, with no other paths.
All four zh-TW locale objects and root metadata still equal main; 48 image
hashes match. Scoped lint returned zero errors, targeted API tests returned
`73 passed, 11 skipped`, and task validation and `git diff --check` passed.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-batch032-content-pr (since 2026-09-28T01:06:06Z) was stale and is released so it stops locking its scope. Landed: #878. Still open: Open a narrow draft PR after #875 merges, without deploying or publishing.
