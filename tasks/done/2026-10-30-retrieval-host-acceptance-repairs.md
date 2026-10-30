---
id: 2026-10-30-retrieval-host-acceptance-repairs
title: Prepare retrieval host acceptance repairs
status: done
priority: P1
area: ops
owner: codex-retrieval-host-acceptance-20261030
claimed_at: 2026-10-30T03:21:35Z
created_at: 2026-10-30T02:21:15Z
completed_at: 2026-10-30T03:31:50Z
branch: codex/retrieval-host-acceptance-repairs-20261030
depends_on: []
scope:
  - tasks/open/2026-10-30-retrieval-host-acceptance-repairs.md
  - apps/api/app/video_speech/admin_api.py
  - apps/api/tests/test_video_speech_session_release.py
  - .agents/skills/deploy/scripts/host-verify.sh
  - tools/deploy-host-verify.test.mjs
---

# Prepare retrieval host acceptance repairs

## Why

The retrieval localization publication and public page checks succeeded, but
its final host acceptance reported 9 PASS / 2 FAIL on 2026-10-30. The API log
contained 28 genuine connection-pool timeouts; the video check could not pair
policy-stop messages with four exits in its short log window. The failed
finalization is immutable and must not be reported as accepted.

Speech routes retain a database transaction while waiting for external
providers. This is a confirmed pre-existing code risk, not a demonstrated
explanation for the incident's actual connection holders. The video parser
also needs bounded context and exact handling of benign interleaved lines.

## Definition of done

- [x] Independently reviewed proposals demonstrate database availability
      during provider waits and preserve pilot-budget settlement boundaries.
- [x] The proposed video check recognizes exact policy stops but still fails
      on unknown errors, missing context, invalid logs and unrelated exits.
- [x] Existing ownership overlaps are explicitly resolved before any held
      repository source or test file is changed.
- [ ] Any implementation receives focused tests, independent review, CI and
      a concrete owner decision for merge; production work remains separate.

## Steps

- [x] Preserve the failed finalizer and validate bounded read-only diagnostics.
- [x] Inspect current main, sibling worktrees and open PR ownership.
- [x] Prepare private source-pinned patches and actual regression-test receipts.
- [x] Independently review the exact patches; prepare the ownership decision package.
- [x] Obtain the narrow scope exception, then expand this task's scope before
      applying approved changes in this isolated worktree.
- [ ] Complete implementation review and CI, then request the exact PR merge.

## How to verify

Run the real Bash/AWK classifier with positive and negative interleaving,
truncation and cross-round cases. Exercise speech/provider waits with an
independent database borrower, pilot rejection/settlement and provider-error
paths without paid network calls. Run relevant existing speech suites, Ruff,
mypy and task checks. Record actual native exits and any unavailable integration
coverage. No test may relabel the original failed production acceptance.

## Notes

Initial proposal checkpoint: scope covered only this task's metadata. Private proposal
copies are outside Git; they grant no authority to edit the held source paths.
The intended code paths must be added only after ownership is resolved:

- `apps/api/app/video_speech/admin_api.py` and focused speech regression tests.
- `.agents/skills/deploy/scripts/host-verify.sh` and
  `tools/deploy-host-verify.test.mjs`.

Ownership evidence at 2026-10-30 02:19 UTC:

- The speech module is under `2026-10-19-worker-video-languages-five`
  (claude-opus-5.5-worker-dubs-five, review). Fresh PR #1928 also holds the
  module through `2026-10-30-runpod-pod-broker` (claude-opus-5-5-runpod,
  claimed 01:18:54 UTC). Its token/pairing additions do not change the proposed
  provider-call boundaries, but the file-level ownership remains active.
- PR #1583 holds both verifier files through
  `2026-10-19-prepare-0133-image-for-guarded-0134`
  (codex-gpt6-a01-precompat). Its pending diff changes schema guards, not the
  video classifier. A main-only ownership scan does not see this remote task.
- No foreign task, branch, quota, host setting or running process was changed.
  Initial proposal base is 42ec79dc57986d093b25a896279627087dd759fb.
- Failure evidence audit SHA-256:
  bfe3eea047054a0779c4d1670b2da9ad826b8e8338e057b51719b7aabcd85c7d.
  Diagnostic integrity/runtime review SHA-256:
  7bd4b6e7472c4e035e9b5f0456bc86d68823b743dff315b1dbd5c3e3d095f6a5.
  Publication/QA remain accepted; full release acceptance and its gated census
  remain incomplete. Further deployment needs its own reviewed, authorized
  target and full pending-range disclosure.

