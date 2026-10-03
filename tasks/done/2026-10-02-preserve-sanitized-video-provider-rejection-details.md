---
id: 2026-10-02-preserve-sanitized-video-provider-rejection-details
title: Preserve sanitized video provider rejection details
status: done
priority: P1
area: api
owner: codex-video-provider-20261003
claimed_at: 2026-10-03T11:23:54Z
created_at: 2026-10-02T19:01:29Z
completed_at: 2026-10-03T11:33:15Z
branch: codex/unfinished-tickets-20261003
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

- [x] A rejected video-media request retains a bounded, sanitized provider diagnostic in the existing error path, sufficient to distinguish an explicit unsupported-parameter response from a safety rejection when the provider supplies that distinction.
- [x] API keys, bearer tokens, credential-bearing query strings, signed URLs, full prompts, image/base64 data and other request secrets are never included in retained errors or logs; do not store an unfiltered response body.
- [x] Missing, malformed, non-JSON or oversized vendor error bodies produce a safe generic fallback.
- [x] Existing error status/kind semantics, safety decisions, pinned provider hosts, approval/budget gates, reservations and retry behavior remain unchanged; this task does not authorize paid reproduction or resubmission.
- [x] Focused tests cover useful sanitized rejection detail, secret redaction, safe fallbacks and unchanged existing error classifications.

## Steps

- [x] Inspect the common `raise_for_status` / `post_json` path and existing provider tests; choose bounded allowlisted diagnostic fields with explicit redaction.
- [x] Add an offline regression fixture for a 400 `INVALID_ARGUMENT` unsupported-parameter response plus adversarial secret-containing and non-JSON error fixtures.
- [x] Implement only in the declared provider helper and existing test file, retaining all request and retry guardrails.

## How to verify

```bash
cd apps/api
uv run pytest tests/test_video_media_providers.py -q
uv run ruff check app/video_media/providers/__init__.py tests/test_video_media_providers.py
```

The tests must make no live provider requests. Inspect captured errors/logs for the
redaction fixture sentinels; a passing status code alone is insufficient.

## Notes

- Final local completion by root on 2026-10-03 supersedes the author's earlier review/no-archive handoff status below: the final provider/job-state selection passed all 64 cases, and all three changed Python files passed Ruff and mypy. Root independently reviewed the bounded request/diagnostic behavior and archived only this implementation ticket. Original RED logs and author receipts are retained. No paid model call, production deployment or real media acceptance is claimed; current-head PR CI is recorded separately.

- Filed only, intentionally `open` and unclaimed; no provider code changed.
- Existing tasks/open and tasks/done were searched for the generic refusal/HTTP 400 diagnostic gap. The separate open Kling provider ticket does not cover it.
- `who-is-on-it.mjs` found no active claim or open PR touching either declared path when filed. Recheck before claiming; this is not a lock.
- Sanitized production evidence is summarized in `docs/videos/series-plans/competition-20261002/episodes/production-run-20261003.md`; raw private receipts stay outside Git. Never replay a paid request merely to reproduce this ticket.
- Model-specific removal of unsupported `negativePrompt` is tracked by `2026-10-02-honor-veo-lite-negativeprompt-compatibility`; this ticket concerns preserving diagnostics, not changing parameters or inferring that all 400s mean safety failures. Both tickets share the existing provider test file, so coordinate sequential claims before implementation.
- Verified local `diagnostic-r02/transport.jsonl` SHA-256 `0111f51712753cb8ed6578b248b82317a3b2d0c2b85f571b04ab663b84f16f47` preserves the sanitized HTTP 400 / `INVALID_ARGUMENT` response identifying unsupported `negativePrompt`. Its normal job receipt still retained only `video_media_rejected`; the separately scoped R03 payload returned HTTP 200 and a ready file after dropping that field while keeping the avoidance instructions in the main prompt. This confirms why actionable error details must survive the common helper; visual QA remains separate.

### 2026-10-03 local implementation and review

- Implementation collision gate: `<home>/.codex/tmp/video-provider-fixes-20261003/scope-gate.json`, result `IMPLEMENTATION_COLLISION_PASS_WITH_AUTHORIZED_METADATA_EXCEPTION`. The normal claim was refused by retained review metadata for `2026-10-03-illustrated-slides-round-2-a-family`; PR #1172 is merged at `b0a2645`, its provider/test implementation is present, and scoped branch/worktree checks found no active implementation overlap. The coordinating owner explicitly authorized narrow forced claims for these two tickets under one owner, including their shared test file. The illustrated review ticket, owner and remaining receipt/deploy acceptance Steps were preserved. This is not a claim that the normal gate passed.
- Local validation used Python 3.13.15 and only fake providers/session/Redis or `httpx.MockTransport`: provider module 46 passed; provider plus existing job state-machine module 64 passed in 23.83s (exit 0); scoped Ruff passed; scoped mypy passed for all three changed files. Logs, original bytes and final source/test hashes are under the same private directory; `implementation-receipt.json` records final bindings. No provider submission, paid reproduction, production connection, settings change, uploader activation, reservation change or automatic retry was performed.
- Independent coordinator review of the three-file diff passed before the final line-ending normalization. Status remains `review` for the shared PR handoff; no archive, merge, deployment or media/owner acceptance is claimed. The code change does not rebind or complete the separate illustrated-video production receipt.
- HTTP 400 diagnostic extraction accepts a bounded Google-style error envelope (at most 8 KiB body and 2 KiB message). Only fixed allowlisted status/parameter names and canonical unsupported-parameter or explicit safety categories leave the helper; arbitrary message/details, URLs, prompt text and media bytes are discarded. Unknown or unusable envelopes retain the generic refusal. Existing status/kind/retry behavior is unchanged.
- Meaningful pre-fix regression: 7 failed / 18 passed (exit 1), all missing actionable diagnostic assertions. The new cases cover unsupported versus safety causes, a statement explicitly denying safety rejection, adversarial key/token/signed-URL/prompt/base64 sentinels in error fields and captured logs, malformed/oversized/deep/unread bodies, unchanged other HTTP classifications, and propagation through one mocked submit without resubmission.
- The existing `jobs._fail` path persists the bounded `error.message`; its code was not changed. [Google AIP-193](https://google.aip.dev/193) supplies the documented nested error envelope. This parser intentionally does not retain untrusted free-form diagnostics or interpret every HTTP 400 as a content-safety refusal. Poll-result behavior and other adapter paths are outside this HTTP rejection correction.
