# Task board

One place to record work that is not finished yet, so that a person and any number
of models can each pick up a batch without waiting for one another and without two
of them editing the same files at the same time.

- [`BOARD.md`](BOARD.md) — the generated overview: everything unfinished, grouped by
  what can be started right now, what someone is already on, and what is waiting.
- [`open/`](open) — one file per unfinished task: why it exists, the definition of
  done, the sub-tasks, how to verify it, and notes for whoever picks it up next.
- [`done/`](done) — the same files after they are finished, kept as the record of
  what was decided and why.

Everything is driven by `tools/tasks.mjs`:

```bash
npm run tasks              # the command list
npm run tasks -- list      # every unfinished task
npm run tasks -- next      # the best task nobody else is on
```

## The five rules that keep two agents out of each other's way

1. **One task is one file.** Only ever write the file of the task you own. Two
   agents on two tasks never touch the same file, so their branches never conflict.
2. **`BOARD.md` is generated, never edited.** Every command that changes a task
   rewrites it. If it ever conflicts in a merge, do not resolve it by hand — run
   `npm run tasks:board` and stage the result.
3. **`scope:` is a claim on files, not a hint.** It lists every path the task is
   allowed to change. `claim` refuses a task whose scope overlaps work already in
   progress, and `next` never offers one. Keep scopes narrow: a task scoped to
   `apps/web` blocks every other web task.
4. **Claim before you work, with a name.** `--owner` is you: `claude-opus-5`,
   `codex`, `pei`. A claim older than 24 hours is stale and anyone may take it over,
   so a crashed agent cannot hold the queue.
5. **Finish or hand back.** `done` when it is done, `release` when you stop. A task
   left in progress with nothing happening is the one thing this board cannot see.

## The loop an agent follows

```bash
npm run tasks -- next --area web                     # pick something free
npm run tasks -- claim 2026-09-05-alert-empty-state \
  --owner claude-opus-5 --branch claude/alert-empty-state
# do the work; tick the checklist and add findings in the task file as you go
npm run tasks -- status 2026-09-05-alert-empty-state review   # pull request is open
npm run tasks -- done 2026-09-05-alert-empty-state            # merged
```

Commit the task file with the work it describes. The task file is the handover: if
you stop halfway, the next model reads your notes instead of starting again.

## Filing a task

```bash
npm run tasks -- new \
  --title "Alert list has no empty state" \
  --area web \
  --scope apps/web/components/alerts,apps/web/messages \
  --priority P1 \
  --depends-on 2026-09-04-alert-api-shape
```

That writes `tasks/open/<date>-<slug>.md` with the sections to fill in, and
regenerates the board. Ids are dated and slugged rather than numbered, so two agents
filing on the same day cannot collide the way sequential numbers do; a repeated slug
gets a `-2` suffix automatically. A title with no ASCII words needs `--slug`.

## Task file fields

| Field | Meaning |
| --- | --- |
| `id` | `YYYY-MM-DD-slug`, identical to the file name |
| `title` | One line, what someone else would call this task |
| `status` | `open`, `in-progress`, `blocked`, `review`, `done` |
| `priority` | `P0` outage, `P1` next, `P2` normal, `P3` someday |
| `area` | `api`, `web`, `ops`, `tools`, `docs`, `meta` |
| `owner` | Who holds it now; empty only while `open` |
| `claimed_at` | UTC stamp of the claim; stale after 24 hours |
| `created_at` | UTC stamp, set once |
| `completed_at` | UTC stamp, set only on `done` |
| `branch` | The branch carrying the work, when there is one |
| `depends_on` | Task ids that must be `done` first |
| `scope` | Every repository-relative path this task may change |

Statuses in words: `open` is unowned and free; `in-progress` is owned and holds its
scope; `blocked` is waiting on something outside the task, with the reason written in
the file's notes; `review` is owned, holds its scope, and is waiting on a pull
request; `done` lives in `done/`.

## Checks

`npm run check:tasks` runs in CI and fails on a task file that would mislead the next
reader: an unknown field, a status that does not match the folder, an owner without a
claim time, an empty scope, a dependency that does not exist or that loops, or a board
that no longer matches the task files. It also prints warnings — a stale claim, or two
active tasks whose scopes overlap — without failing the build.
