---
id: 2026-09-26-review-evergreen-ai-pages-after-claude
title: Review evergreen AI pages after Claude Opus 5.5 and GPT-6 Sol/Luna (2026-09-22/23)
status: done
priority: P2
area: docs
owner: claude-opus-5-5-evergreen-ai-pages
claimed_at: 2026-10-05T06:14:12Z
created_at: 2026-09-26T14:06:22Z
completed_at: 2026-10-05T07:37:47Z
branch: claude/evergreen-ai-pages
depends_on: []
scope:
  - apps/api/app/guides/content/ai-hype-vs-reality-2026.json
  - apps/api/app/guides/content/ai-benchmarks-explained.json
  - apps/api/app/guides/content/ai-search-llmo.json
  - apps/api/app/guides/content/ai-subscription-which-to-pay-2026.json
  - apps/api/app/guides/content/claude-api-first-call.json
  - apps/api/app/guides/content/claude-api-prompt-caching-cost.json
  - apps/api/app/guides/content/claude-beginner-guide.json
  - apps/api/app/guides/content/claude-extended-thinking-guide.json
  - apps/api/app/guides/content/claude-for-translation-zh-tw.json
  - apps/api/app/guides/content/claude-in-chrome-browser-agent.json
  - apps/api/app/guides/content/claude-model-lineup-2026.json
  - apps/api/app/guides/content/claude-plans-free-pro-max-2026.json
  - apps/api/app/guides/content/ai-video-tools-compared.json
  - apps/web/public/guides/claude-model-lineup-2026/diagram-1.svg
  - apps/web/public/guides/claude-beginner-guide/diagram-1.svg
  - apps/web/public/guides/claude-extended-thinking-guide/diagram-1.svg
  - apps/web/public/guides/claude-api-first-call/diagram-1.svg
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

- [x] Every page in scope is either confirmed correct as written (historical mention) or updated
      with the new model, price and check date from the official pages read that day.
- [x] Pages left unchanged are listed in the notes with the reason.

## Steps

- [x] For each page, find the model and price sentences and decide: current-line-up claim or history.
- [x] Update the current-line-up claims from the official pages (the batch 4.8 research records
      list them: `docs/ai-news-2026-09-late/research/ai-news-claude-opus-55-20260922.json`,
      `docs/ai-news-2026-09-late/research/ai-news-gpt-6-sol-luna-20260923.json`).
- [x] `pack_cli lint --kind <kind> --slug ...` for every edited page.

## How to verify

No page in scope names Opus 5 or GPT-5.6 Sol/Luna as the newest model or quotes their old list
prices as current.

## Notes

- Sonnet 5.5 and Haiku 5.5 were announced as "coming weeks" on 2026-09-22; recheck before writing.
  (2026-10-05: Sonnet 5.5 shipped on 2026-09-28; Haiku 5.5 was still "coming weeks" and not on
  anthropic.com/news.)
- The pricing page's plan table is series-level ("Opus"), not version-specific.
- `ai-video-tools-compared` was added for Google Vids: since 2026-09-23 any Google account can make
  AI clips in Vids at no cost on desktop (research record `docs/ai-news-2026-09-late/research/ai-news-google-vids-omni-free-20260924.json`;
  the two help pages disagree on the free quota).
- **Split (2026-10-05, claude-opus-5-5-evergreen-ai-pages).** The work was too large for one PR, so
  this ticket finished the Claude-side pages and the Vids note, and the scope was narrowed to them.
  The 14 OpenAI and cross-vendor pages (ai-coding-cost-tokens-explained, ai-free-vs-paid-plans-2026,
  ai-model-release-timeline-2026, ai-model-tiers-explained, chatgpt-beginner-guide,
  chatgpt-canvas-writing, chatgpt-plans-plus-pro-2026, chatgpt-team-for-small-business,
  claude-vs-chatgpt-writing-test, openrouter-multi-model-api, ai-api-pricing-comparison-2026,
  ai-model-comparison-table-2026, ai-pricing-beyond-list-price, ai-tools-2026-overview) and their six
  stale diagrams moved to `2026-10-05-review-the-openai-and-cross-vendor`, which records the
  OpenAI facts read today and the judgment traps. The ticked boxes above cover the narrowed scope only.
