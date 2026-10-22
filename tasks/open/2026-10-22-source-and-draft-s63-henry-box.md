---
id: 2026-10-22-source-and-draft-s63-henry-box
title: Source and draft S63 Henry Box Brown escape episode
status: in-progress
priority: P2
area: docs
owner: codex-s63-new-episode
claimed_at: 2026-10-22T02:07:57Z
created_at: 2026-10-22T02:07:54Z
completed_at:
branch: codex/curio-s63-box-brown-20261022
depends_on: []
scope:
  - docs/videos/curio-s63
---

# Source and draft S63 Henry Box Brown escape episode

## Why

The owner wants more distinct Curio history films with a complete long and Short package, animated condensed opener/intro/outro, and honest end links. Henry Box Brown's box escape can form a single source-led investigation, but its familiar 27-hour and exact-date claims are frequently told without identifying who said them. This task first pins the 1849 Brown/Stearns account, then writes a script that keeps Brown's own decisions and his continued insecurity central.

## Definition of done

- [x] A distinct A/B outline and recommended single story have an independently feasible pinned primary source, explicit 1848 family-separation versus undated-escape boundary, and full media/end-link plan.
- [x] A script/storyboard and one-to-one line/source/visual map carry a 30–60 second condensed opener, at least eight minutes of body even at 325 Chinese units per minute, the fixed 5-second intro/21-second outro, and no fabricated upload or paid-media receipts.
- [ ] Frozen author hashes pass the Curio video lint; parent workflow then obtains separate source/visual and fresh official dual-blind narrative audits before any paid media.

## Steps

- [x] Search existing S01–S62 briefs/topic catalog/tasks for Brown overlap and claim a narrow S63 scope.
- [x] Pin the GITenberg Brown/Stearns 1849 source by commit and raw SHA; distinguish Brown-mediated narrative from Stearns and Samuel May appended voices.
- [x] Draft source boundaries and A/B outline, including website owner versus local delegated decisions, Shorts and Studio links.
- [x] Independent feasibility receipt, frozen script/storyboard, claims, script export, lint and docs/task check; R3 source/visual audit passed 127/127 lines.
- [ ] Parent receives exact hashes for independent source/visual and two fresh official blind readers; audio and art remain gated.

## How to verify

From this branch worktree:

```bash
sha256sum /tmp/curio-s63-box-brown-1849.txt
VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s63 --json
node tools/tasks.mjs check
git diff --check
```

The fixed raw text must hash to `6d80216184aaf20433e04aa8d1b6920076211304fcede4a095da3ef5bd62ada2`. The `/tmp` file is disposable source cache, not a committed asset.

Frozen preproduction hashes after R3 source/visual PASS: `video.json` `00cb544ad03d325f8eb666c3d037bf8a0aa3df1026c5c528ae54749a7d8e5090`; `script.md` `557427e904b22b40e8f326f9acd7947950c507c089ee6cee5dd4ea5be68dc37d`; `claims.md` `d1548e7232d4660da2518fac718dc1c00d45878a873d1ef90054e41f63769ee7`. The independent [R3 receipt](../../docs/videos/curio-s63/review/r3-source-visual-independent.md) counts 2,686 story-body Han characters excluding the CTA, or 8.26 minutes at 325 CPM, and a 168-character opener, about 31 seconds. `lint` reported 0 errors/0 warnings; docs-video tests passed 236/236. The official 13-question dual blind read and all paid media remain outstanding.

## Notes

Brown's narrative has the wife's and children's forced sale in August 1848, but does not explicitly date his own escape. The book's hymn is signed 1849-09-01, while the cited title page lacks a printed publication year; do not infer a publication year or an escape day from that signature. Exact 27 hours and 3 ft 1 in × 2 ft × 2 ft 6 in are Samuel J. May's appended speech extract, not Brown's stopwatch/measurement. The book was written by Charles Stearns from Brown's statement; it is not Brown's autograph diary. The source is accessible at pinned GITenberg revision `a92658e80effa4cce03bb19c13e96ffaaae5fa2b`; NPS and other sites tested through this cloud proxy returned CONNECT 403, so unviewed pages are not used as evidence. No paid voice, image or music has been requested for S63.
