# Hotel platform rollout — work in progress

## Implementation

The architecture milestone merged in PR #341 at `f2c3b2af431d093bfb2169fefab7deb41cc90427`
on 2026-09-07; post-merge CI 34135118181 passed. This did **not** complete the content
milestone or publish any hotel package. PR #342 subsequently merged the Seoul research
checkpoint, and production was deployed. The 2026-09-08 continuation uses isolated
`codex/hotel-content-review-kyoto` from main `7f21d7eb2af223a561bc04519ce67021198b1068`.
See the dated production review record below; older checkpoints are not current live counts.

PR #344 subsequently merged the Kyoto/Busan/Tokyo content checkpoint at `2e5e9fe` on
September 8 after all eight latest-main checks passed. The next isolated continuation is
`codex/hotel-content-review-osaka`; see `review-2026-09-08-osaka-five.md` for its current
counts and the independently changed production catalog configuration.

PR #348 then merged at `9e94d03`. The latest checkpoint is
`review-2026-09-08-namba-map.md` and `namba-map.review-2026-09-08.json`:
60 identities, 17 approved products / 43 pending; 41 approved options / 319 pending.
Five new location approvals, ten platform approvals and four candidate URLs were added
without changing rollout settings. Five-locale public reads return Tokyo 10 / Osaka 2;
no city yet satisfies official plus two approved OTA links for every hotel.
Earlier dated review files and pending import inputs are historical evidence, not a
live-state synchronization source. Never replay pending packages over reviewed rows.

PR #352 subsequently merged at `f65890a` after latest-main checks. The newest checkpoint
is `review-2026-09-08-kyoto-five.md`: five Rakuten candidate additions, seven platform
approvals, one failed link review preserved pending, and a sourced Hyatt Regency Kyoto
future-closure hold (May 9, 2027). Still 60 identities / 17 approved products; platform
options are now 48 approved / 312 pending. Kyoto remains publicly empty without reviewed
locations, and the prior Tokyo/Osaka public counts and rollout settings are unchanged.

`0057_hotel_booking_options` migrates legacy links into independent reviewed identities.
Products and trip associations retain their IDs. `facts.hotel_links` is accepted/projected
for old clients, but never stored as a second authority. New imports use a JSON
`booking_options` CSV column. Omitting legacy links does not delete managed options.

Public clients get one `booking_options` entry per platform, with a saved-ID POST clickout.
Ordinary navigation requires no Travelpayouts credentials. Affiliate qualification, exact
product/brand/target, project and settings are checked server-side. Failures may fall back
only to that option's approved direct URL, if ordinary links are enabled. Clicks do not book.
Health checks run in the existing background maintenance job. 403/429 and timeouts are
unconfirmed, not proof of delisting. Unsafe redirects and confirmed 404/410 disable the
individual option. Manual review can confirm a bot-blocked page, never bypass URL safety.

Quote adapters are intentionally empty. Credentials alone cannot enable a price provider.
The policy requires comparison rights, terms and a positive budget, plus a reviewed platform
property ID and an explicitly integrated adapter. Searches are on demand; no price sweeps,
no shared TTL, no persisted/reused quotes. Comparison requires complete public same-currency
totals including taxes and at-property charges, matching occupancy and reviewed room/bed/
meal/cancellation/payment identity. Two distinct valid platforms are needed for a lowest
label. Room keys must represent **all rooms in the requested allocation**, not a single
room from a multi-room booking. Source-approved factual terms are displayed alongside prices.

Official integration references (checked 2026-09-07):

- https://support.travelpayouts.com/hc/en-us/articles/25289759198226-API-for-Travelpayouts-partner-links
- https://developers.booking.com/demand/docs/getting-started/prerequisites

## Content status — 60 research inputs, not 60 accepted hotels

