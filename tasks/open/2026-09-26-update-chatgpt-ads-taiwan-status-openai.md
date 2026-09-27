---
id: 2026-09-26-update-chatgpt-ads-taiwan-status-openai
title: Update ChatGPT ads Taiwan status: OpenAI opened ads in Taiwan on 2026-09-23
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-26T14:06:20Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/chatgpt-ads-status.json
  - apps/api/app/guides/content/ai-news-chatgpt-sponsored-agents-20260916.json
  - apps/api/app/guides/content/ai-news-chatgpt-ads-20260505.json
---

# Update ChatGPT ads Taiwan status: OpenAI opened ads in Taiwan on 2026-09-23

## Why

OpenAI announced on 2026-09-23 (Taipei) that ChatGPT ads begin rolling out in Taiwan and six
Southeast Asian markets, and its Help Center "Ads Manager availability" table marks Taiwan as
Available for self-serve Ads Manager (checked 2026-09-26). Three pages on the site still say the
opposite or leave it open, and batch 4.8 publishes `ai-news-chatgpt-ads-taiwan-20260923`, so the
site would carry both statements at once:

- `chatgpt-ads-status` (zh-TW only) says Taiwan is not on the self-serve list.
- `ai-news-chatgpt-sponsored-agents-20260916` (five locales) has "Taiwan not listed" in its title
  area, checked 2026-09-18.
- `ai-news-chatgpt-ads-20260505` (five locales) says the article has no answer on Taiwan.

## Definition of done

- [ ] The evergreen page states Taiwan's current status with the 2026-09-23 announcement and the
      Help Center table as sources, and a new check date.
- [ ] The two dated news articles keep their original reporting but carry a dated update line
      (all five locales) pointing at the new article, instead of being rewritten.

## Steps

- [ ] Re-read the announcement and the Help Center table on the day (both are live pages).
- [ ] Edit the three packs; five locales for the two news articles.
- [ ] `pack_cli lint --kind life --slug ...`, `check_article.py` where the slug is in `RELATED`.

## How to verify

The three pages no longer contradict `ai-news-chatgpt-ads-taiwan-20260923` in any locale.

## Notes

- Research record with the verified wording: `docs/ai-news-2026-09-late/research/ai-news-chatgpt-ads-taiwan-20260923.json`
  (Go is a paid plan and does get ads; the zh-Hant Help Center page mistranslates who can opt out).
- Do this after batch 4.8 is published, so the update line can link the new article.
