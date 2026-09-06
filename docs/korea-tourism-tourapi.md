# TourAPI (Korea Tourism Organization) feasibility

TourAPI is the Korea Tourism Organization's open data service for Korean attractions,
restaurants, festivals and accommodation. This document records whether Mokaair can use it.

**Current answer: no, and the blocker is not the one anyone expected.** Our servers cannot
reach the API gateway at all. That was measured, not assumed, and it is measured below in
enough detail that nobody has to repeat the work. Everything else about TourAPI checks out.

Status as of 2026-09-06:

| Gate | Question | Answer |
| --- | --- | --- |
| A. Account | Can a non-Korean applicant get a data.go.kr service key? | **Unanswered.** Needs the owner. |
| B. Connectivity | Does `apis.data.go.kr` answer from our production egress? | **No.** 0 successes, 2 vantage points. |
| C. Corpus | How many Seoul and Busan rows are there really? | **Cannot measure.** Needs a key from gate A. |

Gate B fails independently of gate A. Obtaining a key would not, by itself, make TourAPI
usable from the current infrastructure.

## Gate B: the gateway does not answer us

Measured 2026-09-06 with [`tools/probe_tourapi.py`](../tools/probe_tourapi.py) and with
plain sockets, from two vantage points on different networks in different countries.

**Production VPS, egress `187.127.118.6`:**

| Target | Port | TCP handshake | After the handshake |
| --- | --- | --- | --- |
| `apis.data.go.kr` `27.101.236.63` | 443 | completes, 0.13 s | TLS handshake never completes, 10 s timeout |
| `apis.data.go.kr` `27.101.236.63` | 80 | completes, 0.13 s | plain `GET /` returns zero bytes, 10 s timeout |
| `www.data.go.kr` `27.101.236.55` | 443 | completes, 0.12 s | TLS completes 0.20 s, HTTP 200 |

Repeated HTTP attempts against the gateway from the same machine: 0 successes out of 5 at a
15-second budget, plus single attempts at 20, 25 and 30 seconds. None returned a byte.

**Developer machine, unrelated network:** 0 successes out of 10, every one of them
`_ssl.c:1015: The handshake operation timed out` — the same signature.

**Everything else in the same subnet answers instantly from the failing machine**, measured
in the same second: `www.data.go.kr` 200, `auth.data.go.kr` 302, `openapi.data.go.kr` 301,
`api.visitkorea.or.kr` 200, `knto.or.kr` 302. So this is not Korea being unreachable, not
data.go.kr being down, and not DNS: `getent` resolves the gateway in about 1 ms and there is
no AAAA record. `api.data.go.kr` is the same host and behaves identically.

Reproduce it:

```bash
python tools/probe_tourapi.py --service KorService2 --repeat 20
```

No service key is needed for this. A request rejected as a bad key still proves it crossed
the network, and that is what is being measured. A run that reports `reached 0/20` means the
situation has not changed.

### What the signature means

Accepting the TCP handshake and then answering nothing, on both ports, is not what a firewall
that blocks you looks like — a blocked port refuses or drops the SYN. Accept-then-silence is
what a source-address filter in front of the application looks like.

That fits one documented fact: data.go.kr defines error code `32 UNREGISTERED_IP_ERROR`, so
the platform does gate on caller IP. **The hypothesis worth testing first is that our address
simply is not registered, and that registering it is what unblocks this.** Registering an IP
requires an account, which is gate A.

This is a hypothesis, not a finding. It has not been tested because testing it needs an
account. Do not write it down anywhere as the cause.

### What to do before writing any TourAPI code

1. Clear gate A and get a key.
2. Register the production egress address with data.go.kr.
3. Re-run the probe from the production VPS. If it still reports `reached 0/N`, TourAPI is
   not usable from this infrastructure and the only remaining options are a Korean egress
   (a relay or proxy inside Korea) or dropping the source. Decide that before building.

## Gate A: nobody has confirmed a non-Korean applicant can get a key

Not attempted. Creating an account is the owner's action, not something to automate: the
data.go.kr signup at `https://auth.data.go.kr/sso/common-signup` offers 일반회원 (내국인,
Korean nationals), 어린이 회원 (내국인) and 기업회원 (a business registered with the Korean
tax office), and step 4 is 본인인증, Korean identity verification. `?lang=en` does not change
the form, and the English portal has no signup entry at all.

The counter-evidence is that the gov.kr service page for TourAPI (B55101100003) lists
신청자격 as 개인 및 민간, 공공 등 with no documents required. That describes eligibility for
the service, not for the portal account that issues keys. The two are not the same thing.

Two questions for the owner, both blocking:

1. **How far along is the NAVER key?** If it is close, this whole source loses most of its
   value: the existing pipeline can already publish 88 Korean seeds, 65 pending attractions
   and 67 Korean merchants once NAVER place URLs exist. See
   [`tasks/open/2026-09-06-naver-maps-key.md`](../tasks/open/2026-09-06-naver-maps-key.md).
