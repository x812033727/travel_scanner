---
id: 2026-09-28-batch043-pair-a-final-independent-review
title: Independently review final Batch043 Google language corrections
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-28T18:10:20Z
completed_at:
branch:
depends_on: []
scope:
  - docs/article-localization/batch043-pair-a-evidence.md
---

# Independently review final Batch043 Google language corrections

## Why

PR #952 adds Google ranking-history and Google Trends translations. After the original authors reached their usage limit, the coordinating reviewer applied 60 zh-CN wording corrections. The coordinator read the final text and checked images, but the applied correction set still needs a distinct final reviewer before repository localization acceptance. CI passed all nine checks at content head 25402931a5aa296341f8ea4f0e4b48ba92f126aa after a failed mobile-admin UI test passed its unchanged-head retry; this task-only commit requires fresh CI.

## Definition of done

- [ ] A reviewer distinct from both the original author and coordinating corrector reads the complete final documents against source, including all corrected wording.
- [ ] Verify exact final pack hashes and the corresponding localized image/document bindings in batch043-pair-a-evidence.md.
- [ ] Return an explicit acceptance or a precise correction list; do not silently edit article JSON or images within this review scope.
- [ ] If corrections are needed, assign a separate narrowly scoped application task and bind review to its final bytes.
- [ ] Record final independent acceptance in the evidence before promoting PR #952.

## Steps

- [ ] Verify source, candidate and asset hashes have not changed.
- [ ] Review the final correction set and complete text, then record the result.

## How to verify

The final LF pack SHA-256 values are fa95257b8cac78c182541209fc541d0ea7cbaf85a0690b96eaace036306efb08 (google-ranking-history) and fcf396b87434d039ac81b585255cb42baa5c962318c289502d98ec8c985189cb (google-trends-research). Confirm original zh-TW, metadata, source URLs/dates, numeric qualifications, code/product names and all locale image text. Existing five-language standalone previews are local layout evidence, not live acceptance.

## Notes

Leave this task unclaimed until an independent reviewer is available. Do not automatically retry the exhausted subagent account. The inherited source summary/self-reference findings are tracked separately and are preserved under the existing-article localization source rule. This task does not authorize deployment, database import or publication; the required isolated rehearsal environment is still unavailable.
