# 2026-09-08 — verified deployment and five Taipei hotel reviews

## Result

PR [#357](https://github.com/x812033727/travel_scanner/pull/357) was synced with latest
main `f48e9a6`, revalidated at head `71f0431120ea0e83e1390dea1c0e7e8457e82a83`
(all eight checks), then SHA-guarded squash merged at 05:43:48 UTC to
`00ffc710ebf902f56a00a69869f96e92bf3e84d0`. Post-merge main run
[34191743658](https://github.com/x812033727/travel_scanner/actions/runs/34191743658)
passed API, web, containers and full-stack smoke before deployment.

The deployed application SHA is `00ffc71`; all eight app services were verified at
that exact version with zero restarts. PostgreSQL/Redis container IDs, runtime `.env`
hash/mode, existing volumes and community switches were preserved. Community remains
off. Schema remains `0062_merchant_platform_links`; no new migration in this batch.
Three consecutive readiness checks, five locale homepages and five actual HTTPS
Seoul BFF reads passed. Independent hotel verification proved the existing 60 hotel
products/options/config and the prior Seoul review checkpoint were unchanged by deployment.

The clean archive's SHA-256 is
`db748e417e36cc4fd6ed9fa238232e24059cf95d4d75120ac1685713a7db767b`.
Release: `/root/mokaair-release-00ffc71-peH6Zbnh/source`.
Verified pre-deploy custom PostgreSQL archive:
`/root/travel_scanner_pre_deploy_00ffc71_20260908T055431Z.dump` (7,099,756 bytes).
Previous images/source/backups remain available; no cleanup, chmod of the canonical
checkout, volume recreation, secret export or deployment-agent enablement.

First script attempt built successfully and ran the no-op migration but stopped before
activation because Compose consumed piped script input. Read-only inspection confirmed
old services remained healthy. Redirecting the migration command's stdin from `/dev/null`
fixed the script; the guarded second execution completed. Startup briefly reset loopback
connections before readiness stabilized. Initial manual BFF probes used an incorrect path/
parameter; corrected to `/api/travel/travel-services?destination_id=seoul&type=hotel`.
Neither diagnostic error is represented as a product fix or an outage-free deployment.

## Taipei continuation

Continued in isolated `codex/hotel-content-review-taipei` from merged main after deployment.
Original dirty workspace was untouched. **60 distinct identities remain: 22 approved
products / 38 pending; 80 approved platform options / 280 pending**. This completes
five already-imported pending hotels, not five new duplicate identities.

| Hotel | Newly approved ordinary options |
| --- | --- |
| Palais de Chine | Official, Booking, Trip |
| Cosmos Hotel Taipei | Official, Booking, Trip, Rakuten |
| Caesar Park Hotel Taipei | Official, Booking, Trip |
| CityInn Taipei Station Branch III | Official, Booking, Trip |
| amba Taipei Ximending | Official, Booking, Trip |

Taipei public results increase **0 → 5 hotels / 16 options** in all five locales.
Each has official plus two independently reviewed OTAs; Cosmos also has Rakuten.
Still **zero complete cities**: Taipei needs five more hotels and three-area coverage;
the broader per-city five-platform checks and six-city acceptance remain open.
No setting/affiliate/quote switch changed, paid provider API request, clickout or test order.

## Identity and source boundaries

Exact saved Place IDs were opened in Chrome. Each hotel heading, street number and
official website matched the already-saved official/government identity. Only the
review result/ID is retained, not Google descriptions, coordinates, ratings, reviews,
prices, photos or Plus Codes. Licensed Tourism Administration coordinates and public
credits remain byte-for-byte unchanged apart from `facts.map_verified=true`.

Primary source URLs and minimal identity facts are in `taipei-five.review-2026-09-08.json`.

- Palais: official address Chengde Road Section 1 **3**; preserve the existing `ph.trip.com`
  property 701703 URL instead of guessing a `www` locale replacement.
- Cosmos: official homepage/English footer confirms Zhongxiao West Road Section 1 **43**.
  Rakuten international property **34123457140865** was discovered through an indexed
  result, then freshly verified in Chrome with its full street address. The web extractor
  timed out; the indexed result alone was not used as current identity proof.
- Caesar Taipei: Zhongxiao West Road Section 1 **38**. Parking directions' 50/47/66,
  Taipei Station's 3, Caesar Metro and Caesar Banqiao are not this property.
- CityInn **Branch III**: Chang'an West Road **77**, not Branch II at 81. Its official
  contact page loaded in Chrome and supplied the address missing from the location-page
  text. Initial navigation timeout was followed by successful visible-page inspection.
- amba **Ximending**: Wuchang Street Section 2 **77**. Current official HTML footer
  corroborates the saved identity; failed PDF extraction was not claimed as a fresh read.

Five Booking pages and the new Rakuten page were actually opened in Chrome and their
hotel names/full addresses checked. Their server health remained `unconfirmed`, not
`healthy`; the existing audited browser-confirmation mechanism permits approval while
retaining HTTPS/DNS and unsafe/unavailable-target rejection. No CAPTCHA, authentication,
certificate or URL-safety bypass. All five Trip documents show matching street numbers.

Cosmos and Caesar official links initially failed normal non-browser review, rolling back
unchanged at version 1 with no review audit. After freshly opening the exact saved URLs
in Chrome, both passed browser-confirmed review: Cosmos healthy, Caesar unconfirmed.
These are documented follow-ups, not silently converted initial successes.

Only one new candidate URL was added (Cosmos Rakuten), via its existing independent slot:
pending/version 2 on edit, then approved/version 3 on separate review. All other approved
options become version 2. Agoda/Expedia and the other Rakuten gaps remain pending. Regional
Expedia lists and Palais's Japanese Rakuten ID 109270 were not turned into invented links.
Pending JSON stays an unapproved research/import input; **never replay it over live rows**.

## Guarded writes and independent verification

After deployment and before content writes, a second verified PostgreSQL archive was made:
`/root/travel_scanner_pre_taipei_review_20260908T055940Z.dump` (7,566,576 bytes).

Preflight whole-catalog fingerprint:
`977a7d3c323289852332b87dcd442706f8d2c3346fb57718ea6a207e407d89ba`.
Untouched other 55 products / 344 options / config-v5 fingerprint:
`5a5e10994fcd003d0d50597a29d96bdc6d274d31fc5bfbfe82b87d414abbd863`.

Normal versioned admin operations created 32 audit records: five product edits, five
location reviews, five product approvals, one option edit and 16 option approvals.
Independent read-only verification checked all expected statuses, versions, health,
browser flags, source facts, audit counts and unchanged-row fingerprint. Its initial
source-credit assertion used the wrong response nesting; corrected to
`product.facts.source_credits` after inspecting the schema, with no production mutation.

Thirty internal five-locale/six-city reads and five real HTTPS Taipei BFF reads passed:
Tokyo 10 / Osaka 2 / Kyoto 0 / Seoul 5 / Busan 0 / Taipei 5. Taipei exposes 16 ordinary
options, five public government-source credits and `quote_status=not_configured` only.
No affiliate link/quote endpoint was called and no click/conversion event was generated.

Chrome also opened the deployed Taipei services page: the initial three cards and
"view all (5)" appear; Cosmos's booking panel lists official, Booking, Trip and Rakuten
with "check price on platform", no fabricated price. Escape dispatch reported a tool
timeout; a fresh DOM read confirmed the dialog closed and the catalog remained visible.
No booking buttons or external clickouts were invoked.

145 relevant content/API/offline-source tests, Ruff/format, mypy across 257 sources,
five-language/25-namespace translation completeness and task/tool checks passed locally.
Content regression tests cover pending input isolation, precise map/source invariants,
independent reviews, browser-confirmed unconfirmed health versus unsafe rejection, original
Trip locale preservation and the observed Rakuten identity. Full new-head CI is tracked
on the continuation PR. Release the shared task at handoff, not done.
