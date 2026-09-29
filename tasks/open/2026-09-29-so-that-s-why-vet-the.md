---
id: 2026-09-29-so-that-s-why-vet-the
title: So That's Why: vet the season 2 and 3 topic banks
status: in-progress
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-09-29T04:38:19Z
created_at: 2026-09-29T04:38:15Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/season2-topics.json
  - docs/videos/so-thats-why/season3-topics.json
  - docs/videos/so-thats-why/topic-checks
---

# So That's Why: vet the season 2 and 3 topic banks

## Why

The owner asked to fact-check everything before production (2026-09-29, 「先全部審核」). Season 1
now has a full package per episode (tasks/done/2026-09-29-so-that-s-why-fact-check.md). Seasons 2
and 3 are banks of 100 candidates each (`season2-topics.json`, `season3-topics.json`): a title, a
hook, a hedged answer, two Shorts angles and `facts_to_verify`, none of it checked. A candidate
whose premise is false (like season 1's 「Google 改名」 or 「電動車沒有變速箱」) should be caught now,
not on the day it is scheduled.

These are not scheduled episodes, so this is a topic-level check, not a full package: the premise,
hook, answer and each `facts_to_verify` item against primary sources, a verdict, and corrected
fields. The full package (outline, Shorts scripts, paste-ready blocks) is still written when a
topic is scheduled, as for season 1.

## Definition of done

- [ ] Every one of the 200 candidates has a verdict — 保留, 修正, 換題 (same subject, a premise
      that holds) or 建議刪除 — with the claims table and sources in `topic-checks/`.
- [ ] Both topic files carry the corrected title, hook, answer and Shorts angles, `status:
      "checked"` (or `"drop-suggested"`), a `check` path to its report, and `facts_to_verify`
      reduced to what must be rechecked on the day.
- [ ] No corrected or replacement title repeats one in `episodes.json` or the other bank.

## Steps

- [ ] One checker per 12–13 topics (8 per season), drafts written outside the repo.
- [ ] Mechanical check: every row has a URL or a labelled reason, titles are 為什麼…？ ≤ 30
      characters, Shorts angles ≤ 20.
- [ ] Merge into the two JSON files and copy the reports into `topic-checks/`.

## How to verify

`npm run check:tasks`; both JSON files parse; every candidate has `status` checked or
drop-suggested and a `check` path that exists.

## Notes
