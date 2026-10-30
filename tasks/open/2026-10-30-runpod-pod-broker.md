---
id: 2026-10-30-runpod-pod-broker
title: RunPod pod broker: video tools start and stop GPU pods through the site without the API key
status: review
priority: P2
area: api
owner: claude-opus-5-5-runpod
claimed_at: 2026-10-30T01:18:54Z
created_at: 2026-10-30T00:37:19Z
completed_at:
branch: claude/runpod-pod-broker
depends_on:
  - 2026-10-30-runpod-admin-settings
scope:
  - apps/api/app/video_runpod
  - apps/api/app/main.py
  - apps/api/migrations/versions/0144_video_runpod_sessions.py
  - apps/api/app/models.py
  - apps/api/app/video_speech/admin_api.py
  - apps/api/app/video_speech/pairing.py
  - apps/api/app/video_speech/schemas.py
  - apps/api/tests/test_video_runpod.py
  - apps/web/app/api/video/runpod
  - apps/web/components/admin-runpod-panel.tsx
  - apps/web/components/video-tool-tokens.tsx
  - apps/web/components/video-tool-tokens.test.tsx
  - tools/video/cli.mjs
  - tools/video/runpod
  - ops/video/worker.sh
  - apps/api/tests/test_migration_0144_video_runpod_sessions.py
  - apps/web/app/api/video/gpu-routes
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-runpod-panel.test.tsx
  - apps/web/lib/runpod-copy.ts
  - apps/web/lib/runpod-copy.test.ts
  - apps/web/lib/runpod-messages
---

# RunPod pod broker: video tools start and stop GPU pods through the site without the API key

## Why

Colab can only hand its token to an agent session. With RunPod the site can do better: keep the
API key in the API container, start and stop pods on the agent's behalf, and enforce the monthly
cap and auto-stop on the server, so a crashed or careless session cannot leave a pod billing.
The owner also wants (2026-10-30) the video tool token to decide which GPU routes an agent may
use, Colab or RunPod, and the agent to be told which one to use for a batch.

## Definition of done

- [x] `video_tool_tokens.runpod_access` (migration 0144, `down_revision = "0143_video_daily_briefs"`,
      idempotent like 0142); the token checkbox "可以開 RunPod GPU" and the pairing flow carry it
      exactly like `colab_access`.
- [x] `GET /api/v1/video/gpu-routes` (mkv_ token): the routes this token may use, each with its
      state (Colab: CU balance from the default slot; RunPod: remaining monthly cap, GPU stock and
      hourly price), and `recommended` from the admin's `gpu_route_default`. `auto` picks RunPod
      when the batch asks for a canvas above 1344×768 or Colab is short of CU or has no A100,
      otherwise Colab. A route the token lacks is never recommended.
- [x] `POST /api/v1/video/runpod/pods` starts one pod from the admin settings with a one-time gate
      token in its environment and returns `{pod_id, base_url, gate_token, cost_per_hr}`; 403
      without `runpod_access`, 409 over the monthly cap or while a pod is already running.
      `GET /pods`, `GET /pods/{id}`, `POST /pods/{id}/heartbeat`, `POST /pods/{id}/stop` (stop and settle).
- [x] Table `video_runpod_sessions` (pod_id, token_id, label, slug, gpu, cost_per_hr, started_at,
      last_heartbeat_at, stopped_at, stop_reason manual|idle|max_hours|cap, usd).
- [x] Reaper: the worker's five-minute `auto` calls `POST /video/runpod/reap`, which stops pods idle
      past `runpod_idle_stop_minutes`, older than `runpod_max_pod_hours`, or over the cap, and
      records why.
- [x] Every action audited (`runpod.pod_started|stopped|reaped`), rate-limited 30/h per token.
- [x] Admin status panel under the RunPod card: running pods with a stop button, month spend
      against the cap, the last 20 sessions.

## Steps

- [x] Migration, model, schemas.
- [x] `apps/api/app/video_runpod/` router + RunPod REST client (fakeable).
- [x] Web forwarders `apps/web/app/api/video/runpod/...` and `gpu-routes` via `forwardToSpeech`.
- [x] Token UI and pairing flag; status panel.
- [x] Reap step in `tools/video/cli.mjs auto`.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_runpod.py
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

## Notes

- The agent never sees the RunPod API key; the runner's receipt uses the `usd` the site settles.
- Both GPU skills (`minimax-h3-colab`, `minimax-h3-runpod`) must say: ask `gpu-routes` before a
  batch, use the recommended route, write the route into the `clips import --note`.
- The gpu-routes endpoint may need a file outside this scope for the Colab balance (the host
  `ai_accounts_agent`); widen the scope before touching it.

### 2026-10-30: broker built (claude-opus-5-5-runpod), stacked on #1927

- API: `apps/api/app/video_runpod/` (`client.py` REST create/get/delete, `service.py` start,
  stop, heartbeat, reap, month spend, gpu-routes, `router.py`), migration 0144 (token
  `runpod_access` + `video_runpod_sessions`), `runpod` flag through token creation and pairing.
  Admin routes are `/admin/provider-settings/runpod/sessions[...]` so they inherit the settings
  card's permission (settings.read / settings.manage) without touching `auth/service.py`.
- Changes from the plan: the tool-side stop is `POST /pods/{id}/stop`, not DELETE, because the
  web forwarder (`forwardToSpeech`) only does GET and POST; `GET /video/runpod/pods` lists the
  token's running pods, which is what a runner checks when a start's answer is lost (the start
  forwarder answers 504 `runpod_answer_lost` then, never a blind retry).
- Pods are terminated (DELETE), not stopped: the models are on the network volume, which a
  delete leaves alone. The create body follows the REST reference read 2026-10-30
  (`env` is a map, `ports` a list, `minRAMPerGPU` 64). The proxy URL
  `https://{pod}-8188.proxy.runpod.net` is RunPod's usual format but was not on the pages read.
- The row is committed before RunPod is asked; a create that never answers is marked `failed`
  after 10 minutes. Its pod (if RunPod made one) carries the row id in its name
  (`mokaair-<8 hex>-<label>`) so the owner can find it in the RunPod console; the reaper does
  not list RunPod's pods to find orphans. A follow-up could.
- gpu-routes does not read the Colab compute-unit balance (that needs the host agent, outside
  this scope): Colab is "ready" when the token has `colab_access`. `auto` sends 1088p or a GPU
  upscale to RunPod and everything else to Colab.
- The reaper runs as `node tools/video/cli.mjs runpod-reap` after each `auto` round in
  `ops/video/worker.sh` (the API worker is a plain RQ worker with no schedule, and
  `tools/video/automation` is held by the daily-brief ticket). Any active video tool token may
  call it; it can only stop pods.
- Strings live in `apps/web/lib/runpod-messages/*.json` (`tokens`, `panel`), not admin.json,
  for the receipt reason recorded in `2026-10-30-runpod-admin-settings`.
- Not done: `tools/video/tts` `login --runpod` (the CLI flag that asks for the flag when
  pairing; the API and admin card accept it already) — outside this scope.
- Verified: API `test_video_runpod.py` + migration test (29 + 1 skipped integration), pairing /
  speech / Colab suites (104), migration+route subset (448), ruff, mypy; web lint, typecheck,
  i18n, four vitest files (71); `runpod-reap` node tests (3);
  `node tools/video/long-form/cli.mjs check` PASS. `npm run test:tools` had 7 failures, all in
  areas this change does not touch (adult-English, Drive backup, elementary renderer, second
  transcript; the known Windows-only set) plus the receipt test, which the copy move fixed.
