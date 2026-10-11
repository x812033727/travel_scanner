---
id: 2026-10-11-recover-ai-agent-control-story-after
title: Recover AI agent control story after audited category correction
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-10-11T08:59:05Z
completed_at:
branch:
depends_on:
  - 2026-10-10-add-audited-held-news-category-correction
scope:
  - docs/news-agent-control-recovery-2026-10-11.md
---

# Recover AI agent control story after audited category correction

## Why

Original208 candidate 28289a1b-5b85-4cb0-8fee-92beef07250f is the Decrypt
story "AI Agents Keep Escaping Their Creators' Control—Here's What We Know".
The native read-only capture at 2026-10-11 08:55:06 UTC shows failed,
news_judge_approved, retry8, no Guide, one stored Evidence, a zh-TW-only cache
and no live job. Its prior translation failure was an English summary item
of 308 characters against the 300-character limit, not the description.

The candidate also inherits crypto from its fixed Decrypt feed. The full
stored article does discuss crypto's financial incentives, a Bitcoin security
group and Bitcoin quantum defenses; crypto is a real secondary angle. Its
headline, publisher section and main incidents concern AI control, so this
recovery recommends AI as the primary category. This is an editorial judgment,
not a claim that the source contains no crypto or that a model approved a
category change. Native save derives GuideTopic from candidate.vertical.
Use the dependent audited category route before ingestion or reverify so the
saved topic reflects that decision. A local draft is not a persisted correction.

## Definition of done

- [ ] The explicitly selected held candidate has a genuine audited category
      correction, preserving source, Evidence, cache, retry and capped history.
- [ ] Five complete drafts accurately attribute the dated tests and reports,
      pass the corrected category's native schema/policy checks, and receive
      an independent full-content review before native ingestion.
- [ ] Fresh full-state CAS, one native save and its independent readback precede
      the ordinary verification, locale, final-source and judge checks.
- [ ] Actual publication has five-locale public verification, or a specific
      remaining blocker is documented without repeated provider requests.

## Steps

- [ ] Read the preserved native snapshot and local author package; distinguish
      controlled tests, third-party tests and reported sandbox incidents.
- [ ] After the dependent category operation is available, verify its real
      actor audit and complete unchanged history before preparing a new bundle.
- [ ] Independently review all five documents under AI policy, then use the
      deployed native no-Guide ingestion and original verification route once.

## How to verify

Use native --capture-ingestion-state before any write. Pin the actual snapshot,
documents, complete Evidence and truthful independent draft review. Validate
the exact native dry-run contract; inspect durable intent, actor audit,
revisions, cache and RQ after the single save and verification operation.
Check every published locale's API document/version and page H1/canonical.
Unknown commit or enqueue acknowledgement requires readback, never replay.

## Notes

Evidence root: <home>/.codex/news-review/20261010-6f71.
agents-control-native-content-state-v1.json SHA256
290522c87bf99efa4a0fa3c568f0e74ed5ce0cb42c63a4f92d4cf9a35d40a9d5,
native state ba27f4c7014e560ba0e8516ef6b6924f94aceb5b12fe8a122b2c68ef202334e9.
The original category remains crypto; Root has not changed the candidate,
source, cache or any history. Preserve the two lifetime judge rewrites.
No native draft save, paid verification or publication has been attempted
for this candidate during this recovery step. Local content preparation is
separate from the dependent category implementation and its acceptance.

2026-10-11 local draft preparation: agents-control-reviewable-five-v1/manifest.json
SHA256 6ba73ab47a56a9f28f75a9ed3fc630efd1a073c15a0499695f8dcadf6afb8a68
contains all five owner proposals, with 11 narrow zh-TW leaf corrections and
complete en/zh-CN/ja/ko translations. Native Guide/write checks pass against
the unchanged current crypto policy, with noHero pending. This does not approve
the AI primary category. Maximum summary item length is233, description248;
no schema-length workaround or source content was added.
The separate primary-category analysis ce6193c3581ccb7315c9292b0ad6bd7db15150d7b236003642cdbd47d62bc620
retains the real crypto secondary material and records that the native pure
classifier returns ai for the exact stored body. Independent full-content
review is pending. All existing source, cache, counter and model history are
preserved; neither native save nor a provider job has been attempted.

2026-10-11 09:08 UTC: independent full-content v1 review a940029a found one
Traditional Chinese FAQ leaf containing Simplified characters. The immutable
v2 successor changes only that leaf from 据此证明 to 據此證明; v1 is retained,
and all other locale documents, complete Evidence, claim ledger, cache and
history bytes are unchanged. v2 manifest SHA256
48158febf0fe6a58c11e0480216b360879b3dfbc372a8b76d56afe9a164d2c45.
Actual independent full-content v2 review at09:08:26 UTC has SHA256
86a469c6d0328a9a8ab55c6489f493038dd9aa4ae51c4e3ee7fd7c717f6a31d2;
it reviewed95blocks/25table rows/20FAQ, full stored Evidence and13 claim items,
and preserved48runs/36assessments. The five proposals pass the current crypto
policy except noHero; this is draft-ingestion-only review, not audited AI
category correction, current ingestion readiness or publication approval.
The category dependency remains open. No native save or provider call.
