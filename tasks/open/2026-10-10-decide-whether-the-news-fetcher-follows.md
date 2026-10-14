---
id: 2026-10-10-decide-whether-the-news-fetcher-follows
title: Decide whether the news fetcher follows a robots.txt redirect on the same host
status: in-progress
priority: P3
area: api
owner: codex-deepmind-20261014
claimed_at: 2026-10-14T13:38:53Z
created_at: 2026-10-10T08:30:56Z
completed_at:
branch: codex/deepmind-news-redirects-20261014
depends_on: []
scope:
  - apps/api/app/news_automation/fetch.py
  - apps/api/app/news_automation/sources.json
  - apps/api/app/news_automation/sources_cli.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_news_sources_cli.py
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

- [x] The owner has chosen: keep refusing, or follow a redirect that stays on the same
      host (and whether a 404 means "no rules" as the robots convention reads it, or
      stays a refusal).
- [x] If the answer changes anything: the fetcher, tests for each case, and the
      documents; then the Google Developers blog tested as a source.

## Steps

- [x] Confirm the two observations through the fetcher itself (they were probed with
      curl): what `developers.googleblog.com/robots.txt` and Moonshot's answer.
- [x] Put the choice to the owner with what each option would let in.
- [x] Implement, or close the task with the decision written here.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py -q
```

## Notes

- A redirect to another host must stay refused whatever is decided: the allow-list is
  per host.
- 2026-10-14: The owner chose to follow only same-host HTTPS robots redirects after the
  usual public-IP, TLS and redirect-limit checks; cross-host redirects and 404 still
  refuse. Native fetcher readback: Google Developers `/robots.txt` returns 301 to
  `/robots.txt/` (200 with no disallow); Moonshot `/robots.txt` returns 404.
- The DeepMind RSS is valid, but the current article redirects to
  `developers.googleblog.com`; two other recent items redirect to `blog.google`. The owner
  separately approved both exact article redirect hosts. The DeepMind source now permits
  those two hosts and uses `blocks-container` for the destination article. Without that parser
  setting, the fetched 200 page yielded zero article characters; with it, the current
  article yielded over 24,000 source characters. Local source validation passed.
- A redirected robots response must be text/plain and contain a `User-agent` rule;
  otherwise a same-host HTML 200 could be mistaken for permission. The redirected
  Google Developers robots file satisfies both checks.
- With the reviewed DeepMind configuration, all four RSS items within the 72-hour window
  fetched over the native safe transport and yielded article text: 5,584 characters on
  `deepmind.google`, 9,001 and 19,466 on `blog.google`, and 24,154 on
  `developers.googleblog.com`. This is local verification; the live source row has not
  been updated or rescanned with this code.
- Google Developers Blog was also tried as a standalone HTML source: its home page was
  readable, but the first parsed candidate was an off-host community link, so source
  validation would refuse it. No separate source was added.
- The live admin page cannot edit redirect hosts or parser config on an existing source.
  Production application therefore needs a one-source CLI run after the safe fetcher is
  deployed. Preserve the existing row if validation fails during that run. A successful
  source validation reads only the first feed article; verify the cited robotics URL
  through the next full scan before calling the live source recovered.
