---
id: 2026-10-07-keep-executable-language-runtime-current
title: Keep executable language runtime current without overwriting persisted video docs
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-10-07T01:27:08Z
completed_at:
branch:
depends_on: []
scope:
  - ops/video/sync-docs.mjs
  - ops/video/sync-docs.test.mjs
  - ops/video/README.md
---

# Keep executable language runtime current without overwriting persisted video docs

## Why

During the 2026-10-07 renewed-final handoff, copying the worker's writable
`/opt/mokaair/docs/videos` produced an old imported-language runner without
`prepareApprovedFinalBatch`, although deployed Git `202430417` contains it.
`sync-docs.mjs` intentionally preserves existing top-level directories to protect
authored video docs; executable helpers inside those directories also remain old.
An operator must be able to select the deployed executable runtime while retaining
the owner's existing video documents and uncertain provider evidence.

## Definition of done

- [ ] Existing authored video directories, translations and provider receipts retain
      their bytes when a newer deployed language runner is selected.
- [ ] The documented source of executable helpers is immutable deployed source or
      an explicitly verified seed, with its actual version/hash recorded.
- [ ] A persisted directory containing an old runner cannot silently supply a
      different executable version to source-bound language preparation.

## Steps

- [ ] Reproduce the old persisted imported-language directory against a new seed.
- [ ] Choose and document a narrow executable-runtime source policy without blindly
      overwriting owner content; extend scope if moving helpers is necessary.
- [ ] Add a regression covering executable freshness and byte preservation.

## How to verify

Run `node --test ops/video/sync-docs.test.mjs` and the relevant tools checks. Verify
the selected runner's real exported preparation entry point, not only image/HEAD
labels. Use temporary fixture directories; this ticket does not authorize production
deployment, volume replacement or media generation.

## Notes

- Production Git runner SHA256:
  `5c1c489e3ef737519f301dc471ea8d8c0c464e7d7fdd57564488a120073e98b0`.
- Runner copied from the writable worker docs volume:
  `c869420eb1a966e1d2b1b6098051c95984bdebc42c104146d8af26e36942092d`.
  This is a volume hash, not proof that the immutable image seed is old.
- The current handoff avoided a service/volume change: it preserved the original
  frozen runtime and archived exact deployed Git source into an isolated
  `/root/renewed-finals-20261007/runtime-v2`, including companion modules, the full
  tools tree and the already pinned pinyin-pro dependency. Preparation restarted
  only after proving the import failure had created no workspace, lock or request.
- Continue existing preservation semantics. Do not refresh every authored document
  merely to fix executable helper selection.
