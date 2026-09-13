---
id: 2026-09-13-launch-articles-batch-3-twenty-taiwan
title: Launch articles batch 3: twenty Taiwan guides in en, ja, ko and zh-CN
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-13T04:45:54Z
created_at: 2026-09-13T04:45:23Z
completed_at:
branch:
depends_on: []
scope:
  - docs/travel-guides.md
---

# Launch articles batch 3: twenty Taiwan guides in en, ja, ko and zh-CN

## Why

The first thirty articles are zh-TW guides for Taiwanese readers going abroad. The owner
asked for twenty guides about visiting Taiwan for the site's other four locales: Japanese
and Korean visitors (Taiwan's two largest inbound markets after Hong Kong), English readers,
and Simplified Chinese readers. One pack per article carries all four locales, so a single
research pass, hero, diagram and photo set serves four audiences; the text is written for
each audience (entry rules, payment habits and language support differ), not translated.

## Definition of done

- [ ] Twenty packs under `apps/api/app/guides/content/`, each with `locales.en`, `.ja`, `.ko`
      and `.zh-CN`, a hero photo, a self-drawn SVG diagram (Traditional Chinese + English
      labels, so one file serves every locale), a table, a callout, sources with `checked_on`
      and partner blocks per `docs/travel-guides.md`; the packaged-content test passes.
- [ ] Photographs from Wikimedia Commons only (CC0 / PD / CC BY / CC BY-SA), licence read
      from the Commons API; every number on a diagram appears in the article text.
- [ ] Facts checked on official pages on the day of writing; audience-specific rules
      (visa-free days, arrival card, payment) verified per locale, anything unverified
      written as "check the official site".

## Steps

The twenty (slug · kind · destination · topics):

1. `taoyuan-airport-to-taipei` · howto · taipei · transport, budget
2. `taipei-metro-easycard-guide` · howto · taipei · transport, budget
3. `taipei-4-day-itinerary` · howto · taipei · itinerary, culture, food
4. `taipei-where-to-stay` · howto · taipei · hotel, budget
5. `jiufen-shifen-yehliu-day-trip` · howto · taipei · itinerary, nature, transport
6. `taipei-night-markets-guide` · howto · taipei · food, culture, nightlife
7. `taipei-hot-springs-beitou-wulai` · howto · taipei · nature, culture, season
8. `taipei-viewpoints-101-elephant-mountain` · howto · taipei · viewpoint, itinerary
9. `taiwan-entry-2026-arrival-card` · intel (2026-12-31) · none · entry
10. `taiwan-esim-sim-wifi` · howto · none · connectivity, packing
11. `taiwan-hsr-tra-ticket-guide` · howto · none · transport, budget
12. `taiwan-payment-easycard-cash-cards` · howto · none · budget, shopping
13. `taiwan-food-guide-must-eat` · howto · none · food, culture
14. `taiwan-convenience-store-guide` · howto · none · shopping, budget
15. `taiwan-tax-refund-shopping-2026` · howto · none · shopping, budget
16. `taiwan-etiquette-safety-tips` · howto · none · etiquette, safety
17. `taichung-sun-moon-lake-2-day` · howto · taichung · itinerary, nature, transport
18. `kaohsiung-3-day-itinerary` · howto · kaohsiung · itinerary, culture, food
19. `tainan-2-day-itinerary` · howto · tainan · itinerary, food, culture
20. `taiwan-winter-events-2026-2027` · intel (2027-03-15) · none · season, culture

- [ ] Ten writing agents, two articles each, from `article_brief_v3.md`: one meta file,
      one document per locale, a Commons manifest and the SVG per article.
- [ ] `ingest_pack3.py <slug>` per article: assemble the pack from the locale files, validate,
      copy the SVG, fetch and licence-check photos, write sizes and credits, save.
- [ ] Review diagrams (numbers vs text, labels >= 15 px), run the packaged-content test,
      commit, open the PR, merge when green, deploy, `guides-import --publish`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.cli guides-import --actor-email <admin> --dry-run
```

## Notes

- Approved offers today: taipei transport and activities. Taichung, Kaohsiung and Tainan
  carry offer blocks that render nothing until the back office approves an offer for that
  city; hotel and connectivity modules likewise.
- Hualien / Taroko is not a catalog destination, so it is not in this batch; a Taroko
  article would need the post-2024-earthquake reopening status verified first.
