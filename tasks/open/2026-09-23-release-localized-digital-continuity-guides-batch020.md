---
id: 2026-09-23-release-localized-digital-continuity-guides-batch020
title: Release localized digital continuity guides batch020
status: in-progress
priority: P1
area: ops
owner: codex-batch020-release
claimed_at: 2026-09-23T10:37:19Z
created_at: 2026-09-23T10:25:20Z
completed_at:
branch: codex/article-localization-020-release-record
depends_on:
  - 2026-09-23-localize-four-digital-continuity-guides-batch020
scope:
  - docs/article-localization/releases/batch020
---

# Release localized digital continuity guides batch020

## Why

Four published digital-continuity guides have sixteen independently reviewed
missing-language documents and sixteen localized SVG diagrams ready in Git.
Repository content does not publish those languages. Track PR/CI, merge, exact
canonical release artifacts, guarded deployment/import/publication and actual
public-page acceptance separately from completed content authoring.

## Definition of done

- [ ] Synchronize the approved current main, verify the final content/source
      hashes, submit the scoped PR and obtain exact-head required CI and review.
- [ ] Merge the reviewed PR and bind the actual merge tree; obtain applicable
      PostgreSQL release-safety evidence for the exact exported dependencies.
- [ ] Refresh all four live full source rows, versions and visibility. Permit only
      still-missing targets; preserve later edits, withdrawals, hiding or expiry.
- [ ] Assemble and independently review the exact canonical jobs/bundle with
      source, tool, Git, document, SVG, render and route-derivative hashes; freeze.
- [ ] Verify the owned hold/four-lock protocol and a fresh database backup before
      deploying necessary files through hostinger2; check revision and health.
- [ ] Dry-run then execute exactly sixteen draft imports and sixteen article
      publications, with zero hubs, explicit lists, sealed journals and rerun
      idempotency. Preserve all original zh-TW rows and article metadata.
- [ ] Verify twenty public article-language pages: full body, sources, images,
      canonical, reciprocal hreflang and same-language links; check all five
      languages on desktop/mobile and complete paginated sitemap/XML coverage.
- [ ] Verify affected-scope draft/state protection without unsupported claims
      about unrelated database rows. Record per-article content/import/publication/
      browser results and clear only the owned hold after actual final acceptance.

## Steps

- [ ] Review final Git export and submit the prepared PR; record its actual URL.
- [ ] Bind required CI, review, merge tree and applicable PostgreSQL evidence.
- [ ] Refresh source/host state; independently review and freeze release inputs.
- [ ] Perform backup, durable deployment, dry-run, drafts and explicit publication.
- [ ] Complete actual DB/journal and public desktop/mobile acceptance.
- [ ] Record the release evidence and approved owned-hold clearance.

## How to verify

Use the existing ArticlePack/GuideDocument pipeline, canonical assembler and
publisher contracts. Bind actual source rows, versions, deployed content and image
bytes, actor identities, sealed operation journals and screenshot hashes. Preserve
every failed/partial attempt separately. Stop and recheck a conflicting item
rather than overwriting concurrent edits. Local test skips do not prove
PostgreSQL or production behavior. Content completion, import, publication and
browser acceptance must remain separate fields in final release evidence.

## Notes

Exact scope (target locales for every row: en, ja, ko, zh-CN):

| Article slug | Source blocks | Operations |
| --- | --- | --- |
| backup-and-restore-home-files | 15 | 4 drafts + 4 publications |
| phone-document-scanning-workflow | 15 | 4 drafts + 4 publications |
| reading-notes-that-you-reuse | 16 | 4 drafts + 4 publications |
| shared-household-calendar | 15 | 4 drafts + 4 publications |

No series hub operation is required. Preserve all four complete zh-TW source
models, metadata and eight original assets (four textless hero JPGs and four
original SVGs). New diagrams are `diagram-1-{en,ja,ko,zh-cn}.svg` under each slug.

The 2026-09-23T09:23 read-only source snapshot found each article active/published
at article v1 and zh-TW locale/published v6, equal full draft/published models,
no target locales and no expiry. These are historical baseline facts that must
be refreshed before release, not an assertion about current production state.
Snapshot `C:/Users/x8120/.codex/article-localization-release/batch020-candidate-inventory/live-source-full-20260923T092314Z.json`,
SHA256 `ad9b670268b46e5e79f808ce694a2fcf77548571bf50eb582f3d977f861c2d7f`.

The dependent content task records both independent body/image approvals and
the independently reviewed integration candidate. Outside evidence is under
`C:/Users/x8120/.codex/article-localization-release/batch020-digital-continuity/`:

- `integration-candidate-v1/integration-manifest.json`, SHA256
  `a80cb36e65a38322e26e640441171263ecebc42641d8c6de78f83414757f9936`.
- `independent-integration-review-v1/receipt-pass.json`, SHA256
  `601912e1505c835d314a0371d62781803b135102ee1c1137e6b24523d5e297f3`.
- `integration-applied.json`, SHA256
  `a8c09d23e4f31924e4db632a561b319463f91dd7b88d7d2b8279227c324b6080`.
- `test-evidence/attempt-v2/summary-pass.json`, SHA256
  `dfbc3fb5e04a0a1a4b8977f77770550ef346db2a91bfb0b8d0f2b94c967657db`.

For four reading-notes targets, only `/blocks/15/url` is derived from the author's
zh-TW `/guides` index URL to the corresponding target-language index. The exact
root-route allowlist fix, five actual route observations and independent route
review are bound in the manifest. Do not broaden that approval to arbitrary
article URLs. Canonical assembly must regenerate/bind the route derivative with
the final Git tool bytes rather than publishing the unchanged author intermediates.

Local checks passed: API64 with5 PostgreSQL skips; frontend9files/333tests after
an explicitly retained initial worker-startup failure and reduced-worker rerun;
tools81 with1 Windows/Bash skip; route32, Ruff, pack lint, lint, i18n, build,
typecheck, task and diff checks. Preserve32 no_summary/text_length advisories and
honest skip accounting. All1,040 strict fields passed with no numeric exceptions.

No batch020 PR, required CI/merge, canonical freeze, deployment, import/publication
or public browser acceptance is completed or claimed here. This task remains
open and unclaimed until a dedicated release worktree claims it.
