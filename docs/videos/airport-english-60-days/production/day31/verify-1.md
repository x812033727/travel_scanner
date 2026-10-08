# verify-1: airport-english-day31

This file binds existing independent reviews to the matching generated script. It does not claim a new human review, a new web retrieval, audio review, production approval or publication approval.

Editorial reviewer: airport_lessons_02_21. Official-source and shared-instruction reviewer: airport_claims_review. Reviewed source date: 2026-10-08.

- [verify-22-41.md](../reviews/verify-22-41.md), SHA-256: `91b075da8fe14079ab79bebce2cbeebb7956a0660bf2804ea9c6447b6a9c1a65`.
- [claims-review.json](../reviews/claims-review.json), SHA-256: `00acb437b7117f900ccbd3c33676c7be0761670c2345a3e05beb74b46ad35541`.
- [claims-review.md](../reviews/claims-review.md), SHA-256: `c288362d1f8d5fddacfbd673afbb425ac5a0c9697ef37fc90b07dcf896c4fb4b`.
- [verify-shared-instructions.md](../reviews/verify-shared-instructions.md), SHA-256: `b841038168857fc96d291a6e0f065de008cd4e609d052265babf60a20d41253d`.

Canonical teaching content: `b9d26d39d01b671ea5d34edb8c54fa303a3d0339fd945c2ba2ca51b571902d11`. English factual-content snapshot: `e632e1b7cf53750402b748ef3e8c06bfeb06fbbac56355be5b0f9a79401c6a99`. Current video.json: `97c58a6396d2ba29939592c55ce3633ff4656fe35ea1657fb01583c2295c03ea`. Complete artifact and claim bindings are in [review-binding.json](review-binding.json).

| # | claim | where | URL | HTTP status | verdict | before -> after |
| --- | --- | --- | --- | --- | --- | --- |
| AE-C01 | Flight numbers, gates, counters, terminal layouts, distances, fares, airline names, meal choices, hotel names and personal itineraries are listening examples. | youtube.description; fictional dialogue and quiz | fictional examples; no external policy claim | not applicable | OUT OF SCOPE | unchanged |
| AE-C10 | Listen to the safety demonstration, read the aircraft's card, locate exits in both directions and ask crew if unclear. | scene.claims:AE-C10; exact scene IDs in review-binding.json claims[1] | https://www.caa.co.uk/air-passengers/about-your-trip/cabin-safety/ | 200 (recorded official retrieval) | CONFIRMED | unchanged |
| AE-C11 | On the demonstrated lift-tab buckle, lift to release; fasten and pull the loose strap to tighten. | scene.claims:AE-C11; exact scene IDs in review-binding.json claims[2] | https://www.aircambodia.com/en/travel-advise | 200 (recorded official retrieval) | CHANGED | Lift the metal buckle to release it, then pull the strap to adjust the fit. -> Lift the metal buckle to release it. To tighten it, fasten it and pull the loose end of the strap. |

Claims: 3; CONFIRMED: 1; CHANGED and independently rechecked: 1; NOT FOUND: 0; fictional OUT OF SCOPE: 1.

No opinion/brief mismatch was identified in the cited reviews. Fictional flight numbers, gates, timings and arrangements are examples, not actual airport policies. Source restrictions may change; checked dates and jurisdiction/airline limits remain in the source ledger. No universal entry permission, baggage allowance or compensation is certified.

Second fact-check round required by more-than-three-factual-changes rule: no. This entry inherits completed source-review corrections; it makes no new factual edits.

Official lint on the current generated sources: 0 errors, 60 warnings. Warning details are in review-binding.json; warnings are not silently relabelled as cleared.

Listener findings and the actual scope of translation/quiz review remain in the cited independent reports. Common instructions allow learners to pause for long lines; final natural pace, number/letter pronunciation, multilingual slots, subtitles, measured 600-second duration, visual quality and final/package QA remain unverified. No approval record was created.
