---
id: 2026-09-29-route-b-reviewed-bundle-compiler
title: Compile reviewed Route B packs for guarded locale publication
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-29T05:56:13Z
completed_at:
branch:
depends_on:
  - 2026-09-22-respect-per-slug-publish-holds-in
scope:
  - docs/article-localization/prepare_route_b_bundle.py
  - docs/article-localization/test_prepare_route_b_bundle.py
  - docs/article-localization/route-b-bundle.md
  - .github/workflows/article-localization.yml
---

# Compile reviewed Route B packs for guarded locale publication

## Why

Reviewed Route B packs have genuine independent document/image receipts but no
Route A job artifacts. They need a local compiler into the existing
`publish_bundle.py` manifest contract. A dry-run followed by bare `guides-import`
does not provide the publisher's durable journal or close concurrent source
changes. Do not fabricate Route A receipts or implement a second writer.

## Definition of done

- [ ] Compile exactly selected missing target locales from pinned candidate,
      independent review and full baseline inputs; verify all pins before use.
- [ ] Produce deterministic native packs, only selected assets, the existing
      schema-1 release manifest and a separate provenance receipt in a new safe
      output directory. Failed validation leaves no success manifest.
- [ ] Feed the actual output to the existing guarded publisher and prove source,
      root metadata and unselected locales remain unchanged.
- [ ] Reject stale reviews, changed documents/assets, unsafe paths, duplicate or
      widened selection, incomplete baseline, nonpublic/expired sources and any
      target already present in the initial baseline. Keep v1 missing-locales only.
- [ ] Preserve editorial/source-correction and per-slug hold gates. Compiler
      success does not authorize production operations or removing a hold.
- [ ] Exercise compiler and publisher contract cases locally and in PostgreSQL
      CI; clearly leave same-image rehearsal and actual release to their tickets.

## Steps

- [ ] Recheck scope ownership and the dependency's actual merged implementation.
      Draft PR #966 contains the publisher hold fix; do not duplicate its scope.
- [ ] Define a truthful Route B review input schema and external SHA-256 pins.
      Require a full publisher-compatible baseline with identities, versions,
      normalized documents and visibility; public projections are insufficient.
- [ ] Add the pure local compiler and focused tests. Reuse `ArticlePack`,
      baseline normalization and `publish_bundle.verify_bundle`; never synthesize
      artifacts expected by `assemble_bundle.reviewed_document`.
- [ ] Copy only selected image resources and permitted same-stem SVG masters.
      Full five-locale packs can retain source assets in the deployed repository;
      the publisher rejects unused assets listed in a targets-only bundle.
- [ ] Document exact selection, provenance review, rejection conditions and
      handoff to the existing dry-run/drafts/publication journal phases.
- [ ] Explicitly add the new module to the release-safety workflow, including its
      database-enabled command so PostgreSQL cases do not silently skip.

## How to verify

Run the new compiler tests with the API Python environment, then the existing
publisher regressions and `npm run check:tasks`. Use only synthetic full
baselines locally. Cover deterministic output, native schema acceptance,
tampered pins/receipts/paths, exact per-wave selection, source preservation,
unchanged replay, drift rejection, lost-response resume and failure before
commit. PostgreSQL tests must exercise real two-session serialization/locking
where required; SQLite cannot establish those guarantees.

The existing PostgreSQL service CI is not a rehearsal of the intended deployed
API image. A same-image isolated rehearsal, fresh explicitly approved live
snapshot, verified backup, deployment and public browser acceptance remain
separate release gates.

## Notes

Filed after local investigation on `8be1cf9bcaddd697df99e505e33f562b010cfbd0`.
The existing writer already validates the externally pinned manifest, source and
target states, deployed files and journal transitions. It does not validate an
arbitrary extra Route B review field: the compiler must validate real review
evidence, and the resulting manifest itself needs explicit review.

T1/T2 historical frozen candidates are evidence, not fresh production inputs.
Their source assets must not all be copied into a targets-only asset allowlist.
Old T2 summary findings remain unresolved for that old freeze; later source
correction requires new exact review/freeze/baseline evidence. Do not silently
substitute newer documents or add zh-TW to the publication selection.

Leave this implementation task unclaimed until the publisher hold dependency
and scope are available. No production connection or write is part of it.
