---
id: 2026-10-23-c-series-video-safety-guards
title: Port C-series video safety guards to main
status: review
priority: P1
area: tools
owner: codex-c-series-video-safety-port
claimed_at: 2026-10-23T12:02:10Z
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
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
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

- [x] C-series subtitles round-trip across a fractional-frame intro.
- [x] Everyday stories keep the approved cute-mystery look, at least 70% illustrated body scenes, and at most three consecutive cards in both local lint and host relint.
- [x] Generated music records fully decoded duration and holds short or stale paid tracks before assembly encoding or dub mixing; no automatic replacement music purchase occurs.
- [ ] Existing long-form duration guards remain independently reviewed and SHA-bound after final code edits; required CI checks pass.

## Steps

- [x] Claim the 14 free code, test and skill paths in this ticket; use the same existing checkout.
- [x] Port #1610 branding fix, #1667 story and host guard, and #1669 music guard without overwriting newer main changes.
- [x] Make audio tests skip only when FFmpeg is absent; CI video-tests must run them with FFmpeg.
- [x] Coordinate narrow ownership release for `tools/video/core/lint.mjs`, `lint.test.mjs`, `state.mjs`, `state.test.mjs` before editing them, then add them to scope and finish the local lint/status guards.
- [ ] Have an independent reviewer inspect final duration-bound file bytes and renew `docs/videos/long-form/review.md/json` under a separate claim.

## How to verify

Run focused Node tests for branding, story, lint, host story, music, clips, state and long-form review; `npm run check:tasks`; `node tools/video/long-form/cli.mjs check`; then confirm hosted `web-checks`, `video-tests` and `smoke` pass on the resulting PR. No paid provider calls are part of this verification.

## Notes

The first claim excluded files held by unrelated active tasks: tutorial-flow held `core/lint*`; A01 lexicon held `core/state*`; multiple older tasks held long-form `review.md/json`. On 2026-10-23 the owner directed the board steward to release only these six clean paths for the C-series safety port and independent final duration review. The four code/test paths above were added to this claim after the narrow release; the canonical review paths belong to the independent reviewer. The #1669 `state.mjs` bug is `pipelineStatus` treating a legacy request-only generated manifest with matching `mix_hash` as "music generated" done. The final generated status must require a current cut, measured sufficient duration, retained file and matching SHA, while owner-supplied tracks keep their current semantics. PR #1669 CI also has five FFmpeg-dependent tests failing in web-checks, where FFmpeg is intentionally absent.

The first port of the 14 free paths passed 94 focused Node tests with FFmpeg present, with zero skips. On this Windows host Node 24 crashes in `fs.cpSync` when fixture sources are reached through the checkout's non-ASCII path. Tests ran through a temporary `subst` drive pointing at the *same* checkout; the drive was removed afterward. `git diff --check` and `npm run check:tasks` passed for that first port.
With FFmpeg hidden, seven relevant music tests produced three passes, four explicit FFmpeg skips and zero failures. With FFmpeg present, none of these tests skipped. The canonical duration review is separately ticketed.
After the lint/state port, their complete focused test files passed 70/70 with zero skips. The state test then gained two more assertions for missing paid bytes and a stale script timeline; that named case passed again. The canonical duration review and hosted CI remain pending.

The unmerged #1669 task `2026-10-22-reconcile-legacy-generated-music-manifests-in` is absorbed by the `state.mjs` change and its focused test: legacy request-only, short, sufficient, changed-cut, missing-file, changed-byte and owner-track cases are covered. Read-only C03 verification found the retained 4,182,166-byte MP3 still matches its manifest SHA, while the old manifest has only requested `seconds: 600` and no decoded duration; the new `pipelineStatus` correctly says `music generated = false` and points to `music --slug story-everyday-moleskine-c03` for cached measurement. No C03 file, ledger or provider job was changed. The unmerged #1669 independent-review task is preserved in `2026-10-23-renew-c-series-canonical-duration-review`.

The shared music guard reaches `dubSound()` only after `dubLocale()` has synthesized pending translation lines. It stops before dub mixing, but does not prevent speech spend first. Follow-up `2026-10-23-preflight-music-before-paid-dub-synthesis` records the separate pre-spend work; no dubs code or paid speech work is part of this port.

2026-10-23 review handoff: draft PR #1784 is open at head
`e4f0390a6` on merged-main budget base `efbb3012f`. The independent reviewer
rebound the eight changed canonical duration files while preserving the other
100 hashes; 52/52 affected tests, 2/2 receipt tests and 473-plan CLI passed.
The owner removed two exact task-board open duplicates after automatic approval
review blocked deletion; `npm run check:tasks` then passed 2117 files. Hosted PR
checks and final merge remain the gate for this task.
