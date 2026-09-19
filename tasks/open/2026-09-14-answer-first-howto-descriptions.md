---
id: 2026-09-14-answer-first-howto-descriptions
title: AIO: 68 how-to descriptions enumerate topics instead of answering
status: in-progress
priority: P3
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:15:21Z
created_at: 2026-09-14T13:48:24Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/guides/content/busan-3-day-itinerary.json
  - apps/api/app/guides/content/dmz-day-trip-from-seoul.json
  - apps/api/app/guides/content/fuji-kawaguchiko-day-trip.json
  - apps/api/app/guides/content/fukuoka-airport-to-hakata-tenjin.json
  - apps/api/app/guides/content/gimhae-airport-to-busan.json
  - apps/api/app/guides/content/hakone-day-trip-free-pass.json
  - apps/api/app/guides/content/himeji-castle-day-trip.json
  - apps/api/app/guides/content/hiroshima-miyajima-2-day.json
  - apps/api/app/guides/content/incheon-airport-to-seoul.json
  - apps/api/app/guides/content/japan-drugstore-shopping-list.json
  - apps/api/app/guides/content/japan-entry-2026-visit-japan-web.json
  - apps/api/app/guides/content/japan-esim-sim-wifi.json
  - apps/api/app/guides/content/japan-ic-card-suica-icoca-guide.json
  - apps/api/app/guides/content/japan-ski-season-2026-2027.json
  - apps/api/app/guides/content/japan-winter-illumination-2026.json
  - apps/api/app/guides/content/japan-year-end-new-year-2026-2027.json
  - apps/api/app/guides/content/jeju-3-day-itinerary.json
  - apps/api/app/guides/content/kamakura-enoshima-day-trip.json
  - apps/api/app/guides/content/kobe-arima-day-trip.json
  - apps/api/app/guides/content/korea-entry-2026-k-eta-e-arrival.json
  - apps/api/app/guides/content/korea-esim-sim-wifi.json
  - apps/api/app/guides/content/korea-money-exchange-wowpass-guide.json
  - apps/api/app/guides/content/korea-olive-young-tax-refund-shopping.json
  - apps/api/app/guides/content/nagoya-3-day-itinerary.json
  - apps/api/app/guides/content/narita-haneda-to-tokyo.json
  - apps/api/app/guides/content/new-chitose-airport-to-sapporo.json
  - apps/api/app/guides/content/okinawa-4-day-itinerary.json
  - apps/api/app/guides/content/osaka-kyoto-where-to-stay.json
  - apps/api/app/guides/content/sapporo-snow-festival-2027.json
  - apps/api/app/guides/content/seoul-4-day-itinerary.json
  - apps/api/app/guides/content/seoul-palaces-hanbok-guide.json
  - apps/api/app/guides/content/seoul-subway-t-money-guide.json
  - apps/api/app/guides/content/suwon-hwaseong-day-trip.json
  - apps/api/app/guides/content/takayama-shirakawago-day-trip.json
  - apps/api/app/guides/content/tokyo-5-day-itinerary.json
  - apps/api/app/guides/content/tokyo-disney-guide.json
  - apps/api/app/guides/content/tokyo-transit-passes.json
  - apps/api/app/guides/content/tokyo-where-to-stay.json
  - apps/api/app/guides/content/yokohama-day-trip-from-tokyo.json
---

# AIO: 68 how-to descriptions enumerate topics instead of answering

## Why

`description` is what an AI answer engine quotes when it summarizes a page, and 68 of the
site's descriptions assert nothing it can lift.

Measured across all 498 localized documents: 72 descriptions are a single sentence containing
three or more `、` separators — a noun-phrase list with no predicate — and 60 of those are
`howto`, plus 8 `intel`. `seoul-subway-t-money-guide`'s 235-character description enumerates
「計費方式、30 分鐘免費轉乘規則、T-money 在哪裡買、怎麼儲值與退款」 and states no fact.

These are the fare-and-timetable pages where the site has its highest-value numbers and its
densest citations (howto carries a median of 19 sources), so they are exactly the pages losing
the extraction. The fix is cheap because the answer is already one block below: every document
opens with a paragraph, and the howto first paragraphs are already answer-first.

## Definition of done

- [ ] Each rewritten description opens with a one-sentence answer carrying the number, then the
      enumeration, then the provenance clause these descriptions already use.
- [ ] No fact is introduced that the article body does not already state and source.

## Steps

- [ ] Select the targets by the measured rule: splits into exactly one sentence on
      `/(?<=[。.])/` **and** contains at least three `、`. That is the 60 howto + 8 intel.
- [ ] Rewrite by hand, lifting the lead from the document's own first paragraph.
- [ ] Split the work by kind or destination so one task does not hold all of
      `apps/api/app/guides/content` — several models work the same queue.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py
```

Spot-check that the new first sentence matches a number the body states and a source backs.

## Notes

**Do not automate the rewrite.** A generated first sentence that states a fare wrongly is the
one failure mode worse than a teaser: it is the sentence an answer engine caches and repeats.

Changing `description` changes both the meta description and the JSON-LD `description`, so this
is a live SEO change on 68 pages, not a silent one. The facts being promoted — fares, minutes —
are also the most perishable content on the site.

### 2026-09-19 split (claude-fable-5-1)

Re-measured with the ticket's rule on 2026-09-19: 72 howto/intel localized documents (64 howto, 8 intel;
the 35 life ones are a different shape — mostly the short ja descriptions of the codex series — and stay
out). This ticket now holds the 39 Japan/Korea documents listed in its scope; the other 33 (Southeast
Asia, Taiwan, Hong Kong/Macau/Singapore, USJ) are `2026-09-19-aio-answer-first-descriptions-part-2`, so
two writers can work at once and neither holds the whole content directory. Per-document current
descriptions were measured into a tab-separated list at the time; re-run the rule rather than trusting it.
