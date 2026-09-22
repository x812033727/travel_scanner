---
id: 2026-09-22-give-guides-import-a-per-slug
title: Give guides-import a per-slug publish hold
status: review
priority: P1
area: api
owner: claude-opus-5
claimed_at: 2026-09-22T04:05:00Z
created_at: 2026-09-22T04:00:00Z
completed_at:
branch: claude/guides-import-publish-hold
depends_on: []
scope:
  - apps/api/app/guides/content_pack.py
  - apps/api/app/cli.py
  - apps/api/app/guides/publish_holds.json
  - apps/api/tests/test_guides_publish_holds.py
---

# Give guides-import a per-slug publish hold

## Why

PR #635 merged as `d52af4d9` with zero reviews although its own description said to keep
it a draft until the content and a Changi fare-boundary source correction had been
reviewed. The content is in `main` now, and nothing in the code would have stopped the
next `guides-import --publish` from shipping it: that command publishes "each imported
locale whose public version differs from the pack", and there was no per-slug hold, no
`skip_publish` and no held-article list.

Task `2026-09-22-do-not-publish-the-two-batch010` recorded the hold on the board, and said
plainly what it could not do: **a task file only stops someone who reads the board.** This
is the code-level guard it asked for.

`ops/release/hold.py` is not that guard. It blocks the whole deploy on the production host
through `/root/travel-scanner-deploy.hold`; it is not per-article and would stop unrelated
releases.

## What it does

`apps/api/app/guides/publish_holds.json` maps a slug to the reason it may not be published.

- **The hold stops publication only.** The draft still imports. An unpublished draft is
  invisible to readers, and blocking the import too would make an unrelated content sweep
  fail on a slug it never meant to publish.
- **A sweep skips held articles and reports them.** `--publish` over every pack publishes
  everything else and lists what it withheld under `publish_held` in the JSON report, so
  the refusal is visible rather than silent.
- **Naming a held slug with `--publish` is refused outright**, before anything is read or
  written, with the reason and the file to edit. Sweeping past a hold is the accident the
  guard is for; asking for a held slug by name is not that accident.
- **A hold never retracts live content.** Applying one to an already published article
  leaves it published and only stops the next publication. Unpublishing is an editorial
  decision, not an import.
- The list lives beside the packs, not inside one, because a pack is the thing under
  review -- rewriting it must not silently drop the hold on it. It cannot live in
  `app/guides/content/` because `load_packs` globs `*.json` there and validates every file
  as a pack.

## Definition of done

- [x] A held slug imports its draft and is never published, by sweep or by name.
- [x] Other packs in the same run still publish.
- [x] A publishing run reports what it withheld and why.
- [x] A hold on a slug with no pack fails a test rather than silently protecting nothing.
- [x] A malformed or missing hold list is refused or treated as empty, not ignored.
- [ ] Reviewed and merged.

## Steps

- [x] Seed the list with the two batch010 Singapore slugs and their reason.
- [x] Honour holds in `plan_import`, surface them in the plan and the report.
- [x] Refuse an explicitly named held slug in `import_guides`.
- [x] Tests in a new file, so the held scope on `test_guides_content_pack.py` is not
      contested.

## How to verify

```
cd apps/api
uv run pytest tests/test_guides_publish_holds.py tests/test_guides_content_pack.py -q
uv run ruff check app/cli.py app/guides/content_pack.py tests/test_guides_publish_holds.py
uv run mypy app
```

Measured on 2026-09-22: publish-hold tests 8 passed / 3 skipped (the PostgreSQL legs),
existing pack tests 9 passed / 5 skipped, ruff clean, mypy clean over 340 source files.

To see the guard from outside, ask to publish a held slug by name:

```
guides-import --slug singapore-4-day-itinerary --publish
```

It exits non-zero naming the slug, the reason and `publish_holds.json`.

## Notes

The claim was refused at first: `2026-09-17-commons-non-ascii-filename-ingest`
(claude-fable-5-1, `review` since 2026-09-19) holds `tests/test_guides_content_pack.py`.
The overlap was only that one file, so the tests went into
`tests/test_guides_publish_holds.py` instead of contesting the claim or forcing it.

The holds file ships the same way `app/guides/content/*.json` does -- hatchling's
`packages = ["app"]` takes everything under `app/` -- so no packaging change was needed.

Removing an entry is how a hold is cleared, and that is a reviewable diff, which is the
point.
