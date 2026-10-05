---
id: 2026-10-05-review-the-openai-and-cross-vendor
title: Review the OpenAI and cross-vendor evergreen AI pages after GPT-6 Sol/Luna, GPT-6.1 Sol and Claude 5.5
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-05T07:33:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-coding-cost-tokens-explained.json
  - apps/api/app/guides/content/ai-free-vs-paid-plans-2026.json
  - apps/api/app/guides/content/ai-model-release-timeline-2026.json
  - apps/api/app/guides/content/ai-model-tiers-explained.json
  - apps/api/app/guides/content/chatgpt-beginner-guide.json
  - apps/api/app/guides/content/chatgpt-canvas-writing.json
  - apps/api/app/guides/content/chatgpt-plans-plus-pro-2026.json
  - apps/api/app/guides/content/chatgpt-team-for-small-business.json
  - apps/api/app/guides/content/claude-vs-chatgpt-writing-test.json
  - apps/api/app/guides/content/openrouter-multi-model-api.json
  - apps/api/app/guides/content/ai-api-pricing-comparison-2026.json
  - apps/api/app/guides/content/ai-model-comparison-table-2026.json
  - apps/api/app/guides/content/ai-pricing-beyond-list-price.json
  - apps/api/app/guides/content/ai-tools-2026-overview.json
  - apps/web/public/guides/ai-free-vs-paid-plans-2026/diagram-1.svg
  - apps/web/public/guides/ai-model-release-timeline-2026/diagram-1.svg
  - apps/web/public/guides/ai-model-tiers-explained/diagram-1.svg
  - apps/web/public/guides/chatgpt-beginner-guide/diagram-1.svg
  - apps/web/public/guides/chatgpt-plans-plus-pro-2026/diagram-1.svg
  - apps/web/public/guides/ai-api-pricing-comparison-2026/diagram-1.svg
---

# Review the OpenAI and cross-vendor evergreen AI pages after GPT-6 Sol/Luna, GPT-6.1 Sol and Claude 5.5

## Why

Split from `2026-09-26-review-evergreen-ai-pages-after-claude`, which updated the Claude-only pages
(and the Google Vids note) for Claude Opus 5.5 (2026-09-22) and Sonnet 5.5 (2026-09-28). These
14 zh-TW life pages still quote the old line-ups: GPT-5.6 Sol/Terra/Luna as OpenAI's current API
models with their old prices, Claude Opus 5 ($5/$25) and Sonnet 5 as Anthropic's current models,
and `anthropic/claude-sonnet-5` in code samples. Since the original ticket was filed, OpenAI also
shipped GPT-6.1 Sol (2026-09-29) and plans to retire GPT-5.5 from ChatGPT on 2026-10-14, so the
OpenAI half needs its own careful pass. Each hit needs a judgment, not a search and replace:
several are dated history, and ChatGPT **Chat** still runs the GPT-5.6 models (see Notes).

## Definition of done

- [ ] Every page in scope is either confirmed correct as written (historical or Chat-only mention)
      or updated with the new model, price and check date from the official pages read that day.
- [ ] Diagrams in scope that show an old line-up or price are redrawn, with `image.description`
      kept a verbatim copy of the SVG `<desc>`, and every diagram number present in the text.
- [ ] Pages left unchanged are listed in the notes with the reason.

## Steps

- [ ] For each page, find the model and price sentences (OpenAI, Anthropic and any other vendor in
      the same table) and decide: current-line-up claim, Chat-only claim, or history.
- [ ] Re-read the official pages that day (list in Notes) and update the current claims, including
      title, description, tables, computed examples and price ranges, and each source's `checked_on`.
- [ ] Redraw the stale diagrams; render them (`pack_cli lint --render-dir`, `CHROMIUM_BIN` = Edge)
      and look at the PNGs.
- [ ] `pack_cli lint --kind life --slug ...` and `intake_check.py --slug ... --from-content` for
      every edited page; `pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py`.

## How to verify

`git diff origin/main -- apps/api/app/guides/content | grep -nE "Opus 5[^.]|Sonnet 5[^.]|GPT-5\.6|gpt-5\.6"`
and check by hand that every remaining hit is history or an explicitly Chat-scoped statement; no
page names Opus 5, Sonnet 5 or GPT-5.6 Sol/Luna as the newest API model or quotes their old list
prices as current.

## Notes

