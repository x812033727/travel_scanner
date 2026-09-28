# Put the authored works on the admin review site

Merging the source packages does not register them on `/zh-TW/admin/videos`.
The existing admin UI can show these works once they are imported. This operation
does not require a frontend release or enabling the drama worker.

## Drama documents: PRs #881 and #894

`ops/video/import_drama_plans.py` imports both packages using the current API
models. It validates the manifest hashes and document schemas, then creates the
ten works and sixty documents in **one transaction**. Every document is `review`,
every work is `setting`, and `hands_off` remains false. There are no episode,
request, media, or approval records. A worker sees the waiting setting document
and has no job, even if drama automation is enabled later.

An identical replay is a no-op. An existing unrelated, edited, or progressed work
causes the entire batch to be refused. The audit records the administrator, source
package, and content hashes. No source document or existing work is overwritten.

Prepare a portable bundle locally, with the API virtual environment installed:

```powershell
$env:PYTHONPATH = (Resolve-Path apps/api).Path
$batches = @(
  'docs/videos/series-plans/binge-five-20260928',
  'docs/videos/series-plans/claude-binge-five-20260928'
)
$packPaths = $batches | ForEach-Object {
  Get-ChildItem -LiteralPath $_ -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName 'series-request.json')
  }
}
$argsForImport = @('ops/video/import_drama_plans.py', '--prepare', 'drama-bundle.json')
foreach ($packPath in $packPaths) {
  $argsForImport += @('--pack', $packPath.FullName)
}
& apps/api/.venv/Scripts/python.exe @argsForImport
```

The prepared bundle is an operational artifact; keep it outside Git. In an API
environment, first run the database dry run (no `--apply`). After the owner
authorizes the production import, apply exactly the reviewed bundle hash:

```text
python import_drama_plans.py --input drama-bundle.json
python import_drama_plans.py --input drama-bundle.json --apply --expected-sha256 <dry-run-hash>
```

The CLI uses the sole configured active administrator when unambiguous. Otherwise
select one using `--actor-email`, without logging account addresses or credentials.
The production transfer/execution follows the `prod-host-ops` skill; preparing a
bundle and passing tests do not mean the production import has happened.

After applying, reload `/zh-TW/admin/videos?tab=drama`. Confirm all ten titles,
open each work, and verify six readable documents and the waiting-for-review
state. Do not approve documents merely to make cards appear. Record the import
hash, timestamp, counts and browser result in the task.

## Conventional video plans: PRs #867, #868 and #891

`ops/video/import_outline_reviews.mjs` prepares ten conventional video plans for
the existing project/report and review APIs. Submission is an outline review with
the original `brief.md` hash and no automated pick. It does not run Jev, produce
media, or approve anything. Prepare and inspect the bundle before applying:

```text
node ops/video/import_outline_reviews.mjs --prepare <outside-repo>/outline-bundle.json
node ops/video/import_outline_reviews.mjs --input <outside-repo>/outline-bundle.json
node ops/video/import_outline_reviews.mjs --input <outside-repo>/outline-bundle.json --apply --expected-sha256 <dry-run-hash>
```

Keep the adjacent `.receipt.json` after an interrupted apply; it identifies this
operation's partial registration so a retry cannot take over an unrelated card.

Run this bounded recovery only while the operator has exclusive control of the
ten target slugs. The existing project/report and review APIs are separate,
unconditional writes: the helper detects collisions already visible at preflight,
but cannot prevent a concurrent writer from changing a target between GET and
PUT/POST. The drama importer has a single database transaction; the conventional
outline helper does not offer that same guarantee or whole-batch rollback.

The four #867/#868 cuts have not cleared the owner's outline gate. The two #867
MP4s found locally have speech hashes that no longer match the current source;
the #868 final files were not found in the standard work directory. The six #891
scripts still need independent verification and comparison with existing topics.
These limitations must remain visible in the submitted review summaries.

Before production submission, also check the server worker's work directory for
existing `auto.json` files for the target slugs. The project API does not create
worker state, but a pre-existing worker state could already own that work.

After submission, reload `/zh-TW/admin/videos?tab=reviews` and confirm each title
has the full brief and a pending outline review. This is not final-video review.

## Remaining review previews

- #880: recover and hash-check the six long and twelve Shorts cuts from the
  original production directory. The packaging worktree contains receipts but
  none of those MP4s. Its custom source format needs a review adapter.
- #871: three Shorts pilots were found and match their delivery hashes. Their
  submission is separate from this import. The initial audit preceded the Shorts
  admin tab in #912; it is now on main alongside the backend. Verify the deployed
  version and push tool before submitting the pilots. #901 supplies BFF routes,
  **not** the admin tab.

The completed implementation task is
`tasks/done/2026-09-28-pr881-drama-plan-admin-import.md`. Remaining browser and
media acceptance is tracked in
`tasks/open/2026-09-28-verify-imported-review-pages-and-reconcile.md`.

## Production receipt

On 2026-09-28, following explicit owner approval, both batches were imported.
Read-only production verification at `2026-09-28T11:48:29.792642Z` confirmed
10 drama works with 60 readable review documents and 10 conventional projects
with one pending outline review each. No episode/request/media rows, approvals,
review attachments or publication fields were created for these targets.

- Drama bundle: `722f4ad0991608aa1455e2fb1fdb5de0723f936e5960af1f3a15e0ada0f0b1a1`.
- Outline bundle: `60deef472e42fdb99090ce21cfac3f37478ec1d1149d958a394e4b5460665604`.

Browser control was unavailable, so rendered-page acceptance remains outstanding.
The import and source-package manifests describe different points in time; their
original `admin_series_created: false` fields remain historical authoring evidence.