Private API proposal completed at 2026-10-30 02:31 UTC. It adds one executable
`await session.commit()` in the nonpilot branch of `reserve_pilot_call`, plus
the new `apps/api/tests/test_video_speech_session_release.py`. The exact base
fails ten real SQLite/SQLAlchemy independent-reader cases; the candidate passes
175 focused tests, with one existing PostgreSQL integration test skipped.
Ruff, mypy and isolated patch-application checks passed. Independent review
reran all sixteen new cases and verified the exact source/AST/receipt hashes:
patch SHA-256 5a5fb5b7c1cef800f53c456bc96cd2314738296a596b194411f192e5b7377333;
review SHA-256 8a9b706a199ca172b8e9b11d9cca4cc5a34cfd6efb3440916cefc64f587ed0f6.
This proves a local SQLite pool lifetime regression, not PostgreSQL behavior
or attribution of the production incident. No held repository file was changed.

Intermediate review checkpoint: the verifier proposal remained under review. Its bounded context must preserve
the most recent thirty-record health window without failing merely because a
long-lived worker has more than 2,000 records. Review found cases involving
error words in benign identifiers, uppercase errors and malformed exit lines;
the author is correcting these before final acceptance. A separate read-only
production probe at 02:38 UTC confirmed GNU Awk 5.3.2 and interval-expression
support; it did not change deployment, logs, quotas, configuration or runtime.

Final verifier proposal passed 18 native Bash/AWK tests with zero skips.
Independent review reran those 18 tests and 35 native edge fixtures: eleven
valid cases accepted and twenty-four invalid cases rejected. Exact patch
reconstruction matched the tested source bytes. All reported identifier,
uppercase-error, malformed-exit and blank-payload regressions are resolved.
Patch SHA-256: 4656ab11569423d51c3356370635acdd3eeecc76be88c3eaa782c3d793bbeba1.
Combined private-proposal review SHA-256:
86ca3bae40c86fce00df1efc272d74732fbd4b5e71c8ea9dd712d51fef6d505e.

At 2026-10-30 02:55 UTC, main remained 42ec79dc5. PR #1928 remained open
at 7db8cb34875b4fd96d0db9815a48a33c412f124e with unchanged relevant file
patches; PR #1583 remained open at f86cf58f3c01c0397debff0a3ab21a7cc7c3a51d.
No held repository source has been modified. The remaining external gate is
the owner's narrow overlap exception under AGENTS.md, before this task's
scope can expand to the four reviewed code/test paths. Merge and production
work have not been authorized by this proposal preparation.

2026-10-30 owner authorization: the owner explicitly selected
「同意窄範圍修補，完成 PR 與 CI（建議）」 for the reviewed four-file plan.
This grants a one-time overlapping claim for these exact code/test paths,
isolated implementation and PR/CI preparation. `claim --force` is justified
only by that explicit exception. Foreign tasks, their status and branches
remain unchanged. The relevant PR heads and main were rechecked unchanged
before implementation. Merge, deployment and production acceptance remain
outside this authorization. Earlier metadata-only and pending-approval notes
above are historical checkpoints, superseded only for the approved local scope.

Implementation checkpoint, 2026-10-30: both accepted patches are now applied
in this isolated branch. The four code/test files exactly match the reviewed
source hashes. Local validation passed: 175 API regressions (one existing
PostgreSQL-only case skipped), all 18 native Bash/AWK verifier tests with
zero skips, full Ruff, mypy app (490 files), mypy tests (427 files), Bash syntax
and diff checks. The full tools suite is also running at concurrency two;
its first run was deliberately interrupted for local memory pressure, not
reported as passing. CI must run the PostgreSQL case with integration enabled.

This ticket is closed in the implementation PR as required by the task-board
protocol. The unchecked combined CI/merge items above remain explicit PR
gates: CI results will be recorded on the concrete PR before requesting its
owner merge decision. The PR must carry no-auto-merge. This does not close
the separate blocked localization release task, grant merge/deploy approval,
or replace the original failed production-finalization receipts. Other owners'
tasks and branches remain unchanged. No migration or production write is part
of this repair implementation.
