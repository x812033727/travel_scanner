---
id: 2026-10-10-load-the-changelog-and-developer-news
title: Load the changelog and developer news sources on the host
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-10T08:30:43Z
completed_at:
branch:
depends_on:
  - 2026-10-10-add-official-changelog-and-developer-update
scope:
  - docs/official-ai-accounts.md
---

# Load the changelog and developer news sources on the host

## Why

`apps/api/app/news_automation/sources.json` is only a file until it is loaded on the
production host: the scanner reads the `news_sources` table. The 2026-10-10 change repairs
"Claude blog" and adds seven sources (Claude developer blog, Claude Code changelog,
Anthropic engineering, GitHub Changelog, Cursor changelog, Ollama blog, OpenRouter
announcements). None of it reaches the site until the file is loaded, and two earlier
batches may not have been loaded either: `2026-09-30-cover-every-major-ai-agent-company`
and `2026-09-30-add-openai-deployment-safety-hub-as` both still list this step as open.

Running a command on the production host needs the owner's go-ahead each time.

## Definition of done

- [ ] The change is deployed (the parser change in `feeds.py` has to be on the host before
      "Claude Code changelog" can validate).
- [ ] The dry run's create / update / unchanged summary is recorded here: it also answers
      whether the two 2026-09-30 batches were ever loaded.
- [ ] `--apply` has run, and every source it refused is listed here with the reason.
- [ ] The old "Claude blog" row (`https://claude.com/blog`) is switched off.
- [ ] A day later: each new source has scanned without `stuck`, and the number of
      candidates it filed is noted.

## Steps

- [ ] Ask the owner; deploy through the `deploy` skill if the change is not live.
- [ ] Dry run, then apply (commands in `docs/news-automation.md`, Sources):
      `docker compose -f docker-compose.prod.yml exec -T api python -m app.news_automation.sources_cli`
      and the same with `--apply --actor-email <admin email>`.
- [ ] Changing a row's `url` creates a new row and leaves the old one alone, so the old
      `https://claude.com/blog` row shows under "not in file": switch it off on
      `/admin/news` (sources tab).
- [ ] Tick the host-load item on the two 2026-09-30 tickets if the dry run shows their
      sources were created or already present.
- [ ] Update the scanner-status column of `docs/official-ai-accounts.md` for any source
      the host refused.

## How to verify

`/admin/news?tab=sources` lists the eight sources enabled, with a last scan time and no
validation error. `GET /api/travel/guides?locale=zh-TW&kind=life&topic=ai-news&sort=news`
is where a published story from them would show.

## Notes

- All eight rows validated on 2026-10-10 from a development machine through
  `validate_source_configuration`. The host has another address: Cloudflare in front of
  `claude.com`, `claude.dev`, `code.claude.com` and `www.anthropic.com` answered 403 to
  that machine after a handful of requests in a few minutes, robots.txt included, and let
  the same requests through minutes later. One request an hour per source should stay
  under it, but a refusal on the first try is worth a second dry run before concluding.
- A first scan records undated entries and entries older than 72 hours as seen. Expect
  up to five candidates from GitHub Changelog, two from the Claude Code changelog and one
  from the developer blog on the first scan, and none from the HTML listings.
