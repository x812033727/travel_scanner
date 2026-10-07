---
id: 2026-10-06-chiang-mai-3-day-itinerary-airport
title: chiang-mai-3-day-itinerary: airport taxi, Grab and city bus wording against AOT's transport detail pages
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-06T04:49:33Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/chiang-mai-3-day-itinerary.json
---

# chiang-mai-3-day-itinerary: airport taxi, Grab and city bus wording against AOT's transport detail pages

## Why

Batch 8's second wave (2026-10-06) found that Chiang Mai airport's transport list has readable,
server-rendered detail pages at
`https://chiangmai.airportthai.co.th/service/transportation/detail/<id>` (125 Airport Taxi,
126 Taxi Meter, 138 Grab pick-up points, 139 RTC City Bus, 145 Airport Shuttle Bus). The live
zh-TW article `chiang-mai-3-day-itinerary` was written when that page looked empty, and
several of its sentences now have no official support or miss what the pages say. The two new
articles (`chiang-mai-airport-transport-where-to-stay`,
`chiang-mai-night-markets-walking-streets`) already follow the detail pages; the three share
eight facts and must keep agreeing.

## Definition of done

- [ ] Each point below is re-read on the AOT page on the day and the article says only what
      the page supports; shared wording still matches the two batch-8 articles.
- [ ] The corrected zh-TW pack is published (owner consent, `guides-import --slug`), and its
      other locales are either re-translated or listed in a follow-up.

## Steps

- [ ] Taxi counter (blocks[2], blocks[3]): the article says the counter is in the arrivals hall;
      AOT 125/126 say Entrance 1, Main Terminal, Floor 1.
- [ ] Fixed fare (blocks[2], blocks[3]): "fixed price to the old city and Nimman, pay at the
      counter and take the slip" has no official text; AOT only says flat-rate, with no
      destinations, amounts or payment steps. The metered taxi adds 50 baht (126) and is not
      mentioned.
- [ ] Grab: add AOT's wording that pick-up and drop-off use designated points (138: Car park,
      Domestic, Floor 1). "GrabBike is common" has no basis on Grab's Thailand service-area page.
- [ ] City bus: the article gives only 06:00-23:30 (AOT home page). TAT Tokyo says 06:30-19:30
      hourly as of November 2024; the batch-8 articles disclose both. Page 139 says 30 baht per
      trip. Pages 139 and the home page swap the yellow and red lines; the article does not
      split stops by colour today, so keep it that way or add the same caveat sentence the
      batch-8 articles use.
- [ ] Late arrivals (blocks[3]): the listed service hours are 07:00-00:00 for the fixed-fare
      taxi and 07:00-23:00 for the metered taxi; Grab pick-up is listed as 24 hours.
- [ ] AOT's Thai name for A1/A2/A3 is a van (รถตู้); all three articles say 接駁巴士. Change all
      three together or none.

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug chiang-mai-3-day-itinerary
uv run pytest tests/test_guides_content_pack.py -q
```

Compare the eight shared facts with the two batch-8 packs; the side-by-side table is in
`docs/travel-guides-batch-8/ERRATA.md` (第二波) and in the batch work directory's
`chiang-mai-airport-transport-where-to-stay/verify-2.md`.

## Notes

- Found by the round-1 and round-2 verifiers of the two batch-8 Chiang Mai articles; nothing in
  the live article was changed by that work.
- The operator site `rtc-citybus.com` was still a host default page on 2026-10-06, so neither
  set of bus hours can be confirmed against the operator.
