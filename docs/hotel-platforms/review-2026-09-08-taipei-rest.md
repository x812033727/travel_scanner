# 2026-09-08 — PR #360 deployment and remaining Taipei reviews

## Verified merge and deployment

PR [#360](https://github.com/x812033727/travel_scanner/pull/360) was checked against
base `8d2fb93d3d95e40409113f64bdcb90edfc53736f`, head
`333114db59a695733e10e139d3a7f6f5acecb437`, CLEAN/MERGEABLE and all eight checks.
SHA-guarded squash merge completed at 06:21:55 UTC with merge commit
`3bc315a29b2795e242116ecadb2a3541f3d05a50`. Post-merge main CI
[34194340864](https://github.com/x812033727/travel_scanner/actions/runs/34194340864)
passed all four jobs before deployment.

Deployed from a clean Git archive, SHA-256
`d617361601b2d788dbd2c2903b0bc5f94db2bda129c8a53f66186765e09ebb94`, to
`/root/mokaair-release-3bc315a-p4ReUmYl/source`. All eight application services
were verified at the exact merged SHA, zero restarts, with three consecutive API
readiness/web checks. Schema remains `0062_merchant_platform_links` (no new schema
or runtime changes). Initial loopback connection resets during startup cleared
before all three readiness checks passed; not claimed as a zero-interruption rollout.

The existing Compose project, PostgreSQL/Redis containers, volumes, runtime `.env`
hash/mode and community-off settings were preserved. No secret export, cleanup,
canonical-checkout permission changes or deployment-agent activation. Previous
application images/source and all backups remain available.

Verified pre-deploy PostgreSQL archive:
`/root/travel_scanner_pre_deploy_3bc315a_20260908T063332Z.dump` (7,572,229 bytes).
Independent post-deploy verification reproduced the previous five-Taipei checkpoint:
22 approved products, 80 approved options, 32 audit records, unchanged licensed facts
and untouched-row/config fingerprint. Five real HTTPS BFF responses had five Taipei
hotels, 16 ordinary options and five source credits.

## Content result

Continued from the merged main in isolated `codex/hotel-content-review-taipei-rest`,
claiming the existing shared task. The original dirty workspace was untouched.

**60 distinct hotel identities remain; 27 approved / 33 pending products, and
88 approved / 272 pending platform options.** This batch promotes five previously
imported candidates, not five duplicate identities. It adds 11 previously missing
platform URLs to existing independent slots, all still pending after review.

| Existing hotel | Newly approved ordinary options | New pending candidates |
| --- | --- | --- |
| WESTGATE Hotel | Official, Trip | Expedia |
| Solaria Nishitetsu Taipei Ximen | Official, Trip | Agoda, Expedia |
| W Taipei | Trip | Agoda, Expedia |
| Grand Hyatt Taipei | Trip | Agoda, Expedia, Rakuten |
| Humble House Taipei | Official, Trip | Agoda, Expedia, Rakuten |

Taipei public results are now **10 hotels / 24 options**, up from five / 16, with
public government-source credits in all five languages. Tokyo 10, Osaka 2, Kyoto 0,
Seoul 5 and Busan 0 public hotel counts are unchanged. Existing global/city settings
remain version 5; this is not a new city enablement or declaration of full acceptance.
**Zero cities meet the full acceptance definition.** The new five still need their
second OTA approval, and W/Grand Hyatt need independently usable official options.

## Evidence and honest failure boundaries

Minimal primary identity evidence is in `taipei-rest.review-2026-09-08.json`:

- WESTGATE: official Zhonghua Road Section 1 **150**.
- Solaria: official Zhonghua Road Section 1 **88**; official access information also
  notes the entrance on Hankou Street. Do not confuse the entrance with a new property.
- W Taipei: official Zhongxiao East Road Section 5 **10**.
- Grand Hyatt Taipei: official Songshou Road **2**; not the separate Kyoto Hyatt hold.
- Humble House: official Songgao Road **18**, Curio Collection by Hilton identity.

Chrome opened all five saved Place IDs and checked heading, street and official site.
Only review outcomes/IDs are retained. Government coordinates, original source facts
and public attribution remain unchanged except `facts.map_verified=true`. No Google
coordinates, descriptions, ratings, reviews, prices, photographs or Plus Codes saved.

Chrome later timed out navigating to Solaria's official page; fresh inventory worked
but reconnection timed out again. Following the computer-use recovery limit, browser
operations stopped. **No platform browser verification is claimed in this batch**;
all `browser_verified` flags are false. Map checks already completed are separate
evidence, not permission to override failed official/OTA link checks.

Official and Trip primary documents match the street identities. Solaria's official
address was available through its primary indexed document; its direct web extractor
returned empty content. Five Expedia leads have primary property-name/street evidence,
but some address-extractor follow-ups failed; provenance/freshness is explicit.
Normal server URL validation was attempted only for five official, five Trip and five
Expedia options. Three official and five Trip reviews passed healthy. W/Grand Hyatt
official and all five Expedia attempts returned `service_link_unavailable`; each was
rolled back with no review audit or version increment. Failure is not asserted to mean
hotel delisting, nor is a page deemed safe just because it appears in search.

Four Agoda fresh opens rendered inputs only. Their indexed leads are saved pending;
W's separate review-page address does not establish fresh `_16` landing identity.
Grand Hyatt Agoda retains its actually observed `/en-sg/` URL. Two Rakuten international
property IDs were found: Grand Hyatt `34123457157057`, Humble House `34123457136539`.
Old index dates, missing street evidence and failed extraction keep both pending.
Japanese Rakuten IDs were not converted to international IDs. The San Diego Westgate
lead was explicitly excluded. Search homepages, reviews-only pages and regional lists
were not invented into new booking URLs.

The five saved Booking URLs remain pending, without a new browser inspection/review.
All Trip property IDs and original `xinyi-district` URL paths are preserved. No platform
prices, room inventories, reviews, full descriptions or photographs were imported.
No paid provider APIs, affiliate/quote activation, clickouts, analytics test conversions
or fake orders. Pending JSON remains a research/import package, not live approval truth;
**do not replay the package over independently reviewed production rows**.

## Guarded changes and verification

Before content writes, verified custom PostgreSQL archive:
`/root/travel_scanner_pre_taipei_rest_review_20260908T064117Z.dump` (7,572,483 bytes).
Read-only preflight checked the authorized admin, exact original row data/status/version,
60 products, 360 options, config version 5 and no prior target review/edit audit.
Whole-catalog baseline:
`8314407a1616eb1d4df45fc2d056e6e2508b2a43aea437149896a4b0e01693b7`.

Normal versioned admin operations created **34 audits**: 11 pending option edits,
five product edits, five location reviews, five product approvals and eight option
approvals. New options remain version 2 pending; reviewed old options become version 2
approved. Failed official options remain version 1 pending. All five products become
version 3 approved after explicit map review.

Independent read-only verification checked each affected product/option, expected
status/version/health, audit payload, source facts and unchanged other 55 products /
339 options / config fingerprint:
`fc2b57d9ed23b67d1267ae6982388104833c387e3c80cb1c0b731bfc0ce1d1fb`.
Thirty internal locale/city reads and five actual HTTPS Taipei BFF reads passed. All
ten Taipei hotels expose source credits; only 24 approved ordinary options appear,
all with `quote_status=not_configured`. No pending candidate leaks into public options.

## Validation and remaining work

Content regression tests cover pending-import isolation, licensed map/source invariants,
separate map/platform browser evidence, truthful failed reviews, independent option
visibility, URL/ID preservation, 11 non-duplicating candidates and incomplete acceptance.
Local checks before syncing the later main change: 149 related tests passed, 20 database
integration tests skipped locally (Linux CI supplies PostgreSQL/Redis). Ruff/format,
mypy across 257 source files, five-language/25-namespace completeness and 27 tool tests
passed. An optional offline Seoul-source run initially lacked research-only `pyproj`;
rerunning with `uv run --with pyproj==3.7.2` passed without changing application dependencies.
New-head CI results are recorded on the continuation PR. Fresh interactive
Chrome UI validation could not continue after the connection failure; existing
responsive/five-language CI tests validate unchanged UI code, not missing live page reads.

Keep the task open/released at handoff. Finish Taipei Booking/official/second-platform
reviews after browser access is available, then remaining city maps/links/coverage.
Preserve existing Hyatt future-closure and Westin holds; do not fill gaps with guesses.
These admin data changes are live; the new evidence/test PR is separate from the
already merged/deployed #360 and does not authorize another automatic merge.
