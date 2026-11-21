# C03 host-only budget metadata probe

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
and verifies both properties with `SHOW` **before any data SELECT**. It rolls back
on all normal paths. Data statements are parameter-bound SELECTs of schema/account
metadata and grouped ledger totals; no ORM session, native summary, provider,
reconciliation, account creation or paid request is used.

Output contains schema version, exact account existence/cap, aggregate settled and
reserved amounts, uncertain counts/amounts, conservative remaining balance, old
pre-ledger uncertain exposure, and source/registry/container version hashes. It
omits individual operation identifiers, provider/task details, receipt values,
requests, credentials, DSNs and process environments. `reserved_usd` already
includes `uncertain_usd`; do not subtract uncertainty twice. `available_usd` is
ledger arithmetic, **not permission to spend**. An unregistered US$200 account is
not treated as the remake's approved US$25 account.

The old C03 exact owner-closed historical receipt is excluded only if the deployed
models/service/db/schema hashes match the reviewed baseline. If they differ, all
settled history remains counted conservatively, the result requires review, and
the worker guard is not imported unless its hash matches its reviewed baseline.
Schema mismatch yields unknown account/balance rather than a fabricated zero.

`umask 077` protects `/tmp/c03-budget-metadata.*`; only safe JSON is retained.
The wrapper prints the same safe summary and its private result directory. It
discards component stderr rather than exposing connection errors. Exit `3` means
the requested readback completed and paid work remains `NOT_READY`; exit `4`
means some metadata is unavailable/unknown, including an absent required account.
There is deliberately no success exit that authorizes provider dispatch.

Local validation: shell syntax, Python compilation, 18 API/arithmetic/transaction
fixtures and 3 real Node guard fixtures passed. No live PostgreSQL/Compose/host or
provider was contacted. SQL behavior against the actual production schema remains
to be observed by the connected operator. File hashes and scope are recorded in
`host-budget-metadata-sourcebinding.json`; do not substitute a different script.
