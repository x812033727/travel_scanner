---
id: 2026-10-17-story-worker-a-rejected-pronunciation-proposal
title: Story worker: a rejected pronunciation proposal sends the chapter back instead of blocking forever
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-17T13:40:56Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/story.mjs
---

# Story worker: a rejected pronunciation proposal sends the chapter back instead of blocking forever

## Why

`story-lexicon-revise` (docs/videos/story-lexicon-revision.md) lets a reviewer `reject` a term a
story writer proposed, and a rejected term never enters the pinned dictionary. But
`advanceStory` in `tools/video/automation/story.mjs` blocks while any term of
`state.story.lexicon_pending` is missing from the snapshot, and nothing ever removes a term from
that list. The word is usually still in the chapter text too, so lint fails on it. A rejection
therefore blocks the story for good unless someone edits `auto.json` by hand.

## Definition of done

- [ ] After a reviewed revision that rejects a term, the worker's next pass sends the chapter(s)
      using that word back to the writer with "do not use <term>", within the existing retry
      ceilings, and removes the term from `lexicon_pending` once no chapter uses it.
- [ ] The decision is read from the immutable review receipt
      (`<workdir>/story/lexicon-reviews/<review_sha256>.json`, bound by the revision event), not
      from a mutable flag.

## Steps

- [ ] Read the head event's `review_sha256` and its receipt's `reject` decisions in `advanceStory`.
- [ ] Route the affected chapters to a writer fix; drop resolved terms from `lexicon_pending`.
- [ ] Tests in the story automation suite.

## How to verify

`node --test tools/video/automation/story.test.mjs` (or the suite that covers `advanceStory`).

## Notes

Filed from 2026-10-17-review-and-apply-a-story-s. Until this lands, the revision doc tells
operators to prefer `accept`/`accept_as`.
