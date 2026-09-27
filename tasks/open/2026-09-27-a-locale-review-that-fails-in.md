---
id: 2026-09-27-a-locale-review-that-fails-in
title: A locale review that fails in round two reports on its own discarded correction
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-27T14:14:26Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_pipeline.py
---

# A locale review that fails in round two reports on its own discarded correction

## Why

The locale review runs two rounds per locale (pipeline.py:864-936):

1. Round 1 reviews the saved translation. If the reviewer returns `revise` with a
   `corrected_document`, that correction replaces the translation, and nothing is stored.
2. Round 2 reviews the correction. If round 2 does not pass, the pipeline stores a `manual`
   assessment with round 2's issues, and the candidate is held with `news_locale_review_failed`.
   The correction is not saved.

So the editor's queue shows issues found in text that no longer exists. The issues round 1 found
in the saved draft, the text the editor actually has to fix, are lost.

This happened on 2026-09-27, when 11 held drafts were fixed by the issues on `/admin/news`:

- `ai-news-gemini-3-8-tts-20260923`, ja: the stored issues are four typos, such as 脆本 for 脚本,
  仲組み for 仕組み and 金銘 for 金銭. None of them is in the saved ja draft. The round-1 reviewer's
  own correction introduced them, round 2 flagged them, and the correction was thrown away.
- `ai-news-anthropic-claude-enzyme-system-art-20260923`, en: the stored issue is a "(translated
  from Chinese)" note in the Feng Zhang quote. The saved en draft has no such note.
- In the other drafts, the stored issues overlapped the saved text only where the correction
  had left a passage unchanged.

The editor cannot tell which issues are real, and a fix made from them cannot pass.

## Definition of done

- [ ] When a locale is held, the issues the editor sees describe the saved draft of that
      locale. Store round 1's issues on the saved text, or say clearly which issues belong to
      the discarded correction.
- [ ] A test in which round 1 revises and round 2 fails shows the round-1 issues on the held
      candidate.

## Steps

- [ ] Store a `revise` assessment for round 1 with its issues and `details.round = 1`. Mark
      round 2's `manual` assessment as reviewing the correction, for example with
      `details.reviewed = "correction"`. Alternatively, save the correction as the held draft
      so that round 2's issues match the text the editor sees.
- [ ] Show the round-1 issues in the review queue (`/admin/news`) when round 2 fails.
- [ ] Test in tests/test_news_pipeline.py.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py -q
```

## Notes

- A related cause of these held drafts is
  `2026-09-27-news-translations-can-lag-behind-a`. The final edit rewrites each locale
  separately after the locale reviews pass. On a later re-check, the locale review then
  compares drifted translations with zh-TW.
  - On 2026-09-27, checkers found 2 to 19 further departures from zh-TW in each held zh-CN
    draft, beyond the stored issues.
  - The drafts were aligned with zh-TW block by block before the next re-check.
- Round 1's correction model also introduces errors of its own, such as the ja look-alike
  kanji above. That is worth watching once round 1's issues are visible.
