---
id: 2026-10-05-review-the-openai-and-cross-vendor
title: Review the OpenAI and cross-vendor evergreen AI pages after GPT-6 Sol/Luna, GPT-6.1 Sol and Claude 5.5
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-openai-evergreen-pages
claimed_at: 2026-10-05T13:36:14Z
created_at: 2026-10-05T07:33:00Z
completed_at:
branch: claude/openai-evergreen-pages
depends_on: []
scope:
  - apps/api/app/guides/content/ai-coding-cost-tokens-explained.json
  - apps/api/app/guides/content/ai-free-vs-paid-plans-2026.json
  - apps/api/app/guides/content/ai-model-tiers-explained.json
  - apps/api/app/guides/content/chatgpt-beginner-guide.json
  - apps/api/app/guides/content/chatgpt-canvas-writing.json
  - apps/api/app/guides/content/chatgpt-plans-plus-pro-2026.json
  - apps/api/app/guides/content/chatgpt-team-for-small-business.json
  - apps/api/app/guides/content/claude-vs-chatgpt-writing-test.json
  - apps/api/app/guides/content/openrouter-multi-model-api.json
  - apps/api/app/guides/content/ai-tools-2026-overview.json
  - apps/web/public/guides/ai-free-vs-paid-plans-2026/diagram-1.svg
  - apps/web/public/guides/ai-model-tiers-explained/diagram-1.svg
  - apps/web/public/guides/chatgpt-beginner-guide/diagram-1.svg
  - apps/web/public/guides/chatgpt-plans-plus-pro-2026/diagram-1.svg
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

- [x] Every page in scope is either confirmed correct as written (historical or Chat-only mention)
      or updated with the new model, price and check date from the official pages read that day.
- [x] Diagrams in scope that show an old line-up or price are redrawn, with `image.description`
      kept a verbatim copy of the SVG `<desc>`, and every diagram number present in the text.
- [x] Pages left unchanged are listed in the notes with the reason.

## Steps

- [x] For each page, find the model and price sentences (OpenAI, Anthropic and any other vendor in
      the same table) and decide: current-line-up claim, Chat-only claim, or history.
- [x] Re-read the official pages that day (list in Notes) and update the current claims, including
      title, description, tables, computed examples and price ranges, and each source's `checked_on`.
- [x] Redraw the stale diagrams; render them (`pack_cli lint --render-dir`, `CHROMIUM_BIN` = Edge)
      and look at the PNGs.
- [x] `pack_cli lint --kind life --slug ...` and `intake_check.py --slug ... --from-content` for
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
- **Split (2026-10-05, claude-opus-5-5-openai-evergreen-pages).** The three multi-vendor price pages
  (ai-api-pricing-comparison-2026, ai-model-comparison-table-2026, ai-pricing-beyond-list-price)
  and the release timeline (ai-model-release-timeline-2026), with their two diagrams, moved to
  `2026-10-05-multi-vendor-ai-price-pages-late`, and the scope above was narrowed to the ten pages
  this ticket finished. Reason: a correct update of those pages means re-reading eight to ten
  vendors' pricing pages on the same day and recomputing every range and worked example; two of
  them are generated by `docs/content-research/*/build_pack.py`; and the other vendors moved too
  (docs.x.ai now leads with grok-4.7, OpenRouter lists a Qwen3.8 Max Prime from 09-23). The
  timeline itself is correct as written: its title, description, intro and diagram all say it
  covers 1 January to 15 September. The ticked boxes above cover the narrowed scope only.
