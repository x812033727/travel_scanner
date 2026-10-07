---
id: 2026-10-05-jev-judge-endpoints-report-an-uncertain
title: Jev judge endpoints report an uncertain provider outcome apart from a settled failure
status: done
priority: P2
area: api
owner: codex-jev-uncertain-endpoints
claimed_at: 2026-10-05T05:35:20Z
created_at: 2026-10-05T00:58:04Z
completed_at: 2026-10-07T01:43:04Z
branch: codex/jev-outcome-uncertain-endpoints-20261005
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

- [x] A Jev outcome that may have been processed reaches the caller under its own error code
      (for example `video_judge_outcome_uncertain`), with `phase`, `status`, `wires_sent` and
      `request_sha256`, and never with the key, a URL or the request body.
- [x] Settled failures (auth, 400/422, 429/529 refused every time, a connection that never
      opened) keep their current codes and statuses.
- [x] The response says that one daily quota unit was consumed for the call, so the caller can
      tell application calls, quota and provider wires apart.

## Steps

- [x] Add an `except JevOutcomeUncertain` branch ahead of the generic `JevError` branch in the
      three endpoints, and decide the HTTP status with the CLI tickets in mind (they treat a
      502 as uncertain today).
- [x] Tests with a fake Jev transport for each endpoint: a ReadTimeout, a 502 and a non-JSON 200
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

## Implementation and caller handoff (2026-10-05)

- The three endpoints keep HTTP 502 and the canonical `application/problem+json`
  envelope, including localized title/detail and `request_id`. The machine-readable
  code is `video_judge_outcome_uncertain`.
- Its added `jev_outcome` object contains only `phase`, `status`, `wires_sent` and
  `request_sha256`; `quota_units_consumed` is 1. The SHA pins the exact provider wire
  body. Neither exception text, credentials, provider URL nor request text is returned.
  One application call, one quota unit and one or more provider wires are distinct.
- This code must hold the logical input for both CLI transport tickets named above;
  it must not trigger an automatic retry. A durable caller still needs to persist the
  raw reply and source/settings identity before parsing, keep unknown outcomes across
  restart, and replay confirmed results only for the same identity. That caller
  adoption remains outside this API task's four-file scope.
- Final fixed-source checks: 94 tests passed across `test_video_automation_judge.py`,
  `test_video_speech_check.py` and `test_jev_client.py`; all five inspected source hashes
  stayed equal before/after. The 36 new MockTransport cases cover lost reads, 502,
  non-JSON success, a never-opened connection followed by a lost answer, safe connection
  retry then success, and the original settled refusals at each endpoint.
- Regression check: with the two original API modules restored from base
  `a3e8fb0869dc80ded38f572e80314f276dc7c72e`, all nine selected uncertainty cases failed
  on the old generic error code; both modified modules were restored byte-for-byte
  afterward. Root `ruff check .`, `mypy app` (461 files) and `mypy tests` (366 files)
  passed after the three test formatting fixes. Independent final source review found
  no blocking defect.
- The contract is recorded here and in the draft PR for the existing CLI tickets.
  No message or PR comment was sent to their owners, and no owner acknowledgment is
  claimed; the communication checkbox remains open. Keep this task in review while
  that handoff and the draft are reviewed.
- Local tests only: no real Jev/TTS/ASR request, quota/account change, production write,
  deployment, activation, approval or YouTube action. This does not start DevDay or
  complete the normal pipeline's durable restart contract.

## 2026-10-07 看板總整理（由站主授權，非原持有者）

標記完成。依據：Codex #1254 landed in train #1348 (ee20f935): jev_outcome_uncertain_response / video_judge_outcome_uncertain in apps/api/app/video_speech/admin_api.py and video_automation/admin_api.py, tests in test_video_automation_judge.py:404 and test_video_speech_check.py:409; all DoD items ticked; the caller handoff is in Notes and the code is held by tools/video/automation/client.mjs (status review, stale claim from 2026-10-05)
未勾的「通知 CLI 兩張票的持有者」已無對象：2026-10-04-prevent-automatic-retries-of-paid-video 與 2026-10-04-prevent-paid-speech-retries-after-ambiguous 都已在 tasks/done。
