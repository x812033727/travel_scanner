# C03 host-only budget metadata probe v2

This probe distinguishes an absent database account from a source admission hold.
The existing hashbound `host-admission-readback.sh` is preserved: its call to the
native `reconcile_cli` for the unknown remake returns the preproduction hold before
reading the account, so it cannot establish whether that account row exists.

After independent review, an operator with an **already established production
host connection** can place the two adjacent probe scripts in a private folder and
run `bash /path/to/host-budget-metadata-readback.sh`. The wrapper uses the existing
`/root/travel_scanner` Compose project and `exec -T` in its running API and video
worker containers. It neither installs the scripts into an image nor invokes a
deployment. No additional website token is needed for this host procedure.

The fixed allowlist contains only old C03 and
`story-everyday-moleskine-c03-remake-20261025`. The API probe uses the deployed
`app.db.engine`, establishes a repeatable-read, read-only PostgreSQL transaction,
and verifies both properties with `SHOW` **before any probe-issued data SELECT**. It rolls back
on all normal paths. Data statements are parameter-bound SELECTs of schema/account
metadata and grouped ledger totals; no ORM session, native summary, provider,
reconciliation, account creation or paid request is used.
Driver connection initialization can issue its own metadata/health queries before
the explicit transaction; no live PostgreSQL behavior has been claimed or tested.

Output contains schema version, exact account existence/cap, aggregate settled and
reserved amounts, uncertain counts/amounts, conservative remaining balance, old
pre-ledger uncertain exposure, and source/registry/container version hashes. It
omits individual operation identifiers, provider/task details, receipt values,
requests, credentials, DSNs and process environments. `reserved_usd` already
includes `uncertain_usd`; do not subtract uncertainty twice. `available_usd` is
ledger arithmetic, **not permission to spend**. An unregistered US$200 account is
not treated as the remake's approved US$25 account.

The old historical closure is excluded only for its exact reviewed operation and
receipt, settled status, active old slug, registered/stored US$25 cap, matching
runtime source hashes, and **one row with actual = maximum = US$25**. Both SQL
parameters and the pure arithmetic check enforce the full amount. A matching
receipt on US$1 or US$26 does not qualify. Missing/anomalous history remains in
settled/reserved totals, emits a fixed reason, and makes `available_usd` unknown;
`observed_ledger_remaining_usd` retains the unexempted arithmetic. An exact full
US$25 uncertain history remains reserved once and is explicitly marked uncertain.

On runtime source mismatch, all settled history stays counted conservatively and
the readback is incomplete/unknown. The worker guard is not imported unless its
hash matches its reviewed baseline. Schema output includes only fixed reviewed
revision identifiers; other DB text is counted without reflection. Schema mismatch
yields unknown account/balance rather than a fabricated zero. The wrapper projects
all component fields onto explicit type/value allowlists and replaces retained
component JSON with that projection before writing/printing its safe summary.

`umask 077` protects `/tmp/c03-budget-metadata.*`; only safe JSON is retained.
The wrapper prints the same safe summary and its private result directory. It
discards component stderr rather than exposing connection errors. Exit `3` means
the required hashbound account/schema/worker metadata was obtained and paid work
remains `NOT_READY`. Exit `4` and `metadata_complete=false` mean metadata is
unavailable or insufficient, including an absent account, source mismatch, missing
balance fields or unverified historical closure.
There is deliberately no success exit that authorizes provider dispatch.

The v1 scripts, original sourcebinding and original `MUST_FIX` review are preserved
under `history/host-budget-metadata-v1/`; the current independent report is also
unchanged. Its historical 21 author fixtures have not been rewritten as v2 results.
V2 local validation consists of shell syntax, Python compilation and 16 focused
regression/baseline fixtures for full-ceiling closure, unknown revisions, wrapper
projection/completeness, and the US$200 mismatch. Only local stubs and Python
subprocesses were used; no live PostgreSQL/Compose/host/network/provider was
contacted. File hashes and scope are recorded in
`host-budget-metadata-sourcebinding.json`; independent re-review is pending.