- Split from 2026-09-26-review-evergreen-ai-pages-after-claude (PR on branch
  `claude/evergreen-ai-pages`). That PR already updated: claude-model-lineup-2026,
  claude-plans-free-pro-max-2026, claude-beginner-guide, claude-extended-thinking-guide,
  claude-api-first-call, claude-api-prompt-caching-cost, claude-for-translation-zh-tw,
  ai-subscription-which-to-pay-2026, ai-search-llmo, ai-video-tools-compared. Reuse its Claude
  wording for the Claude rows here.
- Official facts read on 2026-10-05 (re-read them on the day you edit):
  - developers.openai.com/api/docs/pricing, Flagship "Standard" table, short context per 1M tokens:
    gpt-6-astra 10.00 / cached 1.00 / cache write 12.50 / output 50.00; gpt-6.1-sol 2.00 / 0.10 /
    2.50 / 10.00; gpt-6-luna 0.10 / 0.01 / 0.125 / 0.50. gpt-5.6-sol now sits in the "Cyber models"
    table at 4.00 / 0.40 / 5.00 / 20.00, and the page still says its promotional pricing lasts "at
    least through November 21, 2026". gpt-5.6-terra and gpt-5.6-luna are no longer in the visible
    Flagship table (check the "All models" expansion before writing anything about them).
  - developers.openai.com/api/docs/models: Astra, GPT-6.1 Sol and GPT-6 Luna cards; knowledge
    cutoff Apr 30, 2026 (Astra, 6.1 Sol) and May 18, 2026 (Luna); 1.05M context, 128K output.
  - learn.chatgpt.com/docs/models: GPT-6.1 Sol, GPT-6 Sol and GPT-6 Luna are in ChatGPT Work and
    Codex, "They aren't available in Chat"; GPT-5.6 Sol, Terra and Luna "remain available during
    the rollout"; GPT-5.5 retires from ChatGPT, Work and Codex on 2026-10-14.
  - learn.chatgpt.com/docs/pricing: Free and Go get GPT-6 Luna at Standard speed in the desktop
    app (subject to rollout); Plus gets GPT-6.1 Sol and GPT-6 Luna.
  - Anthropic: models overview lists Fable 5.1 ($10/$50), Opus 5.5 ($4/$20, cache read $0.20),
    Sonnet 5.5 ($2/$10), Haiku 4.5 ($1/$5); Opus 5 and Sonnet 5 are legacy. Haiku 5.5 was still
    "coming weeks" (not on anthropic.com/news on 2026-10-05).
- Judgment traps: ChatGPT Chat still runs GPT-5.6 Luna (Free/Go) and GPT-5.6 Sol (Plus+) per
  learn.chatgpt.com, so "Free uses GPT-5.6 Luna in Chat" may still be right; chatgpt-plans-plus-pro-2026
  was rewritten on 2026-09-30 (#1029) and already separates Chat from Work/Codex, so it may need
  only small changes. Do not call GPT-5.6 Sol "旗艦" where the page means the API line-up.
  ai-model-release-timeline-2026 ends at early September and needs entries for Opus 5.5 (09-22),
  GPT-6 Sol/Luna (09-22/23), Sonnet 5.5 (09-28) and GPT-6.1 Sol (09-29) if it keeps claiming to
  cover the year so far. The price-comparison pages (ai-api-pricing-comparison-2026,
  ai-model-comparison-table-2026, ai-pricing-beyond-list-price) mix Gemini, Qwen and MiniMax rows:
  re-check those vendors too before bumping any check date, and recompute every derived range and
  worked example. openrouter-multi-model-api quotes the OpenRouter model page for
  `anthropic/claude-sonnet-5`; check what OpenRouter lists that day before changing the code.
- Fetching: `help.openai.com` answers 200 to `curl -sSL` with the editorial User-Agent but 403 to
  Node's `fetch`; `chatgpt.com/pricing` and `openai.com/index/*` returned 403 on 2026-10-05 (do not
  use Wayback). Packs allow at most 20 sources per locale; several of these pages are already at 20.
- Research records: `docs/ai-news-2026-09-late/research/ai-news-gpt-6-sol-luna-20260923.json`,
  `ai-news-gpt-61-sol-20260929.json`, `ai-news-claude-opus-55-20260922.json`,
  `ai-news-claude-sonnet-55-20260928.json`.
