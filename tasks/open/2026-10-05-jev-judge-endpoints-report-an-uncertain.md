---
id: 2026-10-05-jev-judge-endpoints-report-an-uncertain
title: Jev judge endpoints report an uncertain provider outcome apart from a settled failure
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-05T00:58:04Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_speech/admin_api.py
  - apps/api/tests/test_video_automation_judge.py
  - apps/api/tests/test_video_speech_check.py
---

# Jev judge endpoints report an uncertain provider outcome apart from a settled failure

## Why

Since 2026-10-04-jev-provider-uncertain-retries, `JevClient` raises `JevOutcomeUncertain` (a
`JevError`) when Jev may have processed a paid question but its answer was lost: a read or
write timeout, a dropped connection, a 5xx other than 529, or a 2xx body that is not JSON. The
exception carries `phase`, `status`, `wires_sent` and `request_sha256` (the SHA-256 of the
exact body sent), and the client never sends that question again by itself.

The three video endpoints that ask Jev on the video tool's behalf throw that evidence away.
`POST /judge/outline` and `POST /judge/policy` (`app/video_automation/admin_api.py`, the
`except (JevError, httpx.HTTPError)` branches) and `POST /speech/judge`
(`app/video_speech/admin_api.py`, same branch) answer every Jev failure with the same
`502 video_judge_upstream_failed` / "Jev 暫時無法判斷". A 529 that the vendor refused four
times, a ConnectError that never reached the provider, and an answer lost after the provider
may have run (and billed) the question all look identical to the caller. Each endpoint has
already consumed one daily Jev quota unit (`consume_jev_call`) before asking, so the CLI side
(`tools/video/automation/client.mjs`, `tools/video/tts/client.mjs`) cannot tell whether
re-sending would pay for the same input twice, and cannot record which input it was.

## Definition of done

- [ ] A Jev outcome that may have been processed reaches the caller under its own error code
      (for example `video_judge_outcome_uncertain`), with `phase`, `status`, `wires_sent` and
      `request_sha256`, and never with the key, a URL or the request body.
- [ ] Settled failures (auth, 400/422, 429/529 refused every time, a connection that never
      opened) keep their current codes and statuses.
- [ ] The response says that one daily quota unit was consumed for the call, so the caller can
      tell application calls, quota and provider wires apart.

## Steps

- [ ] Add an `except JevOutcomeUncertain` branch ahead of the generic `JevError` branch in the
      three endpoints, and decide the HTTP status with the CLI tickets in mind (they treat a
      502 as uncertain today).
- [ ] Tests with a fake Jev transport for each endpoint: a ReadTimeout, a 502 and a non-JSON 200
      give the new code and one wire; a ConnectError then 200 still succeeds.
- [ ] Tell the owners of 2026-10-04-prevent-automatic-retries-of-paid-video and
      2026-10-04-prevent-paid-speech-retries-after-ambiguous (the CLI transports) which code to
      hold on.

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 uv run pytest tests/test_video_automation_judge.py tests/test_video_speech_check.py -q
uv run ruff check . && uv run mypy app && uv run mypy tests
```

Use `httpx.MockTransport`; never reproduce a lost answer against TypeSafe.

## Notes

- Split out of 2026-10-04-jev-provider-uncertain-retries, whose scope was only
  `app/ai/jev.py` and its tests. That change already makes these endpoints safer on their own:
  a lost answer costs one wire instead of two inside the client.
- Other Jev callers already keep the evidence well enough: `news_automation/ai.py` records the
  exception type name per locale, `hotspots/ai_search.py` and `guides/jev_review.py` record
  `TypeName: message` and stop. The admin settings probe (`admin/service.py`) shows only the
  type name, so a probe timeout now reads `JevOutcomeUncertain` rather than `ReadTimeout`; the
  message still names the transport error if that card ever needs it.
