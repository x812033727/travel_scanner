# A01 round20 host-export proposal bridge — read-only, HOLD

`inspect-host-plan.mjs` joins two already separate offline checks without
changing either: the independently pinned [80→81 lexicon/export inspector](../A01-host-transition-export-candidate/README.md)
and the [81→82 round20 existing-chapter revision fixture](../A01-round20-existing-revision-offline-candidate/README.md).
It can consume a new **local copy** of a complete host export and report the
exact proposed 82nd plan hash and, when separately supplied review and receipt
bytes bind to it, the proposed 82nd event pins. It reads files only. There is no
SSH, database, browser, network, installer, `--apply`, retry or provider path.
Every result, including a matching plan, says `production_status: HOLD`,
`installation_allowed: false` and `paid_work_allowed: false`.

## Inputs and result

The first six arguments are absolute local paths following the 80→81 export
contract. `--before80` and `--before81` must be distinct immutable captures;
the separately recorded pinsets must match the original 80-event history, the
exact 81st lexicon event and the sanitized host-state JSON. The routine calls
the complete 80→81 inspector, checks the supplied state has both STOP markers,
no A01 lease, unresolved journal, pending retry, active or uncertain job or
reservation, and no media assets, then builds the round20 82nd plan. Historical
completed or failed stage jobs and resolved run receipts may remain. This
projection is **not** an authenticated live preflight or a writer lock.

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-round20-host-export-plan-candidate/inspect-host-plan.mjs `
  --before80 C:\capture\immutable-80 `
  --before81 C:\capture\immutable-81 `
  --old-lexicon C:\capture\original-lexicon.json `
  --before-pins C:\capture\before-pins.json `
  --after-pins C:\capture\after-pins.json `
  --state C:\capture\sanitized-state.json
```

`LOCAL_82_PLAN_BOUND_TO_SUPPLIED_EXPORT` means the supplied 81st audit source,
database projection and round20 proposal agree locally. Once an independent
human review of the **exact plan** and a genuine operator/owner record have
been produced outside this tool, append `--review C:\capture\review.json
--receipt C:\capture\receipt.json`. A matching result is
`LOCAL_82_BYTES_PREPARED_OFFLINE` with `expected_82_pins`; the checker only
validates the bytes' schema and hashes. Reviewer/operator names and
`owner_approval_ref` fields cannot authenticate people or permission. Missing
or unpaired evidence, a changed STOP/retry/job/budget projection, altered old
event, unrecognized 81st event, changed round20 package or drift during the
two local inspector passes returns nonzero `REJECTED` with a code. The program
never writes the proposed event or chapter files.
Programmatic synthetic-fixture reports explicitly set `synthetic_fixture: true`;
the production-shaped CLI has no flag for fixture hash overrides. The exported
inspector has no caller callback or write hook.

## Why there is no production apply

The existing [host-adapter review](../A01-lexicon-host-adapter-candidate/README.md)
found no common production lock honored by all A01 audit writers, the shared
lexicon writer and direct host operators. A01 `LEASE` fences one story; STOP is
a cooperative pause. `video_docs` and `video_work` are separate writable mounts.
An adapter taking its own `flock` or merely observing STOP plus zero jobs could
race a different story's lexicon update or an out-of-band manual writer. The
current OS-Temp 81→82 transaction and rollback tests do not prove host
exclusion or two-mount crash safety. Therefore this candidate deliberately has
no code path that accepts a production root as a write target.

A future production adapter needs a reviewed common writer protocol and an
owner-authorized maintenance window that drains both video workers, blocks
container recreation and manual writers, holds the deployment lock, and keeps
that exclusion across fresh capture, 81st append, 82nd append and readback.
It must stage source backups and receipt/audit bytes durably on the respective
mounts, refuse any unexpected source/history/control/job/budget change,
publish an immutable receipt before the new audit tip, and preserve an intent
for manual recovery after a crash. A partial transaction must never be blindly
retried or rolled back over somebody else's bytes. Its final readback must
independently verify all 82 events and source hashes. This is a design
condition, **not** authorization or a host runbook.

## Local verification

```powershell
node --check docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-round20-host-export-plan-candidate/inspect-host-plan.mjs
node --test docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-round20-host-export-plan-candidate/inspect-host-plan.test.mjs
```

The focused 5/5 tests cover rejection of changed control/job/budget
projections, missing capture and any `--apply` flag; a complete synthetic
80→81 export bound to the round20 plan; review/receipt binding to exact 82nd
pins; refusal of a changed supplied state file; and strict pure comparison of
the two export reports. The suite does not inject a file change between the
two synchronous reads; that specific race remains untested and, without an
exclusive writer protocol, cannot be ruled out by this read-only bridge.
The underlying 80→81 and 81→82 modules have their own transition suites. This
bridge has **not** been exercised against a real host capture, and its tests do
not establish freshness, completeness, operational lock coverage or permission.
