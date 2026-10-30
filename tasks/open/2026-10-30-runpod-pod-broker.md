---
id: 2026-10-30-runpod-pod-broker
title: RunPod pod broker: video tools start and stop GPU pods through the site without the API key
status: in-progress
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
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# RunPod pod broker: video tools start and stop GPU pods through the site without the API key

## Why

Colab can only hand its token to an agent session. With RunPod the site can do better: keep the
API key in the API container, start and stop pods on the agent's behalf, and enforce the monthly
cap and auto-stop on the server, so a crashed or careless session cannot leave a pod billing.
The owner also wants (2026-10-30) the video tool token to decide which GPU routes an agent may
use, Colab or RunPod, and the agent to be told which one to use for a batch.

## Definition of done

- [ ] `video_tool_tokens.runpod_access` (migration 0144, `down_revision = "0143_video_daily_briefs"`,
      idempotent like 0142); the token checkbox "可以開 RunPod GPU" and the pairing flow carry it
      exactly like `colab_access`.
- [ ] `GET /api/v1/video/gpu-routes` (mkv_ token): the routes this token may use, each with its
      state (Colab: CU balance from the default slot; RunPod: remaining monthly cap, GPU stock and
      hourly price), and `recommended` from the admin's `gpu_route_default`. `auto` picks RunPod
      when the batch asks for a canvas above 1344×768 or Colab is short of CU or has no A100,
      otherwise Colab. A route the token lacks is never recommended.
- [ ] `POST /api/v1/video/runpod/pods` starts one pod from the admin settings with a one-time gate
      token in its environment and returns `{pod_id, base_url, gate_token, cost_per_hr}`; 403
      without `runpod_access`, 409 over the monthly cap or while a pod is already running.
      `GET /pods/{id}`, `POST /pods/{id}/heartbeat`, `DELETE /pods/{id}` (stop and settle).
- [ ] Table `video_runpod_sessions` (pod_id, token_id, label, slug, gpu, cost_per_hr, started_at,
      last_heartbeat_at, stopped_at, stop_reason manual|idle|max_hours|cap, usd).
- [ ] Reaper: the worker's five-minute `auto` calls `POST /video/runpod/reap`, which stops pods idle
      past `runpod_idle_stop_minutes`, older than `runpod_max_pod_hours`, or over the cap, and
      records why.
- [ ] Every action audited (`runpod.pod_started|stopped|reaped`), rate-limited 30/h per token.
- [ ] Admin status panel under the RunPod card: running pods with a stop button, month spend
      against the cap, the last 20 sessions.

## Steps

- [ ] Migration, model, schemas.
- [ ] `apps/api/app/video_runpod/` router + RunPod REST client (fakeable).
- [ ] Web forwarders `apps/web/app/api/video/runpod/...` and `gpu-routes` via `forwardToSpeech`.
- [ ] Token UI and pairing flag; status panel.
- [ ] Reap step in `tools/video/cli.mjs auto`.

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
