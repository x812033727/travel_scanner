---
id: 2026-09-07-hotel-platform-options-and-quote-readiness
title: Hotel platform options and quote readiness
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-07T12:32:44Z
completed_at:
branch: codex/hotel-content-review-taipei-rest
depends_on: []
scope:
  - apps/api/tests/test_hotel_content_package.py
  - docs/hotel-platforms
---

# Hotel platform options and quote readiness

## Latest: 2026-09-08 PR #360 deployment and remaining Taipei review

User authorized merging #360, deploying, then continuing. Verified head 333114d,
base 8d2fb93, CLEAN/MERGEABLE and all eight checks; SHA-guarded merge to
3bc315a29b2795e242116ecadb2a3541f3d05a50. Main CI 34194340864 passed all four jobs.
Clean archive deployed to all eight app services with zero restarts and three ready
checks. PostgreSQL/Redis IDs, env hash/mode, volumes and community-off state preserved;
schema still 0062. Verified database backup and previous five-Taipei checkpoint before
continuing in isolated codex/hotel-content-review-taipei-rest.

Five remaining existing Taipei products map-reviewed and approved: WESTGATE, Solaria
Nishitetsu Ximen, W Taipei, Grand Hyatt Taipei, Humble House. Chrome actually checked
the five saved Place IDs; government coordinates/source credits unchanged. Browser
later timed out and reconnection failed, so stopped per skill; no platform browser
verification or override in this batch. Normal reviews approved five Trip plus three
official links. W/Grand Hyatt official and five Expedia reviews failed safely/rolled
back, with no review audit. Booking remains pending and uninspected in this batch.

Added 11 independently found candidates to existing slots: four Agoda, five Expedia,
two Rakuten international. All remain pending; old/empty/failed extractor evidence
is explicit. Wrong San Diego Westgate and Japanese Rakuten ID conversion excluded.
No new duplicate hotel identities: still 60, now 27 approved products/33 pending;
88 approved options/272 pending. Taipei publicly 10 hotels/24 ordinary options in
all five locales, with source credits/no quotes. Other city counts unchanged.
Zero complete cities: new Taipei rows still need second OTAs plus W/Hyatt official.

34 new audit records independently verified; other 55 products/339 options/config-v5
fingerprint fc2b57d9ed23b67d1267ae6982388104833c387e3c80cb1c0b731bfc0ce1d1fb
unchanged. Five HTTPS BFF reads plus 30 internal locale/city reads passed. Deployment,
backups, provenance and outcomes: docs/hotel-platforms/review-2026-09-08-taipei-rest.md
and matching JSON checkpoint. No paid APIs, settings/affiliate/quote changes, clickouts
or orders. Pending input JSON is not live truth: never replay it over live reviews.
Original dirty worktree untouched. Release task at handoff; remaining acceptance open.

