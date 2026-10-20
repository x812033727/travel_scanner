---
id: 2026-10-20-s54-r16-official-narrative-merge-and
title: S54 R16 official narrative merge and policy gate
status: done
priority: P1
area: docs
owner: codex-s54-r16-merge-policy
claimed_at: 2026-10-20T23:08:57Z
created_at: 2026-10-20T23:08:54Z
completed_at: 2026-10-20T23:12:31Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s54/review/r16-merge-policy
---

# S54 R16 official narrative merge and policy gate

## Why

Two R16 blind readers each failed one different narrative question. Their votes must be preserved and combined with the repository's official OR rule before the exact-version Jev policy gate can run; R15 policy is stale after the two-line oral rewrite.

## Definition of done

- [x] Complete original ballots, formal merge, CLI narrative receipt, and a one-shot exact-version Jev policy receipt are archived with a clear PASS/HOLD.

## Steps

- [x] Verify five frozen hashes and independent source PASS; preserve A/B markdown ballots and transcribe all 13 answers each with cited script lines.
- [x] Run official `panelVerdict` and `mergePanelVerdicts`, then CLI `narrative --answers` using an isolated workdir.
- [x] Build the exact `policyRequest` from frozen `video.json` and `brief.md`, submit once through the repository client, and archive raw response and parsed receipt.

## How to verify

`sha256sum docs/videos/curio-s54/{brief.md,research.md,claims.md,video.json,script.md}` matched R16 throughout. `node tools/video/cli.mjs narrative --slug curio-s54 --answers docs/videos/curio-s54/review/r16-merge-policy/merged-answers.json --workdir /tmp/s54-r16-merge-work --json` exited 0. `node tools/video/cli.mjs lint --slug curio-s54 --json` returned 0 errors/0 warnings. `npm run test:docs-videos` passed 236/236 and `npm run check:tasks` passed.

## Notes

**PASS**: formal panel 13/13 under OR, with A's `payoffs` NO and B's `no_spoiler` NO retained; Jev explainer policy `passed:true` on one HTTP 200 request. All raw inputs/outputs, hashes, and limitations are in `docs/videos/curio-s54/review/r16-merge-policy/summary.md`. No creative file or paid audio was changed.
