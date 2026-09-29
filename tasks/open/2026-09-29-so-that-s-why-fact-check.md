---
id: 2026-09-29-so-that-s-why-fact-check
title: So That's Why: fact-check season 1 days 36-100
status: in-progress
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-09-29T02:36:45Z
created_at: 2026-09-29T02:36:37Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/week6
  - docs/videos/so-thats-why/week7
  - docs/videos/so-thats-why/week8
  - docs/videos/so-thats-why/week9
  - docs/videos/so-thats-why/week10
  - docs/videos/so-thats-why/week11
  - docs/videos/so-thats-why/week12
  - docs/videos/so-thats-why/week13
  - docs/videos/so-thats-why/week14
  - docs/videos/so-thats-why/week15
  - docs/videos/so-thats-why/episodes.json
  - docs/videos/so-thats-why/titles.json
  - docs/videos/so-thats-why/schedule.csv
  - docs/videos/so-thats-why/playlists.md
---

# So That's Why: fact-check season 1 days 36-100

## Why

The owner asked to fact-check everything before production (2026-09-29, 「先全部審核」). Days 1–35
have packages in week1–week5; days 36–100 (65 episodes, weeks 6–15) still have only the plan in
episodes.json. Seasons 2 and 3 follow as their own tasks.

## Definition of done

- [ ] `week6/`…`week15/<id>.md` for all 65, in the week 5 format.
- [ ] episodes.json marks them fact-checked with the answers, hooks and Shorts angles the checks leave; titles.json (all locales), schedule.csv, playlists.md and the previews follow any title change.

## Steps

- [ ] One fact-check agent per episode (weeks 6–9 done), a week at a time, drafts written outside the repo.
- [ ] Mechanical check per week (claim URLs, Shorts lengths), then copy into the repo.
- [ ] JSON, CSV, playlists and previews.

## How to verify

`npm run check:tasks`; the JSON files parse; the Shorts check.

## Notes

- 2026-09-29 weeks 6–7 (days 36–49) done by claude-opus: S10, T10, A09, B10, S11, T11, A10, B11,
  S12, T12, A11, B12, S13, T13. One title changed: B10 is now 「為什麼任天堂一開始是做花札紙牌的？」
  (Nintendo began with hanafuda in 1889 and made Western playing cards only from 1902), carried
  into titles.json in every locale (ja says 食品事業, not 即席麺), schedule.csv, playlists.md and
  A09's preview. Myths not to bring back: Nintendo's "love hotel", the Salute's million piles,
  "QWERTY was made to slow typists", a tourist chewing-gum allowance in Singapore, TSMC's
  largest customer being Apple in 2025, measured 5G speeds for Taiwan (NCC has none).
- The premise and note blocks run up to about 1,000 and 1,700 characters; the request form
  takes 4,000 and 2,000 (`DramaRequestIn`), so they paste as they are.
- Recheck on the day for each episode is in its package's 查核結果 and the agents' notes: pages
  that returned 403/503 here (NINDS, NCC, SSO, UNESCO, DEWA, DSC) were confirmed only through
  search snippets or secondary copies.
- 2026-09-29 weeks 8–9 (days 50–63) done by claude-opus: A12, B13, S14, T14, A13, B14, S15, T15,
  A14, B15, S16, T16, A15, B16. Five titles changed, carried into titles.json, schedule.csv,
  playlists.md and the neighbouring previews:
  T15 「為什麼日本溫泉旅館可以穿浴衣吃晚餐？」 (no rule requires it; some hotels ask guests not to);
  A14 「為什麼有些遊戲主機要賠錢賣？」 (Xbox and early PS5 yes, Nintendo mostly no);
  S16 「為什麼高鐵車頭要做成長鼻子？」 (THSR's 700T nose is shorter than the 700 series');
  T16 「為什麼機票通常越接近出發越貴？」 (an average, fares also drop);
  B16 「為什麼 Supreme 明明賣得掉，還故意少做？」 (Jebbia: "if we can sell 600, I make 400").
  Myths not to bring back: LEGO's rescue by the Star Wars licence or the film, "every console is
  sold at a loss", Dyson's first product being Japanese, "scrolling past is a YouTube signal",
  incognito mode lowering fares, "insulated lines are why birds are safe", Setun as the first
  ternary computer, the Salute's 1,156,650 piles, the Pisa tower being straightened to 3.97°.
- Four checkers (T14, B14, T16, S16) ran out of the 200-search session budget; what they
  could not trace is in their recheck lists.
