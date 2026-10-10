---
id: 2026-10-10-dictionary-merge-treats-constructor-and-tostring
title: Dictionary merge treats constructor and toString as already listed
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-10T08:24:41Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/story.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/story.test.mjs
---

# Dictionary merge treats constructor and toString as already listed

## Why

The video worker merges a writer's `lexicon_additions` into the shared pronunciation dictionary
(`mergeLexicon` in `tools/video/automation/flow.mjs`, `addTerms` in
`tools/video/automation/story.mjs`). Both skip a term that is already there with
`term in lexicon.terms`. The dictionary is a plain object read from JSON, so `in` is also true
for every name `Object.prototype` has: `constructor`, `toString`, `valueOf`, `hasOwnProperty`,
`isPrototypeOf`, `toLocaleString`, `propertyIsEnumerable`.

Lint asks the other way (`isKnownTerm` in `tools/video/core/lexicon.mjs` uses `Object.hasOwn`),
so a narration that says one of those words (a programming tutorial that says "constructor") has
an unknown term, the writer's proposal for it is dropped as if it were listed, and the lint fix
can only reword the line. Three fixes that keep the word end the draft with
`blocked — lint still fails after 3 fixes`.

Unlike `2026-10-10-stop-the-video-worker-merging-dictionary`, nothing is written to the
dictionary, so only the one video is affected. Found while reading the merge for that task; not
seen on the host.

## Definition of done

- [ ] A writer's proposal for `constructor` (and the other inherited names) is merged when the
  dictionary does not list it, through both merge functions.
- [ ] A term the dictionary does list is still left as it is.

## Steps

- [ ] Ask `Object.hasOwn(lexicon.terms, term)` in both merge functions (or share the whole
  merge from `tools/video/core/lexicon.mjs`, beside `isProposableTerm`).
- [ ] A case in `automation.test.mjs` and in `story.test.mjs`: a line that says "constructor",
  proposed with null, passes lint.
- [ ] `flow.mjs` and `automation.test.mjs` are bound by the duration review
  (`docs/videos/long-form/review.json`): an independent reviewer rebinds them.

## How to verify

```bash
node --test tools/video/core/lexicon.test.mjs tools/video/automation/story.test.mjs
node --test --test-name-pattern="dictionary" tools/video/automation/automation.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

- `__proto__` cannot be proposed: `isProposableTerm` wants a Latin letter first.
