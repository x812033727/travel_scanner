---
id: 2026-10-23-source-bound-c19-seven-bank-six
title: Source-bound C19 Seven Bank six-chapter Treatment
status: done
priority: P1
area: docs
owner: codex-root-c19
claimed_at: 2026-10-23T04:10:19Z
created_at: 2026-10-23T04:10:15Z
completed_at: 2026-10-23T05:55:11Z
branch: codex/brand-story-seven-bank-c19
depends_on: []
scope:
  - docs/videos/story-everyday-seven-bank-c19/treatment.md
  - docs/videos/story-everyday-seven-bank-c19/source-matrix.md
---

# Source-bound C19 Seven Bank six-chapter Treatment

## Why

The C19 slot in the approved 20-episode editorial plan had only a source entrance. Build an evidence-bound, six-chapter story about a retail group forming a licensed bank around an ATM network. Separate it from the false first-convenience-ATM claim and from the assumption that every customer fee is Seven Bank income.

## Definition of done

- [x] A six-chapter Treatment and claim-level source matrix exist for independent review.
- [x] Another agent reads the original issuer sources, records M01–M16 verdicts against exact file hashes, and the owner adopts the Treatment before script work.

## Steps

- [x] Read the 2001–2007 issuer timeline, the issuer's own 1999 competitor timeline, the 2001 launch release and 2002 inaugural disclosure, the 2010 annual report, the 2024 integrated report, and the 2005 renaming notice.
- [x] Draft one chronological cause-and-effect story with a narrow 45-second opening and six chapter budgets.
- [x] Commission independent source review and repair its two held Treatment claims.
- [x] Obtain an independent delta review of the repaired Treatment.
- [x] Record owner Treatment adoption; do not start a script on an unadopted Treatment.

## How to verify

- Open every S1–S7 URL and check M01–M16 directly against source text/table.
- Run `npm run check:tasks` and `git diff --check` in this worktree. Owner approval, script, media and release are separate gates.

## Notes

- Seven Bank's own ATM anniversary timeline names Sakura Bank/am-pm and E-net in 1999. No first-in-Japan framing.
- Corporate history separates IY Bank founding (2001-04-10), bank license (04-25), bank opening (05-07) and ATM launch (05-15). It changes name only in 2005.
- The retrospective ATM page groups transfers under May 2001, while the dated corporate timeline starts money transfers on June 18. Use the latter precise date in any script.
- 2010 annual report separates customer ATM transaction fees set by partner institutions from ATM usage fees paid to Seven Bank. Its ATM fee income and placement expense are two dated line items, not profit per machine.
- 2024 integrated report gives later +Connect and cash top-up context; do not backdate them into 2001.
- The 2001 issuer release gives first-day 66 machines at 59 Tokyo sites; the inaugural 2002 disclosure already separates the bank's own account services from its partner-ATM business. These contemporaneous documents make the initial business model concrete without claiming the license was the only possible route.
- Independent review PR #1736 passed M01–M16 and held two Treatment statements: S6 did not explain why the group chose a licensed bank over a partner ATM operator; 2010 fee data did not prove it financed the 2001–2007 rollout. The revised Treatment asks what the bank actually did, and places the dated fee/cost figures after the rollout. Await exact-byte delta review before owner adoption.
- Delta review PR #1738 passed T01/T02 at author head `68bcebdae`; a following one-line title chronology refinement was published at `eb34fb007`. The owner adopted that current treatment and source matrix on 2026-10-23; exact hashes and limits are in `reviews/owner-treatment-approval-20261023.md`.
