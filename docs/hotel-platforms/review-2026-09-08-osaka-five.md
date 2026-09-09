# Osaka five-hotel platform review — 2026-09-08

## Merge and scope

PR #344 was explicitly authorized for merge. Main had advanced to `b060227`, so the first
merge was correctly blocked by required checks. Synced main, then verified all eight CI
checks at head `873e876764b031e85271db16ee0485d86334f1b1` (PR 34175671037,
push 34175669025), `CLEAN / MERGEABLE`, and squash-merged with `--match-head-commit`.
GitHub confirmed merge `2e5e9feb68181d809653ad9ac67cf761e0f98950` at 01:15:52 UTC.

The continuation uses `codex/hotel-content-review-osaka` in the existing isolated clean
worktree, branched from that merged main. The original dirty workspace is preserved.
This batch adds **four missing platform URLs to existing slots**, not new hotel identities.
It does not deploy images, migrate, modify product facts or change rollout/affiliate settings.

## Evidence and independent decisions

| Existing hotel | Official street identity | Official / Trip | New Agoda candidate |
| --- | --- | --- | --- |
| ホテルヴィスキオ大阪 | 大阪市北区芝田2丁目4番10号 | Both approved | Pending |
| ホテル阪急レスパイア大阪 | 大阪府大阪市北区大深町1番1号 | Both approved | Pending |
| ホテルインターゲート大阪 梅田 | 大阪府大阪市北区梅田2-5-2 | Both approved | Pending |
| ホテルグランヴィア大阪 | 大阪市北区梅田3丁目1番1号 | Both approved | Not added |
| ホテルニューオータニ大阪 | 大阪市中央区城見1-4-1 | Both approved | Pending |

Official access/facility documents and the exact Trip property pages were read September 8;
names and street numbers matched. Source URLs, exact IDs, outcomes and evidence are in
`osaka-five.review-2026-09-08.json`. All ten normal reviews then passed fresh server-side
HTTPS, pinned DNS, same-host/path and redirect checks with `browser_verified=false`.
Identity evidence plus link health was required; neither is a price/availability assertion.

Agoda search documents match the four names/streets, but direct documents are opaque.
They remain pending, version 2, health **unchecked**, without inferred property IDs. No
additional health request or browser override was used to promote those four candidates.
Locale variants and alternative Agoda slugs do not become extra platform entries.

Granvia's observed Agoda result has an inconsistent `hotel/kobe-jp.html` path. Without
primary browser identity proof it was not added, nor rewritten into a guessed Osaka URL.
Intergate's official facility page separately lists BREEZE TOWER parking at 梅田2丁目4-9;
that is not the hotel's 梅田2-5-2 identity. Rakuten review-page leads were not repurposed
into fabricated property URLs. Other Osaka platform slots retain their previous state.

Chrome could enumerate surfaces, but reading the existing Kyobashi tab timed out/reset;
one fresh-tab recovery also timed out/reset. **No map or platform browser verification
succeeded this turn**. Osaka products remain pending/version 1 with `map_verified=false`.
Official facts and previously licensed municipal coordinates are preserved. No Google/OTA
coordinates, ratings, reviews, photos, descriptions, prices or availability were imported.

## Production safeguards and changed baseline

Runtime was read-only verified as `travel-scanner-api:b3e49a325edcc41e167653e9fe13619403248507`,
ready database/Redis, schema `0061_merchant_styles`. This task did not deploy that image.

The previous Tokyo verifier correctly rejected its old all-record fingerprint: **catalog
config had changed independently**, at 01:14:02 UTC, to version 5 with public services and
all six destinations enabled. Product counts/reviews were unchanged. Do not replay its
old `public_enabled=false / destinations=[tokyo]` assertion or overwrite current settings.
This task preserved the new configuration exactly; it did not enable those cities or Airalo.
An enabled city is still not proof of completing the ten-hotel/three-area/two-OTA acceptance.

Before writes, backup `/root/travel_scanner_pre_hotel_candidates_20260908T011904Z.dump`
was created with umask 077, 7,058,883 bytes, and validated with `pg_restore --list`.
The existing administrator's active capability was verified without exporting credentials,
creating sessions/tokens or forging authentication. Normal versioned admin functions
`edit_hotel_option` / `review_hotel_option` performed and audited the changes.

- Exact input, status, version, saved ID and URL preflight; no bulk package replay.
- Baseline: `8b4cac74ef6aa5d22772158b3d4e760aca3e65c520348b515afbdb009aefa0dd`.
- Four existing Agoda slots filled: pending/version 2, no verified date or property ID.
- Ten existing official/Trip options: approved/version 2, healthy, no browser override.
- All **60 products, other 346 options and config** preserved; fingerprint
  `01048481d8180800c891863f9a3284c70c8c9a62509eaead879ab28fde7c0ba3` matched after writes.
- An independent read-only verification checked all 14 normal edit/review audit records.

## Final checkpoint and validation

**60 hotels: 12 approved / 48 pending. 360 platform options: 31 approved / 329 pending.**
Hotel identities and location approvals did not increase. Source labels and trip references
are unchanged. No city has completed content acceptance; this is a partial review checkpoint.

Read-only production `en/ja/ko/zh-TW/zh-CN` smoke passed: public Osaka returns no hotels
while their maps are pending, despite reviewed platform options and enabled city config.
Public Tokyo returns seven hotels, each official + Trip, with pending options excluded.
The smoke did not call a clickout, generate a conversion or use a provider/price API.

130 related content/API/platform/offline-source tests, Ruff/format, mypy (255 sources),
27 tooling tests, five locales/25 namespaces, task integrity and diff checks passed.
New regressions cover an enabled public city with pending hotel maps, independent option
approval, four pending non-guessed Agoda candidates, and the Granvia/Intergate exclusions.
New-head CI is tracked on the follow-up PR. Post-merge CI for #344, run 34176066090,
passed API, web, containers and full-stack smoke at the exact merge SHA.
The separately tracked intermittent community failure from prior runs is not fixed here.

Remaining: map identity reviews, second independent OTA approval per hotel, five remaining
Osaka platform pairs, Kyoto/Busan durable location gaps and all city acceptance criteria.
Keep the shared content task open/released at handoff. Never replay pending research inputs
over independently reviewed rows, and never present these four new URLs as four new hotels.
