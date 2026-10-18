---
id: 2026-10-11-recover-two-verge-held-stories-after
title: Recover two Verge held stories after audited navigation repair
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-10-11T10:19:34Z
completed_at:
branch:
depends_on:
  - 2026-10-10-add-audited-repair-for-legacy-navigation
  - 2026-10-11-add-audited-correction-for-obsolete-held
scope:
  - docs/news-verge-held-navigation-recovery-2026-10-11.md
---

# Recover two Verge held stories after audited navigation repair

## Why

Two unpublished existing Guides need editorial corrections and an audited
resolution of retained system navigation Evidence before normal review:
Sanders proposal candidate `0c72c4f4-500d-45f6-9bc4-d08f7c531bea` and Meta
glasses candidate `ddf85a1f-84b9-4eec-8481-5eb0a94e0157`. Their actual primary
stories returned200 and matched native stored hashes, but three retained
Verge listing pages each returned200 with genuinely changed body hashes.
A readable listing does not become reporting evidence for a particular story.

## Definition of done

- [ ] Qualify each exact retained URL as authored evidence or system navigation
      from complete stored/current bodies and all saved Guide references.
- [ ] Save only independently reviewed text through genuine Guide revisions.
- [ ] After the dependency is deployed, apply its audited correction to exactly
      these unpublished CIDs with fresh whole-state CAS and inactive queues.
- [ ] Run the ordinary AI fact/locale/judge and current-source gates once; retain
      actual final decisions and verify every published locale publicly.

## Steps

- [x] Capture full twelve-group native states and all five stored Guide drafts.
- [x] Read primary and every secondary URL using native SafeNewsFetcher only.
- [ ] Complete exact text and source-reference correction review/save receipts.
- [ ] Qualify navigation correction under the separate implementation contract.
- [ ] Reconcile native review outcomes, histories, sources, caps and public pages.

## How to verify

Use exact CID/URL/version/document/history fingerprints, genuine actor audit
and original native service readbacks. A Save, HTTP200, dispatch ACK or judge
proposal alone is not publication. Never delete Evidence rows manually,
substitute body hashes, weaken source qualification or replay uncertain work.

## Notes

Root evidence directory: `<home>/.codex/news-review/20261010-6f71`.
Complete-content index `held-defect-six-native-content-readonly-index-v1.json`
SHA256 be2f56298a9e5e0b84b71a98b0e559f919d7a19f6770e7b5de80e50eabecc221.
All-secondary index `held-defect-six-secondary-native-current-source-readonly-index-v1.json`
SHA256 dec816e5e124d14680b6436e74ec1485e9e4d8e9771f6a1d99be177d50de643e.
Sanders changed `https://www.theverge.com/news`, `/policy`, and
`/ai-artificial-intelligence`; glasses changed `/tech`, `/gadgets`, and
`/ai-artificial-intelligence`. Author-profile pages remained readable and
native-same; this does not qualify profiles as reporting evidence.
All six changed listing bodies are actually retained in nativeRO receipts,
with no production mutation/model/queue call. This follow-up does not itself
authorize a navigation-row deletion or broaden the original208 cohort.


2026-10-11 18:55 Taipei: full historical-ledger review found an additional
blocker. Sanders claim12 and Glasses claim14 still cite selected navigation
for assertions removed from the corrected Guides. Native navigation removal
must refuse any ledger citation. The newly recorded audited-ledger capability
is a separate dependency; deploying navigation repair alone cannot clear
these stories. Existing full claims/Evidence/source roles/caps remain unchanged.
Both five-locale draft corrections reported native Save1->2 once at10:51/52Z;
complete independent post-save readback is pending, not normal review or publication.
