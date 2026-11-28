---
id: 2026-11-25-polish-google-flow-mcp-with-series
title: Polish Google Flow MCP with series cast inheritance, extend planner, 2K/4K still upscale, and batch import/push CLI
status: done
priority: P2
area: tools
owner: antigravity-gemini
claimed_at: 2026-11-25T23:39:33Z
created_at: 2026-11-25T23:39:23Z
completed_at: 2026-11-25T23:43:31Z
branch: antigravity/google-flow-mcp-polish
depends_on: []
scope:
  - tools/video/flow-mcp
  - .agents/skills/google-flow-mcp
  - .claude/skills/google-flow-mcp
---

# Polish Google Flow MCP with series cast inheritance, extend planner, 2K/4K still upscale, and batch import/push CLI

## Why

After merging Phase 1 (`#2225`) and Phase 2 (`#2226`), four practical friction points remained for multi-episode AI drama production: (1) `flow_extend_clip` lacked a dedicated zero-credit `flow_plan_extend` tool to mint its `confirm_token`, (2) multi-episode AI dramas had to re-register fixed characters per episode instead of inheriting a shared series Cast, (3) `import-bridge.json` and Drive backup required manually pasting per-clip/push commands instead of `import-all` / `push`, and (4) Ultra 2K/4K still upscaling and multi-account credit spillover hints were not wired.

## Definition of done

- [x] Shared gitignored series Cast at `work/video-episodes/_series/<dramaName>/cast.json` with `saveToSeries` and auto-inheritance in `flow_init_episode`.
- [x] `flow_plan_extend` (Tool #17) and `flow_upscale_still` (Tool #18) added to `FlowOrchestrator`, `GflowCliDriver`, and `server.mjs` (18 tools total).
- [x] Multi-account spillover profile suggestions attached to `flow_plan_clips` and `flow_plan_extend` when `insufficient_account_credits` triggers.
- [x] `npm run flow -- import-all` and `npm run flow -- push` (pre-push ledger gate + `vdrive.mjs push-episode`) implemented and tested.
- [x] `README.md` and byte-identical `google-flow-mcp` skill updated; all unit tests and `check:tasks` green.

## Steps

- [x] Add `resolveSeriesCastPath`, `upscaleImage`, series Cast inheritance, `flow_plan_extend`, `flow_upscale_still`, and spillover suggestions.
- [x] Add `runImportBridgeBatch` (`import-all`) and `runValidatedDrivePush` (`push`) to `cli.mjs`.
- [x] Update `README.md` and both copies of `google-flow-mcp/SKILL.md`.
- [x] Add Phase 3 unit tests and verify all tests + CI green.

## How to verify

```bash
node --test --test-reporter=spec "tools/video/flow-mcp/*.test.mjs"
npm run check:tasks
```

## Notes

- Shared series Cast lives inside `work/video-episodes/_series/<dramaName>/cast.json`, already gitignored by `work/video-episodes/` in `.gitignore`.
