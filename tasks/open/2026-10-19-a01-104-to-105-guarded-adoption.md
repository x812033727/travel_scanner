---
id: 2026-10-19-a01-104-to-105-guarded-adoption
title: A01 104 to 105 guarded adoption transaction and recovery
status: in-progress
priority: P2
area: tools
owner: codex-gpt6-a01-adoption
claimed_at: 2026-10-19T01:20:19Z
created_at: 2026-10-19T01:19:32Z
completed_at:
branch: codex/a01-adoption-helper-20261019
depends_on: []
scope:
  - tools/video/a01-adoption
---

# A01 104 to 105 guarded adoption transaction and recovery

## Why

A01 already has a 104-link production audit chain and a scoped STOP. The r23 manuscript
is an offline proposal, not a production adoption. A 104→105 source revision must
preserve old evidence, account for separate docs/work mounts, and stop safely after
any interruption before the 105 index is published.

## Definition of done

- [x] A separately reviewable transaction helper applies only six A01 chapters,
      series/video and auto, with the 105 audit index last.
- [x] A failed phase remains HOLD and has deterministic exact-byte recovery/readback.
- [x] Synthetic failure injection covers every durable phase; production stays untouched.

## Steps

- [x] Pin fresh capture/worker/public-source evidence and exact owner-granted paths.
- [x] Build dual-mount intent, backup, atomic replace, audit, readback and recovery.
- [ ] Run local tests and independent review; keep production application gated.

## How to verify

`node --test tools/video/a01-adoption/*.test.mjs` and `node --check` for every new
script. Inspect the synthetic filesystem before/after each injected crash.

## Notes

The 2026-10-18 104 capture and r23 25-public-source proposal are historical/offline.
Regenerate a filtered 18-public-source video with the exact deployed worker before
any installation. Do not connect this ticket's implementation to production.

2026-10-19: The fresh `-03` archive has 104 events, 222 immutable audit files,
and the independently pinned source/tip/inventory hashes; source-only
verification passes while unrelated active media keeps the operational gate
HOLD. The capture helper is separately owned and is not integrated here.
The r23 manuscript failed independent claim/visual review. This core rejects
that manifest and keeps **every** production-pinned adoption at
`R24_EDITORIAL_REVIEW_GATE_NOT_CONFIGURED` until an independently reviewed r24
receipt binds the editorial manifest and exact nine target hashes. The offline
fault tests use a test-runner-only pin override. No host writes occurred.
The full local suite passed 21 tests with one environment-dependent integration
test skipped; the same integration test passed separately against the `-03`
capture and sibling capture-helper checkout. Independent final review remains.
