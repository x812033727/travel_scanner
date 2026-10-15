---
id: 2026-10-14-enforce-usd-25-all-in-cap
title: Enforce USD 25 all-in cap for A01 and B18 pilot
status: in-progress
priority: P1
area: api
owner: codex-story-budget-cap
claimed_at: 2026-10-15T01:22:06Z
created_at: 2026-10-14T23:20:45Z
completed_at:
branch: codex/story-pilot-usd25-cap-20261015
depends_on: []
scope:
  - apps/api/app/models.py
  - apps/api/app/video_automation/ai.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/judge.py
  - apps/api/app/video_speech/admin_api.py
  - apps/api/app/video_speech/align_api.py
  - apps/api/app/video_speech/checking.py
  - apps/api/app/video_speech/gemini.py
  - apps/api/app/ai/jev.py
  - apps/api/app/video_speech/schemas.py
  - apps/api/app/video_media/jobs.py
  - apps/api/app/video_media/admin_api.py
  - apps/api/app/video_media/judge.py
  - apps/api/app/video_media/locate.py
  - apps/api/app/video_media/schemas.py
  - tools/video/media/stages.mjs
  - tools/video/media/stages.test.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/media/ledger.mjs
  - tools/video/media/client.mjs
  - tools/video/tts/cli.mjs
  - tools/video/tts/client.mjs
  - tools/video/dubs/cli.mjs
  - apps/api/app/video_budget
  - apps/api/migrations/versions/0132_video_pilot_budget.py
  - apps/api/tests/test_video_pilot_budget.py
  - apps/api/tests/test_video_automation_ai.py
  - apps/api/tests/test_video_automation_judge.py
  - apps/api/tests/test_video_media_jobs.py
  - apps/api/tests/test_video_media_api.py
  - apps/api/tests/test_video_media_judge.py
  - apps/api/tests/test_video_media_locate.py
  - apps/api/tests/test_video_media_stock.py
  - apps/api/tests/test_video_speech_pilot_budget.py
  - apps/api/tests/test_video_speech_gemini.py
  - apps/api/tests/test_video_story_policy.py
  - apps/api/tests/test_jev.py
  - tools/video/media/client.test.mjs
  - tools/video/tts/client.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Enforce USD 25 all-in cap for A01 and B18 pilot

## Why

A01 (`story-rolling-suitcase`) and B18 (`story-conveyor-belt-sushi`) are the required first brand-story pilots. Their acceptance limit is **USD 25 in total actual cost per finished film**, including media, writing and checking, speech, transcription, judge calls and retries. The current `drama.max_usd_per_video` setting is a global media estimate cap (the production UI read USD 200 on 2026-10-15), not a per-slug all-in cap. Import can start a ready story immediately, so the limit must be proven before either paid pilot begins. This ticket is a code prerequisite to the blocked [pilot](2026-09-28-video-story-pilot.md); it does not authorize deployment or paid calls.

## Definition of done

- [x] Each of the original and isolated v2 pilot slugs has a durable USD 25 limit shared by the attributed paid workflow. The server refuses a call when its conservative reservation would exceed the remaining amount; an unknown price fails closed.
- [x] Successful responses with provider usage settle their charge; uncertain responses keep a bounded reservation, and a repeated operation ID cannot dispatch twice. Other slugs and existing global limits retain their routes.
- [ ] An operator can read each pilot's reserved, settled and remaining total without exposing account secrets, and production dry-run/preflight can prove the limit before import. The read endpoint is implemented locally; live readback is pending deployment.
- [ ] Focused tests cover cross-stage accumulation, retries, timeout/unknown outcome, unknown price, exact boundary, and concurrent dispatches. The A01 and B18 finished-film ledgers are compared with provider receipts before acceptance.

## Steps

- [x] Inventory all charged routes for the two slugs and the selected live providers; account for subscription usage separately from paid API charges, with explicit conservative pricing for every paid route.
- [x] Design the durable per-slug reservation and reconciliation record, including the additive migration and operation ID. Narrow or expand this ticket's scope before touching a new migration or test file.
- [x] Apply the shared gate before the attributed media, judge, model, speech, transcription and Jev dispatches; keep the existing global quotas and other videos' behavior.
- [ ] Verify the live deployed code, provider balances, existing work/charges and release holds using an approved host entry. Keep import and paid generation stopped until the pilot preflight passes.

## How to verify

