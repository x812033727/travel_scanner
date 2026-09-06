# Public holidays (Taiwan, Japan, Korea)

Mokaair marks public holidays on the trip calendar so a traveller can see that 5 May is a
national holiday in Japan before booking a hotel that week. The data is a copy of two
government files plus the Korean decree, kept in the repository and reviewed as a diff.

It is deliberately **not** a provider: a national calendar changes once a year and is
published months in advance, so a runtime integration would buy a key, a cache, a rate
limit and a new 503 path for a file that could simply be committed. Nothing in
`apps/api/app/holidays/` touches the network or the database when serving a request.

## Source policy

| Source | Role | Licence | Status |
| --- | --- | --- | --- |
| [DGPA 中華民國政府行政機關辦公日曆表](https://data.gov.tw/dataset/14718) | Taiwan: every named day, substitute holiday and make-up working Saturday | 政府資料開放授權條款第1版 ([terms](https://data.gov.tw/license)) — commercial use allowed, attribution mandatory | Vendored; refreshed from a manual download |
| [内閣府 syukujitsu.csv](https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv) | Japan: 国民の祝日, 振替休日 and 国民の休日 | 公共データ利用規約 第1.0版 (PDL 1.0) ([terms](https://www.digital.go.jp/resources/open_data/public_data_license_v1.0), [notice](https://www.cao.go.jp/notice/rule.html)) | Vendored; refreshed over the network |
| 관공서의 공휴일에 관한 규정 (대통령령) | Korea: written by hand from the decree's own clauses | Statutory text; no copyright, no attribution obligation | Vendored; written by hand |
| [holidays-jp](https://holidays-jp.github.io/) | Cross-check only, never at runtime | Generated from Google Calendar, so it cannot carry the 内閣府 PDL attribution | Reference |
| Nager.Date | — | "For commercial purposes we require active sponsorship" ([terms](https://nagerholidays.com/legal/termsofservice)). Mokaair earns affiliate revenue. Self-hosting needs a sponsor key too, and it has no Taiwan at all | Excluded |
| Calendarific | — | ToS §4.3(c) caps caching of its data at 30 days and §4.2(e) forbids redistribution; both of this feature's shapes break that | Excluded |
| caldays | — | Wrong data: `?year=2027` silently answers with 2026, and Taiwan is 13 rows against the official 22 | Excluded |
| Festivo | — | `/v2/holidays` is HTTP 410; the free tier forbids commercial integrations | Excluded |

The excluded four are excluded on **licence and correctness**, not on taste. This is the
same standard that ruled out Open-Meteo for weather in favour of MET Norway: a free tier
limited to non-commercial use is unusable here.

## Attribution

These strings are obligations, not decoration. Taiwan's licence says a user who does not
attribute is treated as never having been granted the licence at all, so the strings live
next to the data in `app/holidays/service.py` (`ATTRIBUTION`) and are returned by the API,
which renders them under the calendar whenever a holiday is shown.

- **TW** — 本資料使用行政院人事行政總處「中華民國政府行政機關辦公日曆表」（115年版、116年版），依政府資料開放授權條款第1版（https://data.gov.tw/license）提供，本網站另行標註假日類別。
- **JP** — 出典：内閣府ウェブサイト（https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv）、公共データ利用規約（第1.0版）（https://www.digital.go.jp/resources/open_data/public_data_license_v1.0）。振替休日と国民の休日の区別は当サイトによる加工です。
- **KR** — 「관공서의 공휴일에 관한 규정」(대통령령)과 관련 법률의 조문을 근거로 본 사이트가 직접 작성했습니다.

Both licences allow adaptation and both require saying that the work was adapted. We do
adapt: Taiwan's file has no holiday classification at all, and Japan's calls both a
振替休日 and a 国民の休日 simply `休日`.

## API contract of each source

### Taiwan — 行政院人事行政總處, via data.gov.tw

- Catalogue: `GET https://data.gov.tw/api/v2/rest/dataset/14718`. The file list is
  `result.distribution[]`, and the fields are `resourceDescription`, `resourceFormat` and
  `resourceDownloadUrl` — **not** the `resources[]`/`url` shape most catalogues use.
- The CSV lives behind an opaque GUID under `www.dgpa.gov.tw/FileConversion?...`, so the
  download URL must always be read from the catalogue and never written down.
- One entry per Republic-of-China year, plus a `_Google行事曆專用` variant we ignore. A
  reissued year appears as an extra entry (`114年…(1141020更新)`); the later entry wins.
- Columns: `西元日期,星期,是否放假,備註`, 365 rows. `是否放假` is `2` for a day off and `0`
  for a working day; an empty `備註` is a plain weekend and is not stored.
- **Sniff the encoding, never infer it from the year.** 115年 and 116年 are UTF-8 with BOM;
  114年's original file is UTF-8 BOM while its own (1141020更新) reissue is cp950. The
  refresher tries `utf-8-sig`, `utf-8`, `cp950` in that order.
- **Python cannot download this file.** `www.dgpa.gov.tw` serves an intermediate certificate
  with no Subject Key Identifier; OpenSSL 3.5 rejects the chain with
  `CERTIFICATE_VERIFY_FAILED: Missing Subject Key Identifier`, on a Windows workstation and
  **inside the production API container alike** (verified 2026-09-06). `curl` on the same
  VPS fetches it happily (`ssl_verify_result=0`), which is why this is a chain defect rather
  than a network problem. We do not relax verification. Download the CSV with `curl` and
  pass it to the refresher with `--file`.

### Japan — 内閣府

- The only working URL is `https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv`.
  `https://www.cao.go.jp/syukujitsu.csv`, widely quoted, is a 404 HTML page — adding it as a
  fallback would only fire once the real source had already broken.
- Shift_JIS, CRLF, header `国民の祝日・休日月日,国民の祝日・休日名称`, dates unpadded
  (`2026/5/6`), about 1,067 rows covering 1955 onwards.
- Two rows a year are named only `休日`. A `休日` with a holiday on both sides is a
  国民の休日; otherwise it is the 振替休日 of the nearest preceding Sunday holiday, and we
  name it after that holiday. 2026 has one of each — 05-06 and 09-22 — and they are exactly
  the two days most general-purpose holiday APIs drop.

### Korea — 관공서의 공휴일에 관한 규정

Written by hand; every row carries a `note` naming the clause it comes from.

- 제3조제1항: a 국경일 (삼일절, 광복절, 개천절, 한글날) or 부처님오신날, 어린이날,
  기독탄신일, 노동절, 제헌절 falling on **Saturday or Sunday** gets a 대체공휴일.
- 제3조제2항: 설날 and 추석 연휴 get one **only when they overlap a Sunday**.
- 현충일 (제7호), 1월 1일 (제3호) and the election day (제10호) are in neither list.
- Consequence worth stating plainly: **추석 2026 (Thu 24 – Sat 26 September) has no
  대체공휴일.** Sources that claim a 2026-09-28 holiday are wrong, and acting on them would
  invent a day off in the most expensive travel week of the Korean year. 현충일 2026-06-06,
  a Saturday, likewise gets nothing.
- 2026 includes 2026-06-03, the 9th nationwide local election day (제2조제10호), and the
  two days newly made public holidays: 노동절 (법률 제21543호) and 제헌절 (법률 제21338호).
- Korea's 설날 is one day later than Taiwan's 春節 in 2027 (02-07 against 02-06). Both
  calendars are right for their own country; do not "fix" one against the other.

KASI (한국천문연구원 특일 정보 on data.go.kr) is deliberately out of scope. Its licence is
open and free, but no first-hand source confirms the operation name a client would call —
`getAnniversaryInfo` answers 401 without a key while `getNationalHolidayInfo` answers 400
`NO_OPENAPI_SERVICE_ERROR` — and `apis.data.go.kr` throttles at the TLS layer: after a dozen
probes the source IP stops completing handshakes, with no status code to branch on. A naive
retry loop would black-hole the VPS's address silently.

## Refresh cadence and look-ahead

```bash
cd apps/api
# Japan, straight from the Cabinet Office
uv run python -m app.cli refresh-holidays --country jp --year 2027
# Taiwan, from a copy downloaded with curl (see the TLS note above)
curl -sS -o /tmp/tw2027.csv "$(the resourceDownloadUrl from the catalogue)"
uv run python -m app.cli refresh-holidays --country tw --year 2027 --file /tmp/tw2027.csv
```

Both print a diff and write nothing. `--apply` writes the dates back and carries every
hand-written `names` block across; a key with no translation yet is refused rather than
written with a blank name. Korea is refused outright: it has no machine-readable source.

Run it when a government publishes a new year, and once more each autumn to catch amendments
— Taiwan reissued its 114年 calendar on 2025-10-20 and turned three working days into
holidays, so a one-shot import would have shown 2025-12-25 as a working day all year.

Look-ahead limits, which are hard dates and not opinions:

- **Japan is the binding one.** 内閣府 publishes the following year in February
  (`gaiyou.html`: 令和10年の国民の祝日は令和9年2月に掲載します), and the current file ends at
  2027-11-23. From December 2026 a twelve-month flight window reaches past it.
- Taiwan's dataset already covers through 2027-12-31; the 117年 calendar is normally
  announced in the first half of 2026-2027.
- Korea's 월력요항 for a year is announced in June of the previous year.
- Anything beyond 2027 is unpublished. Japan's equinox holidays are astronomical and are
  only fixed when the government announces them, so do not extrapolate them.

## Shape of the data

`apps/api/app/holidays/data/{tw,jp,kr}_{2026,2027}.json`, one array per country-year:

```json
{
  "date": "2026-05-06",
  "key": "jp_constitution_memorial_day_substitute",
  "kind": "substitute",
  "is_working_day": false,
  "names": { "zh-TW": "憲法紀念日補假", "zh-CN": "…", "en": "…", "ja": "憲法記念日 振替休日", "ko": "…" },
  "source": "cao_go_jp"
}
```

`kind` is one of `public_holiday`, `substitute`, `bridge_holiday`, `makeup_workday`. No
source gives names in five languages — DGPA is zh-TW only, 内閣府 ja only — so `names` is
written by hand, the same way `app/weather/met_norway.py` names its weather families.

**`makeup_workday` is forward-looking, not historical.** 《紀念日及節日實施條例》第8條 still
lets an agency move a working day, and 114年 had one (`20250208,六,0,補行上班`). 2026 and
2027 happen to have none. Treating the kind as dead data would draw the first make-up
Saturday as free — and knowing that a Saturday is a working day in Taiwan is most of what
the Taiwanese calendar is for.

Long weekends are `{weekend ∪ holidays} − {make-up days}`. Adding a holiday count to a
weekend count double-counts every holiday that already falls on one, which in Korea 2026 is
삼일절, 부처님오신날 and three more.

## What this feature deliberately does not do

- No crowd or price **forecast**. The flexible-date chips already show real quotes, which
  contain the holiday premium; a badge that says "5/4 みどりの日" is a fact, one that says
  "this will be expensive" is a second, arguing voice.
- No review queue. This is not per-place data; a pull-request diff is the review.
- No admin panel, no provider row, no migration, no API key.
- Downstream consumers — opening-hours-aware scheduling, the day-health strip, flexible
  flight dates, alerts — are separate tasks. The one worth doing next is opening hours:
  a Japanese museum that closes on Mondays **opens** on a holiday Monday and closes the
  Tuesday instead, so any Monday rule written without this data is wrong.
