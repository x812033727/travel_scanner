# Independent Day01 editorial review

Status: editorial review passed for the content hash below; no media-production or release approval.

Reviewer: independent lesson author for Day02–21; not the author of Day01.
Reviewed file: `production/lessons/day01.json`
Full-file SHA-256: `137ef7a19096c7b3d4afd762426be7e3cf5eb5fdd53bfaf301444d753e3f1c40`
Spoken-content SHA-256: `223b98f323c51f22ec6fc5c68ca02f0fe456bb41202b04b4eba576340eb4fc12`
Reviewed at UTC: 2026-10-08T12:34:51.891504+00:00

The spoken-content hash is computed from exactly the fields `A`, `B`, `quiz`, `guides`, `title_all`, using UTF-8 JSON with recursively sorted keys, `ensure_ascii=False`, and compact separators `(',', ':')`. Claims/source metadata added later may change the full-file hash without changing this reviewed content. Any change to these content fields requires re-review.

## Scope

Read all 14 English dialogue turns and all 56 corresponding Traditional Chinese, Simplified Chinese, Japanese, and Korean translations; all three quiz questions, choices, explanations and evidence selections; all five guides in all five languages; and the adaptation notes. Re-read the corrected answer fields and all five localized recap/comment/subscription sequences after the author revised them. The review concerns meaning, answer support, and spoken editorial structure. It is not a native-speaker certification or an audio listening check.

## Meaning and answer support

No substantive mistranslation found. Zone letters, counter ranges, thirteen-versus-thirty clarification, left/right turns, pharmacy, and beside-versus-upstairs meanings agree across the five languages.

| Question | Evidence | Judgment |
| --- | --- | --- |
| 1 | B01–B02 | Supports option B, Zone D; “D as in Delta” confirms D. |
| 2 | B03–B06 | Supports option C, 30–34; full range and correction from thirteen to thirty are included. |
| 3 | B07–B08 | Supports option A, turn right; stairs describe the counters' location, not an instruction to go upstairs. |

The A06 direction and the combined eight-turn B conversation are internally coherent. B reuses a single fictional airline and preserves all three intended quiz answers. The adaptation note correctly identifies airline names, counters, and directions as fictional examples. The next-lesson subscription topic agrees with Day02.

## Revisions checked

The initial review requested answer-field normalization and a three-utterance outro. Both are resolved:

- `quiz[].answer` now equals the selected choice: `Zone D`, `30–34`, `Turn right`; the spoken explanations remain in `answer_all`.
- The recap is one compound voiced utterance, the comment is one learner-response question, and the subscription is one reasoned utterance in every locale. The Japanese and Korean subscription lines were combined on re-review. Quoted English questions within a narrator utterance are not counted as extra outro utterances merely because they contain question marks.
- The coordinator explicitly retained a learner-response question for Day01's practice format. The review does not expand that choice into a claim of production approval.

## Remaining production checks

Official TTS must confirm that Sunrise Airlines, Maple Airlines, Charlie, Delta, the zone letters, and the thirteen/thirty contrast remain clear. Numeric choice ranges should be spoken as ranges rather than a subtraction expression. Mixed English phrases inside translated teaching lines require pronunciation review. No actual audio or rendered frames were reviewed here.

Array-length, English-source alignment, answer/choice equality, available evidence IDs, and 14 unique turn IDs passed a local structural check. The semantic/editorial review passes only for the content hash above; measured timing, translated-voice pronunciation, subtitle layout, and final-media QA remain separate requirements.

<!-- airport-editorial-review-v1 {"schema_version":1,"decision":"text_review_passed","reviewer":"airport_lessons_02_21","content_hashes":{"1":"223b98f323c51f22ec6fc5c68ca02f0fe456bb41202b04b4eba576340eb4fc12"}} -->
