---
id: 2026-09-26-guides-autolink-tests-windows-encoding
title: test_guides_autolink writes Chinese fixtures without an encoding, so the four tests fail on Windows
status: done
priority: P3
area: api
owner: codex-test-isolation
claimed_at: 2026-09-29T06:43:10Z
created_at: 2026-09-26T02:55:16Z
completed_at: 2026-09-29T06:51:43Z
branch: codex/test-isolation-fixes
depends_on: []
scope:
  - apps/api/tests/test_guides_autolink.py
---

# test_guides_autolink writes Chinese fixtures without an encoding, so the four tests fail on Windows

## Why

Running `uv run pytest` on a Windows checkout (2026-09-26, Python 3.13, locale cp1252) fails three tests and errors one in `tests/test_guides_autolink.py`: the fixtures write Chinese Markdown with `Path.write_text(...)` and no `encoding=`, so the cp1252 codec raises `UnicodeEncodeError` (`test_the_index_keeps_only_names_that_point_at_one_article`, `test_the_command_reports_and_applies_only_the_changed_packs`, `test_autolink_links_the_first_mention_once_with_word_boundaries`, `test_autolink_never_links_an_article_to_itself_and_respects_existing_links_and_the_cap`). CI runs on Linux with UTF-8 and is green, so the failures only cost time on the Windows dev machine, where every full local run has to deselect them.

## Definition of done

- [x] `uv run pytest tests/test_guides_autolink.py -q` passes on Windows without `PYTHONUTF8=1` (verified with the existing API venv Python directly).
- [x] No other test in the file, nor the module under test, changes behaviour on Linux (only explicit UTF-8 file I/O arguments; Linux execution remains CI verification).

## Steps

- [x] Pass `encoding="utf-8"` to every `write_text` / `read_text` in the file's fixtures (and check `app/guides/autolink*.py` reads with an explicit encoding too; if it does not, that is a separate finding).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_autolink.py -q
```

## Notes

Found while running the whole suite for `2026-09-26-video-drama-settings-and-look-gates`; not touched there. `PYTHONUTF8=1` is a workaround for a local run, not a fix.

### 2026-09-29 fix and local validation

The pre-claim survey found no active overlapping task or open PR on the test
file. All 103 worktrees containing it had identical LF-normalized contents, and
none held an active claim on this ticket.

Added explicit UTF-8 to the Chinese Markdown fixture write and the two remaining
JSON reads (`reader.json` and `untouched.json`). All other fixture reads/writes
already selected UTF-8. The production `app/guides/autolink.py` has four explicit
UTF-8 reads and one explicit UTF-8 write, so no production change was needed.
An AST comparison confirms the test file is unchanged after removing exactly
these three added encoding keywords; test data and assertions are preserved.

Reproduced and verified with `.venv/Scripts/python.exe` from `apps/api`, Python
3.13.15, Windows cp1252, `sys.flags.utf8_mode == 0`, and neither `PYTHONUTF8` nor
`PYTHONIOENCODING` set. The complete module ran with `-p no:cacheprovider` and an
external temporary directory; no test was deselected.

- Before: 1 failed, 2 passed, 3 fixture errors in 13.75 seconds; exit 1.
  The fixture write raised `UnicodeEncodeError`; the first implicit JSON read
  raised `UnicodeDecodeError`. This is the current reproduction count, distinct
  from the original report above.
- After final formatting: 6 passed in 4.46 seconds; exit 0.
- `ruff check tests/test_guides_autolink.py`: exit 0.
- `mypy tests/test_guides_autolink.py`: no issues in one source file; exit 0.

Full logs remain outside the repository. This is local Windows validation;
Linux/current-head CI is not claimed here. The coordinating task will perform
the final board move and PR submission. No branch operation, production access
or production module edit was performed by the fixing agent.
