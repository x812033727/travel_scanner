---
id: 2026-10-03-ai-term-calibration-article
title: Write and publish the AI terms article on calibration (ai-term-calibration)
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-03T15:00:59Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-term-calibration.json
  - apps/web/public/guides/ai-term-calibration
  - docs/ai-terms-series/calibration
---

# Write and publish the AI terms article on calibration (ai-term-calibration)

## Why

The AI terms video series requires a published article before an episode
(`docs/videos/ai-terms/README.md` §一個名詞怎麼變成一集): the fact checks live there, the
video description links to it, and the worker's topic deduplication keys on
`source_guide`. Calibration is a new term, not one of the 81 published ones. The
episode brief is `docs/videos/ai-term-calibration/brief.md`.

## Definition of done

- [ ] `ai-term-calibration` is published in zh-TW to the spec in
      `docs/ai-terms-series/brief.md`: first-party sources, a worked example with input,
      steps, expected output and how to read a failure, one diagram, a link to the index.
- [ ] `apps/web/public/guides/ai-term-calibration/diagram-1.svg` is a reliability diagram
      (stated confidence against observed accuracy, with the diagonal).
- [ ] The other four locales follow the article-localization route.

## Steps

- [ ] Read the `content-pipeline` skill, then plan the batch of one.
- [ ] Reuse the sources the brief lists under §會過期的事實, re-opened on writing day.
- [ ] Reuse the demo in `docs/videos/ai-term-calibration/demo-log.md` as the worked example.
- [ ] Ingest, deploy, publish and verify per the skill.
- [ ] Decide with the owner whether `docs/ai-terms-series/catalogue.json` and the
      `ai-terms-index` article gain the term; widen this scope first if so.

## How to verify

The article renders at https://mokaair.com/zh-TW/life/ai-term-calibration and the
skill's post-publish checks pass.

## Notes

- Keep Jev's speed and price claims out; they belong to
  `2026-09-29-video-pilot-jev-decision-model`.
- No medical, financial or legal datasets in the example (channel stance point 7).
