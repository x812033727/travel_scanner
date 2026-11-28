---
id: 2026-11-25-slim-docs-videos-pools-and-plans
title: Slim docs/videos by moving 1.40 GB topic pools and series-plan PNGs to Google Drive after SHA-256 audit
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-11-25T01:16:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
  - docs/videos/history-curiosity/pool
  - docs/videos/series-plans/zhong-tian-qu-qi
  - docs/videos/series-plans/top40-2025-2026
  - docs/videos/rules-sync
  - docs/videos/explainer-series/GITHUB-SLIMDOWN-AUDIT-20261125.md
---

# Slim `docs/videos/` by moving 1.40 GB topic pools and series-plan PNGs to Google Drive

## Why

The 2026-11-25 audit (`docs/videos/explainer-series/GITHUB-SLIMDOWN-AUDIT-20261125.md`) measured
`docs/videos/` at **12,243 files / 1,577.47 MB** inside GitHub. Four static content folders account
for **1,406.82 MB (89.2%)** and are not needed by the running web app, API, or `cli.mjs import`:

1. `docs/videos/so-thats-why/pool/` — 1,750 files, **725.07 MB**
2. `docs/videos/series-plans/zhong-tian-qu-qi/` — 1,838 files, **347.61 MB** (mostly 6 MB PNG set designs; `rules-sync` only reads ~22 small `.md` files)
3. `docs/videos/series-plans/top40-2025-2026/` — 922 files, **170.37 MB** (mostly 2.6 MB PNG set designs; `rules-sync` only reads ~14 small `.md` files in `2025-01-tai-nainai/`)
4. `docs/videos/history-curiosity/pool/` — 424 files, **163.77 MB**

Owner decision (2026-11-25): reduce dependency on GitHub; keep finalized episode scripts, topic
pools, and heavy media assets on Google Drive (`G:\我的雲端硬碟\AI\備份\AI劇\`) as the single
authoritative archive.

## Plan

1. **Phase A (Zero-risk, ~1.40 GB removed)**:
   - Back up the latest `so-thats-why/pool/` and `history-curiosity/pool/` snapshots to Drive
     (`_共用/製作檔/題庫-<系列>-latest/`) with `SHA256SUMS` and independent 0-difference verification.
   - Back up all PNG/JPG images under `series-plans/zhong-tian-qu-qi/` and
     `series-plans/top40-2025-2026/` to their respective `_共用/製作檔/series-plans-archive/` with
     `SHA256SUMS` and independent 0-difference verification.
   - Keep the ~36 lightweight `.md` rule files referenced by `docs/videos/rules-sync/manifest.tsv`
     untouched in Phase A so `sync.test.mjs` stays green.
   - Open a PR removing the verified static pools and binary images from GitHub and update any
     `so-thats-why`/`history-curiosity` pool CLI paths to accept a local/Drive directory flag.
2. **Phase B (Confirmed 2026-11-25 — Route B Google Drive SSOT)**:
   - Owner approved Route B on 2026-11-25: all video data, rules, lessons, scripts, and pools live on
     Google Drive (`AI/備份/AI劇/_START-HERE.md` & `AI/備份/AI劇/_規則/`), pulled via
     `npm run vdrive -- pull-rules` (`tools/video/vdrive.mjs`) with zero per-episode GitHub commits.
   - Disable the legacy production-host `rules-sync` root cron (note: `_規則/` is already outside
     `rules-sync` FILTERS so it cannot be overwritten in the meantime), then retire `docs/videos/rules-sync/`.
   - Decouple the remaining runtime/test references before removing legacy `docs/videos/` content:
     - `ops/video/Dockerfile` & `ops/video/sync-docs.mjs` (keep minimal seed or sync `lexicon.json` from Drive).
     - `tools/video/pool-admin/bundle.mjs` & `apps/api/app/video_pools/data/pools.json` (accept `--pool-dir` from Drive/cache and serve `pools.json` from host volume instead of GitHub).
     - `tools/video/qa/duration.test.mjs` & `tools/video/qa/facts.mjs` (switch from `docs/videos/` to synthetic fixtures / `--file` workdir).
     - Lower `LEGACY_EPISODE_DIRS` and `MAX_LEGACY_BINARY_FILES` in `tools/video-drive-boundary.test.mjs` as legacy files are removed.

## Definition of done

- [ ] Latest `so-thats-why/pool` and `history-curiosity/pool` archived on Google Drive with
      `SHA256SUMS` and independent 0-difference check.
- [ ] All binary images in `series-plans/zhong-tian-qu-qi` and `series-plans/top40-2025-2026`
      archived on Google Drive with `SHA256SUMS` and independent 0-difference check.
- [ ] Runtime/test couplings (`ops/video/sync-docs.mjs`, `pool-admin/bundle.mjs`, `qa/facts.mjs`,
      `qa/duration.test.mjs`) decoupled and `tools/video-drive-boundary.test.mjs` ceilings lowered.
- [ ] Verified pools, legacy episodes, and binary images removed from GitHub via PR with CI green.
- [x] Owner decision recorded on Phase B (2026-11-25: Route B approved — disable `rules-sync` cron on host and use Drive `AI/備份/AI劇/_規則/` as SSOT via `npm run vdrive`).
