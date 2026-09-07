# Hotel platform rollout — work in progress

## Implementation

The architecture milestone merged in PR #341 at `f2c3b2af431d093bfb2169fefab7deb41cc90427`
on 2026-09-07; post-merge CI 34135118181 passed. This did **not** complete the content
milestone or deploy/publish any hotel package. Follow-up research is isolated on
`codex/hotel-catalog-followup`, starting at that verified main revision.

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

## Content status — not a completed 60-hotel catalog

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
Five third-party Naver candidates remain in the evidence file only; four identities have
no candidate yet. Every new product still has `map_verified: false` for independent review.
Chrome subsequently failed to attach (Chrome debugger and in-app fallback); no browser
checks beyond that one property are claimed. No map/OTA coordinate, photo, price or review
was imported. Known restaurant-within-hotel IDs and same-brand wrong branches are excluded.

| City | Research inputs | Accepted for city rollout | Remaining |
| --- | ---: | ---: | --- |
| Tokyo | 10 | 0 | New map checks, all platform checks, background link checks, independent approvals |
| Osaka | 10 | 0 | Map and platform review, remaining OTA checks, independent approvals |
| Kyoto | 0 | 0 | 10 fully sourced hotels / 3 areas |
| Seoul | 10 | 0 | Nine Naver identities, Rakuten usable entries, live link checks, independent approvals |
| Busan | 0 | 0 | 10 hotels / 3 areas / exact Naver identity |
| Taipei | 10 | 0 | Map and platform review, remaining OTA checks, independent approvals |

Do not call this task done or enable any city using the research-input count. Production
hotel data, flags, affiliate credentials and price API permissions have not been changed by
this task. Only 24 IDs-only usage-meter increments were made (four Tokyo, ten Osaka, ten Taipei).
The one-off lookup scripts have already run: do not repeat them to recover saved IDs.

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
is merged; hotel content remains pending and no deployment was performed by this task.

Chrome spot check: the saved Tokyo Station Hotel Place ID resolves to the expected hotel
name/address and official website. This was identity-only inspection: no Google prices,
ratings, reviews, descriptions or coordinates were copied into the catalog. All pending
inputs still require independent admin approval; a single spot check does not certify a city.

## Remaining source research

Kyoto's current licensed permit list is available at
https://data.city.kyoto.lg.jp/dataset/00039/ (CC BY 4.0, July 2026 list).
It establishes licensed names/addresses, not yet ten audited hotel coordinates or platform
identities. Official pages found for Vischio Kyoto, Granvia Kyoto and Daiwa Roynet Kyoto
Terrace Hachijo are research leads only; no duplicate Hachijoguchi property should be guessed.

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

Remaining: Kyoto and Busan content, all cities' independent review and rollout gates.
Do not use Visit Seoul's embedded Tripadvisor descriptions/ratings as government-owned data.
