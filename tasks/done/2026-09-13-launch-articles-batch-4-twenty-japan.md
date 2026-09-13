---
id: 2026-09-13-launch-articles-batch-4-twenty-japan
title: Launch articles batch 4: twenty more travel guides (Japan, Korea, Thailand)
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-13T06:00:01Z
created_at: 2026-09-13T05:58:58Z
completed_at: 2026-09-13T13:16:58Z
branch: claude/guide-articles-batch-4
depends_on: []
scope:
  - apps/api/app/guides/content
  - apps/web/public/guides
---

# Launch articles batch 4: twenty more travel guides (Japan, Korea, Thailand)

## Why

Thirty zh-TW articles were live (PR #443, PR #446) and the Taiwan set for the other four
locales landed as PR #454 while this batch was being written. The owner asked for twenty
more in the same way. This batch deepens the markets Taiwanese readers book most: the two
airport transfers still missing (Fukuoka, New Chitose), the day trips every Tokyo, Osaka
and Busan itinerary asks about (Kamakura, Hakone, Kobe and Arima, Gyeongju), three more
cities (Nagoya, Hiroshima and Miyajima, Okinawa) and Bangkok, the Korean questions the
Seoul and Busan articles keep deferring (KTX and SRT tickets, Everland and Lotte World,
SIM and eSIM, Olive Young and tax refund, Jeju car rental), two dated Japan notices
(year-end closures, the 2026-27 ski season), a Japan IC-card and an onsen-ryokan guide,
and the Thailand entry notice (TDAC) that the Bangkok transfer article had nowhere to
point at.

## Definition of done

- [x] Twenty packs under `apps/api/app/guides/content/`, zh-TW, each with a hero photo, a
      self-drawn SVG diagram, a table, a callout, sources with `checked_on`, and partner
      blocks per the rules in `docs/travel-guides.md`; the packaged-content test passes for
      all seventy packs.
- [x] Every photograph from Wikimedia Commons under CC0 / Public domain / CC BY / CC BY-SA,
      licence and author read from the Commons API; every number on a diagram appears in
      the article text and no label is below 15 px.
- [x] Facts checked on official pages on the day of writing; anything unverified written
      as 以官網為準.

## Steps

The twenty (slug · kind · destination · topics):

1. `fukuoka-airport-to-hakata-tenjin` · howto · fukuoka · transport, budget
2. `new-chitose-airport-to-sapporo` · howto · sapporo · transport, budget
3. `okinawa-4-day-itinerary` · howto · okinawa · itinerary, beach, family
4. `nagoya-3-day-itinerary` · howto · nagoya · itinerary, transport, food
5. `hiroshima-miyajima-2-day` · howto · hiroshima · itinerary, culture, transport
6. `kamakura-enoshima-day-trip` · howto · tokyo · itinerary, culture, transport
7. `hakone-day-trip-free-pass` · howto · tokyo · itinerary, nature, transport
8. `kobe-arima-day-trip` · howto · osaka-kyoto · itinerary, food, culture
9. `japan-ic-card-suica-icoca-guide` · howto · none · transport, budget
10. `japan-year-end-new-year-2026-2027` · intel (2027-01-10) · none · season, culture, shopping
11. `japan-ski-season-2026-2027` · intel (2027-03-31) · none · season, nature
12. `japan-onsen-ryokan-guide` · howto · none · etiquette, culture, hotel
13. `korea-ktx-srt-ticket-guide` · howto · none · transport, budget
14. `everland-lotte-world-guide` · howto · seoul · family, itinerary
15. `korea-esim-sim-wifi` · howto · none · connectivity, packing
16. `korea-olive-young-tax-refund-shopping` · howto · none · shopping, budget
17. `gyeongju-day-trip-from-busan` · howto · busan · itinerary, culture, transport
18. `jeju-car-rental-guide` · howto · jeju · transport, packing
19. `thailand-entry-2026-tdac` · intel (2026-12-31) · none · entry
20. `bangkok-4-day-itinerary` · howto · bangkok · itinerary, culture, food

- [x] Seven writing agents in parallel from one spec (`article_brief_v4.md`: pack, Commons
      manifest, the SVG diagram drawn by the agent, and a self-check every agent runs before
      reporting).
- [x] `ingest_pack4.py --check <slug>` then `ingest_pack4.py <slug>` per article: pydantic
      validation, structure and link rules, diagram rules (numbers vs text, labels >= 15 px),
      copy the SVG, fetch and licence-check the photos, write sizes and credits, save.
- [x] Run the packaged-content test, commit, open the PR; publishing on the host follows
      the deploy (`guides-import --dry-run`, then `--publish`, see Notes).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.cli guides-import --actor-email <admin> --dry-run
```

Then `/zh-TW/guides/howto/<slug>` for each of the twenty renders its hero, diagram, table
and partner blocks; `/sitemap.xml` carries twenty more entries with `lastmod`.

## Notes

- Kamakura and Hakone are filed under `tokyo`, Kobe and Arima under `osaka-kyoto`,
  Gyeongju under `busan`: those are the cities the reader is staying in, the destination
  filter they will use, and the destinations with approved offers today (tokyo, osaka-kyoto,
  seoul, busan, taipei × activities, transport). Fukuoka, Sapporo, Okinawa, Nagoya,
  Hiroshima, Jeju and Bangkok articles carry offer blocks that render nothing until the
  back office approves an offer for that city; the Korea SIM article's connectivity block
  likewise. Back-office follow-up: activities and transport offers for those seven cities,
  connectivity for seoul.
- How it was produced (2026-09-13): seven general-purpose agents, each 2–3 articles, from
  one brief; every agent ran the check script until it printed OK. Three agents were cut
  off by the session limit at the reporting step — their files were complete and passed
  the same check, so they were ingested from the files without a report, as in batch 2.
  Diagrams were rendered with headless Edge (`msedge --headless --screenshot`, a
  `?v=` cache-buster on the SVG URL, otherwise the profile serves the stale file) and
  seven labels that overlapped in the render were moved by hand; the mechanical check
  cannot see overlaps.
- Image budget: one hero (KTX-Cheongryong, a 30 MB original) stayed at 261 KB even at
  JPEG quality 44 and was swapped for a lighter 2026 photo; three inline photos over
  150 KB were re-thumbnailed at 900–1,100 px (`max_width` in the manifest). Every hero is
  now ≤200 KB and every photo ≤150 KB.
- Facts worth remembering: Thailand's visa exemption for Taiwan drops from 60 to 30 days
  on 2026-09-15 (TAT, Royal Gazette 2026-08-31; BOCA already updated); TDAC is free and due
  within 3 days of arrival. Nozomi is all-reserved 2026-12-25 to 2027-01-05. Shuri Castle's
  main hall opens 2026-11-23 and the paid area goes 400 → 1,000 yen that day. Hakone
  ropeway 2,000 / pirate ship 1,700 / bus 1,220 yen since 2025-10-01; Hakone Freepass 2-day
  7,100. Miyajima visitor tax 100 yen; Hiroshima Castle keep closed from 2026-03. Niseko
  United opens 2026-11-28 with a five-tier all-mountain pass (peak 13,500). KTX-Cheongryong
  Seoul–Busan 2 h 18 min; SRT 2 h 11 min, 52,200 won from 2026-09-01; Singyeongju station
  is now "Gyeongju". Bulguksa and Seokguram free since 2023-05-04; Busan–Gyeongju intercity
  bus 7,700 won, +9 % from 2026-10-01. Taiwan's international driving permit is accepted in
  Korea under the 2022 MOU (both foreign ministries confirm). Korea instant tax refund:
  15,000–1,000,000 won per receipt, 5,000,000 cumulative; Taiwan's duty-free allowance
  NT$35,000. Welcome Suica Mobile: 180 days, 13+; blank Suica/PASMO sales resumed
  2025-03-01. Fukuoka subway to Hakata/Tenjin 260 yen; New Chitose JR 1,230 yen, bus 1,500.
- Written as 以官網為準 because the official page did not state it: Fukuoka Airport Express
  journey time and taxi fares; New Chitose first/last buses; Chao Phraya weekend boats
  (the timetable lists weekdays only); Wat Arun and Jim Thompson House admission; BTS/MRT
  fares; KT/SKT eSIM prices; Everland ticket prices (date-tiered); Jeju IDP fee and child-seat
  ages; department-store 初売り dates for 2027; the 2026-27 opening dates of Hakuba and GALA.
- Publishing on the host happens after deploy: `guides-import --dry-run`, then `--publish`
  with the admin e-mail, as for the earlier batches.
