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

The owner wants more distinct Curio history films with a complete long and Short package, animated condensed opener/intro/outro, and honest end links. Henry Box Brown's box escape can form a single source-led investigation, but its familiar 27-hour and exact-date claims are frequently told without identifying who said them. This task pins the Brown/Stearns account, whose quoted title page has no printed year, then writes a script that keeps Brown's own decisions and his continued insecurity central.

## Definition of done

- [x] A distinct A/B outline and recommended single story have an independently feasible pinned primary source, explicit 1848 family-separation versus undated-escape boundary, and full media/end-link plan.
- [x] A script/storyboard and one-to-one line/source/visual map carry a 30–60 second condensed opener, at least eight minutes of body even at 325 Chinese units per minute, the fixed 5-second intro/21-second outro, and no fabricated upload or paid-media receipts.
- [ ] Frozen author hashes pass the Curio video lint; parent workflow then obtains separate source/visual and fresh official dual-blind narrative audits before any paid media.

## Steps

- [x] Search existing S01–S62 briefs/topic catalog/tasks for Brown overlap and claim a narrow S63 scope.
- [x] Pin the GITenberg Brown/Stearns source by commit and raw SHA; distinguish Brown-mediated narrative from Stearns and Samuel May appended voices.
- [x] Draft source boundaries and A/B outline, including website owner versus local delegated decisions, Shorts and Studio links.
- [x] Independent feasibility receipt, frozen script/storyboard, claims, script export, lint and docs/task check; R3 source/visual audit passed 127/127 lines.
- [x] Parent receives exact R4 hashes and an independent source/visual receipt; audio and art remain gated while two fresh official blind readers assess the same freeze.

## How to verify

From this branch worktree:

```bash
sha256sum /tmp/curio-s63-box-brown-1849.txt
VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s63 --json
node tools/tasks.mjs check
git diff --check
```

The fixed raw text must hash to `6d80216184aaf20433e04aa8d1b6920076211304fcede4a095da3ef5bd62ada2`. The `/tmp` file is disposable source cache, not a committed asset.

Frozen preproduction hashes after R3 source/visual PASS: `video.json` `00cb544ad03d325f8eb666c3d037bf8a0aa3df1026c5c528ae54749a7d8e5090`; `script.md` `557427e904b22b40e8f326f9acd7947950c507c089ee6cee5dd4ea5be68dc37d`; `claims.md` `d1548e7232d4660da2518fac718dc1c00d45878a873d1ef90054e41f63769ee7`. The independent [R3 receipt](../../docs/videos/curio-s63/review/r3-source-visual-independent.md) counts 2,686 story-body Han characters excluding the CTA, or 8.26 minutes at 325 CPM, and a 168-character opener, about 31 seconds. `lint` reported 0 errors/0 warnings; docs-video tests passed 236/236. The subsequent formal blind result is recorded below; no paid media has been started.

## R3 official blind HOLD (2026-10-22 UTC)

Two fresh readers each received only the same frozen R3 narration and 13 official questions. Their separate source ballots and CLI receipts are under `docs/videos/curio-s63/review/r3-isolated-blind-{a,b}.*`. The [formal OR merge](../../docs/videos/curio-s63/review/r3-formal-merge-audit.md) is **11/13 HOLD**: both readers answered No on `no_spoiler` (`s63009`) and `no_recap` (different repetitions at `s63015` and `s63029`); B alone marked `no_detour` at `s63016`. The official CLI replay exited 1 with exactly the two shared required failures. R3 script and source/visual PASS remain archived for their frozen hashes, but the episode cannot enter paid media. The author then made the narrow R4 revision recorded below; it needs fresh independent checks.

## R4 author repair and source review (2026-10-22 UTC)

The [R4 author repair](../../docs/videos/curio-s63/review/r4-author-repair.md) changes only seven scene IDs to keep the box exit and Northern speech unresolved in the opener, remove duplicate age and household income facts, and replace the factory number list with Brown's work and ability to leave. Frozen R4 hashes: `video.json` `0f4cb372e473ed68c54de32fffa9449b98e372a920e7e01700927321eba31364`; `script.md` `85af6713b18b42ad1177063cc3dfc5b5665810d70334678114693460dd3161d7`; `claims.md` `5cbcca08555bf337269a4a9b572bb0c3bd5bd28d19662715f93d9ac151861617`. Story body excludes CTA and remains 2,690 Han characters, 8.28 minutes at 325 CPM; opener is 167 Han characters, about 31 seconds. Lint remains 0/0. The [independent R4 source/visual receipt](../../docs/videos/curio-s63/review/r4-source-visual-independent.md) passes 127/127 lines, their anchors and written visuals against these exact hashes. The [formal R4 dual-blind merge](../../docs/videos/curio-s63/review/r4-formal-merge-audit.md) is **12/13 HOLD** on `no_recap`. No paid media may start on this draft.

