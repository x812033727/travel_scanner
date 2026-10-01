---
id: 2026-10-01-after-the-tide-round-2-dramaturgy
title: After the Tide round 2: dramaturgy, character arcs and production feasibility pass
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-10-01T12:16:34Z
created_at: 2026-10-01T12:15:23Z
completed_at: 2026-10-01T13:37:01Z
branch: claude/nifty-heisenberg-0ldw0i-long-drama
depends_on: []
scope:
  - docs/videos/series-plans/tide-after-20260930
---

# After the Tide round 2: dramaturgy, character arcs and production feasibility pass

## Why

The first long-form drama plan (`docs/videos/series-plans/tide-after-20260930/`, merged in
PR #1047) had been through one self-review. A second pass by three independent readers
was needed before it is used to brief writers: tension and pacing (do the 45-minute
climaxes land, do the opponents ever win), character arcs and theme (does the love
line earn its beats, does the ending pay off), and production feasibility (legal
procedure, religious depiction, cast availability gaps, budget realism, retention).

## Definition of done

- [x] Three round-two reviews filed as `REVIEW-2-dramaturgy.md`, `REVIEW-2-characters.md`,
      `REVIEW-2-production.md`, and every adopted item applied to the four chapter
      outlines with the supporting documents (outline, setting, continuity, packaging,
      budget, README) kept consistent; `REVIEW.md` records what was applied, what is
      still pending and what was declined.

## Steps

- [x] Write the three reviews and consolidate decisions (scratch file
      `round2-decisions.md`, summarized in the REVIEW.md change log).
- [x] Apply the decisions to `chapter-01.md` to `chapter-04.md`, then sync the other
      documents and append the round-two change log.

## How to verify

```bash
cd docs/videos/series-plans/tide-after-20260930
grep -h '^## 第 [0-9]* 集' chapter-0*.md | sort | uniq -d        # empty: 40 unique titles
grep -h '^| 接續收尾' chapter-0*.md | grep -oE '\| [a-z]+｜'       # 40 hooks, no two consecutive equal
grep -c '^| 冷開場' chapter-0*.md                                  # 10 per chapter
```

Every chapter title appears verbatim as a row in `outline.md`; the twelve renamed titles
appear in `packaging.md` and `continuity.md`.

## Notes

- Decisions not adopted and why are in `REVIEW.md` under 未採納; the only item left open
  is a full recount of across-the-table confrontations (rule 3), two were converted.
- Episode 3 and 18 endings were moved off the phone after the sync agent flagged them,
  so only episodes 37 and 40 end on a call (the pair review A asked to keep).
- Budget moved from 700–850 to 750–950 萬 per episode (3.0–3.8 億 for 40); dubbing is
  estimated separately outside the 3.4 億 base.
- Opponent appearances recounted from the revised chapters are 48 episode-appearances,
  not review C's 42; `budget.md` shows both.
