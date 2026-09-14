---
id: 2026-09-14-launch-articles-batch-6-twenty-more
title: Launch articles batch 6: twenty more travel guides (Hong Kong, Singapore, Vietnam, Korea day trips, Taiwan departure)
status: done
priority: P2
area: docs
owner: claude-opus-5
claimed_at: 2026-09-14T07:20:11Z
created_at: 2026-09-14T07:03:16Z
completed_at: 2026-09-14T11:13:33Z
branch:
depends_on: []
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
  - apps/web/public/guides/taiwan-long-weekends-2027-flight-planning
  - apps/web/public/guides/power-bank-flight-rules-2026
  - apps/web/public/guides/japan-cherry-blossom-2027
  - apps/web/public/guides/hong-kong-4-day-itinerary
  - apps/web/public/guides/return-to-taiwan-customs-duty-free-guide
  - apps/web/public/guides/hong-kong-airport-to-city
  - apps/web/public/guides/singapore-4-day-itinerary
  - apps/web/public/guides/yokohama-day-trip-from-tokyo
  - apps/web/public/guides/singapore-entry-2026-sg-arrival-card
  - apps/web/public/guides/singapore-changi-airport-mrt-simplygo-guide
  - apps/web/public/guides/dmz-day-trip-from-seoul
  - apps/web/public/guides/suwon-hwaseong-day-trip
  - apps/web/public/guides/hong-kong-entry-2026
  - apps/web/public/guides/hanoi-4-day-itinerary
  - apps/web/public/guides/taoyuan-airport-departure-guide
  - apps/web/public/guides/phuket-airport-transport-where-to-stay
  - apps/web/public/guides/vietnam-money-sim-grab-guide
  - apps/web/public/guides/ho-chi-minh-city-4-day-itinerary
  - apps/web/public/guides/korea-naver-map-kakao-t-guide
  - apps/web/public/guides/kanazawa-2-day-itinerary
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

- [x] Twenty packs under `apps/api/app/guides/content/`, zh-TW. Slug, kind, destination,
      topics, display order and validity match `docs/travel-guides-batch-6/README.md`.
      Each pack has a Commons hero, a self-drawn SVG diagram, a table of at most four
      columns, a callout, sources with `checked_on`, and the partner blocks its spec places.
- [x] Every number is re-checked on the official page on the day of writing. Anything the page
      does not state is written as 以官網為準. Each article keeps a `notes.md` in the writing
      workspace.
- [x] Internal links point only at slugs that exist with a zh-TW version, or at this batch.
      A how-to never links a notice that expires within its reading period unless its spec
      names a removal date.
- [x] The packaged-content test passes. After deploy, `guides-import --dry-run` shows exactly
      these twenty as `create`; then `--publish`.
- [x] The launch PR files a task for every dated item in each spec's "上線後與交叉檢查"
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

- [x] One writer per article, working from its spec and the README. Write into a workspace
      outside the repository, check with `pack_cli ingest --dry-run`, then render each diagram
      and look at it.
- [x] Coordinator review of each article:
  - [x] spot-check `notes.md` against the official pages
  - [x] follow up every "needs attention" item in the writer's report
  - [x] run the checks the tool does not: link targets, offer placement, table width, Commons author strings
- [x] Run `pack_cli ingest` for real and the packaged-content test, then open the PR and
      file the dated follow-ups.
- [x] Deploy, then run `guides-import --dry-run` and `--publish` on the host. Check that the
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
- **Scope and claim (2026-09-14):** the scope lists the twenty pack files and picture folders,
  not the whole content directories. Four codex tasks (`2026-09-14-ai-news-july-september`,
  `2026-09-14-ai-terms-series`, `2026-09-14-claude-code-tutorial-center`,
  `2026-09-14-new-trip-auth-draft-ci`) hold `apps/api/app/guides/content` and
  `apps/web/public/guides` as whole directories. The tool treats any path under them as
  overlapping, so this task was claimed with `--force`. None of their slugs is in this batch.
- **How the articles were written (2026-09-14):**
  - A workflow ran each article through a pipeline: writer, independent fact-checker, then a
    second checker whenever the first one changed more than three facts. 15 of the 20 got the
    second round.
  - A final agent reconciled facts that several articles share: power banks, customs, and the
    Hong Kong / Singapore / Vietnam / Korea sets. It changed 4 places.
  - The checkers re-opened between 34 and 104 claims per article on official pages. Each
    article's corrections are logged under "查核修正" in its `notes.md` in the writing workspace.
  - Every workspace passed `scratchpad/check6.py`, which wraps the repo ingest `--dry-run` and
    also checks link targets, offer placement, tables of at most four columns, and markup. Every
    diagram was rendered with Edge and looked at.
- **Spot-checked by the coordinator on the official pages:**
  - Singapore vapes: fine up to SGD 10,000 from 2026-05-01 under the TVCA (gov.sg).
  - Hanoi bus 86: VND 50,000 (Noi Bai airport site).
  - The notes carry curl or PDF evidence for the customs 5% rate, the Hong Kong e-cigarette
    rules and Kenroku-en's 320 yen.
- **Changed after the workflow:**
  - `taiwan-long-weekends-2027-flight-planning` no longer describes price alerts, LINE alerts
    or per-search charges. Production `/api/travel/runtime/site-visibility` reports
    `alerts_enabled: false` and `pricing_enabled: false`. The H2 lost 「開價格通知」.
  - Three heroes the repo tool left over 200 KB were re-encoded from the same Commons originals
    at JPEG quality 52–54 (`scratchpad/shrink_heroes6.py`), all now under 195–198 KB: Seoul taxis,
    Changi station, and the Changi arrival hall (with a 0.6 px blur).
- **Spec errors are listed in `docs/travel-guides-batch-6/ERRATA.md`.** The published packs are
  authoritative.
- **Filed follow-ups:**
  - `2026-09-14-batch-6-guides-dated-maintenance`: every dated edit, 2026-10 to 2028-01.
  - `2026-09-14-existing-guides-fixes-from-batch-6`: 11 corrections to articles already on main,
    and back-links from 20 of them.
  - `2026-09-14-food-links-city-param-ignored`: the food directory reads `destination_id`, so
    every `foods?city=` link, in 60 packs, opens the unfiltered list.
- **Accepted as they are, flagged by checkers:**
  - Incidental signage in the DMZ, Seoul taxi and Taoyuan heroes.
  - A partial side-face in the Hong Kong entry `photo-1`.
  - Two links from `hong-kong-4-day-itinerary` to `hong-kong-airport-to-city`, as its spec
    intends: one in the transport section and one on Day 4.
- **Privacy incident:** six fact-checkers (cherry blossom, power bank, Hanoi, Yokohama, DMZ,
  Kanazawa) put the site owner's personal e-mail address in the curl `User-Agent` they sent to
  Wikimedia Commons. It cannot be withdrawn. The README now forbids it and names the
  repository's editorial User-Agent instead.
- **Tooling:** one writer reported `pack_ingest` raising `UnicodeEncodeError` on a Commons file
  name with non-ASCII characters. The checkers could not reproduce it, and every final ingest
  succeeded on Windows.