`tokyo.pending.json` contains 10 researched Tokyo hotel candidates, preserving the six
existing `editorial:tokyo:*` keys and adding four Tokyo Station/Ginza properties. Each has
an official source and discovered Booking/Trip property pages. These are **pending inputs**,
not automatic approval or a claim of live availability. Other platform checks are explicitly
incomplete. New four Place IDs were obtained with four metered IDs-only requests; a singular
search result is not a completed visual map review, so `map_verified` remains false for them.
The original six retain their prior reviewed map IDs. Never repeat their lookup unnecessarily.

`osaka.pending.json` and `taipei.pending.json` each add ten researched candidates, three
existing lodging areas, official sources, discovered Booking/Trip property pages and metered
IDs-only results. They are NOT published or approved. Tokyo additionally includes fifteen
discovered Agoda/Expedia/Rakuten options. Each platform still needs its own factual review.

`seoul.pending.json` adds ten candidates across Myeongdong (four), Hongdae (three), and
Gangnam (three). Each has an official source plus Booking, Trip, Agoda and Expedia
property pages whose names and street addresses were cross-checked. All five target OTAs
were searched independently. Rakuten remains unconfirmed: nine Japanese-site leads are
outside the current international-site allowlist; the L7 Gangnam international property
needs its street identity/live landing checked. Do not interchange Japanese/global IDs
or interpret a search result as an available room, affiliation or admin approval.

`seoul.evidence.json` keeps the ten selected public permit IDs, original projected
coordinates, source/license, identity URLs and per-platform findings. Only RYSE has an
official direct Naver link whose actual Chrome name, address and official website matched.
On 2026-09-08, Chrome additionally verified L7 Myeongdong, Four Points Josun Myeongdong,
Mercure Hongdae and L7 Hongdae by their names, street numbers and official websites.
Those four Naver URLs are now in the pending research input; exact observed checks are
recorded in the evidence. The four corresponding production products passed location
review; all their platform options remain pending. Parnas could not be verified after
Chrome disconnected, and four other identities are missing. Pending JSON files deliberately
retain `map_verified: false`; do not replay them over reviewed production products.
No map/OTA coordinates, photos, prices or review text were imported. Known restaurant IDs
and same-brand wrong branches remain excluded.

`kyoto.pending.json` adds ten candidates: four Kyoto Station, three Shijo/Kawaramachi,
three Higashiyama. `kyoto.evidence.json` records selected licensed municipal permit
names/addresses/category/dates, ten official sources and Booking/Trip/Agoda candidate
pages (40 discovered links). All five target OTAs were included in research; Expedia/Rakuten
remain unconfirmed. Indexed names/addresses are not completed browser reviews.
The permit spreadsheet has **no coordinate columns**. Latitude, longitude, coordinate
source and Place ID are absent, not guessed or copied from Google/OTAs. These ten cannot
pass product review until durable coordinates and exact identities are established.

`busan.pending.json` adds ten candidates across Seomyeon (three), Haeundae (five),
and Nampo (two). Official identity facts and Booking/Trip property URLs were cross-checked;
Agoda/Expedia/Rakuten discovery remains unconfirmed with leads in `busan.evidence.json`.
These are pending research, not ten licensed/reviewed locations. No durable coordinates
or exact Naver identities have been established. Source credits explicitly say that no
website content reuse license is asserted; they are not an open-data license or permission
to copy descriptions/images. Do not approve these products before filling the source gaps.
Solaria Busan is excluded because its official notice schedules closure after checkout on
2026-12-29. The unresolved ibis/ Central Seven rename and wrong Arban City branch are also
documented, not silently matched. Toyoko's conflicting tourism-directory address was not used.

| City | Research inputs | Accepted for city rollout | Remaining |
| --- | ---: | ---: | --- |
| Tokyo | 10 | 0 | Three pending map checks, remaining platform checks and second OTA per reviewed hotel |
| Osaka | 10 | 0 | All maps pending; five official/Trip pairs approved, four new Agoda URLs pending; other OTA reviews outstanding |
| Kyoto | 10 | 0 | Licensed coordinates, exact Place IDs, live platform checks and independent approvals |
| Seoul | 10 | 0 | Five unresolved Naver reviews, platform landing checks and independent option approvals |
| Busan | 10 | 0 | Licensed coordinates, exact Naver identities, platform landing reviews and independent approvals |
| Taipei | 10 | 0 | Map and platform review, remaining OTA checks, independent approvals |

