---
id: 2026-09-13-launch-articles-batch-2-twenty-more
title: Launch articles batch 2: twenty more travel guides
status: done
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-13T02:36:54Z
created_at: 2026-09-13T02:36:40Z
completed_at: 2026-09-13T04:08:26Z
branch: claude/guide-articles-batch-2
depends_on: []
scope:
  - apps/api/app/guides/content
  - apps/web/public/guides
  - docs/travel-guides.md
---

# Launch articles batch 2: twenty more travel guides

## Why

The first ten articles (PR #443) cover the two airport transfers, the two transit-pass
questions and the three itineraries the catalog's approved offers point at, plus three
notices. The owner asked for twenty more. This batch widens coverage to the destinations
Taiwanese readers actually book (Busan, Jeju, Fukuoka, Sapporo, Okinawa, Bangkok), adds the
three "where to stay" guides that the hotel module needs, the two theme parks the activities
module sells best, and the cross-destination questions every first trip asks (Shinkansen
tickets, eSIM, drugstores, Japan entry), with three more dated notices.

## Definition of done

- [x] Twenty packs under `apps/api/app/guides/content/`, zh-TW, each with a hero photo, a
      self-drawn SVG diagram, a table, sources with `checked_on`, and partner blocks per the
      rules in `docs/travel-guides.md`; the packaged-content test passes for all thirty.
- [x] Every photograph from Wikimedia Commons under CC0 / Public domain / CC BY / CC BY-SA,
      licence and author read from the Commons API; every diagram labels only numbers the
      article verified.
- [x] Facts checked on official pages on the day of writing; anything unverified written as
      以官網為準.

## Steps

The twenty (slug · kind · destination · topics):

1. `busan-3-day-itinerary` · howto · busan · itinerary, culture, food
2. `gimhae-airport-to-busan` · howto · busan · transport, budget
3. `jeju-3-day-itinerary` · howto · jeju · itinerary, nature, transport
4. `seoul-subway-t-money-guide` · howto · seoul · transport, budget
5. `seoul-where-to-stay` · howto · seoul · hotel, budget
6. `korea-winter-events-2026` · intel (2027-01-10) · none · season, culture
7. `tokyo-where-to-stay` · howto · tokyo · hotel, budget
8. `tokyo-disney-guide` · howto · tokyo · family, itinerary
9. `japan-entry-2026-visit-japan-web` · intel (2026-12-31) · none · entry
10. `kyoto-bus-subway-guide` · howto · osaka-kyoto · transport, budget
11. `osaka-kyoto-where-to-stay` · howto · osaka-kyoto · hotel, budget
12. `usj-guide` · howto · osaka-kyoto · family, itinerary
13. `fukuoka-3-day-itinerary` · howto · fukuoka · itinerary, food, transport
14. `sapporo-3-day-itinerary` · howto · sapporo · itinerary, season, food
15. `okinawa-car-rental-guide` · howto · okinawa · transport, packing
16. `japan-shinkansen-ticket-guide` · howto · none · transport, budget
17. `japan-esim-sim-wifi` · howto · none · connectivity, packing
18. `japan-drugstore-shopping-list` · howto · none · shopping, budget
19. `japan-winter-illumination-2026` · intel (2027-01-15) · none · season, viewpoint
20. `bangkok-airport-to-city` · howto · bangkok · transport, budget

- [x] Seven writing agents in parallel from one spec (`article_brief_v2.md`: pack, images
      JSON, Commons manifest, and the SVG diagram drawn by the agent this time).
- [x] `ingest_pack.py <slug>` per article: pydantic validation, copy the SVG, fetch and
      licence-check the photos, write sizes and credits, save to the content folder.
- [x] Review each pack against its diagram (numbers must match), eyeball a sample through the
      mock API, run the packaged-content test, commit, open the PR stacked on #443 (rebased onto main once #443 merged).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.cli guides-import --actor-email <admin> --dry-run
```

## Notes

- Destinations with approved offers today: tokyo, osaka-kyoto, seoul, busan (activities,
  transport). Jeju, Fukuoka, Sapporo, Okinawa and Bangkok articles carry offer blocks that
  render nothing until an offer is approved for that city; hotel and connectivity modules
  likewise. Fill these in the back office after deploy.
- Second-batch diagrams are agent-drawn; the review checks viewBox 1600×900, no external
  references, system fonts only, and that every time or fare printed on the diagram appears
  in the article's verified text.

## Outcome (2026-09-13)

- All twenty packs ingested; the packaged-content test passes for thirty articles. Fourteen
  came with the agents' fact-check reports; the Kansai and Japan-wide agents (six articles)
  were cut off by the session rate limit after writing every file, so their packs were
  validated and reviewed from the files alone (sources, offers, diagram numbers, renders)
  without a closing report.
- Diagram review was mechanised (`review_diagrams.py` in the session scratchpad): every
  number on a diagram must appear in the article text; labels under 15 px were raised.
  The rule is now in `docs/travel-guides.md`.
- Two ingest pitfalls fixed on the way: the script copied SVGs to `public/<slug>` instead of
  `public/guides/<slug>`, and one hero (`osaka-kyoto-where-to-stay`) only compresses to
  243 KB at the quality floor — within the 300 KB test budget, above the 200 KB guideline.
- After deploy: `guides-import --dry-run` then `--publish` on the host, as for batch 1.
