---
id: 2026-10-02-preserve-sanitized-video-provider-rejection-details
title: Preserve sanitized video provider rejection details
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-02T19:01:29Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_media/providers/__init__.py
  - apps/api/tests/test_video_media_providers.py
---

# Preserve sanitized video provider rejection details

## Why

The common video-media `raise_for_status` maps every vendor HTTP 400 to
`MediaUpstreamError(422, "<vendor> refused the request", "blocked")` and discards the
response details. Operators cannot distinguish an unsupported parameter, invalid
input, model incompatibility or an actual safety rejection from the persisted error.

During the E1 single-shot pilot on 2026-10-03, job
`061183d5-a672-4ae0-ae41-09df30a31752` failed on its only submit attempt with
`video_media_rejected` / `Gemini refused the request`, no vendor operation and no
file. A read-only model GET returned 200, which did not explain the submission
failure. A later separately authorized diagnostic obtained an HTTP 400
`INVALID_ARGUMENT` stating that `negativePrompt` is unsupported by that model;
the existing adapter error had lost this actionable distinction.

## Definition of done

- [ ] A rejected video-media request retains a bounded, sanitized provider diagnostic in the existing error path, sufficient to distinguish an explicit unsupported-parameter response from a safety rejection when the provider supplies that distinction.
- [ ] API keys, bearer tokens, credential-bearing query strings, signed URLs, full prompts, image/base64 data and other request secrets are never included in retained errors or logs; do not store an unfiltered response body.
- [ ] Missing, malformed, non-JSON or oversized vendor error bodies produce a safe generic fallback.
- [ ] Existing error status/kind semantics, safety decisions, pinned provider hosts, approval/budget gates, reservations and retry behavior remain unchanged; this task does not authorize paid reproduction or resubmission.
- [ ] Focused tests cover useful sanitized rejection detail, secret redaction, safe fallbacks and unchanged existing error classifications.

## Steps

- [ ] Inspect the common `raise_for_status` / `post_json` path and existing provider tests; choose bounded allowlisted diagnostic fields with explicit redaction.
- [ ] Add an offline regression fixture for a 400 `INVALID_ARGUMENT` unsupported-parameter response plus adversarial secret-containing and non-JSON error fixtures.
- [ ] Implement only in the declared provider helper and existing test file, retaining all request and retry guardrails.

## How to verify

```bash
cd apps/api
uv run pytest tests/test_video_media_providers.py -q
uv run ruff check app/video_media/providers/__init__.py tests/test_video_media_providers.py
```

The tests must make no live provider requests. Inspect captured errors/logs for the
redaction fixture sentinels; a passing status code alone is insufficient.

## Notes

- Filed only, intentionally `open` and unclaimed; no provider code changed.
- Existing tasks/open and tasks/done were searched for the generic refusal/HTTP 400 diagnostic gap. The separate open Kling provider ticket does not cover it.
- `who-is-on-it.mjs` found no active claim or open PR touching either declared path when filed. Recheck before claiming; this is not a lock.
- Sanitized production evidence is summarized in `docs/videos/series-plans/competition-20261002/episodes/production-run-20261003.md`; raw private receipts stay outside Git. Never replay a paid request merely to reproduce this ticket.
- Model-specific removal of unsupported `negativePrompt` is tracked by `2026-10-02-honor-veo-lite-negativeprompt-compatibility`; this ticket concerns preserving diagnostics, not changing parameters or inferring that all 400s mean safety failures. Both tickets share the existing provider test file, so coordinate sequential claims before implementation.
- Verified local `diagnostic-r02/transport.jsonl` SHA-256 `0111f51712753cb8ed6578b248b82317a3b2d0c2b85f571b04ab663b84f16f47` preserves the sanitized HTTP 400 / `INVALID_ARGUMENT` response identifying unsupported `negativePrompt`. Its normal job receipt still retained only `video_media_rejected`; the separately scoped R03 payload returned HTTP 200 and a ready file after dropping that field while keeping the avoidance instructions in the main prompt. This confirms why actionable error details must survive the common helper; visual QA remains separate.
