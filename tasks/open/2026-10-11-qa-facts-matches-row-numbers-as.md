---
id: 2026-10-11-qa-facts-matches-row-numbers-as
title: QA facts: a verify report's row numbers are matched against claim ids
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T04:04:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/qa/facts.mjs
  - tools/video/qa/facts.test.mjs
---

# QA facts: a verify report's row numbers are matched against claim ids

## Why

The QA `facts` item (`tools/video/qa/facts.mjs`) reads the fact-checker's
`docs/videos/<slug>/verify-<round>.md`, takes every table row whose verdict is NOT FOUND, and
fails if a scene still cites that claim. It takes the row's **first cell** as the claim id
(`notFoundClaims`: `normalizeClaimId(cells[0])`, which strips a leading `c`), and compares it
with the ids the scenes list in `claims` (the c-numbers of `claims.md`). But a verify report
numbers its rows 1, 2, 3 in the order the checker went through the script; they are not claim
ids. On 2026-10-10 row 19 of `docs/videos/sothatswhy-b26/verify-1.md` (a detail in a card's
source line, NOT FOUND and already removed) was read as claim `c19`, an unrelated and confirmed
claim, and the item reported five scenes still citing a dropped claim. It was worked around by
rewording that row's verdict cell in the report.

## Definition of done

- [ ] The check matches a report's rows against claim ids only when the rows are claim ids
      (for example the first cell is `c<number>`, or the table's header names a claim column),
      and otherwise does not treat a bare row number as one; **or** the verifier prompt tells
      the checker to number rows by claim id and to put a row with no claim under a non-numeric
      label, and the check refuses a report that does not.
- [ ] A test with a report shaped like `sothatswhy-b26/verify-1.md`: row 19 NOT FOUND, scenes
      citing `c19`, no failure; and the existing true positive (a NOT FOUND claim id still
      cited) still fails.
- [ ] Reports already in the repository give the same verdict as before, except the false one.

## Steps

- [ ] Read how the three report shapes in `docs/videos/*/verify-*.md` label their first column
      before choosing.
- [ ] If the prompt route is chosen, widen the scope to the prompt file and its test.

## How to verify

`node --test tools/video/qa/facts.test.mjs`; `node tools/video/cli.mjs qa --slug sothatswhy-b26`
with the original wording of row 19 restored in a copy passes `facts`.

## Notes

- 2026-10-11 filed from ticket `2026-10-10-sothatswhy-minimax-images` (its Notes, item 3 of
  what B26 taught).
