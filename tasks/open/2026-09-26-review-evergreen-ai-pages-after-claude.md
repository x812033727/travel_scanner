---
id: 2026-09-26-review-evergreen-ai-pages-after-claude
title: Review evergreen AI pages after Claude Opus 5.5 and GPT-6 Sol/Luna (2026-09-22/23)
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-26T14:06:22Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-coding-cost-tokens-explained.json
  - apps/api/app/guides/content/ai-free-vs-paid-plans-2026.json
  - apps/api/app/guides/content/ai-hype-vs-reality-2026.json
  - apps/api/app/guides/content/ai-model-release-timeline-2026.json
  - apps/api/app/guides/content/ai-model-tiers-explained.json
  - apps/api/app/guides/content/chatgpt-beginner-guide.json
  - apps/api/app/guides/content/chatgpt-canvas-writing.json
  - apps/api/app/guides/content/chatgpt-plans-plus-pro-2026.json
  - apps/api/app/guides/content/chatgpt-team-for-small-business.json
  - apps/api/app/guides/content/claude-vs-chatgpt-writing-test.json
  - apps/api/app/guides/content/openrouter-multi-model-api.json
  - apps/api/app/guides/content/ai-api-pricing-comparison-2026.json
  - apps/api/app/guides/content/ai-benchmarks-explained.json
  - apps/api/app/guides/content/ai-model-comparison-table-2026.json
  - apps/api/app/guides/content/ai-pricing-beyond-list-price.json
  - apps/api/app/guides/content/ai-search-llmo.json
  - apps/api/app/guides/content/ai-subscription-which-to-pay-2026.json
  - apps/api/app/guides/content/ai-tools-2026-overview.json
  - apps/api/app/guides/content/claude-api-first-call.json
  - apps/api/app/guides/content/claude-api-prompt-caching-cost.json
  - apps/api/app/guides/content/claude-beginner-guide.json
  - apps/api/app/guides/content/claude-extended-thinking-guide.json
  - apps/api/app/guides/content/claude-for-translation-zh-tw.json
  - apps/api/app/guides/content/claude-in-chrome-browser-agent.json
  - apps/api/app/guides/content/claude-model-lineup-2026.json
  - apps/api/app/guides/content/claude-plans-free-pro-max-2026.json
  - apps/api/app/guides/content/ai-video-tools-compared.json
---

# Review evergreen AI pages after Claude Opus 5.5 and GPT-6 Sol/Luna (2026-09-22/23)

## Why

Anthropic released Claude Opus 5.5 on 2026-09-22 (list price $4/$20 per million tokens, cache
reads $0.20) and OpenAI released GPT-6 Sol and GPT-6 Luna on 2026-09-23 Taipei (GPT-5.6
promotional pricing continues to at least 11/21). Batch 4.8's research agents found evergreen
zh-TW guides that still present Opus 5 ($5/$25) or GPT-5.6 Sol/Luna as the current line-up,
for example `claude-model-lineup-2026`, `claude-plans-free-pro-max-2026`,
`chatgpt-plans-plus-pro-2026` and `ai-api-pricing-comparison-2026`.

The scope is a grep for "Opus 5" and "GPT-5.6 Sol/Luna" outside the news articles: many hits
are historical mentions that are still correct. Each page needs a judgment, not a search and
replace.

## Definition of done

- [ ] Every page in scope is either confirmed correct as written (historical mention) or updated
      with the new model, price and check date from the official pages read that day.
- [ ] Pages left unchanged are listed in the notes with the reason.

## Steps

- [ ] For each page, find the model and price sentences and decide: current-line-up claim or history.
- [ ] Update the current-line-up claims from the official pages (the batch 4.8 research records
      list them: `docs/ai-news-2026-09-late/research/ai-news-claude-opus-55-20260922.json`,
      `docs/ai-news-2026-09-late/research/ai-news-gpt-6-sol-luna-20260923.json`).
- [ ] `pack_cli lint --kind <kind> --slug ...` for every edited page.

## How to verify

No page in scope names Opus 5 or GPT-5.6 Sol/Luna as the newest model or quotes their old list
prices as current.

## Notes

- Sonnet 5.5 and Haiku 5.5 were announced as "coming weeks" on 2026-09-22; recheck before writing.
- The pricing page's plan table is series-level ("Opus"), not version-specific.
- `ai-video-tools-compared` was added for Google Vids: since 2026-09-23 any Google account can make
  AI clips in Vids at no cost on desktop (research record `docs/ai-news-2026-09-late/research/ai-news-google-vids-omni-free-20260924.json`;
  the two help pages disagree on the free quota).
