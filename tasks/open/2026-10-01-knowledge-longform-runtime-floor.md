---
id: 2026-10-01-knowledge-longform-runtime-floor
title: Reject knowledge and nonfiction long cuts shorter than eight minutes
status: in-progress
priority: P1
area: tools
owner: codex-longform-qa
claimed_at: 2026-10-01T15:59:57Z
created_at: 2026-10-01T15:59:55Z
completed_at:
branch: codex/sothatswhy-season2-complete
depends_on: []
scope:
  - tools/video/core/duration.mjs
  - tools/video/core/duration.test.mjs
  - tools/video/qa/checks.mjs
  - tools/video/qa/cli.mjs
  - tools/video/qa/duration.test.mjs
---

# Reject knowledge and nonfiction long cuts shorter than eight minutes

## Why

The owner requires every knowledge explainer, AI terminology long video and nonfiction
brand story to run at least eight minutes. A planned duration and an older passing cut
report cannot establish the runtime of today's narration or finished cut. Counting the
channel intro and outro would also let a body shorter than eight minutes pass.

## Definition of done

- [x] These long videos require a current actual narration timeline and checked final cut
  of at least 14,400 frames at 30 fps; exactly 480 seconds passes, one frame less fails.
- [x] Narration frames, presentation frames, frame rate and speech hashes agree with the
  cut's checks; missing, stale or invalid timelines fail even with legacy passing checks.
- [x] Intro and outro do not count toward the body floor. Shorts, ordinary drama episodes,
  binge compilations and unrelated videos keep their existing duration rules.
- [x] QA retains its eleven-item report and rejects duration failures in its assemble item.

## Steps

- [x] Recognize category `ai-terms`, `explainer` or `story`, look preset `flat-explainer`,
  and established `sothatswhy-`, `ai-term-` and `story-` long-video slugs.
- [x] Add the actual frame floor to QA and cover boundary, bookend and stale-report cases.

## How to verify

With Node 24, run:

```text
node --test tools/video/core/duration.test.mjs tools/video/qa/duration.test.mjs tools/video/qa/checks.test.mjs tools/video/qa/qa.test.mjs
```

## Notes

- 2026-10-02: Node 24.19.0 ran the four-file check above: 31 passed, 0 failed, exit 0.
  The new core cases prove 14,400 frames passes and 14,399 frames fails without rounding;
  padded bookends, stale hashes, different FPS and mismatched final frames fail. The QA
  integration case exercises the actual CLI and asserts all eleven original item IDs.
- Existing assemble checks already verify final video packets against the presentation
  frame count. Legacy checks do not carry a separate FPS metric, so QA binds them to the
  current narration and presentation timelines' required 30 fps; an explicit FPS metric
  must also match. No planned-minute or estimated-timeline fallback is accepted.
- Brand-story worker output is `format: drama` with `category: story`; ordinary drama
  fixtures have neither that category nor a recognized catalogue slug and stay unchanged.
- Only the QA CLI's assemble call changed; the thumbnail changes from PR #1100 were not
  touched. No media generation, production setting, publication, Git or PR action ran.
