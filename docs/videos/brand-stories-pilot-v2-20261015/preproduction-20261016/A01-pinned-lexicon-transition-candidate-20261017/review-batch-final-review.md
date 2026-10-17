# Independent final bounded review driver assessment

Reviewer: codex-independent-a01-lexicon-1017. Date: 2026-10-17 (Asia/Taipei).

Verdict: **0 remaining P1 / P2 findings in the reviewed final driver/caller scope.** The initial P1 and two P2 findings are resolved in the bound revision. This is code and no-model control-flow validation; it does not report any real verifier/listener/narrative outcome or accept a script/media gate.

## Bound revisions

- review-batch.mjs and private review-batch-r3.mjs: SHA-256 5a20e967d6ed3c620cd7c4af49adc5a90f01cfba1f875f8e7d1658338ee4df19.
- review-run-host-r4.sh: SHA-256 af6ea8e1f082334af653558ceda68438a41f763daab230ba7e4a45aec12a8028.
- Independent harness, outside the repository: review-batch-independent-harness.mjs, SHA-256 5c64ea3c9b7634cd34d5e3c92aed3c7dbcaded10ea0e1252f36c7ebc2681e3ba.

Historical initial findings remain in review-batch-initial-findings.md and are not overwritten.

## Resolved findings

The final driver requires durable_stage_runs=true before STOP removal or stage dispatch. Actual Automation.block invocations set didBlock even when their reason equals the original blocked text; halted/skipped stop subsequent units. The separate pre-loop relint was removed, so the first actual checker performs the merged-source rebuild in the same real-model unit.

Every unit now captures the exact pinned before-source and durable work intent. A successful stage's artifacts are saved first; real artifact path/hash proofs are given to the installed api.adoptRuns, whose semantics were read independently. The now-adopted raw successful journal bytes are copied unchanged to a new immutable audit event with before/after source maps and file hashes. The audit/raw files and source are read back, an after capture and committed record are saved, and only then are consumed runs settled. The initial loss of source-edge/raw-journal evidence before settle is therefore addressed. Pending requests stay within the same unit/intent and retain their durable journal; exceptions preserve evidence and restore STOP.

## Independent no-model execution

Independently created fresh OS Temp split-root clones of the actual snapshot82. The harness used the real per-story lexicon reader, project leases, source-capture collector and exact82 verifier against the real reviewed 80/81 evidence. Only Automation/client/advanceStory were replaced with controlled mock model responses. The driver source was bound to the exact5a20 SHA before transformation.

All five cases passed:

1. Audit-before-settle: the mock settlement asserts immutable audit/index, original journal copy and committed unit record already exist before removing the original journal; real artifact-proof hashes are checked.
2. Same block reason: an actual block callback using unchanged text ends after one unit.
3. Durable mode false: rejects before STOP removal or any model-stage attempt; STOP remains exact.
4. Pending: two attempts reuse one retained journal/request key, create one successful answer and one settlement.
5. retryLater/halt: one successful unit is audited/settled, then no second stage is dispatched.

Every case preserved the original test STOP bytes. No network, provider, host or real model request was made. The mock stage's receipt shape is sufficient for the driver guard but is not a real backend-signed receipt; this harness does not retest the API's durable receipt cryptography or actual provider behavior. For Windows portability the harness skips only POSIX directory fsync and shortens pending sleep from5s to0; neither change was made to implementation. Thus the tests do not prove Linux power-loss durability or real server timing. Results and retained temporary clone path are in this reviewer's execution output; all five were independently observed PASS.

## Driver and host caller boundaries

The five parent levels resolve the fixed POSIX payload layout correctly. The driver imports installed runtime code, fixes A01/drama scope, admits only verifier/story, listener/story and verifier/narrative stages, rejects writer/media, verifies a project lease before units, and retains state.status=blocked. Installed stage fences honor both scoped and global STOP. Bounded units/requests/polls and finally/signal STOP restoration remain. SIGKILL/host failure cannot run finally; a partial unit must be reconciled from retained intent/before capture/journal under the held host release, never treated as permission to retry blindly. The unchanged driver cannot be simply rerun from the initial82 precondition after a partially or fully progressed batch; a later batch needs a freshly reviewed current audit tip.

Read the complete r4 host caller and independently reran bash -n: PASS, exact hash above. The two caller P2 gaps were fixed: after acquiring its own hold under all four locks it verifies the actual container-stage executable's5a20 hash, and it checks A01 queued/running jobs are zero before dispatch as well as afterward. It still requires exact clean deployed HEAD, no previous global hold, exact pre-budget bytes, private release/log, restored scoped STOP and successful post-budget readback before clearing only its own hold. The DB count checks are read-only and A01-scoped, not a globally idle proof or disposition of old uncertain records. The parent reports action-time checks passed and a real batch began; this reviewer did not execute or independently observe that host process and issues no claim about its eventual review results.

## Non-claims

No owner identity, factual truth, listening quality, storytelling PASS, pilot script receipt, actual TTS duration, media acceptance or paid authorization is supplied by this report. The original API budget and production policies remain separate gates. Any real FAIL, uncertain result, partial audit or restored STOP remains a HOLD needing the existing proper path. Only new independent reports/harness were written; production implementation and historical reviews were not edited.
