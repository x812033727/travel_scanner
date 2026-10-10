---
id: 2026-10-10-add-official-changelog-and-developer-update
title: Add official changelog and developer-update feeds to the hourly news sources
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-10T07:35:13Z
completed_at:
branch:
depends_on:
  - 2026-10-10-record-the-official-x-accounts-of
scope:
  - apps/api/app/news_automation/sources.json
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

- [ ] "Claude blog" reads the articles the site lists today, under the same name.
- [ ] Each row below is tested through the scanner's own parsers and added only if it
      passes; the result of each test, pass or fail, is in the row's `note` or in the
      notes here.
- [ ] `docs/official-ai-accounts.md` names the new sources in its scanner-status column
      and records the ones that could not be read, with the reason.
- [ ] `docs/news-automation.md` states the shared-host rule and what
      `max_entries_per_scan` means.
- [ ] Loaded on the host with `sources_cli` after the deploy (owner-approved; a separate
      session).

## Steps

- [ ] Write a throwaway script outside the repository and run it with
      `cd apps/api && uv run python <script> <candidates.json>`. Per row:
      `sources_cli.load_file` on a scratch JSON in `sources.json` shape, then
      `validate_source_configuration(NewsSource(...))` (robots, parser, first article),
      then one `SafeNewsFetcher` to fetch the listing and run `parse_entries`: print the
      count, the first ten entries, and how many fall inside 72 hours. For page sources
      run `read_article` on two entries and print the text length; for summary sources
      print the shortest and the median summary.
- [ ] Fix "Claude blog": url `https://claude.com/resources/articles`, prefix
      `/resources/articles/`. Compare `https://claude.com/resources/product-announcements`
      as the listing and use it if it carries the product posts with less noise.
- [ ] Test and add: Claude developer blog (`https://claude.dev/rss.xml`), Claude Code
      changelog (`https://code.claude.com/docs/en/changelog/rss.xml`, summary evidence,
      top 2, every 720 minutes), Anthropic engineering
      (`https://www.anthropic.com/engineering`, prefix `/engineering/`), GitHub Changelog
      (`https://github.blog/changelog/feed/`, title keyword `Copilot`), Cursor changelog
      (`https://cursor.com/changelog/rss.xml`), Ollama blog
      (`https://ollama.com/blog/rss.xml`), OpenRouter announcements
      (`https://openrouter.ai/blog/`, prefix `/blog/announcements/`).
- [ ] Update the pinned Claude blog test in `apps/api/tests/test_news_automation.py`
      (`test_claude_blog_listing_yields_one_undated_entry_per_card`) to the live markup,
      and add one pinned parse test per new config shape through `_source_config(name)`.
- [ ] In `apps/api/tests/test_news_sources_cli.py`, add two file invariants: a
      summary-evidence row is the only enabled row on its host; rows sharing a host agree
      on `role`, `is_first_party` and the article-reading keys.
- [ ] Update the two documents; bump `reviewed_on`.
- [ ] File the follow-ups listed in the notes.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests
cd apps/api && uv run pytest tests/test_news_sources_cli.py tests/test_news_automation.py -q
npm run check:tasks
```

## Notes

- Rules read from the code, 2026-10-10:
  - Several rows may share a host (`blog.google` already has two), but `by_host`
    (`scanner.py`, `validation.py`) keeps one of them per host, so rows sharing a host
    must agree on `role`, `is_first_party` and the article-reading keys, and a row with
    `evidence_from_feed_summary` must be alone on its host.
  - `max_entries_per_scan` is "the top N of the listing", sliced before the seen and stale
    checks; it is not "N new entries per scan".
  - A candidate the writer declines costs two model calls (the duplicate check and the
    writer), not a whole pipeline run.
  - Changing a row's `url` creates a new row on the host and leaves the old one alone.
    If the old `claude.com/blog` row is in the database, switch it off in `/admin/news`.
- Probed on 2026-10-10 from a development machine with curl, not through
  `SafeNewsFetcher` and not from the host; confirm each before relying on it:
  - Claude Code changelog feed: 15 dated items, one or two a day, summaries of 369 to
    5,898 characters, titles are bare version numbers. The HTML page is 4.8 MB, over the
    fetcher's 2 MB cap, so the feed summary is the only readable evidence.
  - GitHub Changelog feed covers all of GitHub, hence the title keyword.
  - Cursor changelog feed: two or three entries a month, one page per entry.
- Looked at and not worth adding as they are; record each in
  `docs/official-ai-accounts.md`:
  - One long page with no per-entry address: the Claude apps release notes
    (`support.claude.com/en/articles/12138966-release-notes`), the OpenAI API changelog,
    the ChatGPT and Codex changelog, the Gemini API changelog, the Gemini app release
    notes. For the Claude page, the large items also appear as articles; in September and
    October 2026 only "Smart reports" and "Monthly API credits for Max and Team plans"
    were on that page alone.
  - Google Developers blog: robots.txt answers with a redirect, which the fetcher reads
    as refused.
  - VS Code feed: lists the next version as "(Insiders)" with a future date.
  - GitHub `releases.atom`: disallowed by GitHub's robots.txt.
  - DeepSeek: no listing, and its robots.txt answers with an HTML page.
- Follow-ups to file with this work: read one dated section of a single-page changelog;
  an `exclude_title_keywords` filter, then the VS Code feed; whether to follow a same-host
  redirect on robots.txt (a policy decision for the owner).
