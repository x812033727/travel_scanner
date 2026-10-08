# Production adapter: independent technical review

Date: 2026-10-08. Reviewer: `airport_media_rules_audit`, independent of the adapter author.

Status: the five reported preparation defects and the Traditional Chinese
teaching-audio selection issue have been corrected and independently retested. This is a source/tool review, not an outline,
voice, final-media, language-delivery or publication approval. No paid request was made.

## Scope and verification

Read the remediation task and audit, then reviewed `tools/video/core/drama.mjs`, its
tests, `tools/video/airport_english/prepare.mjs`, its tests/README, the production
profile and representative prepared artifacts. The mixed-language audio
module and delivery helper have separate independent reports in this directory.

Ran:

```sh
node --test tools/video/airport_english/prepare.test.mjs tools/video/core/drama.test.mjs
```

Result after corrections: **44 tests passed, zero failed**. Additional independent
in-memory probes used actual Day01 and Day31 sources. Temporary-directory probes did
not change the historical media or production lessons.

## Defects found, corrected and retested

1. **Fact-review results were disconnected from narrated claims.** The first adapter
   wrote claims only in `claims.md`; no generated scene cited them. With a Day31
   verification row marking `AE-C11` `NOT FOUND`, the official `factsChecks` returned
   `ok: true` because no scene cited the rejected claim. The correction conservatively
   cites all applicable nonfiction lesson claims on its dialogue scenes. Retest:
   Day31 has 54 cited dialogue scenes and that same rejection returns `ok: false`.
   This preserves the real official fact-check gate; it does not certify the claims.
2. **The spoken quiz answer could disagree with the selected answer.** Replacing
   Day01 Q1's English `answer_all[0]` with `The answer is A: Zone B.` while its correct
   answer remained B / Zone D passed the original validator and entered narration.
   The correction checks both the spoken answer letter and the choice words, with
   explicit normalization for the reviewed Day01 written/spoken number range.
   Independent retest rejects both the wrong letter and the right-letter/wrong-choice
   variant. This consistency check is not a semantic review of every explanation.
3. **Staging retained withdrawn review/translation files.** The initial recursive copy
   merged directories. A target-only `verify-9.md` remained after restaging even though
   the prepared source had no such report; the official last-round selector could
   therefore continue using a withdrawn report. Staging now replaces the episode's
   derived source directory and checks its expected slug before replacement. The
   regression verifies that stale reviews and translations are removed. Do not place
   unpreserved editorial work in the disposable staging copy.
4. **Unknown character roles became Staff silently.** `speaker: "INVALID"` produced a
   Staff label without an error. Source validation now requires T or S; independent
   Day01 mutation is rejected.
5. **The path guard checked only one ancestry direction.** A media directory containing
   the staged project passed the original “separate directories” guard. Both ancestry
   directions are now refused, with regression coverage.

## Additional integration finding, corrected: Traditional Chinese teaching audio

The first review found that `tools/video/core/stages.mjs:readLanguages` unconditionally skipped
`zh-TW` (`NARRATION_LOCALE`), even when the video's `narration_locale` is `en`.
The airport profile correctly selected four dubs, but the official reader discarded one.
A temporary file written with the profile's actual selections reproduced:

```text
stored dub selections: zh-TW, zh-CN, ja, ko
readLanguages -> dubLocalesOf(..., { narration_locale: "en" }): ja, ko, zh-CN
captions: en, zh-TW, ja, ko, zh-CN
metadata: en, zh-TW
```

Root corrected the official reader to retain an explicitly selected zh-TW dub.
Independent retest with the real profile now returns all four teaching locales for
English narration; zh-TW narration still excludes dubbing itself. CC and metadata
selection were already correct. This selection fix does not by itself integrate the
new mixed-track artifact contract with final review/package discovery; that remains
a separate production step. No unclaimed core file was changed by this reviewer.

## Behaviors that remain correctly bounded

- Slides `audio_ref` uses the existing earlier-original, identical spoken text,
  speaker/effective-voice and no-reference-chain validation. Cast speaker declarations
  remain disallowed for slides. TTS planning also checks canonical words/voice, and
  the existing speech hash includes `audio_ref`; this review found no new replay
  currentness bypass in that schema change.
- Every source dialogue has stable semantic take/line IDs. Replays point at originals;
  the original English text remains the quote card's visible content. Translations
  remain independent CC. The teaching plan retains English for dialogue and localizes
  coaching/questions, rather than replacing dialogue with translated speech.
- Generated translations carry official source text/metadata hashes. Those hashes
  identify their source; they are not assertions of linguistic or audio correctness.
- `duration-plan.json` explicitly calls its value a text estimate, leaves measured
  body/branding/final seconds null, and sets `release_ready: false`. 600 seconds is the
  target, not a newly measured result. The adapter does not lower the official minimum.
- The wrapper calls the existing official CLI. It does not fabricate approvals and
  blocks generic dubbing, direct approval, upload/sync and automation commands.
  Installed branding, checked source audio, mixed-track provenance, final QA and
  package QA still need real evidence.
- After the author froze and regenerated all 60 episodes, independently recomputed
  300 prepared JSON artifacts and 240 translation files, and checked all 60 complete
  line maps and their lesson hashes: zero differences. This final pass includes Day12
  “Docs Ready” and Day46 “Next Flight”, with canonical spoken content unchanged. This checks source preparation currentness,
  not measured media or approvals. Staging now also carries the shared profile,
  lesson and review snapshots needed by relative review links. The final TTS wrapper
  also checks current editorial bindings and the staged artifact/source/review bytes;
  its regression passes. The binding module has its own independent
  [review](binding-tool-review.md).

## Reviewed file identities

SHA-256 at this corrected-tool checkpoint:

| File | SHA-256 |
| --- | --- |
| `tools/video/core/drama.mjs` | `f5e31865984f984b12434854924107afc787a6ffbd02c69a55429166a1b5265a` |
| `tools/video/core/drama.test.mjs` | `c8389b161696c01195de6f505c9ed228f27527637de259b91a04da7de670090a` |
| `tools/video/airport_english/prepare.mjs` | `2d206325a8402e025c96613605e0fe8a704e9fe8fc8e31504ad873aa3f0dbb12` |
| `tools/video/airport_english/prepare.test.mjs` | `7ba214038607ee28651f9fb6074e8bbb6a1f8cee50bb1d2080b055a640d27cbf` |
| `production/profile.json` | `839e447826b0e2dbe10458227143caa8fe2ba8719b68d0800ac6ba2983efb534` |