Do not call this task done or enable any city using the research-input count. On 2026-09-08,
44 new candidates were imported as pending (Tokyo four, Osaka/Taipei/Seoul/Kyoto ten each),
skipping and preserving all six existing Tokyo products/options. Four new Seoul locations
then passed normal admin product review with audit records. All 264 newly imported platform
options remain pending. The live total is **50 hotels: 10 product-level approved, 40 pending;
zero completed cities** at the first batch checkpoint. Product approval is not platform approval or city rollout.
Public/affiliate/price settings are unchanged. Only the earlier 24 IDs-only usage-meter
increments were made (four Tokyo, ten Osaka, ten Taipei); this continuation made no Google
lookup or price API call. The one-off lookup scripts have already run: do not repeat them to recover saved IDs.

Earlier 2026-09-08 Busan continuation: ten Busan products and sixty options were imported as
pending, preserving all fifty existing products/options. RYSE then separately passed product
location review using the 2026-09-07 Naver observation plus a fresh Chrome official-contact
check; its official option passed normal URL/health review. No OTA option was approved.
At that checkpoint the total was **60 hotels: 11 product-approved, 49 pending; 323 pending new options
and one approved new official option**. Original Tokyo six and catalog settings are unchanged.
Public enablement remains off, configured destinations remain Tokyo only, and no city has
completed rollout acceptance. See `review-2026-09-08-busan.md` for that historical checkpoint.

Earlier 2026-09-08 Tokyo review: added the missing source credits on the original six hotels
and thirty independent OTA slots (24 found URLs, six unresolved). Six Trip.com links passed
normal independent admin/health review with no browser override; the remaining 24 slots
stay pending. Existing product identities, names, coordinates, official links and config
were preserved. The total is **60 hotels: 11 product-approved, 49 pending; 360 platform
records: 13 approved, 347 pending**. Five-language read-only smoke shows official + Trip.com
for the original six in the enabled internal catalog; public enablement is still off.
This is not a city rollout or a new map review. See `review-2026-09-08-tokyo.md` and the
per-option `tokyo.review-2026-09-08.json`. Never replay the older original-Tokyo fingerprint
or one-option smoke assertion after this deliberate attribution/platform update.

Earlier Tokyo continuation: Ryumeikan's saved exact Place ID was successfully checked in
Chrome against its name, street number and official website; its product passed normal
review. The next map navigation/recovery timed out, so the other three products remain
pending. Eight official/Trip options were independently approved after document identity
and live safe-health checks, without browser override. Three new Agoda candidate URLs were
added to existing slots and stay pending because their direct identity pages were opaque.
Current total: **60 hotels, 12 product-approved / 48 pending; 360 options, 21 approved /
339 pending**. The enabled internal Tokyo catalog has seven reviewed hotels; public
enablement remains off and no city is fully accepted. See `review-2026-09-08-tokyo-four.md`
and `tokyo-four.review-2026-09-08.json`; older snapshots are historical. Pending JSON still
must not be replayed over the newly reviewed Ryumeikan product.

Latest Osaka continuation: five existing hotels now have independently approved official
and Trip options (ten approvals), after name/street document review and normal live safe
link checks. Four missing Agoda URLs were added pending; their opaque direct documents do
not justify approval. Granvia's inconsistent-city Agoda result was not added. No successful
Chrome identity check occurred this turn, so all Osaka products/maps stay pending.
Current total: **60 hotels, 12 approved / 48 pending; 360 options, 31 approved / 329 pending**.
All 60 product records, other 346 options and configuration were fingerprint-preserved.

Production config independently changed to version 5 with public services/all six cities
enabled before this batch. This task did not change or roll it back. Five-language public
smoke confirms Osaka's pending hotels remain hidden while Tokyo has seven reviewed hotels
with official + Trip options. An enabled city is not a content-complete city: zero cities
meet the full hotel/area/two-OTA acceptance criteria. See `review-2026-09-08-osaka-five.md`
and `osaka-five.review-2026-09-08.json`; previous disabled-catalog snapshots are historical.

