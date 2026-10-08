# Teaching delivery helper: independent technical review

Date: 2026-10-08. Reviewer: `airport_media_rules_audit`, separate from the author.

**Result: no unresolved material defect found in the reviewed helper after the
caption-offset correction.** This is source and isolated-test evidence. No real
combined media package was created, watched, listened to or approved by this review.
No paid request or upload was made.

## Scope and validation

Reviewed the complete `delivery.mjs` and its seven tests, plus the official package
checker/metadata contract and the mixed-track validator/checker it invokes. Ran:

```sh
node --test tools/video/airport_english/delivery.test.mjs tools/video/airport_english/teaching-audio.test.mjs
```

Final result: **18 tests passed, zero failed**: seven delivery and 11 teaching tests.
Tests cover exact main-QA membership and final hash, current mixed checks, actual WAV
bytes/sample lengths, locale/intended-word mismatches, copy integrity, preview routing,
pending review records, missing evidence, and refusal to overwrite an existing delivery.

The successful full `inspectDeliveryEpisode`/copy path has not been exercised against
real newly synthesized media. The tests establish the listed helper contracts and
failure cases, not a completed production QA or end-to-end delivery acceptance.

## Correction found during this review

The mixed manifest initially did not bind `intro_frames` to the actual branded main
picture, while delivery trusted that field to regenerate CC. A self-consistent shifted
caption artifact could therefore survive a newly generated mixed check. The shared
validator now compares the intro offset to current branding, and also binds sample
rate, slug, locale, source script and specification identities. The offset and related
metadata mutations are rejected in the final regression. The source hash below includes
this correction and the official `CHANNEL_ACCENT` import.

## Gate and artifact behavior checked

- Inspection requires the genuine current main audio and final approvals, measured
  source timing/assembly, all 11 official QA items bound to the current final file,
  and a passing official upload-package check. Current source-derived metadata and
  chapters must match the official package; all four requested audio/CC choices remain
  selected. Generic dubbed dialogue tracks are refused by this delivery profile.
- All four mixed manifests must match their current plans and measured source. Every
  required WAV, M4A and caption artifact is hash-checked. Each saved speech verdict is
  re-evaluated against actual decoded WAV length/bytes, current intended words, spoken
  locale and lexicon. A bare passed flag is insufficient.
- SRT is regenerated from the selected actual utterance timing and the verified intro
  offset, then compared exactly with the saved artifact. Caption bounds must fit the
  measured 600-second presentation. This does not replace native-language or final
  synchronized listening review.
- The official main package is copied byte-for-byte, including its original metadata.
  In the official contract, `main.report.final_sha256` is the metadata-file hash;
  `main.finalSha256` separately identifies the main video. The helper uses both in the
  corresponding checks. Supplemental tracks remain described by a separate delivery
  manifest rather than being asserted as part of the original main package approval.
- Copies use full source/destination hashes, regular files, distinct directories and
  a fresh partial output. Source evidence is inspected again before promotion; a
  changed generation aborts promotion. Existing delivery directories are not replaced.
- Preview maps Traditional Chinese, Simplified Chinese, Japanese and Korean audio and
  CC independently; the main English picture remains the source video. This review
  checks data routing, not browser playback on real replacement media.
- `delivery.json` and `COMBINED_REVIEW.json` explicitly leave combined formal QA and
  publication approval false. The review checklist starts unchecked and binds the
  actual delivery and track hashes. The helper does not write official main QA,
  approvals, generic dub manifests, or a YouTube upload result.

## Reviewed source identities

| File | SHA-256 |
| --- | --- |
| `tools/video/airport_english/delivery.mjs` | `92793032afa8688fb75cecae59c31256b27384137780a1a963659ac3a9b0b554` |
| `tools/video/airport_english/delivery.test.mjs` | `3294b6f111ebe46ac9f6df908e92b704aecf82b4999958e975d230d357594dc0` |
| `tools/video/airport_english/teaching-audio.mjs` | `ae637fb8c581f78861ba4340a4122f30b93b9599d89c05d638f8bc1dfa13143e` |
| `tools/video/airport_english/teaching-audio.test.mjs` | `03cc20c2188ce01237ba9473388d2746a5e0a62a88ecde4869ab6a8d9d586dc3` |
