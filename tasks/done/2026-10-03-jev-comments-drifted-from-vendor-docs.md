---
id: 2026-10-03-jev-comments-drifted-from-vendor-docs
title: Jev comments and docs drifted from the code and TypeSafe's docs
status: done
priority: P3
area: api
owner: claude-opus-5-5-jev-contract
claimed_at: 2026-10-04T14:48:52Z
created_at: 2026-10-03T17:48:46Z
completed_at: 2026-10-04T15:31:04Z
branch: claude/jev-criteria-true-false
depends_on: []
scope:
  - apps/api/app/ai/jev.py
  - apps/api/app/config.py
  - docs/news-automation.md
---

# Jev comments and docs drifted from the code and TypeSafe's docs

## Why

Found while planning `docs/videos/ai-term-system-one-model` and confirmed by two independent
checks against the live TypeSafe docs on 2026-10-03. The behaviour is correct; the words around
it are not, and the next person to read them will reason from false premises.

## Definition of done

- [x] `apps/api/app/ai/jev.py:51-54` no longer says the 255-option cap is ours and that
      "TypeSafe documents no maximum". The docs say "You can have a maximum of 255 options per
      Choice" (https://docs.typesafe.ai/api) and "A Choice question accepts up to 255 options"
      (https://docs.typesafe.ai/primitives/choice). `MAX_CHOICE_OPTIONS = 255` stays.
- [x] The `probe()` docstring (`jev.py:420-426`) no longer says "TypeSafe documents no models
      endpoint". https://docs.typesafe.ai/models documents `GET /v1/models`, which lists only
      aliases and accepts versioned ids it does not list, so it still cannot prove that
      `jev-1.13.0` answers. Keep the noul probe; drop the gateway-405 reasoning.
- [x] `route()`'s docstring (`jev.py:383-385`) and the `config.py:516-520` comment say what the
      code does: `route_answer()` applies `jev_act_confidence` / `jev_flag_confidence` to a
      noul's probability and to a choice or score `confidence` alike, although the two are on
      different scales (a noul's equivalent confidence is |2p-1|). Today only noul answers are
      routed, so the defect is latent. Note that 0.9 / 0.5 are the vendor's Choice-confidence
      example (https://docs.typesafe.ai/confidence); its noul example uses other numbers.
- [x] `docs/news-automation.md:158-161` says a candidate spends up to seven Jev calls (as the same
      file says at :135-136) and that a spent budget pauses the candidate as
      `news_jev_quota_paused` (`news_automation/pipeline.py:484-495`), not "uncertain".
      `:287` no longer says "200 in production" (raised to 5,000 on 2026-09-27,
      `tasks/done/2026-09-27-resume-jev-paused-news-candidates-as.md:24-25`).

## Steps

- [x] Comments and docs only; no behaviour change.
- [x] If choice or score answers will ever be routed, file a separate task for noul-specific
      thresholds instead of widening this one.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_jev_client.py
```

## Notes

- Evidence and exact quotes: the verification run behind
  `docs/videos/ai-term-system-one-model/notes.md` §研究中發現、已開票的問題.
- Claimed with `--force` on 2026-10-04 by claude-opus-5-5-jev-contract. The overlapping claims
  had all landed: `2026-09-22-jev-review-advisory-tool` (jev.py) as #663, and the six
  `2026-09-30-*` / `2026-09-24-*` news tickets of claude-opus-5-5-news-4-9
  (docs/news-automation.md, branch `claude/gifted-rubin-umw5s4`) as #1041. No open PR touched
  the three files.
- Re-read on 2026-10-04 (docs.typesafe.ai/api, /primitives/choice, /models, /confidence, plain
  GET, no API key): all four quotes above still stand. The score quote the old comment carried,
  "ordered rubric levels (2-10 levels)", is no longer on the API page either; it now says a score
  should have at least two levels and that the API accepts up to 10, so the rewritten comment
  states the range without quoting. The noul example on /primitives/noul thresholds at
  `YES = 0.8` / `NO = 0.2`; config.py now says the 0.9 / 0.5 defaults come from the Choice
  example instead.
- `route()`'s docstring now says that the two thresholds are compared with a noul's value and with
  a choice's or score's `confidence` alike, and that only nouls are routed today. Callers checked
  with `git grep route_answer`: `guides/jev_review.py` (three nouls), `hotspots/ai_search.py`
  (noul shadow), and `news_automation/ai.py` calls `route()` on a noul with its own thresholds.
- Second step: not triggered. Nothing routes a choice or a score answer, so no task for
  noul-specific thresholds was filed; the docstring says routing one needs per-scale thresholds
  first.
- Found but not fixed (outside scope): `.agents/skills/prod-host-ops/references/news-ops.md`
  (and its `.claude` copy) still says a spent budget makes the duplicate check answer
  "uncertain"; filed as `2026-10-04-news-ops-skill-says-a-spent`.
