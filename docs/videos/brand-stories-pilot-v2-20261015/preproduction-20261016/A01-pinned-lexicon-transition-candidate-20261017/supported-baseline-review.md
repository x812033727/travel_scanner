# Independent offline supported-baseline increment review

Reviewer: `codex-independent-a01-lexicon-1017`. Date: 2026-10-17 (Asia/Taipei).

Verdict: **0 P1 / 0 P2 findings in this exact two-baseline read-only increment. Production remains HOLD.** No actual 81 event, production adoption or paid approval is established by this report.

## Reviewed bindings

| File | SHA-256 |
| --- | --- |
| supported-baseline.mjs | d534bd3cc8bf3b6dd23cc3c8a9d76a7188d2ae3d3e832d7de61287d2e567baf9 |
| transition.mjs | 53fa319c043d35310b37f810f747db036eea9dcee266e8877b6b914e7c7102b7 |

Read the complete supported baseline and its original e640 validator context. The transition changes its baseline import to this isolated module. The new validator retains the old historical 80 pins and ebfa byte hash, exact previous-entry values, full source hashes, audit-chain validation, historical file evidence, narration semantic checks and Temp-only synthetic override rule. It recognizes exactly e640/23 additions or 4d3/27 additions; the extra four are Nieman='尼曼', Daniel=null, Roberts=null and One=null. An actual shared-file SHA chooses the supported exact branch by default. A caller-supplied supported SHA still has to equal the actual captured file. An unknown SHA cannot use the production path; synthetic pins require the original Temp marker gate. The new candidate ID is scoped to the afternoon baseline and does not alter the e640 plan.

## Independent capture and boundary checks

Independently enumerated and byte-compared the two local snapshot-80 roots: **199 files each**, no added/removed files, and only docs/videos/lexicon.json differs. The other 198 files are byte-identical. A parsed old/new shared dictionary comparison found no removed or changed existing entries, and exactly the four additions listed above.

Using bundled Node 24.19, independently invoked planPinnedTransition with the historical round9-lexicon.json against both captures:

| Capture | Added terms checked | Spoken lines scanned | Plan SHA-256 |
| --- | --- | --- | --- |
| A01-20261017-095816-2a72b1e1/snapshot-80 | 23 | 184 | f269a6337f6a7900a02b6a8b0860b055b4e19c203ecab85675026dd17455a41f |
| A01-20261017-afternoon-fe35369c/snapshot-80 | 27 | 184 | 3a08217137dabd3ca57256cb12f73ae6b9ced9e86cf66704b17fd4ea64f21220 |

Both use pinned historical dictionary ebfa590a69b4328ed9bc0141832bb73d27cba51963fca78778258d404c3bc4c9 and propose the same resulting source 766a83c237af95b14d7c23bde133c8362e6a2f140bd959b0c056719d53eb3502. Their observed shared SHA values are respectively e6403c824aac13b4c0a1ae737e8a597a8bf60c353e9faf0cc4915c3214114a30 and 4d3e995b1abf1acd64db3eafd397f1cad8e220880e95f2c39ab108ecaea8c9f6. The plans succeed only with zero narration hits and unchanged used-entry/unknown-term semantics. Both return HOLD with installation/paid false. The unchanged e640 plan SHA also confirms its historical plan binding remains intact.

Independently supplied an unknown expected shared SHA on each non-Temp capture: both rejected with SYNTHETIC_OVERRIDE_FORBIDDEN. Supplying known e640 SHA against the afternoon capture rejected with LEXICON_HASH_MISMATCH. A direct selected-27 matcher check beside Chinese text returned all four new Latin terms (Nieman/Daniel/Roberts/One), confirming they are included in that branch's narration scan.

Independently ran node --test transition.test.mjs adopt-pinned.test.mjs pinned-revision.test.mjs: **10 passed, 0 failed**. This includes the existing exact capture/partial publication/changed evidence tests, seven simulated adoption interruption phases and committed recovery, and round21 pinned-source revision cases. Those synthetic fixtures predominantly use the original 23-term synthetic baseline; the real 27-term path above was independently exercised through read-only planning and explicit rejection/matcher checks rather than a new synthetic 27-term fixture.

## Limits

This report confirms local persisted captures and code behavior; it does not independently refresh deployment locks, DB/jobs, budget, runtime deployment or owner identity at action time. An empty lock observed earlier is not itself a retained production lease. Real adoption still requires caller-held deployment protection, fresh exact source/runtime preflight, uncertain-job disposition and authenticated scope. External review/owner strings remain record data, not proof of a human approval.

The plan pins historical ebfa bytes and preserves shared bytes; it does not authorize silently adopting the newer 27 terms into A01, changing narration or resetting retries. Existing fresh-cycle counter scope for the separate round21 82 revision remains as documented in its independent report. No genuine verifier/listener/narrative-panel receipt or film was created. Only this new Markdown report was written; no host or paid action or implementation edit was performed.
