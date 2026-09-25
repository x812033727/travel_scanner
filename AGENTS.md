# Working in this repository

## Unfinished work lives in `tasks/`

Anything known but not yet done is a file in [`tasks/open/`](tasks/open), and
`npm run tasks -- list` shows all of it at once. That list is the shared queue: several
models and people work from it at the same time, so take work from it rather than
inventing your own, and put anything you notice but do not fix back into it instead of
leaving it in a chat log.

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
- `tasks/BOARD.md` is generated and git ignores it. Read it with `npm run tasks -- list`,
  or write the file with `npm run tasks:board` — never commit it, and never edit it by
  hand. It used to be committed, and then every pull request that filed a task collided
  with every other one in the same table rows.
- Leave the task file better than you found it: tick the checklist, write down what
  you learned, and `release` it if you stop, so the next model can continue.

## Checks before you push

CI runs these; run the ones your change touches first.

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npm run test:tools && npm run check:tasks
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest
```

## Releases on the production host

The host has a one-shot deploy script and staged release drivers that cannot see each
other, and a container rebuild between two phases of a staged release breaks it. Before
writing or running any multi-phase release on the host (`prepare` -> `activate` ->
content phases), read [`ops/release/README.md`](ops/release/README.md): the driver owns
`/root/travel-scanner-deploy.hold` from `prepare` until its last phase succeeds, through
`ops/release/hold.py`, and leaves it in place on failure.

## Where things are

`apps/web` is the Next.js frontend and its same-origin BFF, `apps/api` is the FastAPI
service, worker and migrations, `ops/` is deployment, `tools/` is repository tooling,
and `docs/` holds the long-form specifications. `architecture.md` describes the
boundaries; `README.md` describes the product. `.agents/skills/` holds the skills Codex and
Claude Code share (Claude reads the byte-identical copy under `.claude/skills/`, and
`npm run test:tools` keeps the two in step); start any article batch with the
`content-pipeline` skill, a production deploy with `deploy`, and board work with
`task-board`. The others: `article-localization` (translating published articles),
`catalog-import` (host data CLIs), `catchtable-discovery`, `hotspot-review` (review
queues, Place IDs, coordinates), `prod-host-ops` (nginx, admin settings, host CLIs),
`backend-conventions` (migrations, session helpers, admin pages), `dev-and-ci` (local
checks, CI failures, Dependabot), `web-i18n-e2e` (messages and Playwright) and
`youtube-video`. Read the matching skill before re-deriving a workflow from the docs.
