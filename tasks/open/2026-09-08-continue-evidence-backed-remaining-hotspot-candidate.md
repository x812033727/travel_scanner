---
id: 2026-09-08-continue-evidence-backed-remaining-hotspot-candidate
title: Continue evidence-backed remaining hotspot candidate review
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-09-08T09:35:17Z
completed_at:
branch:
depends_on: []
scope:
  - docs/hotspot-review-next-batch.md
  - ops/hotspot_review_next_batch.py
  - ops/hotspot_review_next_batch.json
---

# Continue evidence-backed remaining hotspot candidate review

## Why

After the 2026-09-08 exact-browser batch, 1,769 hotspots remain pending. Eleven of twelve independently checked Taipei/Kaohsiung candidates were approved and verified in all five locale ranking endpoints; Sun Yat-sen Memorial Hall remains pending because the building is closed. The user requested candidate review using the built-in browser or existing Gemini API, not indiscriminate approval.

## Definition of done

- [ ] Claim a bounded next batch from the current pending set and document exact identities, current official sources, coordinate provenance and decisions.
- [ ] Only candidates passing source, map and durable-coordinate checks are approved; unresolved items retain explicit reasons.
- [ ] Writes use a fresh backup, actual effective administrator, full-snapshot guards, normal services and replay-safe audit receipts.
- [ ] Verify public visibility/exclusion and report actual counts, without claiming the whole backlog is completed after one batch.

## Steps

- [ ] Read docs/hotspot-review-2026-09-08.md and the scoped one-off script before adapting a new dated manifest.
- [ ] Verify live pending data and relevant deployed code; prior containers and request authorization can expire.
- [ ] Research an explicit next batch, independently verify evidence, apply and verify outcomes.

## How to verify

Run read-only snapshots and a complete dry-run before any apply. Verify original actual administrator attribution, strict publication_gaps, normal and supplemental audit counts, same-manifest replay, and public BFF rankings/intro eligibility. Use the existing deployment locks and verify pg_restore -l on new private backups. Run Ruff, Python compilation and task checks for changed artifacts.

## Notes

The working official interactive finder is https://maps-docs-team.web.app/samples/places-placeid-finder/dist/ (linked from Google's official example). CUA AX textbox input followed by Down/Return exposes the selected actual Place ID. Do not derive a Place ID from CID/hex, persist Google coordinates/screenshots, or use paid Google matching merely because the admin UI offers it. Current official notices override old closure pages. Wikidata raw P625 can differ from old stored coordinates; verify actual JSON rank/precision/provenance and never relabel coordinates blindly. Existing one-off authorization expires; obtain valid current attribution through the existing admin workflow, never invent an actor. No quota increase, new discovery or remote Git/deployment authorization is implied by this follow-up task. Full tool tests in this isolated worktree have a missing @playwright/test dependency; focused task tests pass.
