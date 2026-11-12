---
id: 2026-11-12-add-minimax-speech-as-a-third
title: Add MiniMax speech as a third narration voice provider
status: review
priority: P2
area: api
owner: claude-opus-5.5-minimax-speech
claimed_at: 2026-11-12T00:24:43Z
created_at: 2026-11-12T00:24:22Z
completed_at:
branch: claude/fervent-dijkstra-vqykpz
depends_on: []
scope:
  - apps/api/app/video_speech/minimax.py
  - apps/api/app/video_speech/admin_api.py
  - apps/api/app/video_speech/schemas.py
  - apps/api/app/providers/usage_meter.py
  - apps/api/app/config.py
  - apps/api/tests/test_video_speech_minimax.py
  - tools/video/tts/requests.mjs
  - tools/video/tts/cli.mjs
  - tools/video/tts/minimax.test.mjs
  - tools/video/core/schema.mjs
  - tools/video/tts/client.mjs
  - tools/video/cli.mjs
  - apps/web/app/api/video/speech/minimax-quota/route.ts
  - apps/web/app/api/video/speech/route.test.ts
  - tasks/open/2026-11-12-add-minimax-speech-as-a-third.md
  - apps/web/components/trip-editor.test.tsx
  - apps/api/tests/test_trip_creation.py
---

# Add MiniMax speech as a third narration voice provider

## Why

The owner pays MiniMax a monthly M Plan (formerly Token Plan) subscription and asked on
2026-11-12 to narrate with its speech "the way the pictures are made": through the server on
the site's MiniMax key (`minimax_api_key`, `minimax_api_base_url`, image-01's), not the
MiniMax Audio web app. The narration server only knew Azure and Gemini. The owner also asked,
the same day, to read the plan's remaining quota.

## Definition of done

- [x] A `video.json` voice `{ "provider": "minimax", "name": "<voice id>" }` (optional `rate`,
  `model` speech-2.8-hd | speech-2.8-turbo, no `style`) passes lint and is narrated by
  `POST /api/v1/video/speech` with `voice: "minimax:<voice id>"`, returning 24 kHz mono WAV the
  tool resamples to 48 kHz.
- [x] MiniMax has its own month of text characters (`VIDEO_SPEECH_MINIMAX_MONTHLY_CHARACTER_LIMIT`,
  default 300,000), refunded on a refusal and kept on a lost answer (504).
- [x] `GET /speech/status` reports `minimax_configured`, `minimax_models`, `minimax_voices`,
  `minimax_monthly_limit`, `minimax_used`; `audition --voices minimax:<id>` works.
- [x] `node tools/video/cli.mjs minimax-quota [--json]` prints the plan's remaining quota through
  `GET /api/video/speech/minimax-quota` -> `GET /api/v1/video/speech/minimax/quota`.
- [ ] Deployed, and one real call each (narration and quota) checked on production with the
  owner's key.

## Steps

- [x] `apps/api/app/video_speech/minimax.py`: request, text rules, answer parsing, error codes,
  quota call.
- [x] Route, status fields, settings, usage-meter key; tests in
  `apps/api/tests/test_video_speech_minimax.py`.
- [x] Tool: schema, `voiceFields`, `minimaxText`/`billableForRequest`, CLI voice checks,
  audition, `minimax-quota`; tests in `tools/video/tts/minimax.test.mjs`.
- [x] Web route `apps/web/app/api/video/speech/minimax-quota/route.ts` and its proxy test.
- [ ] After deploy: `node tools/video/cli.mjs minimax-quota --json` and an audition with
  `--voices "minimax:Chinese (Mandarin)_News_Anchor"`; write down the answer's real fields here.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_speech_minimax.py tests/test_video_speech*.py
node --test tools/video/tts/minimax.test.mjs
npm run test:tools && npm run test:web
```

## Notes

- Sources read 2026-11-12: T2A v2 https://platform.minimax.io/docs/api-reference/speech-t2a-http,
  voices https://platform.minimax.io/docs/faq/system-voice-id, error codes
  https://platform.minimax.io/docs/api-reference/errorcode, plan FAQ
  https://platform.minimax.io/docs/m-plan/faq (the only source for the quota URL).
- **The quota answer's fields are not published.** The FAQ gives only
  `curl https://www.minimax.io/v1/token_plan/remains -H 'Authorization: Bearer <M Plan key>'`.
  The server checks `base_resp` and passes the rest on bounded (depth 5, 100 items, 200-char
  strings); the CLI prints every list entry with whatever fields came. The China host
  `www.minimaxi.com` (used when the base is `api.minimaxi.com`, the site default) is inferred
  from the API hosts, not from a page: if it 404s, switch the base to `api.minimax.io` or fix
  `_QUOTA_HOSTS`.
- M Plan keys and pay-as-you-go keys are not interchangeable (FAQ). 2057 = not a plan key,
  2062 on the quota = no active plan; both answer `video_speech_upstream_rejected_key` with a
  message saying so. A plan refusal while narrating (1008/2053/2061/2067/2068/2069) uses the same
  code on purpose: the tool reads it as settled and the owner's to fix, while a new 502 code
  would read as possibly paid and stop the run as uncertain.
- 24 kHz because `tools/video/tts/wav.mjs` only upsamples by a whole factor of 48 kHz; MiniMax's
  32 and 44.1 kHz are not.
- Pilot films (`video_budget`) are refused before the call (`max_usd=None`), like Azure: whether
  a call costs the subscription or a balance depends on the key, so no price is known.
- No Taiwanese-accent system voice exists; the curated list in `SYSTEM_VOICES` is Mandarin.
  Cloned voice ids work by name.
- Not done, left for later: `emotion` (MiniMax's fixed list, no free-text style), drama
  `performance`/`emotion` cues and dubs (those still require Gemini), the worker's settings
  voice picker (`tools/video/automation/flow.mjs` drops `model` for non-Gemini voices), and an
  admin card for the quota.
- Claimed with `--force` over three stale claims whose scopes overlap `apps/api/app/video_speech`
  and `tools/video/tts` (2026-10-09-dub-skipped..., 2026-10-16-bind-story-audits...,
  2026-10-19-worker-video-languages-five): claimed 2026-10-17 to 2026-11-01, no branch on origin.
- CI on the PR (#2081) went red in web-unit on `components/trip-editor.test.tsx` (4 tests) and
  would in api-tests on `tests/test_trip_creation.py::test_blank_trip_preferences_are_normalized_for_persistence`:
  both have fixture trips dated 2026-11-10/11, now past, and fail identically on `origin/main`.
  The trip-editor fix is the same hunk as open PR #2060 (pin the system time to 2026-11-10);
  the API test now takes dates relative to today. `tools/deploy-host-verify.test.mjs` fails only
  in this cloud container (its awk panics on `REcompile()`), not on GitHub's Ubuntu runners.
