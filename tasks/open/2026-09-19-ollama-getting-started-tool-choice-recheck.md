---
id: 2026-09-19-ollama-getting-started-tool-choice-recheck
title: ollama-getting-started says tool_choice is unsupported but the Ollama OpenAI-compatibility page now lists it
status: review
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

- [x] Re-read the OpenAI-compatibility page with `curl -sL -A "Mokaair-editorial"` and record the verbatim line for `tool_choice`.
- [x] Update the `tool_choice` sentence (and its source `checked_on`) in `ollama-getting-started` in every locale it appears in, or record why the page's list does not apply.
- [x] `pack_cli lint --kind life` stays at 0 errors; `npm run check:tasks` green.

## Steps

- [x] Fetch the page once with the editorial User-Agent (the only network call), keep the HTML in
      the scratch directory, and read the `tool_choice` line together with the page's checkbox
      markup, so the state of the box is read and not just the presence of the field.
- [x] Check every claim in the sentence against the page: streaming, JSON mode, vision and tools
      ticked; `tool_choice` unticked; `/v1/models` and `/v1/embeddings` present; `/v1/responses`
      with "Note: Added in Ollama v0.13.3".
- [x] Move the source's `checked_on` to 2026-09-19 through `json.load`/`json.dump`
      (`ensure_ascii=False`, `indent=2`, trailing newline), after confirming that a no-op round
      trip of the file is byte-identical; the diff is that one line.
- [x] `pack_cli lint --kind life --slug ollama-getting-started`: 0 errors (one pre-existing
      `no_summary` warning); `pytest tests/test_guides_content_pack.py`: 9 passed, 5 skipped.

## How to verify

```bash
curl -sL -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)" \
  https://docs.ollama.com/api/openai-compatibility \
  | grep -o '<li class="task-list-item"><input[^>]*/> <code>tool_choice</code></li>'
# expected: <input type="checkbox" disabled=""/> with no checked="" -- an unsupported field
git diff --stat -- apps/api/app/guides/content/ollama-getting-started.json   # one line
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --slug ollama-getting-started
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
```

On the host, after the merge (the shipped article has to pick up the new `checked_on`):

```bash
python -m app.cli guides-import --actor-email <admin> --slug ollama-getting-started --dry-run
python -m app.cli guides-import --actor-email <admin> --slug ollama-getting-started --publish
```

## Notes

### 2026-09-19 done in repo (claude-fable-5-1)

- The claim needed `--force`: the JSON is still held by `2026-09-16-retitled-guides-stale-link-text`,
  which sits in `review` under the same owner although its pull request has merged and deployed.
- Verbatim, under `/v1/chat/completions` -> "Supported request fields" (fetched 2026-09-19):
  `<li class="task-list-item"><input type="checkbox" disabled=""/> <code>tool_choice</code></li>`
- The page's lists are checklists: a supported field is `<input type="checkbox" disabled=""
  checked=""/>` (62 on the page) and an unsupported one has no `checked` (19: `Logprobs`, `Image
  URL`, `tool_choice`, `logit_bias`, `user`, `n` under chat completions, and the like under
  `/v1/completions`). `tool_choice` is in the second group, so the page still says it is not
  supported; the series checker read the field's presence in the list as support. The article's
  sentence ("不支援 tool_choice") therefore stands in its one locale (zh-TW), and the text is
  unchanged.
- Only the source's `checked_on` moved (2026-09-14 -> 2026-09-19), since the whole sentence was
  re-verified against the page on that date. Everything else in the file is byte-for-byte as before.
- The article does not say `tool_choice` is unsupported on `/v1/responses`; the page lists no
  field table for that endpoint, so there was nothing further to reconcile.
