---
id: 2026-11-21-release-localized-seoul-where-to-stay
title: Release localized seoul-where-to-stay (en, ja, ko, zh-CN)
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-21T10:14:16Z
completed_at:
branch:
depends_on:
  - 2026-11-21-localize-seoul-where-to-stay-into
scope:
  - docs/article-localization/releases/2026-11-21-seoul-where-to-stay
---

# Release localized seoul-where-to-stay (en, ja, ko, zh-CN)

## Why

`seoul-where-to-stay` (`kind: howto`) now has independently translated and reviewed `en`, `ja`, `ko`, and `zh-CN` documents plus localized SVG area-and-airport-transit maps in the repository (see `tasks/done/2026-11-21-localize-seoul-where-to-stay-into.md`). Publish those four missing locales to production without altering the live `zh-TW` v6 document, and record public verification evidence.

## Definition of done

- [ ] `en`, `ja`, `ko`, and `zh-CN` are live on `mokaair.com` for `seoul-where-to-stay`, while `zh-TW` remains at v6 with normalized `source_sha256: 288e9bc10a2b14dc8f34aa31316168befb1f224fade50b13b5865b541c810cd0`.
- [ ] Post-publish `guides-import` dry-run shows all five locales unchanged and unauthenticated public verification passes all five locales and localized SVGs.
- [ ] Release record (`README.md`, `evidence.json`, and `published-<locale>.json`) committed under `docs/article-localization/releases/2026-11-21-seoul-where-to-stay/`.

## Steps

- [ ] Confirm the localization PR (`2026-11-21-localize-seoul-where-to-stay-into`) is merged on `main` and CI is green on the merge commit.
- [ ] Confirm or run production deployment so the host serves the merged content pack and four localized SVGs (`deploy` skill; requires owner approval).
- [ ] Run host preflight: check `/root/travel-scanner-deploy.hold`, active locks, live `zh-TW` hash invariance (`288e9bc1…`), and `publish_holds.json`.
- [ ] Run read-only `guides-import` / `publish_bundle.py dry-run` and verify expected creates (`en`, `ja`, `ko`, `zh-CN`) and zero changes to `zh-TW`.
- [ ] Obtain explicit owner approval with options, run `pg_dump` and verify TOC with `pg_restore --list`.
- [ ] Publish `en`, `ja`, `ko`, `zh-CN`, rebuild and check internal article links, and re-run dry-run to confirm all five locales are unchanged.
- [ ] Run unauthenticated public verification across all five locales, write release record under `docs/article-localization/releases/2026-11-21-seoul-where-to-stay/`, and open the release-record PR.

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --slug seoul-where-to-stay
npm run check:tasks
```

## Notes

- Pinned `zh-TW` baseline: live v6, `source_sha256: 288e9bc10a2b14dc8f34aa31316168befb1f224fade50b13b5865b541c810cd0`.
- Expected new locale hashes (from `tasks/done/2026-11-21-localize-seoul-where-to-stay-into.md`):
  - `en`: `ad1545bffea60391ab4a7c6967dea0182103f19af419e89b313c486e45b504ff`
  - `ja`: `fb4de3b1c5ecf628d801a682d3683d1aaa419a0d97c016e99119edbef916f918`
  - `ko`: `06b5d54c6dd4d879eb8cfe7ca12c8c499951eb40da8b6c8db44c9e9eb764df8d`
  - `zh-CN`: `360459d8aedae36d4e2579f10e99650ee76616e80343b16596892511bedd2cff`

