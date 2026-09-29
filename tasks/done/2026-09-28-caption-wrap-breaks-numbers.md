---
id: 2026-09-28-caption-wrap-breaks-numbers
title: Caption wrapping can break inside numbers and product names, and start a line with a full stop, in CJK locales
status: done
priority: P2
area: tools
owner: codex-caption-wrap
claimed_at: 2026-09-29T11:29:25Z
created_at: 2026-09-28T05:04:19Z
completed_at: 2026-09-29T11:45:22Z
branch: codex/caption-wrap-boundaries
depends_on: []
scope:
  - tools/video/core/captions.mjs
  - tools/video/core/captions.test.mjs
---

# Caption wrapping can break inside numbers and product names, and start a line with a full stop, in CJK locales
## Why

Found on 2026-09-28 while translating the English season's captions into zh-CN (`docs/videos/<slug>/i18n/zh-CN.json` for `openai-agents-broke-in`, `always-on-agent-explained`, `gpt6-vs-opus55-worth-paying`). Simulating the cues with `buildCues` in `tools/video/core/captions.mjs`, the CJK line wrap produced breaks inside a number or product name (「4 / .0」, 「GPT / -6」, 「0. / 50」) and let a caption line start with 「。」. The translator reworded about 60 lines so these three videos never hit it; the next CJK translation will.

## Definition of done

- [x] A CJK caption line never breaks inside a run of Latin letters, digits and the joiners `. - + # ' _` (a version like `4.0`, a price like `0.50`, a name like `GPT-6`), unless the run alone is longer than the line.
- [x] A caption line never starts with closing punctuation, 「。」 included (`OPENS_BADLY` covers it and the break search honours it).
- [x] Tests in `tools/video/core/captions.test.mjs` cover each case; existing zh-TW captions of earlier videos are unchanged where they had no such break.

## Steps

- [x] Reproduce with a zh-CN line like 「Terminal-Bench 4.0 得分 66.4%」 and a narrow `maxChars`.
- [x] Fix the tokenizer or the break search, add tests, run `npm run test:tools`.

## How to verify

```bash
node --test tools/video/core/captions.test.mjs
npm run test:tools
```

## Notes

- The zh-CN translator's simulation scripts are in the session scratchpad (`zhcn/`), not in the repo; the cases above are enough to reproduce.
- 2026-09-29: Claimed after checking active ancestor scopes, local branches/worktrees, remote heads and fully paginated open-PR files. No competing caption changes were found; repeated before preparing the PR against main `a2fe00f4`.
- Group complete Latin tokens with their following closing punctuation (including intervening whitespace and consecutive closers). Use the same legal boundaries for balanced wrapping, fallback and cue capacity. Preserve the original midpoint score. A layout such as `甲ABCDEF。乙` at width 4 now becomes separate cues instead of a three-line fallback or a line beginning with a full stop.
- `buildCues` also checks the displayed layout, while preserving the original raw-text capacity and timing weights. This avoids unnecessary cue/timing changes when the renderer omits a trailing comma or full stop. Eight real lines covering this regression have exact cue/text/time assertions.
- Regression evidence: initial token/punctuation tests failed 10 cases on the original code; compatibility tests then failed 8 cases on the first fix. Final focused suite: 33 passed, 0 failed. Final full tools suite on the updated main: 784 tests, 782 passed, 2 existing platform skips, 0 failed (Node 24.21.0).
- Independent local checks: 5,427 token/punctuation/width combinations and 1,374 boundary/feasibility cases pass. A frozen corpus of 5,483 real text lines from 16 videos keeps all 5,448 previously safe complete cues and timings unchanged, including all 975 English and 975 Korean lines; the remaining 35 lines fix existing CJK defects.
- Repeating that corpus with 3-second synthetic speech plus the 400 ms linger keeps the same 5,448 safe outputs unchanged and introduces no line-count, punctuation-start, split-token, overlap or time-window error. No adjacent cues in this corpus qualify for merging; focused tests separately exercise short-cue merge decisions.
- When an indivisible token plus closing punctuation is wider than one line, preserve its text and let existing width QA report it. Validation uses local text and synthetic timelines; release and rendered-media acceptance remain separate from this code change.
