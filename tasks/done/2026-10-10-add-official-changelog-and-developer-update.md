---
id: 2026-10-10-add-official-changelog-and-developer-update
title: Add official changelog and developer-update feeds to the hourly news sources
status: done
priority: P2
area: api
owner: claude-opus-5-5-official-accounts
claimed_at: 2026-10-10T08:18:58Z
created_at: 2026-10-10T07:35:13Z
completed_at: 2026-10-10T08:56:02Z
branch: claude/official-update-sources
depends_on:
  - 2026-10-10-record-the-official-x-accounts-of
scope:
  - apps/api/app/news_automation/sources.json
  - apps/api/app/news_automation/feeds.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_news_sources_cli.py
  - docs/news-automation.md
  - docs/official-ai-accounts.md
---

# Add official changelog and developer-update feeds to the hourly news sources

## Why

The owner wants the site to learn of official updates and tutorials as the companies post
them (2026-10-10). X stays out (see `docs/official-ai-accounts.md`), so the same items have
to arrive through the companies' own pages, and several of those are missing or broken in
`apps/api/app/news_automation/sources.json`:

- **"Claude blog" reads nothing by its own config.** `claude.com/blog` redirects to
  `claude.com/resources/articles`, article paths are now `/resources/articles/<slug>`
  (old `/blog/<slug>` links redirect there), and the row's `include_path_prefixes` is
  still `["/blog/"]`. Checked 2026-10-10 with curl: the listing carries no `/blog/` link.
- **Developer posts moved to `claude.dev`**, which is not a source. It advertises
  `https://claude.dev/rss.xml` and its robots.txt allows everything.
- **No changelog-type source** other than "Claude Platform release notes": nothing for
  Claude Code, GitHub Copilot or Cursor.

## Definition of done

- [x] "Claude blog" reads the articles the site lists today, under the same name.
- [x] Each row is tested through the scanner's own parsers and added only if it passes;
      the result of each test is in the row's `note` and in the notes here.
- [x] `docs/official-ai-accounts.md` names the new sources in its scanner-status column
      and records the ones that could not be read, with the reason.
- [x] `docs/news-automation.md` states the shared-host rule and what
      `max_entries_per_scan` means.

Loading the file on the host is its own task,
`2026-10-10-load-the-changelog-and-developer-news`: it needs the owner's go-ahead and a
deploy, and this one would otherwise stay open and hold the next task back.

## Steps

- [x] A throwaway script outside the repository, run with `uv run python` from
      `apps/api`: `sources_cli.load_file`, `validate_source_configuration`, then one
      `SafeNewsFetcher` for the listing, `parse_entries`, and `read_article` on two entries.
- [x] Fix "Claude blog".
- [x] Test and add the seven new sources.
- [x] Update the pinned Claude blog test to the live markup; one pinned test per new
      config shape.
- [x] Two file invariants in `apps/api/tests/test_news_sources_cli.py`.
- [x] Update the two documents; bump `reviewed_on`.
- [x] File the follow-ups.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests
cd apps/api && uv run pytest tests/test_news_sources_cli.py tests/test_news_automation.py -q
npm run check:tasks
```

## Notes

- What the scanner's own code read on 2026-10-10 (development machine, not the host):

  | Source | Listing | Entries | Two entries read |
  | --- | --- | --- | --- |
  | Claude blog (`/resources/product-announcements`) | 200, html | 7, undated | 4,723 and 6,799 characters |
  | Claude developer blog | 200, rss | 15 dated, 1 within 72 h | 15,378 and 26,205 characters |
  | Claude Code changelog | 200, rss | 15 dated, 5 within 72 h | summaries of 186 to 5,715 characters, 15 distinct anchors |
  | Anthropic engineering | 200, html | 25, undated | 27,882 and 10,497 characters |
  | GitHub Changelog | 200, rss | 5 of 10 named Copilot, all within 72 h | 2,534 and 3,088 characters |
  | Cursor changelog | 200, rss | 50 dated, none within 72 h | 2,545 and 6,955 characters |
  | Ollama blog | 200, rss | 59 dated, none within 72 h | 4,155 and 4,886 characters |
  | OpenRouter announcements | 200, html | 13, undated, the category link dropped | 12,484 characters (one entry read) |

- Three things the probe changed from the plan:
  - **Claude blog reads `/resources/product-announcements`, not `/resources/articles`.**
    Both listings show about seven cards. On that day the three product posts on
    `/resources/articles` were all on the announcements page too, and the other three
    cards there were customer stories.
  - **The Claude Code changelog needed a parser change.** Its feed has no `<description>`:
    the text is in `<content:encoded>`, which `parse_xml_feed` did not read, so every
    summary was empty and the source could not validate. `feeds.py` now reads it when the
    usual elements gave nothing; an item with both keeps its description, so no feed that
    already produced a summary changes. `feeds.py` was added to this task's scope for it.
  - **The Claude developer blog needed `article_ids: ["body"]`.** Its pages have no
    `<article>` or `<main>`; with the default tags the feed validated (the summary was
    enough) while every page read as empty.
- Anthropic engineering has had no post since May 2026; developer posts go to claude.dev.
  It is kept for the occasional long piece, with the cap at 50 so that all 25 listed posts
  are recorded as seen (see the row's note).
- Cloudflare in front of `claude.com`, `claude.dev`, `code.claude.com` and
  `www.anthropic.com` answered 403, robots.txt included, after a handful of requests from
  the same machine within a few minutes, and the fetcher reads that as "robots.txt did
  not permit". Each host passed when probed alone a few minutes later. Probe these hosts
  one at a time.
- Rules read from the code:
  - Several rows may share a host (`blog.google` already had two), but `by_host`
    (`scanner.py`, `validation.py`) keeps one of them per host, so rows sharing a host
    must agree on `role`, `is_first_party` and the page-reading keys, and a row with
    `evidence_from_feed_summary` must be alone on its host. The new test checks the file.
  - `max_entries_per_scan` is "the top N of the listing", sliced before the seen and stale
    checks; it is not "N new entries per scan".
  - A candidate the writer declines costs two model calls (the duplicate check and the
    writer), not a whole pipeline run.
  - The candidate's title is the page's own `<title>` when the page is read; the listing's
    link text is only the fallback, so the long card text of claude.com does not show.
- Not added, and why (each is in `docs/official-ai-accounts.md`):
  - One long page with no per-entry address: the Claude apps release notes, the OpenAI
    API changelog, the ChatGPT and Codex changelog, the Gemini API changelog, the Gemini
    app release notes. Task `2026-10-10-read-each-dated-section-of-a`.
  - VS Code feed: lists the next version as "(Insiders)" with a future date. Task
    `2026-10-10-let-a-news-source-leave-entries`.
  - Google Developers blog: robots.txt answers with a redirect. Task
    `2026-10-10-decide-whether-the-news-fetcher-follows`.
  - GitHub `releases.atom`: disallowed by GitHub's robots.txt.
  - DeepSeek: no listing, and its robots.txt answers with an HTML page.
  The last four were probed with curl by a planning agent, not through the scanner.
