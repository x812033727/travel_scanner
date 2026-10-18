---
id: 2026-10-07-coordinate-wave3-localization-installation-journals
title: Coordinate wave3 localization installation journals
status: done
priority: P1
area: tools
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T10:15:23Z
created_at: 2026-10-07T07:52:46Z
completed_at: 2026-10-07T10:21:22Z
branch: codex/article-locales-wave3-20261007
depends_on: []
scope:
  - docs/article-localization/installations/.lock
  - .codex/localization-staging/taiwan-2027-wave3
  - .codex/localization-staging/hong-kong-wave3
  - docs/article-localization/installations/bundles/d66c992766fa3158
  - docs/article-localization/installations/bundles/c8aed1260b9acb44
---

# Coordinate wave3 localization installation journals

## Why

The official local installer serializes writes with one shared lock and records
an exact durable bundle journal. Coordinate the two separately reviewed travel
articles without colliding with another installer or exposing private inputs.

## Definition of done

- [x] Independently reviewed Taiwan and Hong Kong bundles are installed with the
      unchanged official installer, preserving all original media and metadata.
- [x] A replay preserves every journal, receipt, pack and asset byte.
- [x] Private snapshots, jobs, byte backups and journals stay ignored and out of Git.
- [x] Release the shared lock scope after the final verified local installation.

## Steps

- [x] Verify actual source/job/artifact/review bindings and each content claim.
- [x] Add only actual manifest-specific journal paths before installer writes.
- [x] Verify narrow local ignore rules before copying pinned private inputs.
- [x] Install and replay each independently reviewed bundle; retain exact receipts.

## How to verify

Use `publish_bundle.verify_bundle`, `install_bundle.install`, artifact verification
and admitted-installation guards. Compare all operations and durable receipts
after installation and replay. A successful local install is not production
publication, a production backup, a deployment or a fresh deployed baseline.

## Notes

The two content owners are the Taiwan holiday-planning and Hong Kong source-scope
tickets on this branch. Source proposals, original inputs and failing artifacts
remain preserved outside Git. Claim only the exact bundle journal prefixes once
the final manifests exist; no broad installation-directory claim is authorized.

Taiwan's actual assembled manifest is
`d66c992766fa3158ea6e89c6a952fb1ef98c1190749c09bd8e91db8dee119b85`.
Its exact journal prefix is now included before any installer writes.

Hong Kong's actual assembled manifest is
`c8aed1260b9acb44b8a27b9d5e80ce8caa13de67c9f945c5bce57316116a2f1a`.
Its exact journal prefix is included after genuine four-target review and official
assembly, before private staging and installer writes.

Both actual unchanged official installations and exact replays completed.
Their journals bind every operation, backup and per-slug admission; private
staging is ignored. The persistent lock file remains as designed, while its
actual nonblocking byte lock was acquired/released and its bytes stayed exact.
Technical full-map verification also passes for Hong Kong, evidence SHA
`6951b24e3f90df06963596d91c91bd2900998e62a3a9e555e60116759b7dde23`.
The archived task releases ownership of the shared scope. An earlier checklist
update incorrectly tested lock-file absence and stopped before any checklist
write; these verified records correct the premature archival without deleting
the persistent lock or changing any real installer receipt.
