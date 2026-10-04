---
id: 2026-10-03-ai-terms-episode-system-one-plan
title: Plan the AI terms episode on System One models (the TypeSafe Jev launch)
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-10-03T17:01:57Z
created_at: 2026-10-03T17:01:56Z
completed_at: 2026-10-03T17:50:22Z
branch: claude/optimistic-hypatia-r2586e
depends_on: []
scope:
  - docs/videos/ai-term-system-one-model
  - docs/videos/ai-term-calibration
---

# Plan the AI terms episode on System One models (the TypeSafe Jev launch)

## Why

The owner asked for an episode of 「AI 名詞十分鐘」 about TypeSafe's launch post
"Introducing System One Models & Jev" (https://typesafe.ai/blog/introducing-system-one-models-and-jev).
The series covers one term per episode and keeps product names out, so the episode is on the
term the post introduces, the System One model, with Jev as the first example. An earlier plan
in this session chose calibration instead; that was a misreading of the request.

## Definition of done

- [x] `docs/videos/ai-term-system-one-model/brief.md` passes the pipeline's own brief check and
      outline parser, with three outlines (recipes B recommended, A, C).
- [x] Every claim it uses was verified against the live source by two independent checks.
- [x] `demo-log.md` records what was computed offline and pre-registers the writing-day run;
      `demo/` holds the scripts, repo-relative, reusing the site's own Jev client.
- [x] `notes.md` holds the owner's decisions, the catalogue row and what could not be confirmed,
      outside the brief that Jev reads.
- [x] The article and production are filed, and so are the three defects found on the way.
- [x] The calibration brief's false statements about the site's own use of Jev are corrected,
      and its two tasks are blocked pending the owner.

## How to verify

```bash
node --input-type=module -e "import {readFileSync} from 'node:fs'; const l = await import('./tools/video/core/lint.mjs'); console.log(l.checkBrief(readFileSync('docs/videos/ai-term-system-one-model/brief.md','utf8')))"
cd docs/videos/ai-term-system-one-model/demo && python3 demo_live_jev.py --date-probe
```

## Notes

- Research and verification ran as two multi-agent passes (25 agents): claims in the post,
  the term and its origin, the site's own Jev records, overlap and policy, the demonstration;
  three outlines judged on series craft, policy and facts; then two refuters per claim group
  and a completeness critic.
- The P1 pilot `2026-09-29-video-pilot-jev-decision-model` covers the same post as product
  news. This session cannot edit it; the owner decides (`notes.md` item 1).
- The customer agreement's publicity clause (§16.4) bears on chapters 4 and 5; quoted in
  `notes.md` item 3.
- **Owner decisions, 2026-10-03.** The P1 pilot `2026-09-29-video-pilot-jev-decision-model`
  is merged into this episode (closed; its duties moved to
  `2026-10-03-ai-term-system-one-model-video`, now P1). The calibration episode is abandoned:
  its folder and two tasks were deleted, so the calibration items in the definition of done
  above no longer apply.
