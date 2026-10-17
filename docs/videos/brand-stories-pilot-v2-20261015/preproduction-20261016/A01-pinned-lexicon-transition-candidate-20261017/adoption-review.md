# Independent offline adoption API review

Reviewer: `codex-independent-a01-lexicon-1017`. Date: 2026-10-17 (Asia/Taipei).

Verdict: **0 P1 / 0 P2 findings within the reviewed offline adoption API scope. Production remains HOLD.** This Markdown is an independent code/test report, not the evidence JSON accepted by `preparePinnedEvent`, an owner receipt, proof of host preflight or permission to resume production.

## Reviewed bytes

| File | SHA-256 |
| --- | --- |
| adopt-pinned.mjs | 6f1a59479fef4d91d108d3e7e7ee64da543b2794c657445fe5d255049710fd64 |
| adopt-pinned.test.mjs | ed925a11e0cbcd06107b96c254a016e64a8fe3b48893b4b753ad42cffb8e0837 |
| required-runtime.json | 32bb48d5664327806852d681f12c0427fe32f7b412aabaf02043e202c301a3af |

Read the complete API and tests with the previously reviewed transition/readback contract. The runtime manifest binds exactly `tools/video/core/lexicon-store.mjs`, `tools/video/automation/story.mjs` and `tools/video/automation/flow.mjs`; these are deployment prerequisites, not a complete deployed-tree attestation.

## Findings

The API plans the exact before-source transition, checks plan SHA and structurally bound external review/owner-record bytes, verifies the three runtime hashes, and requires separate non-nested document/work roots. It holds the existing project and shared-writer leases while comparing a fresh copied source against the plan and publishing. A scoped STOP is created if absent and retained. Work/docs intents precede immutable evidence and snapshot files, followed by auto state and then the immutable current pointer. Exact captured-transition readback precedes the committed receipt and clearing the two fences. It performs no provider/DB call, STOP removal, merge, deployment or release.

Recovery requires the committed transaction record, matching plan, unchanged scoped STOP hash, any surviving fence bytes, no other work intent and exact transition/source readback before clearing surviving fences. A pre-commit interruption remains held for separate review. Both ordinary commit and committed recovery return HOLD and release false.

The synthetic runtime override is gated to both target roots under the OS temporary directory and fixture options; the underlying baseline validation still requires the original synthetic marker when historical pins/hashes are overridden. Test runtime files are explicit inert synthetic bytes rather than copied machine runtime paths. This fixture route is test admission, not a production authorization channel.

Receipt names, `owner_approval_ref` and the copied `operator`/`reviewer` values are caller-controlled strings. They bind records; they do not authenticate identity or owner authority. The host caller must separately verify real action authorization, own the deployment lock, and establish current DB/stage-job/budget preflight before invoking this API. In particular, the API does not make the currently reported deployment-lock/running-stage condition safe for writes.

## Independently executed verification

Bundled Node 24.19: `node --test adopt-pinned.test.mjs` — **3 passed, 0 failed**, including all seven interruption boundaries:

- work intent; docs intent; immutable files; auto state; current pointer; committed receipt; docs fence cleared.

The tests verify successful exact split-root transition with STOP and shared-dictionary preservation; retained STOP/work fence and refusal of ordinary retry after each interruption; refusal to recover pre-commit phases; recovery only for the two fully committed phases; and refusal of runtime/source drift. These are three top-level tests with nested scenarios, not seven separate test files or a real process/power-loss campaign.

## Limits and follow-up gates

The tests simulate interruptions by throwing at checkpoints, after synchronous calls complete. They do not reproduce a killed process, torn filesystem write, cross-container lease takeover, reboot, power loss or production mount durability. Captured-source snapshots and receipts are retained by the API for investigation; this review does not authorize their cleanup. Readback validates exact copied source bytes and the existing transition contract, not a complete independent run of every production worker/media consumer.

No real host adoption, true 81st event, current host capture, uncertain-job disposition or script approval was created by this review. Before any production action, the caller must satisfy the external deployment-lock/DB/job gates, verify fresh exact source and runtime bytes, authenticate actual authorization, and independently read back the completed held transition. The later 81-to-82 narrative transition, factual/listening/storytelling review and paid-production gates remain separate requirements. STOP must remain until those gates authorize its removal through a separate action.

Only this new report was written. Implementation and historical reviews were not edited; no host, merge or paid action was performed.
