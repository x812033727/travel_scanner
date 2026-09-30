---
id: 2026-09-30-news-batch-4-9-gpt-6
title: News batch 4.9: GPT-6.1 Sol, five languages (hourly automation did not publish it)
status: review
priority: P1
area: docs
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T10:18:55Z
created_at: 2026-09-30T10:18:52Z
completed_at:
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - docs/news-2026-batch-4/agents/DELTA-4-9.md
  - docs/news-2026-batch-4/check_article.py
  - docs/news-2026-batch-4/build_assets.py
  - docs/news-2026-batch-4/update_index.py
  - docs/news-2026-batch-4/HANDOVER.md
  - docs/news-2026-batch-4/translation-corrections.json
  - docs/news-2026-batch-4/factcheck-draft
  - docs/ai-news-2026-09-late/research
  - docs/ai-news-2026-09-late/manifest.json
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - apps/api/app/guides/content/ai-news-gpt-61-sol-20260929.json
  - apps/web/public/guides/ai-news-gpt-61-sol-20260929
  - apps/web/public/guides/ai-news-2026-january-september-index
---

# News batch 4.9: GPT-6.1 Sol, five languages (hourly automation did not publish it)

## Why

OpenAI published "Introducing GPT-6.1 Sol" on 2026-09-29 10:00Z (Taipei 18:00), in the
`openai.com/news/rss.xml` feed the hourly news automation scans. Other Chinese-language sites
had it the same day; Mokaair did not publish it (as of 2026-09-30 it is not in the sitemap),
although the automation published other 9/29 stories. From outside the host we cannot see
which gate held the candidate (likely the duplicate check against
`ai-news-gpt-6-sol-luna-20260923`, a zh-TW draft waiting for the owner's confirmation, a
final-edit/Jev hold, or the 8,000-character evidence cap on a long system card). The owner
asked for a hand-written five-language article, the way batch 4.8 did it.

## Definition of done

- [x] `ai-news-gpt-61-sol-20260929` in five locales, researched from OpenAI's own pages only,
      two fact-check rounds, translated and reviewed per language, with a diagram.
- [x] AI index links to it in five locales.
- [ ] PR merged; deploy and `guides-import --slug` publish done by someone with host access.

## Steps

- [x] DELTA-4-9.md
- [x] Research record (opus)
- [x] zh-TW draft (sonnet)
- [x] Fact check round 1 and round 2 (opus, different agents)
- [x] Translate en/ja/ko/zh-CN (sonnet), per-language review
- [x] Assets, index, `check_article.py --full --assets`, lint, pytest
- [x] PR

## How to verify

`check_article.py ai-news-gpt-61-sol-20260929 --full --assets` zero FAIL;
`python -m app.guides.pack_cli lint --kind life` clean; after publish, `verify_public.py`.

## Notes

- Follow-up (not this scope): find the Sol candidate in `/admin/news` and record which gate
  held it; if the duplicate check treats a new version of a model family as a duplicate,
  file an api task for Jev's duplicate prompt.
- Done 2026-09-30: research 45/45 quotes verified; round 1 131 claims, 10 facts changed; round 2 74
  claims, 9 changes; review adopted en 0, ja 2, ko 3, zh-CN 0. `check_article.py --full --assets` OK,
  `pack_cli lint --kind life` no errors (en body 9,211 characters is a warning the spec allows).
  Details in `docs/news-2026-batch-4/HANDOVER.md` §1i. Left: deploy, re-read the live pages, then
  `guides-import --slug ai-news-gpt-61-sol-20260929 --slug ai-news-2026-january-september-index`
  dry run and publish on the host.
