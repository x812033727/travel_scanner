---
id: 2026-09-28-batch042-pair-b-source-editorial-followup
title: Review Batch042 Pair B source editorial structure
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T18:12:56Z
completed_at:
branch:
depends_on:
  - 2026-09-28-batch042-pair-b-install-reviewed-locales
scope:
  - apps/api/app/guides/content/technical-seo-checklist.json
  - apps/api/app/guides/content/seo-learning-roadmap.json
---

# Review Batch042 Pair B source editorial structure

## Why

Strict intake reports both original sources lack a first summary block. technical-seo-checklist also has two source self-references (limit one). The existing-article localization preserves the original source structure; these findings are visible and are not translation omissions.

## Definition of done

- [ ] Review the existing source's summary/self-reference structure as a distinct editorial change.
- [ ] If changing it, preserve facts and existing paragraphs and maintain all five editions consistently.
- [ ] Rerun strict intake, pack lint, independent review and content/image hash bindings after changes.
- [ ] Reconcile any accepted source change with live versions through the guarded release process.

## How to verify

Run strict intake and scoped pack lint for technical-seo-checklist, seo-learning-roadmap; verify full-text and numeric/source/audience parity. Refresh source and review receipts after any edit.

## Notes

Unclaimed follow-up. These inherited source findings do not negate hash-bound independent acceptance of the added translations. No automatic live source rewrite or publication is authorized by this task alone.
