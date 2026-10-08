# Independent text review: Days 42–60

Reviewed: 2026-10-08. Reviewer: Codex AI agent `airport_lessons_22_41`, separate
from the author `airport_lessons_42_60`.

Decision: **the scoped editorial content passes this independent AI text
review after the corrections below**. This does not approve speech, production,
caption timing, rendered video, publication, or a human/native-speaker review.

## Scope and method

Read all 228 English dialogue turns, all 57 English question/answer pairs and
selected replay exchanges, and all 475 new guide strings across English,
Traditional Chinese, Simplified Chinese, Japanese, and Korean. Checked guide
meaning, factual scope, opening-to-recap consistency, learner questions, and
reasons to subscribe. Compared A/B speaker, English text, and all five locale
arrays against the preserved source snapshot: none changed in this slice.
There were therefore no newly edited A/B translations requiring a change review.
This is not a fresh exhaustive native-language review of every inherited CC
translation or every inherited distractor.

Every quiz's explicit IDs resolve to actual dialogue turns and include the
answer-bearing utterance with enough context. The chosen answer matches
`choices[correct]`; question and dialogue English mirror their first locale
entry. All 19 records have exactly five guide keys and all 475 guide strings are
nonempty. Structure checks corroborate the manual semantic reading; they are
not the basis for asserting answer relevance.

The three closing guide fields form three voiced sentences in each locale:
`recap` answers the episode's opening task, `comment` is one answerable personal
question, and `subscribe` is one reasoned invitation. Quoted practice questions
inside a reporting sentence are part of that sentence, not a separate outro
line. Day 60 invites repetition of the existing airport playlist rather than
inventing an unplanned next episode. English guide word counts are drafting
estimates only; actual five-language speech duration remains unmeasured.

## Corrections requested and checked

| Day | Independent finding | Final correction |
| --- | --- | --- |
| 42 | English hook asked which gate while its translations asked how to confirm it. | English now asks how to confirm the correct gate; K5 printed on the pass and K17 on the display are supported by A03/A04. |
| 49 | Hook promised a return/onward distinction but recap only repeated Friday's return booking. Japanese subsequently narrowed onward travel to immediately after a transfer. | Recap now explains returning versus continuing to another destination in all five locales; Japanese no longer implies that all onward journeys immediately follow a transfer. |
| 50 | Hook asked which address the officer meant, but recap only asked for slower repetition. | Recap now distinguishes current address from hotel address, matching B03/B04. |
| 51 | Hook already knew carousel 7 and asked about absent bags, while recap taught locating the carousel. | Hook now asks which carousel serves the arriving flight, matching the lesson and recap. |
| 52 | Hook asked how to report missing baggage, but recap only discussed later follow-up. | Recap now directly states that the belt stopped without the suitcase appearing. |
| 59 | Hook claimed B20 was printed on the pass; the dialogue only establishes B20 from the check-in agent's spoken instruction. | All five hooks now attribute B20 to what was heard at check-in. New gate B32 remains supported by B01/B02. |
| 60 | Hook promised stay duration, hotel, and missing bag, but recap omitted the hotel. | All five recaps now include eight days at Riverside Hotel and the missing green suitcase. |

The author report initially reversed the interpretation of `T` and `S` in some
lessons. Direct file and source-snapshot comparison established that the actual
records use `S` for staff and `T` for travelers, including the officer-led
conversations. The author corrected the report and did not alter speaker IDs.
Do not swap already-correct voices based on the withdrawn report statement.

## Answer-support decisions

All 57 explicit selections below passed manual review. Particular historical
failures are corrected: Day 55 Q3 includes B05's actual digits 6281; Day 59 Q2
uses the new B32 exchange rather than the old B20 exchange; questions about
conversation B are not forced into an A-conversation replay.

| Day | Q1 | Q2 | Q3 |
| --- | --- | --- | --- |
| 42 | A03, A04 | A05, A06 | B05, B06 |
| 43 | A01, A02 | A03, A04 | B05, B06 |
| 44 | A03, A04 | B01, B02 | B03, B04 |
| 45 | A01, A02 | A05, A06 | B03, B04 |
| 46 | A01, A02 | A05, A06 | B05, B06 |
| 47 | A01, A02 | A03, A04 | B01, B02 |
| 48 | A01, A02 | A05, A06 | B03, B04 |
| 49 | A01, A02 | B01, B02 | B05, B06 |
| 50 | A02, A03 | A04, A05 | B03, B04 |
| 51 | A03, A04 | A03, A04 | B03, B04 |
| 52 | A01, A02 | A03, A04 | B03, B04 |
| 53 | A01, A02 | A03, A04 | B05, B06 |
| 54 | A01, A02 | A03, A04 | B05, B06 |
| 55 | A03, A04 | B01, B02 | B04, B05 |
| 56 | A01, A02 | A03, A04 | B02, B03 |
| 57 | A01, A02 | B01, B02 | B05, B06 |
| 58 | A01, A02 | B01, B02 | B03, B04 |
| 59 | A03, A04 | B01, B02 | B03, B04 |
| 60 | A01, A02 | A05, A06 | B03, B04 |

