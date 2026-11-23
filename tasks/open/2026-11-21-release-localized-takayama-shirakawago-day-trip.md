---
id: 2026-11-21-release-localized-takayama-shirakawago-day-trip
title: Release localized takayama-shirakawago-day-trip and nikko-day-trip-from-tokyo (en, ja, ko, zh-CN)
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-21T11:05:43Z
completed_at:
branch:
depends_on:
  - 2026-11-21-localize-takayama-shirakawago-day-trip-and
scope:
  - docs/article-localization/releases
---

# Release localized takayama-shirakawago-day-trip and nikko-day-trip-from-tokyo (en, ja, ko, zh-CN)

## Why

The Route B localization PR for Wave 3C Batch 6 (`2026-11-21-localize-takayama-shirakawago-day-trip-and`) merges validated `en`, `ja`, `ko`, and `zh-CN` documents plus 8 localized route diagram SVGs for both `howto/takayama-shirakawago-day-trip` and `howto/nikko-day-trip-from-tokyo` into the repository. Once merged and deployed to production, the new locales still need to be bundled, published to the production database, verified live, and recorded under `docs/article-localization/releases/`.

## Definition of done

- [ ] Production host has deployed the merged commit containing the localized content packs and all 8 SVG assets under `apps/web/public/guides/{takayama-shirakawago-day-trip,nikko-day-trip-from-tokyo}/`.
- [ ] Route B bundle is prepared via `prepare_route_b_bundle.py` against the pinned live `zh-TW` baseline and published via `publish_bundle.py` (only after explicit owner approval).
- [ ] All 8 new URLs (`/{en,ja,ko,zh-CN}/guides/howto/{takayama-shirakawago-day-trip,nikko-day-trip-from-tokyo}`) and their localized SVG assets return HTTP 200 with expected titles, diagrams, and links.
- [ ] A release record is committed under `docs/article-localization/releases/`.

## Steps

- [ ] Wait for explicit owner approval to deploy and publish localized Wave 3C batches.
- [ ] Verify production host is running the merged `main` commit and serving all 8 new SVG assets.
- [ ] Run `prepare_route_b_bundle.py` and `publish_bundle.py` on the production host (dry-run first, then apply) for `takayama-shirakawago-day-trip` and `nikko-day-trip-from-tokyo` (`en`, `ja`, `ko`, `zh-CN`).
- [ ] Verify all 8 live pages, SVG responses, and `hreflang` alternates.
- [ ] Write the release log under `docs/article-localization/releases/` and close this task.

## How to verify

```bash
for slug in takayama-shirakawago-day-trip nikko-day-trip-from-tokyo; do
  for loc in en ja ko zh-CN; do
    curl -sI "https://mokaair.com/${loc}/guides/howto/${slug}" | head -n 1
  done
done
```

## Notes

- Pinned `zh-TW` `source_sha256` at localization time:
  - `takayama-shirakawago-day-trip` (live v8): `20d77a324bb70643f4324219ee875738d6e16a2bb4b13aec213d7a0fa1ed60da`
  - `nikko-day-trip-from-tokyo` (live v8): `fe813e51ec6f7615a7ce4254b47e422adc40f83379c4ebbe6d4450661401e1e7`
- Combined independent review receipt (`route-b-review-v1`, 8/8 `PASS`, `open_findings: 0`):
  - `evidence_sha256`: `185a302d520ebabdaf19e37d6ac1a748c0ece8524a042da6c23d1119203f2649`
  - `review_sha256`: `eeb24d2e006265bee6f7e1a0b6bfedfe2ec1e1ad80aa91fe855160b10b8db4de`
- Do not deploy or run `publish_bundle.py` without explicit owner confirmation.
