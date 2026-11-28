---
id: 2026-11-21-release-localized-kansai-rail-passes-guide
title: Release localized kansai-rail-passes-guide and osaka-kyoto-nara-4-day-itinerary (en, ja, ko, zh-CN)
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-21T15:35:36Z
completed_at:
branch:
depends_on:
  - 2026-11-21-localize-kansai-rail-passes-guide-and
scope:
  - docs/article-localization/releases
---

# Release localized kansai-rail-passes-guide and osaka-kyoto-nara-4-day-itinerary (en, ja, ko, zh-CN)

## Why

The Route B localization PR for Wave 3C Batch 7 (`2026-11-21-localize-kansai-rail-passes-guide-and`) merges validated `en`, `ja`, `ko`, and `zh-CN` documents plus 8 localized 1600×900 SVG diagrams for both `howto/kansai-rail-passes-guide` and `howto/osaka-kyoto-nara-4-day-itinerary` into the repository. Once merged and deployed to production, the new locales still need to be bundled, published to the production database, verified live, and recorded under `docs/article-localization/releases/`.

## Definition of done

- [ ] Production host has deployed the merged commit containing the localized content packs and all 8 SVG assets under `apps/web/public/guides/{kansai-rail-passes-guide,osaka-kyoto-nara-4-day-itinerary}/`.
- [ ] Route B bundle is prepared via `prepare_route_b_bundle.py` against the pinned live `zh-TW` baseline and published via `publish_bundle.py` (only after explicit owner approval).
- [ ] All 8 new URLs (`/{en,ja,ko,zh-CN}/guides/howto/{kansai-rail-passes-guide,osaka-kyoto-nara-4-day-itinerary}`) and their localized SVG assets return HTTP 200 with expected titles, diagrams, and links.
- [ ] A release record is committed under `docs/article-localization/releases/`.

## Steps

- [ ] Wait for explicit owner approval to deploy and publish localized Wave 3C batches.
- [ ] Verify production host is running the merged `main` commit and serving all 8 new SVG assets.
- [ ] Run `prepare_route_b_bundle.py` and `publish_bundle.py` on the production host (dry-run first, then apply) for `kansai-rail-passes-guide` and `osaka-kyoto-nara-4-day-itinerary` (`en`, `ja`, `ko`, `zh-CN`).
- [ ] Verify all 8 live pages, SVG responses, and `hreflang` alternates.
- [ ] Write the release log under `docs/article-localization/releases/` and close this task.

## How to verify

```bash
for slug in kansai-rail-passes-guide osaka-kyoto-nara-4-day-itinerary; do
  for loc in en ja ko zh-CN; do
    curl -sI "https://mokaair.com/${loc}/guides/howto/${slug}" | head -n 1
  done
done
```

## Notes

- Pinned `zh-TW` `source_sha256` at localization time:
  - `kansai-rail-passes-guide` (live v8): `88de29318908fd9b1a607322c2456483636086f3a6eae8d73cb1bb0d3c2962cc`
  - `osaka-kyoto-nara-4-day-itinerary` (live v8): `dbfed6f33456622b99e16d1a7e1d219d5ce566343e75660aac33670baede4507`
- Combined independent review receipt (`route-b-review-v1`, 8/8 `PASS`, `open_findings: 0`):
  - `evidence_sha256`: `345ef52c1630b7fe676e18a11618e0871b15aaedff567ecd475af1f370b376b2`
  - `review_sha256`: `54463afc9650b9cdd617ef120f8e1907319ad895664c296bb8cd0d62c434c376`
- Do not deploy or run `publish_bundle.py` without explicit owner confirmation.