2. **Would a KTO `contentid` be accepted as an exact map identity for Korea?** Today
   `has_exact_map_identity()` accepts only a precise NAVER place URL for `country_code == 'KR'`,
   and an attraction with no exact identity is never published and never reaches the planner.
   TourAPI supplies coordinates and prose, not NAVER identifiers, so a content-only
   integration changes nothing a user can see and only lengthens the review queue. If the
   answer is no, TourAPI is worth only its coordinates and its Chinese prose, and this
   document should say so.

Contact for gate A, if the owner wants it pursued: `tourapi@knto.or.kr`, phone
070-4287-3219, cc `opendata_help@nia.or.kr`. Ask two things — whether non-residents can hold
a TourAPI key, and whether the 1,000-call ceiling is per API or per account.

A fallback worth applying for in parallel is the Visit Seoul API
(`https://api.visitseoul.net/apiinfo/apiovr/view/3?lang=en`), whose key page states no
nationality or Korean-entity requirement. It registers a calling URL and only permits calls
from it, and whether a server-side BFF call qualifies is unknown. Its quota is entirely
unpublished, which is weaker than TourAPI's explicit 1,000, not stronger.

## Gate C: not measurable without a key

The commands are ready and will work the moment gates A and B clear:

```bash
python tools/probe_tourapi.py --service KorService2 --ldong 11 --count-only   # Seoul
python tools/probe_tourapi.py --service KorService2 --ldong 26 --count-only   # Busan
python tools/probe_tourapi.py --service KorService2 --count-only              # control
python tools/probe_tourapi.py --service ChtService2 --ldong 11 --count-only
python tools/probe_tourapi.py --service ChtService2 --ldong 26 --count-only
python tools/probe_tourapi.py --service ChtService2 --count-only
```

The first two numbers must be clearly smaller than the control. If all three match, the
region filter did not apply and the numbers are worthless — see `lDongRegnCd` below.

For order of magnitude only, KNTO's own portal index reports Seoul 8,011 and Busan 2,227 for
Korean, and roughly 4,600 and 1,074 for Traditional Chinese. That endpoint has no contract.
Never quote those as API guarantees.

## Verified API facts

These were confirmed by three independent adversarial checks. They are recorded so nobody
re-derives them, and every one of them is a trap that fails silently if you get it wrong.

### Endpoints

Every current path ends in `2`. Any tutorial citing `KorService1`, `areaBasedList1` or
`detailCommon1` describes a retired generation.

- Korean: `https://apis.data.go.kr/B551011/KorService2` (dataset `15101578`)
- Traditional Chinese: `https://apis.data.go.kr/B551011/ChtService2` (dataset `15101769`)

Operations: `areaBasedList2`, `locationBasedList2`, `searchKeyword2`, `searchFestival2`,
`detailCommon2` (carries the long `overview`), `detailIntro2` (hours and menus, schema varies
by type), `detailImage2`, `areaBasedSyncList2` (incremental, with a `showflag` tombstone and
`oldContentid`).

The official multilingual specification is itself wrong: it tells you to use
`https://apis.data.go.kr/B551011/JpnService/~~`, without the `2`. Copying it gives a dead path.

### Authentication

`serviceKey` goes in the query string, URL-encoded. Not a header, not OAuth. `MobileOS` and
`MobileApp` are both mandatory; omitting either returns code `11`. Legal `MobileOS` values are
`IOS`, `AND`, `WIN`, `ETC` — it is `WIN`, not `WEB`. The default response is XML; `_type=json`
is required for JSON.

data.go.kr issues the same key twice, once URL-encoded and once not. Encoding an
already-encoded key turns `%2B` into `%252B` and earns a code 30 that reads exactly like a
wrong key. `tools/probe_tourapi.py --key-is-encoded` covers that case.

### Languages are separate products

Nine languages (KOR, ENG, JPN, CHS, CHT, GER, FRE, SPN, RUS) are nine datasets, each needing
its own 활용신청 and each with its own quota bucket. **One key does not open two languages.**

### `contentTypeId` differs between Korean and multilingual

The most common integration error, and it does not raise — it just returns empty.

| Type | Korean | Multilingual, including CHT |
| --- | --- | --- |
| 관광지 attractions | 12 | 76 |
| 문화시설 cultural facilities | 14 | 78 |
| 축제·공연·행사 events | 15 | 85 |
| 레포츠 leisure sports | 28 | 75 |
| 숙박 accommodation | 32 | 80 |
| 쇼핑 shopping | 38 | 79 |
| 음식점 restaurants | 39 | 82 |

### `areaCode`, `sigunguCode` and `cat1..cat3` are dead

