---
id: 2026-10-02-video-render-settled-layout
title: Validate video layouts after entrance animations settle
status: in-progress
priority: P1
area: tools
owner: codex-t26-render-layout
claimed_at: 2026-10-02T10:44:22Z
created_at: 2026-10-02T10:44:14Z
completed_at:
branch: codex/sothatswhy-t26-pilot
depends_on: []
scope:
  - tools/video/render/browser.mjs
  - tools/video/render/browser.test.mjs
---

# Validate video layouts after entrance animations settle

## Why

The T26 pilot's normal render rejected all 157 diagram states as 4–28px taller
than their area, although their final PNGs fit. The layout check ran while the
theme's full-height paper was entering from `translateY(28px)`, before the
renderer paused and sought that animation. The elapsed loading time therefore
changed the reported overflow. Judge the settled final layout that is captured
as the still, retaining the entrance frames and genuine layout/load failures.

## Definition of done

- [x] An entering full-height diagram that fits at rest passes regardless of the
  wall-clock entrance position; its transition is still rendered frame by frame.
- [x] Truly oversized content, text that cannot fit, missing images and unloadable
  font faces still fail. Repeated stills and all entrance frames remain identical.

## Steps

- [x] Audit active claims, worktree branches, remote heads and open PR paths for
  both exact tools paths; claim this separate dependency before touching them.
- [x] Reproduce the false overflow deterministically in the actual Edge browser,
  with the native diagram template's entrance held at time zero.
- [x] Move the unchanged layout check after the existing exact final animation
  seek; preserve theme CSS, fit/overflow limits, launch flags and two-rAF wait.
- [x] Run the same actual-browser regression against the HEAD renderer and the
  fixed renderer; retain both outputs and independent T26 DOM measurements.
- [x] Run scoped renderer/template/thumbnail tests and the complete tools suite.

## How to verify

Use the configured bundled Node runtime (v24.19.0 in this workspace). The browser
test deliberately opts in on a host with Chromium/Edge installed; ordinary tools
CI skips it rather than pretending to have exercised a missing browser.

```powershell
$env:VIDEO_RENDER_BROWSER_TESTS='1'
$env:VIDEO_BROWSER_CHANNEL='msedge'
node --test tools/video/render/browser.test.mjs
```

Clear those opt-in variables for the ordinary suite, then run:

```text
node --test tools/video/render/render.test.mjs tools/video/render/browser.test.mjs tools/video/templates/templates.test.mjs tools/video/qa/thumbnail.test.mjs
npm run test:tools
npm run check:tasks
```

The T26 production task runs a normal full `render --force` because frame keys
hash the theme/HTML/assets, not this browser module. Preserve its earlier cache
as evidence; do not edit cached diagnostic flags to make it pass.

## Notes

- Collision preflight: exact scopes `tools/video/render/browser.mjs` and the new
  `tools/video/render/browser.test.mjs` have no active task or open PR. Main already
  contains PR #1114 (`57da8b928`) for deterministic software raster/animation seek;
  that behavior is retained. This dependency shares the pilot branch without
  expanding the parent task's documentation scope.
- Independent actual T26 probe: c2-s04 at ordinary load had paper translateY
  13.1125px and content 791/778px; explicit time 0 had translateY 28px and content
  806/778px; final seek 371ms (end 370ms) had no transform, content 778/778px and
  no problems. c1-s02 and c3-s01-detail showed the same cause.
- Red regression uses an outside-repository copy of the unchanged HEAD renderer
  with only its local import URLs mapped back to this checkout. The native theme's
  entrance is paused at time zero for a deterministic reproduction: the fitting
  diagram fails with 28px overflow. A truly taller paper is measured as 76px during
  that entrance rather than its settled 48px. Missing-image/font and text-fit
  cases continue to fail as intended.
- Green actual Edge regression: 6/6 tests passed, exit 0. The settled diagram
  passes, keeps its 12 entrance frames, and two runs have identical still and all
  transition SHA256 values. The genuinely oversized 874px paper retains a 48px
  overflow error; unfit text, missing image and unloadable font still fail.
- Scoped ordinary tests: 47 passed, 1 browser opt-in skipped, exit 0. Complete
  tools suite: 1,206 passed, 3 skipped (two existing plus this browser opt-in),
  0 failed, exit 0; 75.02 seconds. An initial scoped attempt with the system Node
  v24.13.0 crashed in the render test process with Windows exit 3221226505; rerun
  with the configured bundled v24.19.0 passed. No test or production threshold
  was changed to address that environment failure.
- `check:tasks` validated 1,290 files, exit 0, with existing stale-claim and scope
  overlap warnings. Scoped `git diff --check` also exits 0.
- Evidence outside the repo: `C:/Users/x8120/.codex/visualizations/2026/10/01/01a0f5cd-1f4c-7f91-9af1-b02370fcce78/t26-render-settled-browser-red.log`,
  `t26-render-settled-browser-green.log` and `t26-render-settled-full-tools.log` in
  the same directory. The baseline builder and exact original HEAD renderer are
  preserved there too. No media, credentials or evidence binary is committed.
- Root owns final ticket closure together with the finished episode; no commit,
  push or PR is created by this dependency agent.
