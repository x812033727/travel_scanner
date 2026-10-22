---
id: 2026-10-21-tutorial-promise-exemption-in-lint-evaluate
title: Tutorial promise exemption in lint: evaluate TOC patterns on the opening minus the promise sentence; anchor PROMISE_VERB
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-21T14:40:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
---

# Tutorial promise exemption in lint: evaluate TOC patterns on the opening minus the promise sentence; anchor PROMISE_VERB

## Why

PR #1643 let a tutorial's opening carry one promise sentence (teaching-flow.md §一) by skipping
the table-of-contents warning in `episodeScriptProblems` when `doc.category === "tutorial"`, a
`PROMISE_VERB` matches anywhere in the first 60 s, there is no ordinal run and no `SECTION_WORD`.
A code review of the PR (2026-10-21) found two leaks:

1. The flag suppresses the whole check, so a tutorial opening 「這集講 A、B，還有 C。看完你會學會
   四件事」 raises no warning although the list announcement is not the promise sentence.
2. `PROMISE_VERB`'s `能(?:用|做|寫|自己)` matches inside 可能用／不能用／可能做, so an opening with no
   promise can still be exempted.

Both files are bound by the duration receipt (`docs/videos/long-form/review.json`), so the fix
needs its own independent increment; that is why it was not folded into the review's other fixes
(`core/narrative.mjs`, unbound).

## Definition of done

- [ ] The TOC patterns (`OPENING_TOC`, `announcesList`, the ordinal runs) are evaluated on the opening
      with the one promise sentence removed (the first sentence matching `PROMISE_VERB`), so a list
      announcement beside the promise still warns.
- [ ] `PROMISE_VERB` does not match 可能用／不能用／可能做 (`(?<![可不])能…` or a deliverable noun).
- [ ] `lint.test.mjs` covers both: the two tutorial promises still pass, the mixed opening warns,
      the 可能用 opening warns.

## Steps

- [ ] Split the opening on sentence ends, find the promise sentence, lint the rest.
- [ ] Anchor the verb.
- [ ] Tests; then an independent reviewer records the increment in review.md / review.json.

## How to verify

`node --test tools/video/core/lint.test.mjs`; `node tools/video/long-form/cli.mjs check` after the
re-binding.

## Notes

Found by the review that gated the merge of PR #1643; the other three findings (global panel hash
invalidating saved story verdicts, PROGRESS_CARRIER accepting a bare question mark, no test on the
tutorial question keys) were fixed in that PR.
