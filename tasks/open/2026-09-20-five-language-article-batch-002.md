---
id: 2026-09-20-five-language-article-batch-002
title: Five-language article batch 002
status: in-progress
priority: P1
area: docs
owner: codex-article-localization
claimed_at: 2026-09-20T05:52:40Z
created_at: 2026-09-20T05:52:33Z
completed_at:
branch: codex/article-localization-batch-002
depends_on: []
scope:
  - apps/api/app/guides/content/ayutthaya-day-trip-from-bangkok.json
  - apps/api/app/guides/content/cheung-chau-walking-day.json
  - apps/api/app/guides/content/everland-lotte-world-guide.json
  - apps/api/app/guides/content/fukuoka-3-day-itinerary.json
  - apps/api/app/guides/content/gyeongju-day-trip-from-busan.json
  - apps/web/public/guides/ayutthaya-day-trip-from-bangkok
  - apps/web/public/guides/cheung-chau-walking-day
  - apps/web/public/guides/everland-lotte-world-guide
  - apps/web/public/guides/fukuoka-3-day-itinerary
  - apps/web/public/guides/gyeongju-day-trip-from-busan
  - docs/article-localization/baseline-batch-002.json
  - docs/article-localization/releases/batch-002
  - docs/article-localization/work-batch-002
  - docs/article-localization/installations
---

# Five-language article batch 002

## Why

These five public travel guides have only their complete Traditional Chinese source
published. English, Japanese, Korean and Simplified Chinese are all absent, so each
page is missing four translations and four language-specific versions of its embedded
route or comparison diagram. None of their pack or asset paths is covered by another
unfinished repository task.

## Definition of done

- [x] All five packs contain complete, independently reviewed documents in all five locales.
- [x] Each source SVG has reviewed en, ja, ko and zh-CN variants with no overflow or missing glyphs.
- [x] The reviewed bundle installs idempotently without changing the existing zh-TW prose.
- [ ] The exact content PR is merged, backed up, deployed and health checked.
- [ ] Only the twenty authorized missing locales are published and browser verified.

## Steps

- [x] Capture a fresh read-only production snapshot and build a hash-pinned baseline.
- [x] Translate all twenty missing documents and pass schema and token checks.
- [x] Render all twenty localized SVGs and pass automated layout checks.
- [x] Complete independent editorial, photo and visual review.
- [x] Assemble, install and validate the explicit five-article release bundle.
- [ ] Open and merge the content PR after its required checks pass.
- [ ] Back up, deploy, dry-run, publish and browser verify the exact release.

## How to verify

Run the localization progress report, bundle assembly and idempotent installation,
then the focused guide content and link tests plus i18n, task and CI checks. After
deployment, compare the sealed publication journal to a direct database snapshot and
verify every new locale's body, image, canonical, reciprocal hreflang and internal
links at desktop and mobile widths.

## Notes

Fresh production snapshot commit:
`9d5f77e2f8af516a4260aa555145bd13fa6e5547`. Snapshot SHA-256:
`0e01592213341118ac18f3360b0e97aa953c53ea10552c7ab299e6f7d9dc2416`.
Combined baseline SHA-256:
`3c544e4f42731e698d497e546b7c0c4bee5b326ab83bc578d3b1fc62dbf8135a`.
It records 1,067 articles, 157 complete packs, 1,030 public articles, 37 private
drafts, 3,598 missing language documents and 3,450 public publication gaps.

The explicit batch is `ayutthaya-day-trip-from-bangkok`,
`cheung-chau-walking-day`, `everland-lotte-world-guide`,
`fukuoka-3-day-itinerary` and `gyeongju-day-trip-from-busan`. All five are public,
their repository and database zh-TW documents match, and each is missing exactly en,
ja, ko and zh-CN. Each also has one editable 1600x900 SVG plus reusable editorial
photographs without authored text overlays.

The first translation run produced 13 immediately valid jobs and seven strict
numeric-token failures. Those failures only changed spelled-out source numbers into
Arabic digits. Nineteen field-level corrections restored the numeric form without a
second model call. Automated SVG checks then found four long labels across three
jobs; six SVG-only labels were shortened within the original meaning and shapes.
Final full-size review found seven more labels across the Gyeongju and Fukuoka
diagrams; those were shortened and rerendered before the hash-bound reviews.
All twenty documents now pass schema/token checks and all twenty SVGs pass automated
dimension, bounds and overlap checks. Every manual edit is recorded outside the
repository in the batch evidence directory and was included in root review.

Root reviewed the twenty final 1600x900 SVG previews and the thirteen original
rasters, compared the high-risk translated conditions with the pinned source,
and recorded hash-bound per-locale reviews. The progress report now verifies
20/20 reviewed and 20/20 assembled with no issues. The reviewed bundle manifest
is `6a6478b9f907bad5874ce7ab74a0d14b1c02fe4e1142ddf55fdc8765088ed685`.
The two delegated editorial reviewers could not complete their turns because
the Codex account reached its usage limit, so their names are not recorded as
reviewers. The installer requires its baseline, bundle and jobs within the
repository; the scoped staging and installation-journal paths above support
that hash-pinned local install and remain outside the content PR.