## Tokyo coordinate attribution

Coordinates are unchanged excerpts from Tokyo Metropolitan Government's licensed dataset,
not Google/OTA coordinates. `source_credits` adds the previously missing public attribution
to all six existing hotels, plus the four new candidates:

- Dataset: 宿泊施設等の施設情報ポータルサイト「だれでも東京」宿泊施設
- Publisher: 東京都デジタルサービス局
- https://www.opendata.metro.tokyo.lg.jp/digitalservice/130001_Daredemo_Tokyo_accommodation.csv
- https://portal.data.metro.tokyo.lg.jp/terms/
- https://creativecommons.org/licenses/by/4.0/deed.ja

Mokaair extracted names/coordinates, classified areas and updated names from official sites;
this is not a Tokyo-government endorsement. Only verified official-language names are used.
No OTA descriptions, photos, prices, star ratings, reviews or cancellation promises are imported.
Keio Plaza Premier Grand's separate Booking listing was excluded from the main hotel mapping.

## Osaka and Taipei sources

- Osaka: https://www.city.osaka.lg.jp/kenko/page/0000382418.html (CC BY 4.0).
  The combined CSV labels latitude then longitude but actually contains east longitude then
  north latitude. The import explicitly reverses the column assignment, retains numeric values,
  and documents that change in public attribution. Never silently treat 135 degrees as latitude.
- Taipei: https://data.gov.tw/dataset/7780 (Government Data Open License v1).
  Only selected licensed hotel names/coordinates/record IDs were extracted from HotelList.json;
  descriptions, photos, classifications and reference prices were not imported. The dataset's
  own geographic-source note is preserved here: its map coordinates are primarily Google based.
  They are supplied through the government's open-data distribution, not fetched from Places.
  Confirm this provenance and the applicable distribution grant during content review.
- Taipei Solaria's old official page explicitly points to https://solaria-taipei.nnr-h.com/;
  the new official site is used. Caesar Park Banqiao and Kenting were excluded from Taipei
  station mapping. CityInn branch III uses the 77 Changan West Road identity, not branch II.

## Import / rollout

From `apps/api`, print the reviewed transfer format with:

```powershell
uv run python ../../docs/hotel-platforms/prepare_import.py ../../docs/hotel-platforms/tokyo.pending.json
```

Pending packages are research inputs, **not a synchronization source of truth**. Existing
production records now include separately reviewed fields; never bulk-replay an old package
over them. Preview first, skip existing source keys for additions and use version-checked
individual edits for a deliberate review. The September 8 batch enforced serializable
transactions, exactly 44 new keys, preserved product/option/config fingerprints,
pending-only options, no offer/brand writes, and audit records. A validated database backup
was taken first. See `review-2026-09-08.md` for that first import checkpoint and the newer
dated Tokyo review above for current counts.

Paste into admin CSV preview. Review new/modified/duplicate/missing entries before committing;
all changed products and options remain pending. Use the separate option review controls.
Inspect each actual destination, not a platform search page. Do not infer approval from this
file or from a successful HTTP response. Activate each city only after ten accepted hotels,
three valid lodging areas, official plus two OTAs per hotel and checks for all five platforms.
Affiliate and price API switches stay separate and off until their independent checks succeed.

## Verification

Completed so far: fresh PostgreSQL migration through 0057; isolated legacy-schema upgrade,
idempotency, downgrade and preserved trip-link tests; API/quote/link tests; five-language key
and ICU validation; typecheck, lint, production build; responsive platform panel browser tests.
An actual RQ SimpleWorker also executed the daily job against isolated PostgreSQL/Redis
successfully. Related API/migration batch: 113 passed; after row-lock hardening, 40 integration
regressions passed again. Desktop Playwright: 50 passed; mobile project: 53 passed. Provider
calls in tests are mocks and are not evidence of reservations or commissions.

