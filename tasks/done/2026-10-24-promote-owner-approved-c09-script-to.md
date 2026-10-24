---
id: 2026-10-24-promote-owner-approved-c09-script-to
title: Promote owner approved C09 script to guarded intake
status: done
priority: P1
area: tools
owner: codex-c09-v8-promotion
claimed_at: 2026-10-24T06:09:59Z
created_at: 2026-10-24T06:09:55Z
completed_at: 2026-10-24T06:11:05Z
branch: codex/c09-patagonia-script-repair-20261024
depends_on: []
scope:
  - docs/videos/brand-stories-everyday-reversals-20261020/approved-scripts.json
  - tools/video/review/script-intake.mjs
  - tools/video/review/script-intake.test.mjs
---

# Promote owner approved C09 script to guarded intake

## Why

The site script-intake allowlist contains eleven owner-approved scripts but
omits C09. Its approved v8 candidate is still isolated under `reviews/`,
while canonical `script.md` is the earlier 85-line version. Promote the exact
approved bytes and let the guarded intake validate C09 locally without a
backend write.

## Definition of done

- [x] Canonical C09 `script.md` matches the exact owner-approved v8 SHA-256
      `4445ad74bcafbac1dfca65392199fec89700c17ab8c01e665ac79dfffc1aa3f7`.
- [x] Approval manifest and intake allowlist accept exactly 77 C09 lines;
      altered bytes fail before any remote call.
- [x] Local dry-run lists C09 with `dry-run-local-only`; no backend mutation,
      paid media request, or worker run occurs.

## Steps

- [x] Recheck the frozen candidate, independent source/visual receipt, signed
      A/B blind reads, and owner approval; record A's dissent.
- [x] Copy the script without changing bytes and add an explicit approval
      receipt, leaving the old 85-line visual plan out of production.
- [x] Extend the manifest, allowlist and tests; run the local dry-run.

## How to verify

`Get-FileHash -Algorithm SHA256 docs/videos/story-everyday-patagonia-c09/script.md`;
`node tools/video/review/script-intake.mjs --id C09`;
`node --test tools/video/review/script-intake.test.mjs`;
`npm run check:tasks`; `git diff --check`.

## Notes

Owner approved the exact v8 script/visual direction in PR #1806 on
2026-10-24. Independent source and matched-visual review is 77/77 PASS.
Signed A read is 11/12 Yes (`natural_spoken=No` at c090302, c090401,
c090418); signed B is 12/12 Yes, so there is no common veto. The earlier
secondhand A 12/12 handoff is not the signed verdict. The frozen candidate
header still says unapproved, so `reviews/owner-v8-approval-20261024.md`
records the later owner approval without changing approved bytes. The old
85-line `visual-plan.md` must not be paired with the 77-line script.
Production project, actual voice duration and whole-film quote remain HOLD.
