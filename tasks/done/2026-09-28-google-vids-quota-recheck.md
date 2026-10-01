---
id: 2026-09-28-google-vids-quota-recheck
title: Recheck the Google Vids free quota in the Vids news article: the 6-clip figure is labelled Workspace Individual
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-30T15:50:05Z
created_at: 2026-09-28T04:30:56Z
completed_at: 2026-09-30T15:53:43Z
branch: claude/vids-quota-recheck
depends_on: []
scope:
  - apps/api/app/guides/content/ai-news-google-vids-omni-free-20260924.json
---

# Recheck the Google Vids free quota in the Vids news article: the 6-clip figure is labelled Workspace Individual

## Why

`ai-news-google-vids-omni-free-20260924` (checked 2026-09-26) says a personal Google account gets 6 AI short videos a month, combined with AI avatars, and 50 credits. On 2026-09-28 the usage page (support.google.com/docs/answer/15609411) showed, in its static HTML, "6 video clips/month combined with AI avatars" and "50 credits per month" under **Google Workspace Individual**, with a general default of "Up to 500 video clip seconds per month". The page switches tables per account type (Work, School, Google AI Pro, Personal) with script, so the Personal tab could not be read without a browser. The article may have applied the Workspace Individual numbers to personal accounts.

## Definition of done

- [x] Someone opens the usage page in a browser, clicks each account-type tab, and records the AI video clip limit for Personal.
- [x] The article's quota paragraph and FAQ say exactly what the page says per account type, in all its published locales.

## Steps

- [x] Browser check of the Personal, Google AI Pro, Work and School tabs.
- [x] Correct the zh-TW text and any localized copies through content-pipeline.

## How to verify

The article's quota numbers match the tab they come from on the official page, with the account type named.

## Notes

- Found while fact-checking the video `docs/videos/google-vids-free-ai-video-omni-1-1` (see its `claims.md`); the video now lists each page's figure with its account type and does not state a personal-account number.
- 2026-09-30 (claude-opus-5-5): read both pages in a browser. The usage page
  (answer/15609411) has one table per account type, and the **Personal Google Account**
  table does say "6 video clips/month combined with AI avatars" and 50 credits; so do
  Google AI Plus and Workspace Individual. The article's personal figure was right.
  Seconds-based plans: AI Pro 500, Ultra 5x 2,500, Ultra 20x 10,000; Business/Enterprise
  Starter 200, Standard/Plus 500; AI Expanded Access 2,000; the page default is 500.
  answer/16143507 still says "Most users can generate up to 50 videos per month".
  The article's seconds paragraph now names each plan's figure in five locales, the
  disagreement paragraph carries both check dates, and those two sources say
  checked_on 2026-09-30. The diagram's quota card ("two pages disagree") still holds.
