---
id: 2026-09-14-mypy-does-not-check-tests
title: mypy does not check tests, so a signature change breaks integration tests silently
status: in-progress
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T09:28:30Z
created_at: 2026-09-14T04:33:01Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/pyproject.toml
  - .github/workflows/ci.yml
  - apps/api/tests
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

- [x] A call in `tests/` that does not match the signature in `app/` fails a check a
      developer can run before pushing.
- [x] CI runs that check.
- [x] The bar is written down: if `tests/` is checked less strictly than `app/`, this file
      says which settings differ and why.

## Steps

- [x] Measure first: `uv run mypy tests` and count. `test_integration_postgres_redis.py`
      alone has 9 pre-existing errors, all `object` indexing in fixture payloads and none of
      them a real defect, so this is not a one-line change and should not be started as one.
- [x] Decide the shape. Two candidates, and the second is probably right:
      - strict everywhere, fixing every existing error first — cleanest, largest;
      - a `[[tool.mypy.overrides]]` for `tests.*` that relaxes the rules those 9 errors trip
        (`no-any-return`, indexing an `object`) while keeping the ones that catch this class
        — `arg-type` above all, which is exactly what would have caught `_digest`.
- [x] Add the check to `.github/workflows/ci.yml` next to `uv run mypy app`, as its own step
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

## Blocked, and a measurement for whoever picks this up

**2026-09-14, blocked on `2026-09-14-article-image-ci` (`codex-image-ci`)**, which is active
and also covers `.github/workflows/ci.yml`. `npm run tasks -- claim` refuses this task for
that reason and the refusal is correct — the CI step this task has to add lands in the same
file that task is editing. Nothing here needs to change first; claim it once that one is done.

While checking, one measurement worth recording because it changes the shape of the work:

```
$ uv run mypy tests
tests/test_guides.py: error: Source file found twice under different module names:
                             "test_guides" and "tests.test_guides"
tests/test_admin_operations_migration.py:10: error: ... [import-untyped]
Found 2 errors in 2 files (errors prevented further checking)
```

It does not get as far as type errors. The duplicate-module error is a layout problem —
`tests/` has no `__init__.py` and mypy resolves the same file under two module names — so
step one is `explicit_package_bases` plus `mypy_path`, or an `__init__.py`, before any count
of real errors means anything. The "9 pre-existing errors" figure quoted above came from
checking `test_integration_postgres_redis.py` on its own, which sidesteps the collision.

### 2026-09-19 done in repo (claude-fable-5-1)

Scope widened to `apps/api/tests` after the claim: the check cannot pass without touching the
tests it reads, and no active ticket held those files except the four another agent of the
same owner was editing at the time (`test_guides.py`, `test_food_integration.py`,
`test_database_operations_center.py`, `test_warning_codes.py`), which were done last.

**Layout.** `explicit_package_bases = true` in `[tool.mypy]`: mypy names every file from the
cwd (`app.x`, `tests.test_x`) and the "found twice" error is gone. Twelve test modules imported
their siblings as top-level modules (`from test_trip_preferences import harness`), which mypy
cannot resolve without a second package root that would recreate the collision; they now import
`from tests.test_trip_preferences import ...`, the form eleven other files already used. That
works at runtime because the editable install puts `apps/api` on `sys.path`.

**Measurement** (`uv run mypy tests` under `strict`): 2245 errors in 140 files. By code:
841 `no-untyped-def`, 560 `no-untyped-call`, 268 `arg-type`, 180 `attr-defined`, 65
`unused-ignore`, 61 `call-arg`, 57 `union-attr`, 39 `index`, 36 `type-arg`, 30 `list-item`,
20 `operator`, 20 `no-any-return`, 18 `import-not-found`, 16 `assignment`, 10 `dict-item`, 8
`var-annotated`, 7 `misc`, the rest single digits.

**The bar** (the `[[tool.mypy.overrides]]` for `tests.*` in `apps/api/pyproject.toml`):

| relaxed in tests | why |
| --- | --- |
| `disallow_untyped_defs`, `disallow_incomplete_defs`, `disallow_untyped_calls`, `disallow_untyped_decorators` | test functions are unannotated by convention; pytest calls them |
| `disallow_any_generics`, `warn_return_any` | JSON payloads are bare dicts |
| `warn_unused_ignores` | an ignore that app's stricter run needs must not fail here |
| `implicit_reexport` | fixtures are shared by importing them from other test modules |
| `disable_error_code`: `index`, `union-attr`, `operator`, `assignment`, `list-item`, `dict-item`, `var-annotated`, `misc`, `comparison-overlap`, `type-var`, `func-returns-value` | these describe the test's own literal data, not a call into `app/` |

Kept, and this is the point: `check_untyped_defs` (the bodies of unannotated tests are read),
`arg-type`, `call-arg`, `attr-defined`, `name-defined`, `return-value`, `override` and the
import codes — the codes that fire when `app/` changes and a test does not. Under that
override 511 errors remained (269 `arg-type`, 178 `attr-defined`, 61 `call-arg`, 3 singles),
all fixed in the tests without changing what any test exercises: `dict[str, Any]` for payloads
and kwargs, `cast(AsyncSession, fake)` for test doubles, `Base.metadata.tables[...]` for
`__table__`, `assert x is not None` for optionals, and `# type: ignore[code]` with a reason
where the stub is the problem (`add_exception_handler`, partial `model_construct`).

CI: `uv run mypy tests` runs as its own step after `uv run mypy app`.
