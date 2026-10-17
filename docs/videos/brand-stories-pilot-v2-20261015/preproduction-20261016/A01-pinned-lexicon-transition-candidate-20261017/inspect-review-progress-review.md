# Independent read-only review-progress inspector review

Reviewer: codex-independent-a01-lexicon-1017. Date: 2026-10-17 (Asia/Taipei).

Final verdict: **0 remaining P1 / P2 in the reviewed read-only integrity scope.** Bound inspect-review-progress.mjs SHA-256: 29aa011a76e0841c088e2879e8c3e685871d4dd9172b0585cc56e20f8270b0bb. Independent no-model harness SHA-256: e4b133f695fcb788ba7c086a39fec875b459624b66587d957b01856cefcf6e50. No host, provider or actual review stage was executed by this reviewer.

## Findings and fixes preserved

The initially supplied d9db4441978f4edb359b5b0262b30fe05a07f61007fd6263d19070816e31d8bd version had two P2 gaps identified by independent code review: event-ID visitation alone permitted a source cycle returning to an older source, and adoption artifacts were only required to be a nonempty array rather than bound to the corresponding event's exact after-source hashes. The author fixed these with visited source hashes and a complete unique canonical-path-to-after-tuple proof map (13 ordinary files, skipping a genuinely null optional verify input).

A further P2 identity precondition was identified: validateRunReceipt assumes the containing journal record was already validated by the normal store reader. The inspector had not checked schema1, UUID request_key, drama format or site string/URL shape. The final revision supplies those checks. It also requires raw request canonical equality to normalizeRun, source_hash equality, matching source-hash journal filename, canonical receipt_hash, matching succeeded row scope/status and real adoption proof shape. Site validation allows plain http/https without embedded credentials/query/fragment; it is a format check, not authentication of that site, account or person.

## Independently executed final cases

Using bundled Node24.19, independently executed the harness bound to the final29aa source. It uses the actual saved80/81/82 captures for the real baseline verification and separate OS Temp progress clones for synthetic test edges. No original capture file is changed. All six cases completed as expected:

- Actual snapshot82 with no new edge: PASS at82 links and source729a1c47e955448968908cd6ba2a0f8ff4257c0a7a1f951b0de744696c8d5a8d, HOLD and paid false.
- Valid single synthetic adopted/verifier-story edge with a full canonical artifact-proof set: PASS.
- Two-edge source cycle A82→B→A82, using distinct event IDs and otherwise complete proof sets: rejected RECHECK_SOURCE_CYCLE.
- Wrong adopted artifact hash, with outer journal/index hashes recomputed to remain structurally consistent: rejected ADOPTION_PROOF_SOURCE_MISMATCH.
- Renamed journal file with matching index filename adjustment: rejected JOURNAL_REQUEST_HASH_INVALID.
- Non-UUID request key, consistently copied into the synthetic receipt and with hashes recomputed: rejected JOURNAL_IDENTITY_INVALID.

Synthetic journals deliberately use synthetic instructions/provider/result/site and are test data only. They are not genuine review receipts or evidence of a model call. The tests demonstrate local acceptance/rejection logic, not a backend lookup, source fact verification or provider identity check. The earlier e2da increment also independently passed the same first five cases; final29aa reran those cases plus malformed-key rejection.

## Reviewed integrity scope

The inspector first requires the exact verified82 baseline. It preserves every baseline path, hashes all immutable baseline source/history files, allows only the declared current canonical worker outputs/shared dictionary to change, and allows new files only under new audit directories. It checks event schema/result/install receipt, source-map digest edges, journal bytes/names/status/scope/request/receipt identity and canonical digest, exact after-source artifact proofs and the complete event file set. It traverses exactly one next source edge per step, rejects repeated event/source identities and requires the final complete pinned-source tuple to equal actual current files. The pinned snapshot tree remains immutable while shared-dictionary drift is outside that selected pronunciation source. Its result stays HOLD with paid false.

The proof comparison correctly uses each event's after tuple rather than today's files, because later legitimate review units may have changed the same canonical artifacts. The baseline keeps old82 evidence unchanged. This report does not independently assert any number of actual new production units; the no-new-edge real capture and synthetic fixtures were the executed inputs.

## Limitations

This is offline integrity verification of supplied trusted captures and locally self-consistent receipt records. normalizeRun/sourceHash/canonical receipt_hash and validateRunReceipt are structural binding checks, not digital signatures or independent server authentication. The capture's trusted acquisition and any DB/job/provider reconciliation remain separate evidence. Formal content verdicts, deleted-scene claim interpretation, narrative quality, listening/audio, budget and owner approval are not determined here.

A malformed/partial new event or unexpected file rejects the readback; it is not permission to delete evidence or retry. No STOP/hold/file mutation, paid call or production operation exists in this inspector. Only this new report and the repo-external independent harness/bound test copy were written by the reviewer; implementation was not edited.
