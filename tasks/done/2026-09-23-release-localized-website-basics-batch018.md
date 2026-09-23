---
id: 2026-09-23-release-localized-website-basics-batch018
title: Release localized website basics batch018
status: done
priority: P1
area: ops
owner: codex-batch018
claimed_at: 2026-09-23T07:56:10Z
created_at: 2026-09-23T07:02:24Z
completed_at: 2026-09-23T09:37:25Z
branch: codex/article-localization-018-release-record
depends_on:
  - 2026-09-22-localize-four-website-basics-guides-batch018
scope:
  - docs/article-localization/releases/batch018
---

# Release localized website basics batch018

## Why

The four website-basics packs have sixteen reviewed translations and forty-eight
localized images. A merged content PR alone does not publish those languages.
Keep the remaining CI, deployment, import and public acceptance gates explicit.

## Definition of done

- [x] Exact content PR head passes required CI and is reviewed and merged.
- [x] Fresh live source/visibility/version inventory still permits missing-language
      publication for exactly the four slugs below; retain any concurrent edits.
- [x] Freeze reviewed canonical bundle, original/version hashes and image evidence.
- [x] Verify fresh database backup and deployment health under the existing owned
      hold/locking protocol; deploy only the reviewed necessary code and images.
- [x] Dry-run and idempotent import/publish change only en, ja, ko and zh-CN.
- [x] All twenty five-language pages pass full-body/image/canonical/hreflang/link
      checks and desktop/mobile visual review; publisher scope excludes unrelated drafts.
- [x] Record per-article content/import/publication/browser evidence and release
      only this task's owned hold after acceptance.

## Steps

- [x] Review final Git export and CI for the content PR.
- [x] Refresh source snapshot and assemble/review the exact release bundle.
- [x] Deploy, import and publish through the reviewed explicit-list publisher.
- [x] Complete database and public-browser acceptance and delivery receipt.

## How to verify

Use `docs/article-localization/publish_bundle.py` and the existing guarded release
workflow, with explicit slugs and target locales. Bind the full normalized
documents, deployed image bytes, original rows, final journals and screenshots.
Follow `.agents/skills/deploy/SKILL.md` and the content-pipeline publish runbook.

## Notes

Exact scope: `domain-registration-guide`, `hosting-types-explained`,
`website-cms-choice`, `website-maintenance-routine`. Source inventory on
2026-09-22 showed active published article v2 / zh-TW locale v4 with no draft
divergence. Recheck those facts before release; this task does not assert they
remain current.

Reviewed work and receipt pins are in the dependent content task and the persistent
outside-Git directory `C:/Users/x8120/.codex/article-localization-release/batch018-web-basics/`.
All sixteen documents and forty-eight images passed independent review. Five
Japanese number-format equivalences were explicitly reviewed; the strict field
guard is not a zero-warning result. Existing source documents, metadata and twelve
source images are preserved. No production work for this batch has been claimed
as complete by this task.

### 2026-09-23 release preparation

PR #676 passed all eight checks at c9f9ea3c, but strict branch protection required
synchronizing the newly merged CatchTable data PR #677. The current content head
is e17895e3c12ce19fe421536dd2ba543afbdc233c, based on
017caac57c5ced78e95a58acb03981cab9874f92. Its CI is running. The exact fourteen-file
main delta changes only CatchTable data, documentation, skills and its task;
all fifty-two content/asset files and twelve original images remain unchanged.
The earlier reviewed c9f package remains preserved as historical evidence.

The 2026-09-23T07:55:13Z read-only snapshot still shows four active articles at
article v2 / zh-TW locale v4, equal draft/latest/published source documents, and
no target locales. Independent local reviews cover the scoped driver, public
capture readiness, and database acceptance validator. Actual PostgreSQL release
safety CI ran 119 transactional SQLite/PostgreSQL tests successfully; its code
dependencies are separately bound to the current content head. No production
backup, deployment, import or publication for Batch018 has run yet.

### 2026-09-23 guarded deployment and main advancement

