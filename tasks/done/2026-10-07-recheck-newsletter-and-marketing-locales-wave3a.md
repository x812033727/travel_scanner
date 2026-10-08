---
id: 2026-10-07-recheck-newsletter-and-marketing-locales-wave3a
title: Recheck newsletter and marketing locales wave3a
status: done
priority: P1
area: docs
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T07:22:53Z
created_at: 2026-10-07T07:20:09Z
completed_at: 2026-10-07T10:37:26Z
branch: codex/article-locales-wave3-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/content-marketing-calendar.json
  - apps/web/public/guides/content-marketing-calendar
  - apps/api/app/guides/content/email-newsletter-planning.json
  - apps/web/public/guides/email-newsletter-planning
  - apps/api/app/guides/content/influencer-collaboration.json
  - apps/web/public/guides/influencer-collaboration
  - apps/api/app/guides/content/kit-newsletter-setup.json
  - apps/web/public/guides/kit-newsletter-setup
  - apps/api/app/guides/content/mailchimp-wordpress-newsletter.json
  - apps/web/public/guides/mailchimp-wordpress-newsletter
  - apps/api/app/guides/content/short-video-marketing.json
  - apps/web/public/guides/short-video-marketing
  - docs/article-localization/wave3-life-review-a-20261007.md
---

# Recheck newsletter and marketing locales wave3a

## Why

Six public life articles have complete repository translations in en, ja, ko and
zh-CN, but none of those24 targets is published. Reuse the existing documents
after independent whole-document/image review rather than buying duplicate
translations. Preserve the source, original media and root metadata.

## Definition of done

- [x] All24 targets have actual independent full text, image, glyph and link review.
- [x] Every admitted target has hash-bound PASS with no open findings; withheld
      source errors have narrow follow-up tickets and are excluded from compilation.
- [x] A distinct executor applies only reviewed corrections and preserves originals.
- [x] Scoped lint and prospective official compilation verify the exact reviewed bytes.
- [x] A separate release ticket retains merge/deployment/publication and public QA gates.

## Steps

- [x] Compare fresh public originals with repository and original baseline hashes.
- [x] Pin original source/master media and all current target inputs outside Git.
- [x] Complete cross-worktree/remote/PR ownership and original-producer checks.
- [x] Read every full source and target; view actual source/target SVG and raster renders.
- [x] Apply independent findings, render again and re-review final exact outputs.
- [x] Validate reviewed packs and compile/recompile the admitted targets with official guards.
- [x] Record public-safe evidence and open a narrow release ticket without claiming publication.

## How to verify

Use GuideDocument-normalized document digests, actual asset byte hashes and
authentic independent review receipts. Run pack_cli lint for these six slugs,
the official review loader/compiler and verify_bundle; compare every recompiled
file hash. A retained snapshot is prospective evidence, never a fresh production
release baseline. Public APIs do not prove absence of private database drafts.

## Notes

- Selected: content-marketing-calendar, email-newsletter-planning,
  influencer-collaboration, kit-newsletter-setup,
  mailchimp-wordpress-newsletter and short-video-marketing.
- Source/public safety screen has all12 proposed life sources equal to repository
  and original baseline, with all48 target API documents unpublished/null.
  Screen SHA: `5af424199b71147b582d6e9f4da928aee8feabd31029afdb2c759b6875793040`.
- Independent reviewer is distinct from original producers and the root executor.
  Review evidence and raw snapshots remain in the persistent external work root.
- Existing first18 reviewed articles, old provider attempts and source holds are
  outside this task. No merge, deployment or production write is authorized by it.

Final genuine A review has24 PASS, SHA
`4610aac73c83f55d7ee050a915ecffe4defb33212ae20108e70db64b88956717`;
complete evidence
`7a97597b1a9a739be1f2381d3363824f81bb92632a15d41606f32dd1e0cecc5b`.
Root preserved original A/B rows verbatim, verified1003 child evidence files and
all180 media pins, and ran combined twelve-article final pack lint: exit0,
zero errors, inherited missing-summary/English-length advisories only.
Official exact-commit prospective compilation remains pending. The scoped
public note and separate open wave3 release ticket contain the handoff.

Official exact-freeze prospective compilation/recompilation completed:48 targets,
12 articles,180 candidate assets,144 selected assets, all158 bundle files exact.
Both official verify_bundle calls pass; original review attribution/hashes and
source/database guards remain intact. Manifest
`e0492c0f2e438264f784f08d2a2d162e77f20dfa4e6ae004b401b7fb4cd8dad1`; verification
`967d33f5393e479e73b571095474bd8fa08a6d4da56a60fddb64aea02310e48c`. The retained snapshot is not fresh deployment evidence.
The scoped public documents and separate open wave3 release ticket retain the
production handoff. A final-PR-head external compilation is still required before
its later readiness/deployment/publication gates.
