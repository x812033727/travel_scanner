---
id: 2026-10-10-decide-whether-the-news-fetcher-follows
title: Decide whether the news fetcher follows a robots.txt redirect on the same host
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-10T08:30:56Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/fetch.py
  - apps/api/tests/test_news_automation.py
  - docs/news-automation.md
  - docs/official-ai-accounts.md
---

# Decide whether the news fetcher follows a robots.txt redirect on the same host

## Why

`SafeNewsFetcher` reads a host's robots.txt once and treats any answer that is not 2xx as
"not permitted" (`fetch.py`, `_robots_allowed`). That is the careful reading, and it
closes off publishers whose robots.txt answers with a redirect: the Google Developers
blog (`https://developers.googleblog.com/`) was seen doing so on 2026-10-10, so the
developer posts `@googledevs` announces cannot be a source. Moonshot (Kimi) is out for a
different answer, a 404.

Whether to follow the redirect is the owner's call, not a bug: it changes what the site
is willing to treat as permission.

## Definition of done

- [ ] The owner has chosen: keep refusing, or follow a redirect that stays on the same
      host (and whether a 404 means "no rules" as the robots convention reads it, or
      stays a refusal).
- [ ] If the answer changes anything: the fetcher, tests for each case, and the
      documents; then the Google Developers blog tested as a source.

## Steps

- [ ] Confirm the two observations through the fetcher itself (they were probed with
      curl): what `developers.googleblog.com/robots.txt` and Moonshot's answer.
- [ ] Put the choice to the owner with what each option would let in.
- [ ] Implement, or close the task with the decision written here.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py -q
```

## Notes

- A redirect to another host must stay refused whatever is decided: the allow-list is
  per host.
