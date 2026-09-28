---
id: 2026-09-28-install-reviewed-batch040-affiliate-and-store
title: Install reviewed Batch040 affiliate and store locales
status: done
priority: P2
area: docs
owner: codex-batch040-root
claimed_at: 2026-09-28T17:21:30Z
created_at: 2026-09-28T17:18:32Z
completed_at: 2026-09-28T17:27:03Z
branch: codex/article-localization-040-affiliate-a
depends_on: []
scope:
  - apps/api/app/guides/content/affiliate-marketing-basics.json
  - apps/api/app/guides/content/independent-store-marketplace.json
---

# Install reviewed Batch040 affiliate and store locales

## Why

The two published source articles lacked zh-CN, en, ja and ko. Source PR #930
and task closure #948 now allow their frozen reviewed candidates to be installed.

## Definition of done

- [x] Add eight complete language documents while preserving source and metadata.
- [x] Bind independent text/image review to exact documents and assets.
- [x] Run pack/schema/link checks and five-locale desktop/mobile local previews.
- [x] Prepare a focused draft PR with inherited editorial and release gaps explicit.

## Steps

- [x] Verify immutable candidate hashes and parity with current main.
- [x] Install only four missing locales per article; validate 10 documents.
- [x] Complete independent read and capture final hash-bound evidence.
- [x] Create unclaimed release and inherited-editorial follow-up tasks.

## How to verify

See `docs/article-localization/batch040-pair-a-evidence.md`: two-pack lint has no
errors; content/link tests have 15 passed and 11 DB skips; 20 standalone previews
pass. CI and actual public pages remain separate acceptance gates.

## Notes

Root took over after the drafting agents stopped at their usage limit. No retry
of the quota failure occurred. No translation correction was needed in the final
independent read. Strict intake preserves known source defects in the separate
editorial follow-up; it is not reported as passed. No production write occurred.