data.go.kr marks them 미사용항목(삭제예정). They are optional, so sending them raises no error
— they are ignored, and you get the nationwide `totalCount` back looking entirely normal. The
live parameters are `lDongRegnCd` (Seoul `11`, Busan `26`) and `lDongSignguCd`, with
`lclsSystm1/2/3` for categories.

Legal dong codes were rewritten wholesale on 2026-07-01 (Incheon gained a district;
광주 and 전라남도 merged into code 12) and the entire corpus had its `modifiedtime` pushed to
26-06-30 in one batch. Any incremental mirror keyed on `modifiedtime` must survive the whole
corpus going dirty overnight.

### Coordinates are the strongest technical argument

Lists and details both carry `mapx` (WGS84 longitude) and `mapy` (WGS84 latitude). Measured
coverage: Korean 49,720/49,772 (99.90%), Traditional Chinese 14,472/14,472 (100%).
`coordinate_source_type='official_tourism'` is already in `DURABLE_COORDINATE_SOURCES`
(`apps/api/app/locations/coordinates.py`), so TourAPI coordinates could be stored durably and
legitimately. `apps/api/app/places/naver.py` has a `_coordinate()` and an `_in_korea()` that
would be reused as they are.

### The Traditional Chinese corpus is smaller than it looks

14,472 rows, of which 10,797 (74.6%) are `[事後免稅店]` tax-refund shops. Excluding shopping
leaves roughly 500 usable Seoul rows and 167 Busan rows (attractions plus cultural: Seoul 355,
Busan 121). Restaurants are the weak spot: **CHT has 70 in Seoul and 13 in Busan**, against
Korean's 1,604 and 520. So "Traditional Chinese exists, therefore no translation needed" is
false — dining would have to be machine-translated regardless. CHT `overview` quality is good
(99.56% populated, median around 213 characters for Seoul attractions) but there is little of it.

`contentid` does not cross languages. Not one of the 14,472 CHT ids appears among the 49,772
Korean ids. Gyeongbokgung is `126508`/`12` in Korean and `332517`/`76` in Chinese, with
bit-identical coordinates. The only join is the Korean text in parentheses in CHT titles
(`景福宮(경복궁)`), which hits about 91% corpus-wide but only 68.5% for Seoul and 74.4% for
Busan once narrowed to attractions and cultural facilities. Coordinates alone are not a key
either: Korean has 7,474 groups of exactly duplicated coordinates.

## Licensing

Both datasets are free with 이용허락범위 제한 없음, but the descriptions carve images out into
KOGL (공공누리): "공공누리 1유형, 3유형 이미지 제공됨". Never quote the "no restrictions" line
without that caveat next to it.

- **Type 1**: attribution, commercial use, **derivative works allowed**.
- **Type 3**: attribution, commercial use, **no modification and no derivative works**.

Type 3's 변경금지 is defined by the Ministry of Culture and the Korea Copyright Commission to
include 형식의 변경, format changes, word for word. **That makes `next/image` optimisation, CDN
transforms, self-generated thumbnails and cropping to a card ratio a breach for Type 3 images**,
and TourAPI's terms article 11 lets KNTO suspend supply over it. If images are ever used, serve
KNTO's own `firstimage2` / `smallimageurl` and disable optimisation on that path.

`cpyrhtDivCd` must be stored per row and per image, and an unrecognised value must be
**refused, not displayed by default** — KNTO's code table also has Type 2, Type 4 (no
commercial use) and Type 5 (공사만사용).

Attribution is mandatory for every type, including Type 1 (knto.or.kr/helpdeskCopyrightguide,
verbatim: "제 1유형을 포함하여 어느 유형이든 출처…는 반드시 표시하여야"). It must carry the
publication year, the agency name, the agency URL `kto.visitkorea.or.kr`, and the author where
credited, with a link for online use. Two further prohibitions: nothing that damages a depicted
person's reputation or personality rights, and no use as corporate CI/BI. KOGL Type 1 also
forbids implying any special relationship with or endorsement by the agency.

**The recommendation is to exclude images from any first version.** No attraction or merchant
image column exists in the schema today (the only image field anywhere is
`trip_plans.cover_image_url`), so no card would render a photo. Adding them means a migration,
a five-locale card redesign and a Type 3 review.

## Quota: treat 1,000 as a permanent ceiling

Both datasets state 개발단계 자동승인 with 1,000 calls, and 운영단계 심의승인 with an increase
available on registering a use case. But the English "Application for Use" panel on both
datasets reads "Development level : allowed / Operation level : **Not allowed**". That is not a
portal default: the KMA short-term forecast dataset (15084084) reads "Operation level : allowed"
with a 10,000 development account, so it is set per dataset and TourAPI's production tier is
switched off. Any plan needing production traffic rests on an unresolved contradiction, and
`tourapi@knto.or.kr` should confirm it in writing.

