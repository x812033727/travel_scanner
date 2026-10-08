# Independent editorial review — Day 02–21

Reviewer: `/root/airport_lessons_42_60` (AI), 2026-10-08. The reviewer did not author these 20 lessons.

Result: the revised text passes this independent editorial check, with the corrections below applied and re-read. This does **not** approve synthesis, native-language pronunciation, final captions, rendered media, or publication.

## Method and scope

Read every one of the 60 quiz questions and selected answers against its explicitly selected dialogue turns, including cross-conversation selections. Read all 500 new guide strings across English, Traditional Chinese, Simplified Chinese, Japanese, and Korean for meaning, scenario consistency, natural phrasing, and opening/outcome alignment. Checked that each closing sequence has a recap, a personal learner question, and a reasoned subscription invitation referencing the actual next lesson. Quoted English questions embedded inside a narrator sentence are part of that teaching utterance; they are not extra calls to action.

Programmatically compared all 240 original dialogue turns and all original quiz fields against the preserved source snapshot: the author changed neither dialogue text/translation/speaker nor quiz question/choices/answer/translation. The only quiz addition is the explicit evidence selection. Also checked that IDs resolve, evidence IDs do not repeat within a question, choices agree with selected answers, and every guide has five nonempty strings.

All 60 selected replay exchanges support the answers. Day 21 Q3 uses the announcement plus the clarification that boarding has not started; “shortly” means soon, not that boarding is happening now. Day 18 Q1/Q2 intentionally reuse the exchange containing both walking and boarding times. These are editorial decisions about the text; the final timeline must still prove it actually uses these IDs.

## Corrections requested and confirmed

- Day 05: recap now answers the opening's time change: the flight is delayed, with nine twenty as the current estimated departure, without turning it into a guaranteed actual departure.
- Day 06: each translated comment now asks preference and reason in one sentence, keeping the closing sequence at three spoken teaching utterances.
- Day 08: recap now answers what the baggage receipt is for instead of merely repeating a question about it.
- Day 09: recap now asks about options before paying an excess-baggage fee, matching the opening; it does not promise free repacking or a waived fee.
- Day 10: recap now distinguishes the example's seat fourteen A from gate C twelve instead of answering an unrelated boarding-time question.
- Day 15: opening now asks how to check whether belongings may be collected, matching the recap.
- Day 18: opening now asks for the walking time to E twelve, matching the recap's walking-time question.
- Day 19: English opening now says the phone battery is running low; the four existing translations already expressed that meaning.

Re-read all five localized strings for each changed field after the author saved and froze the revision. No further semantic correction was identified in this review.

## Evidence decisions

The answer text below is supported by the named turns; the full selected exchanges were read rather than inferred from word overlap.

| Day | Question 1 | Question 2 | Question 3 |
| --- | --- | --- | --- |
| 02 | A01, A02 → Terminal Two | A03, A04 → Every ten minutes | B03, B04 → On the left |
| 03 | A03, A04 → A language | A05, A06 → The photo page | B03, B04 → A document check |
| 04 | A02, A03 → In an email | A05, A06 → Two | B04, B05 → Vancouver |
| 05 | A01, A02 → Dubai | A05, A06 → Three hours | B03, B04 → Nine twenty |
| 06 | A01, A02 → Row twenty-eight | B01, B02 → An aisle seat | B05, B06 → The original seat |
| 07 | A03, A04 → Row thirty | A05, A06 → Boarding passes | B02, B03 → Seven |
| 08 | A01, A02 → On the scale | B01, B02 → The baggage receipt | B05, B06 → Remove them |
| 09 | A01, A02 → Three kilograms | B01, B02 → Repack the suitcase | B03, B04 → Its size |
| 10 | A01, A02 → Fourteen A | A03, A04 → Boarding time | B03, B04 → The flight number |
| 11 | A03, A04 → On the right | B02, B03 → D eighteen | B05, B06 → Behind the information desk |
| 12 | A01, A02 → Screen brightness | A05, A06 → One at a time | B03, B04 → The assistance desk |
| 13 | A03, A04 → A separate tray | B01, B02 → When signaled | B05, B06 → Keys |
| 14 | A02, A03 → Water | A05, A06 → After security | B01, B02 → The screening officer |
| 15 | A05, A06 → A camera | B03, B04 → A chair | B05, B06 → After the check is complete |
| 16 | A01, A02 → Put the jacket in a tray | B01, B02 → The second belt | B05, B06 → The table on the left |
| 17 | A03, A04 → The right-hand corridor | A05, A06 → No | B03, B04 → Turn around |
| 18 | A01, A02 → Fifteen minutes | A01, A02 → In twenty minutes | B03, B04 → One |
| 19 | A01, A02 → Before the cafe, on the left | A05, A06 → Under some window seats | B05, B06 → The information desk |
| 20 | A04, A05 → A ready-made sandwich | A04, A05 → Boarding is soon | B03, B04 → A sealed product with a label |
| 21 | A01, A02 → Passengers needing assistance | A05, A06 → Near the seat number | B01, B02, B03 → Soon |

## Scope of facts and remaining checks

These are fictional practice conversations. Terminal/floor/gate numbers, seat rows, times, shuttle intervals, walking duration, facilities, and prices/weight examples do not establish directions or rules for a real airport. Day 13 preserves “this lane” for laptop handling; Day 14 asks the screening officer for local liquid/medicine procedures. Day 20's ingredient question does not negate the original employee's inability to promise no allergen cross-contact. The new guides do not turn those qualified examples into universal guarantees.

