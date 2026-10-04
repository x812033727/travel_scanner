---
id: 2026-10-03-claude-code-lesson-first-mod
title: Claude Code tutorial lesson: build your first mod
status: done
priority: P3
area: docs
owner: claude-fable-5-1-first-mod
claimed_at: 2026-10-03T23:46:52Z
created_at: 2026-10-03T19:27:30Z
completed_at: 2026-10-04T02:16:42Z
branch: claude/first-mod-lesson
depends_on: []
scope:
  - docs/claude-code-series/lessons
  - apps/api/app/guides/content/claude-code-first-mod.json
  - apps/web/public/guides/claude-code-first-mod
---

# Claude Code tutorial lesson: build your first mod

## Why

The news article `ai-news-claude-code-mods-20261001` explains what Claude Code mods are and where to start, but does not teach writing one. The Claude Code tutorial series (zh-TW, `docs/claude-code-series`) has lessons on plugins and settings hooks and none on mods.

## Definition of done

- [x] One zh-TW lesson that builds the documentation's `first-mod` (tool-call counter beside the spinner, `/tally` command, `claude plugin validate`, `claude plugin test`), placed after `claude-code-plugins-guide` and `claude-code-plugin-team-distribution`, with the series' starter materials.

## Steps

- [x] Read https://code.claude.com/docs/en/plugins/mods/create on the day; every command and file verbatim.
- [x] Write the lesson spec in `docs/claude-code-series/lessons/`, then the pack and starter zip the way the other advanced lessons do.
- [x] Link it from the tutorial hub (series manifest, path advanced-skills, hub count). Not done: an inline link from the news article's zh-TW body, which lives in PR 1187 and would need that pack republished; file it with the index month-range follow-up if wanted.

## How to verify

`pack_cli ingest --dry-run`, `intake_check.py`, `pack_cli lint --kind life`.

## Notes

- Done 2026-10-04 (Taipei): lesson 97 `claude-code-first-mod`, number 97, group L, path advanced-skills, display_order 197.
  The mod's four files (`tools/claude-code-series/advanced/mods/first-mod/`) are the documentation's first-mod tutorial;
  `claude plugin validate` and `claude plugin test` ran on them in this container with Claude Code 2.1.289 (logs in
  `/root/news411/modlab/`, quoted in the lesson). The interactive `--plugin-dir` session, the spinner, `/tally` in a
  conversation, hot reload, `/plugin` and `claude -p` were NOT run: the lesson states them as the documentation's expectation.
- Independent fact check (opus): about 62 claims, 20 edits; report `docs/claude-code-series/advanced/evidence/lesson-97-factcheck.md`.
- Tooling: `generate.py --only 97`, `package-labs.py --only 97` plus a rebuilt `skill-kit.zip` (a full `package-labs.py` run
  rewrites all 36 archives byte-for-byte differently on this Python, so only the two new/affected archives are committed);
  `render-art.mjs` needs Playwright's own browser build, so the cover was rendered through a temporary copy pointed at
  `/opt/pw-browsers/chromium`. `validate.py` is stale against today's packs (it expects topics {ai, tutorial} and no glossary
  inlines) and reports 191 pre-existing errors; not re-committed.
- Checks: `node --test tools/claude-code-series.test.mjs` 12 passed; `pack_cli lint --kind life` no error for the new pack
  (the no_summary warning is series-wide); `pytest tests/test_guide_series.py tests/test_guides_content_pack.py` 40 passed;
  ruff and mypy clean. Three tests and the tool test pinned the lesson count at 96 and now say 97.
- Left: deploy, then `guides-import --slug claude-code-first-mod --slug claude-code-tutorials` dry run and publish on the host
  (the hub pack changed only in its count sentence).

- Filed by batch 4.11 (`docs/news-2026-batch-4/agents/DELTA-4-11.md` §7).
