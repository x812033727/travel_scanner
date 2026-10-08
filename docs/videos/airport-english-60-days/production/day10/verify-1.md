# verify-1: airport-english-day10

This file binds existing independent reviews to the matching generated script. It does not claim a new human review, a new web retrieval, audio review, production approval or publication approval.

Editorial reviewer: airport_lessons_42_60. Official-source and shared-instruction reviewer: airport_claims_review. Reviewed source date: 2026-10-08.

- [verify-02-21.md](../reviews/verify-02-21.md), SHA-256: `aa02a3dacbbbf14e781898486862aae0e19878831c6e8dab7d13a0271f0bbc6b`.
- [claims-review.json](../reviews/claims-review.json), SHA-256: `00acb437b7117f900ccbd3c33676c7be0761670c2345a3e05beb74b46ad35541`.
- [claims-review.md](../reviews/claims-review.md), SHA-256: `c288362d1f8d5fddacfbd673afbb425ac5a0c9697ef37fc90b07dcf896c4fb4b`.
- [verify-shared-instructions.md](../reviews/verify-shared-instructions.md), SHA-256: `b841038168857fc96d291a6e0f065de008cd4e609d052265babf60a20d41253d`.

Canonical teaching content: `6ccd4ec65b1c87c36ab1a8fa04ed5ad739a00fb3158bdfe0fd2beab5eacf641d`. English factual-content snapshot: `76b53dc47104ae4eb529a56f06eef81c3a3564d80768f78bf62f0b8ac21b7dcd`. Current video.json: `51ae2ba4635f280228aae7046c084bd3e1d726b3299d2db564e354fcaafa71cf`. Complete artifact and claim bindings are in [review-binding.json](review-binding.json).

| # | claim | where | URL | HTTP status | verdict | before -> after |
| --- | --- | --- | --- | --- | --- | --- |
| AE-C01 | Flight numbers, gates, counters, terminal layouts, distances, fares, airline names, meal choices, hotel names and personal itineraries are listening examples. | youtube.description; fictional dialogue and quiz | fictional examples; no external policy claim | not applicable | OUT OF SCOPE | unchanged |
| AE-C06 | Board according to the assigned group and crew instructions; assistance and stroller arrangements require confirmation. | scene.claims:AE-C06; exact scene IDs in review-binding.json claims[1] | https://www.britishairways.com/content/information/checking-in-and-boarding/boarding https://www.aa.com/web/i18n/travel-info/boarding-process.html | 200 (recorded official retrieval) | CONFIRMED | unchanged |
| AE-C07 | Boarding/gate closure occurs before departure; departure time is not the latest gate-arrival time. | scene.claims:AE-C07; exact scene IDs in review-binding.json claims[2] | https://www.aa.com/web/i18n/travel-info/boarding-process.html | 200 (recorded official retrieval) | CONFIRMED | unchanged |

Claims: 3; CONFIRMED: 2; CHANGED and independently rechecked: 0; NOT FOUND: 0; fictional OUT OF SCOPE: 1.

No opinion/brief mismatch was identified in the cited reviews. Fictional flight numbers, gates, timings and arrangements are examples, not actual airport policies. Source restrictions may change; checked dates and jurisdiction/airline limits remain in the source ledger. No universal entry permission, baggage allowance or compensation is certified.

Second fact-check round required by more-than-three-factual-changes rule: no. This entry inherits completed source-review corrections; it makes no new factual edits.

Official lint on the current generated sources: 0 errors, 60 warnings. Warning details are in review-binding.json; warnings are not silently relabelled as cleared.

Listener findings and the actual scope of translation/quiz review remain in the cited independent reports. Common instructions allow learners to pause for long lines; final natural pace, number/letter pronunciation, multilingual slots, subtitles, measured 600-second duration, visual quality and final/package QA remain unverified. No approval record was created.
