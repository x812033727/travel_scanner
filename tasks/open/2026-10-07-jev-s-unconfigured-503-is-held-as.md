---
id: 2026-10-07-jev-s-unconfigured-503-is-held-as
title: Jev's unconfigured 503 provider_unavailable is held as an uncertain paid answer, though nothing ran
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T11:05:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - tools/video/shorts/site.mjs
  - tools/video/shorts/site.test.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
---

# Jev's unconfigured 503 provider_unavailable is held as an uncertain paid answer, though nothing ran

## Why

When Jev's key or base URL is empty, `apps/api/app/ai/jev.py` `jev_client` raises
`AppError(503, "provider_unavailable")`. It does so before any Jev request and before
`consume_jev_call`, so nothing ran and no quota was spent. It is the first statement of
`checking.judge` (`apps/api/app/video_speech/checking.py`, POST `speech/judge`), and the policy
and outline judges reach it the same way through `video_automation/judge.py` `_ask`.

The video tool's clients treat it as a paid 5xx they cannot settle:

- `tools/video/tts/client.mjs` throws `SPEECH_UNCERTAIN` (the owner's, exit 3). The speech journal
  holds the request, so after the owner sets the key the next run still meets the held entry
  until someone runs `speech-journal.mjs forget`.
- `tools/video/shorts/site.mjs` throws `RUN_UNCERTAIN`, whose message says Jev may have judged it.
- `tools/video/automation/client.mjs` (`judgePolicy`, `judgeOutline`) does the same.

## Definition of done

- [ ] A paid Jev call answered 503 `provider_unavailable` is told as the owner's (a key to set),
  with no hold in the speech journal and no "may have run". The same code with any other status
  stays uncertain.

## Steps

- [ ] Treat `{ status: 503, code: "provider_unavailable" }` as an owner refusal in each client
  (as `video_speech_not_configured` and `video_ai_provider_not_configured` are), checked before
  the uncertain branch.
- [ ] Tests in each client's file: the 503 is thrown once as the owner's, with no journal entry
  left; a 500 with the code stays uncertain.

## How to verify

`node --test tools/video/tts/client.test.mjs tools/video/tts/speech-journal.test.mjs tools/video/shorts/site.test.mjs tools/video/automation/client.test.mjs`.

## Notes

- Found by the review of `2026-10-07-the-speech-and-shorts-clients-hold` (2026-10-07), which
  reproduced it in a scratch copy: `judgeLines` against that answer gave `video_speech_uncertain`
  (owner) after one call.
- Check first that no other API path answers `provider_unavailable` after a provider call ran.
