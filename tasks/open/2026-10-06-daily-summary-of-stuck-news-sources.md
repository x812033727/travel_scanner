---
id: 2026-10-06-daily-summary-of-stuck-news-sources
title: Send the owner a daily summary of stuck news sources
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-06T01:03:38Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/scheduler.py
  - apps/api/app/news_automation/owner_summary.py
  - apps/api/tests/test_news_owner_summary.py
  - docs/news-automation.md
---

# Send the owner a daily summary of stuck news sources

## Why

The news scanner reports a source `stuck` when a dated entry of the last week has failed on
every hourly scan for more than six hours (`STUCK_AFTER` in
`apps/api/app/news_automation/scanner.py`, landed in #1041). The owner sees it only by opening
the admin: `/admin/news?tab=sources` lists stuck sources first under a red warning, and the
`/admin` dashboard's News card counts them in red (`news_sources_stuck`, added by the PR that
closed `2026-09-30-alert-in-admin-news-when-a`). A source can therefore stay stuck for days if
nobody opens the admin; OpenAI News lost every first-party story that way before #1041.

The optional "daily summary to the owner" from that ticket was not built because the site has
no channel for messages to the owner. Checked 2026-10-06: the only senders are community SMTP
(`apps/api/app/community/jobs.py` `send_mail`, account e-mails to users) and LINE push
(`apps/api/app/line/client.py`, price alerts to users who linked LINE). `admin_emails` in
`apps/api/app/config.py` only grants admin rights. Which channel to use, and whether to send at
all, is the owner's decision.

## Definition of done

- [ ] The owner has chosen a channel (LINE push to the owner's own linked LINE account, e-mail
      through the community SMTP to an owner address, or none) and that choice is recorded in
      Notes with its date.
- [ ] If a channel was chosen: once a day, when at least one enabled source is `stuck`, the
      owner receives one message naming each stuck source, its first stuck URLs and the hours
      since it got stuck; no message on a day with no stuck source, and never more than one a day.
- [ ] If the owner chose none: this ticket is closed with that decision in Notes.

## Steps

- [ ] Ask the owner which channel (or none), with the options above.
- [ ] Build the daily job next to the news scheduler (`scheduler.py`) with the message text in
      `owner_summary.py`, idempotent per day (a retry after a crash does not send twice).
- [ ] Tests with a fake sender: stuck sources → one message; none → no message; a second run the
      same day → no second message; a disabled stuck source is left out.
- [ ] Document it in `docs/news-automation.md` next to the stuck-source paragraph.

## How to verify

```bash
cd apps/api && PYTHONUTF8=1 uv run pytest tests/test_news_owner_summary.py -q
```

## Notes

- Split from 2026-09-30-alert-in-admin-news-when-a (claude-opus-5-5-news-admin-followups,
  2026-10-06): that ticket's dashboard count and enabled-only stuck count landed; only its
  optional owner summary is left here, because it needs the owner's choice of channel.
- If the threshold should differ per source, `STUCK_AFTER` could read a
  `config.stuck_after_hours` the way `max_entry_age` reads `max_entry_age_hours`; the
  admin copy `stuckSources` in `apps/web/lib/admin-news-messages/*.json` then must stop
  saying "6 hours". Nobody has asked for it yet.
