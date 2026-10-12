---
id: 2026-10-12-select-reviewed-existing-keyframe-take
title: Select an existing reviewed keyframe take without regeneration
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-12T08:15:41Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
---

# Select an existing reviewed keyframe take without regeneration

## Why

When several failed keyframe takes share a score, bestTake deliberately chooses the earliest seed. H04 snow-return-season had three 9.71 takes: seed1 had a visible mascot, while already purchased seed2/3 showed usable empty terrain with only a style mismatch. The CLI can retain the currently selected take with --accept-best, but cannot select a specifically reviewed existing candidate. Production required a narrowly guarded external manifest selection helper to avoid buying another image.

## Definition of done

- [ ] An operator can select one existing, exact-SHA reviewed take without any image or judge request.
- [ ] All candidates, native verdicts, problem history and needs_review/manual-final-review requirements remain intact; contact sheets and downstream approval hashes reflect the selected bytes.
- [ ] Missing files, stale source/look/picture binding, active producer/STOP and invalid candidate identities fail without changing selection.

## Steps

- [ ] Design an explicit existing-take selection option, separate from automatic bestTake ranking and acceptance.
- [ ] Add source, lease and selected-byte validation with a recoverable before/after record.
- [ ] Cover a material-versus-style tie, stale candidates, failure preservation and zero provider calls.

## How to verify

Run the relevant media/keyframe tests with the supported Node runtime. In a temporary project, choose a later candidate in an equal-score fixture, verify every unchanged take/judge byte, regenerate contact sheets through the existing path and prove that the final gate still requires owner review.

## Notes

2026-10-12 H04 source 3f2fdb0864afaa199e994f47bb180c6662e2e46efcc74da2c307e4268353e5e0. Seed2 selected SHA 4d1a6dde4ccf584a734a2a8f21e63fee15a932255f7c15a07f3732a4d9f54cbf. Local production evidence is outside git under curio-h04/_audit/snow-take-selection-2026-10-12T08-15-11-426Z/. The tie-break itself is covered by tests and is not being changed here. This follow-up is unclaimed; H04 does not modify the shared media tools.
