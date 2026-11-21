---
id: 2026-11-20-release-localized-japan-shinkansen-ticket-guide
title: Release localized japan-shinkansen-ticket-guide (en, ja, ko, zh-CN)
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-20T16:51:16Z
completed_at:
branch:
depends_on:
  - 2026-11-20-localize-japan-shinkansen-ticket-guide-into
scope:
  - docs/article-localization/releases/2026-11-20-japan-shinkansen-ticket-guide
---

# Release localized japan-shinkansen-ticket-guide (en, ja, ko, zh-CN)

## Why

`japan-shinkansen-ticket-guide` (`kind: howto`) now has independently translated and reviewed `en`, `ja`, `ko`, and `zh-CN` documents plus localized SVG decision trees in the repository (see `tasks/done/2026-11-20-localize-japan-shinkansen-ticket-guide-into.md`). Publish those four missing locales to production without altering the live `zh-TW` v10 document, and record public verification evidence.

## Definition of done

- [ ] `en`, `ja`, `ko`, and `zh-CN` are live on `mokaair.com` for `japan-shinkansen-ticket-guide`, while `zh-TW` remains at v10 with normalized `source_sha256: e785b0d683a434305a1c3cdf7d040bd4edaecae9ab4a1cebfddc6bea5a1d0814`.
- [ ] Post-publish `guides-import` dry-run shows all five locales unchanged and `verify_public.py` passes all five locales and localized SVGs.
- [ ] Release record (`README.md`, `evidence.json`, and `published-<locale>.json`) committed under `docs/article-localization/releases/2026-11-20-japan-shinkansen-ticket-guide/`.

## Steps

- [ ] Confirm the localization PR (`2026-11-20-localize-japan-shinkansen-ticket-guide-into`) is merged on `main` and CI is green on the merge commit.
- [ ] Confirm or run production deployment so the host serves the merged content pack and four localized SVGs (`deploy` skill; requires owner approval).
- [ ] Run host preflight: check `/root/travel-scanner-deploy.hold`, active locks, live `zh-TW` hash invariance (`e785b0d6…`), and `publish_holds.json`.
- [ ] Run read-only `guides-import` / `publish_bundle.py dry-run` and verify expected creates (`en`, `ja`, `ko`, `zh-CN`) and zero changes to `zh-TW`.
- [ ] Obtain explicit owner approval with options, run `pg_dump` and verify TOC with `pg_restore --list`.
- [ ] Publish `en`, `ja`, `ko`, `zh-CN`, rebuild and check internal article links, and re-run dry-run to confirm all five locales are unchanged.
- [ ] Run unauthenticated public verification (`verify_public.py`) across all five locales, write release record under `docs/article-localization/releases/2026-11-20-japan-shinkansen-ticket-guide/`, and open the release-record PR.

## How to verify

```bash
cd apps/api && uv run python ../../docs/article-localization/verify_public.py --slug japan-shinkansen-ticket-guide
npm run check:tasks
```

## Notes

- Pinned `zh-TW` baseline: live v10, `source_sha256: e785b0d683a434305a1c3cdf7d040bd4edaecae9ab4a1cebfddc6bea5a1d0814`.
- Expected new locale hashes (from `tasks/done/2026-11-20-localize-japan-shinkansen-ticket-guide-into.md`):
  - `en`: `21a6b40604c1017b5eaa417d9f52a86a01001eab1a8408f68e617795f9d1d305`
  - `ja`: `64ad592439186a861af742c576ff52c9a73bae51d753d9d54695f8feb53effed`
  - `ko`: `b3a7004f27d95444630c44e3adb8f37c63dbadbd396661e8e333538548c2e210`
  - `zh-CN`: `d1fd644bd5d034a9c125bdc84b8a2e2f47d30baf47bbbe1c7cd821bf1a476738`

