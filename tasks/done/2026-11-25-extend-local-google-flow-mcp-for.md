---
id: 2026-11-25-extend-local-google-flow-mcp-for
title: Extend local Google Flow MCP for full AI drama production, takes, continuity, and multi-profile support
status: done
priority: P2
area: tools
owner: antigravity-gemini
claimed_at: 2026-11-25T23:12:49Z
created_at: 2026-11-25T23:12:15Z
completed_at: 2026-11-25T23:22:05Z
branch: antigravity/google-flow-mcp-ai-drama
depends_on: []
scope:
  - tools/video/flow-mcp
  - .agents/skills/google-flow-mcp
  - .claude/skills/google-flow-mcp
---

# Extend local Google Flow MCP for full AI drama production, takes, continuity, and multi-profile support

## Why

Phase 1 (`#2225`) built Mokaair's local subscription-backed Google Flow MCP around explainer series (`sothatswhy`, `curio`). Producing full AI dramas (`種田娶妻打天下`, `恁祖媽今年18`, horizontal/vertical anime dramas, and silent vertical Shorts) requires multi-character Cast & Flow `@Name` registration, same-camera `edit_from` image-to-image chaining, Exact-Join `continue_from` last-frame extraction, flexible 3–15s / Veo 3.1 credit estimation, multi-take archival (`takes/`) with `MAX_CLIP_TAKES=2` hard stop, `video.json` <-> `clips import` bridging, FFmpeg PSNR / mid-clip hard-cut QC, orphaned `maybe` credit reconciliation, multi-account profile overview, interactive QA gallery JSON copy + 9:16 safe-zone guides, and a shared `google-flow-mcp` skill.

## Definition of done

- [x] `drama-16x9` and `drama-9x16` presets with per-model/duration credit estimation, `audioPolicy` (`extract_sidecar` / `silent_with_guard`), drama safety nuance, and 9:16 safe-zone flags.
- [x] `bridges/video-json-adapter.mjs` converting Mokaair `video.json` into `flow-shot-list.json` + `cast.json` (H3 tag cleanup, 0-credit `data.source` cuts, silent audio guard) and writing `import-bridge.json` + series-aware `vdrive` commands.
- [x] Driver & Queue extended with `listProfiles`, `createCharacter`, `listCharacters`, `extendVideo`, `listRemoteVideos`, `downloadMedia`, `getVersion`, and per-profile `RuntimeLock`.
- [x] Orchestrator & MCP server expanded to 16 tools including `flow_profiles`, `flow_register_character`, `flow_import_video_json`, `flow_select_take`, `flow_extend_clip`, and `flow_reconcile`, plus `edit_from`, `continue_from`, 3-shot `pilot`, `resumeMissingOnly`, multi-take archival (`takes/`), and `MAX_CLIP_TAKES=2`.
- [x] FFmpeg post-processing extended with `extractLastFrame`, raw-audio WAV sidecar, frame-0 PSNR >= 22 QC, and mid-clip hard-cut detection (`scene > 0.4`), plus interactive `qa-gallery.html` copy button & 9:16 safe-zone overlay.
- [x] Shared skill added identically under `.agents/skills/google-flow-mcp/SKILL.md` and `.claude/skills/google-flow-mcp/SKILL.md`.
- [x] Comprehensive unit & end-to-end tests pass (`tools/video/flow-mcp/*.test.mjs`, hygiene, boundary, tasks, skills).

## Steps

- [x] Upgrade `config.mjs`, `guards/path-boundary.mjs`, `guards/prompt-safety.mjs`, and `guards/budget-guard.mjs`.
- [x] Add `bridges/video-json-adapter.mjs`.
- [x] Upgrade `drivers/` and `jobs/job-queue.mjs` for Phase 2 gflow commands and per-profile locks.
- [x] Upgrade `postprocess/` with QC, last-frame extraction, raw audio sidecar, and interactive QA galleries.
- [x] Expand `orchestrator.mjs`, `server.mjs`, `cli.mjs`, and `README.md` to 16 tools.
- [x] Add shared skill `.agents/skills/google-flow-mcp/SKILL.md` and `.claude/skills/google-flow-mcp/SKILL.md`.
- [x] Add `ai-drama.test.mjs` and verify all tests + CI green.

## How to verify

```bash
node --test --test-reporter=spec "tools/video/flow-mcp/*.test.mjs"
npm run check:tasks
npm run test:tools
```

## Notes

- Merged Phase 1 PR #2225 (`c3dbea64`) first so Phase 2 sits cleanly on `origin/main`.
- Skill strictly follows `tools/skills.test.mjs` contract (byte-identical Claude mirror, description <= 1024 chars without angle brackets, no machine paths, repo-root paths verified).
