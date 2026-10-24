---
id: 2026-10-23-preserve-c-series-episode-evidence-before
title: Preserve C-series episode evidence before PR closeout
status: done
priority: P1
area: docs
owner: codex-c-series-integration
claimed_at: 2026-10-23T16:30:51Z
created_at: 2026-10-23T09:21:17Z
completed_at: 2026-10-24T00:50:36Z
branch: codex/c-series-evidence-c19-v5-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-crocs-c01
  - docs/videos/story-everyday-tupperware-c02
  - docs/videos/story-everyday-moleskine-c03
  - docs/videos/story-everyday-bubble-wrap-c04
  - docs/videos/story-everyday-kincho-c05
  - docs/videos/story-everyday-play-doh-c06
  - docs/videos/story-everyday-dr-martens-c07
  - docs/videos/story-everyday-kikkoman-c08
  - docs/videos/story-everyday-patagonia-c09
  - docs/videos/story-everyday-oxo-c10
  - docs/videos/story-everyday-ucc-c11
  - docs/videos/story-everyday-pyrex-c12
  - docs/videos/story-everyday-victorinox-c13
  - docs/videos/story-everyday-camelbak-c14
  - docs/videos/story-everyday-frixion-c15
  - docs/videos/story-everyday-bialetti-c16
  - docs/videos/story-everyday-nalgene-c17
  - docs/videos/story-everyday-fiskars-c18
  - docs/videos/story-everyday-seven-bank-c19
  - docs/videos/story-everyday-zippo-c20
  - docs/videos/story-everyday-pyrex-c12-script
  - docs/videos/story-everyday-pyrex-c12-review
  - docs/videos/story-everyday-patagonia-c09-review
  - docs/videos/story-everyday-patagonia-c09-revised-script-review
  - docs/videos/story-everyday-patagonia-c09-script-review
  - docs/videos/story-everyday-bubble-wrap-c04-pilot
  - docs/videos/brand-story-independent-reviews
  - docs/videos/brand-story-owner-approvals
---

# Preserve C-series episode evidence before PR closeout

## Why

The twenty C episodes were spread across independent draft PRs. Closing those PRs before
retaining their treatments, source matrices, owner-approved script bytes and independent
review receipts would erase the reliable route from a backend row to the evidence behind it.
The user also reported 85 disposable checkouts consuming 55.6 GB, so this reconciliation
uses one existing checkout and creates no new worktree.

## Definition of done

- [x] All C01–C20 evidence folders and distinct independent receipts are preserved on main
      through integration PR #1778 and C19 corrections #1792 and #1795; original approved
      `script.md` SHA-256 values remain unchanged.
- [x] Each open C-series PR is accounted for before merge or close, with any unique code or
      media outside this narrow documentation scope handled separately.

## Steps

- [x] Restore the twenty tracked episode folders from their latest authored and pilot heads.
- [x] Restore independent receipts from separate review PRs without converting HOLD to PASS.
- [x] Audit provenance, repository hygiene and the integration PR diff.
- [x] Close superseded PRs only after the reviewed content is durable and imported.

## How to verify

`git diff --cached --name-status`, `Get-FileHash -Algorithm SHA256` on the ten approved scripts,
`npm run check:tasks`, and the exact C-series PR inventory with head SHAs and disposition.

## Notes

Copied 20 folders (361 text files, about 2.8 MB) into the single integration checkout.
No media workdir, final.mp4 or clone was copied; this is a source/evidence preservation task.
Some retained source reviews record HOLD. Their presence does not make that episode approved.

Live PR path inventory found additional standalone review and pilot folders outside the twenty
main episode folders. The owner asked to close the draft stack after preservation, so this
claimed scope was extended only to those exact sibling evidence folders. Their PR heads will
be fetched into this same checkout; no extra worktree is needed.

2026-10-24 follow-up audit: integration PR #1778 is merged and there are no open C01–C20
PRs. Final author PR #1742 was closed, but its v5 C19 script and visuals were not the
version in `origin/main`: main had v3. Restored only the four exact author v5 files from
`83415c48249250c3cff6e302c1d7a79514377610` in this existing checkout. The
independent v5 full-source and final-seven-visual receipts bind those SHA-256 values.
Added a 79-line locked narration projection, two fresh independent blind-read receipts,
and `reviews/v5-main-reconciliation-20261024.md`. Both readers HOLD the narrative, so
this is evidence preservation, not owner script approval or a paid production release.
`npm run check:tasks` passes (pre-existing shared-queue warnings); `git diff --check`
passes. `npm run test:docs-videos` runs 235/236 tests green; unrelated existing Windows
test `docs/videos/imported-long-languages/runner.test.mjs:679` reproduces a child Node
exit 3221226505, with no stderr, and is being triaged separately. No new worktree made.

2026-10-24 final preservation audit: #1778 and C19 follow-ups #1792/#1795 are all
merged. The current tree contains all twenty episode folders and distinct C09/C12
review siblings. All eleven entries in `approved-scripts.json` match their current
`script.md` SHA-256 values; the original ten hashes match the #1778 manifest.
No episode C01–C20 PR remains open; the separate #1802 PR only closes the
preproduction progress task. C01/C02 preview media and audio acceptance remain
in `2026-10-23-verify-c01-c02-preview-media-and`; C03–C06 prior charges and
budget routing remain in `2026-10-23-reconcile-c-series-prior-charges-and`.
This closes source/evidence preservation, not media QA, paid production or
upload readiness.
