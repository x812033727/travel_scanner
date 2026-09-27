---
id: 2026-09-27-trip-parser-test-midnight-flake
title: The trip parser LLM tests fail when a CI run crosses midnight UTC
status: done
priority: P3
area: api
owner: claude-opus-ci-subscription
claimed_at: 2026-09-27T00:26:17Z
created_at: 2026-09-27T00:26:15Z
completed_at: 2026-09-27T00:29:07Z
branch: claude/trip-parser-midnight-flake
depends_on: []
scope:
  - apps/api/tests/test_ai_trip_parser_llm.py
---

# The trip parser LLM tests fail when a CI run crosses midnight UTC

## Why

On 2026-09-27, the required `api` check failed on #827 and #834, two video pull requests that do not touch the trip parser. Both runs spanned 00:00 UTC. The failure was `tests/test_ai_trip_parser_llm.py:115`:

```
assert '2026-09-26' in '你是 Mokaair 的旅遊需求解析器…'
```

The test module sets `TODAY = datetime.now(UTC).date()` once, at import. `app/ai/trip_parser.py` calls `_today()`, which reads the clock again every time it builds the system prompt. A run that collects the module before midnight UTC and reaches that test after midnight therefore compares two different days.

## Definition of done

- [x] The trip parser tests read the same day as the parser, whatever the clock does between collection and the test.
- [x] A simulated midnight crossing (the collected module's `TODAY` moved back one day) fails the old test exactly as CI did and passes the new one.

## Steps

- [x] Add an autouse fixture that pins `trip_parser._today` to the module's `TODAY`.
- [x] Prove it with the simulation, then run the whole file, ruff and mypy.

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m pytest tests/test_ai_trip_parser_llm.py -q
```

The simulation used a throwaway pytest plugin. Its `pytest_collection_modifyitems` hook ran `item.module.TODAY -= timedelta(days=1)`. It has to patch `item.module`: pytest imports this file as `test_ai_trip_parser_llm`, not `tests.test_ai_trip_parser_llm`, so importing the module by that name edits a second copy. Old test: 1 failed, at line 115 with `'2026-09-26'`. New test: 1 passed.

## Notes

- The whole file passes (38 tests). `ruff check` and `mypy` on the file pass.
- The #827 and #834 runs that hit this were rerun once each; the failure was not caused by their code.
