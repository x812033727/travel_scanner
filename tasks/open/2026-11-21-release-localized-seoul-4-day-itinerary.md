---
id: 2026-11-21-release-localized-seoul-4-day-itinerary
title: Release localized seoul-4-day-itinerary (en, ja, ko, zh-CN)
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-21T04:50:37Z
completed_at:
branch:
depends_on:
  - 2026-11-21-localize-seoul-4-day-itinerary-into
scope:
  - docs/article-localization/releases/2026-11-21-seoul-4-day-itinerary
---

# Release localized seoul-4-day-itinerary (en, ja, ko, zh-CN)

## Why

`seoul-4-day-itinerary` (`kind: howto`) now has independently translated and reviewed `en`, `ja`, `ko`, and `zh-CN` documents plus localized SVG schematic area maps in the repository (see `tasks/done/2026-11-21-localize-seoul-4-day-itinerary-into.md`). Publish those four missing locales to production without altering the live `zh-TW` v12 document, and record public verification evidence.

## Definition of done

- [ ] `en`, `ja`, `ko`, and `zh-CN` are live on `mokaair.com` for `seoul-4-day-itinerary`, while `zh-TW` remains at v12 with normalized `source_sha256: 92a89aee443596da96a98ca0d8c29966a85707b52c430dbe0f038a65b9a94b2c`.
- [ ] Post-publish `guides-import` dry-run shows all five locales unchanged and unauthenticated public verification passes all five locales and localized SVGs.
- [ ] Release record (`README.md`, `evidence.json`, and `published-<locale>.json`) committed under `docs/article-localization/releases/2026-11-21-seoul-4-day-itinerary/`.

## Steps

- [ ] Confirm the localization PR (`2026-11-21-localize-seoul-4-day-itinerary-into`) is merged on `main` and CI is green on the merge commit.
- [ ] Confirm or run production deployment so the host serves the merged content pack and four localized SVGs (`deploy` skill; requires owner approval).
- [ ] Run host preflight: check `/root/travel-scanner-deploy.hold`, active locks, live `zh-TW` hash invariance (`92a89aee…`), and `publish_holds.json`.
- [ ] Run read-only `guides-import` / `publish_bundle.py dry-run` and verify expected creates (`en`, `ja`, `ko`, `zh-CN`) and zero changes to `zh-TW`.
- [ ] Obtain explicit owner approval with options, run `pg_dump` and verify TOC with `pg_restore --list`.
- [ ] Publish `en`, `ja`, `ko`, `zh-CN`, rebuild and check internal article links, and re-run dry-run to confirm all five locales are unchanged.
- [ ] Run unauthenticated public verification across all five locales, write release record under `docs/article-localization/releases/2026-11-21-seoul-4-day-itinerary/`, and open the release-record PR.

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --slug seoul-4-day-itinerary
npm run check:tasks
```

## Notes

- Pinned `zh-TW` baseline: live v12, `source_sha256: 92a89aee443596da96a98ca0d8c29966a85707b52c430dbe0f038a65b9a94b2c`.
- Expected new locale hashes (from `tasks/done/2026-11-21-localize-seoul-4-day-itinerary-into.md`):
  - `en`: `2a0fb8741e340213d34741df5d4ac240dd3de9a9717bf8781debe4c4decc790c`
  - `ja`: `7e35b675a33e5477dcf01a62d8bf53b0b4a3206c66f761160be6a1ab77762f5e`
  - `ko`: `674f79f6986c651a73903e214ae2934c35e3087c4e5165955803a3eff9034958`
  - `zh-CN`: `2c553935668cd8a81af3bcdbe34c1adc1ead850e59ba917ca21f14564793560a`

