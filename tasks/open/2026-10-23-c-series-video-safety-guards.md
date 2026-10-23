---
id: 2026-10-23-c-series-video-safety-guards
title: Port C-series video safety guards to main
status: in-progress
priority: P1
area: tools
owner: codex-c-series-video-safety-port
claimed_at: 2026-10-23T11:51:35Z
created_at: 2026-10-23T11:51:28Z
completed_at:
branch: codex/c-series-video-safety-port-20261023
depends_on: []
scope:
  - tools/video/core/branding.mjs
  - tools/video/core/branding.test.mjs
  - .agents/skills/brand-story/SKILL.md
  - .claude/skills/brand-story/SKILL.md
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - tools/video/core/story.mjs
  - tools/video/core/story.test.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/assemble/sound.mjs
  - tools/video/assemble/music-loop.test.mjs
  - tools/video/media/music.mjs
  - tools/video/media/clips.test.mjs
  - tools/video/media/music-duration.test.mjs
---

# Port C-series video safety guards to main

## Why

The C01–C20 series needs three retained safety fixes from older draft PRs: subtitle timing at a fractional intro frame (#1610), the Curio illustration mix for everyday stories (#1667), and measured generated music that cannot silently pass or be purchased again (#1669). Their old bases are closed or stale. Port only their unique code onto current main; keep other main changes and paid media intact.

## Definition of done

- [ ] C-series subtitles round-trip across a fractional-frame intro.
- [ ] Everyday stories keep the approved cute-mystery look, at least 70% illustrated body scenes, and at most three consecutive cards in both local lint and host relint.
- [ ] Generated music records fully decoded duration and holds short or stale paid tracks before assembly or dub; no automatic replacement purchase occurs.
- [ ] Existing long-form duration guards remain independently reviewed and SHA-bound after final code edits; required CI checks pass.

## Steps

- [x] Claim the 14 free code, test and skill paths in this ticket; use the same existing checkout.
- [ ] Port #1610 branding fix, #1667 story and host guard, and #1669 music guard without overwriting newer main changes.
- [x] Make audio tests skip only when FFmpeg is absent; CI video-tests must run them with FFmpeg.
- [ ] Coordinate narrow ownership release for `tools/video/core/lint.mjs`, `lint.test.mjs`, `state.mjs`, `state.test.mjs` before editing them, then add them to scope and finish the local lint/status guards.
- [ ] Have an independent reviewer inspect final duration-bound file bytes and renew `docs/videos/long-form/review.md/json` under a separate claim.

## How to verify

Run focused Node tests for branding, story, lint, host story, music, clips, state and long-form review; `npm run check:tasks`; `node tools/video/long-form/cli.mjs check`; then confirm hosted `web-checks`, `video-tests` and `smoke` pass on the resulting PR. No paid provider calls are part of this verification.

## Notes

The first claim excludes files held by unrelated active tasks: tutorial-flow owns `core/lint*`; A01 lexicon owns `core/state*`; multiple older tasks own long-form `review.md/json`. Do not force claim or edit them. The #1669 `state.mjs` bug is `pipelineStatus` treating a legacy request-only generated manifest with matching `mix_hash` as "music generated" done. The final generated status must require a current cut, measured sufficient duration, retained file and matching SHA, while owner-supplied tracks keep their current semantics. PR #1669 CI also has five FFmpeg-dependent tests failing in web-checks, where FFmpeg is intentionally absent.

The first port of the 14 free paths passed 94 focused Node tests with FFmpeg present, with zero skips. On this Windows host Node 24 crashes in `fs.cpSync` when fixture sources are reached through the checkout's non-ASCII path. Tests ran through a temporary `subst` drive pointing at the *same* checkout; the drive was removed afterward. `git diff --check` and `npm run check:tasks` passed. The lint, state and canonical duration review gates remain pending their separate task owners' release.
