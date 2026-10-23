---
id: 2026-10-08-preserve-translator-critique-and-final-when
title: Preserve translator critique and final when repairing malformed outer JSON braces
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-08T15:59:02Z
completed_at:
branch: codex/stalled-video-reviewed-fixes-20261008
depends_on: []
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
---

# Preserve translator critique and final when repairing malformed outer JSON braces

## Why

A genuine cached Japanese caption translator answer contains its draft, critique
and final worksheet but has two surplus outer closing braces. The current
parseAnswer repair selects the first valid draft object, losing the genuine
critique/final, and then rejects it as missing critique. This stalls an already
paid result. Recovery used an explicitly hash-bound private structural view;
the normal parser still needs a general, conservative fix.

## Definition of done

- [ ] A recoverable outer-brace error retains the complete draft/critique/final
      envelope and returns the actual final worksheet through normal validation.
- [ ] Ambiguous or content-changing repair remains rejected; original provider
      text and durable receipts remain immutable.

## Steps

- [ ] Reproduce the actual extra-brace shape with a sanitized local fixture.
- [ ] Preserve the full envelope instead of accepting its earlier draft object.
- [ ] Test missing critique, ambiguous objects, broken strings and unrelated JSON
      without loosening worksheet/source validation.

## How to verify

Run node --test tools/video/automation/prompts.test.mjs and the applicable tools
tests. Prove the recovered final texts and critique equal their source bytes;
do not use a live model call for this parser regression.

## Notes

- Actual private fixture: `<home>/mokaair-work/stalled-video-audit-20261008/`
  `text-wave-candidate/CF-actual-latest-caption-unit-fixture.json`.
- Original raw SHA df3c9eb43f3b6a0195b75a1ce7d59736c7a3d79db067a5b4abc7346168c58370;
  structural view removes only surplus braces at offsets4859 and10464. Its SHA
  d9828dd78d3998ebbe515ac72a3bb628d71e3585c527e5f36604660fb9836b47 passes
  ordinary parseAnswer with25 genuine critique entries and24 final captions.
- The operational recovery preserves the original request, model result and
  durable cache. It is not a permanent parser patch or another model request.