The separate claims reviewer owns current official-source verification. This reviewer did not perform live fact retrieval or listen to synthesized speech. Real guide duration, pronunciation, multilingual audio slots, subtitle readability, exact replay timing, and end-to-end media QA remain production checks. The language review is an AI semantic review, not human native-speaker certification.

## Revision binding

Content hash algorithm: SHA-256 of UTF-8 JSON for exactly `{A,B,quiz,guides,title_all}`, serialized with recursively sorted keys, `ensure_ascii=False`, and compact separators `(',', ':')`. The full-file SHA-256 hashes the exact saved file bytes, including whitespace and trailing newline. Later changes to any bound content require this review to be renewed; changing status or other metadata changes only the full-file hash and must be recorded separately.

| Lesson | Canonical content SHA-256 | Full-file SHA-256 |
| --- | --- | --- |
| day02.json | `bc086fa65f4fbd5687f0db9d329507011a18d0da1fcf7cee7bcb174991a3f865` | `fbef671560cd416fe99f879091323b7036b16ac023b5365d388a7d8be05d528a` |
| day03.json | `16ee338787e5e458c870a3bb173a70f17c2668ec24d4709ae3aa1385056a98e8` | `92d823c7b2299e76e1d9302f8517c421fe1b5f02f44c475837dcbb6166c6065b` |
| day04.json | `4ed2b7fde8924a1df72703a6ec413e3e45452b6f96b8b29e806a843caeb8c256` | `e1bfc5aee18f5aa8ece71fa2d7d7895799b1d823a1eaeb2a59c30813263d3e30` |
| day05.json | `d3db5dcd6bcbff46c0eaddbf7971c21b2b07694e6e293a7bfbc06a24012fdb81` | `4a226996e6283afe6f7c2aaf03d7901d3b3ddd01ebe9d42563760319f081b4c2` |
| day06.json | `03661674ada7e6c2102f39e0cdc47745fb54c6cc168f927fa147c6a5e1261c7e` | `a7df2047a500a733f63699e8e5dd3a072156a233b3390c644d7871c3749db954` |
| day07.json | `471b402c36712dc0c1548cc5947ff66ddafc5a8071aa85a8af173b56fcd808dc` | `d4032e0b2d3417d58303b6f440f7383e77be7e3b2e1ea265d0aa863cce75801e` |
| day08.json | `abeb6eb0c1e6d5011adbbd4d81eb65908fdd54b1e661b2012e7a93f639993dfe` | `cd46baa15cb93970ad9b3e648824742c4efe26beeb3321afaa69be2ddae66e07` |
| day09.json | `02e193d8d7a0aae5ed0599114053450aa0473ff239eb6265803dac53df40738b` | `7ca6b2a942e486e511c59ed4c6f374b9aa93a3bc95aca22e3d0a84570f2384af` |
| day10.json | `6ccd4ec65b1c87c36ab1a8fa04ed5ad739a00fb3158bdfe0fd2beab5eacf641d` | `3021fb370f1f90b061f1ce4a3bb86963b5281137d94f41c701c6a05ca199319b` |
| day11.json | `61cdde969ae4d0af6126d8ac3b77c30e9d25ddac0fa9cbc2853db7404561c156` | `3f3f22390dd7cf81275b0395156e5a611052ba17a6b3bd4c8372aecd09ea7b9d` |
| day12.json | `0ec5426ad5a9efd704f88e16aade0ec9e1b9f04f1673e5f226f6e7a9b63eb1d5` | `04b7de9ae94860524ca1ac99aab675dfdf1f4daf361afb626384ff56275df91c` |
| day13.json | `21eb7454cc6ade209567a896c4c664d963efc14e1b59d68bb40367d46ddb9bab` | `237a96caffaa9c7a532e4670db1282a00901a86165a4d9c755580eb5189e87c8` |
| day14.json | `1672a104957d3b28c6a80b6259687f853b67e4452bbc972da88a120413dce7a3` | `5575c7bb7e55315fb649b1dc67f0571cb16a56466e4a2a5bcb58c7b9a25a438a` |
| day15.json | `614c1cd95168001fd6317948987f24a6ac518b53dda33d1d0d8349ce0fb9b1d5` | `fe16fb52a396a75d051b70bb8eabc155810b72b0107a98faeae528234edb95ea` |
| day16.json | `12acf1d8ea64bb0667b5616ad4ef5173cf4b2adb05116a6a173ce1a3ded7f8d8` | `70059c305d2612baed320df29c2350641202617b6e14051ac41b5aa121b82dee` |
| day17.json | `dba20e8a41d9a16d839c18db1b387c9853e4d7ed9193616ba7ad9c4af850a60b` | `b29477551db022b5c44d9be056baabeefeb9293b28c0896987fe8194744a5fc4` |
| day18.json | `c320338debe314032e05ccaa54adebff0734405999883afc5f025e7371c6e85b` | `3fe8511a6d7dc7c1c24f2e0f0912c114c4267e0c90bc4231815518a1dd8c3315` |
| day19.json | `2ccef564d23b65ec5233962f145f1a2839dfe04deed28bc2ddeffb6194f663a2` | `b624da150294ac59eb703c3be36ec732f0035de04319ba398918ddda012a7986` |
| day20.json | `d7e485dd5b0e8e9038a18fad73a21c804239066b24793849ef12de6960b20e51` | `0d41a4729f3dfff26d0603c42f1fbba6b26c1182ad121ceefe7d1754f34c60fd` |
| day21.json | `c217717812e8d3a7cf075589260113c064d7e28b0552a1de41ca7649a9b3d723` | `185d3e081ab2df7299a44276641bdd14524c392f37bb990b1560d137f0b6dba2` |
