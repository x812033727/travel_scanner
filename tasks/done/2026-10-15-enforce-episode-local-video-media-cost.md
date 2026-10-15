---
id: 2026-10-15-enforce-episode-local-video-media-cost
title: Enforce episode-local video media cost ceiling
status: done
priority: P1
area: tools
owner: codex-gpt6-curio-h09
claimed_at: 2026-10-15T00:56:39Z
created_at: 2026-10-15T00:56:25Z
completed_at: 2026-10-15T02:19:06Z
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - tools/video/media/stages.mjs
  - tools/video/media/stages.test.mjs
  - .agents/skills/animation-production/scripts/drama_preflight.mjs
  - tools/animation-production.test.mjs
  - docs/videos/DRAMA.md
---

# Enforce episode-local video media cost ceiling

## Why

H09 image generation was stopped by auto-review: the offline preflight prices every picture as Gemini Pro (US$39.74 for 92 shots x three takes) while the approved series selects MiniMax image-01 (catalog estimate US$3.726 including judge). The production path has only a shared US$200 media cap and may retry an uncertain, separately charged judge call. H09 has a US$4.50 combined narration, QA and art authorization, so this needs an episode-local estimated media limit before paid calls.

## Definition of done

- [x] Preflight prices a series image_model at its canonical catalog rate and no longer reports the Gemini default for H09.
- [x] H09 look/keyframes image and judge calls check the persisted episode media limit before POST; interrupted or uncertain judge calls stay reserved and cannot silently retry.
- [x] H09 has a visible estimated US$3.84 image/judge media limit after reserving US$0.66 for completed TTS and audio QA; the whole paid image batch passes auto-review before purchase.

## Steps

- [x] Confirm task scope has no active owner or touching PR and claim it on the H09 branch.
- [x] Correct the offline preflight model price with a regression test.
- [x] Apply the episode-local cap and fail-safe judge reservation with focused tests.
- [x] Record quote, authorization and invoice-level uncertainty; run scoped checks and request auto-review of the unchanged whole-episode paid batch.

## How to verify

`node --test tools/video/media/stages.test.mjs tools/video/media/media.test.mjs tools/animation-production.test.mjs`; `npm run test:tools`; `npm run check:tasks`; H09 `drama_preflight.mjs --stage keyframes`, `keyframes --dry-run --takes 3`, and `media-status --slug curio-h09` must all agree on the selected model and effective cap before any paid call.

## Notes

Owner authorized US$4.50 total, not the shared US$200 server cap. Reserve US$0.16 estimated TTS and up to US$0.50 audio QA, leaving a US$3.84 estimated media cap. These are list-price estimates: prior Gemini QA usage was not retained and judge US$0.01 is a catalog estimate, so an invoice-level cap cannot be claimed. The auto-review rejection stopped the paid image command before any image POST.

2026-10-15 focused verification: `stages.test.mjs` 30/30 passes, including image and judge reservations, unknown POST results, positive-cost failed image jobs and same-key retry refusal. H09 offline preflight and live dry-run agree on 92 image-01 frames at US$1.242 first pass / US$3.726 maximum three passes; live `media-status` reports image-01 ready and H09 spend US$0.00. `npm run check:tasks` passes. Full `npm run test:tools` hit multiple unexplained Windows child-process failures and was stopped; it is not a green result. Paid generation remains pending auto-review.

Later checkpoint: auto-review accepted the same whole-episode paid command after the H09 `media_cap_usd: 3.84` guard and catalog-based preflight were installed. A STOP-bounded pilot bought 11 MiniMax images and 11 judge calls for the local catalog estimate US$0.1485, without an outstanding reservation; the cost guard is therefore exercised by real H09 calls. Revised `stages.test.mjs` passes 32/32 outside the restrictive Windows sandbox, and Linux CI at 8cd022593 passes the affected paid media assertions; its only failing check is the separately owned stale duration-review receipt, subsequently rebound at 49203152f. The prior Gemini narration and QA charges remain estimates rather than invoice totals, so this ticket establishes an estimated stop ceiling, not an invoice guarantee. H09's remaining image quality and final film are tracked by the episode task.
