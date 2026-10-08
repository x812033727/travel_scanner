# Independent Day01 editorial review

Status: text_review_passed for the eighteen-turn content below; no audio, media-production, or release approval.

Reviewer: /root/airport_lessons_02_21 (Codex AI), independent of Day01 expansion author airport_production_adapter.
Reviewed file: `production/lessons/day01.json`
Full-file SHA-256: `14ecdeed1cd17bb0f4f9ad1097813c150954b1462177dd4259c92a42e929ec05`
Spoken-content SHA-256: `aa66c6a01286e22a32606f5ad3381fc3fe7dc11356a48a111745920888ca463e`
English-content SHA-256: `4206a5c57022f7a268ee5557e40efa2b15261a4125b0678b35397377de7e985b`
Canonical integration checked at UTC: 2026-10-08T16:31:12.976Z

This decision comes from a fresh independent reading of the expanded eighteen-turn proposal, followed by a value comparison confirming the accepted canonical lesson differs only in its workflow status. It does not reuse the earlier fourteen-turn approval for new text. The outside-Git review was written at `/workspace/airport_production/day01-expansion-editorial-review.md` (report SHA-256 `63e6c40a0113b22aa7115ecab1207cdeabb8c87475fa141da13104758eaacd60`); its frozen proposal full-file hash was `8b902b0dfbaf438eee7bf324a437effa9676dc37c3b1877683d20b425ecc49ab`.

The spoken-content hash is computed with the exported contentHash function in tools/video/airport_english/review-bindings.mjs, from exactly A, B, quiz, guides, and title_all using recursively sorted compact UTF-8 JSON. Metadata-only edits may change the full-file hash without changing this reviewed content; changes to any included field require re-review.

## Fresh eighteen-turn review scope

Read all 18 English dialogue turns and all 72 corresponding Traditional Chinese, Simplified Chinese, Japanese, and Korean translations; all three quizzes with every choice, explanation and evidence selection in all five languages; all five guides in all five languages; titles, adaptation notes and the expansion rationale. Compared the proposal with the existing canonical fourteen-turn version. Every original turn, quiz, evidence ID, guide and title was preserved.

No substantive semantic or translation discrepancy remains. A now has eight turns and B ten, with 18 unique IDs. New A07/A08 ask about checking the Sunrise Airlines sign and confirming the correct queue after the existing Zone C directions. New B09/B10 confirm the Maple Airlines queue beside the stairs already introduced in B08. Airline identity, speaker alternation, landmarks and directions remain coherent in every locale. The additions apply the counter-finding skill to a further practical decision, adding relevant practice content.

| New turn | English | Independent finding |
| --- | --- | --- |
| A07 | Can I join any queue in Zone C, or should I check the airline sign? | All four translations preserve the choice between any queue and first checking the airline sign. |
| A08 | Check the Sunrise Airlines sign above the counters, then confirm your queue with the staff. | Sign position, airline identity and staff confirmation are preserved. |
| B09 | Should I use the queue beside the stairs? Is that the line for Maple Airlines? | The stairs landmark matches B08; both confirmation questions are preserved. |
| B10 | Yes, that's the Maple Airlines queue. Tell the staff your airline before you join it. | The affirmative answer and identifying the airline before joining are preserved. |

Each addition contains 15 English words, or 30 units under the official spokenUnits helper, which counts each Latin word as two units. These are concise one- or two-sentence dialogue turns. The longest new translation is 61 Unicode characters in Korean A08 and needs natural CC segmentation; no spoken-duration pass is inferred from text length.

## Current quiz and guide results

| Question | Explicit evidence | Judgment |
| --- | --- | --- |
| 1 | B01–B02 | Supports choice B, Zone D; D as in Delta confirms D. |
| 2 | B03–B06 | Supports choice C, 30–34; includes the full range and thirteen/thirty correction. |
| 3 | B07–B08 | Supports choice A, turn right; beside the stairs is not an instruction to go upstairs. |

All selected answer fields still equal the indexed choices, and every localized choice/explanation retains the correct letter and meaning. Added turns do not alter any quiz evidence or answer.

The opening, goal and recap remain coherent with the finding-the-counter topic. The closing sequence remains one recap utterance, one learner-response question and one reasoned subscription utterance in every locale; embedded quoted questions are not counted as extra narrator utterances. The subscription topic matches Day02.

## Correction requested and verified

The expansion's first draft retained an adaptation note describing an eight-turn B conversation. I requested a correction and re-read the final note, which now distinguishes original A01–A06/B01–B08 from new A07–A08/B09–B10 and records A8/B10. No other editorial correction remains outstanding for this frozen text.

## Boundaries and remaining production checks

The airline names, counter signs and queue positions are fictional local details, not a claim that every airport uses this arrangement. Existing fictional-scenario framing remains applicable. Independent official-source and English-content binding are maintained by the separate claims reviewer.

