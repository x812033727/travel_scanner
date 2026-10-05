---
id: 2026-10-02-rebind-receipts-after-scrubbing-host-details
title: Rebind receipts after scrubbing host details from hash-bound evidence
status: done
priority: P3
area: docs
owner: claude-opus-5-5-receipts-rebind-scrub
claimed_at: 2026-10-05T06:17:23Z
created_at: 2026-10-02T17:16:40Z
completed_at: 2026-10-05T07:20:25Z
branch: claude/receipts-rebind-scrub
depends_on:
  - 2026-09-23-scrub-host-details-from-docs
scope:
  - docs/ai-terms-series/postgresql-validation.json
  - docs/ai-terms-series/publication.json
  - docs/article-localization/releases/2026-09-22/batch010-singapore
  - docs/article-localization/releases/2026-09-22/batch011-jeju
  - docs/article-localization/releases/batch021/evidence.json
  - docs/article-localization/releases/batch022/evidence.json
  - docs/catalog-content-reviews/2026-09-09-followup.json
  - docs/catalog-content-reviews/2026-09-09-followup-result.md
  - docs/videos/so-thats-why/season2/reviews/completion/T37.md
  - docs/videos/so-thats-why/season2/reviews/completion/T37.json
  - tasks/done/2026-09-22-localize-jeju-car-rental-guide-in.md
  - tasks/done/2026-09-23-release-localized-household-purchasing-guides-batch021.md
  - tasks/done/2026-09-23-release-localized-website-planning-guides-batch022.md
  - tools/repo-hygiene.test.mjs
  - apps/api/tests/test_catalog_content_review_followup.py
  - docs/videos/long-form/plans.json
  - apps/api/app/video_plans/data/catalog.json
  - tasks/done/2026-10-02-expose-reviewed-long-form-plans-in.md
---

# Rebind receipts after scrubbing host details from hash-bound evidence

## Why

Ticket 2026-09-23-scrub-host-details-from-docs replaced local user paths, the PuTTY
saved-session name and a disposable database password with placeholders in about 290 tracked
files. Eleven files were left alone because another file records their SHA-256, so editing
them would silently break that receipt:

| File still carrying a host detail | Recorded by |
| --- | --- |
| `docs/ai-terms-series/postgresql-validation.json` (session name, root login, user path, the disposable password) | `docs/ai-terms-series/publication.json`, written by `export_publication.py` |
| `docs/article-localization/releases/2026-09-22/batch010-singapore/release-candidate-equivalence.json` | `release-evidence.json` in the same folder |
| `docs/article-localization/releases/2026-09-22/batch011-jeju/` — `independent-content-review.json`, `release-candidate-equivalence.json`, `source-correction-review.json`, `structural-qa.json`, `svg-independent-review.json` | each other, `release-evidence.json`, and `tasks/done/2026-09-22-localize-jeju-car-rental-guide-in.md` |
| `docs/article-localization/releases/batch021/evidence.json` | `tasks/done/2026-09-23-release-localized-household-purchasing-guides-batch021.md` |
| `docs/article-localization/releases/batch022/evidence.json` | `tasks/done/2026-09-23-release-localized-website-planning-guides-batch022.md` |
| `docs/catalog-content-reviews/2026-09-09-followup.json` (237 paths; `apps/api/tests/test_catalog_content_review_followup.py` reads it) | `docs/catalog-content-reviews/2026-09-09-followup-result.md` |
| `docs/videos/so-thats-why/season2/reviews/completion/T37.md` | `T37.json` in the same folder |

`tools/repo-hygiene.test.mjs` tolerates exactly these counts in its `KNOWN` table and fails
if they grow. The container behind the password was deleted the day it was made, so nothing
here is live; it is recon-level data in a public repository.

## Definition of done

- [x] None of the files above contains a local user path, the saved-session name or the
      password, and every receipt that records their digest matches the new bytes.
- [x] Their entries are gone from `KNOWN` in `tools/repo-hygiene.test.mjs`.

## Steps

- [x] For each binder, decide: regenerate it with the tool that wrote it (for example
      `export_publication.py` for `publication.json`), or update the recorded digest by hand
      with a sentence saying the evidence was redacted on a later date and why.
- [x] Check whether any binder is itself bound (a digest of `release-evidence.json`,
      `T37.json`, and so on, recorded somewhere else) and follow the chain; also check
      `docs/videos/long-form/review.json`, which binds about 70 files.
- [x] Run `node --test tools/repo-hygiene.test.mjs`, `npm run test:tools`, and the API test
      that reads `2026-09-09-followup.json`.

## How to verify

```bash
node --test tools/repo-hygiene.test.mjs
npm run test:tools
cd apps/api && uv run pytest tests/test_catalog_content_review_followup.py -q
```

## Notes

- Use the placeholders the hygiene test names: `<repo>`, `<home>`, `<saved-session>`,
  `<disposable-password>`. Rotate nothing; history keeps the old bytes and rewriting it is out
  of scope.

### 2026-10-05 claude-opus-5-5-receipts-rebind-scrub

- **Claim and scope.** No active task or open PR touched any path here (who-is-on-it,
  2026-10-05). The scope grew by four paths, each a link in a digest chain the table above
  missed: `apps/api/tests/test_catalog_content_review_followup.py` pins `SEMANTIC_HASH`, a
  hash of the parsed follow-up manifest; `T37.json` is recorded in the `source_hashes` of
  `docs/videos/long-form/plans.json`, whose digest is `plans_sha256` in
  `apps/api/app/video_plans/data/catalog.json`, whose digest is in
  `tasks/done/2026-10-02-expose-reviewed-long-form-plans-in.md`.
