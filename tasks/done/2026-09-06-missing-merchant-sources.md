---
id: 2026-09-06-missing-merchant-sources
title: Most merchants have no first-party page, so nothing can locate them
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T06:33:38Z
created_at: 2026-09-06T00:52:13Z
completed_at: 2026-09-06T07:53:23Z
branch: claude/merchant-sources
depends_on: []
scope:
  - apps/api/app/foods/merchant_catalog.py
---

# Most merchants have no first-party page, so nothing can locate them

## Why

Every seeded merchant carries a `destination_context` source — a city food guide. 272
merchants share about 23 of those, so such a page says a city has food, not where one
restaurant stands. Only a `merchant_website` (the shop's own site) or a `merchant_listing`
(a tourism board's page about that one merchant) is evidence about a specific place.

On 2026-09-05, 63 of 172 merchants had one. The coordinate fill reported `no_source` for the
other **109**, meaning it had nothing to even open. More merchants have been added since, so
the gap is now larger.

This is the upstream cause of `2026-09-06-merchant-coordinate-backlog`: a merchant
with no page of its own has no route to a durable coordinate except a human typing one.

## Definition of done

- [x] Every merchant that can have a first-party page has one, or is explicitly recorded as
      having none available.
- [x] `fill-food-merchant-coordinates` reports `no_source` for only the merchants where that
      is genuinely true.
- [x] `tests/test_food_catalog.py` counts updated to match.

## Steps

- [x] List the merchants with no usable source. `merchant_page_sources()` in
      `app/foods/coordinate_fill.py` is the exact rule: scope in (merchant_website,
      merchant_listing), `source_type` in `DURABLE_COORDINATE_SOURCES`, https.
- [x] Work country by country. Government tourism sites with per-merchant pages already used
      here and known to work: `okinawastory.jp/gourmet/<id>` (OCVB),
      `trip-kamakura.com/stay-gurume/detail.php?id=<id>`, `kanagawa-kankou.or.jp/spot/<id>`,
      `travel.taipei/en/shop/details/<id>`, `english.visitseoul.net`, `khh.travel`.
- [x] Fetch and read every page before citing it. Confirm three things: the page is about
      that merchant, the merchant is still operating, and the page mentions the dish the
      merchant is mapped to. #169 did this for 16 Japanese merchants and rejected several
      candidates on exactly those grounds.
- [x] Use `_merchant_website` when the URL is the shop's own site (it also sets
      `official_website_url`) and `_official_listing` for a tourism page.
- [x] Update the country balance and total assertions in
      `test_direct_sources_are_verified_and_country_balanced`.

## How to verify

```bash
docker compose -f docker-compose.prod.yml exec -T api \
  python -m app.cli fill-food-merchant-coordinates --limit 40 | head -c 400
```

`no_source` should fall by the number of merchants given a page.

## Notes

Adding a page does not by itself produce a coordinate: of the 63 merchants that already had
one, 62 published nothing machine-readable, so expect the direct yield to be near zero. The
value is that a reviewer can open one page per merchant instead of searching, and that the
merchant becomes eligible for the coordinate review queue. Read the Notes of
`2026-09-06-merchant-coordinate-backlog` before assuming otherwise.

Japan had no entries in `MERCHANT_DIRECT_SOURCE_SEEDS` at all until #169 — a test asserted
that (`merchant_country[...] != "JP"`). That assertion is gone; the 16 Japanese entries added
there are the pattern to follow.

Scope overlaps `2026-09-06-broken-merchant-citations`: both edit
`apps/api/app/foods/merchant_catalog.py`. Doing both in one branch is reasonable.

2026-09-06 claude-fable-5-1：110 家沒有第一方頁面的店全部查過一遍，補上 **51 家**（JP 28、KR 13、
TH 5、TW 2、HK 1、VN 2），`MERCHANT_DIRECT_SOURCE_SEEDS` 63 → 113（其中店家自己的站 50）。剩下
60 家逐家的理由寫在常數上方的註解裡，分四類：只有 Facebook／彙整站、官網憑證失效或擋機器人、
官網只剩 JavaScript 殼、seed 本身指不到一家店。

- 每一頁都讀過三件事（是這家、還在營業、提到對應菜色）。有幾頁只寫到前兩件，備註留在 seed 標題
  或註解：すみれ本店（札幌觀光協會頁只標「ラーメン」）、Muslim Restaurant 與 Kiat Ocha（TAT 頁
  只有地區與菜系）、富鼎旺（頁面寫的是豬腳）。
- 型態：店家自己的頁走 `_merchant_website`（含 Gurunavi 代管的官方頁 fb33500.gorp.jp），觀光局、
  市府、市場或商店街協會關於這一家店的頁走 `_official_listing`。食べログ、ぐるなび、HotPepper、
  Retty 一律不收，測試釘住。
- 11 家要人看 seed 本身：あんず金沢（該品牌只在福岡與東京）、炙屋十兵衛（二日町本店 2023-03
  收，只剩車站店）、王功蚵仔煎（王功在彰化）、一中臭豆腐（一中街有兩攤）、Hea Owan 清邁店
  （只有 Silom 一攤）、Wrap & Roll 海巴征店（已不在官網名單）、西羅殿（牛肉湯店卻對到臭豆腐）、
  Gogung 大邱、팔공삼겹살、王記割包、老周／老江。
- 正式機 `fill-food-merchant-coordinates` 在部署後跑，`no_source` 的變化補在下方。
