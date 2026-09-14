---
id: 2026-09-14-launch-articles-batch-6-twenty-more
title: Launch articles batch 6: twenty more travel guides (Hong Kong, Singapore, Vietnam, Korea day trips, Taiwan departure)
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T07:03:16Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content
  - apps/web/public/guides
  - docs/travel-guides-batch-6
---

# Launch articles batch 6: twenty more travel guides (Hong Kong, Singapore, Vietnam, Korea day trips, Taiwan departure)

## Why

After batch 5 (PR #471, live 2026-09-14) and PR #468 (15 travel how-tos), the site has 85 zh-TW
travel articles. Seven destinations in the catalogue still have none: Hong Kong, Singapore,
Hanoi, Ho Chi Minh City, Phuket, Kanazawa and Yokohama.

The departure side of a trip from Taiwan is also missing, although this is a flight search site:
Taoyuan departure, power banks on board, and the customs allowance on the way home.

This batch covers both gaps. It also adds three dated notices readers plan months ahead for
(2027 long weekends, 2027 cherry blossom, the new power-bank rules), the Seoul day trips the
itineraries point at (DMZ, Suwon), and the Korean map and taxi apps.

The specs were planned and fact-checked before writing, one file per article under
`docs/travel-guides-batch-6/`. A writer takes one spec and follows its README; nothing from the
planning session's scratchpad is needed.

## Definition of done

- [ ] Twenty packs under `apps/api/app/guides/content/`, zh-TW. Slug, kind, destination,
      topics, display order and validity match `docs/travel-guides-batch-6/README.md`.
      Each pack has a Commons hero, a self-drawn SVG diagram, a table of at most four
      columns, a callout, sources with `checked_on`, and the partner blocks its spec places.
- [ ] Every number is re-checked on the official page on the day of writing. Anything the page
      does not state is written as 以官網為準. Each article keeps a `notes.md` in the writing
      workspace.
- [ ] Internal links point only at slugs that exist with a zh-TW version, or at this batch.
      A how-to never links a notice that expires within its reading period unless its spec
      names a removal date.
- [ ] The packaged-content test passes. After deploy, `guides-import --dry-run` shows exactly
      these twenty as `create`; then `--publish`.
- [ ] The launch PR files a task for every dated item in each spec's "上線後與交叉檢查"
      section.

## Steps

The twenty (slug · kind · destination · topics · display order):

1. `taiwan-long-weekends-2027-flight-planning` · intel (2027-12-31) · none · season, budget · 810
2. `power-bank-flight-rules-2026` · intel (2027-01-31) · none · packing, safety · 820
3. `japan-cherry-blossom-2027` · intel (2027-05-10) · none · season, nature, viewpoint · 830
4. `hong-kong-4-day-itinerary` · howto · hong-kong · itinerary, viewpoint, culture · 840
5. `return-to-taiwan-customs-duty-free-guide` · howto · none · entry, shopping · 850
6. `hong-kong-airport-to-city` · howto · hong-kong · transport, budget · 860
7. `singapore-4-day-itinerary` · howto · singapore · itinerary, culture, nature · 870
8. `yokohama-day-trip-from-tokyo` · howto · tokyo · itinerary, transport, viewpoint · 880
9. `singapore-entry-2026-sg-arrival-card` · intel (2027-03-31) · singapore · entry · 890
10. `singapore-changi-airport-mrt-simplygo-guide` · howto · singapore · transport, budget · 900
11. `dmz-day-trip-from-seoul` · howto · seoul · itinerary, culture · 910
12. `suwon-hwaseong-day-trip` · howto · seoul · itinerary, culture, transport · 920
13. `hong-kong-entry-2026` · intel (2027-03-31) · hong-kong · entry · 930
14. `hanoi-4-day-itinerary` · howto · hanoi · itinerary, culture, food · 940
15. `taoyuan-airport-departure-guide` · howto · none · transport, packing · 950
16. `phuket-airport-transport-where-to-stay` · howto · phuket · transport, hotel, beach · 960
17. `vietnam-money-sim-grab-guide` · howto · none · connectivity, budget, packing · 970
18. `ho-chi-minh-city-4-day-itinerary` · howto · ho-chi-minh-city · itinerary, culture, transport · 980
19. `korea-naver-map-kakao-t-guide` · howto · none · transport, connectivity · 990
20. `kanazawa-2-day-itinerary` · howto · kanazawa · itinerary, culture, transport · 1000 (not featured)

- [ ] One writer per article, working from its spec and the README. Write into a workspace
      outside the repository, check with `pack_cli ingest --dry-run`, then render each diagram
      and look at it.
- [ ] Coordinator review of each article:
  - [ ] spot-check `notes.md` against the official pages
  - [ ] follow up every "needs attention" item in the writer's report
  - [ ] run the checks the tool does not: link targets, offer placement, table width, Commons author strings
- [ ] Run `pack_cli ingest` for real and the packaged-content test, then open the PR and
      file the dated follow-ups.
- [ ] Deploy, then run `guides-import --dry-run` and `--publish` on the host. Check that the
      twenty pages, heroes, diagrams and sitemap entries return 200.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.guides.pack_cli lint --kind howto
uv run python -m app.guides.pack_cli lint --kind intel
```

On the host, `guides-import --dry-run` should report exactly the twenty slugs as `create`. After
`--publish`, every `/zh-TW/guides/<kind>/<slug>` returns 200 without `noindex`, and its hero and
`diagram-1.svg` load.

## Notes

- **How the plan was made (2026-09-14):**
  - Six market lenses proposed 55 candidates, each with a checked official source.
  - Three judges scored them on reader demand, site value and verifiability.
  - One agent per pick opened the nearest existing articles and read three to six official pages.
  - A critic found that PR #468 had landed 15 zh-TW travel how-tos after the article list was
    exported, so the specs were revised against current main.
  - Three consistency rounds followed. They covered link targets and kinds, links to notices
    that expire too soon, cross-links inside the batch, offer rules, and facts that contradict
    #468 or batch 5.
- **Naoshima was swapped out.** It is not in the destination catalogue, so it could only borrow
  `osaka-kyoto`. Vietnam money, SIM and Grab took its place: both Vietnam itineraries had
  nowhere to link for those sections.
- **Batch 7:**
  - Krabi first. Sendai, Daegu, Chiang Rai, Da Lat, Hue and Jeonju also still have no articles.
  - Zao and Ginzan Onsen winter waits until the resorts publish their dates in November.
  - 2027 Lunar New Year across Asia overlaps the long-weekend notice.
  - Hong Kong Disneyland vs Ocean Park, the Seoul Han River bus, the Korean express bus and Hue
    were dropped: their core figures were not readable on official pages.
- **Facts the plan already settled (writers need not re-argue them):**
  - The 2027 Taiwan calendar has nine long weekends of three days or more. The 2028 New Year
    break, with its 2027-12-31 make-up day, counts in 2027.
  - Japan's government offices close from 12-29 to 01-03. That is office closure, not a
    national holiday; `japan-year-end-new-year-2026-2027` uses the same wording.
  - Over-limit medicines need a TFDA import permit arranged before arrival; declaring them at
    the red channel is not enough. `japan-drugstore-shopping-list` uses the same wording.
  - Exchanging money in Vietnam at an unauthorised exchange point is fined. Always write
    "unauthorised"; never write "gold shops are illegal".
  - Grab in Vietnam needs mobile data, not a Vietnamese SIM.
- **Dated follow-ups are written into each spec.** File them when the articles launch, not
  before. Examples:
  - Remove the 2026 section of the long-weekend notice on 2027-01-10.
  - Remove links to the snow festival and cherry blossom notices the day after each expires.
  - Remove links from the Taoyuan and Kanazawa guides to the long-weekend notice on 2028-01-01.
  - Drop Suwon's 2026 festival callout after 2026-10-14.
  - Add back-links from `da-nang-hoi-an-4-day-itinerary`, `vietnam-entry-2026-evisa`,
    `korea-olive-young-tax-refund-shopping` and `japan-drugstore-shopping-list`.
- **Scope overlap:** `2026-09-13-life-ai-batch-03` (in progress) also covers
  `apps/api/app/guides/content` and `apps/web/public/guides`. The slugs differ, so a rebase onto
  whichever lands first is enough, as with batches 3 to 5.
