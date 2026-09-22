---
id: 2026-09-22-review-thailand-airplane-mode-source
title: Review Thailand guide airplane-mode source instruction
status: blocked
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-22T05:08:03Z
completed_at:
branch:
depends_on:
  - 2026-09-22-localize-thailand-esim-sim-wifi-batch015
scope:
  - apps/api/app/guides/content/thailand-esim-sim-wifi.json
---

# Review Thailand guide airplane-mode source instruction

## Why

The published zh-TW v8 guide says to turn airplane mode off and then on when a newly
installed eSIM has no signal. That direction is unusual and may leave the phone offline.
Batch 015 translations use a neutral instruction to toggle airplane mode, but this is
only a translation-safety choice and is not a verified correction of the zh-TW source.
The repository zh-TW document also has a separate unpublished answer-first description,
so any source edit must preserve that repository-only work and the live/repository state.

## Definition of done

- [ ] Compare the exact published zh-TW v8 instruction with current official Apple and
      Android/Google phone guidance for refreshing cellular service after eSIM setup.
- [ ] Record whether the intended safe sequence is on then off, a neutral toggle, or a
      different operator-specific procedure, with reader-visible primary sources.
- [ ] Propose an exact `/blocks/16/text` source replacement and independently review it
      before changing the repository or production source.
- [ ] Preserve the repository-only AIO description and reconcile the live zh-TW v8,
      repository document, revision and publication state without publishing zh-TW.
- [ ] Re-review all four translations if the approved source meaning changes.

## Steps

- [ ] Wait for batch 015 to finish so its pinned hashes and approved translations remain
      immutable during source review.
- [ ] Capture fresh read-only live and repository baselines and bind exact hashes.
- [ ] Review official device instructions and prepare the source-correction packet.
- [ ] Obtain independent source/editorial approval before applying any correction.

## How to verify

Verify the live source and repository document with a read-only transaction, compare the
exact JSON pointer recursively, run the scoped GuideDocument and pack lint, and bind the
independent source-review receipt to the before/after hashes.

## Notes

- **BLOCKED on** `2026-09-22-localize-thailand-esim-sim-wifi-batch015` so the translation
  candidate and repository-only description are not changed underneath its review.
- The observed zh-TW wording is `落地沒訊號，先關閉再開啟飛航模式，還是不行就手動選 AIS 或 TRUE-H`.
- Batch 015 en/ja/ko/zh-CN use a neutral airplane-mode toggle. Do not cite that editorial
  choice as evidence that the zh-TW source has been verified or corrected.
- Do not silently update the live source, the repository pack, baseline hashes, or any
  summary/description field. Treat those as separate reviewed states.
