---
id: 2026-10-20-prepare-x11-fedex-brand-story
title: Prepare X11 FedEx brand story
status: in-progress
priority: P2
area: docs
owner: codex-x11-author
claimed_at: 2026-10-20T19:02:58Z
created_at: 2026-10-20T18:54:30Z
completed_at:
branch: codex/brand-story-fedex-x11
depends_on: []
scope:
  - docs/videos/story-everyday-fedex-x11
---

# Prepare X11 FedEx brand story

## Why

The owner wants more recognizable brand stories beyond the existing X01–X10 work, with original sources and the 奇聞檔案局 production rules. The earlier FedEx candidate asked about the first overnight hub, but accessible recent SEC filings cannot establish those early details. A source-bounded modern reversal is available: Express and Ground operated independently under the same brand, then began a legal and physical integration on different schedules.

## Definition of done

- [ ] A source-checked six-chapter script, two standalone Shorts and shot package pass the brand-story lint and two independent narrative blind reviews.
- [ ] Paid media, audio, and local preview pass the per-video US$25 ledger, human visual/audio QA, and the series bookend/caption/link rules; create an honest draft PR handoff.

## Steps

- [x] Check source feasibility from FedEx FY2022–FY2026 original SEC 10-K filings and record the event chronology and caveats.
- [x] Obtain root's independent anchor check of the source-feasibility memo, then write a six-chapter Treatment and full narration.
- [ ] Validate the manuscript and Shorts against exact source claims and story gates before paid generation.
- [ ] Produce the bounded pilot, inspect it, and continue only if visual/audio quality passes.

## How to verify

Inspect `docs/videos/story-everyday-fedex-x11/source-feasibility.md` and the author source matrix against the linked SEC filings. Rebuild `compose-video.mjs` and `compose-shorts.mjs`; run `node tools/video/cli.mjs lint --slug story-everyday-fedex-x11`, `npm run check:tasks` and `npm run test:docs-videos` before a later PR. The exact video/Shorts SHA-256 must be retained through independent source and blind-reader review; any script change invalidates those receipts. Future paid-media checks belong to the production steps.

## Notes

The feasibility memo links five primary filings, records their download hashes and date-qualified excerpts, supplies a nonduplicate six-chapter event flow and two Short hooks, and keeps the 2026 Freight spin-off distinct from parcel Ground. SEC access was tested on 2026-10-20. Moleskine/D’Ieteren official domains for the C03 priority item were blocked by this cloud environment, so X11 is a supplemental episode and does not reorder C01–C20. No paid generation. A second source reviewer must not treat this memo as its own PASS receipt.

Root independently verified the initial SEC memo. v3 source audit passed but [blind A](../../docs/videos/story-everyday-fedex-x11/reviews/blind-a-v3-independent.md) and [blind B](../../docs/videos/story-everyday-fedex-x11/reviews/blind-b-v3-independent.md) both failed narrative gates: unanswered station/segment questions, repeated 290/risk wording, and a seven-line Freight detour. The author revised v4 to follow a single concept parcel through actual network operations, moved Freight to the source-backed description, changed chapter handoffs and visual cue `x11-b02-s15`, and added primary FY2025/FY2026 network anchors. The [v4 author delta](../../docs/videos/story-everyday-fedex-x11/revision-v4.md) is not a review receipt.

The [v4 source delta](../../docs/videos/story-everyday-fedex-x11/reviews/source-audit-v4-independent.md) passed, but [blind A](../../docs/videos/story-everyday-fedex-x11/reviews/blind-a-v4-independent.md) and [blind B](../../docs/videos/story-everyday-fedex-x11/reviews/blind-b-v4-independent.md) both failed 8/12 required narrative checks. Their common findings were a delayed chapter payoff, repeated driver arrangements and a late equipment inventory; reader B also flagged the unanswerable historical “why 2024” question and missing Network 2.0 name in Short 1. The [v5 author delta](../../docs/videos/story-everyday-fedex-x11/revision-v5.md) records the repairs and three new SEC anchors, but is not an independent PASS.

Frozen v5 review input was `video.json` SHA-256 `3d2a7d1d422105802fd1d755fa8f90f1ca5667057f76aa133d90db0f5efba0d8` and `shorts.json` SHA-256 `7d352677b785667866b6ef09e7c4f4934d6659fb966f334c8d98c4ac063dcaa6`. Lint had 0 errors/0 warnings; six chapters, 15 loops, 99 shots/6 stats cards/1 outro; the substantive body had 2,015 normalized spoken units, or ~8.06 minutes of voiced words at the planned normal 250 units/minute before pauses.

The [v5 source audit](../../docs/videos/story-everyday-fedex-x11/reviews/source-audit-v5-independent.md) put one claim on HOLD: the FY2026 current use of employee couriers and service providers must be explicitly limited to **U.S. surface operations** at `x110612`; its `x11-b06-s12` image must not imply both types worked at one depot. [Blind A v5](../../docs/videos/story-everyday-fedex-x11/reviews/blind-a-v5-independent.md) passed 11/12 required story checks, with visual clarity failing because Express/Ground and Canada/U.S. have no persistent visual identity in the pivotal paired shots. [v6 author delta](../../docs/videos/story-everyday-fedex-x11/revision-v6.md) records the narrow repair; no independent v6 PASS yet.

Current v6 candidate: `video.json` SHA-256 `e8aa68f3aef2a8d8d1068152fe5cf024cfc9e91590103c37b586b338ba10d240`; `shorts.json` SHA-256 `7d352677b785667866b6ef09e7c4f4934d6659fb966f334c8d98c4ac063dcaa6` (same Shorts JSON bytes, but main-source image prompts changed). Lint 0 errors/0 warnings; six chapters, 15 loops, 99 shots/6 stats cards/1 outro, 122 lines and 2,017 normalized spoken units of substantive body, ~8.07 minutes at planned normal 250 units/minute before pauses. Next: exact-pair independent source delta and two **new** blind reads. No paid generation, push or PR until those gates and media QA.