PR #676 passed all eight checks at e17895e3 and merged as
5a1682a1c62280b99cf7e21f4f583c9cad78a470. The reviewed 478-file inner bundle
and 486-file transport were frozen, independently reviewed and provisioned.
The 08:34 UTC database backup passed `pg_restore --list` and remains preserved.
The durable deployment worker then refused before calling the host deploy script:
`Remote main does not equal reviewed target`. Its failed unit, logs, config,
backup and owned hold are retained; no deployment or publisher operation ran.

PR #679 had meanwhile merged as 38ebec88c91db6ae0f6c8cd812bf04c5e1da9c95.
Its eight checks passed and tested/merged trees are identical. The four-path
delta is two CatchTable JSON files plus documentation and a task; all 79 exact
reviewed Git exports remain unchanged. A fresh 08:40 UTC read-only source export
is identical to the pre-release rows, including article metadata and zh-TW.
Recovery is being reviewed for a fresh target-specific root, preserving the
inner bundle and old evidence, transferring only this task's exact owned hold
under all four locks, and taking a fresh backup before deployment. Recovery,
import/publication and public acceptance are not yet complete.

Outside evidence: `batch018-web-basics/recovery-38ebec88/` contains the current
target/CI review, read-only failed-host capture and root recovery authorization.
The original release directory remains `mokaair-localization-018-5a1682a1c622`.

At 09:01 UTC the independently reviewed recovery transport was provisioned at
`mokaair-localization-018-38ebec88c91d`; the exact owned hold was atomically
transferred under all four locks without removing the hold or changing old
evidence. A separate fresh backup passed at 09:03 UTC. Its metadata and the
three transfer records were captured read-only and prove the new backup follows
the completed transfer. The durable deployment started at 09:03:32 UTC and is
still running at this note. No content import/publication is claimed yet.

Recovery review SHA256:
`dde725bbcba973245d32c576b88316e5529119b1dc119b24e2f8c9ddfd9e9949`.
Recovery transport SHA256:
`fe46b12ec13da57f3f13bd0b745ce17414575486f88b207dca4b440e4d88c985`.
Read-only transfer/new-backup capture SHA256:
`08fbed90c47ad6261e7f46cf390356c8aaa7931c832cc24addf2ed71bd7961f4`.

### 2026-09-23 completed production acceptance

The guarded recovery deployment completed successfully at 09:06 UTC. Read-only
dry-run, sixteen draft imports and sixteen article publications completed in
sequence; the hub phase performed zero operations. Newly published locales are
v2; four original zh-TW v4 full rows and all parent metadata remain unchanged.
Independent review verified twenty complete models, all thirty-two committed
journal operations, the actor, phase seals, transferred hold and fresh backup.

All twenty URLs passed full-body/image/canonical/hreflang/internal-link checks in
forty desktop/mobile viewport cases. Twenty expanded-content/source cases and
all sixty public image SHA256 checks passed. Two independent reviewers actually
viewed eighty original screenshots. Mobile diagram screenshots cover the center
pan; complete labels are covered by desktop diagrams and frozen render evidence.
The existing desktop search placeholder/icon overlap remains separately tracked.
Sitemap pagination returned 1,000 + 928 unique rows, all covered by the XML sitemap.

Final evidence was reviewed and staged before clearing this task's exact owned
hold at 09:34 UTC. The 09:34:28 read-only host check showed clean deployed target
38ebec88, no hold and all three health endpoints at 200. The old failed release
directory and backup remain preserved. This receipt claims only these four
already-public articles; it does not claim a new site-wide draft-visibility audit.

Per-article results, timestamps and external SHA256 references are committed in
docs/article-localization/releases/batch018/README.md and evidence.json.
Final-evidence SHA256:
`90f407364456a582b118c7c5b6f4697933bd0d840f5bccbbafd9dc824ba3f40a`.
Final-acceptance SHA256:
`0e340684df166e324e16aead8934100ba5531ff39aacb09c94b31977c8daaa2f`.
Post-clear host SHA256:
`cd7d6bb1e8e4d00df0fe9cb9ec91d98207d11b470bafcf9f7083dc679238d7b3`.
