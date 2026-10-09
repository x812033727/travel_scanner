---
id: 2026-10-08-audit-next-web-design-locales-source
title: Audit next web design locale candidates and source drift
status: done
priority: P1
area: docs
owner: codex-gpt6-root-source-audit
claimed_at: 2026-10-09T12:22:33Z
created_at: 2026-10-08T02:00:12Z
completed_at: 2026-10-09T13:06:47Z
branch: codex/article-source-audit-wave6-20261009
depends_on: []
scope:
  - docs/article-localization/handoffs/wave6-source-audit-candidates-20261008.md
---

# Audit next web design locale candidates and source drift

## Why

The all-missing-language program has more unpublished work after the completed
32-article release and the reviewed drafts in PR #1374 and PR #1378. A read-only
screen of the October 7 17:44 UTC snapshot identified twelve possible next sources,
four repository/published-source differences and five possible ordinary-word
links to an unrelated AI glossary. These require formal source audit before any
new translations. No selected source has been edited or independently approved.

## Definition of done

- [x] Fresh source and cross-worktree/remote/PR checks establish an eligible cohort.
- [x] Full source text, native media and current primary facts are independently read,
      with retrieval and HTTP-verification limits explicitly recorded.
- [x] All eight current source differences are explained against exact published versions.
- [x] Five further glossary mislinks are confirmed with exact pointers.
- [x] Proposed corrections assign distinct proposal/application/final-review actors;
      this audit grants no SOURCE PASS before actual application and final review.
- [x] A sanitized independently reviewed handoff records decisions and hashes;
      separate narrow authoring task is filed and must be claimed before pack/job work.

## Steps

- [x] Inspect the external candidate proposal and historical source-date limitations.
- [x] Capture fresh live source state and inspect all current competing scopes.
- [x] Audit sources and explain drift before SOURCE admission or authoring.
- [x] Consider the five already-authored local packs for independent review first,
      avoiding duplicate translation where their exact current content is reusable.
- [x] Record a justified selection and formal correction needs in the handoff.

## How to verify

Use article-localization and content-pipeline. This task owns only its audit
handoff, not packs, media, provider jobs or production settings. Do not infer
publication from five local locales or turn this screen into a PASS review.
Authoring requires a separate exact scope and normal claim after source approval.

## Notes

External candidate proposal SHA256:
`5b34b5c452abde90a7ecd284d1accbb8a3979f564ee87b410cc2f62e47943f7c`.
Read-only handoff receipt SHA256:
`aa843a7c0326e4a03fe1a32be29e1527e8237a59770f316203b32e0db07eb7f9`.
All inputs remain in the owner's persistent evidence store outside Git. The screen
uses the snapshot captured `2026-10-07T17:44:18.665109+00:00` and historical
`checked_on` dates of September 14; it is not current publication/ownership proof.

Candidates: design-thinking-practice, portfolio-case-study, brand-identity-logo-brief,
web-design-agency-brief, website-404-recovery, website-www-subdomains,
ai-design-prompt-workflow, canva-design-workflow, customer-journey-funnel,
marketing-copywriting, seo-domain-authority and seo-trust-sensitive-topics.

Repository/source drift was observed in website-404-recovery, website-www-subdomains,
customer-journey-funnel and marketing-copywriting. Do not silently replace the
published source with the local pack. Possible ordinary 標記 to ai-term-token
mislinks occur in design-thinking-practice, web-design-agency-brief,
ai-design-prompt-workflow, canva-design-workflow and seo-trust-sensitive-topics.
These are unreviewed findings, not approved corrections. AI/Canva features, SEO
authority/YMYL claims, marketing claims and brand/licensing advice require current
primary-source checks and a cohort-fit decision based on that audit.

Five existing local five-locale packs are candidates for reviewing existing work:
paid-vs-organic-marketing, wordpress-blog-build, wordpress-comment-spam,
wordpress-performance-plugins and wordpress-reset-safely. Their old-snapshot
missing-public status is separate from local authoring; no language review or
public acceptance is inferred. Inventory SHA256:
`91a103c8b6d6cac39fa9cd6f740229f5b86c9426d0d6f0d215b96edb6267d64c`.

The historical local screen checked eleven immediate job roots and local active scopes;
fresh all-worktree, remote-head and paginated-PR ownership checks remain required.
No repository/task/job claim, translation-provider call, network or production
write occurred in the external screen. Its historical unclaimed state is superseded
by the current Root claim and audit results below.

## 2026-10-09 current checkpoint

The investigation and independently reviewed handoff are now complete. The narrow
follow-up `2026-10-09-localize-reviewed-web-design-wave6` was claimed successfully
after this audit finished. Its separate task records actual application and later
source admission; neither the earlier pending notes nor this audit imply SOURCE PASS.
Final independent proposal/handoff review SHA:
`e759638b4601759e88a30f355b9f136c7f8f11061de2a792d14635feec3514f5`.

- Approved previous release is complete: 57 total articles/228 new languages;
  the 13-article release records are in draft PR #1401, exact HEAD
  `79758f18cf39652a9f4d08dd764f0242f0735ece`, all 22 CI checks successful.
- Fresh current-runtime snapshot `ef3ef1cfeca66169cdb6f77499a2b3c4eec2230a805a46c08ab619203304c209`
  captured 2026-10-09 20:32 Asia/Taipei; actual SSH0, readonly, no retry or writes.
  Current census: 1,551 published scoped articles, 805 incomplete, 3,220 gaps.
- Independent integrity review `3444ab3cc59e6ce2de16422fa12e3685a1bf8853ba04c2a6c8eee0af57bfa6f8`
  verifies all 17 source guards unchanged and all prior 57/285 preserved.
- Current main provides explicit done/release evidence for all five historical
  claim groups; stale copies were not cleared. Paid source citation questions
  remain unfinished. Recheck actual ownership before any later content claim.
- Exact source differences now cover eight articles, including four existing
  reusable WordPress packs. Independent full source/native-media/primary facts
  review and exact-pointer source proposals are in progress; no SOURCE PASS,
  translation approval, correction application or publication is claimed.
- The scoped handoff records the exact 17 current version/hash guards and
  remaining gates. Source/body/date/image bytes are unchanged.
