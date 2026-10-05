---
id: 2026-10-05-sqlalchemy-2-1-4-bump
title: Bump SQLAlchemy to 2.1.4 once it is released (sqlalchemy#13639)
status: blocked
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-05T04:10:58Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/pyproject.toml
  - apps/api/uv.lock
---

# Bump SQLAlchemy to 2.1.4 once it is released (sqlalchemy#13639)

## Why

Production runs SQLAlchemy 2.1.3 (#1226, deployed 2026-10-05). In 2.1.0–2.1.3, iterating a
Result keeps it alive in a reference cycle (sqlalchemy#13639), so ORM objects stay in the
session's identity map until cyclic GC runs. A later re-read of the same row keeps the values
loaded before. The fix is in 2.1.4, which was not released on 2026-10-05.

#1246 fixed the paths where this decided something (the locked re-reads in the Shorts claim,
the Shorts sender, the YouTube connection check and link maintenance; see
`tasks/done/2026-10-05-shorts-claim-re-reads-its-locked.md`). Those fixes hold on any
version. The bump still matters: until then every iterated result lives longer than it should,
in memory and in the identity map.

## Definition of done

- [ ] apps/api runs SQLAlchemy 2.1.4 or later, with the full API checks green.

## Steps

- [ ] When 2.1.4 is on PyPI: `cd apps/api && uv lock --upgrade-package sqlalchemy && uv sync --frozen`.
- [ ] Read the 2.1.4 changelog for typing changes first (#1226 had to retype selects for 2.1),
      then run the API checks from AGENTS.md.
- [ ] Deploy with the `deploy` skill.

## How to verify

```bash
cd apps/api && uv run python -c "import sqlalchemy; print(sqlalchemy.__version__)"
uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest
```

## Notes

- Blocked on the upstream release of SQLAlchemy 2.1.4 (not on PyPI on 2026-10-05).
- Do not wait for Dependabot. On #958 (2026-09-28), `@dependabot ignore sqlalchemy minor
  version` was answered "I won't notify you about version 2.1.x of sqlalchemy again, unless
  you unignore it". 2.1.4 is inside 2.1.x. GitHub's docs say neither whether a patch inside an
  ignored minor is covered, nor whether the manual move to 2.1.3 (#1226) lifted the ignore.
  On the next uv Dependabot PR, `@dependabot show sqlalchemy ignore conditions` tells, and
  `@dependabot unignore sqlalchemy` clears it. Commenting is the owner's call.
