---
id: 2026-09-29-route-b-reviewed-bundle-compiler
title: Compile reviewed Route B packs for guarded locale publication
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-route-b-bundle-compiler
claimed_at: 2026-10-05T09:32:09Z
created_at: 2026-09-29T05:56:13Z
completed_at:
branch: claude/route-b-bundle-compiler
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

- [x] Compile exactly selected missing target locales from pinned candidate,
      independent review and full baseline inputs; verify all pins before use.
- [x] Produce deterministic native packs, only selected assets, the existing
      schema-1 release manifest and a separate provenance receipt in a new safe
      output directory. Failed validation leaves no success manifest.
- [x] Feed the actual output to the existing guarded publisher and prove source,
      root metadata and unselected locales remain unchanged.
- [x] Reject stale reviews, changed documents/assets, unsafe paths, duplicate or
      widened selection, incomplete baseline, nonpublic/expired sources and any
      target already present in the initial baseline. Keep v1 missing-locales only.
- [x] Preserve editorial/source-correction and per-slug hold gates. Compiler
      success does not authorize production operations or removing a hold.
- [ ] Exercise compiler and publisher contract cases locally and in PostgreSQL
      CI; clearly leave same-image rehearsal and actual release to their tickets.

## Steps

- [x] Recheck scope ownership and the dependency's actual merged implementation.
      Draft PR #966 contains the publisher hold fix; do not duplicate its scope.
- [x] Define a truthful Route B review input schema and external SHA-256 pins.
      Require a full publisher-compatible baseline with identities, versions,
      normalized documents and visibility; public projections are insufficient.
- [x] Add the pure local compiler and focused tests. Reuse `ArticlePack`,
      baseline normalization and `publish_bundle.verify_bundle`; never synthesize
      artifacts expected by `assemble_bundle.reviewed_document`.
- [x] Copy only selected image resources and permitted same-stem SVG masters.
      Full five-locale packs can retain source assets in the deployed repository;
      the publisher rejects unused assets listed in a targets-only bundle.
- [x] Document exact selection, provenance review, rejection conditions and
      handoff to the existing dry-run/drafts/publication journal phases.
- [x] Explicitly add the new module to the release-safety workflow, including its
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

### 2026-10-05 implementation (claude-opus-5-5-route-b-bundle-compiler)

- Dependency: PR #966 merged on 2026-09-29 as `452cdd051`; the publisher reads the
  deployed hold list at dry-run, phase entry, per operation and after the durable
  intent. Nothing here changes `publish_bundle.py`. `who-is-on-it` showed no active
  claim and no open PR on any of this ticket's four paths.
- `prepare_route_b_bundle.py` takes three externally pinned inputs, each hashed from the
  exact bytes it then parses (strict UTF-8 JSON, repeated keys refused): a frozen
  candidate (`route-b-candidate-v1`: full packs under `packs/`, images under
  `public/guides/`), an independent review (`route-b-review-v1`: per slug and locale a
  PASS by a reviewer other than the translator, source and document hashes, image
  hashes, four checks, zero open findings) and the unchanged `build_baseline.py`
  output. Schemas and the refusal table are in `route-b-bundle.md`.
- Decision on "present in the initial baseline": a target with a database row (draft or
  published) is refused. A target that only exists in the repository pack
  (`repository-only` provenance, which every baseline built after the content PR
  deploys will show) is accepted only when it equals the reviewed document; otherwise
  refused. "Stale review" means its `source_sha256` is not the baseline's source.
- The source must be `published`, unexpired and cleanly published (no pending source
  edit); a public API projection (no database identity or versions) is refused. The
  compiler recomputes `locale_work` and `locale_provenance` from the baseline's own
  documents and refuses an inconsistent row.
- Out of v1 and refused: the source locale, existing locales, hubs, source corrections,
  and `aliases` for a selected locale (the publisher writes documents only, so a
  reviewed alias would silently not ship). Held slugs are refused from the repository's
  `publish_holds.json`, which is read and never written; the publisher re-reads the
  deployed list anyway.
- Output: deterministic native packs (the candidate pack re-serialized as
  `assemble_bundle` writes it), only the images the selected documents use plus a
  reviewed same-stem SVG master, the schema-1 manifest and `route-b-provenance.json`
  (`authorizes_production: false`). Everything is written to a staging directory,
  checked with `publish_bundle.verify_bundle`, and renamed into place only then; any
  refusal removes the staging directory. The output must be new and outside the
  repository and the candidate.
- Tests, from the repository root with the API environment, PYTHONUTF8=1:
  `pytest -q -o asyncio_mode=auto docs/article-localization/test_prepare_route_b_bundle.py`
  -> 54 passed, 11 skipped (8 PostgreSQL variants of the shared database fixture, the
  2 lock cases' SQLite variants, and the symlink case, which Windows cannot set up
  without privileges). With
  `test_publish_bundle.py` in the same process: 123 passed, 79 skipped. The assembly
  suites (`test_build_baseline.py`, `test_assemble_bundle.py`, `test_install_bundle.py`,
  `test_report_progress.py`): 66 passed. `ruff check tools/article-localization
  docs/article-localization` passes (ruff 0.16's default rule set includes ISC and RUF).
- The database cases compile against a real article, deploy the candidate's own pack
  bytes and images, and run the actual output through all four phases: zh-TW, root
  metadata and the unselected locales stay unchanged, a replay writes nothing, a fresh
  baseline after publication refuses the same targets, source drift stops the
  publisher before and after dry-run, a lost response and a failure before commit
  resume exactly once, and a hold added after compiling blocks publication.
- Unticked: "in PostgreSQL CI". The new file is added to the release-safety step that
  sets `RUN_INTEGRATION_TESTS=1`; its PostgreSQL variants, including a second session
  holding the publisher's advisory lock or the article row lock, skip on this machine
  (no PostgreSQL or Docker). Their result is the PR's `release-safety` run. Same-image
  rehearsal: `2026-10-05-rehearse-a-compiled-route-b-wave`. Pointing the
  `article-localization` skill at the compiler: `2026-10-05-point-the-article-localization-skill-at`.
  Actual release stays with each wave's ticket (T1:
  `2026-09-28-localize-marketing-mix-and-brand-tone`). No production connection or write.
