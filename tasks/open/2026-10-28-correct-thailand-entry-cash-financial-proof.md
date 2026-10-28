---
id: 2026-10-28-correct-thailand-entry-cash-financial-proof
title: Correct Thailand entry cash financial proof wording
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-28T03:08:38Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/thailand-entry-2026-tdac.json
  - docs/article-localization/source-corrections/20261028-thailand-financial-proof
---

# Correct Thailand entry cash financial proof wording

## Why

The published zh-TW Thailand entry guide states at blocks/10/text that cash plus
a credit card's available limit suffices as financial proof. The cited BOCA page
read on 2026-10-28 explicitly says credit cards cannot be financial proof. This
shared live/repository body error blocks faithful four-language localization.

## Definition of done

- [ ] Independently verify the complete current source and the precise financial-proof correction against primary references.
- [ ] Preserve all unrelated source text, original media and the repository's separate description draft.
- [ ] Bind current source/draft/version hashes and exact corrected fields to a source-correction review.
- [ ] Obtain concrete approval and guarded backup/publication verification before changing the live source; only then prepare translations.

## Steps

- [ ] Recheck current source ownership and the original source-maintenance tasks before claiming overlapping files.
- [ ] Replace only the unsupported credit-card phrase with a reviewed cash/equivalent requirement; re-audit the complete source.
- [ ] Resolve live/repository description drift explicitly, without overwriting or silently publishing that separate draft.
- [ ] Publish the approved source correction through native guards and bind the later four-language wave to its new public hash.

## How to verify

Primary reference: [BOCA Thailand visa and entry information](https://www.boca.gov.tw/sp-foof-countrycp-03-24-dec45-02-1.html),
read 2026-10-28. The material statement is `信用卡無法作為財力證明`.
Current phrase: `（現金加可查額度的信用卡就夠）`.
Proposed minimal finding: `（應備足上述金額的現金或等值貨幣，信用卡不能作為財力證明）`.
This is a proposed correction, not a complete newly approved source or publication.

## Notes

Current public source content hash (after removing only transport envelope keys):
`33152685d587214c4980ff71f817297a73d8e8d76f5efa89d4218ec4020b2791`.
The current repository additionally differs at description; do not normalize it away.
The diagram lists numeric amounts without the credit-card claim and needs no inferred edit.
Full findings/captures remain in private retained October 28 intel-source evidence,
whose readiness SHA is `e3d621fc90d9b82c834cd658887ca7f204c5abb418347271bd14408eb3a692ff`.
The existing AIO description task does not cover this body correction. The already
approved seventeen-life-article release does not authorize this Thailand change.
Bangkok route admission is a separate later pipeline prerequisite, not proof the
live destination route is absent. Other entry claims still require current review.
