---
id: 2026-10-03-ai-term-calibration-video
title: Produce the AI terms episode on calibration (ai-term-calibration)
status: blocked
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-03T15:01:00Z
completed_at:
branch:
depends_on:
  - 2026-10-03-ai-term-calibration-article
  - 2026-10-03-ai-terms-episode-calibration-plan
scope:
  - docs/videos/ai-term-calibration
  - docs/videos/ai-terms/terms.json
  - docs/videos/ai-terms/README.md
  - docs/videos/long-form/plans.json
  - tools/video/long-form/plans.mjs
---

# Produce the AI terms episode on calibration (ai-term-calibration)

## Why

The brief for the calibration episode of 「AI 名詞十分鐘」 is written
(`docs/videos/ai-term-calibration/brief.md`). This task takes it from the outline gate
to an upload package, and registers the term in the series catalogue.

## Definition of done

- [ ] `docs/videos/ai-terms/terms.json` has the row in the brief's §名詞庫的一列, with
      `counts` updated, and the long-form plans rebuilt and checked.
- [ ] The episode goes through the automated route (`automated.md`) from
      `review-push --gate outline` to `package`, with `video.json`, `claims.md`,
      `verify-*.md`, `shorts.json` and `i18n/` in `docs/videos/ai-term-calibration/`.
- [ ] `terms.json` carries `video_id` and `published_at` once it is up.

## Steps

- [ ] Get the owner's answers to the brief's §站主要決定的事 (term, naming Jev, the
      shadow-report figures, order).
- [ ] Add the row; raise `CATALOG_COUNTS["ai-terms"]` to 82 in
      `tools/video/long-form/plans.mjs`; `node tools/video/long-form/cli.mjs build`, then
      `check`. The duration review and the admin catalog (`admin-catalog.mjs`, which
      reports 473 entries) are hash-bound to these files: widen this scope to cover
      whatever `check` names before editing them.
- [ ] Rerun the demo script on writing day and update `demo-log.md` if the numbers move.
- [ ] Write, verify, synthesize, illustrate, assemble and package per the series spec.

## How to verify

```bash
node tools/video/long-form/cli.mjs check
npm run test:tools
node tools/video/cli.mjs status --slug ai-term-calibration
```

## Notes

- Depends on the article: the series publishes the article first.
- The brief recommends outline A (recipe A); C would repeat the RAG pilot's recipe.

- **Blocked 2026-10-03, waiting on the owner.** This episode was planned from a misreading: the owner asked for an episode on TypeSafe's launch post, now planned as `docs/videos/ai-term-system-one-model`. Calibration remains a reasonable term; the owner decides whether it gets its own episode (`docs/videos/ai-term-system-one-model/notes.md` item 2). If yes, run `npm run tasks -- status <id> open`. The brief's statements about the site's own use of Jev were corrected the same day after verification.