Run the focused API and video-tool tests plus type/lint checks for changed paths. Use an isolated concurrent test to show two paid stages cannot together reserve more than USD 25 for one slug. On the authorized host, read the pilot totals and provider prices/balances, then run the exact A01/B18 import dry-run without `--apply`; retain redacted evidence. Neither a local test nor an admin setting value is a live-cost receipt.

## Notes

2026-10-15 read-only audit: `tools/video/media/stages.mjs` and `ledger.mjs` gate image/clip/music media estimates on the worker; judge is checked before a call but USD 0.01 is recorded after its reply. `apps/api/app/video_media/jobs.py` reserves monthly image/clip/music units and stores a media `usd_estimate`, with no per-slug USD stop. `apps/api/app/video_automation/ai.py` checks monthly tokens but does not reserve the next call's USD; `apps/api/app/video_speech/admin_api.py` reserves monthly characters but not dollars; transcription has hourly rate limiting, and `video_speech/checking.py` counts Jev calls but drops usage. Monthly meter and series views do not produce all-in per-slug totals. Lowering the global media cap to 20 or 25 would affect other films and still leave these non-media calls outside the limit. The old image-model-pricing task is complete; it does not solve this gap. No host write, import or paid call occurred during this audit.

2026-10-15 scope/blocker audit: A trustworthy shared cap also needs the paid align/transcribe/Jev/judge entry points, speech and media schemas/meter, a PostgreSQL reservation migration, operation IDs in the video tool, and the web speech BFF forwarding the identifiers. This ticket's current scope is only a starting inventory; expand it to the exact paths before implementation. `series.py` was removed from scope because it is unnecessary for this gate and held by the five-story route ticket. The necessary `tools/video/tts/check.mjs` is modified by still-open draft PR [#1387](https://github.com/x812033727/travel_scanner/pull/1387), and the possible journal-level alternative `tools/video/tts/speech-journal.mjs` is modified by still-open draft PR [#1379](https://github.com/x812033727/travel_scanner/pull/1379). The task stays blocked and unclaimed until these scopes are released or a narrowly authorized integration path is agreed; no partial gate should be represented as a USD 25 hard cap. The journal alternative would derive the pilot slug from `<VIDEO_WORKDIR>/<slug>/audio/speech-journal`, persist a unique operation ID per paid attempt, and pass both through the speech BFF; the API must refuse unidentified pilot operations and keep uncertain reservations pending. This design is unimplemented.

2026-10-15 start: owner said 「好 開始」. This branch is based on current `origin/main` and copies this not-yet-merged ticket from draft PR #1499 so the budget implementation can be reviewed separately. Expanded scope above to exact API, worker-client, migration and test paths. The path `tools/video/tts/cli.mjs` appears in a stale 36-hour review claim (`2026-10-12-play-the-channel-intro-bumper-after`), but no local or remote branch or open PR owns that file; the two live speech PRs touch `check.mjs` and `speech-journal.mjs`, which this implementation will leave alone. This is the narrow integration path for propagating pilot slug and operation IDs through existing speech clients. `blocked` was changed to `open` for implementation and this task claimed by `codex-story-budget-cap`; production import remains blocked until the cap is complete, deployed and independently read back.

2026-10-15 implementation/read-only review: `video_pilot_budgets` and operation rows cover both legacy and `-v2` pilot slugs at USD 25 each. MiniMax image-01, Gemini 3.8 Flash text/transcription, Gemini 3.8 Flash TTS, Jev and optional Lyria have explicit ceilings and a dated price window; generated clips, Gemini images, and Azure speech/align fail closed for pilots until priced. The media status API exposes exact reserved/settled/remaining totals. A lost or vendor-busy answer leaves its operation held; an uncertain job remains in the worker's pending cache. Independent review found a failed-job retry race, so the existing media job row is now locked before checking/requeueing and the lock is released before advancing it. Scoped API, Node, Ruff and mypy checks pass; the PostgreSQL concurrency/integration tests require a local database and have not run on this Windows host. Media success records the published fixed list price, not a vendor billing receipt; the finished-film acceptance still requires vendor statement reconciliation. The generic video-tool token trusts the caller's declared project slug; the official pilot CLI now supplies it, but direct requests omitting or spoofing it are outside this gate. The existing speech journal keeps its original body hash rather than the server operation UUID, so crash recovery may require a host budget-record lookup. No deploy, production import, vendor call or paid generation occurred.
