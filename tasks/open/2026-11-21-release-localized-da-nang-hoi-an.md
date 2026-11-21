---
id: 2026-11-21-release-localized-da-nang-hoi-an
title: Release localized da-nang-hoi-an-4-day-itinerary (en, ja, ko, zh-CN)
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-21T05:29:37Z
completed_at:
branch:
depends_on:
  - 2026-11-21-localize-da-nang-hoi-an-4
scope:
  - docs/article-localization/releases/2026-11-21-da-nang-hoi-an-4-day-itinerary
---

# Release localized da-nang-hoi-an-4-day-itinerary (en, ja, ko, zh-CN)

## Why

`da-nang-hoi-an-4-day-itinerary` (`kind: howto`) now has independently translated and reviewed `en`, `ja`, `ko`, and `zh-CN` documents plus localized SVG route zone maps in the repository (see `tasks/done/2026-11-21-localize-da-nang-hoi-an-4.md`). Publish those four missing locales to production without altering the live `zh-TW` v10 document, and record public verification evidence.

## Definition of done

- [ ] `en`, `ja`, `ko`, and `zh-CN` are live on `mokaair.com` for `da-nang-hoi-an-4-day-itinerary`, while `zh-TW` remains at v10 with normalized `source_sha256: cef37cac40c3be0921e18fc51e91169ec06783562744e029c0e1fd72b95f8fec`.
- [ ] Post-publish `guides-import` dry-run shows all five locales unchanged and unauthenticated public verification passes all five locales and localized SVGs.
- [ ] Release record (`README.md`, `evidence.json`, and `published-<locale>.json`) committed under `docs/article-localization/releases/2026-11-21-da-nang-hoi-an-4-day-itinerary/`.

## Steps

- [ ] Confirm the localization PR (`2026-11-21-localize-da-nang-hoi-an-4`) is merged on `main` and CI is green on the merge commit.
- [ ] Confirm or run production deployment so the host serves the merged content pack and four localized SVGs (`deploy` skill; requires owner approval).
- [ ] Run host preflight: check `/root/travel-scanner-deploy.hold`, active locks, live `zh-TW` hash invariance (`cef37cac…`), and `publish_holds.json`.
- [ ] Run read-only `guides-import` / `publish_bundle.py dry-run` and verify expected creates (`en`, `ja`, `ko`, `zh-CN`) and zero changes to `zh-TW`.
- [ ] Obtain explicit owner approval with options, run `pg_dump` and verify TOC with `pg_restore --list`.
- [ ] Publish `en`, `ja`, `ko`, `zh-CN`, rebuild and check internal article links, and re-run dry-run to confirm all five locales are unchanged.
- [ ] Run unauthenticated public verification across all five locales, write release record under `docs/article-localization/releases/2026-11-21-da-nang-hoi-an-4-day-itinerary/`, and open the release-record PR.

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --slug da-nang-hoi-an-4-day-itinerary
npm run check:tasks
```

## Notes

- Pinned `zh-TW` baseline: live v10, `source_sha256: cef37cac40c3be0921e18fc51e91169ec06783562744e029c0e1fd72b95f8fec`.
- Expected new locale hashes (from `tasks/done/2026-11-21-localize-da-nang-hoi-an-4.md`):
  - `en`: `75ae13a06d21901e96ef563001ac915dd3ced24e9c593bbc1007be7cb2fa097e`
  - `ja`: `6967d5b92646a1d1ba9755150770212bf0c9ef085141005cefbd570e04b83c20`
  - `ko`: `eba86a7b96ca8f1419396cf4ffaafce25a0430bbf5e2cafb624b0e0052be4675`
  - `zh-CN`: `490a5843f74849cafe12d26103565793a8d647d9d32c311561a7d9532154ce19`

