---
id: 2026-11-27-add-remote-episode-file-transfer-and
title: Add remote episode file transfer and Drive sync bridge to mokaair-flow MCP gateway
status: done
priority: P1
area: tools
owner: antigravity
claimed_at: 2026-11-27T03:20:44Z
created_at: 2026-11-27T03:20:36Z
completed_at: 2026-11-27T03:31:28Z
branch: antigravity/flow-mcp-remote-file-bridge
depends_on: []
scope:
  - tools/video/flow-mcp
  - ops/flow-gateway
  - apps/api/app/video_flow_mcp
  - apps/api/tests/test_video_flow_mcp.py
  - .agents/skills/google-flow-mcp
  - .claude/skills/google-flow-mcp
---

# Add remote episode file transfer and Drive sync bridge to mokaair-flow MCP gateway

## Why

Paired cloud environments (Antigravity, Claude Cloud, Codex Cloud) can call `mokaair-flow` over HTTPS via `POST /api/video/mcp/flow`, but the host gateway (`flowbot`) stores episodes under `/opt/mokaair-flow-gateway/travel_scanner/work/video-episodes/<slug>/`. Previously, `mokaair-flow` had no MCP tools to upload shot lists / pre-QA'd firstframes into the host gateway or pull generated stills and 1080p clips back out (and `ops/flow-gateway/install.sh` left `/opt/mokaair-flow-gateway` owned by `root:root`, blocking `flowbot` writes). This prevented cloud agents from running Flow episodes end-to-end without local Chrome or SSH.

## Definition of done

- [x] `mokaair-flow` exposes jailed, SHA-256 verified remote file sync tools (`flow_list_files`, `flow_write_file`, `flow_read_file`) and host-side Drive push (`flow_push_drive`), bringing total tools to 22.
- [x] `flow_approve_stills` auto-discovers and dimension-verifies uploaded stills (`stills/` or `flow-clips/firstframes/`, or explicit `relPath`) so cross-machine firstframes unlock clip generation without OS path conflicts.
- [x] `npm run flow -- remote-push` and `npm run flow -- remote-pull` perform chunked (`<= 512 KiB`) 0-diff incremental directory sync over the paired HTTPS MCP bridge.
- [x] `ops/flow-gateway/install.sh` creates `flowbot`-owned `work/video-episodes`, `work/music-library`, and `.cache/video-drive` directories across upgrades.
- [x] `apps/api/app/video_flow_mcp/router.py` raises `MCP_CALLS_PER_HOUR` to `1200` to accommodate chunked episode transfers + clip polling without leaking payloads to audit logs.

## Steps

- [x] Add symlink-safe relative path jail and extension allowlist in `tools/video/flow-mcp/guards/path-boundary.mjs`.
- [x] Implement `flowListFiles`, `flowWriteFile`, `flowReadFile`, `flowPushDrive`, and uploaded-still auto-discovery in `tools/video/flow-mcp/orchestrator.mjs` and register them in `tools/video/flow-mcp/server.mjs`.
- [x] Add chunked SHA-256 sync helpers in `tools/video/flow-mcp/remote-bridge.mjs` and expose `remote-push` / `remote-pull` in `tools/video/flow-mcp/cli.mjs`.
- [x] Fix writable `flowbot` directories in `ops/flow-gateway/install.sh` and raise hourly MCP rate limit in `apps/api/app/video_flow_mcp/router.py`.
- [x] Add end-to-end gateway transfer + security tests and sync README + `.agents`/`.claude` skill mirrors.

## How to verify

```bash
node --test tools/video/flow-mcp/*.test.mjs
npm run test:tools && npm run check:tasks
cd apps/api && uv run ruff check app/video_flow_mcp tests/test_video_flow_mcp.py && uv run mypy app/video_flow_mcp tests/test_video_flow_mcp.py && uv run pytest tests/test_video_flow_mcp.py
```

## Notes

- Chunk cap is fixed at 512 KiB raw (~683 KiB base64) so every JSON-RPC request stays comfortably below the 1 MiB `MAX_RPC_BODY_BYTES` limit across nginx, Next.js BFF, FastAPI, and `gateway.mjs`.
- After merge, re-run `bash ops/flow-gateway/install.sh --runtime-env /root/travel_scanner/.env` on the production host (alongside API deploy) so `flowbot` gets the new 22-tool gateway and writable `work/` directories.
