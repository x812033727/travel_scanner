---
id: 2026-09-30-video-worker-blocks-on-scene-data
title: Video worker blocks on scene data and brief headings lint cannot see
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-30T00:29:31Z
created_at: 2026-09-30T00:28:19Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
---

# Video worker blocks on scene data and brief headings lint cannot see

## Why

On 2026-09-30 four automatic videos sat blocked on /admin/videos, and the owner's retry
button only blocked them again:

- `gemini-connected-apps-permissions` and `google-vids-omni-free-quota` failed `render` with
  "named chat messages are limited to 2". That rule (and every other template data rule in
  `tools/video/templates/templates.mjs`) runs only in `render`, after the narration is
  synthesized and approved, so the writer's lint-fix loop never saw it and the worker blocks.
- `claude-opus-5-5-three-numbers` failed "lint still fails after 3 fixes" because its brief
  copied the planner prompt's headings verbatim (`## 站主觀點 — the owner's first-person
  stance…`). `planProblem` accepts that (it only checks `includes`), but `briefSections` keyed
  the section by the whole heading, so `checkBrief` said the section was missing; the writer
  cannot change brief.md, so three fixes changed nothing.

## Definition of done

- [x] lint reports template data problems (chat names, message counts, …) as errors, so the
      writer fixes them before any audio is paid for.
- [x] A brief heading written as `## 站主觀點 — description` counts as the 站主觀點 section.

## How to verify

`node --test tools/video/core/lint.test.mjs`; the four blocked videos' documents from the host
lint as expected (three chat scenes flagged, all briefs pass).

## Notes

- The worker's writer prompt (`tools/video/automation/prompts.mjs`) still lists chat as
  "messages 1-5 of {name?}" without the two-names limit that writer-video.md has; left out here
  because `2026-09-28-sothatswhy-shorts-from-episode` holds that file. The lint error now reaches
  the writer anyway.
- A render *layout* problem (text taller than its area, e.g. meta-anti-scam's outro with a
  two-line title and four lines) still blocks: only a browser finds it. Fixed by hand on the host.
