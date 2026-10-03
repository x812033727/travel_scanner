---
id: 2026-10-03-news-batch-4-11-claude-code
title: News batch 4.11: Claude Code mods explainer, five languages
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1-news-4-11
claimed_at: 2026-10-03T18:17:06Z
created_at: 2026-10-03T18:04:10Z
completed_at:
branch: claude/admiring-goodall-jpzg46
depends_on: []
scope:
  - docs/news-2026-batch-4/agents/DELTA-4-11.md
  - docs/news-2026-batch-4/check_article.py
  - docs/news-2026-batch-4/build_assets.py
  - docs/news-2026-batch-4/update_index.py
  - docs/news-2026-batch-4/HANDOVER.md
  - docs/news-2026-batch-4/translation-corrections.json
  - docs/news-2026-batch-4/factcheck-draft
  - docs/ai-news-2026-09-late/research
  - docs/ai-news-2026-09-late/manifest.json
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - apps/api/app/guides/content/ai-news-claude-code-mods-20261001.json
  - apps/web/public/guides/ai-news-claude-code-mods-20261001
  - apps/web/public/guides/ai-news-2026-january-september-index
---

# News batch 4.11: Claude Code mods explainer, five languages

## Why

Anthropic published "Customize Claude Code with mods in TypeScript" on `claude.com/blog` on
2026-10-01: mods are TypeScript or JavaScript functions shipped inside a plugin that run inside
Claude Code's own process and can rewrite prompts, guard tool calls, approve or deny
permissions, draw panes and buttons, and replace built-in features such as `/diff`. The hourly
news automation does not read `claude.com/blog`, and as of 2026-10-03 the site has no article
about Claude Code plugins, marketplaces or mods. The owner asked for one article that answers
four questions: what mods are, what they can do, where they are used, and how to start.

The plan is `docs/news-2026-batch-4/agents/DELTA-4-11.md`: sources (Anthropic's blog and the
four mods documentation pages only), the five sections, the comparison table, the 2x2 diagram,
the FAQ candidates, sixteen facts that are easy to get wrong (the two meanings of "hook", mods
are not sandboxed, where `sec-default` loads, where mods draw and where they only run), and the
two closing links. `check_article.py` already carries the slug at `display_order` 192.

## Definition of done

- [ ] `ai-news-claude-code-mods-20261001` in five locales, researched from Anthropic's own pages
      only, two fact-check rounds by different agents, translated and reviewed per language,
      with a hero and a 2x2 diagram.
- [ ] AI index links to it in five locales; index title unchanged (see DELTA-4-11 §6).
- [ ] PR merged; deploy and `guides-import --slug` publish done by someone with host access.

## Steps

- [x] DELTA-4-11.md and the `RELATED` entry (coordinator, 2026-10-03)
- [ ] Research record (opus): `docs/ai-news-2026-09-late/research/ai-news-claude-code-mods-20261001.json`,
      re-read every page on the day, confirm the GitHub directories exist before citing them
- [ ] zh-TW draft (sonnet) following DELTA-4-11 §3 and §4
- [ ] Fact check round 1 and round 2 (opus, different agents), reports in `factcheck-draft/`
- [ ] Translate en/ja/ko/zh-CN (sonnet), per-language review
- [ ] Assets, index (`update_index.py ai --dry-run` first), `check_article.py --full --assets`, lint, pytest
- [ ] PR
- [ ] File the follow-ups from DELTA-4-11 §7 (tutorial lesson "build your first mod", automation
      source for `claude.com/blog`, AI index title month range)

## How to verify

`cd apps/api && uv run python ../../docs/news-2026-batch-4/check_article.py ai-news-claude-code-mods-20261001 --full --assets`
prints `OK`; `uv run python -m app.guides.pack_cli lint --kind life` has no errors; after publish,
`verify_public.py --slug ai-news-claude-code-mods-20261001 --kind life --locale zh-TW`.

## Notes

- 2026-10-03 (coordinator): read the blog post and the `overview`, `create`, `reference` and `admin`
  documentation pages with `curl -sSL` and the editorial User-Agent; all HTTP 200 with body. The
  documentation says "as of v2.1.287" on every page, so treat the built-in mods table, the limits
  table and the settings table as live data (`live_data_warnings`).
- Third-party posts found while searching (smartscope, aitmpl, digitalapplied, neurycode, 4sapi)
  still teach `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`; the documentation says the variable is now
  ignored. They are leads only, never sources (DELTA-4-11 §2).
- No five-locale article about plugins or hooks exists to link to, so the second closing link is
  `ai-news-claude-sonnet-55-20260928`; the zh-TW tutorials `claude-code-plugins-guide` and
  `claude-code-hooks-getting-started` can be wired by `pack_cli autolink` in zh-TW only.
