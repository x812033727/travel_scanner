---
id: 2026-10-07-localize-taiwan-2027-holiday-planning
title: Localize Taiwan 2027 holiday planning
status: done
priority: P1
area: docs
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T07:26:59Z
created_at: 2026-10-07T07:26:48Z
completed_at: 2026-10-07T09:00:54Z
branch: codex/article-locales-wave3-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/taiwan-long-weekends-2027-flight-planning.json
  - apps/web/public/guides/taiwan-long-weekends-2027-flight-planning
  - docs/article-localization/taiwan-holidays-review-20261007.md
  - docs/article-localization/installations/taiwan-long-weekends-2027-flight-planning.json
---

# Localize Taiwan 2027 holiday planning

## Why

The public Taiwan2027 holiday-planning article has only zh-TW. Add its four
missing languages from the verified current source, including all diagram text,
without updating dated claims, changing the audience or modifying original media.

## Definition of done

- [x] Four complete target documents and localized text images pass independent
      whole-document, visual, glyph and link review bound to their final artifacts.
- [x] Actual native diagram labels are at least15px and have no cross-legend overlap.
- [x] Source document, root metadata and original source/master media remain exact.
- [x] Official assembly, verification and local installation/replay pass without bypasses.
- [x] Scoped content checks pass and a separate release ticket owns production/public QA.

## Steps

- [x] Preserve source-review receipt, fresh public source hashes and ownership proof.
- [x] Prepare fresh official jobs outside Git, retaining original baseline and attempts.
- [x] Run ChatGPT-authenticated Codex CLI with workers3 and retries0; stop on quota/auth failure.
- [x] Render every target and independently review full prose, diagrams, photo and links.
- [x] Have a distinct executor apply exact findings, then re-render and re-review final bytes.
- [x] Assemble/verify/install the reviewed bundle and prove a byte-identical local replay.
- [x] Record public-safe evidence, validate the pack and create a separate release ticket.

## How to verify

Use the unchanged official pipeline.py with explicit slug, en/ja/ko/zh-CN,
baseline and external work directory; validate every job artifact and final
independent review. Run render.mjs, assemble_bundle.py, verify_bundle and
install_bundle.py. Bind job, document, asset and manifest hashes, preserve
original inputs, and run pack_cli lint plus applicable content checks.

## Notes

- Initial independent source check verifies the official2027 calendar announcement,
  all leave calculations, Japan/Korea overlaps and dated Nozomi reference. The
  three source assets match public bytes, repository and original baseline.
- Fresh public/ownership proof must be saved before starting provider work. Older
  source-preservation checkout has broad missing API files; determine actual
  competing ownership rather than inferring release from inactivity or deletion.
- Article inline to held Lunar content must be handled by the existing official
  assembly/publication guards. Do not relax them or create a dead foreign link.
- This ticket covers authoring only. Merge, deployment and publication approval,
  fresh deployed baseline, backup/restore and full public QA remain separate.

Earlier offline checkpoint: all four original CLI attempts are retained; the initial
run exited with numeric-guard findings for en/ja, then a distinct root executor
applied precisely reviewed numeric formatting and officially materialized them
without another provider request. All four jobs reached rendered state. This
automated result did not constitute editorial acceptance. The independent final
review subsequently found an English legend overlap and four14px labels. Exact
short-label proposals, re-rendering, renewed final review and new immutable input
plan v2 are required before assembly. The v1 plans and failing artifacts remain
preserved. No content-pack, deployment or production publication is credited yet.

Final resolution: all four genuine independent final reviews pass. The distinct
root executor applied the exact 15 findings, materialized and rendered again,
and the reviewer confirmed all 64 native text nodes are at least15px with the
English legend clear of the Japan block. Official review/artifact verification,
assembly, bundle verification, installation and replay all exit0. Manifest
`d66c992766fa3158ea6e89c6a952fb1ef98c1190749c09bd8e91db8dee119b85`;
installation/replay evidence
`eaf004f9c459cb8180f9558a5e919a17efca1b4b76e2feef423acee9536fef93`.
All seven operations, backups, journal and admission bytes match after replay;
all four external jobs pass drift/artifact/admission guards. Scoped pack lint
checks one entry with zero errors and the inherited English-length advisory.
Public-safe details are in the scoped Taiwan review note. Production/public QA
remain with `2026-10-07-release-wave3-travel-and-life-article`; this authoring
task's completion is not deployment or publication.
