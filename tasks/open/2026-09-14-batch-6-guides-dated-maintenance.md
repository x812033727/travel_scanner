---
id: 2026-09-14-batch-6-guides-dated-maintenance
title: "Batch 6 guides: dated edits after launch (removals, re-checks, expiring notices)"
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-14T10:30:00Z
completed_at:
branch:
depends_on:
  - 2026-09-14-launch-articles-batch-6-twenty-more
scope:
  - apps/api/app/guides/content/taiwan-long-weekends-2027-flight-planning.json
  - apps/api/app/guides/content/power-bank-flight-rules-2026.json
  - apps/api/app/guides/content/japan-cherry-blossom-2027.json
  - apps/api/app/guides/content/hong-kong-4-day-itinerary.json
  - apps/api/app/guides/content/return-to-taiwan-customs-duty-free-guide.json
  - apps/api/app/guides/content/hong-kong-airport-to-city.json
  - apps/api/app/guides/content/singapore-4-day-itinerary.json
  - apps/api/app/guides/content/yokohama-day-trip-from-tokyo.json
  - apps/api/app/guides/content/singapore-entry-2026-sg-arrival-card.json
  - apps/api/app/guides/content/singapore-changi-airport-mrt-simplygo-guide.json
  - apps/api/app/guides/content/dmz-day-trip-from-seoul.json
  - apps/api/app/guides/content/suwon-hwaseong-day-trip.json
  - apps/api/app/guides/content/hong-kong-entry-2026.json
  - apps/api/app/guides/content/hanoi-4-day-itinerary.json
  - apps/api/app/guides/content/taoyuan-airport-departure-guide.json
  - apps/api/app/guides/content/phuket-airport-transport-where-to-stay.json
  - apps/api/app/guides/content/vietnam-money-sim-grab-guide.json
  - apps/api/app/guides/content/ho-chi-minh-city-4-day-itinerary.json
  - apps/api/app/guides/content/korea-naver-map-kakao-t-guide.json
  - apps/api/app/guides/content/kanazawa-2-day-itinerary.json
  - apps/web/public/guides/hanoi-4-day-itinerary/diagram-1.svg
  - apps/web/public/guides/phuket-airport-transport-where-to-stay/diagram-1.svg
  - apps/web/public/guides/ho-chi-minh-city-4-day-itinerary/diagram-1.svg
---

# Batch 6 guides: dated edits after launch (removals, re-checks, expiring notices)

## Why

The twenty batch-6 articles (launched 2026-09-14) contain things that go stale on known dates:
- a table of 2026 long weekends
- links to notices that expire before the linking article does
- temporary closures
- exhibition prices
- winter timetables not published yet
- laws still in the legislature

The writers and fact-checkers wrote every one down. This task collects them in date order, so
nobody has to rediscover them from the specs.

Block numbers refer to `locales.zh-TW.blocks` in the pack as launched. Re-find a block by its
quoted text if earlier edits have moved it. After any edit:
- re-run `uv run pytest tests/test_guides_content_pack.py -q`
- import on the host with `guides-import --dry-run`, then `--publish`

## Definition of done

- [ ] Every item below whose date has passed is done, or re-dated with a reason.
- [ ] Diagrams whose numbers change are redrawn, and every number on them still appears in the text.
- [ ] `sources` entries that no longer support anything are removed; changed ones get a new `checked_on`.
- [ ] When every dated item is done or moved to a successor task, close this task.

## Steps

### 2026

- [ ] **2026-10-12** `taiwan-long-weekends-2027-flight-planning`
  - Delete the 國慶日 row from the 2026 table (block 2) and the matching source title
    wording.
  - **2026-10-27:** delete the 光復節 row. The H2 「2026 年底：還有三個連假」 count follows.
- [ ] **2026-10-01, then every two weeks** `singapore-changi-airport-mrt-simplygo-guide`
  - Check the PTC Newsroom for the 2026 fare review.
  - When it is published, rewrite the block-27 callout 「2026 年 9 月查證時還沒公告」 with the
    announcement and effective dates.
  - On the effective date, update the fares in blocks 16, 24, 25 and 31.
- [ ] **2026-10-01** `yokohama-day-trip-from-tokyo`
  - Read the YOKOHAMA AIR CABIN October calendar.
  - Update the September hours in blocks 15, 25 and 28.
- [ ] **2026-10-10** `dmz-day-trip-from-seoul`
  - In the block-21 callout, delete closure dates that have passed.
  - After 12-25, the title 「2026 年 10 月到 2027 年 2 月的休館日」 follows.
