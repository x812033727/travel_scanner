# A01 round 12 independent code review, second pass — 2026-10-17

**Decision: the frozen second candidate is not ready for production execution.** This pass reviewed the new four-phase driver and its inspector against the actual 104-link A01 source. The production host, model, paid media, merge, and deployment were untouched. The separate host STOP recovery guard is outside this review; the driver's requirement for its pending marker is not proof that a boot guard is installed.

## Frozen inputs and offline checks

| File | SHA-256 |
| --- | --- |
| `review-round12-104.mjs` | `5a4da3e5425720000c6bb312dc8e1aab10690b6cfcc78e57d29fe0b98c9d09e6` |
| `review-round12-core.mjs` | `09833df8eb714e28947089e8a9329ca0cea7bbcfde638515d6217e07a6572495` |
| `review-round12-core.test.mjs` | `41343ea386207f4d3a480b2253e40f34fd1cd06a6ed19b32ba9161621e3cafb3` |
| `inspect-review-progress.mjs` | `52efd0bb0a730f00ee78dfb79dabd170a12d3cb26a983633630cd5cd913946a2` |

- Read-only `verify-progress104.mjs` returned `ACTUAL_REVIEW_PROGRESS_CHAIN_PASS`, 104 links, source SHA `e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7`.
- `node --check` passed for the driver, core and inspector. The provided offline test suite passed **10/10**, including duplicate/reordered claims, nonempty `edits`, model event scope, rehashed manual derivative tamper, pending polling, ordinary STOP restoration, and lint.
- The provided tests import `story.mjs` from the **current worktree** (SHA `0ff27096…`) while production uses the pinned staged copy (SHA `145838ca…`). I separately checked the pinned copy: its `checkChapter` writes a new `report`, and its `composeStory` reproduces the actual 104-link `video.json` as an equal parsed object. Future phase tests should execute against the pinned runtime copy, not rely only on the current worktree.

## Findings

### P1 — The facts phase rejects the real verifier's required report update after paying for it

`review-round12-core.mjs:44-50` removes `claims` and then requires all remaining chapter fields to be unchanged. The pinned production `story.mjs:1328` necessarily writes `report: "### 第 4 輪…"` when the `--facts` verifier saves its real answer. Actual snapshot 104 has a `turn.json` report beginning `### 第 3 輪`. A direct offline probe with the actual chapter and a round-4 report produced `VERIFIER_SAVED_CHAPTER_OUTSIDE_SCOPE`. In `review-round12-104.mjs:60-64, 202-205`, this check runs after the model result and chapter write but before adoption/audit/settlement. It would leave an updated source and unadopted saved journal, preventing clean continuation and risking an unnecessary repeat if recovered incorrectly.

Permit only the documented round-4 `chapter.report` update in addition to verdict/note changes; validate the exact report round and preserved other fields. Exercise the real pinned `checkChapter` path with a deterministic fake stage answer, then verify the stored chapter and journal before production.

### P1 — The 104-link starting source hash is no longer enforced

The phase driver at `review-round12-104.mjs:126-135` requires the correct link **count** but no longer requires the initial tip to equal its declared `source104` constant. `inspect-review-progress.mjs:90-100` only applies the round-12 event sequence if the chain reaches `ROUND12_SOURCE104`; it does not require that source at link 104. Thus `--preflight` can report PASS on a different 104-link tip, and `--listener` can start a real model request from it as long as the target scene and a few auto flags still match. Later phases may fail because their first round-12 event lookup finds no event from the expected source, but that is too late for the first paid call.

At 104 links, require `progress.source_sha256 === source104`. At 105–108, explicitly verify that the first new round-12 event's `before_source_sha256` is `source104`, and that each later phase is the exact successor to the preceding validated event. Add a negative test with a valid-length but wrong-source tip.

### P2 — Panel event scope does not freeze derived manuscript and check files

`assertModelEventScope('narrative_panel')` in `review-round12-core.mjs:62-71` fixes series, lexicon, pilot and chapter hashes, but permits changes to `video`, `claims`, `script` and `verify`. The panel path should change only `auto` and `review/narrative.json`; an unrelated edit to those four derived files could be adopted and recorded as a successful panel event. Require all four to remain equal before adoption, and have `checkRound12Model` enforce the same rule on readback. The installed narrative gate does not normally write these files, so this is a scope/audit gap rather than a demonstrated routine write.

### P2 — Local tests do not exercise the staged runtime or full phase persistence

The tests cover pure guards and a recomposed manual fixture. They do not run `--listener`, `--manual`, `--facts`, or `--panel` against a copy of the actual 104-link source with the pinned staged `story.mjs`/`flow.mjs`, nor simulate a journal that is pending or uncertain at each phase boundary. The report-update failure above escaped 10 green tests. Before production, add a local phase simulation with fake deterministic stage answers and true `advanceStory`/adoption behavior. Confirm no second request key is generated after a pending result, no event is marked saved for an uncertain result, and each phase returns with STOP restored and one valid new link.

## Prior findings rechecked

- The duplicate/reordered claim ID guard is now exact (`assertVerifierClaimsExact`), and the saved claim identity is checked again. The reported P1 on losing `t13` is fixed in these bytes.
- Scope checks now run before `adoptRuns` in `commitModelEvent`, fixing the prior commit-before-check ordering; the narrower panel scope gap above remains.
- Manual derivative evidence now includes before/after video, claims, screenplay, series and chapter bytes, and independently recomposes them. The rehashed tamper test rejects a changed `category`; the previous derivative-audit gap is substantially fixed for this A01 source.
- A nonempty listener `edits` array is now rejected.
- Work is split into four phase commands with a link-count gate, so a committed phase no longer forces restarting from link 104. A crash **within** a phase after a successful model receipt but before audit/settlement still requires manual reconciliation; the retained journal and STOP restoration must remain hard stops rather than a blind new dispatch.
- The driver calls only story review steps and has no direct media, TTS, dub or upload call. `commitModelEvent` still requires one adopted `succeeded` journal before labeling a model event saved. The host wrapper must independently verify A01's US$25 ledger, inactive paid jobs, project STOP and installed startup guard; the driver checks only the marker's JSON fields, not the real startup wiring.

No script-review PASS, A01 paid production, or video completion is established by this review.