## R5 author repair (2026-10-22 UTC)

The [R5 repair memo](../../docs/videos/curio-s63/review/r5-author-repair.md) splits one source sentence into two sequential events at `s63103` and `s63104`: six-o'clock wagon arrival, then inquiry for the addressed box and loading. It removes the repeated receiver planning without adding undocumented speech. Frozen R5 hashes: `video.json` `118430ef07ca7ac2e6d7c198088bdd1ef312755e126fef15ea2b310475a39adf`; `script.md` `dee3cb408979b3ca7dff85fb00e63915c2e54e555a0ee22e776e28fc97556c0f`; `claims.md` `5b616ce92afd61feed9264e57da240388619588e636550a91e93a315e2d6a9fc`. Body excluding opener and CTA is 2,673 Han characters, 8.22 minutes at 325 CPM; opener remains 167 Han characters, about 31 seconds. Lint 0/0. The [independent R5 source/visual receipt](../../docs/videos/curio-s63/review/r5-source-visual-independent.md) passes the unchanged 125/127 lines by exact diff and independently checks the two revised lines. The [formal R5 dual-blind merge](../../docs/videos/curio-s63/review/r5-formal-merge-audit.md) is **12/13 HOLD** on `no_recap`: A flags `s63052`, B flags `s63106`. B alone also flags final `s63126` on `payoffs`; OR merge passes that question while preserving the concern. R6 needs fresh source and blind checks.

## R6 author repair (2026-10-22 UTC)

R6 [作者窄幅修稿](../../docs/videos/curio-s63/review/r6-author-repair.md)從 R5 兩個 `no_recap` 位置及 B 單獨的片尾 `payoffs` 顧慮出發，只改 `s63002`、`s63004`、`s63052`、`s63106`、`s63126` 五個場景 ID。凍結雜湊：`video.json` `8f8903a7ec270c61636953a7d675840a838604c268132722658c05b26f2dbf68`；`script.md` `dfafdb178646575cc4cefab9c14621284835299caf1c75f3eea86e7835d82bd9`；`claims.md` `10a28deb76976f1b7c32eb4ab0188c6fda33e93d1914d2d1536c1ecd7eb9c18e`。開場 175 漢字約 32 秒，正文排除開場與 CTA 2,682 漢字約 8.25 分鐘（325 字／分）；lint 0/0。[R6 獨立來源／畫面審核](../../docs/videos/curio-s63/review/r6-source-visual-independent.md)以完全相同的 R6 凍結雜湊 PASS，五個修改 ID 均無阻擋項，另外 122 個場景逐欄未變。[R6 正式雙人盲讀合併](../../docs/videos/curio-s63/review/r6-formal-merge-audit.md)為 **12／13 HOLD**：A 否決 `no_spoiler`（`s63001`）及 `no_recap`（`s63124`），另非必答章名題否；B 否決 `no_recap`（`s63062`）。官方 OR 與 CLI 重播共同只擋 `no_recap`。作者另凍結 R7 才能重新送獨立審核；付費媒體維持封鎖。

## Notes

R4 [正式雙人盲讀合併審核](../../docs/videos/curio-s63/review/r4-formal-merge-audit.md)為 **12／13 HOLD**：A 否決 `payoffs` 與 `no_recap`，B 只否決 `no_recap`；官方逐題 OR 與 CLI 重播共同只擋 `s63103` 的重複接收者資訊。作者須另凍結 R5，並取得新的獨立史料／畫面審核及兩位未讀 R4 的正式盲讀，才可解鎖付費媒體。

Brown's narrative has the wife's and children's forced sale in August 1848, but does not explicitly date his own escape. The book's hymn is signed 1849-09-01, while the cited title page lacks a printed publication year; do not infer a publication year or an escape day from that signature. Exact 27 hours and 3 ft 1 in × 2 ft × 2 ft 6 in are Samuel J. May's appended speech extract, not Brown's stopwatch/measurement. The book was written by Charles Stearns from Brown's statement; it is not Brown's autograph diary. The source is accessible at pinned GITenberg revision `a92658e80effa4cce03bb19c13e96ffaaae5fa2b`; NPS and other sites tested through this cloud proxy returned CONNECT 403, so unviewed pages are not used as evidence. No paid voice, image or music has been requested for S63.