## Factual boundaries and remaining checks

Days 42–46 keep route-dependent baggage, screening, boarding-pass and
missed-connection instructions conditional. Day 43 does not promise that a
final-destination tag always avoids intermediate bag collection. Days 47–50
and 60 are invented truthful role-play answers, not immigration eligibility
rules or entry guarantees. Days 51–55 do not promise compensation, replacement,
delivery eligibility, or an exact reporting deadline. Day 56 asks an officer
about uncertain customs requirements rather than assigning universal limits.
Day 57 explicitly frames directions as examples. Day 58 leaves rebooking,
seats, baggage and assistance subject to actual review.

The separate official-source claims review must substantiate the applicable
real-world guidance. This review does not independently recertify that source
ledger. Fictional gates, names, hotels, colors, dates, phone digits and times
are listening material, not real operational information or private data.

Speech synthesis and pronunciation/listening checks, actual guide durations,
CC splitting and timing, final layout, media normalization, encoding, packaging,
and the hash-bound final production gate remain outstanding. Passing these
text checks must not relabel previously rendered prototype media as corrected.

## Exact reviewed revisions

`content_sha256` is SHA-256 of UTF-8 canonical JSON containing exactly the fields
`A`, `B`, `quiz`, `guides`, and `title_all`, using recursively sorted keys, compact
separators `(',', ':')`, `ensure_ascii=False`, and no final newline. This binds the
review to the actual teaching content while allowing unrelated claims/status
metadata to evolve. `file_sha256` hashes the entire original JSON file bytes at
review time and includes formatting and metadata. If the content hash changes,
this review no longer covers that revised content.

| Day | content_sha256 | file_sha256 |
| --- | --- | --- |
| 42 | `4cfebca5296b82f615d82b73b47021203af8598014d567dab99cb570c1752cb8` | `d3835f502e0fb98156ebff8e94274b4088759f116c9d62a9678cd2e2a30b1bba` |
| 43 | `e00d66f33f2b2e0e8525c31c5744965b4609a9a6a75ef84e1bcc0365324a3a0b` | `f35802adccfc5f47c9e14ae104a56eae9a042153a522b7a3172a73ba5811b93d` |
| 44 | `34666ae056a4f66e66add87f1a1b59c833ced403190ea5da3c7cedfa8acea2d5` | `793a908352d32b98c4fd31883a78e4a2d903613c0a99619bf958a0f9e9575881` |
| 45 | `d785d8356ca2ec7e86f7aa87346f1733d6b13ef239cee6eadf6e70568fd5d421` | `07647ef6735530dcfd4a9a9e75f81054e2f1b0e646af694c9762529ab365ef18` |
| 46 | `6f7f6402967bd3e5ac2d0bd6f14a86933dc53b45a993508ba17bc484c7e06dbb` | `d33476863fbe36898c68a7e2f57f72dd7dc5f31f23bae8e2fc3a42ec2b65d75e` |
| 47 | `cae22956c7d2bb3a4318eecc54cf84cbfd1fe1e16e3d2daf9ff30776e34ea635` | `d4d259c98ef35116cfdd0857a16bdae840766026a8bb26cbf4d4a9c161f36125` |
| 48 | `840186b108845777b039ac88ffa533896fbb1886bfaf94f0e87ea0bde004b615` | `63beb62a1ace3a4c0dbba4ef047ebff68ab3f83a207be2b8611542c5a788c777` |
| 49 | `575854ea42e866ce378363309c5ff029870e5b54070859c49faee271f772b9e4` | `c1e54a0f6ac3fb613ab6b802284edcf589e275cf825fab0b736e8d96dadf0301` |
| 50 | `d70d3bf7c5f9d7c8acdecf1d1be7b633b39b0bb1d522db520d8c2f22727c3aff` | `55870a6f04f9869b335f2bb1173a3f7c2465570ba23c960aef40ebc4634c2964` |
| 51 | `0016186482be62a5bd15ea0786b2e38feab03149febb662da87d56e051101bc2` | `dee8fc7128890c1c9c9c4c9db21373e12e57df60817449da99455d4a05504b7b` |
| 52 | `9a1d828759a19fee142bd94a18098d40cb90a5d0484b9309c34a126940bd7b61` | `e48a1f7c2941a17adf8f1b064d643d08feea65194551870033b12d859d2494e4` |
| 53 | `b31423225478a034e81df42b39aeafeb05e2f957e27f522e8bc96370f5d6c372` | `0316818a11dd9e3e052b0abe58f98e75fa4eb898919b646c91f7c559167bf032` |
| 54 | `799577c09e4228129774b68dbcb69cbb92c6b6365f99a46faeef85c46cb3007e` | `a644ab8d89a43cc759fee1ac75e2a014775ae648092db71f7eeb57b438211aa9` |
| 55 | `ace211b1dab60facee962956760271020bf8db6722dab4400fb8d34e42917fb3` | `9efdf703e6838aec092b5fbda29c18adb282cb0976c1fd7bb79b758a329d6f86` |
| 56 | `41423c970060aa24da9d301690184f2fd40a5d425cb56a3450c2cef1d6ca7db5` | `958b18ff718947c71904abdaff79f4e00e88d41fd93811999bb30fa9ceb12273` |
| 57 | `c0344d7677aa22b6269d36f99f558df43821fc241acc66315fd7f9cefce0d0aa` | `75fd246e6bba8027ef315d0b7cec4393ce1e815749412fde4474ccbd99e9c203` |
| 58 | `2a55abd86dc1bdc333d72257c01aefadce3852555fb7df564dc9dca34bc837ca` | `cf9bb5453f87971870291d387972ae030bd80193487db2f149058b9513cdad0e` |
| 59 | `e90fff04dcc5df1d626c89ae5172fc5bd0a89b5c588f0cbe5812b540dfe0fcd8` | `212c06c6a331f63cd2072bd2fb77412d9805cfdb583c337f713a04e15a8addbd` |
| 60 | `5bdc9e247c92514045af305553c7cb7e51efd0fc3e98465cf1ca3b874fee05de` | `13af6a92bb09dc4ffc0a5a1a916a9436e46189dd8b773f13ae8df8ec8efb9ac0` |

