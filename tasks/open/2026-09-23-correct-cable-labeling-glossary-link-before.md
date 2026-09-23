---
id: 2026-09-23-correct-cable-labeling-glossary-link-before
title: Correct cable labeling glossary link before localization
status: in-progress
priority: P1
area: api
owner: codex-cable-source-correction
claimed_at: 2026-09-23T11:02:46Z
created_at: 2026-09-23T10:40:33Z
completed_at:
branch: codex/fix-cable-label-glossary-link
depends_on: []
scope:
  - apps/api/app/guides/content/desk-cable-charging-organization.json
---

# Correct the unrelated Token link in the desk-cable source before batch021 translation

This open follow-up records a source-link defect discovered during batch021 inventory. The other two inventory candidates can proceed independently; this article needs a corrected, rechecked source baseline.

## Problem

The currently published zh-TW source has `/blocks/2/inlines/1` equal to `{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}`. Here「標記」means labeling a physical cable after tracing its endpoints. Linking that word to an AI Token article changes the intended meaning and should not be copied into four translations.

## Definition of done

- [ ] Re-export the exact published article and all its locale rows before correction; compare the full current draft, published and latest models against the pinned source. Stop on a concurrent edit, visibility change or unexpected locale row.
- [ ] Prefer the smallest correction: replace this one ArticleInline with the TextInline `{"type":"text","text":"標記"}`. Use another article target only if its relevance and actual publication are independently verified. Keep the visible word unchanged.
- [ ] Preserve every other body field, title, image, credit, source URL, original `checked_on`, pack metadata and article state. Preserve the original snapshot/version evidence; never manually rewrite revision history or counters.
- [ ] Independently compare the corrected normalized source with the original, allowing only the one inline type/target change. Validate the pack and confirm the import/link processing will not recreate the unrelated link.
- [ ] Complete the source-correction PR/publication sequence using the existing revision services and fresh concurrency checks; preserve every historical revision.
- [ ] Re-export after the corrected source is actually published, verify draft/published/latest equality and new real versions, and pin that full source as the baseline before translating this article. Keep the old v1/v6 evidence as history.

## Evidence and verification

Exact repository baseline: `ea893f4c9bdb0f17c153ae2ade526a3ce2a2f164`.

Read-only three-article snapshot: `batch021-candidate-inventory/live-source-full-20260923T103546Z.json`, SHA-256 `9794e7d03a9ba11ced25f245d54f1be0f4c5d43b5304f02cea976831303ac590`. At capture, the cable article was active and published, article v1, zh-TW draft/published/latest v6, and the full normalized model equaled the repository source. No other locale rows existed.

Source/conflict receipt: `batch021-candidate-inventory/live-approval-20260923T103546Z.json`, SHA-256 `997f0a925c39dde398504aff705c51f74be30e976332aa272d2d83e9279ad391`.

The separate household-inventory candidate is article v2 / zh-TW v6; do not generalize the cable article's v1 to the whole batch. No article source, host file or database row was changed during inventory. This follow-up is recorded afterward; it is open and unclaimed.
