---
id: 2026-09-28-google-vids-quota-recheck
title: Recheck the Google Vids free quota in the Vids news article: the 6-clip figure is labelled Workspace Individual
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T04:30:56Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-news-google-vids-omni-free-20260924.json
---

# Recheck the Google Vids free quota in the Vids news article: the 6-clip figure is labelled Workspace Individual

## Why

`ai-news-google-vids-omni-free-20260924` (checked 2026-09-26) says a personal Google account gets 6 AI short videos a month, combined with AI avatars, and 50 credits. On 2026-09-28 the usage page (support.google.com/docs/answer/15609411) showed, in its static HTML, "6 video clips/month combined with AI avatars" and "50 credits per month" under **Google Workspace Individual**, with a general default of "Up to 500 video clip seconds per month". The page switches tables per account type (Work, School, Google AI Pro, Personal) with script, so the Personal tab could not be read without a browser. The article may have applied the Workspace Individual numbers to personal accounts.

## Definition of done

- [ ] Someone opens the usage page in a browser, clicks each account-type tab, and records the AI video clip limit for Personal.
- [ ] The article's quota paragraph and FAQ say exactly what the page says per account type, in all its published locales.

## Steps

- [ ] Browser check of the Personal, Google AI Pro, Work and School tabs.
- [ ] Correct the zh-TW text and any localized copies through content-pipeline.

## How to verify

The article's quota numbers match the tab they come from on the official page, with the account type named.

## Notes

- Found while fact-checking the video `docs/videos/google-vids-free-ai-video-omni-1-1` (see its `claims.md`); the video now lists each page's figure with its account type and does not state a personal-account number.
