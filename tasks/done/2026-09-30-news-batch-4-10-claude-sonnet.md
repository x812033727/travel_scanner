---
id: 2026-09-30-news-batch-4-10-claude-sonnet
title: News batch 4.10: Claude Sonnet 5.5, five languages (the scanner never saw Anthropic's root-level launch pages)
status: done
priority: P1
area: docs
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T11:29:56Z
created_at: 2026-09-30T11:29:56Z
completed_at: 2026-10-04T11:50:06Z
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

- [x] `ai-news-claude-sonnet-55-20260928` in five locales from Anthropic's own pages, two fact-check rounds, translated and
      reviewed per language, with a diagram; AI index links it in five locales.
- [x] PR merged; deploy and `guides-import --slug` publish done by someone with host access.

## Steps

- [x] DELTA-4-10.md and `RELATED`
- [x] Research record (opus)
- [x] zh-TW draft (sonnet)
- [x] Fact check round 1 and round 2 (opus, different agents)
- [x] Translate en/ja/ko/zh-CN (sonnet), per-language review
- [x] Assets, index, checks

## Notes

- Done 2026-09-30, details in `docs/news-2026-batch-4/HANDOVER.md` §1j. `check_article.py --full --assets`
  OK; lint no errors (en 9,370 and ja 6,083 characters are length warnings the spec allows). Left:
  deploy, re-read the live pages, then `guides-import --slug ai-news-claude-sonnet-55-20260928` with
  the index, dry run first.
- Published 2026-10-04 11:47Z on the owner's instruction: `ai-news-claude-sonnet-55-20260928` in five locales (pg_dump `/root/travel_scanner_preimport_20261004_114710.dump`), links rebuilt, the index links resolve, re-run dry run all unchanged. The facts were not re-checked against the vendor pages on publish day.