No new audio or rendered frame was reviewed here. The measured shortfall and the author's expansion-runtime estimate motivated useful additional practice but do not prove a 600-second final video. Official synthesis must verify airline names, letters, numbers, thirteen/thirty contrast, and mixed English phrases in teaching tracks. Actual take identity/replays, response pauses, total duration with branding, translated CC splitting, safe areas, visual pacing, loudness/codec QA, and final media/package gates remain separate requirements.

Local structural checks passed for 18 unique IDs, five-language turn arrays, English/all[0] agreement, selected-answer equality, and all evidence references. The canonical adoption check found only the stated status change from the reviewed proposal. No approval record, paid call, synthesis request, publication action or lesson edit was performed by this reviewer.

## Historical fourteen-turn review

The following is retained as historical evidence only. Its previous content hash and fourteen-turn scope do not authorize the expanded text; the fresh decision above is the sole current authority.

### Earlier fourteen-turn review text

Historical status: editorial review passed for the content hash below; no media-production or release approval.

Reviewer: independent lesson author for Day02–21; not the author of Day01.
Historical reviewed file: `production/lessons/day01.json`
Historical full-file SHA-256: `137ef7a19096c7b3d4afd762426be7e3cf5eb5fdd53bfaf301444d753e3f1c40`
Previous spoken-content SHA-256: `223b98f323c51f22ec6fc5c68ca02f0fe456bb41202b04b4eba576340eb4fc12`
Historical reviewed at UTC: 2026-10-08T12:34:51.891504+00:00

The spoken-content hash is computed from exactly the fields `A`, `B`, `quiz`, `guides`, `title_all`, using UTF-8 JSON with recursively sorted keys, `ensure_ascii=False`, and compact separators `(',', ':')`. Claims/source metadata added later may change the full-file hash without changing this reviewed content. Any change to these content fields requires re-review.

#### Scope

Read all 14 English dialogue turns and all 56 corresponding Traditional Chinese, Simplified Chinese, Japanese, and Korean translations; all three quiz questions, choices, explanations and evidence selections; all five guides in all five languages; and the adaptation notes. Re-read the corrected answer fields and all five localized recap/comment/subscription sequences after the author revised them. The review concerns meaning, answer support, and spoken editorial structure. It is not a native-speaker certification or an audio listening check.

#### Meaning and answer support

No substantive mistranslation found. Zone letters, counter ranges, thirteen-versus-thirty clarification, left/right turns, pharmacy, and beside-versus-upstairs meanings agree across the five languages.

| Question | Evidence | Judgment |
| --- | --- | --- |
| 1 | B01–B02 | Supports option B, Zone D; “D as in Delta” confirms D. |
| 2 | B03–B06 | Supports option C, 30–34; full range and correction from thirteen to thirty are included. |
| 3 | B07–B08 | Supports option A, turn right; stairs describe the counters' location, not an instruction to go upstairs. |

The A06 direction and the combined eight-turn B conversation are internally coherent. B reuses a single fictional airline and preserves all three intended quiz answers. The adaptation note correctly identifies airline names, counters, and directions as fictional examples. The next-lesson subscription topic agrees with Day02.

#### Revisions checked

The initial review requested answer-field normalization and a three-utterance outro. Both are resolved:

- `quiz[].answer` now equals the selected choice: `Zone D`, `30–34`, `Turn right`; the spoken explanations remain in `answer_all`.
- The recap is one compound voiced utterance, the comment is one learner-response question, and the subscription is one reasoned utterance in every locale. The Japanese and Korean subscription lines were combined on re-review. Quoted English questions within a narrator utterance are not counted as extra outro utterances merely because they contain question marks.
- The coordinator explicitly retained a learner-response question for Day01's practice format. The review does not expand that choice into a claim of production approval.

#### Remaining production checks

Official TTS must confirm that Sunrise Airlines, Maple Airlines, Charlie, Delta, the zone letters, and the thirteen/thirty contrast remain clear. Numeric choice ranges should be spoken as ranges rather than a subtraction expression. Mixed English phrases inside translated teaching lines require pronunciation review. No actual audio or rendered frames were reviewed here.

Array-length, English-source alignment, answer/choice equality, available evidence IDs, and 14 unique turn IDs passed a local structural check. The semantic/editorial review passes only for the content hash above; measured timing, translated-voice pronunciation, subtitle layout, and final-media QA remain separate requirements.

<!-- airport-editorial-review-v1 {"schema_version":1,"decision":"text_review_passed","reviewer":"airport_lessons_02_21","content_hashes":{"1":"aa66c6a01286e22a32606f5ad3381fc3fe7dc11356a48a111745920888ca463e"}} -->
