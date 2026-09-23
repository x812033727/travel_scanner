---
id: 2026-09-23-release-localized-digital-continuity-guides-batch020
title: Release localized digital continuity guides batch020
status: done
priority: P1
area: ops
owner: codex-batch020-release
claimed_at: 2026-09-23T10:37:19Z
created_at: 2026-09-23T10:25:20Z
completed_at: 2026-09-23T11:55:19Z
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

- [x] Synchronize the approved current main, verify the final content/source
      hashes, submit the scoped PR and obtain exact-head required CI and review.
- [x] Merge the reviewed PR and bind the actual merge tree; obtain applicable
      PostgreSQL release-safety evidence for the exact exported dependencies.
- [x] Refresh all four live full source rows, versions and visibility. Permit only
      still-missing targets; preserve later edits, withdrawals, hiding or expiry.
- [x] Assemble and independently review the exact canonical jobs/bundle with
      source, tool, Git, document, SVG, render and route-derivative hashes; freeze.
- [x] Verify the owned hold/four-lock protocol and a fresh database backup before
      deploying necessary files through hostinger2; check revision and health.
- [x] Dry-run then execute exactly sixteen draft imports and sixteen article
      publications, with zero hubs, explicit lists, sealed journals and rerun
      idempotency. Preserve all original zh-TW rows and article metadata.
- [x] Verify twenty public article-language pages: full body, sources, images,
      canonical, reciprocal hreflang and same-language links; check all five
      languages on desktop/mobile and complete paginated sitemap/XML coverage.
- [x] Verify affected-scope draft/state protection without unsupported claims
      about unrelated database rows. Record per-article content/import/publication/
      browser results and clear only the owned hold after actual final acceptance.

## Steps

- [x] Review final Git export and submit the prepared PR; record its actual URL.
- [x] Bind required CI, review, merge tree and applicable PostgreSQL evidence.
- [x] Refresh source/host state; independently review and freeze release inputs.
- [x] Perform backup, durable deployment, dry-run, drafts and explicit publication.
- [x] Complete actual DB/journal and public desktop/mobile acceptance.
- [x] Record the release evidence and approved owned-hold clearance.

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

The preceding baseline and local-test notes describe the pre-release state.
The actual release completion below supersedes that earlier pending state.


## Actual release completion — 2026-09-23

