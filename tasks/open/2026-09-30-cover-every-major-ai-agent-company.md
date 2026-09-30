---
id: 2026-09-30-cover-every-major-ai-agent-company
title: Cover every major AI agent company and the big tech companies with official news sources
status: review
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
  - apps/api/app/news_automation/scanner.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_news_evidence.py
  - docs/news-automation.md
---

# Cover every major AI agent company and the big tech companies with official news sources

## Why

The owner asked on 2026-09-30 that every major AI agent company and the big tech companies
be covered. `sources.json` has OpenAI, Anthropic, Google, Microsoft, NVIDIA, Apple, Meta, AWS,
GitHub, Cloudflare and Hugging Face, but none of xAI, Mistral, DeepSeek, Qwen, Kimi, Perplexity,
Cursor, TSMC, Samsung, Intel, AMD, Qualcomm, MediaTek and others.

## Definition of done

- [x] Every company on the list tested through the scanner's own parsers (listing, dates,
      two articles, robots.txt); results in the notes, readable or not and why.
- [x] The readable ones added to `sources.json` with notes and a small `max_entries_per_scan`
      for HTML listings.
- [ ] Loaded on the host with `sources_cli` after the deploy.
- 2026-09-30 survey (44 entries, a sonnet agent through the scanner's parsers, then rechecked by
  the coordinator; full table in the PR discussion, raw results were in `/root/news49/survey/`).
  **Added (15):** Mistral, Cohere, Cursor, Cognition, Replit, Manus, Amazon (AI titles only),
  Stability AI, ElevenLabs, Intel, AMD, MediaTek, Dell, Lenovo, ASUS.
  **Readable but not added:** Moonshot/Kimi, SK hynix, IBM answer 404 for robots.txt, which
  `SafeNewsFetcher` treats as "not permitted"; SK hynix pages also extract to a 1,502-character
  template. Foxconn reset the connection.
  **Blocked (403, mostly Cloudflare):** xAI, Perplexity, TSMC, Micron, Windows blog, Microsoft
  Copilot, Samsung Newsroom, Sony, Tesla, Oracle, Acer.
  **SPA or nothing to extract:** Qwen, Meta AI, Runway, Midjourney, Qualcomm, HP, Arm, Zhipu.
  **No listing:** DeepSeek (single API-docs pages), ASML (connection reset). Gemini and Android
  are covered by blog.google.
  Blocked ones get `news_page_refused` leads only if their feed is readable; most of them block
  the listing too, so they stay uncovered. Recheck the 403s from the host.
- Also added: a first-scan baseline in `scanner.py` (entries older than 72 hours or undated are
  recorded as seen, not drafted), so these sources do not draft their back catalogue. HTML blog
  listings keep the default 20 entries per scan because several pin older posts first.
