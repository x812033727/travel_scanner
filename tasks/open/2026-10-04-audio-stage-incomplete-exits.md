---
id: 2026-10-04-audio-stage-incomplete-exits
title: Audio stages distinguish incomplete runs and chapter failures from success
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-04T18:01:08Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/cli.mjs
  - tools/video/tts/tts.test.mjs
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
---

# Audio stages distinguish incomplete runs and chapter failures from success

## Why

The normal TTS command returns exit 0 when a STOP file interrupts its pending synthesis loop before the current timeline and narration are assembled. It also only prints chapter timing problems before returning 0. The audio-check command similarly returns 0 on STOP before producing a complete check summary. An orchestrator that treats exit 0 as completion can advance an interrupted or invalid audio stage. Existing clips and partial transcripts should remain reusable, but success must distinguish them from complete, valid current audio.

## Definition of done

- [ ] Interrupted TTS and audio-check runs have an explicit incomplete outcome and cannot be reported as completed current audio.
- [ ] Chapter timing failures prevent terminal TTS success; complete valid audio retains the normal successful outcome.
- [ ] Existing caches, partial transcripts, source hashes and paid-request uncertainty evidence remain intact; the change does not widen re-recording or retry paid requests.

## Steps

- [ ] Coordinate with the existing active narration-cache ticket before claiming overlapping CLI/test paths.
- [ ] Add focused offline fixtures for STOP before assembly, chapter timing failure, STOP before full audio-check summary and complete successful runs.
- [ ] Correct the outcome contract and update only consumers necessary to preserve safe resumability.

## How to verify

Run the focused tests for tools/video/tts/tts.test.mjs and tools/video/tts/check.test.mjs. Mock providers so the fixtures incur no paid calls. Verify that retained partial caches can resume safely, chapter errors are distinguishable from success, and complete valid runs still return 0. Do not change provider models, budgets or authorization gates.

## Notes

- Read-only observation at prepared Embedding HEAD 00332287b23e353e4f4ad262fdeaa256b1f5518b: cli.mjs:335-337 returns EXIT.ok on STOP before its narration/timeline assembly at 374-380; line383 merely prints checkChapters problems before the unconditional success at386. check.mjs:262-264 returns EXIT.ok on STOP before the summary/flags/recordStage block at379-396. This is a code-contract finding; no interrupted paid run was manufactured to reproduce it.
- Existing task 2026-10-03-video-worker-narration-takes-made-stale is in-progress under claude-opus-5-5 and scopes cli.mjs and tts.test.mjs. This follow-up is deliberately unclaimed; preserve that ownership and coordinate before implementation.
- The active Embedding producer separately verifies actual current narration/timeline, all156 clips and audio-check coverage instead of treating exit0 as sufficient. No shared audio implementation was changed by filing this task.
