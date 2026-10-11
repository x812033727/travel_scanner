---
id: 2026-10-10-correct-published-bitmine-sole-outlet-attribution
title: Correct published Bitmine sole-outlet attribution
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-10T10:23:41Z
completed_at:
branch:
depends_on: []
scope:
  - docs/news-bitmine-source-attribution-correction-2026-10-10.md
---

# Correct published Bitmine sole-outlet attribution

## Why

Published Bitmine article `28960c6f-cbe0-4bcf-a01c-f39591f094f2`
(news candidate `1fc37533-a7f7-4360-9982-5dcba407e1cb`) states
「目前只有 Decrypt 一家的報導」 in zh-TW and "Only Decrypt has reported it so far"
in en at `/blocks/13/items/4/answer`. Preserved CoinDesk evidence for duplicate
candidate `6c71f06c-a4a0-4853-be00-2e93b70e05d8` describes the same event and
has an earlier October 7 publication time (12:40 versus Decrypt's 14:55).
The duplicate's core event is covered, but the published sole-outlet claim is false.

## Definition of done

- [ ] Independently review the minimal source-attribution correction against
  both preserved full source bodies and all five actual published revisions.
- [ ] Correct every affected locale through normal Guide draft, review and
  publication operations, retaining genuine revision and audit identities.
- [ ] Verify the resulting five public locale API/page responses and persist
  the exact source, revision, content hash and publication receipt.
- [ ] Preserve original208 membership and the duplicate's native terminal
  history; a wording correction does not authorize replaying the duplicate.

## Steps

- [ ] Capture fresh article/revision/history state and check all five locale
  FAQ answers for the same unsupported exclusivity assertion.
- [ ] Prepare a minimal reviewed correction and a concrete native operation.
- [ ] Publish and verify after the normal article review gates succeed.

## How to verify

Compare both source publication timestamps and event facts. Bind each changed
document to its actual prior published revision and native save/publication audit.
Read every public locale after publication; a local corrected document, saved draft
or queued operation does not establish the correction is public.

## Notes

2026-10-10: Independent local review
`duplicate3-terminal-current-event-coverage-independent-operator-review-v1.json`
SHA256 `4a2d6e4b702ed773439f0500f7da8a596024e3b6c727fad0870c5d88fcad19f4`
binds current parent SQL at 10:07:56Z to 15 published revisions, native audit
joins and prior public proofs. It explicitly reports this defect. The historical
duplicate assessment does not record a matched-parent FK; current same-event
coverage is independently established, not a reconstructed historical edge.
Evidence is preserved outside the repository under
`C:\Users\x8120\.codex\news-review\20261010-6f71`.
