---
id: 2026-11-22-release-localized-hong-kong-airport-to
title: Release localized hong-kong-airport-to-city and japan-car-rental-expressway-guide (en, ja, ko, zh-CN)
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-22T01:51:48Z
completed_at:
branch:
depends_on:
  - 2026-11-22-localize-hong-kong-airport-to-city
scope:
  - docs/article-localization/releases
---

# Release localized hong-kong-airport-to-city and japan-car-rental-expressway-guide (en, ja, ko, zh-CN)

## Why

The Route B localization PR for Wave 3C Batch 9 (`2026-11-22-localize-hong-kong-airport-to-city`) merges validated `en`, `ja`, `ko`, and `zh-CN` documents plus 8 localized 1600×900 SVG diagrams for both `howto/hong-kong-airport-to-city` and `howto/japan-car-rental-expressway-guide` into the repository. Once merged and deployed to production, the new locales still need to be bundled, published to the production database, verified live, and recorded under `docs/article-localization/releases/`.

## Definition of done

- [ ] Production host has deployed the merged commit containing the localized content packs and all 8 SVG assets under `apps/web/public/guides/{hong-kong-airport-to-city,japan-car-rental-expressway-guide}/`.
- [ ] Route B bundle is prepared via `prepare_route_b_bundle.py` against the pinned live `zh-TW` baseline and published via `publish_bundle.py` (only after explicit owner approval).
- [ ] All 8 new URLs (`/{en,ja,ko,zh-CN}/guides/howto/{hong-kong-airport-to-city,japan-car-rental-expressway-guide}`) and their localized SVG assets return HTTP 200 with expected titles, diagrams, and links.
- [ ] A release record is committed under `docs/article-localization/releases/`.

## Steps

- [ ] Wait for explicit owner approval to deploy and publish localized Wave 3C batches.
- [ ] Verify production host is running the merged `main` commit and serving all 8 new SVG assets.
- [ ] Run `prepare_route_b_bundle.py` and `publish_bundle.py` on the production host (dry-run first, then apply) for `hong-kong-airport-to-city` and `japan-car-rental-expressway-guide` (`en`, `ja`, `ko`, `zh-CN`).
- [ ] Verify all 8 live pages, SVG responses, and `hreflang` alternates.
- [ ] Write the release log under `docs/article-localization/releases/` and close this task.

## How to verify

```bash
for slug in hong-kong-airport-to-city japan-car-rental-expressway-guide; do
  for loc in en ja ko zh-CN; do
    curl -sI "https://mokaair.com/${loc}/guides/howto/${slug}" | head -n 1
  done
done
```

## Notes

- Pinned `zh-TW` `source_sha256` at localization time:
  - `hong-kong-airport-to-city` (live v8): `a007983a571ef7df3014b8673a503297b8ae2693e2dd03b774afc83c9139b04f`
  - `japan-car-rental-expressway-guide` (live v8): `689e7d89692f05c33efc49d8ad3d964179ddb8fd97c5b25859b0d04e7c6af51e`
- Combined independent review receipt (`route-b-review-v1`, 8/8 `PASS`, `open_findings: 0`):
  - `evidence_sha256`: `d1ccc125d17424a4c929957925fa53b5a107e8289cc671710b7eae46588d83f5`
  - `review_sha256`: `fe498760b7fa83c26e13b31a1ade5d7580224fbd717b24ae372925f453bfa6e9`
- Do not deploy or run `publish_bundle.py` without explicit owner confirmation.
