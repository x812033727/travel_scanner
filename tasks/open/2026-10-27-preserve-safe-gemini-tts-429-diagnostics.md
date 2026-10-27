---
id: 2026-10-27-preserve-safe-gemini-tts-429-diagnostics
title: Preserve safe Gemini TTS 429 diagnostics
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-27T01:45:43Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_speech/gemini.py
  - apps/api/tests/test_video_speech_gemini.py
---

# Preserve safe Gemini TTS 429 diagnostics

## Why

Four bounded Curio S31 narration commands returned the same Gemini busy/quota message without producing a replacement WAV. The site still reported more than 5.7 million monthly speech characters available. The current Gemini adapter retains upstream HTTP status and Retry-After but discards the structured error body, so the available evidence cannot tell a provider quota refusal from temporary availability or identify a usable retry delay.

The public API already distinguishes `video_speech_upstream_busy` from the site's own `rate_limit_exceeded`. Keep that behavior and add bounded, safe server-side evidence at the adapter boundary so an operator can diagnose the provider refusal without replaying a synthesis request.

## Definition of done

- [ ] Existing upstream 429 failures emit a bounded diagnostic record containing HTTP status and finite-allowlist error status/reason, recognized QuotaFailure presence/count or quota scope, and a validated RetryInfo delay when supplied.
- [ ] Missing or unrecognized details remain unknown; an HTTP 429 alone is not labeled as a daily quota exhaustion or a known reset time.
- [ ] The diagnostic omits raw messages/bodies, narration, audio, API keys, request URLs, consumer/project identifiers and unknown metadata. Oversized or malformed JSON is handled without expanding logs.
- [ ] Existing response codes, Retry-After handling, reservations/refunds, uncertain-request classification and number of synthesis submissions are unchanged.

## Steps

- [ ] Recheck main, branches, worktrees and PRs before claiming the two-file scope; coordinate the overlapping pilot-budget work noted below.
- [ ] Add a small bounded extractor and structured adapter log using finite allowlists and validated numeric delays.
- [ ] Add offline fixtures for recognized quota/retry details, missing fields, malformed/oversized JSON, hostile secret echoes and invalid/oversized delays.
- [ ] Verify a failure still makes the same number of HTTP submissions and preserves the current status/retry/uncertain behavior.

## How to verify

From `apps/api`, run `uv run pytest tests/test_video_speech_gemini.py -q` and `uv run ruff check app/video_speech/gemini.py tests/test_video_speech_gemini.py`, plus the existing relevant speech tests when behavior is exercised. Use mocked HTTP responses and captured logs; assert forbidden fixture secrets never appear. Run `npm run check:tasks` from the repository root. No live synthesis is needed.

## Notes

- Current scope collision: `2026-10-14-enforce-usd-25-all-in-cap` includes both files and has a declared branch. Its owner is empty in this checkout; that does not prove another worktree or PR is inactive. This new ticket is filed unclaimed.
- Related completed tickets cover ASR resilience, site-token limits, and known-versus-lost provider answers; the open news upstream-status ticket targets `news_automation/validation.py`. None directly covers this Gemini synthesis diagnostic gap.
- Current primary pointers: `gemini.py` HTTPStatusError mapping and `admin_api.py` upstream-busy/site-limit branches. Keep any logger output behind the existing failure path and preserve the public error contract.
- S31 receipts remain outside Git under `~/mokaair-work/curio-s31-v2-preflight/`; public sanitized production evidence is `docs/videos/curio-s31-v2/speech-retry-20261027-0930.json`. The most recent command's actual native exit 4 was captured immediately; no replacement WAV or unsettled journal remained.
- Implementation/deployment and provider, key, voice or budget changes are separate from filing this observability follow-up. The S31 producer continues under its recorded backoff.
