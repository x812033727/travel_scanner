---
id: 2026-10-07-coordinate-refund-localization-installation-journal
title: Coordinate refund localization installation journal
status: done
priority: P1
area: tools
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T06:21:37Z
created_at: 2026-10-07T06:21:32Z
completed_at: 2026-10-07T06:37:47Z
branch: codex/refund-source-correction-v2-20261007
depends_on: []
scope:
  - docs/article-localization/installations/.lock
---

# Coordinate refund localization installation journal

## Why

The official local installer uses a shared lock and a durable journal. The
first-wave coordinator is already complete. Claim the lock for the separate
reviewed Japan refund source correction and four missing-language documents.

## Definition of done

- [x] Run the unchanged official installer only against pinned, independently reviewed inputs.
- [x] Preserve original bytes and the installer journal; a replay must be byte-identical.
- [x] Verify source correction, four target documents, metadata and original photographs after installation.
- [x] Release the shared lock scope after completing the local installation.

## Steps

- [x] Audit active content claims and PR paths; claim the shared lock separately.
- [x] Bind exact bundle-manifest journal/staging paths to the content task before installer writes.
- [x] Run guarded installation and replay, preserve receipts and verify admitted external jobs.

## How to verify

Use the official `install_bundle.py`, `publish_bundle.verify_bundle`, pipeline
artifact verification and admitted-installation drift guards. Compare installed
pack/assets to the reviewed bundle, and compare journal/receipt bytes before and
after replay. Keep raw inputs and journals ignored; commit only public evidence.

## Notes

The owned content task is `2026-10-07-correct-japan-tax-free-shop-logo` on
`codex/refund-source-correction-v2-20261007`. Exact source SVG admission is
complete; four materialized targets await final independent text/image review.
This ticket authorizes local installation only. It does not authorize deployment,
database import or publication, and it does not reopen the first 13-article PR.

The root executor verified the ignored private staging rules before copying any
inputs, then ran the pinned official-install wrapper. First install/replay both
completed with exit 0; all journal, receipt, pack and asset hashes matched.
Manifest `05e3b08b830ab2e5aa89c117f8d87f41891a3174991e17631eaeefdc118f1585`;
journal `788ed729ef5062136fda1eeaac03327e5383156eff9ab32e60b06112de1a6519`.
Raw inputs, source byte backups, journals and receipts remain ignored. Shared
scope is released by the final done-task commit in the content PR. No production
operation was performed.
