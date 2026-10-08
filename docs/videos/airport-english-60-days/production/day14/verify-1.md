# verify-1: airport-english-day14

This file binds existing independent reviews to the matching generated script. It does not claim a new human review, a new web retrieval, audio review, production approval or publication approval.

Editorial reviewer: airport_lessons_42_60. Official-source and shared-instruction reviewer: airport_claims_review. Reviewed source date: 2026-10-08.

- [verify-02-21.md](../reviews/verify-02-21.md), SHA-256: `aa02a3dacbbbf14e781898486862aae0e19878831c6e8dab7d13a0271f0bbc6b`.
- [claims-review.json](../reviews/claims-review.json), SHA-256: `00acb437b7117f900ccbd3c33676c7be0761670c2345a3e05beb74b46ad35541`.
- [claims-review.md](../reviews/claims-review.md), SHA-256: `c288362d1f8d5fddacfbd673afbb425ac5a0c9697ef37fc90b07dcf896c4fb4b`.
- [verify-shared-instructions.md](../reviews/verify-shared-instructions.md), SHA-256: `b841038168857fc96d291a6e0f065de008cd4e609d052265babf60a20d41253d`.

Canonical teaching content: `1672a104957d3b28c6a80b6259687f853b67e4452bbc972da88a120413dce7a3`. English factual-content snapshot: `a41314bf6480b96728ad5a4ff16de2bbfd0d3cbde4837f71b6a212f285d6b045`. Current video.json: `5c226daa2a62d7ab4c9726bb2d39ba4df1485c09ed8af7e86c7a66b633d1519e`. Complete artifact and claim bindings are in [review-binding.json](review-binding.json).

| # | claim | where | URL | HTTP status | verdict | before -> after |
| --- | --- | --- | --- | --- | --- | --- |
| AE-C01 | Flight numbers, gates, counters, terminal layouts, distances, fares, airline names, meal choices, hotel names and personal itineraries are listening examples. | youtube.description; fictional dialogue and quiz | fictional examples; no external policy claim | not applicable | OUT OF SCOPE | unchanged |
| AE-C04 | Screening instructions can differ by checkpoint; follow staff and lane-specific procedures. | scene.claims:AE-C04; exact scene IDs in review-binding.json claims[1] | https://www.gov.uk/hand-luggage-restrictions/liquids https://www.heathrow.com/connecting-flights | 200 (recorded official retrieval) | CONFIRMED | unchanged |
| AE-C05 | Declare liquid medicine to screening staff and have supporting prescription information available; needed medicines should remain accessible. | scene.claims:AE-C05; exact scene IDs in review-binding.json claims[2] | https://www.gov.uk/hand-luggage-restrictions/essential-medicines-and-medical-equipment https://www.britishairways.com/content/information/travel-assistance/medical-conditions-and-pregnancy | 200 (recorded official retrieval) | CONFIRMED | unchanged |

Claims: 3; CONFIRMED: 2; CHANGED and independently rechecked: 0; NOT FOUND: 0; fictional OUT OF SCOPE: 1.

No opinion/brief mismatch was identified in the cited reviews. Fictional flight numbers, gates, timings and arrangements are examples, not actual airport policies. Source restrictions may change; checked dates and jurisdiction/airline limits remain in the source ledger. No universal entry permission, baggage allowance or compensation is certified.

Second fact-check round required by more-than-three-factual-changes rule: no. This entry inherits completed source-review corrections; it makes no new factual edits.

Official lint on the current generated sources: 0 errors, 60 warnings. Warning details are in review-binding.json; warnings are not silently relabelled as cleared.

Listener findings and the actual scope of translation/quiz review remain in the cited independent reports. Common instructions allow learners to pause for long lines; final natural pace, number/letter pronunciation, multilingual slots, subtitles, measured 600-second duration, visual quality and final/package QA remain unverified. No approval record was created.
