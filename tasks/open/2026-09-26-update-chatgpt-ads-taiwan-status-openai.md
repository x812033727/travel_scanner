---
id: 2026-09-26-update-chatgpt-ads-taiwan-status-openai
title: Update ChatGPT ads Taiwan status: OpenAI opened ads in Taiwan on 2026-09-23
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-chatgpt-ads-tw
claimed_at: 2026-10-02T18:51:19Z
created_at: 2026-09-26T14:06:20Z
completed_at:
branch: claude/chatgpt-ads-taiwan-status
depends_on: []
scope:
  - apps/api/app/guides/content/chatgpt-ads-status.json
  - apps/api/app/guides/content/ai-news-chatgpt-sponsored-agents-20260916.json
  - apps/api/app/guides/content/ai-news-chatgpt-ads-20260505.json
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - docs/ai-news-2026-09-late/research/ai-news-chatgpt-sponsored-agents-20260916.json
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

- [x] The evergreen page states Taiwan's current status with the 2026-09-23 announcement and the
      Help Center table as sources, and a new check date.
- [x] The two dated news articles keep their original reporting but carry a dated update line
      (all five locales) pointing at the new article, instead of being rewritten.

## Steps

- [x] Re-read the announcement and the Help Center table on the day (both are live pages).
- [x] Edit the three packs; five locales for the two news articles.
- [x] `pack_cli lint --kind life --slug ...`, `check_article.py` where the slug is in `RELATED`.

## How to verify

The three pages no longer contradict `ai-news-chatgpt-ads-taiwan-20260923` in any locale.

## Notes

- Research record with the verified wording: `docs/ai-news-2026-09-late/research/ai-news-chatgpt-ads-taiwan-20260923.json`
  (Go is a paid plan and does get ads; the zh-Hant Help Center page mistranslates who can opt out).
- Do this after batch 4.8 is published, so the update line can link the new article.
- 2026-10-03 (claude-opus-5-5-chatgpt-ads-tw): re-read with curl (HTTP 200 each) the 9/23
  announcement (dated September 23, 2026; "Starting today, ChatGPT Ads will begin rolling out
  across ... Taiwan"; ads only on Free and Go, Plus/Pro/Enterprise ad-free; self-serve Ads
  Manager "for eligible businesses"; no mention of Sponsored Agents), Ads Manager Availability
  (updatedAt 2026-09-25T21:12Z, "Taiwan Available", legal entity that advertises and is billed
  must be in an available country) and Ads in ChatGPT (updatedAt 2026-09-28T19:13Z; Free and Go
  may see ads, Plus/Pro/Business/Enterprise/Edu none, under-18 accounts none; Settings > Ad
  Controls: turn off personalization (contextual ads remain), hide ads, see why, clear ads data;
  Ads-Free is a Free-plan option). The ticket's claim holds. The new article is live (zh-TW and
  en `/life/ai-news-chatgpt-ads-taiwan-20260923` return 200), so the update lines link it.
- Evergreen `chatgpt-ads-status`: PR #1017 (task `2026-09-25-chatgpt-ads-status-article-says-taiwan`)
  had already rewritten it for Taiwan with the 9/23 announcement and the Help Center table as
  sources, checked 2026-09-30, but production still serves the 9/14 version (not imported yet).
  This change only re-checks it: all six sources re-read today (Europe 8/31 update, May CPC and
  pixel, ad policy v1.6 "Updated: September 10, 2026" with the interface-imitation rule, plus
  the three above) and every "9 月 30 日" check date and `checked_on` moved to 2026-10-03.
- News packs: update lines in place, not rewrites. Sponsored Agents: block 16 (the status
  paragraph) loses its "check the page's date" sentence and gains a dated update with a link to
  the new article (now a `rich_paragraph`); summary sentence 2, description, the FAQ "台灣看得到
  這些廣告嗎？" answer and the callout carry the update; every update says the 9/23 announcement
  does not mention Sponsored Agents (re-read today: still "tested with select advertisers in the
  United States"). May article: block 16's "台灣是否已開放，本文沒有答案" becomes a dated
  pointer to the new article, the FAQ "台灣的廣告主現在能不能用這個工具？" answer and the callout
  carry the update (self-serve: Help Center table lists Taiwan, entity-location rule). All five
  locales, same blocks.
- Title: the Sponsored Agents headline said 台灣未列入開放名單 in all five locales, which no
  update line can fix, so it now reads 美國測試中，只限特定廣告主 (and the four translations).
  That pulled two files into scope: the AI index links the article with its old title as link
  text (five locales), and `check_article.py` requires the research record's `title` to equal
  the zh-TW title (record also gets a `corrections_applied` line describing this update).
  `check:tasks` warns that those two paths overlap `2026-09-16-news-batch-4-4-the-8` (claimed
  2026-09-23, PR #672 merged) and `2026-09-30-news-batch-4-9-gpt-6` / `-4-10-claude-sonnet`
  (status review, PR #1041 merged 2026-09-30, branch gone): all stale claims whose work landed,
  and no open PR touches the index or the record, so they were left alone.
- Not done on purpose: no source added to the two news packs. `check_article.py` requires every
  source's `checked_on` to equal the record's (2026-09-18) and caps sources at four (the May pack
  already has four); the linked article carries the 9/23 sources. The Sponsored Agents diagram
  still draws "官方清單上沒有台灣" with "查核日 2026 年 9 月 18 日" printed on it; it sits right
  under the updated paragraph, so it was left as dated artwork rather than redrawn in five locales.
- zh-TW body length is at the batch cap (`check_article.py` 1800–3000): Sponsored Agents 2999,
  May 3000, which is why the zh-TW update lines are short. Any further edit there must trim.
- Checks: `check_article.py --full` OK for both packs and for the new article; `pack_cli lint
  --kind life --slug` for the four changed packs: 0 errors, warnings unchanged from origin/main
  (text_length on en/ja/ko, no_summary on the evergreen and the index); `intake_check.py
  --from-content`: same pre-existing failures as origin/main (first block not summary,
  self-reference count, two-attribution paragraph, ja diagram '4'), self-reference counts one
  lower; `pytest tests/test_guides_content_pack.py` and four neighbouring guides tests green.
- Publishing is the owner's step after merge and deploy: `guides-import --slug` for
  `chatgpt-ads-status` (zh-TW), the two news slugs and `ai-news-2026-january-september-index`
  (five locales).
