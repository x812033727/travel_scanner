---
id: 2026-10-08-retain-existing-guide-packs-in-imported
title: Retain existing guide packs in imported language runtime snapshots
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-08T07:53:24Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/imported-long-languages/package-runtime.mjs
  - docs/videos/imported-long-languages/prepare.test.mjs
---

# Retain existing guide packs in imported language runtime snapshots

## Why

The frozen imported-language sibling finished twelve journalled translation/
review answers and then stopped because its normal local loader needed the
already-published free-versus-paid guide content pack. The actual repository
contained the pack, but the runtime snapshot omitted it. Copying only that exact
existing source-bound pack fixed local verification with zero model requests.
Runtime construction should retain needed existing packs so this dependency
cannot strand completed paid work again.

## Definition of done

- [ ] Every snapshot includes each selected video's referenced existing guide
      pack and binds its original bytes in its manifest.
- [ ] Missing or changed dependencies fail preflight before any model dispatch.
- [ ] Unrelated packs, credentials and new content are not silently imported.

## Steps

- [ ] Inspect the current package-runtime loader contract and active PR1359.
- [ ] Add a source-bound pack fixture matching a real referenced guide.
- [ ] Verify snapshot loading without provider calls or changed source hashes.

## How to verify

Run prepare/runtime packaging tests. Load a packaged selected video with its
original referenced pack; reject missing/stale manifest hashes before dispatch.

## Notes

Original pack apps/api/app/guides/content/ai-free-vs-paid-plans-2026.json SHA-256
2952f35f52a8ef0800eacd492a3ba17bfaea6da4afda3d09f1406255ff3155a6.
Private continuation copied those exact bytes into the existing sibling and
preserved its namespace and completed records. No publication/import was needed.
