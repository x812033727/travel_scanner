---
id: 2026-09-14-mypy-does-not-check-tests
title: mypy does not check tests, so a signature change breaks integration tests silently
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-14T04:33:01Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/pyproject.toml
  - .github/workflows/ci.yml
---

# mypy does not check tests, so a signature change breaks integration tests silently

## Why

CI runs `uv run mypy app`. `tests/` is never type-checked, and on 2026-09-14 that cost a
full CI cycle in a way worth writing down, because two blind spots lined up.

`2026-09-13-analytics-hash-key-separation` changed one signature:

```python
def _digest(key: bytes, purpose: str, value: str) -> str:   # was (secret: str, ...)
```

Every call site in `app/` moved with it. One call site in `tests/` did not:

```python
# tests/test_integration_postgres_redis.py
session_hash = _digest(get_settings().app_secret_key, "analytics-session", browser_session)
```

Nothing local caught it. mypy does not read `tests/`. And the one test that exercises it is
gated on `RUN_INTEGRATION_TESTS`, so it skips on a developer machine — the local run said
"3703 passed, 266 skipped" and looked clean. It surfaced thirteen minutes into CI as
`TypeError: key: expected bytes or bytearray, but got 'str'`.

Either gap alone is survivable. Together they mean a refactor can be green everywhere a
person looks and still be broken.

## Definition of done

- [ ] A call in `tests/` that does not match the signature in `app/` fails a check a
      developer can run before pushing.
- [ ] CI runs that check.
- [ ] The bar is written down: if `tests/` is checked less strictly than `app/`, this file
      says which settings differ and why.

## Steps

- [ ] Measure first: `uv run mypy tests` and count. `test_integration_postgres_redis.py`
      alone has 9 pre-existing errors, all `object` indexing in fixture payloads and none of
      them a real defect, so this is not a one-line change and should not be started as one.
- [ ] Decide the shape. Two candidates, and the second is probably right:
      - strict everywhere, fixing every existing error first — cleanest, largest;
      - a `[[tool.mypy.overrides]]` for `tests.*` that relaxes the rules those 9 errors trip
        (`no-any-return`, indexing an `object`) while keeping the ones that catch this class
        — `arg-type` above all, which is exactly what would have caught `_digest`.
- [ ] Add the check to `.github/workflows/ci.yml` next to `uv run mypy app`, as its own step
      so a failure names itself.
- [ ] Re-run the scenario that motivated this: change a signature in `app/`, leave a `tests/`
      caller alone, and confirm the check fails.

## How to verify

```bash
cd apps/api && uv run mypy app && uv run mypy tests && uv run pytest -q
```

## Notes

- The separate half of the same lesson — that integration tests skip locally and so are only
  ever exercised in CI — is not something to fix here. It is a reason to weight this task
  higher: type checking is the only pre-push signal that covers those files at all.
- Filed 2026-09-14 while getting #472 to green.