- Updated (every changed fact re-read on 2026-10-05 on the vendor's own page; those sources' `checked_on`
  bumped):
  - claude-model-lineup-2026: line-up is now Fable 5.1, Opus 5.5 ($4/$20, released 09-22, thinking
    always on, default effort medium), Sonnet 5.5 ($2/$10, released 09-28, thinking can't be turned
    off in the Claude apps), Haiku 4.5; Opus 5 and Sonnet 5 listed as legacy; Haiku 5.5 "coming weeks";
    cache read 10% / Opus 5.5 5% / Fable 5.1 2.5%; Sonnet 4.5 deprecated 09-30 (retires 11-30,
    replacement Sonnet 5.5); retirement commitments; Enterprise $20/seat + API usage; fallback
    models for Opus 5.5. The "default model per plan" claim was dropped: the Opus 5.5 and Sonnet 5.5
    announcements no longer say which model each plan defaults to, so the page now tells readers to
    look at the model name next to the send button. Daily advice changed from "use the default" to
    "start with Sonnet 5.5". The Sonnet 5 promo-price note was dropped as less relevant now that
    Sonnet 5 is legacy (pricing footnote 3 still says its $2/$10 price is standard and the $3/$15
    increase will not happen); the paragraph compares Opus 5.5 and Sonnet 5.5 with their
    predecessors instead. The 1M ≈ 555k-word / 200K ≈ 150k-word conversion stays: the models overview
    still gives it (re-read 2026-10-05). Sources trimmed to the 20-item limit.
  - Review round (2026-10-05, PR #1263): the legacy list no longer names Sonnet 4.5 (the overview's
    "Legacy models (still available)" line lists Fable 5, Opus 5, Opus 4.8, 4.7, 4.6, 4.5, Sonnet 5
    and Sonnet 4.6; model-deprecations shows Sonnet 4.5 as Deprecated, which the page says
    separately). "點數按標準 API 價格計費" was taken out of the Fable paragraph: its only source,
    "Manage usage credits for paid Claude plans" (12429409, still live and still saying so), had
    been cut for the 20-source limit, and each of the 20 remaining sources backs a claim no other
    source on the list carries. The plans comparison page (claude-plans-free-pro-max-2026) still
    states the API-rate billing with that source, and the lineup page links to it.
  - Review round, check dates: pages whose body now carries 10-05 facts say so next to their
    original check date instead of claiming one date for everything — claude-api-first-call
    (description, intro, table caption), claude-api-prompt-caching-cost (description and intro;
    its diagram names no model and its multipliers did not change, so the diagram keeps 9/14),
    claude-extended-thinking-guide (description, intro, diagram caption, diagram description, and
    the SVG title and `<desc>`; the task table keeps 9/13 because no row carries a model or effort
    fact), ai-search-llmo (intro), ai-subscription-which-to-pay-2026 (description, intro, closing
    paragraph; only the Claude facts were re-read, ChatGPT and Gemini keep 9/15) and
    ai-video-tools-compared (description, intro, comparison-table caption).
  - claude-plans-free-pro-max-2026, claude-beginner-guide, claude-for-translation-zh-tw,
    ai-subscription-which-to-pay-2026: paid-plan context windows (Opus 5.5, Sonnet 5.5 1M; Fable 5
    now listed at 500K). ai-subscription also: the pricing table now says "Up to 1M varies by
    model", and Max is monthly-only (the page said both Pro and Max had annual billing).
  - claude-beginner-guide, claude-extended-thinking-guide: thinking can't be turned off for
    Sonnet 5.5, Opus 5.5, Fable 5.1 and Opus 5 in the Claude apps; effort selector list (Opus 4.8
    is no longer in it); each model's recommended effort is marked "Default" instead of "High is
    the default"; Max advice now says start from the model's default.
  - claude-api-first-call: `claude-opus-5-5` in the Python and curl samples (the official
    quickstart uses it), prices, the 1,000-in/1,000-out example (0.024 USD), current model IDs.
  - claude-api-prompt-caching-cost: Opus 5.5 cache read 0.05x, minimum cacheable length
    (512 tokens for Opus 5.5, Sonnet 5.5, Opus 5, Fable 5.1), worked example on Sonnet 5.5
    (same prices as Sonnet 5, so the table numbers are unchanged).
  - ai-search-llmo: Opus 5.5 knowledge and training cutoffs (Jun 2026); GPT-6 Astra Apr 30, 2026
    re-checked.
  - ai-video-tools-compared: new paragraph and link to the Vids news article (free Omni 1.1 clips
    on desktop since 2026-09-23, quotas left to the news piece because the pack was at 20 sources).
    To make room, the OpenAI deprecations-page source was replaced by the Sora 2 model page, which
    now says the Sora 2 models and Videos API shut down on 2026-09-24 with no one-to-one replacement.
  - Four diagrams were outside the original scope and are added to it: their text and `<desc>` were
    updated with the pages (lineup, beginner, extended thinking, first call), rendered with Edge and
    checked by eye.
- Unchanged, with reasons:
  - ai-hype-vs-reality-2026: every Opus 5 and GPT-5.6 Sol figure is attributed to a named system
    card (Opus 5, GPT-6 Astra) and is still what that card says; it does not call Opus 5 the newest.
  - ai-benchmarks-explained: the Opus 5 mention is a dated example of a launch-page footnote
    (2026-07-24) and the Arena date is "as of the check day".
  - claude-in-chrome-browser-agent: the Opus 4.5 / Opus 5 / Sonnet 5 attack-success numbers are
    measured results from a dated Anthropic report, not a line-up claim; its diagram repeats them.
- Not fixed here (pre-existing, flagged by `intake_check.py`, unrelated to the model update):
  these older life pages have no summary block, some tables have 5 or 6 columns, and most use
  本文/這篇 more than once. The edit removed one 這篇 from claude-model-lineup-2026 and added none.
- Fetching tip: `help.openai.com` answers `curl -sSL` with the editorial User-Agent but returns 403
  to Node's `fetch`; `support.claude.com/en/articles/11049762-choose-a-claude-plan` is now a 404
  (replaced by the Max plan article in claude-model-lineup-2026). On platform.claude.com, stripping
  the HTML loses the footnote bullets under the comparison table (word conversion, cache-read
  rates) and the "Legacy models (still available)" line; append `.md` to the page URL
  (`.../docs/en/models/overview.md`) and read the Markdown, which has them. That is the likely reason
  the word conversion was first judged gone.
