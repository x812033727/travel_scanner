# A01 81st lexicon event fixture: independent review

Date: 2026-10-16. Verdict: **PASS for the frozen offline fixture only; HOLD for production installation or paid work.** The reviewer did not author or modify the three reviewed files, access the host, or call a media provider.

| Reviewed file | SHA-256, checked before and after review |
| --- | --- |
| `apply-fixture.mjs` | `92e28647d677ecd2b2042e9e2373c90d1cd673ee05e34570111d019f7c5f4be7` |
| `apply-fixture.test.mjs` | `db83d3785109b96ba86c3655efaa760ff77f744c406fa5854e7c4067e307ce55` |
| `README.md` | `ffed512e4822c2d810fa76074572aaf90aa996c53fc51b8cf210823ede388214` |

`node --check apply-fixture.mjs` passed. The independent `node --test apply-fixture.test.mjs` run passed **9/9**. The review checked the marked OS Temp fixture restriction, binding to the 80-link source and external evidence, exact 81-link readback, refusal of partial retry, rollback of only unchanged new files, and crash cases. Relevant implementation points are `apply-fixture.mjs:32-75`, `:108-133`, `:218-236`, and `:258-293`; the existing transition verifier is in `../A01-lexicon-rebaseline-candidate/rebaseline.mjs:292-328`. No defect was found within the stated offline scope.

The live path remains **HOLD**. `apply-fixture.mjs:84-125` receives its safety, review and owner-reference values from a caller; these strings do not authenticate a reviewer, owner, host state, or fresh database reading. `:253-266` has no lock shared by actual A01 writers between precommit and final readback. A separately reviewed host adapter must acquire and recheck real state under a coordinated lock, handle a partial publish, and install a reviewed 81-link production inspector. The documented host capture lacks STOP files and real external review/receipt bytes, and is too old to serve as an action-time preflight. This PASS neither writes the 81st audit event nor approves a script, image, TTS, render, B18, five-film production or upload.
