---
id: 2026-09-12-launch-articles-batch-1-ten-travel
title: Launch articles batch 1: ten travel guides with images
status: done
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-12T18:51:47Z
created_at: 2026-09-12T17:42:18Z
completed_at: 2026-09-12T18:54:02Z
branch: claude/guide-launch-articles
depends_on:
  - 2026-09-12-guide-content-pack-and-import-command
scope:
  - apps/api/app/guides/content
  - apps/web/public/guides
  - docs/travel-guides.md
---

# Launch articles batch 1: ten travel guides with images

## Why

The travel section has nineteen topics, a working editor and zero articles. The owner asked
for ten guides that introduce readers to the destinations the catalog already sells
(approved Klook offers for tokyo, osaka-kyoto, seoul, busan × activities/transport), with
pictures, and with the partner links placed where a reader has just decided to buy.

## Definition of done

- [x] Ten packs under `apps/api/app/guides/content/`, zh-TW first (en in a follow-up), each
      with a hero photo, at least one self-drawn SVG diagram, a table, sources with
      `checked_on`, and its partner blocks per the placement rules in `docs/travel-guides.md`.
- [x] Every image under `apps/web/public/guides/<slug>/`: hero 1600×900 JPEG ≤200 KB, inline
      WebP ≤1200 px wide ≤150 KB, SVG diagrams with `<title>`/`<desc>` and system-font
      fallbacks only; every photo credited (author, licence, source page) and licensed
      CC0 / Public Domain / CC BY / CC BY-SA only.
- [x] Every fare, duration and rule checked against an official page on the day of writing
      and cited in `sources`; nothing the official page did not confirm.
- [x] `docs/travel-guides.md` carries the image and placement rules as the review standard.

## Steps

The ten (slug · kind · destination · topics):

1. `narita-haneda-to-tokyo` · howto · tokyo · transport, budget
2. `tokyo-transit-passes` · howto · tokyo · transport, budget
3. `tokyo-5-day-itinerary` · howto · tokyo · itinerary, culture, shopping
4. `kansai-airport-to-osaka-kyoto` · howto · osaka-kyoto · transport, budget
5. `osaka-kyoto-nara-4-day-itinerary` · howto · osaka-kyoto · itinerary, culture, food
6. `incheon-airport-to-seoul` · howto · seoul · transport, budget
7. `seoul-4-day-itinerary` · howto · seoul · itinerary, culture, shopping
8. `japan-autumn-leaves-2026` · intel (valid_until 2026-12-15) · none · season, nature, viewpoint
   (offer blocks name `osaka-kyoto` and `tokyo` themselves)
9. `korea-entry-2026-k-eta-e-arrival` · intel (valid_until 2026-12-31) · none · entry
10. `japan-tax-free-refund-2026` · intel (valid_until 2027-01-31) · none · shopping (no offers)

- [x] Research and write each pack; diagrams as SVG with local script + English labels so one
      file serves every locale.
- [x] Photos from Wikimedia Commons only, downloaded and resized with Pillow (`apps/api`
      venv), credit recorded from the Commons API (licence, artist, file page).
- [x] Dry-run import locally (the packaged-content test) and eyeball every kind of block
      through a mock API; publishing on the VPS happens after deploy.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.cli guides-import --actor-email <admin> --dry-run
```

Then `/zh-TW/guides` lists ten cards with heroes; each article shows its diagram, table and
partner blocks; `/sitemap.xml` carries ten entries with `lastmod`.

## Notes

- Placement rules: one disclosure line, ≤3 offer blocks, after the paragraph that creates
  the intent, never before the first heading; topics with no honest module (entry, packing,
  budget, etiquette, safety, food, shopping, nightlife) get no end panel and only an offer
  block that is directly about that section; nothing under an expired notice.
- How it was produced (2026-09-13): four writing agents in parallel from one spec, each
  delivering the pack plus Commons candidates; a script read the Commons API licence and
  artist for every photo and refused anything NC/ND; diagrams were drawn by hand and their
  times aligned to the article's verified numbers (unverified ones, like limousine bus
  journey times, are not printed on the diagram).
- Facts worth remembering from the research: Weathernews' first 2026 foliage forecast is
  out (9/3, later than average); K-ETA exemption extended to 2026-12-31; Japan's tax-free
  refund system starts 2026-11-01 by sale date with no transition; JR Pass 7-day rises to
  53,000 yen on 2026-10-01; Tokyo Subway Ticket is 1,000/1,500/2,000; TOURIST PASMO launched
  2026-05; HARUKA timetable changed 2026-03-14 (last from KIX 22:16).
- Things the official pages did not state, written as 以官網為準: Keisei Access Express fares,
  Haneda flat-rate taxi amounts, KAL limousine 6703 fare, Kiyomizu-dera admission on its own
  site (taken from the 西国三十三所 site), Nami Island prices (KTO page), Hankyu/Keihan fares.
- Second batch candidates (not here): Busan 3 days, Japan eSIM comparison (needs a
  connectivity destination offer), hotel-area guides for Tokyo / Osaka / Seoul (need hotel
  destination offers), Fukuoka and Sapporo airport transfers, Taipei for en/ja/ko readers,
  and the en versions of these ten (`locales.en` in the same packs).