- Content PR [#684](https://github.com/x812033727/travel_scanner/pull/684) merged
  at 11:08:18 UTC. All nine checks, including PostgreSQL release-safety, passed
  for exact head `f46361790ef938a60c234d28f95813fa16d46539` before merge.
  The full content-head tree equals merge/deployment
  `fd185a9964274e25856cdaad7c8ac7277aa4738a`.
- Refreshed source at 11:12 UTC retained the same four active published article
  v1 / zh-TW v6 rows with no target locales. The canonical wrapper and final
  transport received independent approval; the owned hold/four-lock procedure,
  fresh custom-format backup with restore-list verification and durable
  deployment completed through hostinger2.
- Exactly sixteen missing-language drafts and sixteen article publications
  completed, with zero hubs. The final sealed journal has 32 committed operations
  and no pending operation. Four original complete zh-TW rows, article metadata
  and eight original assets are unchanged; all sixteen new locales are published
  at v2. No repository-only article or unrelated source was published.
- Independent actual database/journal acceptance passed 219 checks. Public
  acceptance passed all twenty language URLs and forty desktop/mobile cases;
  both independent reviewers actually viewed all eighty original PNGs. All
  twenty expanded-description/source cases and all twenty-four public asset-byte
  checks passed. API sitemap pages 1000 + 960 contain 1960 unique rows, all
  represented by XML article URLs.
- Final acceptance was staged before the owned hold was cleared at 11:48 UTC.
  The 11:48:41 UTC post-clear snapshot has no hold, a clean exact fd185 deployment
  and all three health endpoints returning HTTP 200. No production operations
  were performed while preparing this repository record.
- Per-article content, draft import, publication and browser completion are
  recorded separately in
  [`docs/article-localization/releases/batch020/README.md`](../../docs/article-localization/releases/batch020/README.md)
  and its evidence JSON. This accepts only the four scoped articles. Browser
  viewport captures are not physical-device verification, mobile diagram PNGs
  show the center pan, and site-wide draft visibility is not asserted. The
  existing shared desktop search icon/placeholder overlap remains in its own
  task `2026-09-22-fix-desktop-global-search-placeholder-icon`.

Immutable outside evidence, under
`C:/Users/x8120/.codex/article-localization-release/`:

| Evidence | SHA-256 |
| --- | --- |
| `batch020-digital-continuity/pr684-nine-green-exact-f4636179.json` | `52bd971a2d8c0e26fd1a5180eef63d262e25faacac4f3ca5f6b9ea43b784c464` |
| `batch020-digital-continuity/pr684-merge.json` | `10bc486b0c5b1e2abfb20ee1dfe394a4b3654fc480c385b84bb2204848d1f3cb` |
| `batch020-digital-continuity/live-source-full-20260923T111246Z.json` | `1b8ea3c37d57dc7f1a11caf2f581db5815db8fc3f075b22f68ecfb3865989ace` |
| `batch020-digital-continuity/independent-wrapper-review-f4636179/receipt-pass.json` | `8495491dbaf602980195ab2dd38f428658ed19340de6e859c28d0541cf482110` |
| `mokaair-localization-020-fd185a996427/independent-final-transport-review.json` | `3a6bdb7a392b1c9bc6227e438582b91a4412f8f2ea9c48022ced3f36bc292d74` |
| `mokaair-localization-020-fd185a996427/database-acceptance.json` | `1fac24958912307b11ab33da11b0fb193d3733313e50c71006116adc04d26145` |
| `mokaair-localization-020-fd185a996427/independent-database-journal-review.json` | `5f5c0607cf3d0fd296132f84d9fadc1b036018d4eb7138923de80c83787dd6c5` |
| `mokaair-localization-020-fd185a996427/public-qa-v1/results.json` | `533c014383c0aa626e59ca52064340b7aab29e3166d1ee1528e1b01c26ab3046` |
| `mokaair-localization-020-fd185a996427/public-details-v1/expanded-description-and-sources.json` | `eb88d1f0f1fcb354a9dfc41ddeb6d01bbc56ff9ff107efb3cb60915a5f076faa` |
| `mokaair-localization-020-fd185a996427/public-assets.json` | `245c942a1ce3c06fd97aa2906ac7ce2d0f91c49df71ca622d102fa617f8cf4d8` |
| `mokaair-localization-020-fd185a996427/public-visual-backup-scan-v1/receipt-pass.json` | `7b22fe60f7ee4022a81db833469cf370e9f2ea2c1f24a12cf5586ca391fa14a1` |
| `mokaair-localization-020-fd185a996427/public-visual-notes-calendar-v1/receipt-pass.json` | `d41f028b5ebd49d1098cead4d39d76007803a25952a0287b7a8cc702a09c5745` |
| `mokaair-localization-020-fd185a996427/final-evidence.json` | `1b72ab2802a158402ff00e9df6bab45e9b808993f75cea38eb1aa19cfa390cbd` |
| `mokaair-localization-020-fd185a996427/final-acceptance.json` | `8b4988c678ea7fdc195878d59fa8b52fc4b78e184c8943ce7428b9d140f9da0d` |
| `mokaair-localization-020-fd185a996427/clear-host-20260923T114823453630Z.receipt.json` | `4fe5f353bc918674cdee4e042d57c9b2a1eb82045c09e3ee2dc2e444b0763c4c` |
| `batch007-017-release-protocol/host-readonly-20260923T114841835343Z.json` | `9bf87a4c2cb4f677de25e9f9454ab517e6db318bcc1da6b693dc8d895ba48e6c` |

The queued, unclaimed cable-correction task originally added on this record
branch at `8a4a4ff8` was byte-verified and archived outside Git before removing
that old duplicate from this branch. Its real claimed and implemented task
remains in the separate `codex/fix-cable-label-glossary-link` worktree, untouched.
It is excluded from this release record's PR scope.
