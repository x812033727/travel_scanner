---
id: 2026-10-28-fit-localized-svg-labels-to-required
title: Fit localized SVG labels to required inner padding
status: in-progress
priority: P1
area: tools
owner: codex-gpt6-article-locales-20261028
claimed_at: 2026-10-28T02:21:33Z
created_at: 2026-10-28T02:21:28Z
completed_at:
branch: codex/article-locales-completion-20261028
depends_on: []
scope:
  - tools/article-localization/render.mjs
  - tools/article-localization/render-layout.mjs
  - tools/article-localization/render-layout.test.mjs
---

# Fit localized SVG labels to required inner padding

## Why

Five localized Ansoff/BCG diagrams fail the renderer's four-pixel inner-padding
check even though font fitting skips them as contained. The fit trigger only
checked overflow, so seven labels remained visibly against their card borders.

## Definition of done

- [x] Font fitting handles newly introduced edge contact using the final validator's padding rule.
- [x] Existing source edge contact and the 15px font floor retain their current behavior.
- [x] Focused regression and artifact-binding checks pass; all five actual failed jobs rerender successfully.
- [x] Independent code and final-image reviews pass without content or geometry changes.

## Steps

- [x] Diagnose the measured difference between containment and edge-clearance rules.
- [x] Share the fit decision with the geometry helpers and test the previously skipped case.
- [x] Rerender only five failed jobs and preserve the three already-approved job bindings.

## How to verify

`node --test tools/article-localization/render-layout.test.mjs tools/article-localization/artifact-integrity.test.mjs`
passes 25 tests. The five previously failing native renders now pass with zero
layout issues; independent reviewers viewed the resulting images. New tests
cover contained edge contact, exactly four pixels, overflow and inherited contact.

## Notes

The fit decision now uses the same introduced-contact condition as final
validation. It changes only font sizes through the existing rendering transaction;
it does not edit text, anchors, positions, shapes, source SVGs or guard thresholds.
Independent code review binds all three changed files and found no actionable
defect. Failed render receipts and before-images remain in private external evidence.