Everything must therefore work under 1,000 calls. A full backfill does not: Seoul plus Busan in
Korean is about 10,238 list rows, and three detail calls each is roughly 30,700 requests, a
month of cold start. Only a few hundred rows plus a nightly `areaBasedSyncList2` diff fits.

A per-second limit exists but is unpublished for these two datasets, so throttle client-side
regardless.

Error codes: `03` no data, `11` missing mandatory parameter, `22` quota exhausted, `30` key not
registered, `31` expired, `32` IP not registered.

## Still unverified

- Whether a non-Korean can register on data.go.kr at all. Gate A.
- Whether production traffic is genuinely closed for these two datasets.
- Whether the 1,000 ceiling is per API or per account. If per account, KorService2 and
  ChtService2 share one bucket.
- The real cause of the gate B blackhole. The IP-allowlist hypothesis above is untested.
- The text of TourAPI terms articles 11, 12 and 13. `api.visitkorea.or.kr` is a
  client-rendered app and `#/agrAgreement` yields no text to a fetch. The summary circulating
  in our notes (mandatory attribution, suspension for breach, no continuity guarantee, Korean
  courts) is probably right but has not been read at the source.
- Whether the Visit Seoul API is actually open. Its homepage still carries an "Expected
  opening: End of October 2025" notice while its key page reads as live. Its published category
  counts are seven-language totals; the zh-TW split is unknown, so they cannot be compared
  like-for-like against TourAPI's 70 Traditional Chinese Seoul restaurants.
- The real Type 1 / Type 3 split. `cpyrhtDivCd` is not in the portal index; only
  `detailImage2` with a key would show it.

## Things already settled — do not re-argue them

- Do not quote 약 26만 건 (Korean) or 약 8만 건 (Chinese) as POI counts. Both are marketing
  figures counting rows across all operations, and 8만 appears verbatim on the English,
  Japanese and Traditional Chinese dataset pages alike. The measured distinct POI counts are
  49,772 and 14,472.
- Do not use `areaCode=1` / `areaCode=6` for Seoul and Busan. See above.
- Do not treat `api.visitkorea.or.kr/hub/*.do` as a contract. Every coverage percentage in
  this document comes from that undocumented portal index (80.9 MB for Korean, 18.2 MB for
  Chinese, with `areaCd` empty on 58% and 81% of rows respectively, city distribution inferred
  from the `addr1` prefix). Order of magnitude only.
- Do not key anything on a CHT `contentid`, and do not join on coordinates alone.
- Do not claim TourAPI solves opening-hours scheduling. `detailIntro2`'s `usetime` and
  `restdate` are free prose, and
  [`tasks/open/2026-09-06-opening-hours-aware-scheduling.md`](../tasks/open/2026-09-06-opening-hours-aware-scheduling.md)
  explicitly forbids guessing hours from prose.
- Do not touch the ranking formula. TourAPI is not a fifth scoring input.
- Do not touch `apps/api/app/hotspots/discovery.py` while `ALLOWED_TYPES` is being measured
  under `2026-09-06-measure-the-flood-before-widening-allowed`.

## If all three gates clear

Open an implementation task with this scope, checked against every currently open task for
conflicts:

```
apps/api/app/korea_tourism/        # new package: client.py, import_hotspots.py, cli.py
apps/api/app/config.py
apps/api/app/admin/service.py
apps/api/app/cli.py
apps/api/tests/test_korea_tourism.py
apps/web/components/admin-settings-panel.tsx
```

Landing points are already located. `PROVIDER_DEFINITIONS` is in `apps/api/app/admin/service.py`
with the `odsay` entry as the closest template; `OFFICIAL_PROVIDER_HOSTS` in
`apps/api/app/config.py` would need `apis.data.go.kr`; `providerCategoryOf` in
`apps/web/components/admin-settings-panel.tsx` silently drops unknown providers into "other",
and the right category is `content`. Use literal `label:` strings in `fieldMeta` and
`secretLabels` rather than `localized: true`, so no `apps/web/messages/*/admin.json` change is
needed and nothing collides with the admin i18n task.

No migration is needed for a first stage. `TravelHotspot` already has `coordinate_source_type`,
`coordinate_source_url`, `origin`, `review_status` and `metadata_json` (which is `JSON`, not
`jsonb`, so `?`, `@>`, `<@` and `||` are unavailable), and `FoodMerchantSource.source_type`
already permits `official_tourism`. Put `contentid` in `metadata_json` and deduplicate in
Python. The governance template to copy is the docstring at the top of
`apps/api/app/foods/trend_import.py`: import as `review_status='pending'`, `is_active=False`,
`map_match_status='unverified'`. Cap the import size. The last review backlog was 482 rows and
cost a full P2 task and an entire session to clear.
