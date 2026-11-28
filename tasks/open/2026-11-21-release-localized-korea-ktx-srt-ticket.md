---
id: 2026-11-21-release-localized-korea-ktx-srt-ticket
title: Release localized korea-ktx-srt-ticket-guide and jeju-3-day-itinerary (en, ja, ko, zh-CN)
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-21T17:10:52Z
completed_at:
branch:
depends_on:
  - 2026-11-21-localize-korea-ktx-srt-ticket-guide
scope:
  - docs/article-localization/releases
---

# Release localized korea-ktx-srt-ticket-guide and jeju-3-day-itinerary (en, ja, ko, zh-CN)

## Why

The Route B localization PR for Wave 3C Batch 8 (`2026-11-21-localize-korea-ktx-srt-ticket-guide`) merges validated `en`, `ja`, `ko`, and `zh-CN` documents plus 8 localized 1600×900 SVG diagrams for both `howto/korea-ktx-srt-ticket-guide` and `howto/jeju-3-day-itinerary` into the repository. Once merged and deployed to production, the new locales still need to be bundled, published to the production database, verified live, and recorded under `docs/article-localization/releases/`.

## Definition of done

- [ ] Production host has deployed the merged commit containing the localized content packs and all 8 SVG assets under `apps/web/public/guides/{korea-ktx-srt-ticket-guide,jeju-3-day-itinerary}/`.
- [ ] Route B bundle is prepared via `prepare_route_b_bundle.py` against the pinned live `zh-TW` baseline and published via `publish_bundle.py` (only after explicit owner approval).
- [ ] All 8 new URLs (`/{en,ja,ko,zh-CN}/guides/howto/{korea-ktx-srt-ticket-guide,jeju-3-day-itinerary}`) and their localized SVG assets return HTTP 200 with expected titles, diagrams, and links.
- [ ] A release record is committed under `docs/article-localization/releases/`.

## Steps

- [ ] Wait for explicit owner approval to deploy and publish localized Wave 3C batches.
- [ ] Verify production host is running the merged `main` commit and serving all 8 new SVG assets.
- [ ] Run `prepare_route_b_bundle.py` and `publish_bundle.py` on the production host (dry-run first, then apply) for `korea-ktx-srt-ticket-guide` and `jeju-3-day-itinerary` (`en`, `ja`, `ko`, `zh-CN`).
- [ ] Verify all 8 live pages, SVG responses, and `hreflang` alternates.
- [ ] Write the release log under `docs/article-localization/releases/` and close this task.

## How to verify

```bash
for slug in korea-ktx-srt-ticket-guide jeju-3-day-itinerary; do
  for loc in en ja ko zh-CN; do
    curl -sI "https://mokaair.com/${loc}/guides/howto/${slug}" | head -n 1
  done
done
```

## Notes

- Pinned `zh-TW` `source_sha256` at localization time:
  - `korea-ktx-srt-ticket-guide` (live v10): `a1f2009e10ef794a922f992b0be47e4fd7ecc1e28fe7a4c603b12d0fa76ce0ee`
  - `jeju-3-day-itinerary` (live v8): `b90731ffa49e2dd425111e9a0e7b0b12fb1f030539050ddac839c77e4855e164`
- Combined independent review receipt (`route-b-review-v1`, 8/8 `PASS`, `open_findings: 0`):
  - `evidence_sha256`: `c306c969cd00a840762960d690ff11e1773e3189dd7f1a05d395327d421bc507`
  - `review_sha256`: `1dc16df1c4353e6767b90e95587410fc8f4502ab74bfb57bc532d4c89d7d2129`
- Do not deploy or run `publish_bundle.py` without explicit owner confirmation.
