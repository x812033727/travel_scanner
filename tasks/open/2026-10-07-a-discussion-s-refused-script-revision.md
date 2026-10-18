---
id: 2026-10-07-a-discussion-s-refused-script-revision
title: A discussion's refused script revision leaves its lexicon terms behind
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T03:20:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/discuss.mjs
  - tools/video/automation/discuss.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# A discussion's refused script revision leaves its lexicon terms behind

## Why

When the owner discusses a screenplay, the writer can answer with a revised video.json, and
`discuss.mjs` hands that revision to `Automation.saveAndLint`. Each attempt writes video.json and
merges the answer's `lexicon_additions` into `docs/videos/lexicon.json` (`flow.mjs`, `mergeLexicon`
right after `writeVideo`).

If lint still refuses the revision after its fixes, or a STOP or a lost lease interrupts the fixes,
`discuss.mjs` puts the last good video.json back with `restoreVideo`. The lexicon terms that the
refused revision added stay in the shared lexicon, and `auto.json`'s `lexicon_added`
keeps them as well. Every video's pronunciation reads the lexicon, so a term from a script nobody
kept can change how other videos are spoken.

This was found during the 2026-10-07 code review of the lease gaps. It is older than that change.

## Definition of done

- [ ] A refused or interrupted discussion revision leaves `lexicon.json` and `lexicon_added` exactly as they were before it, and a test shows it.
- [ ] A revision that is kept still merges its terms, as it does today.
- [ ] A term the same unit added for another reason is not removed.

## Steps

- [ ] Snapshot the lexicon bytes (or the added keys) before `saveAndLint`, and restore them on the refused and interrupted paths, under the same lease check as `restoreVideo`.
- [ ] Run `node tools/video/long-form/cli.mjs check`. `flow.mjs` and `discuss.mjs` are bound, so an independent reviewer adds an increment.

## How to verify

```bash
node --test tools/video/automation/discuss.test.mjs tools/video/automation/automation.test.mjs
npm run test:tools
```

## Notes

- `restoreVideo` uses `fence(..., { stop: false })`: a STOP never keeps the last good script from going back. The lexicon restore should behave the same way.
