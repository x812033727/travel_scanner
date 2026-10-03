---
id: 2026-10-02-honor-veo-lite-negativeprompt-compatibility
title: Honor Veo Lite negativePrompt compatibility
status: done
priority: P1
area: api
owner: codex-video-provider-20261003
claimed_at: 2026-10-03T11:23:54Z
created_at: 2026-10-02T19:02:53Z
completed_at: 2026-10-03T11:33:09Z
branch: codex/unfinished-tickets-20261003
depends_on: []
scope:
  - apps/api/app/video_media/providers/gemini_video.py
  - apps/api/tests/test_video_media_providers.py
---

# Honor Veo Lite negativePrompt compatibility

## Why

`GeminiVideo.request_body` already handles several capabilities of
`veo-3.1-lite-generate-preview`, but it still sends `parameters.negativePrompt`
whenever a request has a negative prompt. On 2026-10-03, the E1 S01 pilot and its
separately authorized diagnostic submit failed before returning an operation.
The diagnostic for job `fc63bb73-174e-49ee-96c1-23a1289541fa` obtained HTTP 400
`INVALID_ARGUMENT`: `negativePrompt` is not supported by this model. This is a
confirmed parameter-compatibility failure; it is not evidence of a content safety
rejection.

The production owner submitted a separately bound R03 manifest that omits the
unsupported field while preserving the same scene constraints in the main prompt.
The HTTP response became 200 and job `340951d1-4f13-43fb-91fe-c6f42c40f032` later
returned a ready file. Later visual QA rejected that file for a second watch and
extra hand movement; transport success is separate from usable footage. The
scoped workaround does not repair the shared adapter for future Lite jobs.

## Definition of done

- [x] Lite requests never send the unsupported `parameters.negativePrompt` field, while preserving the requested scene constraints through supported input rather than silently dropping them.
- [x] The handling is specific to verified model capabilities; other video models retain their supported request behavior.
- [x] Existing Lite rules for first frames, reference images, 1080p/eight-second requests and native audio remain covered.
- [x] `personGeneration=allow_adult`, model choice, source frames, provider host/key safeguards, approval/budget guards and retry/reservation behavior are unchanged.
- [x] Offline request-body tests reproduce the unsupported field and verify the corrected model-specific payload without a paid call.

## Steps

- [x] Recheck the pinned Lite model's supported inputs against official API documentation and the sanitized captured `INVALID_ARGUMENT` evidence.
- [x] Add a regression in the existing provider test file covering Lite with a negative prompt, preserved constraints, and a non-Lite request that still supports its existing field.
- [x] Implement the narrow request-body compatibility fix, with no model fallback, safety relaxation, automatic retake or production configuration change.

## How to verify

```bash
cd apps/api
uv run pytest tests/test_video_media_providers.py -q
uv run ruff check app/video_media/providers/gemini_video.py tests/test_video_media_providers.py
```

Inspect generated request bodies under the existing mock transport. No live model
invocation is needed to verify omission of an unsupported parameter.

## Notes

- Filed only, intentionally `open` and unclaimed; no provider code was changed in this reporting task.
- Searched current tasks/open for Lite, negativePrompt and unsupported-parameter work; no existing ticket covered this compatibility gap. Scope checks found no active task or open PR touching `gemini_video.py` or the provider test file at filing time; recheck before claiming.
- `2026-10-02-preserve-sanitized-video-provider-rejection-details` separately covers discarded provider diagnostics. Both tickets use `test_video_media_providers.py`, so coordinate sequential claims or explicitly combine their test work; do not race the file.
- The failed diagnostic still consumed a conservative reservation. Keep its failed job and receipts; do not replay it or treat the generic app classification `blocked` as a reason to bypass safety checks.
- Local sanitized evidence is referenced by `docs/videos/series-plans/competition-20261002/episodes/production-run-20261003.md`; original provider credentials and request image data remain outside Git.
- Verified local `diagnostic-r02/transport.jsonl` SHA-256 `0111f51712753cb8ed6578b248b82317a3b2d0c2b85f571b04ab663b84f16f47` records HTTP 400 / `INVALID_ARGUMENT` and explicitly identifies unsupported `negativePrompt`. R03 `diagnostic-r03/transport.jsonl` SHA-256 `3b24d7859fa89081a5a41b8a71406eeb458e146fbc8054bde19d24529e317d99` records HTTP 200 after removing that API field; all avoidance text was retained in the main prompt.

### 2026-10-03 local implementation and review

- Implementation collision gate: `C:/Users/x8120/.codex/tmp/video-provider-fixes-20261003/scope-gate.json`, result `IMPLEMENTATION_COLLISION_PASS_WITH_AUTHORIZED_METADATA_EXCEPTION`. The normal claim was refused by retained review metadata for `2026-10-03-illustrated-slides-round-2-a-family`; PR #1172 is merged at `b0a2645`, its provider/test implementation is present, and scoped branch/worktree checks found no active implementation overlap. The coordinating owner explicitly authorized narrow forced claims for these two tickets under one owner, including their shared test file. The illustrated review ticket, owner and remaining receipt/deploy acceptance Steps were preserved. This is not a claim that the normal gate passed.
- Local validation used Python 3.13.15 and only fake providers/session/Redis or `httpx.MockTransport`: provider module 46 passed; provider plus existing job state-machine module 64 passed in 23.83s (exit 0); scoped Ruff passed; scoped mypy passed for all three changed files. Logs, original bytes and final source/test hashes are under the same private directory; `implementation-receipt.json` records final bindings. No provider submission, paid reproduction, production connection, settings change, uploader activation, reservation change or automatic retry was performed.
- Independent coordinator review of the three-file diff passed before the final line-ending normalization. Status remains `review` for the shared PR handoff; no archive, merge, deployment or media/owner acceptance is claimed. The code change does not rebind or complete the separate illustrated-video production receipt.
- Only exact `veo-3.1-lite-generate-preview` moves the complete negative prompt to `prompt` after `\n\nAvoid: ` and omits `parameters.negativePrompt`. Non-Lite bodies, frames, personGeneration, resolution, seed, native-audio handling and model/host/key behavior remain unchanged. The input dataclass is not mutated.
- Meaningful pre-fix regression: 3 failed / 4 passed (exit 1), specifically the lost avoidance prompt and unsupported field in the mocked submit. The seven new cases then passed with the existing Lite guard tests; the mocked submit records exactly one POST.
- Opened the [official Veo documentation](https://ai.google.dev/gemini-api/docs/veo) and [Gemini troubleshooting](https://ai.google.dev/gemini-api/docs/troubleshooting). The current Veo parameter table does not list negativePrompt; that omission alone is not asserted as proof. The specific incompatibility is evidenced by the original task's sanitized R02 receipt and repository production-run report. R03 transport success remains separate from the subsequently rejected footage. No historical paid request was replayed.
