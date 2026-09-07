# Busan addition and RYSE review — 2026-09-08

This continues PR #344 on codex/hotel-content-review-kyoto. It does not merge, deploy,
enable a city, activate affiliate rights, call price APIs or claim a completed catalog.

## Research and rejection decisions

Ten Busan pending inputs cover three existing areas: Seomyeon (LOTTE, ARBAN, Toyoko),
Haeundae (Park Hyatt, Grand Josun, Paradise, Shilla Stay, L7) and Nampo (Stanford, Foret).
Each has an official identity reference and indexed Booking/Trip property pages with matching
street numbers. Other platforms remain unconfirmed; lead URLs are evidence only.
No official translations were invented. No prices, ratings, reviews, images, availability,
map coordinates or unsupported facility/cancellation promises were imported.

Busan does not yet have verified reusable coordinate sources or exact Naver identities.
The official-name/address reference is not an asserted content reuse license. Every Busan
product and option remains pending, and none can pass the full city rollout acceptance.

- Chrome read the official Solaria Busan notice: operations end after checkout on
  2026-12-29, not already closed. This candidate was excluded from the new open-ended catalog.
  Source: https://solaria-busan.nnr-h.com/news/YjrKmYk0
- ibis Ambassador Busan City Centre's official identity conflicts with the current Trip
  title Central Seven Hotel by Kwon at the same address; excluded pending rename review.
- Arban City Hotel at 20 Bansong-ro is not ARBAN HOTEL at 32 Jungang-daero 691beon-gil.
- Toyoko's official 00221 property, Booking and Trip agree on 39 Seojeon-ro; a conflicting
  tourism-directory address was not used.

Chrome successfully rechecked RYSE's official CONTACT page, 130 Yanghwa-ro, and its direct
Naver link 1578505636. That Naver property had a saved name/address/homepage match on
2026-09-07. The fresh Naver visit timed out; one fresh Chrome tab recovery also timed out.
The older Naver observation is used with its actual date, not misrepresented as a new check.
No safety barriers were bypassed; no other Busan/Naver/OTA browser checks are claimed.

## Production content operation

Runtime remained 7f21d7eb2af223a561bc04519ce67021198b1068, schema 0060_community_places.
Backup: `/root/travel_scanner_pre_hotel_candidates_20260907T232859Z.dump`, 6,714,842 bytes,
verified with pg_restore --list. It is a recovery artifact, not authorization to restore.

Existing active admin capability was verified. The normal CSV validator/import service ran
inside a serializable transaction with an exact ten-new-Busan-key guard. All fifty existing
products/options plus catalog config were locked, skipped and fingerprint-checked unchanged.
The preflight fingerprint was matched again at apply. No existing research package was replayed.

Import `cb5921a5-d87a-4ff9-9946-5c3c3ad19689`: ten pending products, sixty pending options.
Normal preview/commit audit records were written. RYSE subsequently passed a version-checked
individual product review and independent official-option review (health_status=healthy).
The option was browser_verified only for the exact CONTACT URL observed in Chrome; no OTA
option was approved. These operations used existing admin services over authorized SSH,
not forged web sessions, direct status SQL or a deployment.

| City | Product approved | Product pending | Total |
| --- | ---: | ---: | ---: |
| Tokyo | 6 existing | 4 | 10 |
| Osaka | 0 | 10 | 10 |
| Kyoto | 0 | 10 | 10 |
| Seoul | 5 | 5 | 10 |
| Busan | 0 | 10 | 10 |
| Taipei | 0 | 10 | 10 |

New platform options across the two imports: 324; 323 pending, one approved RYSE official.
Product approval is not platform approval or city acceptance. Zero cities meet the complete
ten-hotels/three-areas/official-plus-two-OTAs release requirement.

Read-only verification confirmed original Tokyo six, original options and config fingerprint
`9103b9b40c3abdc1ccf1e64e3961d26b88345f77f215c646ff0a7ecf1dcc8994` unchanged.
public_enabled=false; enabled_destinations=[tokyo]. Five-language catalog smoke retained the
original Tokyo six, excluded the new city and preserved the public gate. No click or paid
provider requests were generated. Affiliate and price settings were not changed.

## Validation and handoff

120 related API/content/platform/offline-source checks passed. Ruff, formatting, mypy across
254 source files, 27 tools tests, five locales/25 translation namespaces and task integrity
passed. This is content/tests/docs only, with no new runtime, schema or responsive UI behavior.
CI for this continuation must be checked at the new head before any later merge.

At previous head fe8a61d, PR run 34148400225 passed all four jobs. The same-head push run
34148381308 failed community.spec.ts with ECONNRESET alongside uq_community_metric errors.
The suspected race is recorded separately in the open community-read-metric-concurrency task;
no unrelated remediation or claim that a retry fixed it is made here.

Next: exact Naver and licensed Busan coordinates; remaining Seoul Naver and platform checks;
Kyoto coordinates/Place IDs; individual OTA approvals; deliberate original Tokyo source-credit
update. Do not replay pending inputs over reviewed rows. Keep content task open and release
ownership at handoff; do not enable a city based solely on the sixty-input count.
