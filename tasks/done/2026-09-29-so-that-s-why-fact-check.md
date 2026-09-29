---
id: 2026-09-29-so-that-s-why-fact-check
title: So That's Why: fact-check season 1 days 36-100
status: done
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-09-29T02:36:45Z
created_at: 2026-09-29T02:36:37Z
completed_at: 2026-09-29T04:36:23Z
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

- [x] `week6/`…`week15/<id>.md` for all 65, in the week 5 format.
- [x] episodes.json marks them fact-checked with the answers, hooks and Shorts angles the checks leave; titles.json (all locales), schedule.csv, playlists.md and the previews follow any title change.

## Steps

- [x] One fact-check agent per episode, a week at a time, drafts written outside the repo.
- [x] Mechanical check per week (claim URLs, Shorts lengths, form limits), then copy into the repo.
- [x] JSON, CSV, playlists and previews.

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
- The request form takes a premise of up to 4,000 characters and a note of up to 2,000
  (`DramaRequestIn`, and the web form's maxLength). Weeks 6–7 fit as written, but 13 packages in
  weeks 8–11 had notes of 2,018–3,116 characters (their long 「必用來源」 lists). Both fields reach
  the script writer together (`flow.mjs` planPayload), so in every package whose note was over
  2,000 the 「必用來源」 line now ends the 故事前提 block instead; A19's list is split, with the
  rest kept in the note as 「必用來源（續）」. Every package now fits both limits.
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
- 2026-09-29 weeks 10–11 (days 64–77) done by claude-opus: S17, T17, A16, B17, S18, T18, A17,
  B18, S19, T19, A18, B19, S20, T20. Four titles changed:
  A16 「為什麼 AI 特別容易畫錯手指？」 (developers report big gains; 2025–26 studies still list hands);
  B18 「為什麼 Google 頭上多了一家 Alphabet？」 (no rename: a new holding company above Google);
  S19 「為什麼洋芋片袋裡那麼多「空氣」？」 (nobody measured "half"; the worst Korean test bag was 46.3%);
  B19 「為什麼 Airbnb 快撐不下去時，跑去賣選舉麥片？」 (cereal bought time; YC and Sequoia saved it).
  Myths not to bring back: the Roadster funding the Model S, "you are the product" as fact,
  Bhatt "apologising" for USB, a 30-30 rule countdown as safety, Finland's "statutory" coffee
  break, prohibition driving Finnish coffee, "the Dutch were short 100 years ago", milk making
  the Dutch tall, alphabet.com as the reason for abc.xyz, the 25-hour body clock.
- 2026-09-29 weeks 12–13 (days 78–91) done by claude-opus: A19, B20, S21, T21, A20, B21, S22,
  T22, A21, B22, S23, T23, A22, B23. Two titles changed:
  A19 「為什麼晶片製程越小越快？」 (transistors shrink, chips don't; "3nm" is a generation name);
  B22 「為什麼 Samsung 從賣乾貨和麵條變成科技巨頭？」 (produce and dried seafood, plus a noodle
  factory, per the Hoam Foundation history). T21 (Kyoto) takes no side on the bombings and shows
  no mushroom cloud or casualties. T23's checker ran while the review classifier was down; its
  output was checked by hand (repo untouched, 26 sourced rows, nothing unexpected in the blocks).
  Myths not to bring back: "Moore's law = every 18 months", Gillette inventing razors-and-blades,
  Stimson's Kyoto honeymoon, Warner saving Kyoto, Kurita as the sole inventor of emoji, the
  1998 "Yahoo could have bought Google for $1M", "GDPR requires cookie banners", "0–100 °F from
  body heat and a Danzig winter", "Korea's law used Korean age until 2023", "THSR has no ballast".
- 2026-09-29 weeks 14–15 (days 92–100) done by claude-opus: S24, T24, A23, B24, S25, T25, A24, B25,
  A25. Three titles changed: A23 「為什麼電動車大多只有一檔？」 (EVs have a single-speed reduction
  gear; EPA lists 302 of 321 MY2026 EV configurations as one speed); B24 「為什麼 Zara 三週就能把新款
  送到店裡？」 (Inditex's own "3 weeks", for part of the range; "two weeks" was a 2003 case's
  restock figure); B25 「為什麼 LINE 在台灣日本很紅，在美國卻紅不起來？」 (LINE's 2016 prospectus
  reports US users; the US was never a core market). A25 is the season 1 finale: its 結尾預告 thanks
  viewers and asks for season 2 questions without naming a topic. T24 settles the Buddhist Era
  epoch as the traditional parinirvana (Thailand starts year 1 a year later, hence +543; Sri Lanka
  and Myanmar +544), and Thailand adopted BE in 1913, not 1912.
- Season 1 is fully fact-checked: all 100 in episodes.json are `fact-checked`, and every package's
  premise and note fit the request form. Seasons 2 and 3 are candidate banks, not scheduled
  episodes; they get their own tasks.
