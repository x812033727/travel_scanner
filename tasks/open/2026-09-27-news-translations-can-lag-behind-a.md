---
id: 2026-09-27-news-translations-can-lag-behind-a
title: News translations can lag behind a zh-TW changed by the final edit
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-27T09:42:29Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/pipeline.py
---

# News translations can lag behind a zh-TW changed by the final edit

## Why

In the 2026-09-27 review of held drafts, all four translations of
`ai-news-google-project-suncatcher-20260924` differed from the saved zh-TW in the same way.
They had a three-item summary where zh-TW has four; the missing item is the energy case,
"up to eight times the solar power". They also carried a longer callout with an unsupported
"not yet independently verified" line, and ja, ko and zh-CN framed a table as "Google's three
major challenges". The reviewer concluded that they were translated from an earlier zh-TW
draft. Other drafts showed smaller one-sided differences, for example a zh-TW sentence
missing from en.

The second stage translates first, then runs `final-edit-<locale>` on each locale
separately (#763). If the final edit changes zh-TW, nothing carries that change into the
other four locales. Their locale reviews compare them with the zh-TW they were translated
from, not with the zh-TW that is saved.

## Definition of done

- [ ] After a final edit changes zh-TW, the saved translations are made from, or reviewed
      against, the final zh-TW.
- [ ] A test in which the final edit changes a zh-TW fact shows that the saved en carries the
      change, or that the candidate stops for review.

## Steps

- [ ] Confirm the mechanism on `ai-news-google-project-suncatcher-20260924`: its pipeline runs
      and the zh-TW revision history.
- [ ] Choose the fix: final-edit zh-TW before translating, re-translate the changed parts, or
      run the locale review against the final zh-TW.
- [ ] Test.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py -q
```

## Notes

- The reviewer's report is summarised in the ticket
  `2026-09-27-news-evidence-excerpts-stop-at-8`. Both come from the same review.
