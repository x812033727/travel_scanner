---
id: 2026-09-30-news-batch-4-10-claude-sonnet
title: News batch 4.10: Claude Sonnet 5.5, five languages (the scanner never saw Anthropic's root-level launch pages)
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T11:29:56Z
created_at: 2026-09-30T11:29:56Z
completed_at:
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - docs/news-2026-batch-4/agents/DELTA-4-10.md
  - docs/news-2026-batch-4/check_article.py
  - docs/news-2026-batch-4/build_assets.py
  - docs/news-2026-batch-4/update_index.py
  - docs/news-2026-batch-4/HANDOVER.md
  - docs/news-2026-batch-4/translation-corrections.json
  - docs/news-2026-batch-4/factcheck-draft
  - docs/ai-news-2026-09-late/research
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - apps/api/app/guides/content/ai-news-claude-sonnet-55-20260928.json
  - apps/web/public/guides/ai-news-claude-sonnet-55-20260928
---

# News batch 4.10: Claude Sonnet 5.5, five languages (the scanner never saw Anthropic's root-level launch pages)

## Why

Anthropic launched Claude Sonnet 5.5 on 2026-09-28 (`https://www.anthropic.com/claude-sonnet-5-5`).
The hourly automation never saw it: the Anthropic source only took links under `/news/`, and
model launches live at the site root (fixed in the same PR). The owner asked on 2026-09-30 for a
hand-written five-language article, the way batch 4.9 did GPT-6.1 Sol.

## Definition of done

- [ ] `ai-news-claude-sonnet-55-20260928` in five locales from Anthropic's own pages, two fact-check rounds, translated and
      reviewed per language, with a diagram; AI index links it in five locales.
- [ ] PR merged; deploy and `guides-import --slug` publish done by someone with host access.

## Steps

- [ ] DELTA-4-10.md and `RELATED`
- [ ] Research record (opus)
- [ ] zh-TW draft (sonnet)
- [ ] Fact check round 1 and round 2 (opus, different agents)
- [ ] Translate en/ja/ko/zh-CN (sonnet), per-language review
- [ ] Assets, index, checks
