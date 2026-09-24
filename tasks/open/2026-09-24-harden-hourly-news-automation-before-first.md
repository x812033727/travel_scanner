---
id: 2026-09-24-harden-hourly-news-automation-before-first
title: Harden hourly news automation before first activation
status: in-progress
priority: P1
area: api
owner: claude-opus-5.5
claimed_at: 2026-09-24T00:03:26Z
created_at: 2026-09-24T00:03:16Z
completed_at:
branch: claude/ai-hourly-news-refinement-d2d87f
depends_on: []
scope:
  - apps/api/app/news_automation
  - apps/api/app/worker.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_news_pipeline.py
  - docker-compose.yml
  - docker-compose.prod.yml
  - docs/news-automation.md
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news.ts
  - apps/web/lib/admin-news-copy.ts
---

# Harden hourly news automation before first activation

## Why

PR #694 shipped the hourly news automation switched off. Reading it end to end before
anyone turns it on showed that the first real run would not get past the first model
call, and that ordinary feed noise would stall the loop:

- Every structured stage sends the raw pydantic JSON Schema of a `GuideDocument`
  (optional properties, `oneOf` + `discriminator`, `minLength`/`maxLength`,
  `minimum`/`maximum`, `maxItems`, and a `dict[Locale, GuideDocument]` for the
  translation bundle). OpenAI strict Structured Outputs and Anthropic structured
  outputs both reject those keywords over raw HTTP, so the default `openai` writer
  fails with HTTP 400 on the draft.
- The translation stage asks for four complete documents in one non-streaming call
  under a 90-second read timeout.
- One unreachable article or linked page in a feed aborts and rolls back the whole
  scan, and the same entry breaks every later hourly scan. Every entry is refetched
  every hour, robots.txt is fetched again for every request, and drifting page text
  files a fresh "duplicate" row each hour.
- A worker killed mid-pipeline (a deploy restarts containers) leaves the candidate in
  `drafting`/`verifying`/... forever. It holds the concurrency slot, so with the
  default per-vertical limit of 1 the whole vertical stops, and every other candidate
  re-enqueues itself once a minute forever. The same one-minute loop runs forever for
  every candidate when the global switch is off or the candidate is already terminal.
- The semantic duplicate check only compares against other automation candidates, not
  the 120+ news articles the site already published by hand.
- News jobs share the single general worker with search and trip routing; one
  candidate is 20+ model calls and can hold that worker for up to an hour.
- The candidate job builds its model clients from `get_settings()`, the environment
  only. API keys (Jev's included) and default models live in the admin card
  「AI 供應商與金鑰」 since migration 0047, which the hotspot AI tasks read through
  `load_runtime_settings`; in production the news job would not find its keys.
- The writer/checker model is a free-text box (site owner asked for a dropdown like the
  other AI settings), and the value is not checked although a Gemini model id is
  interpolated into the request path.

## Definition of done

- [x] Every schema a news stage sends is accepted by OpenAI strict mode and Anthropic
      structured outputs (all properties required, `additionalProperties: false`,
      `anyOf` only, no unsupported keywords, no map types), with the dropped
      constraints still enforced by pydantic and visible to the model as text.
- [x] Translation is one call per locale with a timeout that fits a full article.
- [x] A failing entry or linked page is skipped and reported; the scan still commits
      everything else. Already-seen URLs are not refetched; robots.txt is fetched once
      per host per scan.
- [x] Candidates stuck in an in-flight status past the job timeout become `failed`
      (`news_processing_stale`) and stop holding capacity; only capacity deferrals
      re-enqueue; orphaned `discovered` candidates are picked up again once enabled.
- [x] The duplicate check also sees news articles published in the last 30 days.
- [x] A dedicated `news-worker` in the `news` compose profile consumes the `news`
      queue; the general worker no longer does.
- [x] `docs/news-automation.md` explains how to switch it on, in order, and what each
      switch does.
- [x] The candidate job reads keys and models the way the admin AI settings store them.
- [x] Writer and checker models are chosen from dropdowns built on the server model
      catalog (default = the model the job will actually use, catalog entries, custom),
      and stored ids must match the catalog's id pattern.

## Steps

- [x] Provider-portable schema transform + tests.
- [x] Per-locale translation, stage timeout.
- [x] Scanner isolation, seen-URL skip, robots cache + tests.
- [x] Claim lock, deferral outcomes, stale recovery, orphan sweep + tests.
- [x] Duplicate check against published news + test.
- [x] news-worker service, worker queue list.
- [x] Activation runbook.
- [x] Runtime settings in the candidate job; model dropdowns in `/admin/news`.

## How to verify

```bash
cd apps/api && uv run ruff check app/news_automation tests/test_news_automation.py tests/test_news_pipeline.py
cd apps/api && uv run mypy app && uv run pytest tests/test_news_automation.py tests/test_news_pipeline.py tests/test_news_admin.py tests/test_guides_publish_bundle.py tests/test_catalog_review_jobs.py -q
npm run lint:web && npm run check:i18n && npm run typecheck:web
npm run test:web -- admin-news-workspace
npm run check:tasks
```

## Notes

- Production (2026-09-24): main at 0f9eb1dc includes #694, so migration 0084 is applied;
  `docker compose ps` shows no `news-scheduler` (the `news` profile is not started by
  `/root/deploy-travel-scanner.sh`, which passes only `--profile hotspots`). Nothing has
  run yet. Reading the settings row was blocked by the auto-mode classifier.
- The provider requirements were checked against the documented limits, not a live
  call (no keys here): OpenAI strict mode needs every property in `required`,
  `additionalProperties: false` and no `oneOf`; Anthropic structured outputs rejects
  `minLength`/`maxLength`, `minimum`/`maximum`, complex array bounds and open objects and
  its SDKs strip them client-side, which raw `httpx` does not. The test pins the
  invariants for all four reply models.
- A linked page that fails transiently (timeout, reset, DNS, 429, 5xx) holds the whole
  entry back so it is retried on the next scan with its evidence; a permanent failure
  (4xx, robots, content type) drops only that link. Two links redirecting to one page no
  longer produce a duplicate evidence URL (a unique-constraint failure that would have
  rolled back the scan).
- Robots policy is unchanged (non-2xx robots.txt still disallows); it is only cached per
  fetcher.
- Follow-ups filed: 2026-09-24-let-gemini-serve-news-stages-without (the shared
  `gemini_response_schema` keeps only the first `anyOf` option, so Gemini cannot write a
  `GuideDocument`), 2026-09-24-attach-a-second-evidence-source-to (first-party feeds
  rarely yield a second evidence page), 2026-09-24-keep-every-news-review-item-reachable
  (the review list is the newest 100 candidates filtered in the browser).
- Not done here, needs the site owner: adding `--profile news` to
  `/root/deploy-travel-scanner.sh`, keys, sources, and turning the scanner on.
