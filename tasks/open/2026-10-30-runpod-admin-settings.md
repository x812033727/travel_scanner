---
id: 2026-10-30-runpod-admin-settings
title: RunPod GPU provider card in admin settings
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-runpod
claimed_at: 2026-10-30T00:42:06Z
created_at: 2026-10-30T00:37:00Z
completed_at:
branch: claude/runpod-video-workflow-plan-c111be
depends_on: []
scope:
  - apps/api/app/config.py
  - apps/api/app/admin/service.py
  - apps/api/app/video_runpod/__init__.py
  - apps/api/app/video_runpod/probe.py
  - apps/api/tests/test_admin_readiness.py
  - apps/api/tests/test_admin_runpod_settings.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# RunPod GPU provider card in admin settings

## Why

The owner is moving the H3 clip route from Google Colab to RunPod (RTX 6000 Ada 48 GB, 1080p
output; plan 2026-10-30). Every RunPod setting the route needs has to live in the admin, not in
env files or an agent's chat: the API key, the GPU type, the data centre and network volume the
models sit on, the pinned image, and the spending guards that stop a forgotten pod.

## Definition of done

- [x] `/admin/settings` shows a "RunPod GPU" card under the video media category, stored in
      `provider_configs` (Fernet-encrypted secret) like `stock_photos`.
- [x] Fields: `runpod_api_key` (secret); `runpod_api_base_url` (default `https://rest.runpod.io/v1`,
      pinned to `rest.runpod.io`; GraphQL `runpod_graphql_url` pinned to `api.runpod.io`); `runpod_gpu_type_id`
      (select, default `NVIDIA RTX 6000 Ada Generation`; L40S and A100 80GB as fallbacks);
      `runpod_cloud_type` (`SECURE` default / `COMMUNITY`); `runpod_data_center_id`;
      `runpod_network_volume_id`; `runpod_image` (must carry a digest, `:latest` refused);
      `runpod_serverless_endpoint_id` (phase two, may be empty); `runpod_idle_stop_minutes`
      (1–120, default 15); `runpod_max_pod_hours` (1–24, default 4); `runpod_monthly_usd_cap`
      (0–2000, default 50); `runpod_default_canvas` (`736p_upscale` default / `1088p_native`);
      `runpod_default_profile` (`smooth` default / `hero` / `draft`); `gpu_route_default`
      (`auto` default / `colab` / `runpod`, read by the broker's route endpoint).
- [x] "Test connection" only reads: account balance, the volume exists in the chosen data centre,
      and whether the GPU type is available there and at what hourly price. Nothing is created.
- [x] Invalid values (off-host URL, `:latest` image, out-of-range numbers) are refused with 422.

## Steps

- [x] `config.py`: Settings fields, `OFFICIAL_PROVIDER_HOSTS`, base-URL/key pairing.
- [x] `admin/service.py`: `PROVIDER_DEFINITIONS["runpod"]`, `_configured`,
      `CONNECTION_TESTED_PROVIDERS`, `_test_provider`, `_validate_provider_values`.
- [x] `admin-settings-panel.tsx`: `providerCategoryOf.runpod = "video"`, `fieldMeta`.
- [x] Five locales: `providerFields` / `providerSecrets` labels and help.
- [x] Tests: readiness sets, validation, read-only test with a fake RunPod REST.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_admin_readiness.py tests/test_admin_runpod_settings.py
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

## Notes

- Owner steps on runpod.io that the admin cannot do: create the account, prepay (start with
  US$25, auto top-up off as the last cap), create a restricted read-write API key, create a
  ~100 GB network volume in a data centre that has RTX 6000 Ada stock.
- Prices read 2026-10-30 (runpod.io pricing page): RTX 6000 Ada Community US$0.79/h, Secure
  US$1.03/h; re-read before relying on them.
- The status panel (running pods, monthly spend, stop button) belongs to
  `2026-10-30-runpod-pod-broker`, which owns the sessions table it reads.

### 2026-10-30: card built (claude-opus-5-5-runpod)

- Two pinned URLs, not one: REST (`rest.runpod.io/v1`) answers `GET /networkvolumes/{id}` with
  `dataCenterId` and `size` (docs.runpod.io API reference, read 2026-10-30), but balance and GPU
  stock are only on GraphQL (`api.runpod.io/graphql`: `myself { clientBalance }`,
  `gpuTypes(input:{id}) { lowestPrice(input:{gpuCount, dataCenterId, secureCloud}) { stockStatus
  uninterruptablePrice } }`). The GraphQL field names come from the RunPod SDKs and are **not yet
  checked against a live account**; the first real "Test connection" proves them. Auth is a
  Bearer header on both, never the `?api_key=` query parameter the old SDK used.
- The probe lives in `apps/api/app/video_runpod/probe.py` so the broker ticket can reuse the
  client shape; the scope was widened to it and to `admin-settings-panel.test.tsx`.
- Claimed with `--force`: `apps/web/messages` is held by three older tasks
  (2026-10-12 studio link, 2026-10-19 five languages, 2026-10-29 daily brief). This change only
  inserts new `providerFields` / `providerSecrets` keys next to the Gemini narration limit and
  `pixabay_api_key`; nothing those tasks edit was touched.
- The locale files contain duplicate keys; rewriting them through `json.loads`/`json.dumps`
  silently drops the earlier copies. Insert text instead.
- Owner-side setup outside the site: RunPod's agent guide (https://agents.runpod.io/) installs
  the Claude Code plugin `runpod@runpod` (MCP `https://mcp.runpod.io/`, OAuth sign-in) so an
  agent can create the volume and check stock on the owner's account during the pilot. The
  session's permission classifier refused the plugin install ("code from external"); the owner
  runs it. It is independent of this card: the site still needs its own API key here.
- Verified: `pytest tests/test_admin_runpod_settings.py` (17), the admin/settings subset
  (1,360 passed), ruff, mypy; `lint:web`, `check:i18n`, `typecheck:web`,
  `admin-settings-panel.test.tsx` (60). Not done: the full `test:web`, and a real connection test
  (needs the owner's key).
