---
id: 2026-09-12-guide-content-pack-and-import-command
title: Guide content pack and import command
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-12T17:51:40Z
created_at: 2026-09-12T17:42:18Z
completed_at: 2026-09-12T17:55:03Z
branch: claude/travel-guide-10-posts-56a1a9
depends_on:
  - 2026-09-12-guide-offer-content-block
scope:
  - apps/api/app/guides/content_pack.py
  - apps/api/app/guides/content
  - apps/api/app/cli.py
  - apps/api/tests/test_guides_content_pack.py
  - docs/travel-guides.md
---

# Guide content pack and import command

## Why

There is no way to put an article into the database except clicking through the back
office or hand-posting the admin API. Ten launch articles, each with a hero, several images,
tables and partner blocks, in two languages, are not something to type into a form — and
their source of truth should be reviewable in a pull request, next to the images they
reference, and re-runnable when a fare changes. Migrations must never write an article
(`docs/travel-guides.md`), so this is a command, not a migration.

## Definition of done

- [x] `apps/api/app/guides/content/<slug>.json` is the authoring format: article identity
      and taxonomy plus one `GuideDocument` per locale, validated by a pydantic `ArticlePack`.
- [x] `python -m app.cli guides-import --actor-email <admin> [--dir …] [--slug …] [--locale …]
      [--publish] [--dry-run]` validates every pack first (pydantic, destination, topics, offer
      rules) and writes nothing if any fails; then writes per (slug, locale) through
      `admin_service` (create → translations → draft → optional publish), each its own commit,
      stopping at the first failure with a report
      (created / updated / unchanged / published / taxonomy_updated / failed). Re-running is a no-op.
- [x] A test walks the real `content/` directory: every pack validates, every referenced
      image exists under `apps/web/public` and is ≤300 KB, every locale cites a source
      (skipped when the web folder is not checked out).

## Steps

- [x] `content_pack.py`: `ArticlePack`, `load_packs(dir)`, `plan_import(session, packs)`
      (read-only), `apply_import(session, actor, plan, *, publish)`; "unchanged" compares
      normalised dumps (`GuideDocument.model_validate(draft_json).model_dump(mode="json")`),
      never raw `draft_json` (new rows carry `"hero": null`, old rows lack the key).
- [x] After `create_article`, call `update_article` when `featured`/`display_order` differ
      from the defaults (`ArticleCreate` has neither); re-read each locale's version from
      `article_detail` between draft and publish.
- [x] `cli.py` subcommand; actor resolved with `catalog_review/enrich_cli._admin_user`
      (`is_admin and is_active`); default directory `files("app.guides") / "content"`.
- [x] Errors are `ContentPackError(ValueError)` or re-wrapped `admin_service` errors — no new
      `AppError` literal outside `admin_service.py` (`tests/test_error_localization.py`).
- [x] `docs/travel-guides.md`: the format, the command, the deploy-time sequence.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.cli guides-import --actor-email <admin> --dry-run
```

On the VPS after deploy: `docker compose exec api python -m app.cli guides-import
--actor-email <admin> --dry-run`, then again with `--publish`.

## Notes

- `admin_service` functions each commit, so "all or nothing across ten articles" is not
  available without refactoring five write paths; the honest contract is validate-all, then
  per-article writes that stop at the first failure and are safe to rerun. The test
  `test_a_refusal_mid_run_is_reported_and_the_rest_waits` pins that contract.
- Fixtures are reused from `tests/test_guides.py` by assignment (`database = guides.database`),
  not import: an imported fixture name reused as a test parameter is F811 to ruff.
- Sibling tasks: `2026-09-12-guide-offer-content-block` (the blocks this format uses) and
  `2026-09-12-launch-articles-batch-1-ten-travel` (the packs themselves, the next PR).
