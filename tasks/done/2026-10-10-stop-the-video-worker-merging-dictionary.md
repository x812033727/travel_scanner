---
id: 2026-10-10-stop-the-video-worker-merging-dictionary
title: Stop the video worker merging dictionary terms lint will refuse
status: done
priority: P1
area: tools
owner: claude-opus-5-5-lexicon-merge-fix
claimed_at: 2026-10-10T08:19:39Z
created_at: 2026-10-10T08:19:33Z
completed_at: 2026-10-10T08:36:32Z
branch: claude/lexicon-merge-letter-first
depends_on: []
scope:
  - tools/video/core/lexicon.mjs
  - tools/video/core/lexicon.test.mjs
  - tools/video/core/fixtures/load.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/story.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/story.test.mjs
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Stop the video worker merging dictionary terms lint will refuse

## Why

Every video shares one pronunciation dictionary, `docs/videos/lexicon.json`. A script writer may
propose terms for it (`lexicon_additions`), and the worker merges them: `mergeLexicon` in
`tools/video/automation/flow.mjs` for a tutorial, a drama and an episode, `addTerms` in
`tools/video/automation/story.mjs` for a brand story's chapters. Both took a term that matched
`/^[A-Za-z0-9][A-Za-z0-9.+#'_-]{0,39}$/`, which lets a term start with a digit.

The dictionary's own check, `validateLexicon` in `tools/video/core/lexicon.mjs`, refuses a term
that does not start with a Latin letter, and lint reports that for every video, because the file
is shared: `lexicon.terms.8B: a term starts with a Latin letter`.

On 2026-10-09 a writer on the production host proposed `8B` and the merge took it. From then on
no video on the host passed lint. The worker's three lint fixes could not help: a fix round can
add terms and reword lines, and nothing removes an entry. Four drafts in a row ended
`blocked — lint still fails after 3 fixes`: 2026-10-09 11:42Z, 17:48Z, 23:50Z and 2026-10-10
05:54Z. A later writer added `6abc` the same way. One bad proposal blocked every later video.

## Definition of done

- [x] A proposed term the dictionary's check would refuse is left out of the dictionary by both
  merge functions, like any other unusable proposal; `{ "8B": null, "6abc": null, "Ai2": null }`
  merges `Ai2` alone and the dictionary still passes `validateLexicon`.
- [x] The merge and the check ask one function about a term's first character, so they cannot
  disagree again.
- [x] The merge's own limits are as they were: 40 characters of letters, digits and
  `. + # ' _ -`, a spoken form of 80 characters at most, a listed term left alone.
- [x] A refused proposal blocks nothing: a word the narration still says that lint does not know
  is that line's ordinary error and goes back to the writer.
- [x] No code rewrites a dictionary that already holds such an entry, and the repository's
  `docs/videos/lexicon.json` is untouched.
- [ ] The host's dictionary has `8B` and `6abc` removed and the four blocked drafts are retried
  (the owner, on the host; see Notes).
- [ ] The duration receipt is rebound by an independent reviewer (see Notes).

## Steps

