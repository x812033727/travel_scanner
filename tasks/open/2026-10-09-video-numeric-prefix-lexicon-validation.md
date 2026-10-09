---
id: 2026-10-09-video-numeric-prefix-lexicon-validation
title: Handle valid numeric-prefix video lexicon terms without blocking unrelated films
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-09T14:16:21Z
completed_at:
branch: codex/stalled-video-reviewed-fixes-20261008
depends_on: []
scope:
  - tools/video/core/lexicon.mjs
  - tools/video/core/lexicon.test.mjs
---

# Handle valid numeric-prefix video lexicon terms without blocking unrelated films

## Why

The production shared dictionary contains `8B: "八 B"`, while validateLexicon
requires every key to start with a Latin letter. Consequently normal lint and
the dub CLI reject an unrelated approved Travel film that contains no such term.
The existing substitution matcher accepts a whole-word 8B alias, and the Latin
term scanner sees only its B suffix. These contracts need one deliberate rule.

## Definition of done

- [ ] Establish and document consistent validation, detection and substitution
      for numeric-prefix terms such as 8B; retain rejection of invalid keys.
- [ ] Normal lint accepts a valid dictionary on a film that does not use 8B.
- [ ] Actual 8B narration receives its intended alias without altering unrelated
      words, line identities, or unused-term speech hashes.
- [ ] Regression coverage includes an actual numeric-prefix use, an unrelated
      film, malformed keys and unchanged ordinary acronym behavior.

## Steps

- [ ] Read the existing term grammar and choose one consistent public contract.
- [ ] Implement and test within the two-file scope. Coordinate separate ownership
      before changing any shared dictionary or film source.

## How to verify

Run `node --test tools/video/core/lexicon.test.mjs` and the affected narration,
timeline and lint checks. Use the unchanged Travel source with the captured
actual shared dictionary to reproduce the unrelated-film failure, and compare
normal speech hash and complete request objects before and after the fix.

## Notes

- Actual 2026-10-09 14:01:23 UTC production HEAD c2a153ab406714bbc5c8fa00b10f38f8a9af38e9;
  shared lexicon SHA f7a50da50b619512a04215c856eb95387578554e7bada80aac13ee5fa83ad84a.
  The sole lint error is lexicon.terms.8B: a term starts with a Latin letter.
- Evidence lives outside Git under
  `C:/Users/x8120/mokaair-work/stalled-video-audit-20261008/overnight-20261009/dubs-selected/`:
  `actual-Travel-8B-global-lexicon-current-readonly.jsonl`,
  `actual-Travel-current-frozen-normal-lint-readonly.jsonl`, and
  `actual-Travel-private-unused8B-full-normal-lint-and-three-quotes-v3.jsonl`.
- A tightly bound private input view removed only this proven-unused term for
  the retained Travel production. The complete project, speech hash, translation
  context and every full request/key/body remain equal except the explicit unused
  lexicon entry. All normal lint and three normal GET-only dub quotes passed.
  This workaround does not fix the shared validation contract.
- Preserve the original shared dictionary: other films may use 8B. No production
  tool, setting, source, cap, provider result, deployment or approval was changed
  while recording this follow-up.
