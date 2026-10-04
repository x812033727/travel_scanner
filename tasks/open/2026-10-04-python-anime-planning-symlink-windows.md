---
id: 2026-10-04-python-anime-planning-symlink-windows
title: Make Python anime planning symlink fixture portable on Windows
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-04T07:14:15Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/tests/test_video_anime_planning.py
---

# Make Python anime planning symlink fixture portable on Windows

## Why

On Windows without symbolic-link privileges, `test_prepare_checks_actual_directory[symlink]` raises `OSError: [WinError 1314] A required privilege is not held by the client` while creating its fixture. The failure occurs at `target.symlink_to(PACK / "README.md")`, before `prepare_bundle` can exercise its link rejection. This prevents the API suite from passing on an ordinary Windows checkout even though the planning validator is unchanged.

The test must remain meaningful: a portability fix must retain real filesystem coverage proving that linked input cannot bypass the bundle's directory boundary.

## Definition of done

- [ ] The planning tests handle Windows hosts without symbolic-link privileges explicitly, without requiring privilege changes on the host.
- [ ] Real symlink rejection remains covered on platforms that can create symlinks; Windows symlink or junction rejection uses actual filesystem metadata wherever the platform permits it.
- [ ] Any platform skip is narrow and explains the unavailable fixture capability; it does not replace all link rejection coverage or loosen the production validator.
- [ ] The focused planning tests pass on Windows and the existing POSIX link refusal remains covered.

## Steps

- [ ] Inspect `test_prepare_checks_actual_directory` and the existing linked-input validation contract before choosing the smallest fixture change.
- [ ] Adjust only `apps/api/tests/test_video_anime_planning.py`, preserving real link rejection coverage and explicit handling of fixture permission failure.
- [ ] Run the focused Windows tests and verify the POSIX symlink rejection path in an environment that supports symlinks.

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
