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
npm run test:tools && npm run test:docs-videos && npm run check:tasks   # docs-videos needs ffmpeg
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest
```

## Releases on the production host

The host has a one-shot deploy script and staged release drivers that cannot see each
other, and a container rebuild between two phases of a staged release breaks it. Before
writing or running any multi-phase release on the host (`prepare` -> `activate` ->
content phases), read [`ops/release/README.md`](ops/release/README.md): the driver owns
`/root/travel-scanner-deploy.hold` from `prepare` until its last phase succeeds, through
`ops/release/hold.py`, and leaves it in place on failure.

## Video rules, scripts & backups live on Google Drive (Route B SSOT, 2026-11-25)

**Google Drive is the single authoritative source of truth (SSOT)** for all video rules, lessons,
locked character sheets, pronunciation lexicons, topic pools, drafts, finalized episode scripts
(`video.json`, `script.md`, `brief.md`, `i18n/*.json`, `review/`), and production media.
**Never commit new episode scripts, topic pools, business rules, or binary media assets to GitHub**
(`0 GitHub commits`; enforced by `tools/video-drive-boundary.test.mjs`). Do not push `transfer/*`
or `claude/backup-*` branches (`tobranch.sh` refuses).

Before starting any video, explainer (`sothatswhy-*`, `curio-*`), or Shorts episode, pull the
latest authoritative rules from Google Drive into gitignored `.cache/video-drive/rules/`:

```bash
npm run vdrive -- pull-rules explainer   # 原來如此事務所 + 奇聞檔案局 + 通用
npm run vdrive -- pull-rules sothatswhy  # 原來如此事務所 + 共用
npm run vdrive -- pull-rules curio       # 奇聞檔案局 + 共用
npm run vdrive -- pull-rules shorts      # 零台詞 Shorts 短劇 + 通用
npm run vdrive -- status                 # check detected backend (G:\, rclone, or gdrive CLI)
```

| What you need | Exact Google Drive location (`AI/備份/AI劇/` / Windows `G:\我的雲端硬碟\AI\備份\AI劇\` / rclone `videobackup:AI劇/`) |
| --- | --- |
| **Universal entry map (works with or without GitHub)** | `AI/備份/AI劇/_START-HERE.md` |
| **Authoritative rules, checklists, lessons & canon sheets** | `AI/備份/AI劇/_規則/` (`解說系列共用/FLOW-PRODUCTION-RULES.md`, `奇聞檔案局/CURIO-FLOW-CHECKLIST.md`, `原來如此事務所/`, `通用/lexicon.json`, `短劇與漫劇/`). Outside legacy `rules-sync` ownership so it is never overwritten. |
| **Update a rule (owner-approved, optimistic lock)** | `npm run vdrive -- push-rule <localFile> --target <relUnderRules> --note "<reason>"` — checks remote SHA-256, archives previous copy to `_規則/_history/`, and appends `_規則/CHANGELOG.md`. |
| **Shared assets, music libraries, outros & pools** | `<系列>/_共用/製作檔/` & `<系列>/_總表/` (exact IDs in `_START-HERE.md`). |
| **Local workdir & finalized episode delivery (0 GitHub commits)** | Draft locally under gitignored `work/video-episodes/<slug>/`, lint with `node tools/video/cli.mjs lint --file <path>`, upload finalized `腳本定稿/` + production files with `npm run vdrive -- push-episode --series <sothatswhy|curio|shorts> --path "<分類>/<代碼>/製作檔/<slug>" --from <dir>` (SHA-256 0-diff), then publish via `node tools/video/cli.mjs import --from <import_pkg>`. |

Legacy files still under `docs/videos/` are frozen for migration to Google Drive
(`tasks/open/2026-11-25-slim-docs-videos-pools-and-plans.md`); always treat Drive `_規則/` as
authoritative over any stale copy in `docs/videos/`.

## Multi-agent workspaces on Google Drive (`Claude`, `Codex`, `Gemini`)

Never place a live `.git` worktree, `node_modules` or `.venv` directly on a mounted Google Drive
folder (`G:\我的雲端硬碟` or `rclone mount`): `.git/index.lock` races, symlink limitations and
100k-file rate limits corrupt the checkout. Instead, keep active checkouts on local/VPS disk and
hand off uncommitted work across Claude Code, Codex and Gemini (`agy` / Antigravity) through a
hash-verified Google Drive workspace capsule (`tools/workspace-sync.mjs`, `npm run ws`), stored under
`AI/工作區/<id>/` (or `videobackup:工作區/<id>/`):

```bash
npm run ws -- status                                          # branch, base SHA, tracked/untracked & Drive target
npm run ws -- push [id] --note "Ready for cross-model review" # pack wip.patch + untracked/ + HANDOFF.md to Drive
npm run ws -- pull <id>                                       # verify SHA-256, checkout branch, apply patch & files
npm run ws -- list                                            # list capsules on Drive
npm run ws -- delegate --to <claude|codex|gemini> --slot a --prompt "..."  # cross-agent call via host account pool
```

`AGENTS.md`, `CLAUDE.md` and `GEMINI.md` at the repository root are byte-identical (`npm run test:tools`
enforces parity) so all three agent harnesses load the same rules on startup.

## Where things are

`apps/web` is the Next.js frontend and its same-origin BFF, `apps/api` is the FastAPI
service, worker and migrations, `ops/` is deployment, `tools/` is repository tooling,
and `docs/` holds technical specifications. `architecture.md` describes the
boundaries; `README.md` describes the product. `.agents/skills/` holds the skills Codex and
Claude Code share (Claude reads the byte-identical copy under `.claude/skills/`, and
`npm run test:tools` keeps the two in step); start any article batch with the
`content-pipeline` skill, a production deploy with `deploy`, and board work with
`task-board`. The others: `article-localization` (translating published articles),
`catalog-import` (host data CLIs), `catchtable-discovery`, `hotspot-review` (review
queues, Place IDs, coordinates), `prod-host-ops` (nginx, admin settings, host CLIs),
`backend-conventions` (migrations, session helpers, admin pages), `dev-and-ci` (local
checks, CI failures, Dependabot), `web-i18n-e2e` (messages and Playwright),
`youtube-video` (video tooling CLI and publishing flow), `curio-episode` (奇聞檔案局 `curio-*`
and 原來如此事務所 `sothatswhy-*` both follow the Google Drive SSOT rules pulled via
`npm run vdrive -- pull-rules explainer` → `_START-HERE.md` + `_規則/解說系列共用/FLOW-PRODUCTION-RULES.md`
+ `_規則/奇聞檔案局/CURIO-FLOW-CHECKLIST.md`, with 0 GitHub commits per episode),
`brand-story`, `minimax-h3-runpod`, `animation-preproduction`, `animation-camera`, and
`animation-production`. Read the matching skill and pull the latest Drive `_規則/` before
starting any video production.
