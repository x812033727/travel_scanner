---
id: 2026-10-04-python-anime-planning-symlink-windows
title: Make Python anime planning symlink fixture portable on Windows
status: done
priority: P3
area: api
owner: claude-opus-5-5-anime-symlink-fixture
claimed_at: 2026-10-04T14:45:32Z
created_at: 2026-10-04T07:14:15Z
completed_at: 2026-10-04T15:20:49Z
branch: claude/anime-planning-symlink-windows
depends_on: []
scope:
  - apps/api/tests/test_video_anime_planning.py
---

# Make Python anime planning symlink fixture portable on Windows

## Why

On Windows without symbolic-link privileges, `test_prepare_checks_actual_directory[symlink]` raises `OSError: [WinError 1314] A required privilege is not held by the client` while creating its fixture. The failure occurs at `target.symlink_to(PACK / "README.md")`, before `prepare_bundle` can exercise its link rejection. This prevents the API suite from passing on an ordinary Windows checkout even though the planning validator is unchanged.

The test must remain meaningful: a portability fix must retain real filesystem coverage proving that linked input cannot bypass the bundle's directory boundary.

## Definition of done

- [x] The planning tests handle Windows hosts without symbolic-link privileges explicitly, without requiring privilege changes on the host.
- [x] Real symlink rejection remains covered on platforms that can create symlinks; Windows symlink or junction rejection uses actual filesystem metadata wherever the platform permits it.
- [x] Any platform skip is narrow and explains the unavailable fixture capability; it does not replace all link rejection coverage or loosen the production validator.
- [x] The focused planning tests pass on Windows and the existing POSIX link refusal remains covered.

## Steps

- [x] Inspect `test_prepare_checks_actual_directory` and the existing linked-input validation contract before choosing the smallest fixture change.
- [x] Adjust only `apps/api/tests/test_video_anime_planning.py`, preserving real link rejection coverage and explicit handling of fixture permission failure.
- [x] Run the focused Windows tests and verify the POSIX symlink rejection path in an environment that supports symlinks.

## How to verify

From `apps/api`, reproduce the original Windows failure:

```powershell
.venv/Scripts/python.exe -X utf8 -m pytest 'tests/test_video_anime_planning.py::test_prepare_checks_actual_directory[symlink]' -q
```

After the fix, run the whole planning file without deselection:

```powershell
.venv/Scripts/python.exe -X utf8 -m pytest tests/test_video_anime_planning.py -q
```

The bounded baseline rerun excluded only the fixture that could not be created:

```powershell
.venv/Scripts/python.exe -X utf8 -m pytest tests/test_video_anime_production_policy.py tests/test_video_anime_planning.py tests/test_video_anime_planning_cli.py '--deselect=tests/test_video_anime_planning.py::test_prepare_checks_actual_directory[symlink]' -q
```

Baseline result: **173 passed, 1 skipped, 1 deselected in 25.68 seconds**, exit 0. A separate UTF-8 rerun without deselection had **173 passed, 1 skipped, 1 failed**, with only `WinError 1314` remaining.

## Notes

- Observed on Python 3.13.15, Windows AMD64. Without `-X utf8`, the preferred encoding was `cp1252`; 26 production-policy failures and one planning-CLI failure came from test fixture reads using the default encoding. Those all passed under UTF-8 mode and are outside this task's scope.
- All three test files were unchanged in video recovery PR #1203. This is a local Windows fixture limitation, with no demonstrated product-source regression.
- Local evidence: `%TEMP%/mokaair-video-recovery-windows-portability.log`. Keep raw machine logs out of the commit.
- Related tickets have different scopes: `2026-09-12-api-windows-agents-md` covers warning/guide tests; completed `2026-09-26-guides-autolink-tests-windows-encoding` covers guide test encoding; completed `2026-10-03-anime-input-test-windows-junction` covers the Node anime-input test. No existing open ticket covered this Python planning fixture when this task was filed.
- This ticket is intentionally unclaimed. Do not change the production validator, permissions, or other API test files as part of this task.

### 2026-10-04 fix (claude-opus-5-5-anime-symlink-fixture)

- Claimed with `--force` over `2026-10-03-illustrated-slides-round-2-a-family`
  (claude-fable-5-1-illustration-round2, `review`, 30 h old, scope includes all of
  `apps/api/tests`). Its work landed as #1172 (`b0a264567`), which touched only
  `apps/api/tests/test_video_media_providers.py` under that directory.
- The validator's contract (`prepare_bundle`, unchanged): the pack must be a directory and not
  `is_symlink()`; every entry must be `is_file()` and not `is_symlink()`, else "pack cannot
  contain symlinks". Python reports `is_symlink()` as `False` for a Windows junction, but a
  junction is a directory, so an entry that is a junction fails `is_file()` and gets the same
  refusal. A scratch probe confirmed it for a junction aimed at a directory and at a file.
- The test now has two link cases. `[symlink]` is unchanged where symbolic links can be made
  (Linux CI, an elevated or Developer Mode Windows shell); only `WinError 1314`
  (`ERROR_PRIVILEGE_NOT_HELD`) turns into a skip that names the missing privilege, and any
  other `OSError` still fails. `[junction]` (Windows only, marker skip elsewhere with a reason)
  swaps `README.md` for a real junction made with `_winapi.CreateJunction`, asserts
  `is_junction()` so the fixture cannot quietly become a plain directory, and expects the
  refusal. Both link cases now `match="symlinks"`, so a missing-file or hash error cannot pass
  for the link guard; `missing` and `unexpected` match their own message.
- The junction points at an empty `outside` directory in `tmp_path`, not at the checked-in
  pack, so nothing that cleans or walks pytest's temporary tree can reach `docs/`.
- Measured on this Windows account (no symlink privilege), Python 3.13.15:
  before, `[symlink]` failed with `WinError 1314`; after, the three focused files gave
  **174 passed, 2 skipped** (the `[symlink]` privilege skip and the production-policy file's
  existing "requires PostgreSQL" skip), exit 0. `ruff check .`, `mypy tests` and
  `mypy --platform linux tests/test_video_anime_planning.py` are clean (the `_winapi` import
  sits under `sys.platform == "win32"`).
- POSIX: WSL could not be used from this agent's isolated worktree. The Linux `api-tests`
  shards in CI run `[symlink]` (real symbolic link, refused) and skip `[junction]` with its
  reason; the PR cannot merge without them green.
- Found, not fixed (validator out of scope): a pack directory that is itself a junction is
  **accepted**, because the pack check uses `is_symlink()` only. Filed as
  `2026-10-04-anime-planning-pack-accepts-a-windows` with the probe's evidence.
