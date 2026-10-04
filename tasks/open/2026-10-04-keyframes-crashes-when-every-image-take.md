---
id: 2026-10-04-keyframes-crashes-when-every-image-take
title: Keyframes crashes when every image take is rejected
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-04T12:07:14Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
---

# Keyframes crashes when every image take is rejected

## Why

When every image take is refused, keyframes records a needs-review shot without a file, then includes that record in pictureHashes. path.join receives undefined and the CLI throws a TypeError instead of reporting the original generation refusal. A two-shot LLM pilot reproduced this after the provider rejected its combined prompt length; no new image was created.

## Definition of done

- [ ] An all-refused shot produces a clear nonzero generation/check result with its original refusal, without an undefined-path exception.
- [ ] Existing valid shots, failed-job receipts and pending-job recovery remain intact; contact sheets and duplicate checks only inspect actual picture files.
- [ ] A mixed successful/refused run and an all-refused run have meaningful regression coverage without external API calls.

## Steps

- [ ] Reproduce the fileless needs-review record using the existing fake media client.
- [ ] Guard post-generation picture processing and verify the terminal result preserves the refused-shot details.

## How to verify

`node --test tools/video/media/look-keyframes.test.mjs`

## Notes

- Reproduced 2026-10-04 with `keyframes --slug ai-term-large-language-model --shot counter-arrival,counter-handoff`. Both shots received three definitive MiniMax `prompt length must be less than 1500` refusals; six terminal failed receipts accounted for zero cost and local pending jobs were empty. Fourteen unaffected shot entries/verdicts and all 23 existing image caches were preserved exactly. This is a definite rejection, not an uncertain paid POST.
- `tools/video/media/keyframes.mjs` builds `drawn` from the presence of a shot record, which can have `takes: []`, `needs_review: true` and no file; `pictureHashes` then receives undefined. The saved private rejection log/audit is under `<home>/mokaair-work/ai-series-continuation-20261004`.
- Related source preflight gap: schema's 1000-character scene prompt limit does not include Style, Camera or the provider's appended Avoid text. The failed combined strings measured 1644/1640 characters; the author shortened only the two prompts to actual combined lengths 1350/1367, preserving narration. Any broader provider-limit guard or non-retakeable parameter classification needs an explicitly claimed scope before changing shared tooling.
