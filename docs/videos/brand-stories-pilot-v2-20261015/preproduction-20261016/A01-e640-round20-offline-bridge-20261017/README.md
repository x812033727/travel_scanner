# A01 e640 80→81→82 offline bridge — HOLD

This is a separate, read-only continuation of the 2026-10-17 A01 capture. It
uses the exact 23-term `e6403c82…` lexicon candidate for the proposed 81st
audit event, then binds the unchanged round20 manifest
`4d701779891e1076c3729788cc82165901d71140bfbd77c07fa9b1c060b32549`
to a proposed 82nd existing-story chapter revision. The older two-term
`835e09df…` candidates and their reviews are unchanged. Neither old review can
approve the new 23-term event.

## Files and contract

| File | Read-only job |
| --- | --- |
| `inspect-transition-export.mjs` | Check distinct 80/81 snapshots, original 80 links, exact e640 81st event, supplied SQL/budget/inventory state and pinned source hashes. |
| `revision-plan.mjs` | Plan the exact round20 eight-file source revision and verify a separate 82-link snapshot. It has no fixture-apply, host-write or CLI path. |
| `inspect-host-plan.mjs` | Join those checks, optionally bind independently supplied raw review/receipt bytes, then rerun the complete 80→81 export check to detect local drift. |
| `capture-gate.mjs` | Read one sanitized local capture summary and explain why it cannot enter the 81→82 bridge. |
| `synthetic-fixture.mjs`, `inspect-host-plan.test.mjs` | Build marked OS-Temp data only; synthetic reviewer/operator strings and receipts are test data, never production evidence. |

All successful plans and comparisons still report `production_status: HOLD`,
`installation_allowed: false` and `paid_work_allowed: false`. The output is a
local byte-level proposal, not host-origin authentication, an exclusive writer
window, a genuine independent review, an owner approval or permission to retry.
The CLI has no `--apply` option. It neither calls a model nor changes worker
state. The old 80-link pinset and all historical audit and installation bytes
must remain intact; a changed old link makes the 82-link check fail.

## Current real capture

The sanitized receipt outside Git is
`<local-capture>/A01-20261017-095816-2a72b1e1/capture-receipt.json`,
SHA-256 `d15566f3ec2a9792975823347bebe750bd2aa951281a0acb38c1d6776277149d`.
Read-only `capture-gate.mjs` returned nonzero `REJECTED` and `HOLD` with
`NO_VERIFIED_81_EVENT`, `CAPTURED_CONTROLS_ABSENT`, `UNCERTAIN_STAGE_JOB` and
`AUDIT_SOURCE_NOT_REBASELINED`. That export has 80 audit events, all three
observed control files absent (global STOP, A01 STOP and LEASE), one uncertain
stage job, and no 81st event. It is **not** a supplied 81-link after-snapshot.
The earlier e640 tool separately computed an 80→81 *proposal* on that capture;
it did not append an event. The current export cannot pass this bridge.

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-e640-round20-offline-bridge-20261017/capture-gate.mjs `
  --receipt C:\capture\A01-20261017-095816-2a72b1e1\capture-receipt.json
```

## Future local export check

If a separately authorized and reviewed 81st append ever occurs, supply two
*distinct, immutable, complete* local host captures and independently recorded
pinsets. `--state` must be a sanitized SQL/budget/filesystem projection in the
schema of the earlier host export checker. This command reads only; a syntactic
review or receipt is not proof of its human origin. The actual host paths and
write protocol are outside this candidate.

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-e640-round20-offline-bridge-20261017/inspect-host-plan.mjs `
  --before80 C:\capture\immutable-80 `
  --before81 C:\capture\immutable-81 `
  --old-lexicon C:\capture\round9-lexicon.json `
  --before-pins C:\capture\before-pins.json `
  --after-pins C:\capture\after-pins.json `
  --state C:\capture\sanitized-state.json
```

`LOCAL_82_PLAN_BOUND_TO_SUPPLIED_EXPORT` is possible only if the supplied 81st
event and quiet projection agree. The optional `--review` and `--receipt`
arguments merely bind exact *externally provided* bytes; they do not invent or
authenticate approval. A 82nd snapshot can be read with the exported
`verify82Fixture()` function after a separately reviewed, authorized install.

Even a matching local 82-link comparison will not start formal review. A01
still needs the common writer exclusion and dual-mount crash recovery protocol,
current job/receipt disposition, a fresh production preflight, an independently
approved exact transition, and genuine worker verifier, listener and narrative
results. The ninth narrative panel remains FAIL on `chapters_link`, `payoffs`
and `one_thread`; no existing result is changed by this bridge.

## Focused verification

```powershell
node --check docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-e640-round20-offline-bridge-20261017/revision-plan.mjs
node --test docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-e640-round20-offline-bridge-20261017/inspect-host-plan.test.mjs
```

The six focused tests construct the exact synthetic 23-addition transition,
bind a round20 plan, verify a separate 82-link snapshot with all older index
bytes preserved, reject a forged historical link, reject changed state/control
readbacks, and confirm that the shape of the real 80-link capture remains HOLD.
The synthetic reviews/receipts are never copied into the repository or used
against the real capture.
