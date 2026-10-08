# Mixed teaching-audio module: independent technical review

Date: 2026-10-08. Reviewer: `airport_media_rules_audit`, separate from the module author.

**Result: the reported module defects were corrected and independently retested.**
This is a review of the offline planner, safeguards and isolated tests. It is not a
claim that real teaching tracks have been synthesized, listened to, approved or
included in the official upload package. No paid requests were made by this reviewer.

## Scope and checks

Reviewed `tools/video/airport_english/teaching-audio.mjs`, its tests, and the existing
helpers it calls for source approvals, measured audio evidence, TTS/check journals,
caption segmentation, fitting, branding and two-pass audio encoding.

Ran:

```sh
node --test tools/video/airport_english/teaching-audio.test.mjs
```

The corrected version passes **11 tests, zero failures**. Those tests use synthetic
PCM and injected transports; they are not substitutes for official transcription or
listening checks on the real voices.

Independently planned all **240 episode/language combinations** from the current
prepared sources after the final Day12/Day46 thumbnail refresh: zero errors,
13,008 preserved English dialogue occurrences and
7,440 translated teaching occurrences. Also re-read the actual Day01 project/spec
for all four locales to exercise the on-disk freshness helper. Planning made no
network request and claimed no production approval.

## Findings resolved during review

1. **A manifest could omit all output bindings.** The initial validator accepted
   a missing/empty artifact map. The checker iterated its entries, so an empty map
   could skip verification of the assembled track and captions. The validator now
   requires exactly `body.wav`, `presentation.wav`, `track.m4a`, `captions.srt` and
   `captions.vtt`, each with a full SHA-256. Regression cases reject an empty map,
   a missing track and malformed hashes.
2. **Long-running operations did not refresh all source inputs.** The initial trailing
   gate re-read English `video.json` but trusted the in-memory teaching specification
   and translations. Build/check now re-read the spec, current project/translation
   files and lexicon, re-plan and compare the fingerprint at entry and before recording
   success. A changed translation or source-take reference is rejected by tests.
3. **WAV timing metadata was not checked against actual samples.** Hash checking alone
   did not compare a coaching clip's decoded length with `audio_samples`. The checker
   now decodes every selected clip and checks its sample count, including cached
   transcription cases, before relying on the fitted timing.
4. **A spec could relabel English dialogue as localized coaching.** Using actual Day01
   data, changing the first dialogue entry (`c95cf077`) to `kind: coach`, replacing its
   speech with the existing Japanese CC and deleting `reuse_source_take` initially
   entered Japanese synthesis while all source/translation hashes remained valid.
   Classification now comes from the bound English scene's canonical
   Traveler/Staff/Airport English role. Both the original and replay relabeling cases
   are rejected. The independent Day01 mutation now fails with “Teaching kind
   contradicts the English source role”.
5. **Translated coaching could consume the learner's response pause.** The original
   window included the source line's explicit pause, allowing a longer localized
   “choose” instruction to use the four-second response interval. Windows now reserve
   `pause_after_ms`; a six-second instruction window retains four seconds for the
   learner, and a three-second translated clip is rejected instead of eating the pause.

6. **The CC offset was not bound to current branding.** The saved manifest could
   change `intro_frames` while keeping other source bindings. Delivery used that
   value when regenerating CC. The validator now requires the current branding
   intro offset, 48 kHz sample rate, episode/locale identity and exact source/script
   specification identities. Offset, format, locale and source mutations are rejected
   by the independently rerun regression.

## Safeguards retained

- Real build/check requires current measured English source audio, exact WAV evidence,
  current request keys, a genuine official audio approval and current per-line checks.
  Main assembly/branding must match the source and total 18,000 frames. None of these
  prerequisites is satisfied merely by the successful offline plans.
- Only translated coaching is synthesized. English dialogue input WAV containers are
  copied exactly from checked source takes, with tempo 1; CC remains translated and
  independent. Final mixed AAC is normalized/encoded, so this is exact input-take
  provenance, not a claim that compressed bytes or overall gain are identical between
  final language tracks.
- Coaching fits within its own measured window, preserves response pauses, may speed
  up only to 1.15, and cannot borrow time from later dialogue. Measured output length
  is checked after `atempo`; overflow requires revising the text.
- CC timing uses each chosen utterance's actual samples rather than a common longest
  language slot. Official word/character boundaries are inherited when available;
  otherwise the existing caption helper uses proportional segmentation. This review
  does not claim forced alignment or native-language listening coverage.
- Speech/check caches bind current words, spoken locale and actual clip bytes. Repeated
  identical English takes can reuse genuine current source checks. Corrupted audio,
  changed source words, stale translations and missing required artifacts are rejected.
- Project leases, STOP handling, official credentials, quotas and paid-request journals
  remain in use. Tests use injected transports; production uses the official clients.
- Output stays in a separate `airport-teaching-audio/v1` work-area contract. Its build
  and check records explicitly leave `formal_qa_approved` and `publication_approved`
  false. They do not overwrite the main project's QA or approval files.

## Remaining production work and limits

Real source synthesis/approval, end-to-end branded encoding with measured speech,
all-language listening checks, final QA and actual delivery packaging still require
execution and evidence. The separate delivery helper now has its own
[independent review](delivery-review.md); its presence does not mean a real media
package was built or approved. Passing these tests does not establish YouTube
multi-audio eligibility.

The earlier zh-TW selection problem in `core/stages.mjs` was separately corrected by
root and independently re-probed: English narration now retains zh-TW/zh-CN/ja/ko
choices; zh-TW narration still excludes dubbing itself. This fixes selection, not the
remaining actual packaging and review execution.

The final code also imports the official `CHANNEL_ACCENT` for Traditional Chinese
coaching. Independently reran the combined teaching/delivery tests after the last
correction: **18 passed, zero failed** (11 teaching tests and seven delivery tests).

Reviewed source identities at this checkpoint:

| File | SHA-256 |
| --- | --- |
| `tools/video/airport_english/teaching-audio.mjs` | `ae637fb8c581f78861ba4340a4122f30b93b9599d89c05d638f8bc1dfa13143e` |
| `tools/video/airport_english/teaching-audio.test.mjs` | `03cc20c2188ce01237ba9473388d2746a5e0a62a88ecde4869ab6a8d9d586dc3` |
