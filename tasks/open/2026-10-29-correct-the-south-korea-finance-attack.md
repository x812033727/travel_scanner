---
id: 2026-10-29-correct-the-south-korea-finance-attack
title: Correct the South Korea finance attack article: the country, not the regulator, plans the IT checks
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-29T04:55:01Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-29-correct-the-south-korea-finance-attack.md
---

# Correct the South Korea finance attack article: the country, not the regulator, plans the IT checks

## Why

The published article `tech-news-south-korea-finance-cyberattacks-20261028`
(https://mokaair.com/zh-TW/life/tech-news-south-korea-finance-cyberattacks-20261028) says the
financial regulator plans security checks on dozens of IT systems. Its source, TechCrunch, says
"The country also plans to conduct security checks on dozens of IT systems": the subject is
South Korea, not the regulator. Found by both fact checks of the daily brief episode
`daily-ai-20261028` (`docs/videos/daily-ai-20261028/verify-1.md` claim g2yg, `verify-2.md`),
which corrected the video.

The article was written by the news automation and lives in the database; the fix goes
through /admin/news or the guide editor on the host.

## Definition of done

- [ ] The sentence names South Korea (or the government) as planning the checks, in zh-TW and
      every published locale.

## Notes

- Scope is this file only: the fix is a database edit on the host, not a repository change.
