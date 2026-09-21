---
id: 2026-09-21-jev-typesafe-system-one-decision-provider
title: Jev (TypeSafe System One) decision provider: settings, client and catalog
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-21T15:37:12Z
created_at: 2026-09-21T15:37:08Z
completed_at:
branch: claude/add-jev-key-msana6
depends_on: []
scope:
  - apps/api/app/ai/jev.py
  - apps/api/app/ai/catalog.py
  - apps/api/app/config.py
  - apps/api/tests/test_jev_client.py
  - apps/api/tests/test_ai_catalog.py
  - apps/api/tests/test_security_config.py
  - .env.example
  - README.md
---

# Jev (TypeSafe System One) decision provider: settings, client and catalog

## Why

Every classification this product does today runs through a model built to write
prose. The guide search asks a generative vendor for a `relevance_score` between 0
and 100 and then compares it to 60; food-merchant enrichment asks one for a
confidence it invented. Jev, TypeSafe's System One model, answers `choice`, `score`
and `noul` questions with a calibrated probability distribution and cannot write a
sentence at all. It costs $0.042 per million input tokens with output unbilled, so
the work where a generating model is doing a classifier's job gets cheaper, faster
and measurable at the same time.

This task lands the key, the client and the catalog entry only. The encrypted admin
card is a separate task because its files are held by another claim (see Notes).

## Definition of done

- [x] `JEV_API_KEY` is a real setting, host-pinned to `api.typesafe.ai`, and
      production refuses a base URL that leaves that host.
- [x] A client exists that batches questions into one call, parses all three answer
      types, and never puts the key in a URL.
- [x] `jev-1.13.0` is selectable from the server-curated model catalog, and no
      generating code path can be pointed at it.
- [ ] The key can be entered from the admin panel -- **not this task**, see
      `2026-09-21-jev-api-key-on-the-ai`.

## Steps

- [x] `apps/api/app/config.py`: `jev_api_base_url` / `jev_model` / `jev_api_key`, the
      decision budgets, `jev_configured`, `OFFICIAL_PROVIDER_HOSTS`, `pinned_endpoints`.
- [x] `apps/api/app/ai/catalog.py`: `jev` vendor, `jev_structured_decision` capability,
      three model entries, `MODEL_FIELDS["jev_model"]`.
- [x] `apps/api/app/ai/jev.py`: `JevClient.ask`, `route`, `consume_jev_call`, `probe`.
- [x] Tests: `test_jev_client.py`, plus the host-pinning case and the catalog cases.
- [x] `.env.example` and `README.md`.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
```

`probe(settings)` is the end-to-end check once a real key exists; it is wired to the
admin card by the follow-up task. It sends one noul question over a four-word state,
about forty input tokens, and output is not billed.

## Notes

- **What Jev is.** `POST https://api.typesafe.ai/v1/systemone`, `Authorization: Bearer`.
  One `state` plus a map of named questions. `choice` returns the option, a confidence
  and the full distribution (max 255 options); `score` returns a position on 2-10
  ordered levels with a legend; `noul` returns one probability and **no `confidence`
  field** -- `route()` branches on the answer type for exactly that reason.
- **Why no SDK.** `typesafe-sdk` exists, but every vendor in this repo is a hand-rolled
  httpx call, and an SDK's own retry loop would fight the provider circuit breaker.
- **Why the vendor's `TYPESAFE_API_KEY` name was not used.** `Settings` has no
  `validation_alias` anywhere; env name is the uppercased field name. A comment in
  `.env.example` records the vendor's name instead.
- **422 is never retried.** It means this module built an illegal question. The size
  and shape guards in `_check_questions` / `_check_size` exist so that most of those
  never leave the process; the batch-splitting caller gets `JevRequestTooLarge`.
- **The language caveat is code, not prose.** `docs.typesafe.ai/models` states that
  "English is the primary training language and where accuracy is currently best", and
  TypeSafe publishes no accuracy figures for any other language. This product ships in
  five, so `jev_cjk_autopilot_enabled` defaults to false and `route()` downgrades a
  confident non-English answer from `act` to `confirm` while it is off. The thresholds
  0.9 / 0.5 are the vendor's example numbers and are placeholders until shadow-mode
  numbers from our own content replace them.
- **What the first-party docs corrected, after this was first written.** The initial
  pass was built partly from third-party write-ups; `docs.typesafe.ai` confirmed the
  endpoint, auth, error codes, 64k/32k limits, the `jev-1.13.0` id, the pricing and
  the 2-10 score range, and corrected three things. A noul takes an **optional
  `criteria`** to clarify what yes and no cover, so `NoulQuestion` carries it and the
  payload is dumped with `exclude_none` rather than sending `criteria: null`. The
  255-option **choice cap is ours, not the vendor's** -- TypeSafe documents no maximum
  -- and the constant says so. And the "validate on your own Traditional Chinese data"
  instruction is not in the docs; only the English-is-best statement above is.
- **`docs.typesafe.ai/model-jaggedness/jev-1.13` is the page to read before pointing
  Jev at anything new.** Two entries rule out whole categories here: Jev "reads dates
  as text, not as ordered quantities", so date ordering, intervals and windows are
  unreliable -- which is most of what a travel product asks about dates; and it is
  "not a calculator", does "not count reliably", and its "score levels are weak in
  numerical calibration". Also documented: it answers the question as literally
  written, multi-hop or doubly-negated instructions cost accuracy, and accuracy falls
  as the state grows with content unrelated to the decision.
- **Jev is deliberately not a planner vendor.** It cannot generate. It is absent from
  `AIProviderName` in both `app/ai/itinerary.py` and `app/hotspots/ai_search.py`, from
  `ai_planner_priority`, and from every `*_default_provider` allow-list. A vendor on
  those lists that can never return a draft would fall through to the catalog forever.
- **The admin card is blocked, not skipped.** `apps/api/app/admin/service.py`,
  `apps/web/components/admin-settings-panel.tsx` and their tests are in the scope of
  `2026-09-14-planner-budget-admin-card` (status `review`, owner `claude-fable-5-1`),
  and the five `admin.json` files are also in `2026-09-13-adsense-ads-txt-drift`.
  `claim` refuses an overlapping scope regardless of staleness (`tools/tasks.mjs:475`),
  and `--force` would defeat the point of the board. Both blockers look already merged
  -- `ai_planner_user_budget` is in the panel and `apps/web/app/ads.txt/` exists -- so
  the unblock is for their owner to run `npm run tasks -- done <id>` on each.
- **Where Jev should be used first**, once the key path is live: the guide-candidate
  assessment in `app/hotspots/ai_search.py` (the `relevance_score < 60` threshold),
  in shadow mode, recording Jev's answer beside the current one and changing no
  behaviour. That is the vendor's "validate on your own dataset" done properly, and it
  produces the numbers that decide whether `jev_cjk_autopilot_enabled` may ever be on.
  Ranked after it: food-merchant/platform-row matching, crawler page-shape alerting.
  Explicitly not: any generation, money arithmetic (`alerts/policy.py`, `pricing/`),
  anything on a user request path, and auth or permission decisions. **Withdrawn after
  reading the jaggedness page**: scoring guide-article staleness by how long ago a fact
  was last checked. That is date ordering, which Jev does unreliably by its own
  documentation, and it was the one idea here that would have been graded on exactly
  the axis the model is weakest on.
