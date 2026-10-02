# Ten drama production plans in the admin

On 2026-10-02 the original ten drama works received sixty new **v2 review**
documents: setting, outline and four chapter outlines per work. The setting books
include the current source-bound production direction for all 400 episodes,
selected Taiwan Mandarin voices, character looks, camera and sound direction,
switchable CC, and Japanese/Korean/English dubbing after Chinese-final acceptance.

Open <https://mokaair.com/zh-TW/admin/videos?tab=drama>, choose a work, then expand
its setting book's full text or production data. The generated production appendix
starts with `動畫攝製規格`. For example:
<https://mokaair.com/zh-TW/admin/videos?tab=drama&series=wedding-reckoning>.

## What was missing

The deployed release `a62483cc7` already contained PR #1094, but Git deployment
does not revise database documents. The admin still held the original sixty
2026-09-28 v1 review documents. Every body and authored series field matched the
historical import at `a14d45f8a`; there were no intervening admin edits, episodes
or production requests for these works.

The checked-in `production-20261001` bundles also predated some merged source
look/continuity changes. The synchronized documents were rebuilt in memory from
current sources, not copied from those older generated bundles. Historical
source receipts and the old database documents were retained.

## Executed scope and evidence

- Source revision: `0d7267d8d2d727de57260b34dde1caee5acda7bf`.
- Canonical reviewed package SHA-256:
  `5010ee303ae536bc0e994ff2de67e80b6ebc6ac4739c9d099b91fc77b0ec580e`.
- Executed updater file SHA-256:
  `286fbac28a9d1de50c2a90b5fd196e09b587f0048ecfd8866849eb09fd639486`.
- A fresh PostgreSQL custom archive was readable, mode 0600 and 175,550,845 bytes;
  SHA-256 `4f26d620c850b6066665105d311150f2306362ae63e18b85114451a9a52dfe69`.
- The default read-only PostgreSQL dry run selected exactly ten existing works
  and six revisions each. Application committed the full batch in one transaction.
- All sixty old document IDs, bodies and metadata remained identical. Each work
  now has twelve historical rows and exactly six latest v2 review documents.
- Every latest persisted body and the admin `series_view` serializer matched the
  candidate package. A subsequent read-only replay reported ten unchanged works.
- Series IDs/titles/statuses stayed the same. Only source premise/note corrections,
  `visual_tier=clips` and update timestamps changed on the series rows.
- Global media settings remained unchanged, `drama_enabled=false`, episode and
  request counts stayed zero, and every work's scheduler returned no next job.

Full snapshots, package, original dry run, apply receipt and replay receipt are
private operational artifacts outside Git. The small public verification summary
is [verification.json](verification.json).

## Guarded updater

`ops/video/sync_drama_plan_revisions.py` accepts a version-1 package with
`source_git_sha` and up to ten works. Each work pins the exact canonical hashes
of its existing series and all historical documents, six candidate documents,
`visual_tier: "clips"`, and optional `series_updates` limited to premise/note.

Use the API environment with `PYTHONPATH=apps/api`. Omit `--apply` for the read-only
dry run. Application requires `--apply --expected-sha256 <dry-run-package-hash>`.
The updater requires an active, unsuspended administrator, disabled drama
automation, undecided review documents, no episodes/requests and no pending owner
discussion. It locks and checks the entire batch before appending revisions;
drift, invalid documents or a failed transaction leave no partial update.

The CLI does not create series, grant approval, start generation or alter budgets,
provider settings, uploads or publication. Exact replay is a no-op only while
the audited post-state still matches. This deliberately limited updater is for
pre-production review works, not progressed or approved series.

## Validation and remaining acceptance

- Sync regression suite: **31 passed**; focused Ruff and mypy passed.
- Independent review covered source/package hashes, history, rollback, actor
  eligibility, idempotence and locks. SQLite transactions and PostgreSQL lock SQL
  compilation were tested; no PostgreSQL concurrency stress test was performed.
- Current `production-check`: ten works, 400 episode designs, no design errors.
- Real production PostgreSQL dry run, application and read-only replay passed.
- Production database and admin payloads were verified. **Authenticated browser
  rendering was not verified in this run.**

These are planning documents. No auditions, images, animated footage, pilot,
Chinese final, multilingual dubs or YouTube publication were produced. The
existing six works' minor-character provider constraints still apply. Global
provider/CC defaults were not changed by this sync; the per-work profile records
the Chinese-first CC/Veo Lite requirements and existing generation guards must
accept the actual provider configuration before any paid pilot.
