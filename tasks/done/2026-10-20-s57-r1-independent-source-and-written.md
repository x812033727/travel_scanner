---
id: 2026-10-20-s57-r1-independent-source-and-written
title: S57 R1 independent source and written visual audit
status: done
priority: P1
area: docs
owner: codex-s57-source
claimed_at: 2026-10-20T22:47:05Z
created_at: 2026-10-20T22:47:02Z
completed_at: 2026-10-20T22:52:06Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s57/review/r1-source-independent.md
---

# S57 R1 independent source and written visual audit

## Why

S57 has a new 189-line Stanley/Livingstone author candidate. It needs a reviewer who did not write the script to check its two fixed printed sources and every written scene before policy or paid narration.

## Definition of done

- [x] A five-hash independent 189/189 source and written-visual verdict is recorded with exact blocking IDs and source links.

## Steps

- [x] Reopen both fixed full texts, confirm SHA and citation reachability, and check 189 claims, scenes, cards, metadata, and script alignment.
- [x] Record narrow HOLDs without editing the frozen creative files or buying media.

## How to verify

`sha256sum docs/videos/curio-s57/{research.md,brief.md,claims.md,video.json,script.md}`; fixed-source `curl` downloads and SHA; `node tools/video/cli.mjs lint --slug curio-s57 --json`; `npm run check:tasks`.

## Notes

Report: `docs/videos/curio-s57/review/r1-source-independent.md`. HOLD: three spoken source-tier/precision lines (`s57050`, `s57077`, `s57116`) and written visual locations/timing (`s57028`, `s57030–s57032`, `s57100–s57112` except the card `s57103`, `s57188–s57189`). The other lines/cards were checked against the fixed books. Parent was informed early; creative freeze stayed untouched.