Full local Python collection is blocked by the existing deployment agent's UnixStreamServer
import on Windows. Linux CI 34132295317 ran 1,722 passing API tests (one existing skip),
plus successful container and full-stack smoke jobs. Full web suite: 126 files / 729 tests passed. No city
is considered complete from a pending-file count, and no paid price API was enabled.
See the task record for remaining validation and content acceptance. Architecture PR #341
is merged; hotel content acceptance remains incomplete. This content continuation did
not deploy application images, migrate the schema or change rollout settings.

Chrome spot check: the saved Tokyo Station Hotel Place ID resolves to the expected hotel
name/address and official website. This was identity-only inspection: no Google prices,
ratings, reviews, descriptions or coordinates were copied into the catalog. All pending
inputs still require independent admin approval; a single spot check does not certify a city.

## Remaining source research

Kyoto's current licensed permit list is available at
https://data.city.kyoto.lg.jp/dataset/00039/ (CC BY 4.0, July 2026 list).
The July 31 permit spreadsheet was inspected on September 8. It establishes licensed
names/addresses, not coordinates. The selected ten records are in `kyoto.evidence.json`;
do not download again just to recover them. Only selected accommodation fields are retained,
not operator/personal names. Whitespace/full-width Latin normalization is editorial;
Celestine's source has a private-use glyph, so its public title uses confirmed official English.
Terrace Hachijo is not the separate Hachijoguchi property; Kyoto Shijo is not Shinmachi Bettei.

## Seoul licensed coordinates and repeatable checks

Source: [서울시 숙박업 인허가 정보](https://data.seoul.go.kr/dataList/OA-16044/S/1/datasetView.do),
published by 서울특별시 시민건강국 보건의료정책과, updated 2026-09-07.
[KOGL Type 1](https://www.kogl.or.kr/info/licenseType1.do) requires source attribution;
the public credit includes publisher, 2026 source year, direct source/license links,
permit ID and transformation explanation, without suggesting government endorsement.

The separate file-download tab says there are no files, but the **public Sheet tab's CSV
form works** with `serviceKind=1`, `infId=OA-16044`, `srvType=S`, `pageNo=1`,
`ssUserId=SAMPLE_VIEW`, and empty `strWhere` / `strOrderby`, posted to
`https://datafile.seoul.go.kr/bigfile/iot/sheet/csv/download.do`. No API key or login is
required. It is CP949 encoded. The full CSV is processed in memory only; the saved evidence
retains only selected active permit facts, not unrelated rows or personal/employee fields.

The source explicitly documents **EPSG:5174**, not the EPSG:2097 used by older mirrors.
`inspect_seoul_source.py` transforms X/Y to WGS84 with `always_xy=True`, rounds to seven
decimals, rejects non-finite/swapped/out-of-city coordinates and flags missing, closed or
duplicate permits. These are administrative permit coordinates, not claims of exact hotel
entrance routing. The projection dependency is research-only, not added to the application.

The initial source fetch already ran; use the offline checks to avoid downloading again:

```powershell
# From apps/api; no network, import or approval performed by these checks.
uv run --with pyproj==3.7.2 python ../../docs/hotel-platforms/inspect_seoul_source.py --verify-saved
uv run --with pyproj==3.7.2 pytest tests/test_hotel_content_package.py ../../docs/hotel-platforms/test_seoul_source.py tests/test_hotel_platforms.py tests/test_hotel_direct_booking.py tests/test_travel_services.py -q
uv run python ../../docs/hotel-platforms/prepare_import.py ../../docs/hotel-platforms/seoul.pending.json
```

Calling the inspector **without** `--verify-saved` re-fetches the public CSV and prints
selected facts only, for a later deliberate review; it never writes/imports/approves.
The additional research-tool tests require the optional pyproj command above. Default API
CI also validates the package/evidence, review gates and lossless admin CSV transfer.

Remaining: Busan/Kyoto reusable coordinate and exact map sources, remaining map and platform
reviews, and all cities' rollout gates. The research total is 60, not sixty accepted hotels.
Do not use Visit Seoul's embedded Tripadvisor descriptions/ratings as government-owned data.