- [ ] **2026-10-04 and 2026-10-14** `suwon-hwaseong-day-trip`
  - In the block-22 callout, delete lines as their dates pass: the shortened Eocha route to
    10-03, the Eocha suspension 10-04 to 10-11, the archery range closure 09-30 to 10-13, and
    the cultural festival.
  - The title becomes 「2026 年秋季：行宮夜間跆拳道公演」.
- [ ] **2026-10-19** `kanazawa-2-day-itinerary`
  - Block 34 gives the 21st Century Museum price as 「收藏展到 10 月 18 日為 450 日圓」.
    Rewrite it for the next exhibition, or as 「票價依展覽，以官網為準」.
- [ ] **2026-11-01** `kanazawa-2-day-itinerary`
  - Winter timetable for Komatsu–Taipei in block 12, and the times in the block-17 callout
    (10:25 arrival, 11:45 return).
- [ ] **2026-11-01** `taoyuan-airport-departure-guide`
  - Airport MRT timetable, currently published only to 115/10/31.
  - Re-check 「A1 往機場的直達車首班 05:30」 in block 12.
- [ ] **2026-11-02** `suwon-hwaseong-day-trip`
  - Delete the block-22 callout.
  - Block-9 table: 「2026 年為 5 月 1 日到 11 月 1 日…」 becomes 「下一年度期間以官網公告為準」.
- [ ] **2026-11-03** `hanoi-4-day-itinerary`
  - Rewrite the block-17 callout 「2026 年 9 月 4 日到 11 月 2 日，胡志明陵整修暫停瞻仰」 as
    a general 「定期整修，以官方公告為準」.
  - Delete the renovation-notice source.
- [ ] **2026-11** `singapore-4-day-itinerary`
  - Christmas Wonderland season: does the Supertree Grove charge, and does Garden Rhapsody
    change? Garden Rhapsody times are on the diagram.
- [ ] **2026-12-01** `singapore-4-day-itinerary`
  - When Borealis ends, delete its sentence in block 18.
  - When Jurassic World: The Experience ends, delete its sentence in block 15.
  - Check both again on 2027-03-01.
- [ ] **2026-12, then quarterly** `dmz-day-trip-from-seoul`
  - Ministry of Unification JSA page and the Paju monorail notice.
  - If foreigners are accepted again, update blocks 33–34 and the diagram's JSA column.
- [ ] **2026-12-15 to 2027-01-10** `power-bank-flight-rules-2026`
  - Re-check ICAO 2027–28, CAA Taiwan, korea.kr and MLIT.
  - If nothing changed, extend `valid_until` past 2027-01-31.

### 2027

- [ ] **2027-01** `hanoi-4-day-itinerary`
  - Yearly price check: Trang An 300,000; bus 86/17/07; Temple of Literature 70,000; Hoa Lo 50,000.
  - The last four are on the diagram.
- [ ] **2027-01-05** `singapore-changi-airport-mrt-simplygo-guide`
  - Re-read Adult Fares, align the block-27 callout, and close the fare-review watch.
- [ ] **2027-01-10** `taiwan-long-weekends-2027-flight-planning`
  - Delete blocks 1–3: the 2026 H2, the 2026 table, and the link to the year-end notice.
  - Block 0 「下面兩張表列出 2026 年底和 2027 年的連假」 describes 2027 only.
  - Description: drop 「另附 2026 年底剩下的連假」.
  - Delete the sources for the 115 calendar (pid=12573) and 「2026년 월력요항」.
- [ ] **2027-01-15** `taoyuan-airport-departure-guide`
  - Re-check the power-bank rule in the block-20 callout.
  - If it changed, update the diagram's security box too.
- [ ] **2027-01 (mid)** `hong-kong-entry-2026`
  - Re-check pre-arrival registration, the visitor e-Channel list, the tobacco office and BOCA
    Macau days.
- [ ] **2027-01-16** `phuket-airport-transport-where-to-stay`
  - Re-check the Smart Bus timetable, payment and pass pages.
  - Resolve the Route 2 terminal: official pages say both Terminal 1 and 2.
  - The diagram carries the times and fares.
- [ ] **2027-02 (first forecast)** `japan-cherry-blossom-2027`
  - Add the 2027 forecast section.
  - Rewrite the 「預測還沒出來」 sentences in block 0, the description and blocks 7, 36–37.
