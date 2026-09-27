---
id: 2026-09-27-release-localized-wordpress-content-guides-batch027
title: Release localized WordPress content guides batch027
status: in-progress
priority: P2
area: ops
owner: codex-batch027-release
claimed_at: 2026-09-27T08:45:30Z
created_at: 2026-09-27T07:22:21Z
completed_at:
branch: codex/article-localization-027-release
depends_on:
  - 2026-09-23-localize-four-wordpress-content-guides-batch027
scope:
  - docs/article-localization/releases/batch027
---

# Release localized WordPress content guides batch027

## Why

PR #849 added complete four-language translations and localized diagrams/covers for four existing published WordPress content guides. Merging the packs does not publish the 16 missing production language rows. This task controls the exact deployment, draft import, article publication, independent public acceptance, hold clearance, and durable release record without changing the four published zh-TW originals.

## Definition of done

- [ ] Exact merged content tree, all nine exact-head CI checks, current full published source versions/hashes, owner eligibility, host/migration/runtime state, and final transport are frozen and independently reviewed.
- [ ] A fresh verified protected database backup, release-owned hold and locks, deployment (if required), healthy target runtime, and dry-run scope of exactly 16 drafts + 16 article publications + 0 hubs are recorded.
- [ ] All 16 missing locales are published once; four complete zh-TW originals, article category/order/visibility, and audit/revision history are preserved. Re-run creates no duplicate edits.
- [ ] Five-language public API and HTML pages, all localized and original asset bytes, canonical/reciprocal hreflang, conditional internal links, sitemap pages/XML and desktop/mobile visuals pass independent checks; no draft is accidentally public.
- [ ] Release hold is cleared only after a hash-bound final acceptance review; per-article results, evidence paths, and any remaining limitations are committed in `docs/article-localization/releases/batch027/`.

## Steps

- [x] Merge Batch027 content PR #849 and close its content task.
- [ ] Recheck exact merged tree/CI and fresh source + actor; freeze reviewed offline wrapper/transport.
- [ ] Review host/deployment/migrations/runtime, back up and dry run under a release-owned hold/locks.
- [ ] Deploy required code/assets and apply journaled drafts/publications only on unchanged target/version gates.
- [ ] Independently verify database, public API/HTML/assets/sitemap/visuals, clear hold, and commit release record PR.

## How to verify

Use the guarded Batch027 offline gate and canonical `tools/article-localization/pipeline.py`, `docs/article-localization/assemble_bundle.py`, and `publish_bundle.py`. Verify `pg_dump -Fc` with `pg_restore --list`; inspect exact deployment revision, health, all 13 runtime services, dry-run operation plan and publisher journal. Re-run the publisher idempotently, inspect all 20 full article pages, 60 assets, 32 conditional links, reciprocal hreflang, API/XML sitemap, and 40 desktop/mobile cases. Run `npm run check:tasks` and release-record PR CI.

## Notes

Content PR #849 merged 2026-09-27T08:43:02Z from reviewed head `b22a98b629696c0f2116fdf068439bc87f521192` to squash commit `790868bffcda4631280fec5f24f702bbb1a4a302`; all nine exact-head CI checks passed. Four slugs: `wordpress-posts-pages`, `wordpress-taxonomy-navigation`, `wordpress-themes-plugins-install`, `wordpress-widgets-sidebar`. Independent 52-path integration receipt SHA-256 `48e90587b00d190d81da4a0fbd21d4b0422fbad05b5137a8acc73f8b2d42d4f0`; 16 SVG Git LF conversions were independently checked as line-ending-only (root receipt SHA-256 `b61631a304ad28707c6bb47ddf55bd450be6b221eec47b6aba3b1280f71a8b59`). Offline preparation and scripts are under `C:\Users\x8120\.codex\article-localization-release\batch027-wordpress-content\release-prep-agent\`. The earlier 06:59 production snapshot is historical: obtain fresh read-only rows/actor evidence before freeze. Nothing in this task has yet been deployed, imported or published.
