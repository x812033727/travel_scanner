# verify-1: airport-english-day30

This file binds existing independent reviews to the matching generated script. It does not claim a new human review, a new web retrieval, audio review, production approval or publication approval.

Editorial reviewer: airport_lessons_02_21. Official-source and shared-instruction reviewer: airport_claims_review. Reviewed source date: 2026-10-08.

- [verify-22-41.md](../reviews/verify-22-41.md), SHA-256: `91b075da8fe14079ab79bebce2cbeebb7956a0660bf2804ea9c6447b6a9c1a65`.
- [claims-review.json](../reviews/claims-review.json), SHA-256: `73dc51b7b1e92bda19baac9a3195ebda4e6cb2cb6f58fd735f48971de0951168`.
- [claims-review.md](../reviews/claims-review.md), SHA-256: `fe1e4dcb3ca013bc9d427b36ae0450f583c4132ad70b063c953442f1522a87c2`.
- [verify-shared-instructions.md](../reviews/verify-shared-instructions.md), SHA-256: `b841038168857fc96d291a6e0f065de008cd4e609d052265babf60a20d41253d`.

Canonical teaching content: `a3406793915f8adb0dcb888fed0851693b6b34d375423615ffcbaca08b54f4ae`. English factual-content snapshot: `5e90a8586a63ca875de6a6dec1d7c0f14aed36e18dea4fa94d4987e639b8a6f1`. Current video.json: `539fca2364a26163c1e440d68d74c6e0c4ed652fa222b2db924db66c7a8f95da`. Complete artifact and claim bindings are in [review-binding.json](review-binding.json).

| # | claim | where | URL | HTTP status | verdict | before -> after |
| --- | --- | --- | --- | --- | --- | --- |
| AE-C01 | Flight numbers, gates, counters, terminal layouts, distances, fares, airline names, meal choices, hotel names and personal itineraries are listening examples. | youtube.description; fictional dialogue and quiz | fictional examples; no external policy claim | not applicable | OUT OF SCOPE | unchanged |
| AE-C09 | Underseat stowage depends on the seat's permitted storage configuration, restraint and clear aisle. | scene.claims:AE-C09; exact scene IDs in review-binding.json claims[1] | https://regulatorylibrary.caa.co.uk/965-2012/Content/Document%20Structure/04%20CAT/3%20AMC/AMC1%20CAT%20OP%20MPA%20160%20Stowage.htm https://www.iata.org/en/programs/ops-infra/baggage/passenger-baggage-rules/ | 200 (recorded official retrieval) | CHANGED | Yes, if it fits fully underneath and does not block the aisle. -> Yes, if the crew permits it and it fits fully under the seat without blocking the aisle. |
| AE-C12 | Follow seat-belt signs and crew directions; keep the belt fastened while seated, and avoid accessing bins during turbulence. | scene.claims:AE-C12; exact scene IDs in review-binding.json claims[2] | https://www.faa.gov/travelers/fly_safe/turbulence https://www.caa.co.uk/air-passengers/about-your-trip/cabin-safety/ https://www.jal.co.jp/jp/en/dom/boarding_attention/sudden-shake/ | 200 (recorded official retrieval) | CONFIRMED | unchanged |

Claims: 3; CONFIRMED: 1; CHANGED and independently rechecked: 1; NOT FOUND: 0; fictional OUT OF SCOPE: 1.

No opinion/brief mismatch was identified in the cited reviews. Fictional flight numbers, gates, timings and arrangements are examples, not actual airport policies. Source restrictions may change; checked dates and jurisdiction/airline limits remain in the source ledger. No universal entry permission, baggage allowance or compensation is certified.

Second fact-check round required by more-than-three-factual-changes rule: no. This entry inherits completed source-review corrections; it makes no new factual edits.

Official lint on the current generated sources: 0 errors, 58 warnings. Warning details are in review-binding.json; warnings are not silently relabelled as cleared.

Listener findings and the actual scope of translation/quiz review remain in the cited independent reports. Common instructions allow learners to pause for long lines; final natural pace, number/letter pronunciation, multilingual slots, subtitles, measured 600-second duration, visual quality and final/package QA remain unverified. No approval record was created.
