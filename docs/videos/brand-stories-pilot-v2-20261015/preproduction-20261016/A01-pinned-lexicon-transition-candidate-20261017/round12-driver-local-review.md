# A01 round 12 bounded continuation: local review

Date: 2026-10-17. This is a code and fixture result, not a production execution, script PASS, media approval, or provider spend receipt.

## Frozen input

- Verified `snapshot-104` source chain: 104 links, tip `e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7`.
- `turn.json` SHA-256 `31157cfd9435d4ff2f94f2506224c21a5e4bd0a1997a788dbd88aa303858a981`.
- Independent editorial decision is in `round11-editorial-review.md`, SHA-256 `6033bd8662eebe9212b53ac0c08967238522c3f9f73b2eacd1a705a0415c29cc`: drop only scene `turn-08` and its sole line `6i8x`; retire only its claim `t19`.

## Candidate SHA-256 for independent re-review

| File | SHA-256 |
| --- | --- |
| `review-round12-104.mjs` | `f0712d5bc5722cc6b6d0f7c220e815e8ed280b3a70805dafa5fa51fb976db363` |
| `review-round12-core.mjs` | `07b9a216da6753e77e8624a3bd30d3ece5e85cdca2831683643c5192554acdeb` |
| `inspect-review-progress.mjs` | `3d4fa7a891244a7e0c0ca620fb6a01d9e967b4fc3b4c6c8cee3cf0e156b3415d` |
| `review-round12-core.test.mjs` | `e8daae93acb0c2018646e528e0e30cb9bfc4e29cee37e0972f5e84904de6e614` |
| `review-round12-donor.test.mjs` | `f9278fd12adae78964eabd7201d873dc88b276368f4fad39441664f19a44a8ef` |
| `review-round12-preflight.test.mjs` | `b878506ac79b808ed82c7e3c07bb48342a054a695f801c3398784932605f3f12` |

## Candidate path and boundary

- `review-round12-104.mjs` runs one phase per invocation: `--listener`, `--manual`, `--facts`, or `--panel`. The 104-link starting tip must be exactly `e1499cd6…97add7`; later phases must extend that tip through the exact preceding audit event. Each phase requires zero unsettled journals. A crash with a saved request or an incomplete audit is held for inspection; the next invocation cannot submit a new model request against it. The old all-in-one `--run` command is removed.
- `--preflight` validates without acquiring or releasing A01's canonical `LEASE`. It writes a bounded capture under host `/tmp`, so it is a **no-model validation with a temporary host write**, not a strictly read-only command. Every production phase acquires A01 `LEASE` before capturing and inspecting the source, verifies the lease again, rehashes the live source under that lease, then checks the source and lease once more before lifting STOP.
- The driver uses the installed `advanceStory` and durable model API for exactly one turn listener, one turn verifier, then a bare whole-film narrative panel. It stops at the pilot script receipt gate or the panel failure. It cannot invoke a media stage.
- The listener answer must have `patch: {}`, `drop: ["6i8x"]`, and no nonempty `edits`. The saved chapter must match the 104 chapter with precisely that scene removed; the other five chapter hashes must remain unchanged. The verifier's claim IDs must be unique and in their original order, with claim, scene, source, and fact unchanged. After saving, only verdict, note, and report may change within each claim; the chapter report must advance to a nonempty `### 第 4 輪` report while every other chapter field stays fixed.
- The worker's listener relint leaves `t19` as a transient claim pointing to the removed scene. A separate manual amendment event stores the 104 chapter, the listener output, the amended output, both `auto.json` versions, their hashes and the editorial approval reference. It removes only `t19`, invalidates only `turn.checked` and aggregate `verified`, then invokes the installed `script passes lint` remerge. The old fact, listener and narrative receipts remain historical.
- `inspect-review-progress.mjs` validates the four event sequence from the exact source 104 tip, including per-event predecessor hashes, turn bytes, scope checks, and the zero-model manual event. The manual event carries series, all six chapters, before/after video, claims, and script bytes; the inspector recomposes the derived video, claims table, and screenplay and rejects an altered result even when its hashes are recomputed. A panel event must leave `video.json`, `claims.md`, `script.md`, and `verify-1.md` unchanged. All model scope checks run before adoption, audit commit, and journal settlement.
- A pending durable request is polled with the same source and fixed `today` date; changed source, out-of-scope answer, unsettled journal, changed STOP, and unexpected stage all stop for review. A separate host recovery guard is required before any phase removes the project STOP. `finally` and SIGTERM/SIGINT restoration remain a second line of protection, but do not cover SIGKILL or reboot by themselves.

## Local verification

- `node --check` passed for driver, core guards, inspector, and all three test modules.
- Combined `node --test review-round12-core.test.mjs review-round12-donor.test.mjs review-round12-preflight.test.mjs` with `A01_SNAPSHOT104_ROOT` set to the verified private capture and `A01_PINNED_RUNTIME_ROOT` set to the staged payload: **16 passed, 0 failed**. The 11 core tests include exact source-tip rejection, nonempty listener edits refusal, duplicate/reordered verifier claims, round-4 report, panel derived-file scope, manual derivative recomposition with a rehashed tamper refusal, same-source pending poll, STOP restoration, and the transient-orphan lint path. The preflight test executes the driver's actual `--preflight` control path against private fixture files with an instrumented lease dependency and stubbed capture/inspector; it verifies that an existing canonical `LEASE` remains byte-identical and no dead-lease rename occurs. The live capture and inspector are separately exercised by the actual 104-chain readback.
- The four donor tests verify byte-for-byte SHA-256 matches for the production `story.mjs` (`145838ca…e808`), `flow.mjs` (`39495483…3af`), and `lexicon-store.mjs` (`84440a1b…21ccf`) before loading them. With a deterministic fake model/API and no network, the installed `advanceStory` executes listener, manual remerge, verifier, and narrative panel from the actual 104 snapshot; persisted source tuples form a synthetic 104→108 tip chain. The stage returns `pilot_script_review` after a round-12 panel; no media stage runs. Pending is injected once at each model stage and retains one request key per stage (six attempts, three keys); uncertain is injected separately at listener, facts, and panel, leaving the prior tip and one unsettled journal while restoring STOP. The fake API adoption checks source artifact hashes and settlement follows an accepted scope check. This is a local integration simulation, not a real durable API receipt, host audit event, or execution of the host wrapper.
- The snapshot copy lacks the host's `brief.md`, so the lint probe rebuilt its brief with the installed `storyBrief` from the frozen series plan. With `turn-08` removed but `t19` still present, `lintProject(loadProject(...))` returned zero errors. The transient orphan is still retired in the next guarded event before factual recheck.
- Re-running the full read-only `verify-progress104.mjs` with the amended inspector returned `ACTUAL_REVIEW_PROGRESS_CHAIN_PASS`, 104 links, unchanged tip.
- `git diff --check` passed for tracked changes; no production write or model call was made by this local development task.

## Staging requirements

The host's isolated payload must receive the driver, core, updated inspector, editorial review Markdown, and the original verified base82 historical inputs. Run `--preflight` against a fresh host readback. Each phase requires a durable `round12-restore-stop.pending.json` sentinel written by a separately reviewed host runner after its boot/worker-startup STOP recovery hook is verified. **No phase is approved for production until that hook and runner pass independent review and local interruption tests.** The host caller must independently check the exact current HEAD/runtime hashes, owner hold, deployment locks, A01 STOP, active jobs, and US$25 budget ledger. The restored `/tmp` payload is not itself a fresh production preflight. If a model proposes another edit or a job remains pending beyond the bound, retain its journal and STOP for inspection; do not start a new request key.
