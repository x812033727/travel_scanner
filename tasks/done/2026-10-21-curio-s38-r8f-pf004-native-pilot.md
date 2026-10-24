---
id: 2026-10-21-curio-s38-r8f-pf004-native-pilot
title: Run and audit the bounded S38 R8f pf004 native image pilot
status: done
priority: P2
area: docs
owner: codex-s38-r8f-native-pilot
claimed_at: 2026-10-21T00:18:00Z
created_at: 2026-10-21T00:18:00Z
completed_at: 2026-10-21T00:20:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/verify-16-r8f-native-stop.md
---

# Run and audit the bounded S38 R8f pf004 native image pilot

## Why

The R8f paper prompt passed independent review but its actual MiniMax image had not been checked. Only one named shot and one take were allowed before a new quality decision.

## Definition of done

- [x] Verify the frozen R8f SHA, dry run, STOP, ledger, and existing full-episode cap.
- [x] Draw only `pf004` with one take, inspect its native JPEG and machine judge, and restore STOP.
- [x] Record exact media hashes, cost, rejection, and the bounded next step in [the pilot receipt](../../docs/videos/curio-s38/verify-16-r8f-native-stop.md).

## How to verify

Check `sha256sum docs/videos/curio-s38/video.json`, the private JPEG and log hashes, `media-status --slug curio-s38 --json`, and the private STOP. The judge failed; no other new image was bought.
