---
id: 2026-10-15-h09-navy-source-link
title: Replace unavailable H09 Navy source link
status: done
priority: P2
area: docs
owner: codex-gpt6-curio-h09
claimed_at: 2026-10-15T07:34:35Z
created_at: 2026-10-15T07:34:27Z
completed_at: 2026-10-15T07:36:51Z
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09/video.json
---

# Replace unavailable H09 Navy source link

## Why

H09's final QA could not fetch the U.S. Navy history URL in the planned YouTube description. The same museum article is available on the National Naval Aviation Museum's own site. The broken URL would otherwise be included in the upload metadata.

## Definition of done

- [x] The H09 upload metadata points to a reachable museum source for Colorado (BB-45) and its O3U Corsair search aircraft, without changing the approved script or media.

## Steps

- [x] Confirm the replacement is the same official museum article and returns HTTP 200 with the video QA link checker.
- [x] Change only `video.json`'s source title and URL; keep the H09 final review receipt and approved media intact.

## How to verify

`node tools/video/cli.mjs lint --slug curio-h09` reports 0 errors and the same 3 narrative warnings. `npm run check:tasks` passes. `checkLinks([url], linkChecker())` returns HTTP 200. Compare the SHA-256 of `script.md`, `timeline.json`, `keyframes/manifest.json` and `final.mp4` against their approved hashes in the H09 production task.

## Notes

2026-10-15: The first final QA report remains 9/11, with a failed link and an unrelated missing pre-decision language snapshot. It was already submitted for manual owner review. This narrow source correction does not rerun TypeSafe Jev or rewrite that historical QA report. The replacement article is https://navalaviationmuseum.org/naval-aviation-and-the-search-for-amelia-earhart/ .
