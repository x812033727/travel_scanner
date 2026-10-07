---
id: 2026-10-07-jev-s-unconfigured-503-is-held-as
title: Jev's unconfigured 503 provider_unavailable is held as an uncertain paid answer, though nothing ran
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-jev-unset
claimed_at: 2026-10-07T10:59:59Z
created_at: 2026-10-07T11:05:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - tools/video/tts/speech-journal.test.mjs
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

- [x] A paid Jev call answered 503 `provider_unavailable` is told as the owner's (a key to set),
  with no hold in the speech journal and no "may have run". The same code with any other status
  stays uncertain.

## Steps

- [x] Treat `{ status: 503, code: "provider_unavailable" }` as an owner refusal in each client
  (as `video_speech_not_configured` and `video_ai_provider_not_configured` are), checked before
  the uncertain branch.
- [x] Tests in each client's file: the 503 is thrown once as the owner's, with no journal entry
  left; a 500 with the code stays uncertain.

## How to verify

`node --test tools/video/tts/client.test.mjs tools/video/tts/speech-journal.test.mjs tools/video/shorts/site.test.mjs tools/video/automation/client.test.mjs`.

## Notes

- Found by the review of `2026-10-07-the-speech-and-shorts-clients-hold` (2026-10-07), which
  reproduced it in a scratch copy: `judgeLines` against that answer gave `video_speech_uncertain`
  (owner) after one call.
- Check first that no other API path answers `provider_unavailable` after a provider call ran.
- 2026-10-07 (claude-opus-5-5-jev-unset). On the video tool routes, only `jev_client` answers
  `provider_unavailable` (the other API hits are flight search and other features). It is the
  first statement of `checking.judge` and of `video_automation/judge.py` `_ask`, before
  `consume_jev_call` and the Jev request.
- Each client now has `JEV_NOT_SET = { status: 503, code: "provider_unavailable" }`. It is the
  owner's answer and is thrown at once, before the uncertain branch:
  - `tts/client.mjs` (`ownersAnswer`): an owner `SpeechError`, so the speech journal removes the
    entry as for any settled answer, and nothing is held for `forget`;
  - `shorts/site.mjs`: an owner `SiteError`, with no retry;
  - `automation/client.mjs`: an owner `AutomationError` for `judgePolicy` and `judgeOutline`.
  The code with any other status stays uncertain.
- Tests, each failing on the old code: the 503 is told once as the owner's in each client's
  owner or refusal table; through the journal it leaves nothing behind and the next run sends it.
  The lost tables gain the code at a 500, which stays uncertain (and passes on both). Accepting
  the code at any status fails a test in each client. `tts/speech-journal.test.mjs` joined the
  scope for its row.
