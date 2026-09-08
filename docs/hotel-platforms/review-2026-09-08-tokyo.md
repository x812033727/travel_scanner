# Tokyo source credits and platform review — 2026-09-08

This is the latest production content checkpoint for PR #344. The earlier fifty-hotel
and Busan checkpoints remain historical evidence. This batch adds no hotel identities:
it fills gaps on the six existing Tokyo hotels and independently reviews their OTA options.
No merge, deployment, migration, city release, affiliate enablement or paid API activation.

## Evidence and decisions

Official documents and exact Trip.com hotel documents were matched by name and street
number. Full URLs, minimal identity facts and individual decisions are recorded in
`tokyo.review-2026-09-08.json`. No prices, ratings, reviews, photos or descriptions were
copied. Platform IDs came from observed property URLs, not inferred from Google Place IDs.

| Hotel | Trip.com property ID | Result |
| --- | --- | --- |
| Keio Plaza Hotel Tokyo | 994639 | Approved, healthy |
| Hotel Gracery Shinjuku | 1841600 | Approved, healthy |
| JR Kyushu Hotel Blossom Shinjuku | 1857678 | Approved, healthy |
| THE GATE HOTEL KAMINARIMON by HULIC | 686539 | Approved, healthy |
| Hotel Gracery Asakusa | 15915697 | Approved, healthy |
| Henn na Hotel Premier Tokyo Asakusa Tawaramachi | 33514908 | Approved, healthy |

Chrome create-tab and one recovery both timed out/reset the kernel. No successful Chrome,
Google Maps or OTA UI review is claimed in this batch. Primary web-document inspection is
distinct from a browser UI check. All six approvals used the normal server HTTPS/DNS/redirect
health review with `browser_verified=false`; no bot-block override was used.

Booking and Expedia checks were unconfirmed; Rakuten requests timed out. Agoda returned
healthy responses for three URLs, but the web documents did not expose reviewable identities:
HTTP success alone did not earn approval. Other missing URLs have no asserted network check.
All twenty-four non-Trip option records remain pending. The evidence's health fields are
dated research observations, not claims that pending options have been approved or rechecked
by the background scheduler. Missing URLs are unresolved, not proof of no inventory.

Tokyo's existing six hotels now also have the missing source attribution: dataset title,
publisher, source URL, CC BY 4.0 link and a transformation/non-endorsement explanation.
The [Tokyo open-data terms](https://portal.data.metro.tokyo.lg.jp/terms/) were checked on
September 8. Saved coordinates, exact Place IDs, reviewed map flags, official options,
names, product IDs and trip relationships were preserved; this is not a new map review.

## Guarded production operations

Runtime remained `7f21d7eb2af223a561bc04519ce67021198b1068`, schema `0060_community_places`.
Validated backup: `/root/travel_scanner_pre_hotel_candidates_20260907T234914Z.dump`,
6,726,413 bytes, archive index checked with `pg_restore --list`. Do not restore without
separate authorization. No secrets, tokens or credentials are stored in the evidence.

The operator verified the existing active administrator capability, compared an exact
sixty-product/330-option/config fingerprint at preflight and apply, and used normal admin
services over SSH. For each original Tokyo hotel, one transaction:

1. Locked and version-checked the saved product and existing official option.
2. Prepared a source-credit-only edit from saved facts with `prepare_credit_update.py`.
3. Added five independent pending OTA slots, without replaying the research product.
4. Re-reviewed the product through the normal validator and wrote admin audit records.

The helper rejects changed identities, unreviewed maps, conflicting credits and projected
legacy `hotel_links`; it preserves saved labels and is idempotent. No direct status SQL or
legacy list projection was used. The original official options were fingerprint-checked
unchanged. The other 54 products, original 330 options and config kept fingerprint
`0c227110b0a44372958ccddfef43970beea95293af0429488978ea43ac06e522`.

A separate preflight/apply operation selected only the six new Trip options by exact saved
URL, property ID, evidence URL, pending status and version. Normal option review performed
fresh safe-health checks, then set each to approved/version 2 with an audit record.
All products, the other 354 options and config retained fingerprint
`49d6c97d20528f6f76ce523ef25e2b93d4c389f90cfa15441afa2564cef02754`.

The old `9103b9...` original-Tokyo fingerprint is now intentionally historical: attribution
and product review timestamps/versions changed. Do not reuse old scripts asserting that
all original Tokyo records or their option counts are untouched after this deliberate edit.

## Verified result

- Hotels remain **60: 11 product-approved, 49 pending** (Tokyo 6 approved; Seoul 5 approved).
- Platform records are **360: 13 approved, 347 pending**, now six slots per hotel.
- This batch added **30 records: 24 discovered URLs and six unresolved platform slots**.
  Six Trip.com records passed review; the other twenty-four remain pending.
- The thirteen approved options comprise six original Tokyo official links, RYSE official,
  and the six new Tokyo Trip.com links. No other OTA approval is implied.
- All six source-credit and six option-review audit records were verified.
- Read-only service smoke passed in en/ja/ko/zh-TW/zh-CN: the existing six Tokyo hotels each
  show official + Trip.com in direct mode and their source credits. Non-enabled Seoul and
  the public catalog remain hidden. No clickout, provider API or commission event was sent.
- `public_enabled=false`, configured destinations remain `[tokyo]`; affiliate and quote
  settings were not changed. No city meets ten hotels / three areas / official + two OTAs
  per hotel. One OTA per original Tokyo hotel is progress, not completed rollout acceptance.

## Validation and remaining work

126 related API/content/source/platform tests, Ruff/format, mypy across 254 sources, 27 tools
tests, five locales/25 namespaces and task checks passed. This is content/tests/docs only; no UI or schema
change. New-head CI must pass before any later merge. Previous head `9de855e` passed all
four jobs on both PR run 34170581417 and push run 34170579355. The previously observed
community smoke/read-metric issue remains a separate open task, not a claimed hotel fix.

Next: finish independent Booking/Agoda/Expedia/Rakuten identity and landing checks without
overriding unobserved browser failures; review the four new Tokyo maps and other cities;
find reusable Kyoto/Busan coordinates and precise map identities. Keep the content task
open, release ownership on handoff and do not replay pending packages over reviewed rows.
