---
id: 2026-11-25-add-local-google-flow-mcp-server
title: Add local Google Flow MCP server and CLI with Mokaair production guards
status: done
priority: P2
area: tools
owner: antigravity-gemini
claimed_at: 2026-11-25T17:02:01Z
created_at: 2026-11-25T17:01:53Z
completed_at: 2026-11-25T17:15:11Z
branch: antigravity/google-flow-mcp
depends_on: []
scope:
  - tools/video/flow-mcp
  - package.json
---

# Add local Google Flow MCP server and CLI with Mokaair production guards

## Why

Mokaair's long-form explainer series (`sothatswhy` and `curio`) produce 35–48 animated clips plus 35–85 stills per episode on Google Flow (`flow.google.com`) using a Google AI subscription account's monthly credits rather than a pay-per-use video API. Driving Flow manually is slow and error-prone (Flow silently resets `16:9` to `1:1` after switching modes, character refs can leak into scenery shots, safety-filter words waste retries, and overspending credits or downloading paid 1080p breaks per-episode budgets). Wrapping `gflow-cli` behind a project-specific local Node.js MCP server (`tools/video/flow-mcp/`) lets Claude Code, Codex, and Antigravity on Windows/macOS run Flow end-to-end while enforcing every guard in `FLOW-PRODUCTION-RULES.md` and `CURIO-FLOW-CHECKLIST.md` with zero GitHub episode commits (Route B).

## Definition of done

- [x] Pure Node.js 22 ESM MCP stdio server (`tools/video/flow-mcp/server.mjs`) exposing 10 high-cohesion tools with async `job_id` + `flow_wait` support and `runtime.lock` cross-client locking.
- [x] All 6 Mokaair production guards implemented and enforced before spending credits: dual-project isolation, full-axis safety prompt scanner, 16:9 (`1376×768`) binary dimension check, 0-credit stills-first QA gate, per-episode credit cap with single-use `confirm_token`, and Route B `work/video-episodes/<slug>/` path boundary.
- [x] Swappable `FlowDriver` interface with verified `GflowCliDriver` (`nano2.1` stills, `omni-1.2-flash` 4s `720p` clips, RFC 9457 fail-fast error handling).
- [x] Local `ffmpeg` post-processing pipeline (`1080p30`, Lanczos, `bt709`, `video_full_range_flag=0`, `-an`), 4-frame QA contact sheets, HTML QA gallery, and SHA-256 `manifest.json`.
- [x] Companion CLI (`npm run flow -- doctor|login|status|setup|preflight|ledger|mcp`) with Windows-first multi-client config generator (`Claude Code`, `Claude Desktop`, `Codex`, `Antigravity`), `install-windows.ps1`, and complete Traditional Chinese README.
- [x] Unit and stdio MCP integration tests pass under `npm run test:tools` and `npm run check:tasks`.

## Steps

- [x] Build `config.mjs` and the 4 guard modules under `tools/video/flow-mcp/guards/`.
- [x] Build `FlowDriver` interface and `GflowCliDriver` under `tools/video/flow-mcp/drivers/`.
- [x] Build `ffmpeg` 1080p30 upscaler, 4-frame QA sheet, and HTML gallery under `tools/video/flow-mcp/postprocess/`.
- [x] Build single-worker `JobQueue` with cross-client file lock and async wait/cancel under `tools/video/flow-mcp/jobs/`.
- [x] Build `orchestrator.mjs`, JSON-RPC 2.0 stdio `server.mjs`, companion `cli.mjs` (including Windows client setup), `install-windows.ps1`, and `README.md`.
- [x] Wire `flow` / `flow:mcp` scripts into `package.json`.
- [x] Write comprehensive tests covering guards, driver, post-processing, job queue, orchestrator, CLI setup, and live stdio MCP framing; verify `npm run test:tools` and `npm run check:tasks`.

## How to verify

```bash
node --test "tools/video/flow-mcp/*.test.mjs"
npm run test:tools
npm run check:tasks
npm run flow -- doctor
npm run flow -- setup --platform win32 --repo-root "C:\dev\travel_scanner"
```

## Notes

- Owner approved Route A (project-guard MCP wrapping `gflow-cli` behind a swappable `FlowDriver` interface) with Windows as primary local host.
- Pure Node.js 22 ESM with zero added npm dependencies to keep supply-chain and lockfile footprint untouched.
- Confirmed `flowGenerateClips` validates all start/end stills and safety prompts before consuming single-use `confirm_token`.