- [x] `isValidTerm` in `core/lexicon.mjs`, used by `validateLexicon`; `isProposableTerm` (that,
  within the worker's limits), used by `mergeLexicon` and `addTerms`.
- [x] Look for a third writer of the dictionary: there is none. `anime-write.mjs` gathers the
  acts' `lexicon_additions` into the answer `saveAndLint` hands to `mergeLexicon`;
  `dubs/plan.mjs` and `production/audio-contract.mjs` build objects of their own;
  `ops/video/sync-docs.mjs` seeds the file once and never writes a term;
  `docs/videos/imported-long-languages/prepare.mjs` adds a fixed list of names to a copy in its
  own output directory.
- [x] Tests: the two predicates and `validateLexicon` over one list of proposals
  (`lexiconProposals` in `core/fixtures/load.mjs`: every kind of first character, lengths around
  40, usable and unusable spoken forms); the same list and the 2026-10-09 proposal through
  `saveAndLint` (`automation.test.mjs`) and through a story's chapters (`story.test.mjs`).
- [x] Run the tests with the merge's old rule put back: all three files fail, the worker's with
  the host's own message (`lint still fails after 3 fixes: lexicon.terms.8B: a term starts with a
  Latin letter; lexicon.terms.6abc: …`).
- [ ] Rebind `docs/videos/long-form/review.json` and `review.md` (an independent reviewer).

## How to verify

```bash
node --test tools/video/core/lexicon.test.mjs tools/video/automation/story.test.mjs
node --test --test-name-pattern="dictionary term the writer proposes" tools/video/automation/automation.test.mjs
node --test tools/video/core/*.test.mjs tools/video/automation/automation.test.mjs tools/video/automation/story.test.mjs
node tools/video/long-form/cli.mjs check   # red for flow.mjs and automation.test.mjs until the receipt is rebound
```

## Notes

- What a writer sees after proposing `8B`: nothing. The proposal is dropped without a word, as
  `bad term!` always was, and it is not recorded in the video's `lexicon_added`. Lint reads the
  narration's `8B` as the single letter `B` (`latinTerms` starts a term at a letter), and a
  single letter needs no entry, so the script passes and no fix is asked for. The proposal was
  never needed.
- `6abc` is different: lint reads it as `abc`, which is unknown. With the proposal refused the
  writer gets the line's own error in `lint_errors`
  (`scenes[0].lines[0] (…): "abc" is not in docs/videos/lexicon.json: add how to say it, or null
  once it sounds right`) and answers by rewording or by proposing `abc`. That costs one of the
  three fix rounds of that video and touches no other video. For a story the error goes back
  for its chapter (`chapter idea fixed for 1 lint errors`).
- The prompts are unchanged. They ask for "every Latin-letter word" of the narration; a writer
  that proposes `8B` has misread that, and the worker now ignores it.
- **The host is still blocked until its dictionary is cleaned.** `lexicon.json` on the host
  belongs to the worker after its first seed (`ops/video/README.md`): a deploy does not replace
  it and this change does not repair it. Remove the two entries `8B` and `6abc` from the host's
  `docs/videos/lexicon.json` by hand, then retry the four blocked drafts (11:42Z, 17:48Z and
  23:50Z on 2026-10-09, 05:54Z on 2026-10-10) from /admin/videos. Deploy this change first, or
  the next proposal of the kind blocks the host again.
- A story met the same entry differently: its chapters are linted as a draft until the sixth is
  written, and only then does an error outside the chapters block it (`the merged story fails
  lint outside its chapters`).
- The receipt: `tools/video/automation/flow.mjs` and `tools/video/automation/automation.test.mjs`
  are bound by SHA-256 in `docs/videos/long-form/review.json`, so
  `node tools/video/long-form/cli.mjs check` reports both as stale and
  `tools/video/long-form/review.test.mjs` is red until a reviewer who is not the author rebinds
  them. The change is duration-neutral: it decides which proposed terms reach the dictionary and
  touches no length, target or budget. `core/lexicon.mjs`, `core/lexicon.test.mjs`,
  `core/fixtures/load.mjs`, `story.mjs` and `story.test.mjs` are not bound.
- Not changed: a dictionary entry may not start with a digit, though `isKnownTerm` would look
  one up for a part of a joined term (`4o` in `GPT-4o`); such a term is listed whole.
- Found on the way, filed as `2026-10-10-dictionary-merge-treats-constructor-and-tostring`: both
  merges test `term in lexicon.terms`, which is true for `constructor`, `toString` and the other
  names every object inherits, so a proposal for one of those words is dropped as already listed.
- `tools/video/core/project-lease.test.mjs` has two tests that fail on Windows only (a child
  process imports a module by a drive-letter path); `2026-10-07-make-project-lease-test-children-use`
  has it. Nothing here touches it.
