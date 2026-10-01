---
id: 2026-09-30-google-vids-zh-cn-article-still
title: Google Vids zh-CN article still says the official pages give no age limit or Chinese-prompt answer
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-30T14:15:20Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-news-google-vids-omni-free-20260924.json
---

# Google Vids zh-CN article still says the official pages give no age limit or Chinese-prompt answer

## Why

The site article `ai-news-google-vids-omni-free-20260924` (zh-CN version, and possibly the other locales) says Google's official pages give no age limit and do not say whether Chinese prompts work. The 2026-09-30 fact-check of the Google Vids video (`docs/videos/google-vids-free-ai-video-omni-1-1/verify-1.md`, `verify-2.md`, claims c7 and c8) found both answers on Google's own pages: the generation help page links to answer 13952129, whose first requirement is "Be 18 or over", and the supported-languages page (answer 14925782) says English is the only supported language for the other Workspace with Gemini features, with no row for AI video generation.

## Definition of done

- [ ] Every locale of the article states the 18+ requirement and the English-only language support, each with its official source, re-read on the day of the edit.
- [ ] The article's other quota figures still match the video's verified ones (50 videos a month for most users on the generation page; 6 clips a month shared with avatars for personal accounts on the usage page; the 500-second default).

## Steps

- [ ] Re-open both Google help pages and confirm the wording.
- [ ] Edit the article through the content pipeline (`content-pipeline` skill) and publish per locale.

## How to verify

Open the article in each locale on the live site and find the age and language sentences with their source links.

## Notes

- Found by the zh-CN caption reviewer of the Google Vids video on 2026-09-30.
