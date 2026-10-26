# Independent DuckDB episode collision inventory

Proposed slug: `duckdb-agent-full-export`. Proposed title: 表格只顯示40列？用DuckDB 2.0交出完整跟進清單.

No exact same-episode collision was observed on the inspected surfaces. Safe proposed content scope: `docs/videos/duckdb-agent-full-export` only. This is a timestamped inventory, not a future lock or a backend uniqueness claim.

Observation window: 2026-10-25T23:06:12.606324+00:00 through 2026-10-25T23:08:22.719907+00:00. Assessment: 2026-10-25T23:09:47.173877+00:00.

## Coverage and actual outcomes

- Read `AGENTS.md`, `.agents/skills/task-board/SKILL.md`, and `.agents/skills/task-board/references/collisions.md`; hashes retained in JSON.
- `git worktree list --porcelain`: exit 0; four worktrees. `git branch --list -vv` / `git for-each-ref`: exit 0; five local branches, including the un-checked-out `work` branch.
- All four worktrees: recorded full `git status --short`, targeted task status, every open/done Markdown task path, frontmatter, SHA-256, primary search matches, all video directory names, and text topic searches. Committed trees for all five local branches include task paths, video directory inventory and content matches.
- Normal `git ls-remote --heads origin`: exit 0; all 231 actual head/SHA lines retained. No head name matches DuckDB, proposed slug, agent-mode, full-export or follow-up CSV topic.
- Normal `gh pr list --state open --limit 1000 --json number,title,headRefName,baseRefName,url,body,headRefOid,updatedAt`: exit 0; 30 open PRs. All bodies retained. No DuckDB, proposed slug, agent-mode or full-export episode match.
- Searches cover DuckDB, agent mode/代理模式, full export, complete lists/exports, follow-up/跟進, 40-row phrasing, CSV, spreadsheet/Excel, PDF, table and slides context. Exact DuckDB/proposed-slug/跟進清單 matches: zero in all four worktree task/content inventories and successful origin/main search.

| Worktree | Branch | Open task Markdown | Done task Markdown |
| --- | --- | ---: | ---: |
| `/workspace/travel_scanner` | `refs/heads/codex/ai-tech-dns-20261025` | 547 | 1635 |
| `/workspace/work/travel-scanner-formal-255` | `refs/heads/codex/ai-tech-formal-20261025` | 550 | 1635 |
| `/workspace/work/travel-scanner-forty` | `refs/heads/codex/ai-tech-forty-20261025` | 549 | 1635 |
| `/workspace/work/travel-scanner-slides` | `refs/heads/codex/ai-tech-slides-20261025` | 548 | 1635 |

Task Markdown counts exclude `.gitkeep` and seven historical `.before-closeout.txt` attachments, which are still included in complete branch-tree path inventories. One formal-255 task is untracked (`2026-10-25-local-first-build-without-branding.md`); slides has a modified task. Both are captured and do not concern DuckDB.

## Near matches and scope distinctions

| Observed work | Evidence | Distinction |
| --- | --- | --- |
| Active PDF/slides episode | PR #1857, `codex/ai-tech-slides-20261025`, worktree `travel-scanner-slides`, `docs/videos/ai-slides-outline-review`; local title “AI簡報先審大綱：公開PDF變成4頁有來源的成品” | A public report becomes four cited PDF/PPTX/SVG/PNG slides with outline review. It does not cover DuckDB, capped table previews, complete follow-up CSV or export validation. Keep its files separate. |
| Active formal verification episode | PR #1856, `docs/videos/claude-formal-verification-255` | Two C programs, 256-input checks, finite control/proof boundaries; unrelated data workflow. |
| Active ForTy data episode | PR #1851, `docs/videos/forty-forest-map` | Taiwan forest-map pixels, six class scores, 2020 source-data limits; “forty” is the product name, not a 40-row table cap. |
| Existing full-candidate comparison | `docs/videos/ai-term-embedding/README.md:45–49`; main history #1211 | Six hand-authored toy activity vectors, comparing first two versus all six candidates; no model embedding test, DuckDB engine, export or follow-up CSV. Related completeness lesson but distinct operation and artifact. |
| Existing citation lesson | `docs/videos/ai-citation-check/brief.md` | Open a URL, check whether quoted claim is supported, amend an invented wrong answer; no tabular export. |
| Existing jobs-chart data episode | `docs/videos/ai-real-jobs-chart/brief.md`; main history #867/#968 | Interpret Remote Labor Index percentages and a job task checklist, using original chart cards; not an export tutorial. |
| Existing general AI-agent episodes | `ai-agents-explained-what-they-cost`, `always-on-agent-explained`, `ai-agent-vs-chatbot`, `openai-agents-broke-in` | Broad agent behavior/cost/security themes. No exact DuckDB/full-export topic evidence found. |
| Other CSV/PDF hits | English course catalogs, `dots-lesson-*` shot lists, drama production/schedule CSVs, unrelated report citations | Supporting production artifacts rather than this proposed DuckDB teaching episode. |

No active task scope is an ancestor, descendant or exact match for `docs/videos/duckdb-agent-full-export`. The broad `docs/videos` scope belongs only to the historic done ticket `2026-09-27-video-binge-docs`. Active formal, ForTy and slides tickets all include `docs/videos/lexicon.json`; the new episode should not add that shared file to its scope without coordination.

## Main, DNS base and history

- Remote `refs/heads/main` and local `origin/main` both resolved to `76cc8aa1a3385f4176af3d7e588025d3ef6c8e15` in this capture.
- There is no local `main` ref. Explicit `rev-parse`, `show` and scope/history `log main` commands returned exit 128; those failures are recorded rather than treated as an empty history.
- Authorized DNS base `6354ed3` resolves to `6354ed3ebcc82c1baefe57bcd1f8d436f183581a`, dated 2026-10-25T16:55:43Z, subject “docs(video): deliver checked eight-language DNS media and record pending formal binding”. Its 13-path commit stat concerns DNS language/delivery evidence and follow-up tasks, not DuckDB.
- `git log origin/main -- docs/videos/duckdb-agent-full-export` and `git log 6354ed3 -- docs/videos/duckdb-agent-full-export`: both exit 0, zero commits. `git ls-tree origin/main` for the proposed directory: exit 0, zero files.
- Successful `git grep` on origin/main for DuckDB/proposed slug/跟進清單 returned exit 1 (no matches), with empty stderr.
- Both ancestry directions between `6354ed3` and `origin/main` returned exit 1. Their merge base is `c29462d3424e245ea0e7da72545f62c5432b8736`. They have diverged; the authorized DNS base must not be described as current main. Parent handles scoped compatibility and isolated-worktree/base decisions.

## Limits and handoff

The remote-head check inventories names and SHAs; it does not inspect arbitrary un-fetched remote branch trees. The parent handles normal VideoTool backend dedupe. These observations can age while other sessions work, so repeat local/remote/PR checks before opening the eventual PR.

This subtask did not fetch, checkout, create/claim/register anything, mutate repository/worktrees/tasks, commit, open PRs, call the backend/browser or run paid/media work. Its only writes are the two requested scratch evidence files.

Full actual commands, UTC times, exit codes, stdout/stderr, task inventories, PR bodies and analysis: `fifth-collision-independent.json`.
