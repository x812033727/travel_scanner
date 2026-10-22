---
id: 2026-10-22-research-c13-victorinox-treatment
title: Research and draft C13 Victorinox everyday reversal treatment
status: review
priority: P2
area: docs
owner: codex-root
claimed_at: 2026-10-22T15:31:42Z
created_at: 2026-10-22T15:31:19Z
completed_at:
branch: codex/brand-story-victorinox-c13-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-victorinox-c13/treatment.md
  - docs/videos/story-everyday-victorinox-c13/source-matrix.md
---

# Research and draft C13 Victorinox everyday reversal treatment

## Why

The C13 series card asks what Victorinox sold after airlines restricted pocketknives. Its watch and travel-gear lines predate 2001, while the only direct 2002 category figures located are for the separate U.S. distributor SABI. A source-bound treatment must preserve those chronology and reporting-entity limits before any script is drafted.

## Definition of done

- [x] Six-chapter, hook-led Treatment and claim-by-claim source matrix exist under the scoped C13 folder.
- [x] The treatment distinguishes Victorinox AG from SABI and avoids inventing post-9/11 watch/travel launches or sales recovery.
- [ ] A different agent reopens the sources and signs M01–M13 against the final hashes; owner then decides whether to adopt the Treatment.

## Steps

- [x] Check local/remote branches, existing PRs and the 20-episode plan for C13 ownership.
- [x] Read Victorinox history, the July 2001 SABI 8-K, 2001 10-K, 2002 Q2 10-Q, contemporary Swissinfo report and CEO interviews.
- [x] Draft one causal line and six chapters, with chronology, entity scope, visual limits and editorial caveats.
- [ ] Obtain independent Treatment/source-matrix review bound to the final SHA-256 values.
- [ ] Leave a draft no-auto-merge PR for owner review and mark this task review/done as appropriate.

## How to verify

Check `git diff --check`, exact SHA-256 of `treatment.md` and `source-matrix.md`, the independent M01–M13 receipt, and PR head readback. No paid generation is within this ticket.

## Notes

The first-hand Swiss Army Brands filing is for the U.S. marketing/distribution company, not a consolidated Victorinox AG report. Its 2002 Q2 knife/tool −34%, watch +7%, professional cutlery +16% figures have that narrow denominator. Two contemporary Swissinfo reports disagree on whether an approximately 30% Victorinox knife-sales fall covered only October 2001 or the full fourth quarter; the revision surfaces the conflict and does not use a single denominator as fact. The 1989 watch and 1999 licensed travel-gear milestones precede 9/11. A later CEO interview attributes relief to existing watches and kitchen/professional knives and recounts temporary employee lending; employee counts vary by retrospective account, so the proposed narration omits a number. C13 must not inherit C03–C06 paid approvals.

2026-10-22: Draft PR https://github.com/x812033727/travel_scanner/pull/1693 targets the source series-plan branch; it has `no-auto-merge`. Treatment SHA-256 `2936F4A2F2426E483B261F75411E88075A60606AF73B34609397AED5FB395ABE`, matrix SHA-256 `3750387A5183E88AB1B4FC6746782DF8E4C6974338DE55B98B2A5AE43BC81767`. `git diff --cached --check` passed; `npm run check:tasks` validated 2,075 task files with existing unrelated warnings. Independent source review and owner Treatment approval remain outstanding.

2026-10-23: Independent first review at PR head `259164cc9` held M05 because the direct Camenzin interview and later agency report disagree on the 30% time window. Revised Treatment SHA-256 `25401671F26EF052B519A6E27A4624D1AB2286CDDFDECD38707D91432DCCDAC4`; matrix SHA-256 `D6DA3BA8676876645D058A634DBA1D86230D2FA0FB80CA65584A7AEBA5C4B30C`. Fresh independent delta and owner adoption pending.

During delta review, the reviewer flagged two residual wording mismatches before signing: S10 should preserve Camenzin's contrast between broader buying/recession effects and new security measures as his own view; M09's products and brochure have different reported statuses, rather than all being trials. Narrowed both. Current Treatment SHA-256 `A4A47F06F52490B4044267405445F31AC31EF7FB2C19575D59511D5BE0C57F20`; matrix SHA-256 `295A7793DE618FEF714FA530F78592527EF77E82BAA38EE5594745B8386641D1`. Final independent delta and owner adoption still pending.
