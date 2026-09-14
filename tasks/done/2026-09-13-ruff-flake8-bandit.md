---
id: 2026-09-13-ruff-flake8-bandit
title: ruff does not run flake8-bandit, so the checks miss whole classes of finding
status: done
priority: P3
area: api
owner: claude-opus-5
claimed_at: 2026-09-14T01:00:35Z
created_at: 2026-09-13T23:37:54Z
completed_at: 2026-09-14T05:16:09Z
branch: claude/security-check-o5zaj1
depends_on: []
scope:
  - apps/api/pyproject.toml
  - apps/api/app/auth/oauth.py
  - apps/api/app/auth/schemas.py
  - apps/api/app/auth/service.py
  - apps/api/app/config.py
  - apps/api/app/infra.py
---

# ruff does not run flake8-bandit, so the checks miss whole classes of finding

## Why

`apps/api/pyproject.toml` selects `["E", "F", "I", "UP", "B", "ASYNC"]`. Those catch style,
unused names, import order, outdated idiom, common bugs and async mistakes. None of them
look for security patterns.

ruff already ships those rules as the `S` ruleset (flake8-bandit) — it is a line in a
config file, not a new tool, a new dependency, or a new CI job. The 2026-09 audit noted
that `S` would have found two of its own findings mechanically: the unescaped LIKE
wildcards in `hotspots/service.py` (API-07) and the missing request body limit (API-05).
Both were found by a human reading code, which is the expensive way to find the cheap
class of problem.

The point is not that there is a known vulnerability hiding. `pip-audit` is clean, there is
no `subprocess` use outside the deployment agent's fixed `shell=False` command set, no
string-built SQL, and no hardcoded secrets. The point is that this check is free and
permanent, and the next hundred commits are written by several different agents.

`docs/security-audit-2026-09.md` filed this as recommendation #11.

## Definition of done

- [x] `S` is in `[tool.ruff.lint] select`, `uv run ruff check .` is clean, and CI enforces it
      on every push (`.github/workflows/ci.yml` already runs `ruff check`).
- [x] Every rule that had to be turned off is listed individually with the reason. No blanket
      `# noqa: S` anywhere, and no category-wide ignore.

## What fired, and what happened to it

10,395 findings, which sounds like a lot until they are sorted.

| Rule | Count | Disposition |
| --- | --- | --- |
| S101 `assert` | 10,209 | Off globally, one rule, with the reason in `pyproject.toml` |
| S106/S105 hardcoded password | 149 + 18 | Test fixtures ignored per-directory; 9 in `app/` given an inline `# noqa` each |
| S108 `/tmp` | 6 | Tests only — the deploy-agent cases bind a real unix socket |
| S608 SQL from a string | 4 | Migrations and one migration test: table names and status tuples from module constants |
| S311 non-crypto `random` | 3 | Fake prices and poll jitter |
| S603 subprocess | 2 | The deployment agent's fixed command set, and one test running a repo script |
| S310 `urlopen` | 2 | GitHub CI status on a built Request; health probe on a config URL |
| S314 `xml` | 1 | **A real gap.** Suppressed here, filed as `2026-09-14-airalo-feed-utf16-doctype` |
| S314/S310/S603 in `app/guides/pack_ingest.py` | 4 | Arrived from `main` after this task started — see below |
| S110 try/except/pass | 1 | Deployment failure cleanup, which must not mask the original error |

### The one real finding

`parse_airalo` guards its XML with `b"<!DOCTYPE" in body.upper()`, which only folds ASCII, so
a UTF-16 feed carrying a DOCTYPE walks straight past it. Not reachable by anyone but Airalo
— the URL is hardcoded — and `ElementTree` resolves no external entities, so the exposure is
entity-expansion DoS in the worker rather than file disclosure. Filed separately rather than
fixed here, because the choice between a one-line NUL strip and taking on `defusedxml` is a
real decision and this task is about turning the lint on.

### Why S101 is off rather than triaged

The rule exists because `python -O` compiles asserts out. Nothing here runs with `-O`; the
image starts `uvicorn app.main:app`. All 29 uses in `app/` narrow a type for strict mypy
(`assert x is not None`, `assert isinstance(...)`) rather than enforcing something a caller
could violate, and in `tests/` an assert is the point. Turning it on would mean 29 `# noqa`
comments across 20 files for no change in behaviour, and would bury the eight rules that
actually found something. The `pyproject.toml` comment says to turn it back on first if the
service ever runs with `-O`.

### What arrived from main mid-task

`main` gained `app/guides/pack_ingest.py` (#468) after this branch was cut, and the merge
commit was the first place the new rules met it — CI went red on the PR while the branch
alone was green. The content-pack CLI is not reachable from any request, so `S314` (an SVG
from the repo workspace) and `S603` (headless Chromium, fixed argument list, `shell=False`)
are suppressed with reasons. `S310` is the one with something behind it: the transport hands
`urlopen` whatever URL Commons returned, and `urlopen` opens `file:` too. Filed as
`2026-09-14-pack-ingest-urlopen-scheme` rather than fixed inline, for the same reason as the
Airalo one — this task is about turning the lint on, not about changing another module's
behaviour.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest -q
```

The rules that matter are still live — checked by running ruff over a scratch file containing
one violation each: `S608` (SQL built by concatenation), `S602` (`shell=True`), `S324` (MD5),
`S501` (`verify=False`), `S113` (request with no timeout). All five fire.

## Notes

- Every suppression is either an inline `# noqa: S###` with the reason on the same line, or a
  per-file entry with a comment above it. A rule that is off for a stated reason is
  documentation; a rule that is off for no reason is the same as never having added it.
- The nine `app/` S105 hits are all names, not values: three OAuth endpoint URLs, a Redis key
  prefix, a request header name, the `bearer` token type, a bot User-Agent, the placeholder
  `APP_SECRET_KEY` that production refuses by name, and the comparison that refuses the
  default database password.
- **Scope overlap:** `app/auth/schemas.py` and `app/config.py` are also held by
  `2026-09-13-password-policy-length-only` and `2026-09-13-analytics-hash-key-separation`.
  Both are this agent's own tasks on this same branch, so there is no second writer; the
  overlap is recorded rather than left for a merge to find.
- Filed by the 2026-09-13 security review (`docs/security-review-2026-09-13.md`).
