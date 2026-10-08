---
id: 2026-10-08-video-branding-true-peak
title: Limit true peaks after video branding audio join
status: in-progress
priority: P1
area: tools
owner: codex-video-peak-fix
claimed_at: 2026-10-08T06:08:54Z
created_at: 2026-10-08T06:08:53Z
completed_at:
branch: codex/stalled-videos-completion-20261008
depends_on: []
scope:
  - tools/video/assemble/branding.mjs
  - tools/video/assemble/branding.test.mjs
  - tools/video/assemble/branding-smoke.mjs
---

# Limit true peaks after video branding audio join

## Why

The stalled Cloudflare Workers video has a valid body mix (-14 LUFS, -0.9 dBTP),
but its branded final reaches 0 dBTP and fails assembly. The branding wrapper
concatenates the selected bookend audio with the body and encodes AAC once more,
without controlling peaks after the join. Re-normalizing the body cannot fix a
peak introduced by the bookends or this last encode.

## Definition of done

- [x] Final joined audio has a unity-gain, latency-compensated, oversampled peak
      limiter with AAC headroom; video, selected source bytes, and body offsets stay intact.
- [x] A real AAC regression reproduces the original failed peak and passes after
      the fix; decoded PCM keeps its exact sample count and body/outro tone phases.
- [x] The built-in branding smoke measures decoded AAC peaks, exact video frames,
      unchanged retained body bytes, sample count, and CC/chapter offsets.
- [ ] The production Cloudflare Workers candidate passes normal assembly and QA
      with the corrected wrapper and reaches its ordinary review/package gates.

## Steps

- [x] Confirm the body passes and the branding join creates the failed peak.
- [x] Add a 4x oversampled -2 dBFS limiter after concatenation, without makeup gain
      or uncompensated lookahead delay; retain normal assembly checks.
- [x] Run focused branding, assembly, drama and compilation tests and the real
      offline MP4/WAV smoke with synthetic bookends.
- [ ] Independently review the source and execute the normal production pipeline
      using a private copy, without deploying or changing shared production code.

## How to verify

Use the compatible bundled Node executable on Windows:

```bash
node --test tools/video/assemble/branding.test.mjs tools/video/assemble/assemble.test.mjs tools/video/assemble/drama.test.mjs tools/video/compile/compile.test.mjs
node tools/video/assemble/branding-smoke.mjs --assets <outside-repo-package> --workdir <outside-repo-evidence>
node tools/tasks.mjs check
```

Then run ordinary assembly, captions, final review, package and publish review
for the source-bound production project; read actual checks and review decisions.

## Notes

- 2026-10-08 codex-video-peak-fix: 63 focused tests passed, zero skipped, using real
  local FFmpeg for the AAC regression. Unprotected decoded peak was 0 dBTP;
  corrected decoded peak was -1.9 dBTP. The WAV had exactly 576000 samples per
  channel, with body/outro phase tests at their original absolute offsets.
- Offline smoke evidence is outside git at
  `C:/Users/x8120/mokaair-work/handoff/branding-peak-20261008/smoke/evidence.json`:
  540 frames / 18 seconds, 864000 WAV samples per channel, decoded peak -2 dBTP,
  retained body SHA unchanged, quiet body PCM difference at most one unit away
  from seams, CC 5000-15000 ms and unchanged chapter/frame offsets. This synthetic
  package checks peaks and timing; its overall -15.1 LUFS is not a production
  loudness acceptance claim. Normal assembly still checks actual programme loudness.
- Frozen implementation `tools/video/assemble/branding.mjs` SHA-256:
  `1d5c89b5e54ebfee67fae5fececa7b4e8d5e1dba7dd145dca6e459bfe5d4658c`.
- No paid/provider calls, production mutations, commits, deploys or worker
  restarts were performed by the implementation agent.
