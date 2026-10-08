# verify-1: airport-english-day28

This file binds existing independent reviews to the matching generated script. It does not claim a new human review, a new web retrieval, audio review, production approval or publication approval.

Editorial reviewer: airport_lessons_02_21. Official-source and shared-instruction reviewer: airport_claims_review. Reviewed source date: 2026-10-08.

- [verify-22-41.md](../reviews/verify-22-41.md), SHA-256: `91b075da8fe14079ab79bebce2cbeebb7956a0660bf2804ea9c6447b6a9c1a65`.
- [claims-review.json](../reviews/claims-review.json), SHA-256: `73dc51b7b1e92bda19baac9a3195ebda4e6cb2cb6f58fd735f48971de0951168`.
- [claims-review.md](../reviews/claims-review.md), SHA-256: `fe1e4dcb3ca013bc9d427b36ae0450f583c4132ad70b063c953442f1522a87c2`.
- [verify-shared-instructions.md](../reviews/verify-shared-instructions.md), SHA-256: `b841038168857fc96d291a6e0f065de008cd4e609d052265babf60a20d41253d`.

Canonical teaching content: `9b3ceea2e897d3719e31a3d2b74030d731120ba972fe77c94c06aa422f7cc9ae`. English factual-content snapshot: `d324cc33d91bc2dd36ab9929d8de0eb631fb83a183df8f8e70e47d2df33b0818`. Current video.json: `992dec140f3a2ac250341aefec48bb9039cf8e182a3d14773ba4057bf1e3a32c`. Complete artifact and claim bindings are in [review-binding.json](review-binding.json).

| # | claim | where | URL | HTTP status | verdict | before -> after |
| --- | --- | --- | --- | --- | --- | --- |
| AE-C01 | Flight numbers, gates, counters, terminal layouts, distances, fares, airline names, meal choices, hotel names and personal itineraries are listening examples. | youtube.description; fictional dialogue and quiz | fictional examples; no external policy claim | not applicable | OUT OF SCOPE | unchanged |
| AE-C02 | Baggage allowances and gate-checking depend on the booking, airline, aircraft and capacity. | scene.claims:AE-C02; exact scene IDs in review-binding.json claims[1] | https://www.iata.org/en/programs/ops-infra/baggage/passenger-baggage-rules/ | 200 (recorded official retrieval) | CONFIRMED | unchanged |
| AE-C05 | Declare liquid medicine to screening staff and have supporting prescription information available; needed medicines should remain accessible. | scene.claims:AE-C05; exact scene IDs in review-binding.json claims[2] | https://www.gov.uk/hand-luggage-restrictions/essential-medicines-and-medical-equipment https://www.britishairways.com/content/information/travel-assistance/medical-conditions-and-pregnancy | 200 (recorded official retrieval) | CONFIRMED | unchanged |
| AE-C08 | A power bank must be removed before the bag is checked at the gate and kept in permitted cabin storage. | scene.claims:AE-C08; exact scene IDs in review-binding.json claims[3] | https://www.faa.gov/hazmat/packsafe/lithium-batteries | 200 (recorded official retrieval) | CHANGED | Tell the agent before handing over the bag. They will explain the applicable battery rules. -> Remove it before the bag is checked. Ask the agent how to carry it safely in the cabin. |
| AE-C21 | Report delayed/damaged baggage promptly, keep identifying documents/report numbers, describe the bag and confirm delivery details. | scene.claims:AE-C21; exact scene IDs in review-binding.json claims[4] | https://www.transportation.gov/lost-delayed-or-damaged-baggage https://www.iata.org/en/programs/ops-infra/baggage/passenger-baggage-rules/ https://www.britishairways.com/content/en/ca/information/baggage-essentials/lost-and-damaged-baggage/reporting-baggage-problems https://www.lufthansa.com/au/en/prepare-for-your-trip/baggage/baggage-irregularities/faq-baggage-delay | 200 (recorded official retrieval) | CONFIRMED | unchanged |

Claims: 5; CONFIRMED: 3; CHANGED and independently rechecked: 1; NOT FOUND: 0; fictional OUT OF SCOPE: 1.

No opinion/brief mismatch was identified in the cited reviews. Fictional flight numbers, gates, timings and arrangements are examples, not actual airport policies. Source restrictions may change; checked dates and jurisdiction/airline limits remain in the source ledger. No universal entry permission, baggage allowance or compensation is certified.

Second fact-check round required by more-than-three-factual-changes rule: no. This entry inherits completed source-review corrections; it makes no new factual edits.

Official lint on the current generated sources: 0 errors, 58 warnings. Warning details are in review-binding.json; warnings are not silently relabelled as cleared.

Listener findings and the actual scope of translation/quiz review remain in the cited independent reports. Common instructions allow learners to pause for long lines; final natural pace, number/letter pronunciation, multilingual slots, subtitles, measured 600-second duration, visual quality and final/package QA remain unverified. No approval record was created.
