---
id: 2026-09-19-aio-answer-first-descriptions-part-2
title: AIO: answer-first descriptions, part 2 — 東南亞、台灣、港澳新加坡的 how-to 與 intel（33 份文件）
status: in-progress
priority: P3
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:16:15Z
created_at: 2026-09-19T11:14:27Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/guides/content/bangkok-4-day-itinerary.json
  - apps/api/app/guides/content/bangkok-airport-to-city.json
  - apps/api/app/guides/content/bangkok-bts-mrt-boat-guide.json
  - apps/api/app/guides/content/bangkok-where-to-stay.json
  - apps/api/app/guides/content/chiang-mai-3-day-itinerary.json
  - apps/api/app/guides/content/da-nang-hoi-an-4-day-itinerary.json
  - apps/api/app/guides/content/hanoi-4-day-itinerary.json
  - apps/api/app/guides/content/ho-chi-minh-city-4-day-itinerary.json
  - apps/api/app/guides/content/hong-kong-4-day-itinerary.json
  - apps/api/app/guides/content/jiufen-shifen-yehliu-day-trip.json
  - apps/api/app/guides/content/kaohsiung-3-day-itinerary.json
  - apps/api/app/guides/content/krabi-ao-nang-railay-4-islands.json
  - apps/api/app/guides/content/macau-day-trip-from-hong-kong.json
  - apps/api/app/guides/content/sentosa-day-guide.json
  - apps/api/app/guides/content/singapore-4-day-itinerary.json
  - apps/api/app/guides/content/tainan-2-day-itinerary.json
  - apps/api/app/guides/content/taipei-metro-easycard-guide.json
  - apps/api/app/guides/content/taipei-night-markets-guide.json
  - apps/api/app/guides/content/taipei-viewpoints-101-elephant-mountain.json
  - apps/api/app/guides/content/taipei-where-to-stay.json
  - apps/api/app/guides/content/taiwan-entry-2026-arrival-card.json
  - apps/api/app/guides/content/taiwan-esim-sim-wifi.json
  - apps/api/app/guides/content/taiwan-etiquette-safety-tips.json
  - apps/api/app/guides/content/taiwan-food-guide-must-eat.json
  - apps/api/app/guides/content/taiwan-payment-easycard-cash-cards.json
  - apps/api/app/guides/content/taiwan-tax-refund-shopping-2026.json
  - apps/api/app/guides/content/taoyuan-airport-to-taipei.json
  - apps/api/app/guides/content/thailand-entry-2026-tdac.json
  - apps/api/app/guides/content/thailand-esim-sim-wifi.json
  - apps/api/app/guides/content/usj-guide.json
  - apps/api/app/guides/content/vietnam-money-sim-grab-guide.json
---

# AIO: answer-first descriptions, part 2 — 東南亞、台灣、港澳新加坡的 how-to 與 intel（33 份文件）

## Why

Part 2 of `2026-09-14-answer-first-howto-descriptions` (read it first: the measured rule, the reason,
and the one prohibition — **do not automate the rewrite**). That ticket keeps the 39 Japan/Korea
documents; this one holds the other 33 localized documents (Southeast Asia, Taiwan, Hong Kong, Macau,
Singapore, USJ) so that two writers can work at once and neither holds all of
`apps/api/app/guides/content`.

A `description` is what an answer engine quotes. These 33 are a single sentence with three or more
「、」 and no predicate — a list of topics that asserts nothing — on exactly the fare-and-timetable
pages whose numbers are the site's best-sourced.

## Definition of done

- [ ] Each of the 33 descriptions opens with a one-sentence answer carrying a number or fact the
      article's own first paragraph states, then the enumeration, then the provenance clause these
      descriptions already use; 120–200 characters where the original was in that range.
- [ ] No fact is introduced that the article body does not already state and source; the lead is
      lifted from the document's first paragraph, not invented.
- [ ] The description is changed in the listed locale only (most are zh-TW; two are zh-CN — write each
      in its own locale from its own body); titles, blocks, images and sources untouched.
- [ ] `uv run pytest tests/test_guides_content_pack.py -q` green; `pack_cli lint --kind howto` and
      `--kind intel` show no new error.

## Steps

- [ ] Select the targets by the rule (one sentence on `/(?<=[。.])/` and ≥3 「、」) restricted to the
      files in scope; expect 33 (31 files: `taiwan-entry-2026-arrival-card` and `thailand-entry-2026-tdac`
      carry two locales each, or re-count).
- [ ] Rewrite by hand, one document at a time, reading its first paragraph first.
- [ ] Spot-check five at random: the new first sentence's number appears in the body and a source backs it.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
cd apps/api && uv run python -m app.guides.pack_cli lint --kind howto && uv run python -m app.guides.pack_cli lint --kind intel
```

After merge and deploy the owner imports the 31 packs with `guides-import --dry-run` then `--publish`
(`--slug` per pack).

## Notes

- Filed 2026-09-19 by claude-fable-5-1 when splitting the parent ticket; three of these packs
  (bangkok-4-day-itinerary, chiang-mai-3-day-itinerary, da-nang-hoi-an-4-day-itinerary) and
  sentosa-day-guide are also held by review tickets of the same owner whose code is merged; a claim
  refused for that reason may be taken with `--force`.
