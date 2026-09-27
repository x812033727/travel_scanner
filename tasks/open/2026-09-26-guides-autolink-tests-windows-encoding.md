---
id: 2026-09-26-guides-autolink-tests-windows-encoding
title: test_guides_autolink writes Chinese fixtures without an encoding, so the four tests fail on Windows
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-26T02:55:16Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/tests/test_guides_autolink.py
---

# test_guides_autolink writes Chinese fixtures without an encoding, so the four tests fail on Windows

## Why

Running `uv run pytest` on a Windows checkout (2026-09-26, Python 3.13, locale cp1252) fails three tests and errors one in `tests/test_guides_autolink.py`: the fixtures write Chinese Markdown with `Path.write_text(...)` and no `encoding=`, so the cp1252 codec raises `UnicodeEncodeError` (`test_the_index_keeps_only_names_that_point_at_one_article`, `test_the_command_reports_and_applies_only_the_changed_packs`, `test_autolink_links_the_first_mention_once_with_word_boundaries`, `test_autolink_never_links_an_article_to_itself_and_respects_existing_links_and_the_cap`). CI runs on Linux with UTF-8 and is green, so the failures only cost time on the Windows dev machine, where every full local run has to deselect them.

## Definition of done

- [ ] `uv run pytest tests/test_guides_autolink.py -q` passes on Windows without `PYTHONUTF8=1`.
- [ ] No other test in the file, nor the module under test, changes behaviour on Linux.

## Steps

- [ ] Pass `encoding="utf-8"` to every `write_text` / `read_text` in the file's fixtures (and check `app/guides/autolink*.py` reads with an explicit encoding too; if it does not, that is a separate finding).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_autolink.py -q
```

## Notes

Found while running the whole suite for `2026-09-26-video-drama-settings-and-look-gates`; not touched there. `PYTHONUTF8=1` is a workaround for a local run, not a fix.
