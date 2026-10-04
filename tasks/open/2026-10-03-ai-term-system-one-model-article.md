---
id: 2026-10-03-ai-term-system-one-model-article
title: Write and publish the AI terms article on System One models (ai-term-system-one-model)
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-03T17:48:47Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-term-system-one-model.json
  - apps/web/public/guides/ai-term-system-one-model
---

# Write and publish the AI terms article on System One models (ai-term-system-one-model)

## Why

The AI terms video series publishes the article before the episode
(`docs/videos/ai-terms/README.md` §一個名詞怎麼變成一集): the fact checks live there, the
video's single next step and `source_guide` point to it, and the worker's topic deduplication
keys on it. The episode brief is `docs/videos/ai-term-system-one-model/brief.md`; owner
decisions that bear on the article are in `notes.md` beside it.

## Definition of done

- [ ] `ai-term-system-one-model` is published in zh-TW to the spec in
      `docs/ai-terms-series/brief.md`: whose definition it is (TypeSafe's), first-party sources,
      a worked example with input, steps, expected output and how to read a failure, one
      diagram, and a link to the index.
- [ ] `apps/web/public/guides/ai-term-system-one-model/diagram-1.svg`: left, a model writing a
      string token by token that a program must parse; right, a state plus your questions and
      options, one probability per option, used directly by code. No English-only labels.
- [ ] The other four locales follow the article-localization route.

## Steps

- [ ] Read the `content-pipeline` skill and plan a batch of one.
- [ ] Re-open the sources in the brief's §會過期的事實 on writing day.
- [ ] Keep the series' exclusions: no prices, speed multipliers, model names or leaderboards;
      "can't hallucinate" only as "answers stay inside the list but can be wrong".
- [ ] Decide with the owner whether `docs/ai-terms-series/catalogue.json` and the
      `ai-terms-index` article gain the term; widen this scope first if so.
- [ ] Before publishing anything that says Mokaair is a TypeSafe customer, check the owner's
      answer to `notes.md` item 3 (the customer agreement's publicity clause).

## How to verify

The article renders at https://mokaair.com/zh-TW/life/ai-term-system-one-model and the skill's
post-publish checks pass.
