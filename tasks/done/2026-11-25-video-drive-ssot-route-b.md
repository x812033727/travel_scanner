---
id: 2026-11-25-video-drive-ssot-route-b
title: Switch video rules, lessons, and episode scripts to Google Drive SSOT (Route B) with vdrive CLI and anti-leak guard
status: done
priority: P1
area: tools
owner: antigravity
claimed_at: 2026-11-25T01:38:00Z
created_at: 2026-11-25T01:38:00Z
completed_at: 2026-11-25T01:49:00Z
branch: antigravity/video-drive-ssot-route-b
depends_on: []
scope:
  - AGENTS.md
  - CLAUDE.md
  - GEMINI.md
  - .gitignore
  - package.json
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - tools/video/vdrive.mjs
  - tools/video/vdrive.test.mjs
  - tools/video-drive-boundary.test.mjs
  - tasks/open/2026-11-25-slim-docs-videos-pools-and-plans.md
---

# Switch video rules, lessons, and episode scripts to Google Drive SSOT (Route B)

## Why

Owner decision on 2026-11-25 (Route B): move all video rules, lessons, canon character sheets,
lexicon, topic pools, and finalized episode scripts to Google Drive (`AI/備份/AI劇/_START-HERE.md`
and `AI/備份/AI劇/_規則/`) as the single authoritative source of truth (SSOT), minimizing GitHub
dependency and preventing business/content data from leaking into GitHub.

After PR #2223 merged, `AGENTS.md` and `.agents/skills/curio-episode/SKILL.md` still pointed agents
to GitHub `docs/videos/` as the primary rule source and carried conflicting pre-Flow (`generate_image`)
instructions. This task implements Stage 1 (Drive SSOT bootstrap + Route B entrypoints) and Stage 2
(cross-environment `npm run vdrive` tool + anti-leak CI guard).

## Definition of done

- [x] Bootstrapped Google Drive `AI/備份/AI劇/_START-HERE.md` (ID `1Ft5RT2RrJbGjcwqT1tqrz2qEJW_S6rNH`)
      and `AI/備份/AI劇/_規則/` (ID `1hIlOekB13nMZRiuRtMaBHSR4tYU7NuNT`, outside legacy `rules-sync`
      FILTERS so hourly host cron cannot overwrite it) with all 26 authoritative rule/lesson/lexicon/canon
      files, `CHANGELOG.md`, and `SHA256SUMS`, verified 27/27 OK (`0 differences`) via `sha256sum -c`.
- [x] Implemented `tools/video/vdrive.mjs` (`npm run vdrive`) supporting local Drive mount, `rclone`,
      and `gdrive` CLI plugin auto-detection, scoped `pull-rules`, optimistic-lock `push-rule`
      (SHA-256 check + `_history/` archive + `CHANGELOG.md` append), and secret-filtering
      `push-episode` with `SHA256SUMS`.
- [x] Added unit tests (`tools/video/vdrive.test.mjs`) and anti-leak repo boundary guard
      (`tools/video-drive-boundary.test.mjs`), plus `.gitignore` rules for `.cache/video-drive/` and
      `work/video-episodes/`.
- [x] Updated `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` (byte-identical) and
      `.agents/skills/curio-episode/SKILL.md` / `.claude/skills/curio-episode/SKILL.md` (byte-identical)
      to Route B thin pointers (`npm run vdrive -- pull-rules` → Drive `_START-HERE.md` & `_規則/`).
- [x] Updated `tasks/open/2026-11-25-slim-docs-videos-pools-and-plans.md` with owner's Route B Phase B
      decision and Stage 3 runtime/test decoupling checklist.

## How to verify

- `node --test tools/video/vdrive.test.mjs tools/video-drive-boundary.test.mjs tools/repo-hygiene.test.mjs`
- `node --test docs/videos/rules-sync/sync.test.mjs`
- `npm run check:tasks`
- Live Drive verification: `npm run vdrive -- pull-rules all` + `sha256sum -c .cache/video-drive/rules/_規則/SHA256SUMS`

## Notes

- Stale claims from October 2026 (`2026-10-14-curio-episodes-keep-the-series-look` etc.) were untouched
  per `task-board` rules; no open PR touched `AGENTS.md`, `tools/video/vdrive.mjs`, or `curio-episode`.
- Production host follow-up for owner/ops: disable the legacy root cron running
  `docs/videos/rules-sync/sync.mjs` when ready (`AI/備份/AI劇/_規則/` is already outside its FILTERS).
