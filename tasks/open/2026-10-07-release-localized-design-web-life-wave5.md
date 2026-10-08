---
id: 2026-10-07-release-localized-design-web-life-wave5
title: Release localized design workflow life articles wave5
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-07T23:53:23Z
completed_at:
branch:
depends_on:
  - 2026-10-07-localize-twelve-design-workflow-and-performance
scope:
  - docs/article-localization/releases/wave5-design-web-life-20261008
---

# Release localized design workflow life articles wave5

## Why

Twelve published life articles have 48 reviewed locale documents and four approved
source corrections prepared locally. Repository installation is complete; merge,
deployment, publication and five-language public acceptance remain unfinished.
The owner approved only the earlier 32-article release. This new cohort needs its
own concrete release choice or an explicit standing permission covering it.

## Definition of done

- [ ] The approved content commit is merged with CI green at the exact current head.
- [ ] Live code contains that commit; normal deployment and hold checks are verified.
- [ ] Fresh production source/version guards, rehearsal and dry-run match this cohort.
- [ ] Owner release choice and a readable, verified database backup precede writes.
- [ ] All 48 new locales and four approved source updates complete durable phases.
- [ ] Replay is unchanged and all 60 five-language pages pass desktop/mobile acceptance.
- [ ] Sanitized release evidence and final source/version hashes are committed.

## Steps

- [ ] Check the exact content PR head, current CI and approved merge scope.
- [ ] Check live HEAD, holds, release locks and publish_holds; use normal deployment.
- [ ] Capture a fresh snapshot and rebind the reviewed bundle without changing content.
- [ ] Rehearse with the deployed API image; dry-run and compare all expected operations.
- [ ] Obtain the cohort choice, create pg_dump and verify its restore table of contents.
- [ ] Run durable drafts, article publication and hub phases; preserve failures/holds.
- [ ] Rebuild links, inspect selected locale findings and verify unchanged replay.
- [ ] Verify document/media hashes, links, hreflang, sitemaps and desktop/mobile pages.
- [ ] Record results, clear only this release's owned hold and finish this task in its PR.

## How to verify

Follow article-localization, content-pipeline and deploy skills, and
`ops/release/README.md`. Use only these twelve slugs and en, ja, ko, zh-CN plus
the four explicitly approved source corrections. Record actual CLI exit codes,
durable phase outcomes and fresh five-language public responses; healthy services
or green CI alone do not establish publication. Do not use force/ignore-hold or
retry an uncertain provider/write request.

## Notes

Prepared manifest:
`58fe016c0fe00a1b3256fdf67a0718d2d6451ee9b90cc5feba1324d3eec28c01`.
All 48 genuine review pins:
`2c3d09dac1c51faa18698b400c3e35700129ddb467035c414db583701244a9a5`.
Actual local install/replay receipt:
`feb551e70b55ef01c407dfb24f5a5c040b2e5d8ac345f81fc34f32963674db16`.
Both official installer executions exited 0 with 164 operations and identical
full pack/asset/journal/backups/article-receipt captures. This does not publish.

The sanitized preparation record and exact cohort are in
`docs/article-localization/releases/wave5-design-web-life-20261008/README.md`.
Private baselines, DB guards, genuine reviews and full native inspection evidence
remain in the owner's persistent storage outside Git. Preserve original attempts,
the authoring CLI exit 1, the assembly wrapper topic-order failure and the
read-only finalization receipt. Eight unchanged sources retain their canonical
hashes; four source changes are exactly five approved inline objects with the
same visible words. All 36 original media files and original dates are unchanged.

This task stays open and unclaimed until a concrete approved release starts.
The separate frozen PR #1374 and completed first 32 articles are not part of it.