149 local related/offline-source tests passed with research-only pyproj==3.7.2;
20 PostgreSQL integrations deferred to full Linux CI. Ruff/format, mypy 257 sources,
five-language catalogs and 27 tooling tests passed. Later main 737cdbb (#358) contains
separate destination-brand work; sync/revalidate the continuation without claiming
that later main was part of the already verified 3bc315a deployment.

## Previous: 2026-09-08 deployment and Taipei five-hotel review

User authorized merging #357, deploying, then continuing content. Synced latest main
f48e9a6; all eight checks passed at 71f0431, SHA-guarded merge to
00ffc710ebf902f56a00a69869f96e92bf3e84d0. Main CI 34191743658 passed all four jobs.
Deployed that clean archive via existing SSH/Compose project. All eight app images
verified, readiness three times, five-language home/BFF reads and existing hotel
checkpoint passed. PostgreSQL/Redis IDs, runtime env, volumes, config and community-off
state preserved. Schema remains 0062. First piped script stopped before activation;
fixed migration stdin after read-only inspection, then completed guarded deployment.

Five existing Taipei products now location-approved: Palais, Cosmos, Caesar Taipei,
CityInn Station III, amba Ximending. Chrome verified their saved Place IDs against
names/street/official sites. Existing Tourism Administration coordinates/credits untouched.
All five official/Booking/Trip options approved, plus newly discovered Cosmos Rakuten
international 34123457140865: 16 newly approved options. Booking/Rakuten and Caesar
official retain truthful unconfirmed server health with actual browser review evidence;
unsafe/unavailable blocking unchanged. Cosmos/Caesar official first failed, then were
freshly checked in Chrome and passed normal browser-confirmed follow-up review.

No new distinct identities: still 60, now 22 product-approved/38 pending, 80 options
approved/280 pending. Taipei public five-locale results now five hotels/16 ordinary options,
with source credits and no quotes; other cities unchanged. No city meets full acceptance.
No settings, paid API, affiliate/quote activation, clickouts, fake bookings or UI changes.

Backups and deployment/source/browser/admin evidence:
docs/hotel-platforms/review-2026-09-08-taipei-five.md and matching JSON checkpoint.
Independent postflight verified 32 audits, product facts and untouched 55 products/344
options/config-v5 fingerprint 5a5e10994fcd003d0d50597a29d96bdc6d274d31fc5bfbfe82b87d414abbd863.
Pending JSON is NOT sync truth; never replay it over live approvals. Remaining five
Taipei hotels, missing second OTAs/maps in other cities and full per-city acceptance
remain open. Preserve Hyatt future-closure/Westin holds. Release shared task at handoff.

145 relevant tests, Ruff/format, mypy 257 sources, five locales/25 namespaces and tooling/
task checks passed. Chrome confirmed live catalog and four-option Cosmos panel, without
clickouts or fake prices. Full latest-head CI tracked on continuation PR; no new code
deployment needed for these admin data changes. New evidence PR remains separate from #357.

## Latest: 2026-09-08 Seoul independent platform review

User authorized #355 merge. Verified head a8a750c, latest main 88eb4b1,
CLEAN/MERGEABLE and all eight CI checks, then SHA-guarded squash merged to
9ca88c22435759d4d6edbd6b34e7a0186318280d at 05:06:35 UTC. Post-merge main run
34189379559 passed all four checks. Isolated continuation codex/hotel-content-review-seoul-links.

Five previously location-approved Seoul hotels gained five Trip approvals plus Mercure
official approval. Four Points official and two Expedia attempts failed normal server
review and remain pending/version 1, with no browser override or inferred delisting.
Lotte official bot pages and five unreadable Booking pages were not approved. Other three
Expedia address extractions returned Internal Error and were not re-reviewed.

Two new Rakuten international candidates: RYSE 34123457159873 and Mercure 34123457217428.
Both remain pending; the latter's observed hkg/zh-hk URL is not rewritten to an invented
English equivalent. Indexed documents are stale/partial, not live inventory or address proof.
No new identities/map approvals/coordinates, provider photos/prices/reviews, quote/affiliate toggles,
clickouts, paid API requests, deployments or migrations. Prior licensed facts unchanged.

Runtime aaa33f0/schema 0062 and catalog config v5 unchanged. Verified backup before writes:
/root/travel_scanner_pre_hotel_candidates_20260908T051250Z.dump (7095043 bytes).
Exact preflight 6a70a44e0190a0591021100f6046c2d336ae6346ca3d4a94868f73b5e8207c90;
independent postflight validates 8 audits, all 60 products/other 349 options/config
fingerprint 8da6cf45fe63270b3bc46855503fb5c7faf84f5eda085e1ac355f3e1eba836e7.
Still 60 products (17 approved/43 pending), options 64 approved/296 pending. Public
Seoul five hotels now have seven options instead of one; five real HTTPS BFF reads pass,
plus five-locale internal reads across six cities. No city meets full acceptance yet.

Evidence: docs/hotel-platforms/seoul-links.review-2026-09-08.json and matching markdown.
Never replay pending JSON over live rows. Shared task remains open; release at handoff.
142 content/API/offline-source tests passed; Ruff/format and mypy across 257 sources
passed. Five locales/25 namespaces, tool/task checks and full latest-head CI are tracked
on the continuation PR. No runtime/UI/migration changes in this content batch.

## Latest: 2026-09-08 Kyoto station-area platform review

PR #353 verified CLEAN/MERGEABLE and all eight checks at exact 252a2d8, merged with
head guard to 6db0f51a127246beb82d30d3eef4a0624a649e50 at 04:05:33 UTC. Post-merge main
34185756687 passed all four jobs first attempt. Continued in isolated
codex/hotel-content-review-kyoto-station; original dirty worktree preserved.

Five existing Kyoto Station/Kawaramachi hotels (Granvia, Vischio, Daiwa Terrace Hachijo,
Miyako Hachijo, Cross) gained observed Rakuten international candidate URLs, all pending.
Their ten official/Trip options passed normal versioned review, all healthy with
browser_verified=false. Kyoto products remain pending for missing exact maps/licensed
coordinates. No new hotel identities, map approvals, city switches, paid provider calls,
clickouts, fake bookings, affiliate/quote enablement, deployments or migrations.

Granvia Trip shows JR Kyoto Station Central Entrance, not permit house number 901;
no invented Trip address. Miyako Trip's existing otokuni-district URL shows the correct
Kyoto property/street 17; preserve observed URL/ID rather than guessing a rewrite.
Exclude wrong Daiwa Hachijoguchi branch at Kitakarasuma-cho 9-2 (Terrace is Higashisanno-cho
14-1). Existing Booking kyoto-station page yielded no readable identity and stays pending,
not presumed mismatched/delisted. Expedia Vischio regional result has malformed hotel URL;
save only unresolved evidence, not a fabricated corrected link or regional hotel option.
Prior Hyatt future-closure and Westin link holds remain unchanged.

Chrome Intergate selection timed out waiting for CDP Emulation.setFocusEmulationEnabled;
fresh inventory plus one reconnect returned the same error. Stopped per computer-use
recovery rule. No new map/browser verification claimed from a tab title.

Production aaa33f0/schema 0062 unchanged. Backup before writes:
/root/travel_scanner_pre_hotel_candidates_20260908T041040Z.dump (7090398 bytes).
Preflight adc6db5cc7270269a2b637a3a97029d9ca4222f8ff922b0b8bb1f180791b95c6;
independent verification confirmed 15 new audits and all 60 products / other 345 options /
config version 5 preserved. Still 60 products, 17 approved/43 pending; platform options
58 approved/302 pending. Five-language internal and actual HTTPS BFF reads retain
Tokyo 10 / Osaka 2 / Kyoto 0. Zero complete cities. Never replay pending input over live rows.

139 related tests, Ruff/format, mypy 257 sources, five locales/25 namespaces and 27 tooling
tests passed. New-head full CI on continuation PR. Evidence:
docs/hotel-platforms/review-2026-09-08-kyoto-station.md and matching JSON checkpoint.
Release at handoff, not done: exact maps, reusable coordinates, independent OTA review
and city acceptance remain unfinished. Older sections below are historical checkpoints.

## Latest: 2026-09-08 Kyoto five-platform continuation

User authorized #352 merge and continued review. Main had advanced to aaa33f0 (#349);
synced, reran all eight checks at 5f1e661 (PR 34183706585 / push 34183705002), verified
CLEAN/MERGEABLE, then SHA-guarded merge to f65890ad76c7d6f3c47076e813e5e6cbebcec1e3.
Continued from merged main on codex/hotel-content-review-kyoto-links. Original dirty
worktree preserved. Post-merge CI 34184188769 is being checked separately; no new runtime
fix or claim of remediation for unrelated smoke failures is part of this content batch.

Chrome Intergate creation returned Debugger unattached; fresh inventory found the actual
tab, but one reconnect timed out/reset. The computer-use skill stopped further retries.
No new map/location reviews, coordinates, hotel identities or public city activation.

Added five observed Rakuten international IDs/URLs for Royal Park Kyoto Sanjo, Mitsui
Garden Kyoto Shijo, Hyatt Regency Kyoto, Celestine Gion and Westin Miyako; all pending.
Full street/current landing identity is still unresolved. Shijo is not Shinmachi Bettei
(excluded ID 10123456795625). Eight normal official/Trip reviews attempted: seven approved;
Westin's saved Marriott link failed service_link_unavailable and rolled back, still
pending/version 1/unchecked. No browser override or substituted URL used. Celestine's
same-ID locale page supports Komatsucho 572 but lists inconsistent postcodes; official
605-0933 is authoritative and provider postal-code data was not imported.

Important content hold: ORIX Real Estate's 2026-04-09 official announcement confirms
Hyatt Regency Kyoto ends operations 2027-05-09 (not closed today). Product and every
option remain pending; official/Trip notes and new Rakuten candidate contain the notice.
Do not approve without operating-date safety or a reviewed replacement. Source and
unresolved blocker are in Kyoto permit evidence; preserve existing hotel/trip IDs.

Runtime guard first stopped because another work deployed aaa33f0/schema 0062. Hotel
fingerprint and relevant travel-service/auth code remained unchanged; no deployment or
reset here. New backup /root/travel_scanner_pre_hotel_candidates_20260908T034012Z.dump,
7084300 bytes, preceded normal guarded admin writes. Read-only verification confirmed
14 audit records and all 60 products / other 345 options / config version 5 preserved.

Current: 60 hotel identities, 17 approved products / 43 pending; 360 platform options,
48 approved / 312 pending. Five locales' internal recommendations AND actual HTTPS BFF
responses return Tokyo 10 / Osaka 2 / Kyoto 0, only approved official + Trip public options.
No city is complete; no provider price API, clickout, order, affiliate or config changes.
Details: docs/hotel-platforms/review-2026-09-08-kyoto-five.md and matching JSON evidence.

Validation: 136 related tests, Ruff/format, mypy 257 files, five locales/25 namespaces,
27 tooling tests and independent production smoke passed. New-head full CI goes on the
continuation PR. Release this shared task, not done; remaining maps, platform reviews,
Hyatt closure hold and city acceptance are still open. Earlier sections are snapshots.

## Latest: 2026-09-08 Namba platform and five-map review continuation

User authorized merge #348 then continuing. Synced latest main 67234d9, verified exact
head 4ed2cdb all eight checks/CLEAN/MERGEABLE, SHA-guarded merge to 9e94d03. Initial PR
smoke manifest failure and post-merge main community reset are documented in the open
community task; one failed-job rerun each, not a runtime repair. Continued from merged
main in isolated codex/hotel-content-review-namba; dirty original checkout preserved.

Chrome confirmed exact saved Place IDs/name/street/official website for Tokyo Station,
Mitsui Garden Kyobashi, Millennium Mitsui Garden Tokyo, Vischio Osaka and Hankyu Respire.
Intergate navigation plus one state recovery returned Debugger unattached; stopped as
the computer-use skill requires, no further maps claimed. Normal map/product review
approved these five only; existing licensed coordinates/credits/IDs preserved. Research
map flags remain false and must not be replayed as production synchronization inputs.

Remaining five Osaka hotels' official and Trip links independently approved with healthy
normal URL checks and no browser override. Four new Agoda URLs pending, no inferred IDs.
Sotetsu's old-name Agoda slug is retained as pending; same-ID US Trip evidence supports
identity without replacing the saved www URL. Swissotel's Kobe-path Agoda lead excluded;
historical PDF supplemented by official HTML contact address, not claimed newly published.

Backup /root/travel_scanner_pre_hotel_candidates_20260908T022544Z.dump, 7063947 bytes,
preceded normal guarded admin writes. Runtime b3e49a3/schema 0061 unchanged. Independent
read-only check confirmed all 29 audit records, exact other-55-products/346-options/config
fingerprint, and source facts unchanged except map review flags. No deploy, migration,
settings/affiliate/quote changes, provider API requests, clickouts or fake reservations.

Current: 60 identities, 17 product approved / 43 pending; 360 options, 41 approved /
319 pending. Five-locale public reads return Tokyo 10 / Osaka 2, each official + Trip,
pending options hidden. No complete cities: two approved OTAs are still required, not
official plus one OTA. Details: docs/hotel-platforms/review-2026-09-08-namba-map.md.

Validation: 133 related tests, Ruff/format, mypy 255 sources, 27 tools tests, five locales /
25 namespaces and production read-only five-locale smoke passed. New-head full CI is
tracked on the continuation PR. Keep task open/released for remaining maps/platforms
and per-city acceptance; the following sections are earlier historical checkpoints.

## 2026-09-08 merged checkpoint and Osaka five-hotel continuation

User authorized merging #344, then continuing additions/review. Latest main b060227 caused
the initial merge to be blocked; synced main and verified head 873e876, all eight checks
(PR 34175671037 / push 34175669025), CLEAN/MERGEABLE, then SHA-guarded squash merge.
GitHub confirmed merged commit 2e5e9feb68181d809653ad9ac67cf761e0f98950, 01:15:52 UTC.
Continued on codex/hotel-content-review-osaka from that main in the isolated worktree.
The original dirty workspace is preserved. No runtime deployment or migration performed.

Five Osaka official/Trip exact pages match names and street numbers. Chrome existing-tab
read timed out/reset and one fresh-tab recovery also failed; no map/browser identity
review succeeded. Ten normal official/Trip option reviews passed healthy HTTPS/DNS/redirect
checks with browser_verified=false. Four missing Agoda URLs were added to existing slots,
pending/version 2/unchecked, without guessed property IDs. No hotel identities were added.
Granvia's inconsistent-city Agoda URL was not used; Intergate's separate parking address
was excluded. All product/location facts and approved Tokyo/Seoul records are preserved.

The old Tokyo fingerprint guard failed read-only because config independently changed at
01:14:02 UTC to version 5, public services/all six cities enabled. Preserved it exactly;
do not replay older disabled/Tokyo-only assertions or claim this task enabled public rollout.
Runtime is still b3e49a3/schema 0061. Verified backup
/root/travel_scanner_pre_hotel_candidates_20260908T011904Z.dump (7058883 bytes) preceded
normal versioned admin writes. Baseline and all-60-products/other-346-options/config
fingerprints matched; independent verification confirmed all 14 edit/review audit records.

Current: 60 hotels, 12 approved/48 pending; 360 options, 31 approved/329 pending.
Five-language public smoke: Osaka zero hotels despite enabled city and approved options;
Tokyo seven with official + Trip, pending options hidden. No city is content-complete.
No clickout/conversion/provider-price API calls or affiliate/quote/config changes.

130 related tests, Ruff/format, mypy 255 sources, 27 tools tests, five locales/25 namespaces,
task checks and diff checks passed. Evidence: review-2026-09-08-osaka-five.md and
osaka-five.review-2026-09-08.json. New PR CI tracked separately; #344 post-merge run
34176066090 passed API, web, containers and full-stack smoke at the exact merge SHA.
Previous unrelated community CI failure remains separately tracked, not fixed here.
Remaining: map reviews, second OTAs, other five Osaka platform pairs, durable Kyoto/Busan
locations and every city's full acceptance. Release at handoff, do not mark task done.

## 2026-09-08 latest Ryumeikan and four-hotel platform continuation

Same isolated branch and draft PR #344, main still b3e49a3. Original dirty workspace remains
untouched. Chrome succeeded once: Ryumeikan Tokyo exact saved Place ID, hotel name, Yaesu
1-3-22 and official website matched the official access page. The next Kyobashi navigation
and one state recovery timed out/reset; no other new map browser verification is claimed.
No provider coordinates, photos, ratings, reviews, prices or descriptions were imported.

Four hotels' official/Trip documents matched name/street, and all eight saved target links
passed normal safe HTTPS/DNS/redirect review. Tokyo Station's home document timed out but
the exact official access identity was readable and server homepage health was healthy.
Kyobashi Trip was indexed last month, not claimed freshly indexed. Three Agoda exact URLs
were discovered by name/street; opaque direct documents and no browser proof mean pending,
even though HTTP health is good. Booking and Rakuten stay pending/unconfirmed/timeout.

The old backup runtime guard correctly refused when another task deployed b3e49a3/schema
0061. Read-only ready/image and hotel baseline checks passed; a new verified backup
/root/travel_scanner_pre_hotel_candidates_20260908T003418Z.dump (7048465 bytes) preceded
guarded writes. No image/schema deployment was performed by this content task.

Normal versioned admin services filled three existing Agoda slots (pending/version 2),
atomically edited/reviewed Ryumeikan's map flag (approved/version 3), then independently
approved eight official/Trip options (healthy/version 2, browser_verified=false). Exact
snapshot/version guards and audits were verified. Other 59 products/349 options/config
fingerprint b5b854cb3cdf9bf2596df6ca187289879856054fadb102f0f8547d450214c352 preserved.

Current: 60 hotels, 12 product-approved / 48 pending; 360 options, 21 approved / 339 pending.
Five-language read-only smoke displays seven internal Tokyo hotels, each official + Trip
with source credits; unreviewed maps and pending Agoda hidden. Public gate false, configured
destinations [tokyo]. Zero accepted cities, no affiliate/price enablement, no generated clicks.

128 related tests, Ruff/format, mypy (255 files), 27 tools checks, five locales/25 namespaces
and task integrity passed. See docs/hotel-platforms/review-2026-09-08-tokyo-four.md and
tokyo-four.review-2026-09-08.json. CI will be verified at the new PR head. Prior head 5571190
passed all eight checks. No merge/deploy authorization; release at handoff, task not done.
Remaining: three Tokyo maps, second OTA approvals, remaining Seoul identities and other
cities' durable coordinates/maps/platform reviews. Do not replay the old pending package
or smoke expectation of six Tokyo hotels over this new intentional review checkpoint.

At dc6cabb, PR CI 34174167430 passed API, web, containers and full-stack smoke. Push
34174165077 passed API/web/containers but its community smoke failed on account-confirm
JSON parsing / missing confirmation button, alongside recurring uq_community_metric
duplicates. New evidence is recorded in the open community-read-metric-concurrency task;
causality is unproven and no unrelated fix was attempted. Documentation-only follow-up
records this outcome; a subsequent green run must not be described as fixing the defect.

## 2026-09-08 earlier Tokyo source-credit and platform review

Latest continuation stays on PR #344 / codex/hotel-content-review-kyoto. Main and runtime
were reverified at 7f21d7e, schema 0060; no deployment or migration. Previous head 9de855e
passed all four jobs on PR 34170581417 and push 34170579355. The earlier community smoke
metric defect remains separately tracked; no claim that this hotel work fixed it.

Six Tokyo official pages and exact Trip.com documents matched hotel names/street numbers.
Chrome create-tab and recovery timed out; no successful browser UI/map review or override
is claimed. Trip links passed ordinary safe HTTPS/DNS/redirect checks. Booking/Expedia
were unconfirmed; Rakuten timed out. Three Agoda URLs were healthy but lacked reviewable
document identity, so HTTP success alone did not cause approval. Other slots lack URLs.

Verified backup /root/travel_scanner_pre_hotel_candidates_20260907T234914Z.dump preceded
production writes. Guarded, versioned admin services added source credits to the original
six Tokyo products plus thirty independent pending OTA slots (24 URLs, six unresolved).
Each credit edit and restored product approval committed atomically with its five options;
existing official links, product IDs, labels and locations were preserved. A tested pure
prepare_credit_update helper rejects old legacy projections and changed identity/credits.
Other 54 products/original 330 options/config fingerprints remained unchanged.

A separate exact-ID/URL/version preflight and normal option review approved only the six
Trip.com links, all healthy and browser_verified=false, with audited outcomes. All products,
other 354 options and config were fingerprint-checked unchanged in that second operation.
No replay of pending packages, direct approval SQL, provider credential export or city switch.

Current live counts: 60 hotels (11 product-approved, 49 pending), 360 platform records
(13 approved, 347 pending). Approved: six original Tokyo official + six Tokyo Trip + RYSE
official. All six original Tokyo source credits and six Trip audit records verified.
Read-only en/ja/ko/zh-TW/zh-CN service smoke exposes official + Trip direct options with
attribution for those six; public_enabled remains false and destinations remain [tokyo].
Zero cities accepted; no affiliate/price enablement or generated click/conversion events.

126 related API/content/platform/offline-source tests passed, plus Ruff/format, mypy across
254 sources, 27 tooling tests, five locales/25 namespaces and task integrity. Content/docs/
tests only; full new-head CI runs on the existing draft PR. See
docs/hotel-platforms/review-2026-09-08-tokyo.md and tokyo.review-2026-09-08.json for evidence.
The older Tokyo fingerprint/single-official-option smoke is now historical, not a valid
post-credit baseline. Remaining: other independent OTA checks, four new Tokyo maps,
remaining Seoul Naver identities, reusable Kyoto/Busan coordinates and per-city acceptance.
Release the task at handoff; it is not done. No merge authorization in this continuation.

While CI ran, main advanced to b3e49a3 via PR #345. Synced that main into this work branch;
the only conflict was generated tasks/BOARD.md, resolved solely with tasks:board. No merchant
code was altered. Narrowed this unfinished task's scope to hotel evidence and its content
tests, since the architecture is already merged and shared models/translations need not
remain claimed. Post-sync: 126 related tests, Ruff and mypy across 255 sources passed;
five-language and task checks rerun. This branch sync is not a PR merge or a deployment.

## 2026-09-08 first import checkpoint (historical)

Continuation claimed on `codex/hotel-content-review-kyoto` from latest main
`7f21d7eb2af223a561bc04519ce67021198b1068`, preserving the original dirty workspace.
PR #342 had already merged and production later advanced to this main revision; observed
readiness is schema `0060_community_places`. This turn did not redeploy or migrate.

Added ten Kyoto pending research inputs and municipal CC BY 4.0 permit evidence, three
areas and 40 official/Booking/Trip/Agoda candidate links. Expedia/Rakuten remain unconfirmed.
The July 2026 permit spreadsheet has no coordinates; none were guessed, geocoded or copied
from providers, and no paid Places lookup ran. Kyoto still lacks coordinates/Place IDs.
Selected names/addresses/category/permit dates only are saved; do not re-download the whole
spreadsheet to recover these facts. Busan's ten hotels remain outstanding.

Chrome recovered long enough to verify primary Naver names, street numbers and official
sites for L7 Myeongdong, Four Points Josun Myeongdong, Mercure Hongdae and L7 Hongdae.
These are four new identity checks, plus RYSE's earlier one. Parnas navigation was interrupted;
debugger/fresh-tab recovery failed. Five Naver identities now have primary evidence, not ten.

With user authorization to add/review hotels, a verified database backup was taken and the
normal CSV/admin import service was run over the existing SSH session. The serializable,
exact-new-key guarded import skipped all six existing Tokyo products/options, added 44
pending hotels and 264 pending options, and recorded preview/commit audits. Run ID:
`31379d38-7180-4ceb-b2af-75ba5b6238ad`. Four newly browser-verified Seoul product locations
then passed version-checked admin edit/review; all their platform options remain pending.
No browser auth tokens were forged or exported, and no affiliate/API/public switches changed.

Verified live: 50 total hotels, 10 product-approved (six original Tokyo plus four Seoul
locations), 40 pending. Zero cities meet rollout acceptance. Original Tokyo/config/options
fingerprint stayed identical. See `docs/hotel-platforms/review-2026-09-08.md` for counts and
backup evidence. Pending JSON remains research input, not sync truth: never blindly replay
it over reviewed production rows or reset original hotels to pending.

117 related tests passed; Ruff, formatting, five-language catalogs (25 namespaces), and
task checks passed. Content/test/docs-only change; no new UI behavior or full-60 acceptance
claimed. Remaining: Busan, Kyoto durable locations, five remaining Seoul Naver checks,
independent platform landing checks/approvals, existing six Tokyo source-credit update,
and per-city rollout gates. Keep task open and release at handoff.

## Why

### 2026-09-08 Busan continuation checkpoint

Continuing the same draft PR #344 from main 7f21d7e. Ten Busan pending candidates now
cover Seomyeon/Haeundae/Nampo, with official and Booking/Trip identity references.
Other OTA leads stay unconfirmed; no licensed Busan coordinates or precise Naver IDs
are claimed. Source credits explicitly do not assert a content reuse license.
Excluded Solaria's announced 2026-12-29 closure, unresolved ibis/ Central Seven rename,
wrong Arban City branch, and conflicting Toyoko tourism-directory address.

After a verified PostgreSQL backup, normal import service staged ten Busan products and
sixty options pending; run cb5921a5-d87a-4ff9-9946-5c3c3ad19689. Serializable preflight/apply
fingerprint guard preserved all fifty existing products/options/config. Then RYSE alone
passed normal versioned location review, using its dated Sep 7 Naver observation and a
fresh Sep 8 Chrome official-contact check. Its official link independently passed healthy
URL review. No OTA approvals, city switches, affiliate/quote enablement, deployment or merge.

Live verification: 60 hotels, 11 product approved, 49 pending; 324 new options across batches,
one approved RYSE official and 323 pending. Original Tokyo six/config fingerprint unchanged.
Five-language read-only smoke passed without provider requests/clicks. Zero complete cities.
Details: docs/hotel-platforms/review-2026-09-08-busan.md. Never replay pending files over
reviewed rows. Chrome timed out on the next Naver check and one fresh-tab recovery failed;
do not claim new Naver/OTA browser reviews. Task remains open for location/platform/source gaps.

Previous SHA fe8a61d PR CI passed all jobs; same-SHA push smoke failed in unrelated community
test with ECONNRESET alongside metric uniqueness errors. Recorded the suspected race in
2026-09-07-community-read-metric-concurrency, not patched as part of hotel content.

Continuation validation: 120 related tests, Ruff/format, mypy (254 source files), 27 tools
tests, five locales/25 namespaces, task checks and production read-only five-locale smoke
passed. New head CI is checked in PR #344. Release rather than mark done; city acceptance
and remaining independent reviews are still open.

Keep one hotel identity while independently reviewing each platform, enabling commission links only after qualification, and preparing honest on-demand quotes without activating paid APIs.

## Definition of done

- [x] Ordinary and qualified affiliate links share one independently reviewed platform option; legacy clients remain compatible.
- [x] Migration preserves product/trip IDs and removes dual authority in facts.hotel_links.
- [x] No unlicensed live API, fake price, guessed platform identity, or automatic booking.
- [ ] Six cities each have ten verified hotels, three areas, official and two OTA links, checks for all five OTAs, and public source attribution.
- [x] API, migration, i18n, typecheck, lint, production build, five-language responsive E2E pass.
- [ ] City rollout only after factual review and actual link checks. No unverified affiliate enablement.

## Steps

- [x] Isolated worktree from verified main 54009ba; original dirty worktree preserved.
- [x] Independent options, compatibility import, safe clickout, quote contract and policy gates.
- [x] Five-language public/admin panels and source attribution.
- [x] Extended regression tests and full validation.
- [ ] Verified 60-hotel research/import package and city release gates.

## How to verify

Run uv pytest for travel services and hotel platforms; fresh Alembic migration on a disposable PostgreSQL database; web i18n/typecheck/lint/build/Vitest and travel-services Playwright on 320/390/1280px.

## Notes

Full web regression completed: 126 test files / 729 tests passed. All three pending city packages validate (four content tests), including the licensed Osaka coordinate-column correction. Taipei CSV preview has ten rows; i18n and Ruff rerun passed.

Branch CI 34131439819: web, containers and unmocked full-stack smoke passed. Full Linux API ran 1,721 tests; two new assertions incorrectly assumed empty shared audit tables. Fixed them to assert exact before/after deltas (ordinary adds zero affiliates, one affiliate plus one fallback adds exactly one). Related integration rerun: 19 passed. Added independent option recheck reminders and hotel affiliate/fallback counters, and preserved saved evidence in the admin editor; three admin component tests passed. A new full CI run is required for the fix.

Corrected branch CI 34132295317: Linux API 1,722 passed / one existing skip; containers and full-stack smoke passed. Final hardening refreshes/locks legacy omitted options before disabling, preventing a stale identity-map version from overwriting an independent review; three related integration tests passed. A final push reruns CI for that change. Chrome separately opened the saved Tokyo Station Hotel Place ID and confirmed name/address against the official identity; no Google price/rating/review/coordinate fields were copied. This is one spot check, not blanket approval of the 30 candidates.

Previous handoff: the architecture was isolated on codex/hotel-platforms, with content acceptance open. The user subsequently authorized merging that architecture milestone, not declaring a finished 60-hotel release; see the follow-up below. Do not re-request already saved Place IDs, copy OTA/Google content, or mark pending rows approved merely because schema tests pass. Finish source/platform/map reviews before staged admin import. No new paid APIs, affiliate activation, production migration, content writes or deployment were performed.

0057 migration succeeded on empty PostgreSQL. Related migration/API regression batch: 113 passed; row-lock hardening rerun: 40 passed. Ruff and full mypy (236 source files) passed. Five-language i18n, typecheck, lint and production build passed. Related Vitest: 32 passed; Playwright desktop 50 and mobile 53 passed. Actual Redis/RQ daily worker smoke passed on isolated PostgreSQL/Redis. Tools: 27 passed. Full Python collection on Windows hits the existing deployment agent UnixStreamServer import; Linux CI must verify the full suite.

Original content checkpoint: thirty pending research inputs (Tokyo, Osaka and Taipei each ten), preserving the original Tokyo six source keys. Twenty-four metered IDs-only lookups have already run; saved IDs must not be re-requested unnecessarily. Production settings, secrets and hotel rows are unchanged. Do not mark this task done or enable cities from the pending-input count.

## 2026-09-07 content follow-up

PR #341 merged the architecture milestone at f2c3b2af431d093bfb2169fefab7deb41cc90427 with explicit user authorization; post-merge CI 34135118181 passed all jobs. No deployment was requested/performed by that merge. The continuation uses codex/hotel-catalog-followup from that latest verified main in C:\Users\x8120\hotel-platforms; the original dirty worktree remains untouched.

Added ten Seoul pending inputs: four Myeongdong, three Hongdae, three Gangnam. Forty research inputs now exist, but **zero cities have completed rollout acceptance**. Each Seoul hotel has an official source plus cross-checked Booking, Trip, Agoda and Expedia property pages (50 discovered links including official). All five target OTAs were independently searched. Rakuten remains unconfirmed: Japanese-site leads are outside the current international-only host policy; L7 Gangnam's international listing needs street/address and live landing confirmation. Do not mix Rakuten Japan/global IDs or broaden affiliate rights to fill a content gap.

Resolved Seoul public licensed coordinates: OA-16044's Sheet CSV form works with serviceKind=1 despite the empty file tab. CP949, EPSG:5174 explicitly documented by Seoul, not older mirrors' EPSG:2097. Selected active permit IDs/raw X/Y and transformed WGS84 are in seoul.evidence.json, with KOGL Type 1 attribution also in public source_credits. No complete CSV or unrelated/personal fields retained. The optional pyproj==3.7.2 inspector can verify all saved transforms offline; no dependency was added to the application. Do not fetch again just to recover the saved facts.

Chrome inspected RYSE's official direct Naver link 1578505636; heading/address/homepage matched 130 Yanghwa-ro. All new map_verified flags remain false until independent admin review. Five other Naver IDs are third-party leads only in evidence; four are still missing. Further Chrome attempts failed with Debugger unattached, and in-app fallback also failed to attach. Do not claim those map checks happened. Known hotel-restaurant Naver IDs and wrong same-brand properties are explicitly excluded in evidence. Solaria's old host failed DNS; new official NNR site is used. Parnas standalone sites failed TLS; no certificate checks bypassed, official IHG SEOHA used instead.

Validation: 114 related tests passed (API content/platform/direct-link/travel-service tests plus 13 optional offline research-tool checks). Verified all ten stored projections without network, UTF-8 admin CSV transfer, closed/missing/duplicate permit rejection, and pending candidates never publicly usable. Five-language catalog and task integrity checks passed. No runtime/UI/migration changes in this follow-up; full CI will still run on the PR. Remaining: Kyoto/Busan, Rakuten usable entries, remaining map/landing reviews, separate product/option approvals and staged city release. Content task stays open; no new merge authorization or production writes/enablement/deployment assumed.