- **Scrub.** Each file was rebuilt from `git show HEAD:<path>` with three substitutions and
  nothing else: the profile root `C:\Users\<account>` in every spelling (`\`, `\\`, `\\\\`,
  `/`) became `<home>` (355 matches in 11 files), the PuTTY session name `<saved-session>`
  (23, including the `scope` sentence and `preflight.ssh_session`, which the hygiene regex
  does not see) and the disposable password `<disposable-password>` (5). The counts equal
  the old `KNOWN` entries. Line endings are kept (the 2026-09-22 folder is `-text`; five of
  its receipts are CRLF) and every JSON file still parses. A check that re-applies only the
  substitutions to the HEAD bytes shows that eight files differ by placeholders alone and the
  three jeju receipts that bind each other also by their digest lines and one note each.
- **Rebind.** Digests were computed by script, never typed, in chain order: jeju
  `source-correction-review.json` and `structural-qa.json` → `independent-content-review.json`
  → `svg-independent-review.json` → `release-candidate-equivalence.json` → jeju
  `release-evidence.json` and the jeju done task; singapore `release-evidence.json`;
  `publication.json`; the batch021 done task (LF and CRLF digests) and the batch022 done task
  (CRLF digest, plus the LF one in a new bullet); `2026-09-09-followup-result.md` (semantic
  and file digests) and the API test's `SEMANTIC_HASH`; `T37.json`. Every hand-edited digest
  has a dated sentence beside it (`redaction_note`, `receipt_redaction_note` or
  `evidence_redaction_note` in JSON, a sentence in Markdown) naming the commit that holds the
  unredacted bytes and the first digest: 53bd1b8a2 (#489), 65ef4328b (#648), ffa424762 (#693),
  048d20f8f (#696), 2bd7c5153 (#376), 6d60a1efb (#1098), a62483cc7 (#1115).
- **Regenerated by their own tools.** `plans.json` with `node tools/video/long-form/cli.mjs
  build` (only the T37.json line changed) and `catalog.json` with `node
  tools/video/long-form/admin-catalog.mjs build` (only `plans_sha256`; still 7,897,635 bytes;
  `check` passes). `publication.json` cannot be regenerated: `export_publication.py` needs the
  private host snapshots `--release-state`, `--journal` and `--backup-receipt`. Instead its own
  `sha()` over `REPORT_NAMES` and `postgresql_proof()` on the redacted report were run; both
  equal what `publication.json` records.
- **Search.** Before and after, every changed file's SHA-256 (raw, LF, CRLF), base64, SHA-1,
  MD5, git blob id and parsed-JSON hashes were searched for across all tracked files. Each new
  digest is recorded exactly where the old one was. The old digests remain only where they
  should (next bullet).
- **Left on purpose.**
  - `docs/videos/long-form/review.json` and `review.md` still record the old `plans.json`
    digest. That is the duration receipt: it needs an independent DURATION_ONLY increment and
    is not edited here. `node tools/video/long-form/cli.mjs check` prints
    `stale duration review binding: docs/videos/long-form/plans.json` (the only stale file,
    also after rebasing onto #1235, which added its own increment).
  - `apps/api/app/video_plans/REVIEW.md` keeps the reviewed catalog digest. The expose task
    records that file, by its own SHA-256, as the reviewer's report copied unchanged, and three
    of its 24 rows were already historical. The expose task's new note says so.
  - `docs/videos/series-plans/production-20261002-{handoff,voice}-review/duration-review-before.*`
    keep the old `plans.json` digest: they archive an earlier receipt, and `review.md` says
    those archives keep their recorded values.
  - In `postgresql-validation.json`, the root login (`-l root`, `ssh_user`), the disposable
    run's server temp directory (named in `cleanup.retained_private_source_directory` for
    whoever removes it), the loopback tunnel addresses and one Docker bridge address stay. The
    Definition of done names only the three details above, the deploy runbook already documents
    the root login, and none of these names or reaches the host.
  - The batch022 outside root review (not in the repository) records the old Git blob; that
    blob is in 048d20f8f.
- **Checks (Windows, 2026-10-05).** `node --test tools/repo-hygiene.test.mjs` 3/3;
  `node docs/videos/so-thats-why/season2/validate.mjs --batch=completion` PASS;
  `node tools/video/long-form/admin-catalog.mjs check` PASS; `cd apps/api && PYTHONUTF8=1 uv
  run pytest tests/test_catalog_content_review_followup.py tests/test_video_plans.py -q` 61
  passed, `ruff check` and `ruff format --check` clean; `npm run check:tasks` exit 0.
  `npm run test:tools`: 1,634 pass, 2 skipped, 3 fail. One is the expected duration-receipt
  test (`review.test.mjs`, plans.json stale until the increment), one the known Windows-only
  `tts/check` test, and one `nginx-install.test.mjs` whose 300-round bash loop hit its 90 s
  spawn timeout on a loaded machine (it reads only `ops/nginx/install.sh`, which this change
  does not touch; it failed the same way when run alone).
- **Filed** 2026-10-05-scrub-local-user-paths-from-the for the ten
  `docs/videos/sothatswhy-t27/` files still in `KNOWN`: their task is done, so the "another
  ticket's" reason no longer holds, and two of them are hash-bound inside that folder.
