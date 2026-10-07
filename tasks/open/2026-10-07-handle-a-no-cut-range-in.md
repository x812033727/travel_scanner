---
id: 2026-10-07-handle-a-no-cut-range-in
title: Handle a no-cut range in the reference-analysis FFmpeg sinks
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T02:57:16Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/youtube-video/scripts/reference_analysis.mjs
  - .claude/skills/youtube-video/scripts/reference_analysis.mjs
  - tools/reference-analysis.test.mjs
---

# Handle a no-cut range in the reference-analysis FFmpeg sinks

## Why

Reference analysis fails for a requested range with no detected cuts, instead of
returning an empty measured cut list. The comparison regression's synthetic blue
range `--range 4-6` produces no packets on `[cutsout]`; the installed FFmpeg build
rejects that empty output stream while `[motionout]` still has frames. Reporting
no cuts must not hide a failed analysis command or omit motion/silence results.

## Definition of done

- [ ] A static no-cut range completes successfully with an empty cut list and
      accurate range, motion and silence measurements.
- [ ] Nonempty cut ranges and the reference comparison preserve existing results.
- [ ] Both skill copies remain byte-identical; FFmpeg failures remain visible.

## Steps

- [ ] Review how `analyzeRange` maps `[cutsout]` and `[motionout]` to the null muxer.
- [ ] Add or refine a static-range regression and validate the sink arrangement
      with the reported Windows FFmpeg build and the supported Linux runtime.

## How to verify

Use the bundled compatible Node runtime:

```text
node --test --test-name-pattern "--compare matches" tools/reference-analysis.test.mjs
```

Then run the full reference-analysis test file. No production or provider call is
required; the input is a synthetic local fixture.

## Notes

- Independently reproduced on 2026-10-07 in an isolated targeted run (about 2.4 s),
  apart from the interrupted full tools attempt. Assertion at
  `tools/reference-analysis.test.mjs:447` expects `other.status === 0`.
- FFmpeg `N-125875-g5d4d3bdc61-20260731` exits `4294967274` (signed `-22`), with
  `wrapped_avframe` thread `Invalid argument` and a stream receiving no packets.
- The analysis source was introduced in `5df492340` / PR #1300 and is unchanged
  by the renewed-language caller repair. This does not indicate a paid-media or
  production-language failure. Do not widen this task into that caller work.
- Full-attempt evidence is retained outside Git at
  `<home>/mokaair-work/handoff/renewed-finals-20261007/tools-r3-check.log`;
  that attempt lost its execution session before a final suite summary/exit, so
  it must not be reported as a completed suite.
