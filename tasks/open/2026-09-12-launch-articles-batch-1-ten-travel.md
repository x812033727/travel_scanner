---
id: 2026-09-12-launch-articles-batch-1-ten-travel
title: Launch articles batch 1: ten travel guides with images
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-12T17:42:18Z
completed_at:
branch:
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

- [ ] Ten packs under `apps/api/app/guides/content/`, zh-TW first (en in a follow-up), each
      with a hero photo, at least one self-drawn SVG diagram, a table, sources with
      `checked_on`, and its partner blocks per the placement rules in `docs/travel-guides.md`.
- [ ] Every image under `apps/web/public/guides/<slug>/`: hero 1600×900 JPEG ≤200 KB, inline
      WebP ≤1200 px wide ≤150 KB, SVG diagrams with `<title>`/`<desc>` and system-font
      fallbacks only; every photo credited (author, licence, source page) and licensed
      CC0 / Public Domain / CC BY / CC BY-SA only.
- [ ] Every fare, duration and rule checked against an official page on the day of writing
      and cited in `sources`; nothing the official page did not confirm.
- [ ] `docs/travel-guides.md` carries the image and placement rules as the review standard.

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

- [ ] Research and write each pack; diagrams as SVG with local script + English labels so one
      file serves every locale.
- [ ] Photos from Wikimedia Commons only, downloaded and resized with Pillow (`apps/api`
      venv), credit recorded from the file page.
- [ ] Dry-run import locally against SQLite, then publish on the VPS.

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
- Second batch candidates (not here): Busan 3 days, Japan eSIM comparison (needs a
  connectivity destination offer), hotel-area guides for Tokyo / Osaka / Seoul (need hotel
  destination offers), Fukuoka and Sapporo airport transfers, Taipei for en/ja/ko readers.
