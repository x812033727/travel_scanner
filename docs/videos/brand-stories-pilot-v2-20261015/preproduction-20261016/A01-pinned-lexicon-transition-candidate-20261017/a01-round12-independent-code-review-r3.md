# A01 round 12 driver: independent code review, revision 3

Date: 2026-10-17. This review covers only the frozen local candidate below. It is not a production execution, manuscript PASS, paid-media receipt, or approval to remove A01 STOP.

## Frozen bytes

| File | SHA-256 |
| --- | --- |
| `review-round12-104.mjs` | `648110ac2b9801ce000cc1dc60be28f97bec5cb66ecf26cdc19f0f84168a3d6a` |
| `review-round12-core.mjs` | `07b9a216da6753e77e8624a3bd30d3ece5e85cdca2831683643c5192554acdeb` |
| `inspect-review-progress.mjs` | `3d4fa7a891244a7e0c0ca620fb6a01d9e967b4fc3b4c6c8cee3cf0e156b3415d` |
| `review-round12-core.test.mjs` | `e8daae93acb0c2018646e528e0e30cb9bfc4e29cee37e0972f5e84904de6e614` |
| `review-round12-donor.test.mjs` | `f9278fd12adae78964eabd7201d873dc88b276368f4fad39441664f19a44a8ef` |

The direct private production snapshot has 104 verified audit links and tip `e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7`. The donor test checks exact copied production modules: `story.mjs` `145838ca8c1f707d68925c8dee2bdb0647fe5c4192142040737fabcda1e9e808`, `flow.mjs` `394954833450ac9cc4b65209e107f4ec997d23c0f740378b9fb997a66b8bc3af`, and `lexicon-store.mjs` `84440a1b2430cd7548c09cccfd9be0058734337b9819ef4b8137863b03021ccf`. The audit itself is local evidence, not a fresh host readback.

## Verdict

**Code logic is conditionally acceptable; production phase execution is still NO-GO.** The four concrete findings from revision 2 are fixed in these bytes and the deterministic local path passes. The finding below requires a revised freeze and another targeted review before calling any host command a read-only preflight. The host startup/STOP guard and exact host caller are external dependencies and need separate independent review, action-time host checks, and the applicable owner approval.

## Finding

### P1 release gate — `--preflight` writes to the production host

In `review-round12-104.mjs:120`, `acquireProjectLease(workdir)` runs before the `--preflight` return at lines 136–138. The pinned `project-lease.mjs` creates `<A01 workdir>/LEASE` exclusively and removes it on release. If it takes over a definitely dead holder, it also renames the old lease to a persistent `LEASE.<token>.dead.json`. Thus a command described as a read-only preflight can change the A01 canonical workdir. Lines 124–125 also create and fill a private capture under host `/tmp`. Moving the lease acquisition behind the early return removes the canonical lease mutation but does not make the entire preflight strictly read-only. Either use an explicitly authorized bounded host capture and label it accurately, or provide a truly read-only inspection route. In both cases re-freeze the driver and recheck the command path.

## Revision-2 findings rechecked

1. **Facts report:** `assertSavedVerifierClaimsExact` now allows only the real round-4 `chapter.report` update in addition to claim verdict/note/report changes; it rejects other chapter or claim fields. The production-donor `checkChapter` integration wrote `### 第 4 輪` and passed this guard.
2. **Exact source tip:** `assertRound12Tip` requires the original 104-link source hash and a predecessor-linked 105–108 sequence. The test rejects a wrong 104 tip, wrong predecessor, and wrong phase count. Re-running the local full inspector returned `ACTUAL_REVIEW_PROGRESS_CHAIN_PASS`, 104 links, unchanged tip.
3. **Panel source scope:** both driver and readback inspector now freeze `video.json`, `claims.md`, `script.md`, and `verify-1.md` for the panel event. A tamper test rejects each.
4. **Real phase behavior:** the donor integration copies pinned production modules, uses the actual 104 source, and runs listener → manual remerge → round-4 verifier → narrative panel with deterministic fake model answers. It checks a synthetic 104→108 source chain, one request key across each pending retry, adoption only after scope checks, settlement after adoption, and project STOP restoration. Separate listener/facts/panel uncertain tests leave the preceding source and one unsettled journal with STOP restored. The fake API does not prove the live server receipt or host wrapper.

## Local checks and limits

- `node --check` passed for the five frozen modules.
- `node --test review-round12-core.test.mjs review-round12-donor.test.mjs` with the private snapshot and pinned runtime: **15 passed, 0 failed**. The integrated success path reported 108 links, three distinct request keys from six pending attempts, three adoptions and three settlements, and stopped at `pilot_script_review` without a script-review receipt or media.
- The local source inspector recheck returned `ACTUAL_REVIEW_PROGRESS_CHAIN_PASS`, 104 links, source `e1499cd6…97add7`.
- The tests simulate the model/API; they do not run the production host phase caller, reconcile a live uncertain job, or establish a script PASS. They also cannot prove a SIGKILL/reboot STOP recovery path. The driver requires a `round12-restore-stop.pending.json` assertion, but its boolean alone cannot establish that the host startup wiring really works. A separate reviewed host guard and caller must enforce that condition before removing STOP.
