# Uber X19 v4 — independent narrative ballot A

## Freeze and first-blind lock

I read only the two frozen JSON artifacts before recording this section. SHA-256 at the read:

| Artifact | SHA-256 |
| --- | --- |
| `video.json` | `5feac02ca62feb4625959c1bd8a48266d185e84ac3776783fdc3b3eddb628988` |
| `shorts.json` | `bc2c17924498699adc6f8267ae820589ec7321c2e0f2e63e9931e10357f44c64` |

**Uninfluenced first-reader score: 7/10.** The through-line is clear: a driver shifts from rides to deliveries, Delivery overtakes Mobility in 2020 Q2 gross bookings without becoming profitable, the Postmates transaction follows that crossing, and Mobility retakes the gross-bookings lead in 2022 Q4. The accounting boundaries are unusually careful. My immediate friction is that the driver has almost no concrete choice or consequence after the first minute. Much of the middle reads as sequential financial commentary with repeated question-and-answer transitions. Both Shorts make sense on their own.

The Q labels below are my *own provisional first-reader checks*, fixed before seeing the official Q1–Q13 wording. Yes/no reflects the work as spoken and viewed from these JSON files; a “no” includes a repair.

| Provisional check | Vote | Exact evidence and, for NO, repair |
| --- | --- | --- |
| Q1 — Opening attracts attention | YES | `x19-b01-s01` opens on the car and driver changing what he waits for: “司機拿起手機，改等一只餐袋”; `x190105` asks whether the bag’s June lead means profit. |
| Q2 — A central question is established | YES | `x190105` poses “那條路就賺錢了嗎？” and `x190108` asks whether the passenger car can reclaim the lead. These are answered by `x190317`, `x190611`, and `x190625`. |
| Q3 — The human conduit has agency | NO | The driver presses a dispatch button at `x190210`, but the script says “示意司機”; the last return (`x190613`) simply has him receive another rider. Give this explicitly illustrative driver one concrete, repeatable decision at each pivot—e.g. which request to accept and what wait or trip it replaces—while keeping it clear that company data cannot attribute the macro change to this one driver. |
| Q4 — Chronology is legible | YES | The crossing is `x190301`; `x190401` says the Postmates signing was July 6 after the June quarter; `x190501` dates close to December 1; `x190601` and `x190610` move to 2021 Q4 and 2022 Q4. |
| Q5 — The reversal has proof | YES | `x190302` gives Mobility at US$3.046bn, `x190304` Delivery at US$6.961bn, and `x190317` Delivery adjusted EBITDA at negative US$232m. |
| Q6 — Causal claims are bounded | YES | `x190220` says the filings do not break out the effect of restaurant recruitment; `x190309` says driver reassignment cannot be separated; `x190403` rejects the acquisition as a cause of the prior June result. |
| Q7 — The financial stakes are understandable | YES | `x190307`: gross bookings are platform transactions, not all Uber revenue; `x190320`: the company still recorded a GAAP net loss of US$1.775bn. |
| Q8 — The middle sustains momentum | NO | Twenty-five recorded loops include near-immediate question/answer pairs (`x190306`→`x190307`, `x190311`→`x190313`, `x190314`→`x190317`) and later repeat the same “which side leads / which side profits” frame (`x190604`, `x190609`, `x190614`, `x190624`). Consolidate the Q2 accounting explanation and use fewer, more consequential open questions so each act adds a new complication. |
| Q9 — The pictures tell the story | NO | The recurring visual language is generic phone/car/bag/ledger. The quantified turn is strongest on `x19-b03-s02`, `x19-b03-s04`, and `x19-b03-s17` stats cards, whereas `x190316` merely illustrates a pickup. Add a recurring visual transformation of the same dispatch screen or curb/restaurant geography at the three reversals; keep exact figures on the existing postproduction cards. |
| Q10 — The ending pays off | YES | `x190611` resolves the riding lead, `x190616` clarifies both businesses grew, and `x190625` resolves the separate department metric with both 2022 Q4 adjusted EBITDA values positive. |
| Q11 — Short 1 stands alone | YES | Its hook says “二〇二〇年第二季，優步外送交易額超過載客”; its middle distinguishes platform bookings from revenue, then cites negative Delivery and positive Mobility adjusted EBITDA; “超車不等於賺” is a clear standalone payoff. |
| Q12 — Short 2 stands alone | YES | Its hook asks whether the acquisition caused the 2020 lead; the sequence says June already crossed, July 6 was only signing, Q3 was still pre-close, and December 1 was closing. “時間不能倒放” answers its own hook. |
| Q13 — Ready as a compelling spoken film | NO | The closing `x190626` asks the viewer about their own change in rides and delivery, a promising human angle that arrives after 110 prior scenes; `x190627` then pivots to subscription. Move a version of that lived choice into the first act and echo it at the June crossing and final curb, while trimming repeated ledger questions. |

