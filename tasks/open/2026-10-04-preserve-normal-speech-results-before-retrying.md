---
id: 2026-10-04-preserve-normal-speech-results-before-retrying
title: Preserve normal speech results before retrying uncertain paid requests
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-tts-client-paid-retries
claimed_at: 2026-10-05T00:14:55Z
created_at: 2026-10-04T13:06:25Z
completed_at:
branch: claude/tts-client-paid-retries
depends_on: []
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
---

# Preserve normal speech results before retrying uncertain paid requests

## Why

The shared native speech client defaults to five attempts for a synchronous paid
POST. Losing a response can repeat synthesis, transcription or audio judgment
after the first server operation has already completed. Normal videos still use
that client behavior. The isolated approved-final language runner now has a
source-bound fetch journal, but that protection is scoped to its six current
sources and must not be reported as a general speech-client fix.

## Definition of done

- [x] A lost paid POST or response body cannot trigger another paid dispatch in
  the normal client; safe GET retries and owner/quota classification still work.
- [ ] Confirmed complete response bytes can be consumed without being bought
  again; unresolved results remain a visible hold rather than fake success.
- [x] Preserve current source, voice, model and budget authority and never infer
  listening acceptance from an HTTP response or local audio check.

## Steps

- [ ] Choose a result-preserving contract before extending beyond the current
  batch journal; inspect real native consumers and current backend capabilities.
- [ ] Exercise real synthesize/transcribe/judge consumers with lost POST, lost
  body, corrupt result, changed request and restart fixtures.

## How to verify

Use an injected counting fetch with the actual native client. A dropped paid
response must submit once, not five times. Verify owner and exhausted-budget
errors retain their existing meaning and no test calls a live paid endpoint.
Run the affected tools tests and the repository tools suite.

## Notes

- Found during the 2026-10-04 video recovery. The existing call loop is in
  tools/video/tts/client.mjs; default attempts are five and network/429/5xx retry.
- docs/videos/imported-long-languages/speech-journal.mjs is a reviewed local
  reference with raw WAV/JSON preservation and unknown-result holds. Its 54
  native-consumer regressions passed independently; do not simply enable that
  source-specific contract for unrelated projects or weaken existing gates.
- This is an unclaimed follow-up, not completed or deployed work. Expand scope
  only after checking active claims if integration requires other files.

### 2026-10-05 closed in part, rest split (claude-opus-5-5-tts-client-paid-retries)

- Done with 2026-10-04-prevent-paid-speech-retries-after-ambiguous in the same PR (branch
  claude/tts-client-paid-retries): `tools/video/tts/client.mjs` no longer replays a paid POST
  (`speech`, `speech/transcribe`, `speech/judge`) whose outcome is unknown. A lost POST, a 5xx
  without the API's settled code, or a body that breaks off or cannot be read throws
  `SPEECH_UNCERTAIN` (who "owner", exit 3) with `path` and `requestSha256` after one dispatch;
  never-sent connect errors, settled codes and the status GET keep the bounded retry; owner
  codes, 401 and both exhausted budgets keep their meaning. The classification, the caller audit
  and the backend codes are written up in that ticket's Notes.
- DoD 3 is ticked for this change only: the client sends the caller's body unchanged, returns
  only the answer that request received (billable from that answer's header) and decides
  nothing about listening. The follow-up carries the same constraint.
- Not done, moved to 2026-10-05-reuse-confirmed-speech-results-across-restart (split from this
  ticket): DoD 2 and both Steps, that is, choosing the durable result-preserving contract,
  reusing confirmed bytes across a restart for `synthesis.mjs` (receipt-bound),
  `shorts/speech.mjs` and `dubs/cli.mjs`, holding a request recorded as sent without an answer
  across runs, and the changed-request and restart fixtures. The lost-POST, lost-body and
  corrupt-result cases are exercised against the real `synthesize`, `transcribeClip` and
  `judgeLines` in `tools/video/tts/client.test.mjs`; the consumer-level fixtures are part of the
  follow-up.
- Backend capability checked: the speech endpoints take no idempotency key and keep no answer
  to fetch again, so a client-side journal is the only way to reuse a paid result.
- Claimed with `--force`: the only overlapping claim was this agent's own claim of
  2026-10-04-prevent-paid-speech-retries-after-ambiguous on the same branch (same two files).
