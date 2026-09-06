# Working in this repository

## Unfinished work lives in `tasks/`

Anything known but not yet done is a file in [`tasks/open/`](tasks/open), and
[`tasks/BOARD.md`](tasks/BOARD.md) lists all of it at once. That board is the shared
queue: several models and people work from it at the same time, so take work from it
rather than inventing your own, and put anything you notice but do not fix back into
it instead of leaving it in a chat log.

```bash
npm run tasks -- next                                  # a task nobody else is on
npm run tasks -- claim <id> --owner <your-model-name>  # take it
npm run tasks -- done <id>                             # finish it
npm run tasks -- new --title "..." --area web --scope apps/web/components/alerts
```

[`tasks/README.md`](tasks/README.md) has the full protocol. The parts that matter for
staying out of another agent's way:

- Claim a task before you touch its files, and use a name that identifies you.
- A task's `scope` lists every path it may change. Stay inside it, keep it narrow,
  and never claim a task whose scope is already active — the tool will refuse.
- Never hand-edit or hand-merge `tasks/BOARD.md`; run `npm run tasks:board`.
- Leave the task file better than you found it: tick the checklist, write down what
  you learned, and `release` it if you stop, so the next model can continue.

## Checks before you push

CI runs these; run the ones your change touches first.

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npm run test:tools && npm run check:tasks
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
```

## Where things are

`apps/web` is the Next.js frontend and its same-origin BFF, `apps/api` is the FastAPI
service, worker and migrations, `ops/` is deployment, `tools/` is repository tooling,
and `docs/` holds the long-form specifications. `architecture.md` describes the
boundaries; `README.md` describes the product.
