---
id: 2026-09-27-correct-wordpress-user-roles-unrelated-ai
title: Correct WordPress user roles unrelated AI parameters link before Batch031 release
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-27T13:09:35Z
completed_at:
branch: codex/batch031-user-roles-source-link
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-user-roles.json
---

# Correct WordPress user roles unrelated AI parameters link before Batch031 release

## Why

The published zh-TW `wordpress-user-roles` article links the ordinary word `參數`
in its User Role Editor Pro admin-menu discussion to `ai-term-model-parameters`.
That AI glossary article explains model weights, not WordPress plugin settings.
Batch031 translations deliberately do not repeat the wrong link. The original
published source must be corrected before Batch031 can be released.

## Definition of done

- [x] In zh-TW block 20 (zero-based), inline 1 is plain text `參數` instead of an
      ArticleInline to `ai-term-model-parameters`; neighboring wording and every
      other zh-TW field remain unchanged.
- [ ] The corrected zh-TW revision is published through the guarded existing
      release procedure; then Batch031 source version/hash is recaptured and its
      translation bundle is rebound before new locales publish.

## Steps

- [x] Apply the narrow source-pack correction after Pair B releases its file scope.
- [x] Validate links, pack lint, and source diff.
- [ ] Publish the corrected source in a guarded release after Batch030 closes.
- [ ] Verify the public revision and rebind Batch031 source evidence.

## How to verify

Compare the sole changed inline in the pack and the published zh-TW revision;
run pack lint and guide-link tests. Confirm the public page no longer exposes the
AI glossary link and record the new revision/hash before Batch031 publication.

## Notes

Published zh-TW source is article v2, locale v4, model SHA-256
`c87ffb175ceade26d4ab3e33e175d9fcc5198df4402417ce6225462c1e046c9a`
as captured in the Batch031 inventory
`C:\Users\x8120\.codex\article-localization-release\batch031-inventory\batch031-candidate-inventory.json`.
The wrong link was not covered by the earlier Batch030 #855 correction.
Pair B's local translation commit `e8fa87d9abb0969a5c9861e5b0b551757cd47ba6`
is complete and its worktree is clean. This separate source correction is based
on `origin/main` `63d3997e04795296f7d56e4eda7132294ac5ec67`.
Read-only production recapture at 2026-09-27T23:56:12Z:
`C:\Users\x8120\.codex\article-localization-release\batch031-inventory\identity-source-20260927T235607Z.json`,
SHA-256 `6831ad3f1724c4a6a05dbaaed6523a2c3720d0692d5f7ae72ac6e2194182196e`.
The corrected pack SHA-256 is
`b05de046a6eab14423fe4c4ed0a090145d473cb02e847267d6e695a580d2ff88`;
its normalized zh-TW document SHA-256 is
`657f82a170b298b59e3f9e86bc9693d0aa6eb8b5fb204864fd17d19642afc23c`.
Structural comparison found only the `type` change and removal of `kind` and
`slug` at `locales/zh-TW/blocks/20/inlines/1`. Pack lint: one entry, no errors,
one pre-existing no-summary warning. Targeted guide pack/link/ingest tests:
73 passed, 11 skipped. `npm run check:tasks` and `git diff --check` passed.
No production revision, import, or public verification has occurred for this fix.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-batch031-source-link (since 2026-09-27T23:57:26Z) was stale and is released so it stops locking its scope. Landed: #875. Still open: Publish corrected zh-TW revision via guarded release (after Batch030 closes); Verify public revision, recapture Batch031 source version/hash and rebind translation bundle.
