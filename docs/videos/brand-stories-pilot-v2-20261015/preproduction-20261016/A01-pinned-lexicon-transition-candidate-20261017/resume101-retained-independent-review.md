# Resume101 retained-request incremental independent review

Reviewer codex-independent-a01-lexicon-1017. Remaining P1/P2:0. Offline only; no host calls, provider calls or real request resubmission by reviewer.

## Exact bytes

- driver review-resume-101-retained.mjs421f59553a595914b0001509e7822b7fb0046321419fa618e3c72303b5fa363d
- original retained101-journal.json9e068ebb5fa24c203a519e43e29d9a68d0da310418c1c585313456b50b156b27
- caller resume-retained101-host.sh8b4db685fc70f7a95b75ad4905283e739e4d05a993c0fc47be037c165c7aeb28
- independent mock harness a29687a109e10aed0ceac1149fb1c329f2ee6c7bb4120436dff8abbae9d027d5
- installed-store local test de32c9c22de6f4b23d3d0fdb492340252776180ffa9e53276b2d06e2597f03cd

Paths for tests are in capture A01-20261017-afternoon-fe35369c as retained101-independent-harness.mjs and retained101-real-store-test.mjs.

## Static delta

Compared to independently reviewed f851f26 original101driver: only the zero-journal prerequisite becomes one exact reviewed queued journal (name1ed3c7b1b1f1109d575722685fd295ba40cf11cd44da0d1ff1987c8383d949e9.json, above bytehash, request key3261b741-f119-4e7e-9ed7-114d48d9e6ce, A01/listener/story/engine,queued/not adopted), and pending limit12→100. Overall120stage-call and8successful-unit bounds unchanged. Same source101 guard, single-line listener restriction, counter preservation, invalidation, audited adoption before settlement, STOP finally and no-media stage scope remain in force. Pending100 is an attempt bound, not a guaranteed wall-clock deadline; provider/client waiting influences elapsed time.

Read installed run-receipts/client semantics: exact normalized request finds the retained receipt; known receipt path polls the existing job rather than POSTing a fresh job. Source drift is rejected by the normalized identity/store rather than silently opening a replacement request. Installed identity/receipt hashing checks remain required; wrapper strings alone are not authorization.

Caller delta preserves fourlocks, same exact clean target and verifies the existing own resume101 release hold instead of acquiring another. Active-before1 matches the one retained queued A01 job; driver independently checks the exact journal. Active-after0 plus STOP and budget recording remain prerequisites to clearing only this hold. Independent bash -n exited0. The database active count is not by itself proof of job identity; retained-journal/store identity binding supplies that prerequisite. Race-to-terminal before active-before may safely refuse and require a new readback; it cannot permit a second job.

## Independent local tests

Real101source and80/81/82baselines copied into unique OS Temp split roots, with exact queued journal bytes copied before invocation. No driver source/hash gate weakening. Same previous harness-only import substitutions, Windows directory-fsync exception and short wait used; provider/advanceStory mocked.

Single four-case run PASS:
1. Exact journal→success: one answer/settle; audit+committed asserted before settle; source101precheck accepted; engine.checked/verified invalidated; check_rounds2/narrative_fixes2 preserved; STOP exact restored.
2. Exact journal→pending→success: two attempts on retained original key, one successful answer/settle; same assertions.
3. Changed request key: refusal before mocked stage; original auto/engine bytes unchanged,STOP restored.
4. Appended whitespace changes only journal hash: same pre-stage refusal,original auto/engine unchanged,STOP restored.

Separately used REAL installed runReceiptStore, exact original journal and unmodified normalized request in a Temp workbase. Three prepare calls all returned the same queued receipt/key/file; directory still exactly one journal and bytes remained identical. No network invocation. Initial test setup mistakes (workbase mistakenly equalled repository root, then Windows slash-style path assertion) were corrected in the test only; final real-store test PASS. These were not implementation failures.

Inherited original101tests already cover extra patch/drop rejection, source tamper pre-stage refusal and STOP preservation. Incremental tests do not prove real provider success or panel acceptance. Power-loss/SIGKILL recovery, provider cost and the eventual genuine returned patch remain outside these mocks. No formal verifier/listener/narrative verdict or owner approval is issued here.
