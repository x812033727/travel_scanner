---
id: 2026-10-07-correct-korea-winter-planned-dates
title: Resolve Korea winter planned dates source conflict
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-07T05:57:33Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/korea-winter-events-2026.json
  - apps/web/public/guides/korea-winter-events-2026/diagram-1.svg
  - docs/article-localization/source-corrections/20261007-korea-winter
---

# Resolve Korea winter planned dates source conflict

## Why

The winter guide categorically says Gwangbok-ro dates are unannounced and
Haeundae is Busan's only dated winter event. The government festival dataset
lists Gwangbok-ro planned dates of 2026-12-04 through 2027-01-31, with data date
2026-07-27. Planned official data and final operator confirmation must be
distinguished before translating this article.

## Definition of done

- [ ] Independently resolve the official planned-calendar/source-cutoff conflict.
- [ ] Preserve previous-season operating times as explicitly previous-season data.
- [ ] Correct only approved source/document/diagram fields through version/hash guards.
- [ ] Start translations only after the source decision and source asset review.

## Steps

- [x] Preserve primary evidence and exact source/diagram findings outside Git.
- [ ] Review /blocks/0/text, /blocks/2/rows/6/1, /blocks/10/text and diagram
      visible labels 25/27, description, timeline geometry, legend and sources.
- [ ] Check archival/operator evidence rather than treating the exposed data
      date as a proven historical publication timestamp.
- [ ] Resolve unverified Elysian prior-season claims and keep later-season facts dated.
- [ ] Apply genuine independent correction approval, render and prepare missing locales.

## How to verify

Check https://www.data.go.kr/en/data/15013104/standard.do against organizer
evidence and the source's September cutoff. Check Haeundae's official dates
separately from old-season 18:00-23:00 times. The independent source-correction
review must bind exact old/new public document versions and source SVG hashes.

## Notes

- Independent conflict finding SHA
  3472bfc035829186d2a887ec28887644d1a76d310078f8e770a648bde5038707.
- Preserved government evidence SHA
  566b58cf6c1024d80d3b75d680ce80df44521a478224108208915e0149b11857.
- The government row is a planned calendar, not final organizer confirmation.
  No September archived snapshot was verified; do not overstate this as a
  proven publication-date error. The wording/source conflict remains held.
- No source document, SVG, database row or target translation was changed.
