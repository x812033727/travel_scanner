---
id: 2026-09-25-offer-claude-opus-5-5-in
title: Offer Claude Opus 5.5 in the admin model dropdowns
status: done
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-25T01:37:22Z
created_at: 2026-09-25T01:37:10Z
completed_at: 2026-09-25T01:39:07Z
branch: claude/catalog-claude-opus-5-5
depends_on: []
scope:
  - apps/api/app/ai/catalog.py
  - apps/api/tests/test_ai_catalog.py
---

# Offer Claude Opus 5.5 in the admin model dropdowns

## Why

On 2026-09-25 the site owner noticed that the AI news writer and fact-checker dropdowns
(`/admin/news` settings) offer Claude Opus 5, Sonnet 5 and Haiku 4.5 but not Claude Opus
5.5 (`claude-opus-5-5`), Anthropic's newer Opus at a lower price ($4 / $20 per MTok
against Opus 5's $5 / $25). Every Anthropic dropdown in the admin (news, planner, trip
parser, guide search, introductions) is built from `apps/api/app/ai/catalog.py`, so the
model has to be listed there.

## Definition of done

- [x] `claude-opus-5-5` is offered first under Anthropic wherever the catalog feeds a
      dropdown, with Opus 5 kept.
- [x] A test pins that every Anthropic request the code sends is one Opus 5.5 accepts,
      and that its always-on thinking block does not break parsing.

## Steps

- [x] Check the request shape against the model's breaking changes: Opus 5.5 always
      thinks (`thinking` disabled or budgeted is a 400) and rejects temperature/top_p/
      top_k and forced `tool_choice`. `AnthropicResearchProvider` (news, guide search,
      introductions), `app/ai/itinerary.py` and `app/ai/trip_parser.py` send only
      `model`, `max_tokens`, `system`, `messages` and `output_config.format`, and all read
      replies through `anthropic_output_text`, which joins text blocks only.
- [x] Add the catalog entry and tests.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_ai_catalog.py -q
```

After deploying, `/admin/news` settings: choose Anthropic as the writer or fact-checker
and Claude Opus 5.5 is the first model.

## Notes

- Production had no Anthropic API key on 2026-09-24 (only MiniMax, Gemini and Jev).
  Saving the news settings does not check for one, so choosing Anthropic without adding a
  key under 「AI 供應商與金鑰」 makes every candidate fail at the drafting stage. The Claude
  subscription accounts on `/admin/ai-accounts` sign in the host's Claude Code CLI; they
  are not an API key.
- Opus 5.5 defaults to `medium` effort; the requests send no `output_config.effort`, so
  that default applies. News stages allow 32,000 output tokens, thinking included.
