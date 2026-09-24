---
id: 2026-09-24-let-news-model-replies-be-repaired
title: Let news model replies be repaired instead of failing whole candidates
status: done
priority: P1
area: api
owner: claude-opus-5.5
claimed_at: 2026-09-24T02:52:07Z
created_at: 2026-09-24T02:51:59Z
completed_at: 2026-09-24T02:54:48Z
branch: claude/news-model-output-repair
depends_on: []
scope:
  - apps/api/app/news_automation/provider_schema.py
  - apps/api/app/news_automation/schemas.py
  - apps/api/app/news_automation/ai.py
  - apps/api/app/news_automation/jobs.py
  - apps/api/app/ai/structured_output.py
  - apps/api/app/ai/gemini.py
  - apps/api/app/hotspots/ai_search.py
  - apps/api/tests/test_news_pipeline.py
  - apps/api/tests/test_structured_output.py
  - apps/api/tests/test_hotspot_ai_search.py
---

# Let news model replies be repaired instead of failing whole candidates

## Why

The first production run of the news pipeline (MiniMax writer and checker, 2026-09-24)
drafted, verified and translated real candidates, and failed three of the first five on
reply validation:

- the writer set the source site's logo (`https://blog.google/.../google-logo.svg`) as
  `document.hero`, which only self-hosted images may be;
- an English translation had a 326-character summary item against a limit of 300;
- a draft came back as JSON with a missing comma at column 3363.

Each adapter already retries once, but its repair prompt only says "repair the previous
invalid JSON" with the reply attached, so the model mostly repeats the mistake. Then RQ
reran the whole candidate twice (draft, verification, four translations, reviews) for a
failure that recurs.

## Definition of done

- [x] A news reply's hero and image/offer/partner-link blocks are dropped before
      validation; the pipeline supplies the artwork.
- [x] The repair attempt of every structured adapter (Responses, Anthropic, Gemini) says
      which fields failed and why.
- [x] Writer, translator and locale-review instructions state the imagery rule and the
      length limits.
- [x] A candidate that fails on a reply's validation (or an incomplete reply) is not
      rerun by RQ; provider outages still are.

## Steps

- [x] `repair_instruction` in `app/ai/structured_output.py`, used by the three adapters.
- [x] `ProviderReply.document_fields` and a before-validator that drops model imagery.
- [x] Prompt rules in `app/news_automation/ai.py`.
- [x] `run_candidate` swallows `ValidationError`/`ValueError` after the candidate is
      marked failed.
- [x] Tests.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py tests/test_structured_output.py tests/test_hotspot_ai_search.py tests/test_hotspot_candidate_generation.py -q
```

On the host after deploying: new `failed` candidates with `ValidationError` become rare,
and none is retried by RQ (one `run_candidate` job per failure in the worker log).

## Notes

- The repair prompt change is shared with the hotspot guide search, the introduction
  writer and the candidate generator; their tests still pass and they gain the same
  error detail.
- Candidates that already failed this way can be rerun from /admin/news (「重新執行」).
