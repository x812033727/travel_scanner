---
id: 2026-10-23-preserve-c-series-episode-evidence-before
title: Preserve C-series episode evidence before PR closeout
status: in-progress
priority: P1
area: docs
owner: codex-c-series-integration
claimed_at: 2026-10-23T09:21:22Z
created_at: 2026-10-23T09:21:17Z
completed_at:
branch: codex/everyday-story-review-import-20261023
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

- [ ] All C01–C20 evidence folders and distinct independent receipts are preserved in one
      reviewable integration PR; original approved `script.md` SHA-256 values remain unchanged.
- [ ] Each open C-series PR is accounted for before merge or close, with any unique code or
      media outside this narrow documentation scope handled separately.

## Steps

- [x] Restore the twenty tracked episode folders from their latest authored and pilot heads.
- [x] Restore independent receipts from separate review PRs without converting HOLD to PASS.
- [ ] Audit provenance, repository hygiene and the integration PR diff.
- [ ] Close superseded PRs only after the reviewed content is durable and imported.

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