**First-blind verdict:** Solid research-led narrative with a credible two-part reversal and two self-contained Shorts. I would request a narrative pass for human agency, visual continuity, and compression before treating the long film as ready.

## Official NARRATIVE_PANEL ballot (independent reader A)

I then read `AGENTS.md`, `.agents/skills/brand-story/SKILL.md`, `.agents/skills/youtube-video/references/story.md`, and the `NARRATIVE_PANEL` plus its reader instructions in `tools/video/core/narrative.mjs`. This is my own 13-question vote, not a merged two-reader worker receipt. I apply the panel's strict rule that one breaking sentence makes a required check NO. Quoted lines below are the spoken wording (`say` where supplied).

| Official question | Vote | Exact spoken evidence and repair for NO |
| --- | --- | --- |
| Q1 `scene_first` — concrete action in first four sentences | **YES** | `[x190101] 二〇二〇年春，路邊一輛車停下；司機拿起手機，改等一只餐袋。` The year, curb, driver, and action are already in the first line. |
| Q2 `no_spoiler` — opening withholds later results | **YES** | `[x190107] 年底，兩張配送地圖挪到同一張桌上，中間那條接線被遮住。` It previews the later integration moment while explicitly hiding its outcome; the first chapter does not give the June profit answer or the final riding result. |
| Q3 `one_line` — one chronological story | **YES** | `[x190301] 六月季報揭曉：外送訂單額真的高過載客。` The main sequence then advances to the July signing (`x190401`), December close (`x190501`), 2021 Q4 (`x190601`), and 2022 Q4 (`x190610`). The opening's forward glimpses function as the permitted opening preview. |
| Q4 `no_toc` — no structural announcements | **YES** | `[x190306] 六月那兩根柱子突然換位，司機手機上的錢和公司帳上的錢，究竟比的是哪一種？` Transitions ask what the unfolding event means rather than announcing a list or chapter plan. |
| Q5 `chapters_link` — chapter starts answer or carry a concrete prior beat | **YES** | The chapter-2 first line picks up the opening phone: `[x190201] 司機能轉接餐袋，是因為優步早有外送網，只是當時載客遙遙領先。` Chapter 3 answers `x190222` with `x190301`; chapter 4 answers `x190323` with `[x190401] 開場桌上那張還沒接入的外送網，是 波斯特梅茲；七月六日優步才簽約，六月季度早已結束。` Chapter 5 answers `x190422` with `x190501`, and chapter 6 answers `x190522` with `x190601`. |
| Q6 `open_loops` — an unresolved question or turn within each 90 seconds | **YES** | `[x190408] 店家網站的一筆單，變成司機手機上的取件地址；秋季載客能追回外送嗎？` This stays open through the Q3 ride recovery and Delivery comparison (`x190409`–`x190411`). The script has recurring unanswered hooks from `x190105` through `x190624`; at the stated 280–300 spoken characters/minute, the longest question-to-question stretch in the JSON is about 46–49 seconds. That is a text estimate, not a measured TTS timeline. |
| Q7 `payoffs` — open questions receive new answers and distant callbacks | **YES** | `[x190317] 開場那只餐袋雖跑在前，外送部門調整後 E B I T D A 仍虧兩點三二億美元。` This names the opening bag while answering `x190105` with a new result. `[x190501] 開場還留在桌上的第二張網，十二月一日才因 波斯特梅茲 收購完成進到優步。` recalls the earlier hidden connection; `x190611` recalls the opening car with the later lead. |
| Q8 `no_recap` — no same fact more than once without an explicit callback | **NO** | `[x190416] 外送訂單總金額較大，載客部門調整後卻仍較早為正。` It immediately restates the facts just given by `x190411` (Delivery still ahead) and `x190414`–`x190415` (Mobility positive, Delivery negative), without adding a new result. **Repair:** remove `x190416` and let the next beat, `x190417` (the app's additional delivery entry point), move the story forward. The same compression pass should examine `x190503`–`x190505`, which explain the separate consumer apps and joining merchant/delivery network, then restate those same two points as a metaphor. |
| Q9 `chapters_are_events` — event/reveal chapter titles (**advisory, not required**) | **YES (advisory)** | The titles identify developments: “六月底，外送跨過了載客”, “七月簽約時，交叉早已發生”, and “十二月交割，隔年用戶才遷移”. `[x190301] 六月季報揭曉：外送訂單額真的高過載客。` demonstrates how the chapter headline becomes a reveal in the spoken story. |
| Q10 `outro_no_next` — no next-video mention | **YES** | `[x190627] 想看熟悉品牌的轉折究竟由哪筆帳撐住，歡迎訂閱品牌故事。` The outro asks for a subscription but names no next installment or file. |
| Q11 `opening_hooks` — at least three later moments after first scene | **YES** | `[x190105] 如果六月餐袋真的衝到前面，那條路就賺錢了嗎？` `[x190106] 七月，桌上又出現另一張還沒接入的外送網。` `[x190107] 年底，兩張配送地圖挪到同一張桌上，中間那條接線被遮住。` `[x190108] 等人們重新出門，那輛載客車又能開回前面嗎？` These are later unknowns, not a spoken table of contents. |
| Q12 `one_thread` — identifiable subject or problem advances through every chapter | **YES** | `[x190103] 同一支手機，一邊等乘客，一邊等餐廳的袋子。` The same dispatch phone/driver and competing ride/delivery paths return in the acquisition (`x190408`, `x190505`) and the final curb: `[x190613] 回到路邊，那位示意司機又接到乘客；同一支手機另一側仍有餐袋取件路線。` This meets the panel's identifiable-thread threshold, although the first-blind ballot separately finds the driver's agency thin. |
| Q13 `no_detour` — every passage advances the opening problem | **NO** | `[x190520] 公司說同時使用載客和外送的人，帶來近半的總訂單額。` In `x190519`–`x190521`, the film opens a new question about customer overlap, gives its share, and then warns against attributing the crossing to a driver or shop. It supplies no consequence for the opening profit question, the Postmates timing, or the riding recovery. **Repair:** cut the three-line customer-overlap passage and move directly from the driver handling different orders (`x190516`) to the year-end Delivery profitability question (`x190522`), or retain it only if a verified, explicit consequence for the two-route business can be spoken. |

**Panel result from this reader:** 11 YES and 2 NO, with Q9 counted among the YES votes as an advisory question. The two required NO votes are Q8 and Q13. This count is a single independent ballot, so it does not predict a two-reader merged decision.

## Shorts as standalone stories

**Short 1 — YES, standalone.** Its first narrated sentence supplies the company, period, and reversal: “二〇二〇年第二季，優步外送交易額超過載客。” The setup gives both sides of the comparison, “外送六十九點六一億，載客三十點四六億美元。” The turn says “可是這是平台訂單額，不是優步全部收進的營收。” Then the Short gives the company revenue and contrasting department indicators before paying off its title with “外送確實超車，卻還不是獲利的答案。” It does not require a long-film scene or an unexplained prior character.

**Short 2 — YES, standalone.** Its first line asks the causal question: “優步二〇二〇年外送反超，是收購帶來的嗎？” The Short itself establishes that June had already crossed, July 6 was only the signing, Q3 still preceded closing, and December 1 was the close. “時間不能倒放：六月反超，不能算成十二月交割成果。” resolves the hook in the Short's own words. The two-app and merchant-network lines add the integration nuance without assuming the viewer saw the long film.

The two NO repairs above are editorial and do not require changing the financial claims. A separate creative pass could strengthen the driver as a recurring decision-maker and vary the visuals; those are quality improvements behind the 7/10 first impression, not extra official panel failures.
