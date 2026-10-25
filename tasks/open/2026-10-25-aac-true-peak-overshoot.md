---
id: 2026-10-25-aac-true-peak-overshoot
title: Keep normalized AAC true peaks below the assembly ceiling
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-25T10:47:08Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/assemble/plan.mjs
  - tools/video/assemble/plan.test.mjs
---

# Keep normalized AAC true peaks below the assembly ceiling

## Why

The first native assembly of openai-dns-containment measured -14.0 LUFS but
+1.0 dBTP after AAC encoding, failing the existing -1 dBTP ceiling. The current
two-pass linear loudnorm request did not give this source enough encoded-peak
headroom. A local episode adapter passed native final checks at -14 LUFS and
-2.8 dBFS decoded true peak; the shared assembler has not been changed.

## Definition of done

- [ ] Native assembly meets integrated loudness and decoded true-peak limits for peaky TTS sources after AAC encoding.
- [ ] A meaningful regression covers post-encode overshoot without weakening the existing measurement or thresholds.

## Steps

- [ ] Reproduce the encoded peak result with a retained or representative transient-rich source.
- [ ] Evaluate output headroom, dynamic normalization and a latency-compensated limiter; keep narration timing stable.
- [ ] Run native probe, loudness and audio/video synchronization checks on the final encoded file.

## How to verify

Run affected assemble plan tests and an actual encode. Measure the decoded output
with `ebur128=peak=true`; source-WAV or loudnorm first-pass values alone are not
the final result.

## Notes

- Observed with ffmpeg 7.1.5 on 2026-10-25. Native checks correctly rejected the first cut; no thresholds were changed.
- Episode-specific reproducible adapter: `docs/videos/openai-dns-containment/assemble-with-peak-guard.mjs`. It retains native assembly/checks, requests -3 dBTP normalization headroom, disables linear normalization and adds a latency-compensated limiter before AAC output.
- This is a shared-tool follow-up. The video task owns only the adapter and its measured delivery, documented in `docs/videos/openai-dns-containment/production-result.md`; the shared normalizer still needs a general fix and regression coverage.
