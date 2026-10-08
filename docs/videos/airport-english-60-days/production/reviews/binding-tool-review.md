# Independent review of airport editorial-evidence binding tool

Reviewer: `/root/airport_duration_review`, independent of the binding-tool author `airport_claims_review` and the production adapter author. Review date: 2026-10-08.

Decision: **PASS for source-review binding and currentness checks at the hashes below.** Required fixes remaining in this reviewed scope: none. This is neither media acceptance nor a production, audio, package or publication approval.

## Scope and method

Read the complete `review-bindings.mjs` implementation and its regression tests, the actual independent editorial reports and shared-instruction record, the factual-ledger structure, and the production adapter's role, replay and translated-audio routing. Checked how generated files enter the official lint/facts checks. This review concerns whether genuine existing text reviews are connected to the current source bytes; it is not a new semantic or native-language review of all lessons, a fresh retrieval of travel sources, or a complete review of the adapter or mixed-audio implementation.

## Findings resolved

The first implementation extracted editorial content hashes without checking a current PASS decision or reviewer identity. A historical hash could therefore survive an explicitly rejected or superseded review. The author added explicit machine-readable editorial decisions and reviewer validation, with regressions for missing, rejected, superseded, ambiguous and wrong-reviewer records. The factual ledger now also validates its schema, series, review type and reviewer instead of merely attributing every input ledger to the expected reviewer.

The original Day02–21 reviewer is no longer available. The final implementation preserves the original report and original reviewer identity, while a separate reviewer records the exact existing PASS-report byte hash. It does not impersonate the original signer or claim a fresh language review. Any change to that recorded report, including a withdrawal appended beneath its historical hash table, fails. Other editorial reports use the actual reviewer's current decision marker; the shared report documents that this marker is authoritative and must be changed when the decision is withdrawn or superseded. This is an explicit repository-evidence contract, not automated interpretation of arbitrary prose or cryptographic proof of reviewer identity.

## Currentness and provenance

- Canonical editorial hashes cover dialogue text, roles and translations, quiz choices/explanations/evidence IDs, all five-language guides and localized titles. The separate English factual hash binds the reviewed source content. A matching historical full-file hash is not falsely claimed after metadata changes.
- Claim text, accepted factual verdicts, official-source URLs and source dates must match the reviewed ledger. Referenced retrieval records require recorded HTTP 200 and a SHA-256 body identifier. Missing or unresolved facts fail. The tool reuses the cited retrieval evidence and explicitly does not claim a new fetch.
- Shared instructions and thumbnail wording must match the independent shared record. All twelve generated artifacts per episode are compared byte-for-byte with fresh preparation from the current sources, including role/replay maps, teaching-audio routes and all four translation files. The binding also records profile, lexicon and review hashes.
- Existing per-episode binding/verify files must match a newly computed binding exactly. A changed source, generated artifact or review cannot silently retain an old receipt. The selected batch is checked before any receipt is written; this guarantees no partial write caused by a failed validation, not transactional recovery from an unrelated filesystem failure.
- The generated `verify-1.md` cites real existing reviews, preserves their recorded dates and limitations, exposes official lint warnings, and distinguishes fictional examples from current travel claims. Both generated outputs explicitly deny production/release approval. No approval record, media file or publication call is created by this helper.

## Independent validation

- Ran `node --test tools/video/airport_english/review-bindings.test.mjs`: **11 passed, 0 failed, 0 skipped**. These use actual reviewed reports in temporary fixtures, including official facts-table acceptance and invalidation of each generated artifact.
- Ran a separate, independently written temporary harness with **18 adversarial cases**. Rejected English-source, translation, speaker-role, quiz-evidence, generated-video and generated-CC drift; a withdrawn legacy report; explicitly rejected/superseded/missing/duplicate/wrong-reviewer editorial records; claim-URL drift; a wrong factual reviewer; unresolved facts; missing retrieval evidence; changed shared instructions; and a failed multi-episode batch. The failed batch wrote no receipt. Production inputs were not mutated.
- Planned bindings for **all 60 current episodes in memory**: **720 generated artifacts matched**, with **0 official-lint errors**. Warnings remain recorded and do not become cleared merely because a binding exists.
- After the author wrote the per-episode bindings, independently ran `node tools/video/airport_english/review-bindings.mjs --check`: **60/60 current bindings passed**, with `approvals_created: false`, `media_created: false` and `release_ready: false`.
- Independently traced all **180 quiz replay sequences** to the lesson's reviewed evidence IDs, in order. Checked Traveler/Staff labels against the source T/S roles and replay references against the earlier original take. Checked **13,008 translated-track dialogue entries**: each retains the original English text, `speech_locale: en`, exact source-take identity and separate localized CC. These are generated-source checks, not proof of heard audio or rendered timing.

The actual 600-second cuts, selected translated teaching voices, timing/readability of final CC, pronunciation, branding, final video quality and official audio/final/package gates remain outside this review. No synthesis, production render, human listening, approval or publication was performed by this reviewer.

## Reviewed implementation bytes

| File | SHA-256 |
| --- | --- |
| `tools/video/airport_english/review-bindings.mjs` | `bd10cf88b911fccbd52d91ef37e82b14a394c1dd7c48ebca8aa753c079a63ef6` |
| `tools/video/airport_english/review-bindings.test.mjs` | `265502e2ac5764f4ba5589f23ac685fb7024d6521af6bdd4d96c248331e6a308` |