## Machine-readable current text decision

The same independent reviewer rehashed all 19 current lesson teaching-content
payloads against the original table above before writing this attestation; all
19 canonical hashes still match. The whole-file hashes above remain the
original review snapshots and are not overwritten by later metadata changes.
This attests only the scoped text-review pass already described here and does
not approve audio, rendered media, production, or release.

<!-- airport-editorial-review-v1 {"schema_version":1,"decision":"text_review_passed","reviewer":"airport_lessons_22_41","content_hashes":{"42":"4cfebca5296b82f615d82b73b47021203af8598014d567dab99cb570c1752cb8","43":"e00d66f33f2b2e0e8525c31c5744965b4609a9a6a75ef84e1bcc0365324a3a0b","44":"34666ae056a4f66e66add87f1a1b59c833ced403190ea5da3c7cedfa8acea2d5","45":"d785d8356ca2ec7e86f7aa87346f1733d6b13ef239cee6eadf6e70568fd5d421","46":"6f7f6402967bd3e5ac2d0bd6f14a86933dc53b45a993508ba17bc484c7e06dbb","47":"cae22956c7d2bb3a4318eecc54cf84cbfd1fe1e16e3d2daf9ff30776e34ea635","48":"840186b108845777b039ac88ffa533896fbb1886bfaf94f0e87ea0bde004b615","49":"575854ea42e866ce378363309c5ff029870e5b54070859c49faee271f772b9e4","50":"d70d3bf7c5f9d7c8acdecf1d1be7b633b39b0bb1d522db520d8c2f22727c3aff","51":"0016186482be62a5bd15ea0786b2e38feab03149febb662da87d56e051101bc2","52":"9a1d828759a19fee142bd94a18098d40cb90a5d0484b9309c34a126940bd7b61","53":"b31423225478a034e81df42b39aeafeb05e2f957e27f522e8bc96370f5d6c372","54":"799577c09e4228129774b68dbcb69cbb92c6b6365f99a46faeef85c46cb3007e","55":"ace211b1dab60facee962956760271020bf8db6722dab4400fb8d34e42917fb3","56":"41423c970060aa24da9d301690184f2fd40a5d425cb56a3450c2cef1d6ca7db5","57":"c0344d7677aa22b6269d36f99f558df43821fc241acc66315fd7f9cefce0d0aa","58":"2a55abd86dc1bdc333d72257c01aefadce3852555fb7df564dc9dca34bc837ca","59":"e90fff04dcc5df1d626c89ae5172fc5bd0a89b5c588f0cbe5812b540dfe0fcd8","60":"5bdc9e247c92514045af305553c7cb7e51efd0fc3e98465cf1ca3b874fee05de"}} -->
