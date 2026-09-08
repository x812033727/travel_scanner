# 2026-09-08 — Namba platform continuation and five exact-map reviews

## Merge and scope

PR #348 merged at `9e94d031d6e1755195d818de90340d362b2c9e96` after latest-main
head `4ed2cdb7b849747bf70aea6b4ece601a85a77498` passed all eight checks.
The PR smoke initially failed in Next development manifest JSON parsing; one disclosed
failed-job rerun passed. See the open community concurrency task for exact evidence;
a rerun is not a repair. This batch starts from that merged main in the isolated
`codex/hotel-content-review-namba` worktree, preserving the original dirty checkout.

## Current production checkpoint

There are still **60 hotel identities**, now **17 product-approved / 43 pending**,
and **360 platform options: 41 approved / 319 pending**. This batch adds four
candidate URLs to existing slots, ten independent platform approvals and five
product/location approvals; it does not invent additional hotels or duplicate IDs.

Normal versioned administrator operations and audit logs were used. Preflight checked
the full catalog fingerprint and exact source/options/status/version. Five products'
only factual change was `map_verified: false -> true`; their existing coordinates,
source credits, Place IDs, names and all other facts stayed unchanged. The other
55 products, 346 platform options and catalog config were fingerprint-preserved.

Backup before writes: `/root/travel_scanner_pre_hotel_candidates_20260908T022544Z.dump`,
7,063,947 bytes, custom dump readable by pg_restore. Runtime remained
`travel-scanner-api:b3e49a325edcc41e167653e9fe13619403248507`, ready schema
`0061_merchant_styles`. No deploy, migration, runtime setting, affiliate qualification,
price API policy, paid provider call, test booking or clickout was performed.

Config version 5, public/direct hotel links and existing enabled cities/kinds were
already enabled independently before this batch. They were not changed or treated as
city acceptance. Read-only recommendation smoke returned **Tokyo 10 / Osaka 2 hotels**
in all five locales. **Zero cities meet full acceptance**: hotels still need at least
two independently approved OTAs, not one OTA plus their official website.

## Successful location reviews

Chrome displayed the exact saved Place ID, hotel name, street and official website
for these five records. Official name/street evidence is recorded separately in
`namba-map.review-2026-09-08.json`; Google prices, ratings, reviews, photos and
coordinates were not copied. Licensed source coordinates were not re-derived.

| Hotel | Location outcome |
| --- | --- |
| 東京ステーションホテル | Approved, existing official and Trip links preserved |
| 三井ガーデンホテル京橋 | Approved, existing official and Trip links preserved |
| ミレニアム 三井ガーデンホテル 東京 | Approved, existing official and Trip links preserved |
| ホテルヴィスキオ大阪 | Approved, existing official and Trip links preserved |
| ホテル阪急レスパイア大阪 | Approved, existing official and Trip links preserved |

Next Intergate navigation returned Debugger unattached; one state recovery also failed.
The computer-use skill required stopping the retry. No Intergate or further map review
is claimed. Pending input files retain false map flags: dated review evidence and
production state are separate, and pending imports must never overwrite reviewed rows.

## Remaining Osaka five — platform reviews only

The official and Trip.com options for Monterey La Soeur, Royal Classic, Swissotel Nankai,
Sotetsu Grand Fresa Namba and Gracery Namba all passed normal HTTPS/DNS/redirect and
link-health checks, with independent name/street evidence and no browser override.
Their products remain pending because their maps were not verified in this batch.

Swissotel's existing PDF is historical. Its current official HTML contact address
provides supporting evidence; the saved source URL was not silently replaced.
Sotetsu's saved www Trip page could not be extracted by web tooling. The observed US
locale page has the same property ID 4064224 and matching street; it was indexed four
weeks ago. The saved URL independently passed server health; it was not rewritten.

New Agoda candidates: Monterey La Soeur, Royal Classic, Sotetsu and Gracery.
All remain pending/unchecked, without inferred property IDs. Direct documents were
opaque; a search name/street match alone is not approval. Sotetsu's observed old-name
slug is preserved and specifically flagged for identity confirmation. Swissotel's
conflicting Kobe-path lead is excluded; no Osaka URL is guessed from it.

Only minimal factual identity evidence is retained; no OTA room prices, reviews,
descriptions, photographs or ratings were imported.

## Remaining work

Complete further map reviews when Chrome is healthy, then independently verify
Booking/Agoda/Expedia/Rakuten landing identities. Keep pending brands/links off public
booking options, preserve normal safety/version checks, and continue city acceptance
without silently enabling affiliate or price APIs. Historical dated files are snapshots,
not current production truth and not authority to bulk replay pending input.

Independent read-only verification confirmed all 29 audit records, unchanged fingerprints,
five products' preserved source facts and all five locales' public options (official + Trip).
133 related content/platform/API/offline-source tests, Ruff/format, mypy (255 sources),
27 tools tests and five locales/25 namespaces passed. New-head CI is tracked in the PR.
Post-merge main smoke also exposed the existing community reset class of failure; see
the separate task for exact evidence and the single failed-job rerun, not a claimed fix.
