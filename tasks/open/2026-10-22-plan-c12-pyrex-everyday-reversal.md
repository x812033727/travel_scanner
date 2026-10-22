---
id: 2026-10-22-plan-c12-pyrex-everyday-reversal
title: Plan C12 Pyrex everyday reversal Treatment and source matrix
status: in-progress
priority: P2
area: docs
owner: codex-root-pyrex-c12
claimed_at: 2026-10-22T13:43:07Z
created_at: 2026-10-22T13:42:57Z
completed_at:
branch: codex/brand-story-pyrex-c12-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12
---

# Plan C12 Pyrex everyday reversal Treatment and source matrix

## Why

Series slate C12 described laboratory glass becoming kitchenware. The currently readable Corning Museum history instead starts with Nonex for railway lantern globes, a family kitchen experiment, further cooking-formula work, and 1915 ovenware. Current U.S. consumer, French consumer, and Corning laboratory products also have different material claims. A treatment must distinguish these lines before the story can be scripted.

## Definition of done

- [x] Six-chapter Treatment follows one causal story with Curio visual and hook rules.
- [x] Source matrix ties each proposed factual claim to direct sources and limits.
- [ ] Independent reviewer reopens sources and binds final hashes.
- [ ] Owner adopts the reviewed Treatment before script authoring.

## Steps

- [x] Check no active scope owner, branch, or PR for C12.
- [x] Read museum and brand primary pages directly and correct the series slate premise within this episode.
- [x] Write draft Treatment and source matrix in this episode folder.
- [ ] Hand a separate narrow review scope to a different agent.

## How to verify

Get-FileHash docs/videos/story-everyday-pyrex-c12/treatment.md -Algorithm SHA256
Get-FileHash docs/videos/story-everyday-pyrex-c12/source-matrix.md -Algorithm SHA256
npm run check:tasks
git diff --cached --check

## Notes

Direct read 2026-10-22: Corning Museum S1/S2 gives Nonex railroad lanterns, Bessie Littleton's battery-jar-bottom cooking trials, later formula work, 1915 12 consumer ovenware items, and promotion through home economists. Museum FAQ S3 says U.S. consumer bakeware was originally borosilicate but has long used heat-strengthened soda-lime. Its 2025 research FAQ S6 adds that all-caps versus lower-case branding does not establish any old item's formulation. Pyrex EU S4/S7 provides a French borosilicate product example; Corning lab FAQ S5 is a separate PYREX product line. No original diary, original patent, contemporary sales ledger, precise U.S. formula-switch year or per-object material assay read. The EU page contains a 1916 dish line beside its 1915 brand banner; use the museum's 1915 first assortment claim narrowly and ask reviewer to recheck. No paid generation or script authorized.
