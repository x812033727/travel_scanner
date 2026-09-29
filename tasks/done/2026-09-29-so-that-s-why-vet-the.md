---
id: 2026-09-29-so-that-s-why-vet-the
title: So That's Why: vet the season 2 and 3 topic banks
status: done
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-09-29T04:38:19Z
created_at: 2026-09-29T04:38:15Z
completed_at: 2026-09-29T06:31:08Z
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

- [x] Every one of the 200 candidates has a verdict — 保留, 修正, 換題 (same subject, a premise
      that holds) or 建議刪除 — with the claims table and sources in `topic-checks/`.
- [x] Both topic files carry the corrected title, hook, answer and Shorts angles, `status:
      "checked"` (or `"drop-suggested"`), a `check` path to its report, and `facts_to_verify`
      reduced to what must be rechecked on the day.
- [x] No corrected or replacement title repeats one in `episodes.json` or the other bank.

## Steps

- [x] One checker per 12–13 topics (8 per season), drafts written outside the repo.
- [x] Mechanical check: every row has a URL or a labelled reason, titles are 為什麼…？ ≤ 30
      characters, Shorts angles ≤ 20.
- [x] Merge into the two JSON files and copy the reports into `topic-checks/`.

## How to verify

`npm run check:tasks`; both JSON files parse; every candidate has `status` checked or
drop-suggested and a `check` path that exists.

## Notes
- 2026-09-29 season 2 done by claude-opus (8 checkers, B/S/T/A 26–38 and 39–50): 3 保留, 95 修正,
  2 換題 (A35 retitled to the 2006 Western Digital settlement at the owner's request, to avoid
  repeating season 1's A03; A43 to 「為什麼有些詐騙訊息假得很明顯？」, since the typo premise is not
  in Herley 2012), 0 建議刪除; 53 titles changed, mostly 「都／總是」 overstatements. Reports are
  `topic-checks/s2-*.md`. A35's settlement facts were checked against the NBC article by hand.
- The checkers stopped once on the account's weekly usage limit (2026-09-29 ~04:45 UTC) and were
  resumed after the 06:00 UTC reset; partial work was kept.
- 2026-09-29 season 3 done by claude-opus: 6 保留, 94 修正, 0 換題, 0 建議刪除; 41 titles changed.
  Premises that were wrong and are now fixed: Giant launched its brand before Schwinn left (B64),
  the Lamborghini car company never made tractors (B75), Kroger scanned a barcode before the 1974
  gum (B69), Pepsi's "navy" is a legend (B61), Japan's shutter sound is carrier practice, not law
  (A63), not all AI images start from noise (A69). B69 dropped its barcode-digits Short so only A67
  explains the digits. Checkers ran out of the 200-search allowance in several batches and
  finished by direct fetch; what they could not read is in each report's 製作當天重查.
- Overlaps left for scheduling: S55 (banana browning) with S50 (apple browning); A29/A30 with A70;
  A38 with A58. Pick one angle per pair when scheduling.
