---
id: 2026-09-28-so-that-s-why-season-3
title: So That's Why: season 3 topic bank (100 candidates)
status: done
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-09-28T23:07:47Z
created_at: 2026-09-28T23:07:39Z
completed_at: 2026-09-28T23:12:40Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/season3-topics.json
---

# So That's Why: season 3 topic bank (100 candidates)

## Why

Season 1 (`episodes.json`, B01–A25) and the season 2 bank (`season2-topics.json`, B26–A50) plan
200 questions. The owner asked for another 100: `season3-topics.json`, B51–A75, 25 per pillar, in
the same shape as the season 2 bank and marked `candidate` (checked only when made).

## Definition of done

- [x] 100 candidates, 25 per pillar (business, science, travel, tech), ids B51–B75, S51–S75, T51–T75, A51–A75.
- [x] No question repeats or closely overlaps any of the 200 already planned.
- [x] Every candidate has hook, a careful answer (hypotheses marked as such), two Shorts angles, key visuals and facts_to_verify.

## How to verify

The JSON parses; ids and counts check; a title overlap check against the other two files.

## Notes
- 2026-09-28 claude-opus: four agents, one per pillar, wrote 25 each; merged into season3-topics.json. Checks: ids B51–A75 in order, 25 per pillar, same keys as season2-topics.json, every title 為什麼…？ ≤ 30 characters, title similarity against the 200 existing and within the file (difflib > 0.55) plus a keyword grep. One duplicate found and fixed: T52 and A52 were both the power bank in checked luggage; A52 became the proximity sensor (手機螢幕講電話會變黑).
- Related but different angles kept on purpose: B54 IKEA meatballs vs B04 IKEA self-assembly; B55 McDonald's in India vs B06 McDonald's as real estate; A51 charging slowing after 80% vs S17 battery wear; S73 green yolk vs S30 onsen egg; S75 moon illusion vs S21 moon's same face.
- Myths the candidates already hedge (keep them hedged when made): Tokyo/Osaka escalator side from the 1970 Expo (T55, no records per Hankyu); Pepsi's "sixth-largest navy" (B61); Guinness bird-speed origin story (B59); Lamborghini clutch story (B75); bubble tea inventor (B52, disputed); Wansink studies (B72, some retracted); CERN room 404 (A59); Japan shutter sound as law (A60, industry practice). T70's Thai afternoon alcohol ban was suspended on 2025-12-03 for a 180-day trial, so recheck it on the day.
- No web searches for most candidates: every answer is a starting point and every facts_to_verify item must be checked when the episode is made.
