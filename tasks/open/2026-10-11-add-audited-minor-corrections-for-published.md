---
id: 2026-10-11-add-audited-minor-corrections-for-published
title: Add audited minor corrections for published news
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-11T06:48:12Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/service.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/app/news_automation/backfill_cli.py
  - apps/api/tests/test_news_automation.py
---

# Add audited minor corrections for published news

## Why

Published news may need a small source-backed correction. The native news
reverify, retry, reopen and judge routes all exclude published candidates.
The pipeline also refuses saving any locale with a published version. Generic
Guide draft/publication operations retain article history but do not qualify
new news documents through verification, five locale reviews and final JEV.

Securitize candidate `e4d83c5d-19a1-43b2-9876-f1cfe7dff448`, article
`21f79632-da3e-43db-864d-1e1343022cb3`, is published in five locales at version4.
TW/CN/EN/KO explain Jump Trading's provision of liquidity as ensuring willing
counterparties or smooth execution, beyond the stored CoinDesk source. A
minimal local correction is prepared; the public wording remains unchanged.
The earlier published Bitmine attribution task needs the same safe route.

## Definition of done

- [ ] An explicitly selected published candidate accepts a minor correction
  with exact source, evidence, article/version/document and complete-history CAS.
- [ ] Genuine editor revisions and audit provenance retain the original public
  documents while the corrected five-language draft passes fresh news gates.
- [ ] Publication requires the corrected fingerprints, current evidence,
  locale/final editor/JEV decisions and an atomic five-language commit.
- [ ] Original history, rewrite caps and unknown requests remain preserved;
  a proposed or saved correction is never reported as publicly applied.

## Steps

- [ ] Add an explicit correction request instead of changing status directly
  or borrowing a previous publication approval.
- [ ] Add a narrowly qualified save path for corrected published articles,
  preserving existing published pointers during review and the ordinary
  refusal for unrelated pipeline writes.
- [ ] Run corrected drafts through normal fact, locale, hard-policy, final
  editor and JEV checks; preserve missing-asset or changed-evidence holds.
- [ ] Publish and verify actual public API/HTML documents after native success.

## How to verify

Test exact version/document/source/history drift, concurrent work, an uncertain
or repeated operation, native actor/revision/audit joins, retained public
pointers before review, stale-approval refusal and atomic publication rollback.
Run the focused news tests and API Ruff/mypy checks. A separately guarded
production pilot must read persisted history and every public locale; local
tests, queued checks and a model answer do not prove public correction.

## Notes

- Independent actual Secure content review:
  `next15-normal-secure-post1212-five-content-independent-review-v2.json`,
  SHA256 `bc99013f4adf7a9814c9a0ba8959bf4852af07a675151b8cf37375b6d76d4d14`.
  A second independent package review identified the same residual Korean
  assurance at `/blocks/4/text` and `/blocks/9/rows/2/0`; the new local proposal
  adds those two fields without changing Japanese.
- Read-only native-route feasibility:
  `securitize-minor-postpublication-correction-route-readonly-feasibility-v2.json`,
  SHA256 `dd9e42547b6789de32085f115e26e4daedbab50bc02964d061dbfc72d68c9974`.
- Evidence root: `<home>\.codex\news-review\20261010-6f71`.
- `report_major_error` disables the whole vertical and records a major safety
  incident; it is unsuitable for this wording correction. No major-error
  incident, direct status edit, source extension or generic publication bypass
  has been performed.
- The related existing task is
  `2026-10-10-correct-published-bitmine-sole-outlet-attribution`.
  This new implementation task remains unclaimed while the held-bundle
  ingestion task uses the same exact code paths. The user's scope exception
  authorizes only that ingestion task's news test file, not a foreign release.
