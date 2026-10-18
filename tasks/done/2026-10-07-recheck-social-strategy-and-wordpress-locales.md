---
id: 2026-10-07-recheck-social-strategy-and-wordpress-locales
title: Recheck social strategy and WordPress locales wave3b
status: done
priority: P1
area: docs
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T07:23:02Z
created_at: 2026-10-07T07:20:15Z
completed_at: 2026-10-07T10:39:33Z
branch: codex/article-locales-wave3-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/social-media-planning.json
  - apps/web/public/guides/social-media-planning
  - apps/api/app/guides/content/stp-persona-research.json
  - apps/web/public/guides/stp-persona-research
  - apps/api/app/guides/content/wordpress-500-error.json
  - apps/web/public/guides/wordpress-500-error
  - apps/api/app/guides/content/wordpress-ad-placement.json
  - apps/web/public/guides/wordpress-ad-placement
  - apps/api/app/guides/content/wordpress-social-embeds.json
  - apps/web/public/guides/wordpress-social-embeds
  - apps/api/app/guides/content/wordpress-social-login.json
  - apps/web/public/guides/wordpress-social-login
  - docs/article-localization/wave3-life-review-b-20261007.md
---

# Recheck social strategy and WordPress locales wave3b

## Why

Six public life articles have complete repository translations in en, ja, ko and
zh-CN, but none of those24 targets is published. Independently review the existing
social-strategy and WordPress documents and artwork, preserving original sources
and media while applying only exact reviewed target corrections.

## Definition of done

- [x] All24 targets have actual independent full text, image, glyph and link review.
- [x] Every admitted target has hash-bound PASS with no open findings; withheld
      source errors have narrow follow-up tickets and are excluded from compilation.
- [x] A distinct executor applies reviewed corrections and preserves the original inputs.
- [x] Scoped lint and prospective official compilation verify the exact reviewed bytes.
- [x] A separate release ticket retains merge/deployment/publication and public QA gates.

## Steps

- [x] Compare fresh public originals with repository and original baseline hashes.
- [x] Pin source/master media and all current target inputs outside Git.
- [x] Complete cross-worktree/remote/PR ownership and original-producer checks.
- [x] Read every full source and target; view actual source/target SVG and raster renders.
- [x] Apply independent findings, render again and re-review final exact outputs.
- [x] Validate reviewed packs and compile/recompile the admitted targets with official guards.
- [x] Record public-safe evidence and open a narrow release ticket without claiming publication.

## How to verify

Use GuideDocument-normalized document digests and actual asset byte hashes.
Authentic independent reviews must bind every final target. Run pack_cli lint
for these six slugs, the official review loader/compiler and verify_bundle;
compare every recompiled file hash. Future publication requires a genuinely
fresh deployed baseline, current database guards, backup/restore and owner choice.

## Notes

- Selected: social-media-planning, stp-persona-research, wordpress-500-error,
  wordpress-ad-placement, wordpress-social-embeds and wordpress-social-login.
- All six sources match the original baseline and current public source; original
  source/master assets and root metadata are byte-pinned outside Git.
- Source/public screen SHA:
  `5af424199b71147b582d6e9f4da928aee8feabd31029afdb2c759b6875793040`.
- The source-drift WordPress articles blog-build/comment-spam/performance-plugins/
  reset-safely are separate and remain excluded; paid-vs-organic remains held.
- This task owns local review/corrections only. No merge, deployment or production
  publication has occurred in this program.

Final independent current-hash review:24 PASS; original review SHA
`8b309a0e397f949eaf539e972ae558f68748d7242cb14916289fe8b49ddeb611`,
evidence SHA `fdf40bcdf70b8d2f0040ff8131ed09c9c79a0fc8930f36133c2c45b61fb36d12`.
The official loader accepts all24 rows. Root combined A/B48 rows verbatim and
verified1003 evidence children,180 media pins and original source/DB guards.
Prospective compile/recompile from an exact commit is still pending; this task
is not done yet. See the scoped public review note for actual corrections and
verification limits. No production publication occurred.

Combined twelve-article final pack lint exits0 with zero errors; inherited
missing-summary/English-length advisories remain. No source text was removed
to satisfy those advisory limits. Exact-commit prospective compilation is the
remaining local authoring check.

Official exact-freeze prospective compilation/recompilation completed:48 targets,
12 articles,180 candidate assets,144 selected assets, all158 bundle files exact.
Both official verify_bundle calls pass; original review attribution/hashes and
source/database guards remain intact. Manifest
`e0492c0f2e438264f784f08d2a2d162e77f20dfa4e6ae004b401b7fb4cd8dad1`; verification
`967d33f5393e479e73b571095474bd8fa08a6d4da56a60fddb64aea02310e48c`. The retained snapshot is not fresh deployment evidence.
The scoped public documents and separate open wave3 release ticket retain the
production handoff. A final-PR-head external compilation is still required before
its later readiness/deployment/publication gates.
