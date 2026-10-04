---
id: 2026-10-03-news-automation-claude-blog-source
title: News automation: add claude.com/blog as a source
status: review
priority: P2
area: api
owner: claude-fable-5-1-news-blog
claimed_at: 2026-10-04T00:51:41Z
created_at: 2026-10-03T19:27:30Z
completed_at:
branch: claude/news-claude-blog-source
depends_on: []
scope:
  - apps/api/tests/test_news_automation.py
---

# News automation: add claude.com/blog as a source

## Why

The hourly news automation reads Anthropic's `/news/` and the model pages, not `claude.com/blog`. Product announcements such as Claude Code mods (2026-10-01) and "Build plugins for Claude" (2026-09-25) were missed and had to be hand-written (batches 4.8, 4.11).

## Definition of done

- [x] `claude.com/blog` is a source of the hourly automation: it already is, in `sources.json` ("Claude blog", HTML listing, `/blog/` prefix). What was missing is the host step: the source has never been loaded with `sources_cli`, which ticket `2026-09-30-cover-every-major-ai-agent-company` tracks as its open item. A test now pins what the shipped config reads from the page.
- [ ] Loaded on the host with `sources_cli` (owner or a host session; this container has no host access).

## Steps

- [x] Check whether `claude.com/blog` has an RSS or Atom feed: none (`/blog/rss.xml`, `/blog/feed`, `/blog/feed.xml`, `/rss.xml`, `/blog/atom.xml` are 404, `/feed` is 403; the page has only hreflang alternates). The listing is read as HTML.
- [x] The source needs no code change; `test_claude_blog_listing_yields_one_undated_entry_per_card` reads a card in the page's Webflow markup with the shipped config.
- [ ] On the host: `docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.sources_cli` (dry run), then `--apply --actor-email <admin>`. The first scan records every listed post as seen (`news_baseline`), the mods post included, because the cards carry no `<time>` and undated entries are baselined; so do not expect it in `/admin/news` as a duplicate. The next new post on the listing becomes a candidate.

## How to verify

`uv run pytest tests -k news_automation`; after deploy, the admin news queue.

## Notes

- Filed by batch 4.11 (`docs/news-2026-batch-4/agents/DELTA-4-11.md` §7).
- 2026-10-04: the premise was wrong. `sources.json` already carries "Claude blog" with `include_path_prefixes: ["/blog/"]`;
  run against the live page (saved 2026-10-04, 804,982 bytes) the shipped config yields 15 entries, the mods post first,
  all undated. Dates do exist on the page (a hidden `fs-list-field="date"` div, "October 1, 2026", and a visible
  "Oct 1, 2026" caption) but the listing parser only reads anchors, so the 72-hour window cannot apply to this source;
  reading those divs would be a per-publisher date extractor, which `docs/news-automation.md` chose not to build.
  If the owner wants dated entries here, that is a parser change worth its own ticket.
- Scope narrowed to the test file; the earlier ticket keeps the host step.
