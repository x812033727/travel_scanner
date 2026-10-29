---
id: 2026-10-21-curio-s38-r8i-pf006-final-native-stop
title: Audit the final bounded S38 pf006 native take and preserve STOP
status: done
priority: P2
area: docs
owner: codex-s38-r8i-final-native-stop
claimed_at: 2026-10-21T00:31:00Z
created_at: 2026-10-21T00:31:00Z
completed_at: 2026-10-21T00:33:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/verify-23-r8i-final-native-stop.md
---

# Audit the final bounded S38 pf006 native take and preserve STOP

## Why

R8i had one paid image trial remaining. Its result had to be checked directly before any more art spending.

## Definition of done

- [x] Verify exact R8i SHA, paper pass, budget, dry run and STOP before the one named-shot call.
- [x] Inspect the native image and judge; reject the 3D result and restore STOP.
- [x] Record exact image/log hashes, US$0.0135 spend, cumulative ledger, and the no-new-purchase fallback in [the receipt](../../docs/videos/curio-s38/verify-23-r8i-final-native-stop.md).

## How to verify

Inspect the private JPEG, manifest and log; run `media-status --slug curio-s38 --json` and confirm the private STOP. No further pf006 image call is allowed under this pilot plan.