- Sources re-read on 2026-10-05 with `curl -sSL` and the editorial User-Agent (all HTTP 200;
  appending `.md` to a developers.openai.com, learn.chatgpt.com or platform.claude.com URL returns
  the Markdown with every table row): OpenAI API pricing, models and the gpt-6-astra, gpt-6.1-sol,
  gpt-6-luna model pages, reasoning and prompt-caching guides; learn.chatgpt.com models and pricing;
  help.openai.com "GPT-5.6 and GPT-6 Pro in ChatGPT", About ChatGPT Pro tiers, What is ChatGPT
  Go / Plus, Free tier FAQ, Multi-currency billing, Using Codex with your ChatGPT plan, Model
  release notes, Retiring GPT-4o; openai.com/index/introducing-chatgpt-go (200 this time);
  Anthropic models overview, pricing, choosing-a-model, thinking, prompt-caching; claude.com/pricing;
  support.claude.com "Claude Fable models on your plan"; Gemini API models, pricing, thinking;
  openrouter.ai quickstart, models doc, models page, Models API (text, `output_modalities=all`,
  `supported_parameters=tools`) and the claude-sonnet-5.5, gemini-3.8-flash and gpt-oss-20b pages.
- Updated (each changed fact's source `checked_on` bumped to 2026-10-05; sources that were not
  re-read keep their date):
  - ai-model-tiers-explained: OpenAI tiers are now the three featured models (GPT-6 Astra 10/50,
    GPT-6.1 Sol 2/10, GPT-6 Luna 0.10/0.50, all 1.05M context), GPT-5.6 kept as "still on the API,
    and what Chat runs"; Anthropic Fable 5.1 / Opus 5.5 (4/20, "start here for most workloads") /
    Sonnet 5.5 / Haiku 4.5, Opus 5 and Sonnet 5 legacy; thinking always on for Fable 5.1 and Opus
    5.5; Astra-to-Luna ratio 100x (was 50x / 42x), mid-tier one fifth to two fifths of the flagship;
    table rows; ChatGPT paragraph says GPT-6.1 Sol / 6 Sol / 6 Luna are only in Work and Codex,
    Free and Go get GPT-6 Luna in the desktop app, Pro is $100/$200/$500 (the 9/10 Pro 200 pause
    sentence was dropped: it reopened on 9/29); choosing-a-model path starts from Opus 5.5; the
    dead `support.claude.com/.../11049762-choose-a-claude-plan` source (404) was removed, since
    claude.com/pricing carries the same plan facts. Google rows re-checked and unchanged; the Gemini
    app subscription paragraph keeps its own explicit 9/13 date (the subscriptions page geolocates
    to the Taiwan page, so the USD prices could not be re-read). learn.chatgpt.com models and pricing
    were added as sources (17 → 19) for the Work/Codex-only and desktop-Luna sentences. Diagram
    redrawn.
  - ai-coding-cost-tokens-explained: Anthropic Opus 5.5 4/20 and Sonnet 5.5 2/10; OpenAI GPT-6 Luna
    0.10/0.01/0.50; flagship-to-light gap 100x; output "usually five times input"; Codex Plus
    estimate GPT-6 Luna 350–3,000 per 5 hours; Claude minimum cacheable length Sonnet 5.5 512
    tokens; OpenAI cache write 1.25x and read 0.1x (0.05x on GPT-6.1 Sol), "up to 95%"; worked
    example renamed to Sonnet 5.5 (same prices, so the 5.92 / 1.20 USD figures are unchanged).
    Copilot, Cursor and Gemini CLI rows keep 9/14 and the caption says which date covers what.
  - ai-free-vs-paid-plans-2026: GPT-5.6 Sol is no longer called "旗艦" (it is the paid Chat model);
    Plus's Codex offers GPT-6.1 Sol and GPT-6 Luna, Free and Go get GPT-6 Luna in the desktop app;
    Claude's context window is "up to 1M, depends on the model" (claude.com/pricing) instead of
    200k. Diagram redrawn (coding branch and the Claude context line).
  - chatgpt-beginner-guide: Plus's slider is Instant / Medium / High, Extra High and Pro are Pro
    only (the page said Plus had Extra High); the Multi-currency billing page now lists TWD for
    Taiwan (the page said Taiwan was not listed). Diagram footnote and title date updated.
  - claude-vs-chatgpt-writing-test: Anthropic's four current models are Fable 5.1, Opus 5.5,
    Sonnet 5.5, Haiku 4.5; GPT-6.1 Sol is only in Work and Codex, not in Chat.
  - openrouter-multi-model-api: code samples and the fallback JSON use `anthropic/claude-sonnet-5.5`
    (OpenRouter lists it at 2/10, 1M context; the quickstart itself now uses
    `~openai/gpt-sol-latest`, the page keeps its "only the model ID is swapped" wording); model-page
    examples (gpt-oss-20b is now 0.018/0.09); pricing.overrides example is GPT-6 Luna (0.1/0.5,
    0.2/0.75 above 272,000 tokens); counts re-measured on 10-05: 466 text models, 649 with
    `output_modalities=all`, 17 and 24 `:free`, 376 from `supported_parameters=tools`; routing modes
    now include Floor (cheapest).
  - ai-tools-2026-overview: example models, ChatGPT Pro tiers $100/$200/$500, Chat on GPT-5.6 versus
    the GPT-6 family in Work, Codex and the API (GPT-6 Pro, powered by Astra, is the one GPT-6 model
    in Chat, on Pro 100/200, Business and Enterprise; the page names Pro 100/200), Claude Opus 5.5 / Sonnet 5.5, Codex Pro tiers with
    Astra Ultrafast on Pro 500 (GPT-5.3-Codex-Spark retired on 2026-09-14, so it is no longer
    offered as a Pro perk). The chatgpt.com/plans/free/ source no longer states the unlimited-text
    rule, so it was replaced by the help article that does.
  - The help article 20001354 now lives at `.../20001354-gpt-56-and-gpt-6-pro-in-chatgpt`; edited
    packs cite that URL (the old slugs still redirect).
