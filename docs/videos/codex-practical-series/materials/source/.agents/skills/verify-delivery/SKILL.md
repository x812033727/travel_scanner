---
name: verify-delivery
description: Verify delivery of the local Small Steps task and weekly-report practice project using existing tests, source truth and browser checks. Use for this project's acceptance or final review, not feature implementation or unrelated repositories.
---

# Verify Small Steps delivery

Confirm the current folder has core.mjs, index.html and core.test.mjs. Read README.md and docs/data-contract.md when available; read the requested lesson's acceptance.md.
Run `node --test` in that folder. Preserve original tests and inputs. Do not implement fixes during an acceptance run.
For v2 projects, run `node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11`; independently compare fixtures/truth.json.
In a fresh local browser context, verify same-title IDs, filter/search, reload, literal markup text, focus and 390px/1280px layout. Inspect storage failure only with fictional practice data and leave unrelated keys intact.
Record each result as PASS, FAIL or NOT RUN, with command/observation, path and actual exit code. Distinguish structural JSON validation from matching source truth.
If a file/tool is absent, state the exact missing prerequisite and do not claim a run. Return findings and reproduction steps; repairs require a separate requested task.
