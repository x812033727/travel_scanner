---
id: 2026-10-03-ai-news-index-month-range
title: AI news index: title and month range now that October articles exist
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-03T19:27:31Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - docs/news-2026-batch-4/update_index.py
---

# AI news index: title and month range now that October articles exist

## Why

`ai-news-2026-january-september-index` now carries an October group (batch 4.11 added `2026 年 10 月新聞解析`), but its title, description and opening sentence still say January to September in all five locales. The slug never changes (`docs/article-architecture.md`), and retitling rewrites the frozen link text of every pack that points at the index (about 30 packs, see `docs/news-2026-batch-4/ai.md`), so it is a change of its own.

## Definition of done

- [ ] Decide the wording that stays true as months are added (for example a title without a month range), apply it in five locales with `update_index.py retitle`, and rewrite every `article` inline whose slug is the index.
- [ ] `check_article.py --full` passes for every AI article that links to the index.

## Steps

- [ ] Count the packs that link to the index (walk the JSON, not a regex).
- [ ] Pick the title with the owner; update `update_index.py`'s edit tables and run `--dry-run` first.
- [ ] One PR with the index and the relinked packs; publish them in one `guides-import --slug` run.

## How to verify

`update_index.py ai --dry-run`, `check_article.py <slug> --full` over the linking packs, `pack_cli lint --kind life`.

## Notes

- Filed by batch 4.11 (`docs/news-2026-batch-4/agents/DELTA-4-11.md` §7).