- Check-date wording: each edited page says next to its original date which facts were re-read on
  10-05 (description and/or intro, table captions, diagram notes), instead of claiming one date.
- Unchanged, with reasons:
  - chatgpt-plans-plus-pro-2026: every GPT-5.6 mention is a Chat claim (Free/Go GPT-5.6 Luna and
    Think, Plus GPT-5.6 Sol up to High, Pro adds Extra High and Pro, Business on GPT-5.6 Sol), all
    still what the help article says on 10-05; its Work/Codex lines (GPT-6 Astra in Plus Work and
    Codex, GPT-6.1 Sol rolling out, Codex 5-hour estimates 5–45 / 15–160 / 350–3,000, Pro 500 with
    Astra Ultrafast, Pro 200 reopened with a lower allowance) match learn.chatgpt.com and the Pro
    tiers article on 10-05. Its diagram shows only Chat models and plan prices.
  - chatgpt-canvas-writing: GPT-5.6 Luna (Free/Go) and GPT-5.6 Sol (paid) are still the Chat
    defaults; Model release notes still say canvas stays on "legacy models until those models are
    sunset" with no date (GPT-5.5's 10-14 retirement does not date it: GPT-5.5 already lost canvas).
  - chatgpt-team-for-small-business: the one hit, Pro messages shared by GPT-6 Pro and GPT-5.6 Sol
    Pro on Business seats, is still what the help article says.
- Checks: `pack_cli lint --kind life` (with `--render-dir`, Edge) passed for the seven edited slugs;
  the only warning is the pre-existing `no_summary`. `intake_check.py --from-content` reports the
  same FAILs these older life pages already had (no summary block, 5–6 column tables, 本文/這篇 over
  the limit); the edits added no 本文/這篇 (counts before and after are equal) and every diagram's
  numbers are in the text. The three redrawn diagrams (tiers, free-vs-paid, beginner) were rendered with Edge and checked by eye.
- Also found, not fixed here (not model or price claims, and each needs a source swap in a pack at
  the 20-source limit): ai-tools-2026-overview still says ChatGPT bills in USD and only Google has
  NT$ pricing, and chatgpt-beginner-guide still describes ads as a US test. Filed as
  `2026-10-05-chatgpt-taiwan-currency-and-ads-lines`.
