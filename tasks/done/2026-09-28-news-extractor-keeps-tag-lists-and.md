---
id: 2026-09-28-news-extractor-keeps-tag-lists-and
title: News extractor keeps tag lists and navigation instead of the story, so first-party posts are rejected
status: done
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-28T04:48:35Z
created_at: 2026-09-28T04:48:20Z
completed_at: 2026-09-28T05:04:47Z
branch: claude/ai-hourly-news-efficiency-b1c0d2
depends_on: []
scope:
  - apps/api/app/news_automation/feeds.py
  - apps/api/app/news_automation/validation.py
  - apps/api/app/news_automation/sources.json
  - apps/api/tests/test_news_automation.py
---

# News extractor keeps tag lists and navigation instead of the story, so first-party posts are rejected

## Why

The owner said on 2026-09-28 that the hourly AI news publishes too little. A read-only look at
production that morning (04:25Z) showed the news worker was mostly idle, so throughput was
not the limit. Of the candidates created in the previous 48 hours, 63 were rejected as
`news_not_eligible`. For Cloudflare, Chainalysis and SEC the writer's reason was the same
every time: the evidence excerpt held only the blog's tag list or site navigation, so there
was nothing to write from.

`feeds._ArticleParser` caused it:

- `handle_startendtag` calls `handle_endtag`, and end tags pop the capture by depth without
  checking the name. On SEC pages the first `<... />` inside `<main>` ended the capture
  after the side navigation (248 characters).
- Nothing was skipped inside the region. Cloudflare's `<article>` starts with a list of every
  tag on the blog, which filled the whole 8,000-character excerpt. On Meta Newsroom and the
  Ethereum Foundation blog the captured text was an inline `<style>` block.
- Chainalysis puts the story in `div.single-post__content`, outside `<article>` and `<main>`.
  Those hold only the related-post cards (302 characters).

## Definition of done

- [x] Cloudflare, SEC, Meta, Ethereum Foundation and Chainalysis pages extract the story body.
- [x] No enabled source extracts less of its story than before (compared on each source's
      latest post).
- [x] A candidate stored before the fix is not held as `source_content_changed` at publish just
      because the extractor changed. A real edit still fails closed.

## Steps

- [x] Rewrite `_ArticleParser`: a name-aware stack of open elements, self-closing tags that do
      not end the region, and skipped subtrees (script, style, noscript, template, svg,
      iframe, nav, aside, footer, form, button, select), plus per-source `exclude_tags`,
      `exclude_ids` and `exclude_classes`.
- [x] Keep the old parser as `_LegacyArticleParser` (`extract_article(..., legacy=True)`), and
      let `validation.revalidate_evidence` accept a stored hash that matches it.
- [x] `sources.json`: Chainalysis `article_tags: []`, `article_classes: ["single-post__content"]`.
- [x] Tests.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py -q
```

After deploy, on the host:

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.sources_cli
```

Chainalysis should show `action: update`. Then apply it with `--apply --actor-email`.

## Notes

- This covers step 1 of `2026-09-27-news-evidence-hashes-page-chrome-so`, the extractor. That
  task's body-only hash column is still open. Skipping scripts removes TechCrunch's JW Player
  id and nav/aside rails, which should already cut much of the churn it describes. The
  Verge's "Most Popular" rail and CoinDesk's "Latest Crypto News" list are not in
  nav/aside, so they may still churn.
- Candidates already rejected as `news_not_eligible` because of empty excerpts are not rerun
  here. Rerunning costs model calls and is the owner's decision.
- The 2026-09-28 per-source comparison: Meta went from 40,000 characters of CSS to 7,144 of
  story, and Ethereum Foundation from CSS to 1,549. Cloudflare went from 20,688 characters,
  mostly tags, to 6,536 starting at the story. SEC went from 248 to 2,438 and DeepMind from
  9,909 to 4,678. Anthropic, CFTC and Microsoft Research were unchanged, and the rest lost
  only share buttons, scripts and rails.
