---
id: 2026-10-19-read-a-translator-answer-whose-draft
title: Read a translator answer whose draft and final each closed one brace early
status: done
priority: P2
area: tools
owner: claude-opus-5-5-translator-brace
claimed_at: 2026-10-19T05:00:26Z
created_at: 2026-10-19T05:00:22Z
completed_at: 2026-10-19T05:02:50Z
branch:
depends_on: []
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Read a translator answer whose draft and final each closed one brace early

## Why

On 2026-10-19 the ko translator of `story-adapt-michelin-guide-stars` (part 8 of 8) answered four
times running with `{"draft":{…}}},"critique":[…],"final":{…}}}}`: the draft and the final each
closed one brace too many. `parseObject` in `tools/video/automation/prompts.mjs` mended only the
first early close, so the second made the whole mend fail; the first object alone (a draft) was
taken, `finalAnswer` refused it as a draft that skipped its critique, and the video blocked.

## Definition of done

- [x] An answer whose objects close early more than once is read whole when a next key follows
      each early close; anything else still falls back to the first object.
- [x] A test with the translator's shape.
- [x] Independent DURATION_ONLY increment for `prompts.mjs` in the long-form review receipt.

## How to verify

```bash
node --test tools/video/automation/prompts.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

- Claimed with `--force` (owner's choice, 2026-10-19): `prompts.mjs` is also in the scope of
  2026-10-14-ai-and-tech-videos-tell-one; this change touches only the JSON mending in
  `parseObject`.
