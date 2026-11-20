---
id: 2026-11-20-release-localized-busan-3-day-itinerary
title: Release localized busan-3-day-itinerary (en, ja, ko, zh-CN)
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-20T18:02:57Z
completed_at:
branch:
depends_on:
  - 2026-11-20-localize-busan-3-day-itinerary-into
scope:
  - docs/article-localization/releases/2026-11-20-busan-3-day-itinerary
---

# Release localized busan-3-day-itinerary (en, ja, ko, zh-CN)

## Why

`busan-3-day-itinerary` (`kind: howto`) now has independently translated and reviewed `en`, `ja`, `ko`, and `zh-CN` documents plus localized SVG schematic area maps in the repository (see `tasks/done/2026-11-20-localize-busan-3-day-itinerary-into.md`). Publish those four missing locales to production without altering the live `zh-TW` v8 document, and record public verification evidence.

## Definition of done

- [ ] `en`, `ja`, `ko`, and `zh-CN` are live on `mokaair.com` for `busan-3-day-itinerary`, while `zh-TW` remains at v8 with normalized `source_sha256: afde92628b0224e33c9b7a5a2b319b504b5cfdae17d23a9bf91c3a3d9123c21f`.
- [ ] Post-publish `guides-import` dry-run shows all five locales unchanged and `verify_public.py` passes all five locales and localized SVGs.
- [ ] Release record (`README.md`, `evidence.json`, and `published-<locale>.json`) committed under `docs/article-localization/releases/2026-11-20-busan-3-day-itinerary/`.

## Steps

- [ ] Confirm the localization PR (`2026-11-20-localize-busan-3-day-itinerary-into`) is merged on `main` and CI is green on the merge commit.
- [ ] Confirm or run production deployment so the host serves the merged content pack and four localized SVGs (`deploy` skill; requires owner approval).
- [ ] Run host preflight: check `/root/travel-scanner-deploy.hold`, active locks, live `zh-TW` hash invariance (`afde9262…`), and `publish_holds.json`.
- [ ] Run read-only `guides-import` / `publish_bundle.py dry-run` and verify expected creates (`en`, `ja`, `ko`, `zh-CN`) and zero changes to `zh-TW`.
- [ ] Obtain explicit owner approval with options, run `pg_dump` and verify TOC with `pg_restore --list`.
- [ ] Publish `en`, `ja`, `ko`, `zh-CN`, rebuild and check internal article links, and re-run dry-run to confirm all five locales are unchanged.
- [ ] Run unauthenticated public verification (`verify_public.py`) across all five locales, write release record under `docs/article-localization/releases/2026-11-20-busan-3-day-itinerary/`, and open the release-record PR.

## How to verify

```bash
cd apps/api && uv run python ../../docs/article-localization/verify_public.py --slug busan-3-day-itinerary
npm run check:tasks
```

## Notes

- Pinned `zh-TW` baseline: live v8, `source_sha256: afde92628b0224e33c9b7a5a2b319b504b5cfdae17d23a9bf91c3a3d9123c21f`.
- Expected new locale hashes (from `tasks/done/2026-11-20-localize-busan-3-day-itinerary-into.md`):
  - `en`: `fe730d1622809868d0ef99db8a3604e4dfa6ef2cfb7a00cc9b703b59e9abd9c7`
  - `ja`: `749917e4f0f1cff0851fc0276068c9dfdb4731b00ce06c6b3d59f21dcc46112c`
  - `ko`: `56d00e2185bcab02f8d78ed97ca1d88d6fcc9c7cf8b19d1f687a83dba0be81d7`
  - `zh-CN`: `57f9d93356e4d59f21c87a38f8aa295565c8de2ea5d3c952cd575d2fdec70189`

