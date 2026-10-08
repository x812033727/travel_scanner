# Independent review: optional guided-practice response intervals

Reviewer: `airport_brief_independent_review`  
Date: 2026-10-08  
Workspace: `/workspace/airport-pr`  
Verdict: PASS. No P0–P3 defects identified within this narrow change.

## Scope

Reviewed the added `practice_pause_ms` validation/application, changed duration-plan pause calculation, corresponding tests, and documentation in `tools/video/airport_english/prepare.mjs`, `prepare.test.mjs`, and `README.md`. Applicable repository, video-production, and task-board rules were read during this review assignment. No source, staging, media, approval, or production-setting edits were made; this report is the only file written.

This review validates the optional capability. It does not choose any lesson's pause values, approve a future lesson edit, certify an exact 600-second final, or approve audio/video production. Canonical lessons currently contain no `practice_pause_ms` properties.

## Findings and evidence

1. **Strict optional field.** An omitted property retains 4,000 ms. An explicitly supplied value must be an integer in the inclusive range 4,000–5,000. Independently exercised 28 rejected inputs across Conversation A and B: null, undefined, values below/above bounds, negative, fractional, NaN, positive/negative infinity, string, boolean, object, array, and boxed number. Tested accepted values 4,000, 4,001, 4,500, 4,999, and 5,000. Invalid input fails before generation.
2. **Practice-only application.** Used the current real Day01 lesson as an in-memory fixture and varied all 18 A/B turns' response intervals. Compared every entire generated scene against the original after normalizing only the intended practice line's pause. All other scene fields, line IDs, words, voice configuration, and `audio_ref` references were identical. First listening, connection passes, quiz evidence, final listening, coaches, answer narration, and separate 4-second choose pauses were unchanged.
3. **Takes are reusable; timings are invalidated.** Complete serialized `planRequests` output remained byte-identical, covering request bodies, request IDs, request keys, individual take keys, and reference mapping. `speechHash` changed. The official `buildTimeline` was independently exercised with deterministic audio sample counts: spoken sample counts stayed identical while total frames increased by the expected sum of each line's rounded pause increment. This used synthetic sample counts, not a claim to have remeasured actual audio files.
4. **Pause total reflects the generated script.** The report's `fixed_practice_pause_seconds` matched the independently calculated sum of all actual guided-practice intervals plus three separate 4,000 ms choose intervals. The varied Day01 fixture added 8,250 requested milliseconds and 251 timeline frames, consistent with per-line rounding at 30 fps. The field remains explicitly inside a `text_estimate_only` plan, with measured fields null and `release_ready: false`.
5. **Old editorial review cannot authorize a pause edit.** `contentHash` includes the complete A/B turn objects, so adding or changing `practice_pause_ms` changes the reviewed content hash. Independent negative checks invoked the actual `planReviewBinding` with read-only, in-memory filesystem substitution for Day01's lesson. Values 4,000, 4,750, and 5,000 each failed with `teaching content changed after independent editorial review`. No disk lesson was changed. The English factual-content hash stayed unchanged, correctly distinguishing a timing edit from altered factual words.
6. **Current sources and staging remain current.** Regenerated all 60 lessons in memory and compared all 720 serialized artifacts to current on-disk bytes: all identical. The actual `assertReviewBindingCurrent` and `assertStagedReviewBinding` passed for all 60 episodes. Verified that all 60 canonical lessons omit the new optional field. No silent pause adjustment or automatic padding was applied.
7. **Documentation preserves the production constraints.** The README requires measured voice and installed branding, justified learner-response pacing, fresh independent lesson review, new bindings, and timing-dependent checks. It explicitly disallows using this option as automatic padding. It accurately documents reuse of identical synthesis requests while timing evidence must be regenerated.

## Operational limit

The allowed millisecond values are not restricted to 30 fps frame boundaries. The official timeline rounds each pause separately, so the pause-sum estimate must not be used as proof that the final is exactly 18,000 frames. Rebuild and inspect the measured timeline after any approved edit, then perform the required downstream checks. This is expected existing timeline behavior, not a defect in this change.

No full test suite, network service, paid request, or approval action was invoked during this independent review. The coordinator is running the broader required tests separately.

## Exact reviewed code

| File | SHA-256 |
| --- | --- |
| `tools/video/airport_english/prepare.mjs` | `2eb6ff8a221cabd6381dca07abdc44d835532ff1065690f9049280bb0731db30` |
| `tools/video/airport_english/prepare.test.mjs` | `66b6fe40cf6bbcf725a44f543bbe70adf22df7b90d9e605029877639895df4a6` |
| `tools/video/airport_english/README.md` | `2d387b466aff743997e44541b171f7931d92e6b1f59396288b93ad9d62a70550` |
