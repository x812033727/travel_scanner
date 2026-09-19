---
id: 2026-09-19-ollama-getting-started-tool-choice-recheck
title: ollama-getting-started says tool_choice is unsupported but the Ollama OpenAI-compatibility page now lists it
status: in-progress
priority: P3
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:15:05Z
created_at: 2026-09-19T01:09:18Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/guides/content/ollama-getting-started.json
---

# ollama-getting-started says tool_choice is unsupported but the Ollama OpenAI-compatibility page now lists it

## Why

While fact-checking the ai-workflow series on 2026-09-19, the checker for `ai-workflow-local-and-cloud-mix` read https://docs.ollama.com/api/openai-compatibility and found `tool_choice` listed under "Supported request fields". The shipped article `ollama-getting-started` states that Ollama does not support `tool_choice`. The two now disagree; the series article does not mention `tool_choice`, so nothing on the site contradicts itself yet, but the older statement should be re-verified against the current page and corrected if it no longer holds.

## Definition of done

- [ ] Re-read the OpenAI-compatibility page with `curl -sL -A "Mokaair-editorial"` and record the verbatim line for `tool_choice`.
- [ ] Update the `tool_choice` sentence (and its source `checked_on`) in `ollama-getting-started` in every locale it appears in, or record why the page's list does not apply.
- [ ] `pack_cli lint --kind life` stays at 0 errors; `npm run check:tasks` green.

## Steps

- [ ] First sub-task.
- [ ] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.
