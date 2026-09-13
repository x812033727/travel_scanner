---
id: 2026-09-13-ruff-flake8-bandit
title: ruff does not run flake8-bandit, so the checks miss whole classes of finding
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-13T23:37:54Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/pyproject.toml
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

- [ ] `S` is in `[tool.ruff.lint] select`, `uv run ruff check .` is clean, and CI enforces
      it on every push.
- [ ] Every rule that had to be ignored is listed individually with the reason, not
      silenced as a whole category.

## Steps

- [ ] Add `"S"` to `select` and run `uv run ruff check .` to see the real list. Expect most
      of it in `tests/` — `S101` (assert) fires on every test file.
- [ ] Add `"tests/*.py" = ["S101"]` to `[tool.ruff.lint.per-file-ignores]`, which already
      has an entry for `deployment_agent/*.py`.
- [ ] Triage the rest one at a time. `S603`/`S607` on `deployment_agent/executor.py` are
      the deliberate design — a fixed command set run with `shell=False` — so ignore those
      two rules on that path with a comment saying so, not the whole `S` category.
- [ ] Fix anything that is a real finding rather than ignoring it. If a fix is larger than
      this task's scope, file it separately and link it here.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest -q
```

## Notes

- Resist a blanket `# noqa: S` or a category-wide ignore. A rule that is off for a stated
  reason is documentation; a rule that is off for no reason is the same as not having
  added it.
- `S` overlaps `B` in places; ruff resolves that itself, no action needed.
- Filed by the 2026-09-13 security review (`docs/security-review-2026-09-13.md`).
