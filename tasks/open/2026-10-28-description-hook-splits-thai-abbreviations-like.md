---
id: 2026-10-28-description-hook-splits-thai-abbreviations-like
title: Description hook splits Thai abbreviations like ค.ศ. as a sentence end
status: in-progress
priority: P2
area: tools
owner: claude-opus-curio-v2
claimed_at: 2026-10-28T10:37:52Z
created_at: 2026-10-28T08:07:07Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/metadata.test.mjs
---

# Description hook splits Thai abbreviations like ค.ศ. as a sentence end

## Why

`splitFirstSentence` in `tools/video/core/metadata.mjs` takes the description's first sentence as the
hook shown above the fold. Its terminator pattern treats any `.` followed by a space as a sentence end,
so a Thai description opening with "ค.ศ. 210 …" (Common Era, also พ.ศ. for the Buddhist era) gets a
hook of just "ค.ศ.". The curio-s04-v2 Thai translator worked around it by writing "ปี 210". The same
would hit Latin-script abbreviations such as "No. 5", "St. Paul" or "a.C." in es/pt.

## Definition of done

- [ ] A description that opens with "ค.ศ. 210 …" or "พ.ศ. 2300 …" keeps the whole first sentence as the hook.
- [ ] Ordinary sentence ends in every target locale still split where they did.

## Steps

- [ ] Skip a terminator when the text before it is a short dotted abbreviation (letters with dots,
  e.g. `ค.ศ.`, `พ.ศ.`, `a.C.`, `d.C.`) or a known title abbreviation.
- [ ] Tests in `tools/video/core/metadata.test.mjs` for Thai era abbreviations and an es/pt one.

## How to verify

`npm run test:tools`

## Notes

Found while translating curio-s04-v2 (th). The quote-aware fix from
`2026-10-27-description-hook-quote` lives in the same function.