- [ ] **2027-02-10** `dmz-day-trip-from-seoul`
  - Replace the block-21 callout with the 2027 closure dates: 5/5 어린이날, 5/13
    부처님오신날 (check against the 2027 월력요항), 9/15 추석.
- [ ] **2027-02-16** `taiwan-long-weekends-2027-flight-planning`
  - Delete the `sapporo-snow-festival-2027` link. The sentence before it stays as plain text.
- [ ] **2027-03-10** `singapore-entry-2026-sg-arrival-card` and **2027-03 (early)** `hong-kong-entry-2026`
  - Both expire 2027-03-31. Decide between a 2027 edition and an extended `valid_until`.
  - A new slug means updating the links from each other and from `power-bank-flight-rules-2026`.
- [ ] **2027-03 (after the JR spring timetable change)** `kanazawa-2-day-itinerary`
  - Replace the Thunderbird 45 / Tsurugi 46 example in blocks 2 and 9.
  - Re-check the Kagayaki time in block 6 and the four pass prices in block 19.
  - The diagram shows 「最快 2 小時 24 分」 and 「1,400 円」.
- [ ] **2027-03** `japan-cherry-blossom-2027`
  - Replace the 2026 Kiyomizu-dera night viewing dates and the Mint's walk-through dates in
    block 26 with the 2027 dates.
- [ ] **2027-03** `korea-naver-map-kakao-t-guide`
  - k.ride pay-driver option, 「133 種語言」, and Google Maps navigation in Korea (conditional
    approval 2026-02-27).
- [ ] **2027-03** `taoyuan-airport-departure-guide`
  - In-town check-in airlines and hours, A1 first train, and staffed e-Gate registration
    counters.
  - Find a newer liquids page than the 2007 CAA Q&A.
- [ ] **2027-04** `kanazawa-2-day-itinerary`
  - Kanazawa accommodation tax (block 44) and Kenroku-en hours and price (block 32; the diagram
    shows 320 円).
- [ ] **2027-04-01, then every six months** `return-to-taiwan-customs-duty-free-guide`
  - African swine fever country list (block 12) and the block-13 table.
  - When the amended Tobacco Hazards Prevention Act passes its third reading, rewrite block 23
    and the block-34 table. The same wording is in `taiwan-etiquette-safety-tips` and
    `taiwan-entry-2026-arrival-card`.
- [ ] **2027-05-11** `taiwan-long-weekends-2027-flight-planning` and `kanazawa-2-day-itinerary`
  - Delete the links to `japan-cherry-blossom-2027`, or point them at a 2028 edition. The
    sentences before them stay.
- [ ] **2027 H1, then every six months** `ho-chi-minh-city-4-day-itinerary` and `vietnam-money-sim-grab-guide`
  - Metro Line 1 fares and hours; the diagram's fare box.
  - SIM face-verification rules, if formally published: rewrite the SIM registration H3 with
    the decree number.
  - NAPAS QR partners and Grab / Xanh SM / Be payment options.
  - The Bank of Taiwan rate example date in block 15.
- [ ] **2027-06-30** `ho-chi-minh-city-4-day-itinerary`
  - Saigon Notre-Dame renovation: blocks 4, 19, 20.
- [ ] **2027-07** `hong-kong-airport-to-city`
  - MTR fare revision and the Airport Authority's new leaflet.
  - All fares on the diagram.
  - When T2 departure gates open, update the return-trip section.
- [ ] **2027-07 (after the 117 calendar)** `taiwan-long-weekends-2027-flight-planning`
  - Link the 2028 edition at the end.
- [ ] **2027-08-01** `singapore-4-day-itinerary`
  - Full re-check, including every time on the diagram.
- [ ] **2027-09** `hong-kong-4-day-itinerary`, `yokohama-day-trip-from-tokyo`, `singapore-changi-airport-mrt-simplygo-guide`
  - Yearly fare check. The diagrams carry fares or times.
- [ ] **2027-12-01** `taoyuan-airport-departure-guide`
  - Point block 7 at the 2028 long-weekend notice, or delete the link before 2028-01-01.

### 2028

- [ ] **2028-01-01** `kanazawa-2-day-itinerary`
  - Delete or re-point the block-15 link to `taiwan-long-weekends-2027-flight-planning`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.guides.pack_cli lint --slug <slug>
```

## Notes

- Source: the batch-6 writing workflow (writer attention notes, two rounds of fact-check
  "unresolved" lists, and the cross-article reconciliation), consolidated on 2026-09-14.
- The scope lists only the three diagrams that carry dated numbers. Widen it if another
  diagram needs a change.
