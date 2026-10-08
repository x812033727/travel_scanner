# Day 42–60 editorial revision

Date: 2026-10-08. Author: `/root/airport_lessons_42_60` (AI).

Status: editorial revision ready for independent review; no production approval.

Read the repository `AGENTS.md`, `youtube-video/SKILL.md`, its `script-writing.md` reference, and the earlier content audit. Reviewed all 228 dialogue turns and 57 quiz questions in these 19 lessons. This is an author review of text, not an audio listening check, native-speaker review, or measured final-video QA.

## Changes

- Added explicit `evidence_ids` to every quiz, selecting actual supporting dialogue turns instead of the old A/A/B word-overlap heuristic.
- Added episode-specific `hook`, `goal`, `recap`, `comment`, and `subscribe`, each in English, Traditional Chinese, Simplified Chinese, Japanese, and Korean: 475 strings in total.
- Every English guide has at most 22 whitespace-delimited words. This is a drafting estimate only; the 10–12 second limits still require measurement after official synthesis. The three closing guides give the practice outcome, a personal learner-response question, and a subscription reason tied to the already planned next lesson. Day 60 points back to the existing playlist.
- Kept the original dialogue, quiz wording, choices, correct-answer selections, and existing translations. No answer changes were necessary. Original `T`/`S` voice identifiers were preserved.
- Day 43 retains route-dependent baggage language. The new guides ask staff to check the specific journey; they do not say a final-destination tag guarantees through-transfer.
- Day 47's recap explicitly limits the tourism answer to truthful circumstances. No guide promises entry permission, assistance eligibility, replacement bags, or delivery.
- Day 57's guide identifies locations as example-conversation details, rather than real directions for an unspecified airport.
- Applied the independent reviewer's opening/outcome alignment corrections: Day 42's English hook now asks how to confirm the correct gate; Day 49's recap explains return versus onward travel; Day 50's recap clarifies which address; Day 51's hook asks for the carousel rather than what to do when bags have not arrived; Day 52's recap directly explains that the suitcase has not appeared.
- Applied the final independent-review corrections: Day 59's hook attributes B20 to what the traveler heard at check-in, without inventing a printed-pass detail; Day 60's recap now includes the Riverside Hotel along with the eight-day stay and missing green suitcase.

## Quiz evidence reviewed

Each pair includes the answer-bearing turn and enough surrounding context to make the question intelligible.

| Day | Q1 evidence | Q2 evidence | Q3 evidence |
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

Particular corrections: Day 44 Q2, Day 49 Q2, Day 55 Q2, Day 57 Q2, Day 58 Q2, and Day 59 Q2 now explicitly select conversation B, rather than assuming the second question belongs to A. Day 55 Q3 includes B05, where the digits six, two, eight, one are actually spoken. Day 59 Q2 selects B01–B02 and therefore replays the new B32 gate, not the earlier B20 gate. Day 60 Q3 includes the green suitcase and white strap in B03.

## Facts and integration checks still required

The independent claims reviewer has reported current official evidence; the final claims ledger must bind that evidence to the final lessons. This author did not fetch or independently verify those pages.

- Days 42–46: operating-carrier details, boarding-pass validity, baggage rechecking, repeat transfer screening, sealed duty-free handling, and missed-connection arrangements depend on the journey, airport, and airline. Do not generalize the scripted staff answers into worldwide rules. The claims reviewer identified Heathrow's connecting-flights guidance, the U.S. DOT baggage page, and GOV.UK liquid restrictions as relevant scoped sources.
- Days 47–50 and 60: visit purpose, accommodation, duration, and tickets are fictional truthful role-play responses, not a statement of admission criteria or a script guaranteeing entry.
- Days 51–55: baggage tracing, damage claims, reporting deadlines, and delivery availability need official airline or regulator context. Numbers, colors, dates, hotel names, and locations are fictional listening data. The last four digits in Day 55 are invented practice data; no full private phone number is present.
- Day 56: customs disclosure and food/gift restrictions are jurisdiction dependent; the lesson asks an officer and does not assign a universal allowance or exemption.
- Day 57: Door Three, train-machine positions, routes, card acceptance, taxi capacity, and fare arrangements are illustrative; actual airport guidance must be consulted for a real journey.
- Day 58: cancellation, rebooking, seat/bag transfer, and assistance terms need airline/jurisdiction-specific verification. The dialogue does not promise compensation or automatic arrangements.
- Independent review also checked speaker identifiers against the original snapshot: `S` is staff and `T` is traveler, including the staff-opening conversations in Days 47, 48, 49, and 53 and Day 60 A. The author's initial suspicion that these were reversed was incorrect and has been withdrawn; no dialogue or speaker IDs were changed.

Local structural checks passed for 19 valid JSON lessons, 57 resolvable evidence mappings, correct-choice/answer consistency, and all 475 nonempty guide translations. Independent semantic review, final speech duration/pronunciation, captions, and video checks remain separate gates.
