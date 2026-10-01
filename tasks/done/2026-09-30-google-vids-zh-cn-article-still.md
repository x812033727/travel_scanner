---
id: 2026-09-30-google-vids-zh-cn-article-still
title: Google Vids zh-CN article still says the official pages give no age limit or Chinese-prompt answer
status: done
priority: P3
area: docs
owner: claude-opus-5-5-vids-article
claimed_at: 2026-10-01T04:02:24Z
created_at: 2026-09-30T14:15:20Z
completed_at: 2026-10-01T04:14:54Z
branch: claude/google-vids-article-age-language
depends_on: []
scope:
  - apps/api/app/guides/content/ai-news-google-vids-omni-free-20260924.json
---

# Google Vids zh-CN article still says the official pages give no age limit or Chinese-prompt answer

## Why

The site article `ai-news-google-vids-omni-free-20260924` (zh-CN version, and possibly the other locales) says Google's official pages give no age limit and do not say whether Chinese prompts work. The 2026-09-30 fact-check of the Google Vids video (`docs/videos/google-vids-free-ai-video-omni-1-1/verify-1.md`, `verify-2.md`, claims c7 and c8) found both answers on Google's own pages: the generation help page links to answer 13952129, whose first requirement is "Be 18 or over", and the supported-languages page (answer 14925782) says English is the only supported language for the other Workspace with Gemini features, with no row for AI video generation.

## Definition of done

- [x] Every locale of the article states the 18+ requirement and the English-only language support, each with its official source, re-read on the day of the edit.
- [x] The article's other quota figures still match the video's verified ones (50 videos a month for most users on the generation page; 6 clips a month shared with avatars for personal accounts on the usage page; the 500-second default).

## Steps

- [x] Re-open both Google help pages and confirm the wording.
- [x] Edit the article through the content pipeline (`content-pipeline` skill). Publishing per locale on the production site is a separate, owner-approved step after merge and deploy (`guides-import --slug ai-news-google-vids-omni-free-20260924` per locale, dry-run first); it was not done here.

## How to verify

Open the article in each locale on the live site and find the age and language sentences with their source links.

## Notes

- Found by the zh-CN caption reviewer of the Google Vids video on 2026-09-30.
- 2026-10-01 (claude-opus-5-5-vids-article): fetched with curl (editorial User-Agent,
  `?hl=en`, all HTTP 200). answer/13952129 "Get started with Google Workspace with
  Gemini": the first item under "What you need to use Google Workspace with Gemini" is
  "Be 18 or over." answer/16143507 (generation page) links it as "Learn about Gemini
  features and plans" and links answer/14925782 for languages. answer/14925782
  "Supported languages for Google Workspace with Gemini": the Vids rows are image
  generation, AI voiceovers, AI avatars and Slides to Vids, no AI video generation;
  the page ends "For other Google Workspace with Gemini features, English is the only
  supported language" and says to set the Google Account language to English.
  answer/15609411 still says "Many AI features in Vids are only available in English at
  this time." Quotas unchanged: 16143507 "Most users can generate up to 50 videos per
  month"; 15609411 personal "6 video clips/month combined with AI avatars", default
  "Up to 500 video clip seconds per month".
- Changed, in all five locales: the description, summary item 4, the language-and-age
  paragraph (block 16) and the Chinese-prompt FAQ answer. They now say, attributed to
  Google's pages, that users must be 18 or over and that AI video generation is not on
  the language list, so only English is officially supported and Chinese prompts are
  outside it. Two sources added per locale (13952129, 14925782, checked_on 2026-10-01).
  PR #1052's quota wording is untouched. The phrasing says "not officially supported",
  not "does not work": the page lists supported languages, it does not say other prompts
  fail. The en summary item was shortened to fit the 300-character limit.
- Not changed: the voiceover "Coming soon" sentences, which the video fact-check found
  out of date (Workspace Updates 2026-09-29); filed as
  2026-10-01-google-vids-article-still-calls-the.
- Checks: `pack_cli lint --slug` only the existing en/ja length warnings (present on
  origin/main too); `intake_check.py --from-content` fails only "first block is not
  summary", which is the article's existing structure.
