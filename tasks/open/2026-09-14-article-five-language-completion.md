---
id: 2026-09-14-article-five-language-completion
title: Complete all article translations and localized artwork
status: in-progress
priority: P1
area: docs
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T21:10:11Z
created_at: 2026-09-14T13:55:52Z
completed_at:
branch: codex/article-locales-wave5-20261008
depends_on: []
scope:
  - docs/article-localization/handoffs/legacy-completion-20260914.md
---

# Complete all article translations and localized artwork

## Why

The 2026-09-14 starting inventory had 626 first-party article packs and 2,404
missing translations. A fresh 2026-09-20 read-only inventory at repository commit
`8264c01a77f1044c9b8e756addaaa997bbc1c58a` has 1,067 packs and 3,578
missing translations (3,430 on 1,030 public articles; 148 on 37 repository-only
drafts). The user authorized full five-language body/artwork completion and
publication of missing languages on already-public articles. Unpublished articles
must remain drafts. Codex subagents were explicitly authorized; no additional
paid translation provider is authorized.

## Definition of done

- [ ] All 1,067 articles in the refreshed baseline have complete zh-TW, en, ja, ko and zh-CN content and artwork, with later additions re-inventoried before closure.
- [ ] All 1,030 currently public articles have their 3,430 missing languages published.
- [ ] All 37 currently repository-only articles have 148 missing-language private drafts.
- [ ] Sitemap and both tutorial series handle all five languages and real publication state.
- [ ] Version-pinned import, publication, assets and desktop/mobile verification receipts exist.

## Steps

- [x] Read-only live snapshot and repository inventory, source hashes and batches of at most 20.
- [ ] Complete the refreshed 3,578 missing language documents, artwork and editorial checks in batches of at most 20 articles.
- [ ] Validate and review sitemap pagination and localized tutorial-series changes.
- [ ] Review exact per-locale changes, merge green CI, deploy assets/application and verify backup.
- [ ] Import private drafts and publish only baseline-public articles' target locales.
- [ ] Verify all public pages, links, artwork, metadata and protected private state.

## How to verify

`apps/api/.venv/Scripts/python.exe -X utf8 docs/article-localization/build_baseline.py`
reproduces the pinned inventory from the read-only production snapshot. Run translation
pipeline unit tests, ArticlePack and publication regression tests, affected API/web checks,
full CI and publication dry-run before changing production. Verify actual public documents,
not only HTTP status codes. Final per-article receipts belong under docs/article-localization.

## Notes

- Baseline repository commit: `8c83e90ab401f05044f614e5843c00d26aaed3dd`.
- Production read-only transaction: 287 published articles, zero draft/hidden/expired articles;
  267 zh-TW and 30 each en/ja/ko/zh-CN documents. Repository adds 339 unimported articles.
- 596 packs lack four languages; 20 Taiwan packs lack zh-TW; 10 packs already have five languages.
- One current published document differs from the repository: `chatgpt-troubleshooting-common-errors:zh-TW`.
  Its current published document is pinned as source; the original locale must not be overwritten.
- Source/live snapshots and normalized hashes are baseline.json, production-baseline.json and
  source-differences.json. They contain editorial content and version metadata, no credentials.
- PR #485 was verified merged and ancestral to this checkout; its leftover review claim was
  archived. Windows task archival left an open copy; after comparing status/date-only differences,
  the duplicate was removed with apply_patch. Existing task records this tooling issue.
- Team assignments: sitemap_pagination owns its separate claimed task; series_localization owns
  a narrow series task; translation_pipeline owns tools/article-localization and staged work outputs.
  Root owns inventory, publication and verification under docs/article-localization.
- No translations, imports, publication or deployment have completed at this checkpoint.
- Resume audit on 2026-09-20 found `origin/main` 78 commits ahead. It adds or changes
  article packs and both tutorial centres; the original 626/2,404 inventory remains a
  pinned historical baseline, not a claim about the current repository or production.
  Batch 001's 20 source packs and the reviewed Gemini Markdown pilot source are unchanged.
- Staged state before rebasing: five rendered locales, three translated locales, three
  validation failures, one usage-limit stop and 72 prepared jobs. The earlier invalid MCP
  override was fixed and preflighted before translation; no failed attempt was treated as
  content. Production import, publication, deployment and browser verification remain zero.
- Read-only inventory refresh captured at `2026-09-20T09:12:47.562977+00:00` in
  the owner's persistent batch-005 inventory refresh evidence from September 20
  (SHA-256 `c197fd0e0768c5179c1cddb3f907f8149acfc055240a71165de31468072a4dc5`).
  It pins production snapshot SHA-256
  `de9bc67409ff777ef40761379ccf6066b4b1ca81230218123ae1da80741ff7cc` and
  combined baseline SHA-256 `07a3fd80c72f05a149808dac667dce9eace3611f21ab9ae62ab8dd4e64489e1d`.
  The 626/2,404 numbers above are historical, not the current completion target;
  88 repository/database locale differences require per-article reconciliation.

- 2026-10-08 coordination handoff: the official ordinary claim command adopted
  this expired claim as `codex-article-localization-4e16`; no force, release or
  done command was used. The historical goals and every unchecked item remain.
  Scope now contains only the coordinator handoff; specific current content,
  installation and release paths belong to separately claimed cohort tasks.
  Original worktrees, sources, jobs, failed attempts, STOP markers, locks and
  receipts are preserved. Historical inventory counts are not current completion.
