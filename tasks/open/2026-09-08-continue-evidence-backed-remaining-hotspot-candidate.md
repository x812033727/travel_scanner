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

- [x] Claim a bounded next batch from the current pending set and document exact identities, current official sources, coordinate provenance and decisions.
- [x] Only candidates passing source, map and durable-coordinate checks are approved; unresolved items retain explicit reasons.
- [x] Writes use a fresh backup, actual effective administrator, full-snapshot guards, normal services and replay-safe audit receipts.
- [x] Verify public visibility/exclusion and report actual counts, without claiming the whole backlog is completed after one batch.

## Steps

- [x] Read docs/hotspot-review-2026-09-08.md and the scoped one-off script before adapting a new dated manifest.
- [x] Verify live pending data and relevant deployed code; prior containers and request authorization can expire.
- [x] Research an explicit next batch, independently verify evidence, apply and verify outcomes.

## How to verify

Run read-only snapshots and a complete dry-run before any apply. Verify original actual administrator attribution, strict publication_gaps, normal and supplemental audit counts, same-manifest replay, and public BFF rankings/intro eligibility. Use the existing deployment locks and verify pg_restore -l on new private backups. Run Ruff, Python compilation and task checks for changed artifacts.

## Notes

The working official interactive finder is https://maps-docs-team.web.app/samples/places-placeid-finder/dist/ (linked from Google's official example). CUA AX textbox input followed by Down/Return exposes the selected actual Place ID. Do not derive a Place ID from CID/hex, persist Google coordinates/screenshots, or use paid Google matching merely because the admin UI offers it. Current official notices override old closure pages. Wikidata raw P625 can differ from old stored coordinates; verify actual JSON rank/precision/provenance and never relabel coordinates blindly. Existing one-off authorization expires; obtain valid current attribution through the existing admin workflow, never invent an actor. No quota increase, new discovery or remote Git/deployment authorization is implied by this follow-up task. Full tool tests in this isolated worktree have a missing @playwright/test dependency; focused task tests pass.

## 2026-09-12 batch

`docs/hotspot-review-next-batch.md` has the full write-up and
`ops/hotspot_review_next_batch.json` the row-level receipt. Pending went 987 -> 458.

The batch was not bounded to a dozen rows: all 987 were judged from a pre-built Wikidata +
Wikipedia evidence pack, every proposed rejection was put to two independent skeptics (90 of
132 overturned, 42 applied), and the map-identity gate was filled for 469 keeps through the
admin's own `map-candidates` endpoint, which bills Text Search Pro rather than the Place
Details tier that was already exhausted for September.

Writes went through the normal `POST /admin/hotspots/review` route from a logged-in admin
session in the browser, so attribution and audit receipts are the ordinary ones; no one-off
server script and no invented actor. Coordinates stayed `wikidata` on every row.

What this task still covers:

- 123 Korean rows cannot be approved without a `map.naver.com/p/entry/place/` URL. Blocked on
  `2026-09-06-naver-maps-key`, though note the gate wants the URL, not the API key.
- 233 rows judged `unsure` - mostly Hong Kong and Bangkok streets and municipal buildings with
  two-sentence articles. These need a person who knows the city.
- 49 rows whose Google candidate was a different place, and 14 whose Place ID already belongs
  to a published row (a duplicate signal worth chasing).
- 12 unresolvable AI-candidate names worth re-seeding by hand; they are listed in the doc.

Two findings were filed separately: `2026-09-12-denylist-tombstones-real-attractions` (three
of PR #403's seven deny types would tombstone real sights on 2026-09-15) and the observation
that `collect_hotspots` downgrades every `auto_approved` candidate to
`pending / map_identity_required`, which is why whitelisting a type never publishes anything
on its own.

A second session was draining the same queue at the same time; 61 of the rejections and 18 of
the approvals in the production window are theirs, not this batch's.
