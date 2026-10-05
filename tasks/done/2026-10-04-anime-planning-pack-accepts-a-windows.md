---
id: 2026-10-04-anime-planning-pack-accepts-a-windows
title: Anime planning pack accepts a Windows directory junction as the pack itself
status: done
priority: P3
area: api
owner: claude-opus-5-5-incomplete-tickets
claimed_at: 2026-10-04T16:50:18Z
created_at: 2026-10-04T15:17:34Z
completed_at: 2026-10-04T16:58:42Z
branch: claude/anime-pack-junction
depends_on: []
scope:
  - apps/api/app/video_automation/planning.py
  - apps/api/tests/test_video_anime_planning.py
---

# Anime planning pack accepts a Windows directory junction as the pack itself

## Why

`prepare_bundle` (behind `python -m app.video_automation.planning_cli --pack <dir>`) refuses a
pack directory that is a symbolic link: `pack.is_dir() and not pack.is_symlink()`, "pack must be
a real directory". On Windows a directory junction is a link too (a mount-point reparse point,
`st_reparse_tag == IO_REPARSE_TAG_MOUNT_POINT`), but Python reports `is_symlink()` as `False`
for it, so a `--pack` that is a junction is read as if it were a real checked-in directory and
the bundle's `source` is labelled `docs/videos/series-plans/<junction name>` while its bytes come
from wherever the junction points. Any Windows account can create a junction without privileges,
unlike a symbolic link.

Measured on 2026-10-04 (Windows 11, CPython 3.13.15, account without
SeCreateSymbolicLinkPrivilege) with a scratch probe that copied
`docs/videos/series-plans/borrowed-dawn` to a temporary directory and called `prepare_bundle`:

| Fixture | `is_symlink()` | `is_junction()` | Result |
| --- | --- | --- | --- |
| Pack directory is a junction to a full copy elsewhere | False | True | **accepted** |
| `README.md` inside the pack is a junction to a directory | False | True | refused, "pack cannot contain symlinks" |
| `README.md` inside the pack is a junction aimed at a file | False | True | refused, "pack cannot contain symlinks" (reading it raises `PermissionError`) |

The entry check only refuses junction children because `is_file()` is `False` for them, not
because it recognises the link. Linux production cannot create junctions and its symlink check
already works, so this is a Windows-operator gap in the "the pack is a real directory" contract,
not a production incident.

## Definition of done

- [x] `prepare_bundle` refuses a pack directory that is a Windows directory junction with the
      same "pack must be a real directory" error it gives a symbolic link.
- [x] Entries that are junctions are refused by an explicit link check, not only as a side
      effect of `is_file()`.
- [x] A test proves the pack-junction refusal on Windows with a real junction
      (`_winapi.CreateJunction`), skipped elsewhere with a reason; the existing symlink
      coverage stays.

## Steps

- [x] Add `or pack.is_junction()` (Python 3.12+, the project requires 3.13) to the pack check,
      and to the per-entry check; keep the messages.
- [x] Add a `test_prepare_checks_actual_directory`-style case that makes the pack itself a
      junction; reuse the file's `windows_only` marker and the junction fixture in
      `link_readme`.
- [x] Run the focused planning tests on Windows and let Linux CI cover the symlink case.

## How to verify

From `apps/api` on Windows:

```bash
PYTHONUTF8=1 uv run pytest tests/test_video_anime_planning.py tests/test_video_anime_planning_cli.py -q -rs
uv run ruff check . && uv run mypy app && uv run mypy tests
```

The new pack-junction case must fail before the validator change and pass after it.

## Notes

- Found while making the `[symlink]` fixture portable
  (`2026-10-04-python-anime-planning-symlink-windows`); that ticket only changed the test file
  and deliberately left the validator alone.
- `os.path.isjunction` / `Path.is_junction` exist since Python 3.12; on non-Windows they always
  return `False`, so the added check is a no-op on Linux.
- Do not resolve the path before the check: `resolve()` follows the junction and hides it.
- 2026-10-04 (claude-opus-5-5-incomplete-tickets): `_is_link()` (`is_symlink() or is_junction()`)
  now guards both the pack and each entry, with the old messages. Claimed with `--force` over
  `2026-09-27-video-drama-room-withdraw-a-one` (landed as #870) and
  `2026-10-03-illustrated-slides-round-2-a-family` (landed as #1172), both stale.
- New `test_prepare_refuses_a_pack_that_is_itself_a_junction` (Windows only): fails on
  origin/main's validator ("1 failed, 1 passed" with `-k junction`), passes with the change.
  `PYTHONUTF8=1 uv run pytest tests/test_video_anime_planning.py tests/test_video_anime_planning_cli.py -q -rs`:
  87 passed, 1 skipped (the `[symlink]` privilege skip). `ruff` clean; `mypy` and
  `mypy --platform linux` on the two changed files clean; the full `mypy app`/`mypy tests` run is
  left to CI.
