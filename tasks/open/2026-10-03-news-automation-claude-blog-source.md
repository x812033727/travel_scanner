---
id: 2026-10-03-news-automation-claude-blog-source
title: News automation: add claude.com/blog as a source
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-03T19:27:30Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation
---

# News automation: add claude.com/blog as a source

## Why

The hourly news automation reads Anthropic's `/news/` and the model pages, not `claude.com/blog`. Product announcements such as Claude Code mods (2026-10-01) and "Build plugins for Claude" (2026-09-25) were missed and had to be hand-written (batches 4.8, 4.11).

## Definition of done

- [ ] `claude.com/blog` is a source of the hourly automation (listing page or feed, whichever the site offers; the batch 4.8 candidate list notes the listing page is 200 with dated cards), with the duplicate check against hand-written packs working.

## Steps

- [ ] Check whether `claude.com/blog` has an RSS or Atom feed; otherwise parse the listing page's cards.
- [ ] Add the source in `apps/api/app/news_automation` the way the Anthropic root-page prefix fix of batch 4.10 was done; test with a fixture.
- [ ] After deploy, confirm in `/admin/news` that the first scan lists the mods post as a duplicate of `ai-news-claude-code-mods-20261001`.

## How to verify

`uv run pytest tests -k news_automation`; after deploy, the admin news queue.

## Notes

- Filed by batch 4.11 (`docs/news-2026-batch-4/agents/DELTA-4-11.md` §7).
