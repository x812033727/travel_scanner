---
id: 2026-09-30-cover-every-major-ai-agent-company
title: Cover every major AI agent company and the big tech companies with official news sources
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T11:31:53Z
created_at: 2026-09-30T11:31:52Z
completed_at:
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - apps/api/app/news_automation/sources.json
  - docs/news-automation.md
---

# Cover every major AI agent company and the big tech companies with official news sources

## Why

The owner asked on 2026-09-30 that every major AI agent company and the big tech companies
be covered. `sources.json` has OpenAI, Anthropic, Google, Microsoft, NVIDIA, Apple, Meta, AWS,
GitHub, Cloudflare and Hugging Face, but none of xAI, Mistral, DeepSeek, Qwen, Kimi, Perplexity,
Cursor, TSMC, Samsung, Intel, AMD, Qualcomm, MediaTek and others.

## Definition of done

- [ ] Every company on the list tested through the scanner's own parsers (listing, dates,
      two articles, robots.txt); results in the notes, readable or not and why.
- [ ] The readable ones added to `sources.json` with notes and a small `max_entries_per_scan`
      for HTML listings.
- [ ] Loaded on the host with `sources_cli` after the deploy.
