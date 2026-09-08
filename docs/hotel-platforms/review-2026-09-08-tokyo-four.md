# Four pending Tokyo hotels: review continuation — 2026-09-08

Latest content checkpoint for draft PR #344. This batch fills three missing Agoda URLs,
reviews eight existing official/Trip options, and approves one existing pending hotel's
map identity. The hotel count stays sixty; it is not a sixty-hotel acceptance or city launch.

## Evidence and decisions

- Chrome successfully opened Ryumeikan Tokyo's saved Place ID
  `ChIJD7G_2_2LGGARcK8ZATyh2U8`. Hotel name, street number and official website matched
  the [official access page](https://www.ryumeikan-tokyo.jp/access/), Yaesu 1-3-22.
  The result was the hotel, not the separately listed restaurant or office building.
- The next Kyobashi navigation timed out; its state recovery also timed out and reset the
  session. No Kyobashi, Millennium or Tokyo Station browser verification is claimed here.
  No safety barriers, CAPTCHA, certificate checks or browser permission settings were bypassed.
- The four official access documents and four Trip property documents established name/
  street matches. All eight saved official/Trip URLs passed the normal server safe HTTPS,
  DNS and redirect review with `browser_verified=false`. Tokyo Station's homepage document
  timed out, so its readable official access document supplied identity evidence; the exact
  homepage URL separately passed live health. Kyobashi's Trip document was labeled indexed
  last month, not falsely reported as freshly indexed today.
- Three new Agoda URLs (Tokyo Station, Ryumeikan, Kyobashi) have matching name/street search
  documents, but direct page documents remained opaque. Their HTTP health was successful,
  which alone is insufficient: all three candidate options remain pending. Missing Expedia
  entries and Millennium's unresolved Agoda identity remain gaps, not guessed mappings.
- Booking health was unconfirmed; three Rakuten URLs timed out. None was approved. No
  alternate language slug or duplicate Agoda property was treated as an additional option.
- No prices, availability, review text, ratings, photos, descriptions or provider coordinates
  were copied. Existing licensed Tokyo coordinates and attribution were preserved.

See `tokyo-four.review-2026-09-08.json` for per-hotel evidence, observed dates, exact targets,
option IDs and review outcomes. Candidate JSON deliberately retains false map-review flags;
it is research input, not a synchronization source that may overwrite reviewed production rows.

## Guarded production operation

The previous runtime-version guard refused to start its backup after another deployment
advanced production. Read-only inspection confirmed image
`travel-scanner-api:b3e49a325edcc41e167653e9fe13619403248507`, schema `0061_merchant_styles`,
database and Redis ready. This hotel task did not deploy that image or migrate that schema.
The earlier 60-hotel/360-option baseline and protected-record fingerprint still matched.

New backup `/root/travel_scanner_pre_hotel_candidates_20260908T003418Z.dump`, 7,048,465 bytes,
was validated with pg_restore's archive listing before writes. No restore authorization is
implied. No credentials, user sessions or database contents were exported to the repository.

Preflight and apply matched fingerprint
`d79ed6a5fe98c59a7d76e69a4cf0754d684a0d8ee1f1538a1f275ebc16c06e5e`.
The existing active administrator capability was checked. Normal versioned admin services:

1. Filled the three empty Agoda slots, preserving their IDs; each remains pending/version 2.
2. Updated only Ryumeikan's map verification flag and passed normal product review, atomically
   committing the edit/review plus location evidence audit. Its product is approved/version 3.
3. Independently reviewed the four official and four Trip options; each approved/healthy,
   version 2, with normal audit records and no browser-health override.

All 59 other products, 349 other options and catalog config retained fingerprint
`b5b854cb3cdf9bf2596df6ca187289879856054fadb102f0f8547d450214c352`.
Existing hotel IDs, source coordinates, names, original links and trip associations remain.
No direct approval SQL, bulk replay, affiliate configuration or price API was used.

## Verified outcome

| Scope | Approved | Pending | Total |
| --- | ---: | ---: | ---: |
| Hotel products | 12 | 48 | 60 |
| Independent platform options | 21 | 339 | 360 |

Tokyo now has seven product-approved hotels; Seoul still has five. This batch does not
approve the other three Tokyo products just because their official/Trip links were reviewed.
Read-only en/ja/ko/zh-TW/zh-CN service smoke shows seven Tokyo hotels, each with official +
Trip direct options and source credits. Pending Agoda options and the three unreviewed map
identities stay hidden. No click/conversion event or provider API call was generated.

Catalog public enablement stays false; configured destinations remain Tokyo only. No city
meets the ten-hotels/three-areas/official-plus-two-OTAs acceptance rule. No affiliate or paid
quote switch, merge, deployment, UI or schema change is part of this continuation.

## Validation and handoff

128 related API/content/platform/offline-source tests passed, including separation of map,
option and research-input status. Ruff/format, mypy across 255 sources, 27 tools checks,
five locales/25 namespaces and task integrity passed. Full CI is checked at the new head
of PR #344. Prior head 5571190 passed all eight jobs, PR 34172384315 and push 34172381941.

At content head `dc6cabb`, PR run 34174167430 passed all four jobs; push 34174165077 passed
API/web/containers but failed the community account-confirm smoke (JSON parse error and
missing confirm button). Repeated community metric duplicates were also logged; causality
is not established. Evidence is in the existing open community-read-metric-concurrency
task, without personal IDs or tokens. This hotel batch did not modify those runtime paths,
and neither a later green run nor this documentation follow-up is a fix for that defect.

Continue with remaining exact map identities, browser-supported OTA reviews and reusable
Kyoto/Busan coordinates. Do not rerun old snapshot/smoke scripts expecting six Tokyo hotels
after this intentional review. Keep the content task open and release it at handoff.
