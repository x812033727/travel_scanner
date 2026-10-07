---
id: 2026-10-06-phuket-airport-smart-bus-child-fare
title: phuket-airport-transport-where-to-stay: Smart Bus child fare, under 6 years (Payment page) vs under 90 cm (2026-06-25 notice)
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-06T18:00:43Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/phuket-airport-transport-where-to-stay.json
---

# phuket-airport-transport-where-to-stay: Smart Bus child fare, under 6 years (Payment page) vs under 90 cm (2026-06-25 notice)

## Why

The live zh-TW article `phuket-airport-transport-where-to-stay` ends blocks[14] with
「未滿 6 歲由付費成人陪同免費，以官網為準。」 That is what the operator's Payment page says,
but the operator published a newer rule that uses height instead of age, and the article does
not mention it. A parent with a child under 6 who is 90 cm or taller would expect a free ride,
but under the newer rule the child pays.

Two official Phuket Smart Bus pages, both HTTP 200 on 2026-10-06:

- `https://www.phuketsmartbus.com/payment`, under the fare table: "Children under 6 ride free
  with a paying adult."
- `https://www.phuketsmartbus.com/blog/children-under-90-cm-ride-for-free`, dated June 25, 2026:
  "Children under 90 cm in height can travel free of charge", "Children must be accompanied by a
  parent or guardian during the journey", "Bus staff may measure a child's height if necessary to
  verify eligibility", and "Height is the determining factor, regardless of age."

Batch 8's README rule for two conflicting official sources asks that the article disclose the
other version in one sentence. Found by the independent round-2 fact-check of PR #1335 (batch 8
wave 2, FOLLOWUPS row 7); that PR does not touch the live article.

## Definition of done

- [ ] On the day of the edit, both pages are re-read with the editorial User-Agent. blocks[14]
      then states what they say: one rule if the two pages agree by then, or both rules in one
      sentence if they still disagree.
- [ ] The Payment source title in `sources` names whichever rule the article now cites, and the
      blog post is added as a source when the article cites it. `checked_on` is the day of the edit.
- [ ] The corrected zh-TW pack is published with owner consent (`guides-import --slug
      phuket-airport-transport-where-to-stay --locale zh-TW`).

## Steps

- [ ] Re-open both pages (`curl -sSL --compressed -A 'Mokaair-editorial/1.0
      (https://mokaair.com; support@mokaair.com)'`, strip `<!-- -->`, check the status).
- [ ] If they still disagree, replace the last sentence of blocks[14] with wording such as
      「官網付款頁寫未滿 6 歲由付費成人陪同免費，2026 年 6 月的官方公告則改以身高未滿 90 公分為準，以現場為準。」
      Keep the reader-first rules: no verification narration and at most one attribution phrase.
- [ ] Add the blog post to `sources` (title such as 「Phuket Smart Bus：Children Under 90 cm Ride for
      FREE!（身高未滿 90 公分免費、須由家長陪同、可能現場量身高，2026-06-25）」) and update the
      Payment source title if needed.
- [ ] Search the other Phuket packs for a child-fare sentence before closing. On 2026-10-06 only
      this pack had one (`phuket-old-town-big-buddha-viewpoints` has none).

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug phuket-airport-transport-where-to-stay
uv run python ../../.agents/skills/content-pipeline/scripts/intake_check.py --slug phuket-airport-transport-where-to-stay --from-content
uv run pytest tests/test_guides_content_pack.py -q
```

## Notes

- The pack has only the zh-TW locale today, so there is nothing to re-translate.
- `tasks/open/2026-09-14-batch-6-guides-dated-maintenance.md` already schedules a general Smart
  Bus re-check of this article for 2027-01-16 (timetable, payment and pass pages). This ticket
  covers only the child-fare conflict, which exists today. Whoever does the January re-check can
  confirm this fix still holds.
- Round-2 record: `docs/travel-guides-batch-8/verify-1.md`, section "verify-2", error 3.
