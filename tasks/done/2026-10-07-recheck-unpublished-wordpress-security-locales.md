---
id: 2026-10-07-recheck-unpublished-wordpress-security-locales
title: Recheck unpublished WordPress security locales
status: done
priority: P2
area: docs
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T05:26:30Z
created_at: 2026-10-07T05:26:23Z
completed_at: 2026-10-07T06:11:06Z
branch: codex/article-missing-locales-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-security-basics.json
  - apps/web/public/guides/wordpress-security-basics
  - docs/article-localization/wordpress-security-review-20261007.md
  - tasks/open/2026-10-07-recheck-unpublished-wordpress-security-locales.md
---

# Recheck unpublished WordPress security locales

## Why

The published zh-TW source is unchanged, but en, ja, ko and zh-CN still have
no database locale rows. Existing Batch031 translations and art were reviewed
again on 2026-10-07. Eight terminal related-reading labels differ from the
actual published titles in their own locales and need exact corrections before
a fresh guarded-release review receipt can be issued.

## Definition of done

- [x] Apply the eight exact reviewed link-label corrections through a party
      distinct from the independent reviewer.
- [x] Preserve the zh-TW document, root metadata and all existing assets.
- [x] Independently recheck all four corrected document hashes and produce a
      current route-b-review-v1 receipt with no unresolved findings.
- [x] Record compiler-ready evidence; merge, deployment and publication remain
      separate steps and are not implied by this content review.

## Steps

- [x] Verify the current production snapshot source hash, absent targets,
      aliases/holds, and task/worktree/PR scope conflicts.
- [x] Review every source/target block and primary cited source; render and
      inspect all eight target SVGs plus four actual hero JPGs.
- [x] Prepare exact pointer corrections externally for root application.
- [x] Receive the application receipt and independently recheck the final pack.
- [x] Persist reviewed source/document/asset bindings and local validation.

## How to verify

Validate the pack with GuideDocument/ArticlePack, compare it to the preserved
original with only the eight approved pointer changes, and check the source
hash remains `f6d8210b4aafdc0e2bd60ec1a450bd92908baa477cd6a0d3d4eaf85f32fcea94`.
Recheck all image SHA-256 values and same-locale published target titles from
the retained production snapshot. Run scoped pack lint and task-format checks.

## Notes

The independent reviewer is
`codex-current-independent-next-review:/root/localization_existing_work`.
The reviewer must not apply the article corrections. Root is the distinct
application party. Original pack SHA-256:
`cdf7a2d7e585878448f1fdd9e1a902187d665d88972676ffbbfb49d208f62f28`.

Private current evidence lives under
the owner's persistent storage, under the current independent-review evidence.
`findings.json` SHA-256 is
`e7f567907ebb7a4665a09d999fc5db2a54fca08617199cf9eeb61101ccd4da46`;
`review-evidence.json` SHA-256 is
`38eed3ada64824e526998d32691709f65b97847ca685cf4f6889dd58b98fecc0`.
At claim, the originals are CORRECTIONS_REQUIRED, not PASS. All changes stay
in the four target documents; there are no source corrections or production
writes in this task.

Root applied the exact eight changes; independent final review PASS for all
four targets. Corrected pack SHA-256:
`3f302f520a3c83f2ec972736761d0e6738d94699e925c90970867c7c321806bf`.
Combined current route-b-review receipt SHA-256:
`6215361cac8abb391690d973feee8dc1b775400ab4477f8384b83fbd61e0bf72`.
Final evidence SHA-256:
`28b83c1c26db0c0a2ee57795fbccc6e09a19262e7bdc9665c698c0b905d79c49`.
See `docs/article-localization/wordpress-security-review-20261007.md` for
the sanitized current hashes and checked scope. Task closure awaits the
prospective content PR; no merge, deploy, import or publication is implied.

## Final cohort review, 2026-10-07

Current independent final review at 2026-10-07T05:57:52.724199+00:00 verifies this task's
exact current content, unchanged source/root metadata/assets and all same-cohort
terminal link labels. Combined 32-row route-b receipt SHA-256
`87986003cd9e266df5e569270ab3d2859f1573433d5c0f1d967c331e1969beaa`; common evidence SHA-256
`d6e10b7546c48b0cdd76c0c03517c6d8ba0a2c0a84a99462ada3e6ed74e91527`.
Use only the immutable external `reuse-t1/life-cohort-final-review-v2` receipts.
All current eight life-pack lints exited 0; no production publication is claimed.
The prospective content PR must freeze exact committed blobs separately.

### Content PR handoff

PR: https://github.com/x812033727/travel_scanner/pull/1365.
Authoring, exact independent review, local validation and local installation/replay
are complete for this ticket's selected scope. Required GitHub checks and merge
remain enforced PR gates; marking this authoring ticket done does not claim those
checks are green. The PR remains draft pending owner approval.
Production deployment, publication and public desktop/mobile verification remain
open in 2026-10-07-release-localized-travel-life-wave-20261007.
Any unchecked CI/merge/publication lines above are handed to those explicit gates,
not waived or reported as completed.
