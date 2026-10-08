# Days 22–41 editorial revision

Date: 2026-10-08. Author: Codex AI agent `airport_lessons_22_41`.
Status: **editorial revision ready for independent review**. This is an author
record, not independent verification, human language review, measured voice
timing, rendered-video QA, or production approval.

## Changes and checks

- Read every A/B exchange and all 60 question/answer pairs in Days 22–41.
  Added explicit `evidence_ids` for every question. No keyword scoring or
  assumption that the first two questions refer to conversation A remains in
  these lesson records.
- Added episode-specific `hook`, `goal`, `recap`, `comment`, and `subscribe`
  guides in the ordered locales `[en, zh-Hant, zh-Hans, ja, ko]`: 100 guide
  utterances, 500 localized strings. Hooks and goals explain a concrete task;
  recaps provide a usable phrase or the promised answer. Comment prompts ask
  learners for their own preferences or practice needs, not another quiz.
  Subscription lines name the next lesson in the existing curriculum, including
  Day 42's onward-flight lesson after Day 41.
- All English guide utterances contain at most 21 whitespace-delimited words.
  This is a writing-length check, **not** evidence of a spoken-duration pass.
  The production timeline must measure every language and keep the authorized
  600-second total without cutting phrases or adding empty padding.
- Confirmed 12 unique dialogue turn IDs per lesson, five locales per text
  array, `text == all[0]`, `question == all[0]`, and that every selected answer
  equals `choices[correct]`. Every evidence ID resolves to a real dialogue turn.
  Re-read each selected exchange for actual answer support.
- All dialogue remains English in alternative teaching-audio tracks. The four
  dialogue translations in these records are for selectable CC.

## Explicit answer-bearing replay map

| Day | Question 1 | Question 2 | Question 3 |
| --- | --- | --- | --- |
| 22 | A01, A02 | A03, A04 | B01, B02 |
| 23 | A01, A02 | B01, B02 | B05, B06 |
| 24 | A01, A02 | A03, A04 | B03, B04 |
| 25 | A01, A02 | B01, B02 | B03, B04 |
| 26 | A03, A04 | A03, A04 | B03, B04 |
| 27 | A01, A02 | A03, A04 | B03, B04 |
| 28 | A01, A02 | A03, A04 | B05, B06 |
| 29 | A03, A04 | A05, A06 | B01, B02 |
| 30 | A01, A02 | A05, A06 | B03, B04 |
| 31 | A03, A04 | A05, A06 | B01, B02 |
| 32 | A01, A02 | B01, B02 | B05, B06 |
| 33 | A01, A02 | B01, B02 | B03, B04 |
| 34 | A01, A02 | A03, A04 | B03, B04 |
| 35 | A01, A02, A03 | A03, A04 | B02, B03 |
| 36 | A01, A02 | A03, A04 | B01, B02 |
| 37 | A01, A02 | B01, B02 | B04, B05 |
| 38 | A01, A02 | A03, A04 | B05, B06 |
| 39 | A05, A06 | A05, A06 | B04, B05 |
| 40 | A03, A04 | A05, A06 | B05, B06 |
| 41 | A01, A02 | B01, B02 | B01, B02 |

Known wrong-replay cases from the previous audit corrected by these mappings:
Day 23 Q2; Day 25 Q2/Q3; Day 32 Q2; Day 33 Q2; Day 37 Q2/Q3; Day 40 Q3;
Day 41 Q2. Day 35 Q1 deliberately uses three turns because "no ice" and the
selection of still water occur in different traveler utterances. Day 37 Q3
includes the replacement offer and the traveler's explicit confirmation that
it works. Day 39 Q3 includes the medication question and its location answer.

## Text edits beyond the new guides and evidence IDs

All edits below update English and all four CC translations. No answer index,
answer choice, or correct-answer explanation changed.

| ID | Edit | Reason |
| --- | --- | --- |
| Day22 Q1 | “Which group is boarding now?” | The source establishes the group currently boarding; it does not establish the first group of the entire boarding process. |
| Day28 B02 | “Remove it before the bag is checked. Ask the agent how to carry it safely in the cabin.” | A power bank must be removed before gate checking; merely asking about unspecified rules omitted the immediate action. |
| Day30 A06 | “Yes, if the crew permits it and it fits fully under the seat without blocking the aisle.” | Under-seat stowage depends on the seat and crew instructions as well as size and aisle clearance. |
| Day31 B02 | “Lift the metal buckle to release it. To tighten it, fasten it and pull the loose end of the strap.” | Separates release from tightening and makes fastening before tightening explicit. B01 and the new recap identify the demonstrated type and aircraft-specific instructions. |
| Day41 Q2 | “What does the screen in the second conversation show?” | Avoids implying a second physical screen has already been shown when the intended reference is the second conversation. |

