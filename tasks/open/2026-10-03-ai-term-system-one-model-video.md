---
id: 2026-10-03-ai-term-system-one-model-video
title: Produce the AI terms episode on System One models (ai-term-system-one-model)
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-03T17:48:48Z
completed_at:
branch:
depends_on:
  - 2026-10-03-ai-term-system-one-model-article
  - 2026-10-03-ai-terms-episode-system-one-plan
scope:
  - docs/videos/ai-term-system-one-model
  - docs/videos/ai-terms/terms.json
  - docs/videos/ai-terms/README.md
  - docs/videos/long-form/plans.json
  - tools/video/long-form/plans.mjs
  - docs/videos/lexicon.json
---

# Produce the AI terms episode on System One models (ai-term-system-one-model)

## Why

The brief for the System One model episode of 「AI 名詞十分鐘」 is written
(`docs/videos/ai-term-system-one-model/brief.md`). This task takes it from the outline gate to
an upload package and registers the term in the series catalogue.

## Definition of done

- [ ] The owner has answered `docs/videos/ai-term-system-one-model/notes.md` §站主要決定的事,
      at least items 1, 3, 5, 6 and 7, before anything is generated.
- [ ] `docs/videos/ai-terms/terms.json` has the row in `notes.md`, `counts` updated,
      `CATALOG_COUNTS["ai-terms"]` raised in `tools/video/long-form/plans.mjs`, and
      `node tools/video/long-form/cli.mjs build` then `check` pass. The duration review and the
      admin catalog are hash-bound to these files: widen this scope to whatever `check` names.
- [ ] The writing-day run in `demo-log.md` is done and its output pasted there.
- [ ] The episode goes through the automated route from `review-push --gate outline` to
      `package`, with `video.json`, `claims.md`, `verify-*.md`, `shorts.json` and `i18n/`.
- [ ] `lexicon.json` has the words the brief lists under 素材.

## Steps

- [ ] Wait for the article task, and for the tasks currently holding `docs/videos/ai-terms` and
      `docs/videos/lexicon.json` (`npm run tasks -- claim` refuses until they release them).
- [ ] Turn off Jev's outline pick and final auto-approval for this one video, or approve both
      gates by hand (`notes.md` item 6).

## How to verify

```bash
node tools/video/long-form/cli.mjs check
npm run test:tools
node tools/video/cli.mjs status --slug ai-term-system-one-model
```
