---
id: 2026-11-18-drive-db-encryption-retention
title: Encrypt and thin the nightly database copies on Drive, export content weekly
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-11-18T02:27:52Z
completed_at:
branch:
depends_on: []
scope:
  - ops/backup/offsite.py
  - ops/backup/README.md
---

# Encrypt and thin the nightly database copies on Drive, export content weekly

## Why

The nightly database dumps (`主機/資料庫/nightly/`) are unencrypted on the same Drive as creative files, keep only 14, and share the full-Drive token used everywhere. Articles, content packs and the merchant/hotspot catalogue have no copy on Drive apart from those dumps.

## Definition of done

- [ ] Dumps encrypted with the host's age key; 14 daily, 8 weekly, 12 monthly kept.
- [ ] A weekly export of content packs and catalogue tables to `AI/備份/內容/`.
- [ ] The host's offsite job uses its own narrower token; an admin warning at 80% Drive usage.

## Steps

- [ ] Encrypt in offsite.py, document restore.
- [ ] Retention tiers.
- [ ] Weekly export.

## How to verify

See the steps; each lands with tests.

## Notes

Phase 4 of the Drive plan. Needs the owner for the new token.
