# verify-1: airport-english-day08

This file binds existing independent reviews to the matching generated script. It does not claim a new human review, a new web retrieval, audio review, production approval or publication approval.

Editorial reviewer: airport_lessons_42_60. Official-source and shared-instruction reviewer: airport_claims_review. Reviewed source date: 2026-10-08.

- [verify-02-21.md](../reviews/verify-02-21.md), SHA-256: `aa02a3dacbbbf14e781898486862aae0e19878831c6e8dab7d13a0271f0bbc6b`.
- [claims-review.json](../reviews/claims-review.json), SHA-256: `73dc51b7b1e92bda19baac9a3195ebda4e6cb2cb6f58fd735f48971de0951168`.
- [claims-review.md](../reviews/claims-review.md), SHA-256: `fe1e4dcb3ca013bc9d427b36ae0450f583c4132ad70b063c953442f1522a87c2`.
- [verify-shared-instructions.md](../reviews/verify-shared-instructions.md), SHA-256: `b841038168857fc96d291a6e0f065de008cd4e609d052265babf60a20d41253d`.

Canonical teaching content: `abeb6eb0c1e6d5011adbbd4d81eb65908fdd54b1e661b2012e7a93f639993dfe`. English factual-content snapshot: `b5748e5793c74673498ec55b22e7fad56622464bb116849b3c20651a502f3856`. Current video.json: `ab71b466f53501166ea3e238f57a019c644b9d0fa3ef3170e06a383fd2c1fec9`. Complete artifact and claim bindings are in [review-binding.json](review-binding.json).

| # | claim | where | URL | HTTP status | verdict | before -> after |
| --- | --- | --- | --- | --- | --- | --- |
| AE-C01 | Flight numbers, gates, counters, terminal layouts, distances, fares, airline names, meal choices, hotel names and personal itineraries are listening examples. | youtube.description; fictional dialogue and quiz | fictional examples; no external policy claim | not applicable | OUT OF SCOPE | unchanged |
| AE-C02 | Baggage allowances and gate-checking depend on the booking, airline, aircraft and capacity. | scene.claims:AE-C02; exact scene IDs in review-binding.json claims[1] | https://www.iata.org/en/programs/ops-infra/baggage/passenger-baggage-rules/ | 200 (recorded official retrieval) | CONFIRMED | unchanged |
| AE-C03 | Keep the baggage receipt; remove old routing tags so scanners use the current tag. | scene.claims:AE-C03; exact scene IDs in review-binding.json claims[2] | https://www.gatwickairport.com/passenger-guides/preparing-hold-baggage.html https://www.lufthansa.com/au/en/prepare-for-your-trip/baggage/baggage-irregularities/faq-baggage-delay | 200 (recorded official retrieval) | CONFIRMED | unchanged |
| AE-C17 | Transfer routing and baggage collection depend on itinerary/local process; a final-destination bag tag does not always avoid reclaim/recheck. | scene.claims:AE-C17; exact scene IDs in review-binding.json claims[3] | https://www.heathrow.com/connecting-flights https://www.transportation.gov/lost-delayed-or-damaged-baggage | 200 (recorded official retrieval) | CONFIRMED | unchanged |
| AE-C21 | Report delayed/damaged baggage promptly, keep identifying documents/report numbers, describe the bag and confirm delivery details. | scene.claims:AE-C21; exact scene IDs in review-binding.json claims[4] | https://www.transportation.gov/lost-delayed-or-damaged-baggage https://www.iata.org/en/programs/ops-infra/baggage/passenger-baggage-rules/ https://www.britishairways.com/content/en/ca/information/baggage-essentials/lost-and-damaged-baggage/reporting-baggage-problems https://www.lufthansa.com/au/en/prepare-for-your-trip/baggage/baggage-irregularities/faq-baggage-delay | 200 (recorded official retrieval) | CONFIRMED | unchanged |

Claims: 5; CONFIRMED: 4; CHANGED and independently rechecked: 0; NOT FOUND: 0; fictional OUT OF SCOPE: 1.

No opinion/brief mismatch was identified in the cited reviews. Fictional flight numbers, gates, timings and arrangements are examples, not actual airport policies. Source restrictions may change; checked dates and jurisdiction/airline limits remain in the source ledger. No universal entry permission, baggage allowance or compensation is certified.

Second fact-check round required by more-than-three-factual-changes rule: no. This entry inherits completed source-review corrections; it makes no new factual edits.

Official lint on the current generated sources: 0 errors, 59 warnings. Warning details are in review-binding.json; warnings are not silently relabelled as cleared.

Listener findings and the actual scope of translation/quiz review remain in the cited independent reports. Common instructions allow learners to pause for long lines; final natural pace, number/letter pronunciation, multilingual slots, subtitles, measured 600-second duration, visual quality and final/package QA remain unverified. No approval record was created.