## Claims requiring independent official-source verification

Gate numbers, destinations, seat numbers, meals, times, named passengers, and
where a fictional desk or display stands are invented listening examples. They
must be presented as scenario details, not current airport or airline facts.
The English recaps for Days 25, 29, 36, and 41 explicitly identify such details
as belonging to this conversation.

The separate `airport_claims_review` agent supplied the following source
findings during revision. That agent's source capture and independent claims
record are the verification evidence; this author report does not claim its
own independent fetch.

- **Day 28 B01/B02, batteries:** the reviewer reported a successful official
  FAA fetch on 2026-10-08 confirming power banks/spare lithium batteries remain
  in the cabin, including when a bag is gate checked; terminals require
  protection and stricter carrier limits may apply. Source:
  <https://www.faa.gov/hazmat/packsafe/lithium-batteries>.
- **Day 31 B01/B02, buckle operation:** the reviewer reported a successful
  official Air Cambodia passenger-briefing fetch on 2026-10-08 supporting
  fastening, pulling the free strap to tighten, and lifting the metal tab to
  release the demonstrated belt. Source:
  <https://www.aircambodia.com/en/travel-advise>. This does not make the mechanism
  universal across every restraint; follow the aircraft's demonstration.
- **Day 32 B05/B06 and recap, trapped phone:** the reviewer reported an official
  TTCAA page supporting not moving the seat and contacting crew immediately.
  Source: <https://caa.gov.tt/safety-security-2/cabin-safety/passenger-information/>.

Remaining source-sensitive points for the independent review to cover:

| Days | Statements to verify or preserve as conditional scenario instructions |
| --- | --- |
| 22–23 | Boarding group order, companion assistance, family boarding, and stroller collection vary by carrier, airport, and flight; the dialogue directs learners to the staff. |
| 24–27 | A gate can close before scheduled departure. Delays and estimated times can change; a connection is not promised to wait. No invented number is a universal cutoff. |
| 28 | Cabin/checked-baggage restrictions and essential-item carriage; retain explicit power-bank removal and staff confirmation. |
| 30–32 | Seat-specific baggage stowage; safety-card/exit guidance; following the demonstration; seat-belt use while seated; permitted device settings/charging; reporting hot devices; trapped-phone response. |
| 33 | An entertainment-screen reset is a fictional system-specific action, not a guarantee that every aircraft's seat controls are independent. |
| 34–37 | Meal availability, vegetarian ingredients, allergy cross-contact, labels, special meals, blankets and headphones vary. No allergy-free guarantee or medical treatment advice is offered. |
| 38 | Remain seated with the belt sign on; arrival-form requirements depend on destination/current official instructions; do not invent missing passenger details. |
| 39 | Inform crew promptly about symptoms or breathing difficulty, describe known conditions and medication location, and follow crew instructions. No diagnosis or dosing advice is included. |
| 40 | Seat belts, stowing belongings/larger devices, closed overhead bins during turbulence, interrupted service, and changing device settings only when crew permits. |
| 41 | Transfer routes and document checks differ by airport/itinerary; the displayed route is a fictional example, not a universal immigration or baggage instruction. |

## Remaining production work

The independent reviewer subsequently requested a stricter three-sentence
outro. All 20 episodes now use one personal comment question without an extra
"tell us" sentence, one reasoned subscription sentence in Japanese and Korean
as well as the other locales, and one recap sentence per locale. Reported
questions within a teaching sentence remain part of that one utterance.
Day 26's hook now attributes the 30-minute departure assumption to the traveler;
Day 32's recap includes calling the crew as well as not moving a seat with a
trapped phone; Day 41's recap directly practices asking for the departures
screen. The independent reviewer must bind its review to these final records.

Independent English/content review and all-language review must check the
revised records. Synthesis, measured timing in five audio tracks, speech
verification, new CC segmentation, rendered safe-area/readability review,
loudness/codec QA, and the final hash-bound review all remain outside this
authoring subtask. Existing media must not be relabeled as corrected merely
because these lesson records changed.
