---
id: 2026-10-05-news-jev-final-stage-stops-at
title: News Jev final stage stops at the first uncertain answer instead of spending one quota unit per locale
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-jev-news-locale-uncertain-stop
claimed_at: 2026-10-05T07:49:19Z
created_at: 2026-10-05T07:47:05Z
completed_at:
branch: claude/jev-news-locale-uncertain-stop
depends_on: []
scope:
  - apps/api/app/news_automation/ai.py
  - apps/api/tests/test_news_pipeline.py
---

# News Jev final stage stops at the first uncertain answer instead of spending one quota unit per locale

## Why

`jev_assessments` (apps/api/app/news_automation/ai.py) asks Jev about one news article once
per locale: one locale (`zh-TW`) for the stage-one draft, all five for "Jev's last call"
(`_jev_final` in pipeline.py). Each locale first takes one unit of the daily Jev budget
(`consume_jev_call`) and then sends one paid question. Any locale that does not come back
`act` holds the whole candidate for a person (`_jev_final` returns it in the held list and
the pipeline stops with `news_jev_final_hold`).

Before #1233, a timeout or a 5xx from Jev escaped `JevClient.ask` as an httpx error. That is
not a `JevError`, so it skipped the per-locale `except (JevError, TimeoutError)` and hit the
outer `except Exception`, which ended the loop and marked every locale `confirm`. A provider
outage on the first locale cost one quota unit (and two wires, because the client retried
once) and the candidate held.

#1233 made the client raise `JevOutcomeUncertain` instead, after one wire. It is a `JevError`,
so the per-locale handler now catches it and the loop goes on to the next locale. During an
outage, or whenever answers are being lost, the five-locale last call takes five quota units
and sends five questions that each may have been run and billed, although the first failure
already decided that the candidate holds. Nothing on the success path needs to change.

## Definition of done

- [x] When Jev fails or the answer is uncertain for one locale, `jev_assessments` asks no
      further locale: no more `consume_jev_call` units and no more wires for that article.
      The failing locale and every locale after it are `confirm`, so the candidate holds as it
      did before #1233.
- [x] Locales answered before the failure keep their real decisions, and an article whose
      locales are all answered is assessed exactly as before (one unit and one wire each).
- [x] A regression test drives the real `JevClient` over a fake transport that counts wires,
      and counts the quota units taken.

## Steps

- [x] Read #1233's diff (`JevOutcomeUncertain`, `_send`) and the two `jev_assessments`
      callers in pipeline.py.
- [x] In the per-locale `except (JevError, TimeoutError)` branch, record the failing locale,
      mark the locales not yet asked `confirm` with a reason that says they were not asked,
      and leave the loop.
- [x] Tests in tests/test_news_pipeline.py: a lost answer (ReadTimeout) on the first and on a
      later locale, a 5xx, and an all-answered control, each counting wires and quota units.

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 uv run pytest tests/test_news_pipeline.py tests/test_jev_client.py -q
uv run ruff check . && uv run mypy app && uv run mypy tests
```

The fake transport is `httpx.MockTransport`; never reproduce a lost answer against TypeSafe.

## Notes

- Found while following up #1233 (`2026-10-04-jev-provider-uncertain-retries`), whose Notes
  already say that an uncertain outcome now marks only that locale `confirm` where an escaping
  httpx error used to mark every locale. That change of behaviour is what this ticket
  reverses for the loop, keeping #1233's one-wire guarantee inside the client.
- `jev_duplicate_check` asks once per candidate and already stops on any exception; it is not
  affected.

### 2026-10-05, claude-opus-5-5-jev-news-locale-uncertain-stop

- **Claim reconciled with `--force`.** The overlap was
  `2026-10-05-news-auto-publish-reads-its-switches` (claude-opus-5-5, status review), which
  lists tests/test_news_pipeline.py. Its branch `claude/news-auto-publish-fresh-switches`
  merged as #1247 (1ff45131f) at 07:26Z today; no open pull request touched
  `apps/api/app/news_automation/` or that test file when this was claimed. That ticket file was
  not edited.
- **What changed.** In `jev_assessments`, the per-locale `except (JevError, TimeoutError)`
  branch now records the failing locale as `confirm` with the error's type name (as before),
  marks every locale after it `confirm` with reasons `["not_asked", <type name>]`
  (`ai.JEV_NOT_ASKED`), and leaves the loop. Those locales take no quota unit and send no
  question. Locales answered earlier keep their tier, confidence and usage. The settled-success
  path, the `quota_unavailable` path (which takes no unit and sends nothing, so it still moves
  on) and the outer `except Exception` handler are unchanged.
- **Every `JevError` stops the loop, not only `JevOutcomeUncertain`.** Any locale that is not
  `act` already holds the article (`_jev_final` returns it as held and the run stops with
  `news_jev_final_hold`; stage one has only `zh-TW`), so after any failure the remaining
  answers cannot change the outcome. Before #1233 a settled `JevError` (401/403, 400/422, an
  oversized document, a malformed answer) let the loop go on; that now stops as well, which only
  saves quota units.
- **Not quite "as before" in one way, on purpose.** Before #1233 the escaping httpx error
  replaced every locale's decision, including ones already answered, with the error name. Now
  the answered locales keep their real decisions and the unasked ones say `not_asked`, so the
  admin table shows which locale's question may have been run and billed. A 429/529 refused
  every time or a connection that never opened still escapes as an httpx error to the outer
  handler and marks every locale with that error's name, as before.
- **The admin news page shows `not_asked` raw.** `named(copy.reasonCodes, ...)` falls back to the
  code, the same way it already shows `JevOutcomeUncertain` or `ReadTimeout`. A translated label
  would need the five `apps/web/lib/admin-news-messages/*.json` files, outside this scope; not
  filed, since the type names beside it are untranslated too.
- **Verified.** Four new parametrized cases drive the real `JevClient` over
  `httpx.MockTransport` with a counting handler and an `AsyncMock` for `consume_jev_call`:
  ReadTimeout on the first locale, 502 on the third, a non-JSON 200 on the fourth and a 422 on
  the second. Each sends `failing + 1` wires and takes `failing + 1` units; on origin/main's
  ai.py all four sent 5 wires (`assert 5 == (0 + 1)` and so on). The all-answered control sends
  5 wires, takes 5 units and returns the five `act` decisions with their usage, on both.
  `pytest tests/test_news_pipeline.py tests/test_jev_client.py tests/test_news_resume_saved_bundle.py`
  103 passed; `ruff check .`, `mypy app` (461 files) and `mypy tests` (367 files) are clean.
