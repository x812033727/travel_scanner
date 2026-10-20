# Garmin X15 — independent blind narrative review A, v1

**Verdict: HOLD.** Eight of the twelve required `NARRATIVE_PANEL` checks pass; four fail. The advisory chapter-event check passes. This is a narrative and planned-Shorts assessment, not a source or factual verification. I read the current panel, the frozen `video.json` narration and scene data, `shorts.json`, `series.json`, and the matching `script.md`; I did not consult the source matrix, treatment, prior Garmin reviews, or author notes before voting.

| Frozen input | SHA-256 |
| --- | --- |
| `video.json` | `0a8ca399e47d274d0163b9268f4813f9f1037a7a40435feb5bcbb569065ff88a` |
| `shorts.json` | `b216f9b598aa512148bd2f673e71e509c0c3fcc3f2ca64d0e9d6ffbb653e2da6` |

Panel rules SHA-256: `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`. Votes use the panel's strict rule: one counterexample makes a check **No**; uncertainty also means **No**.

| Panel check | Vote | Script evidence and reason |
| --- | --- | --- |
| `scene_first` | **Yes** | `[x150101] 二〇一一年，一份年報把一個字改了。` The first line places a document's concrete change in a year; the opening does not greet the viewer or introduce a topic in the abstract. |
| `no_spoiler` | **No** | `[x150103] 現在，報表寫的是：已使成長停滯。` This gives away the 2011 wording and result that chapter 4 later presents as its reveal in `[x150423–x150426]`. `[x150109]` also states the later roughly doubled revenue before chapter 6. |
| `one_line` | **Yes** | `[x150336] 兩年後，新的全年財報到了。` After the opening's preview, the body proceeds from 2006 through 2008, 2010–11, and 2025, tracking the automotive/mobile share and the later revenue mix. |
| `no_toc` | **Yes** | `[x150110] 車裡的路線變擁擠後，Garmin 把生意帶去哪裡？` This asks the story's question. The chapter transitions pose next consequences rather than announce a sequence of sections. |
| `chapters_link` | **Yes** | `[x150231] 一個產品系列，究竟能占到公司收入多少？` leads directly to `[x150301] 二〇〇八年的答案，是百分之六十四。` The other boundaries likewise move from the next annual report to that report, from the wrist-device tease to the watches, and from the call for a later full-year table to its release. |
| `open_loops` | **Yes** | `[x150335] 那條占七成的收入線，能撐住嗎？` is one of many live questions. The current estimated timeline's 45-second cadence check reports no gap, exceeding this panel's 90-second minimum; this is an estimate, not measured audio. |
| `payoffs` | **No** | `[x150317] 更麻煩的是，產品價格和毛利還會怎麼走？` promises outcomes for both price **and** gross margin. `[x150318–x150319]` gives earlier discounts and a possibility; `[x150417–x150420]` later answers average selling price, but the margin outcome is never stated. That leaves one named question only partly paid off. |
| `no_recap` | **No** | `[x150401] 二〇一〇年，車用與行動收入約十六億七千萬。` is restated four lines later as `[x150405] 可它仍賣了十六億多，究竟變的是什麼？` without a named callback or a new figure. The second line could ask about the reversal without repeating the amount. |
| `chapters_are_events` (advisory) | **Yes** | Chapter 4, 「金額下滑，風險用語也變了」, names the change opened by `[x150401]`; the other titles name a rise, a concentration, a move beyond the car, or a five-department reveal. They are events or findings rather than generic functions. |
| `outro_no_next` | **Yes** | `[x150635–x150637]` answers, asks the viewer a related question, and invites subscription. None mentions another video or episode. |
| `opening_hooks` | **Yes** | After the first four-line report scene, `[x150105]` asks why the small screen's position changed, `[x150108]` asks how the two watches relate, and `[x150110]` asks where the business went. These are three unanswered questions that point to later chapters, even though other opening lines spoil some results. |
| `one_thread` | **Yes** | `[x150110]` poses the continuing business problem; `[x150543] 到底分散成什麼樣，哪張表能回答？` carries it into the final financial table, and `[x150635]` gives the resulting mix. The recurring subject is Garmin's dependence on one revenue line and where the income later sits. |
| `no_detour` | **No** | `[x150513] 同年還有入門款自行車紀錄器，供騎士使用。` begins a rapid run of cycling, golf, handheld and tracking products through `[x150517]`; `[x150535–x150536]` and `[x150617–x150620]` add more marine, aviation and outdoor products. These runs read as product catalogues before the revenue mix advances. |

The two Shorts are understandable without the long film. **Short 1** has its own setup (2008 “可能”), turn (2011 “已經”), and payoff that the whole revenue decline cannot be assigned to phones. Its nine spoken beats total 163 characters. The 9:16 reading is **not yet verified**: `x15-b01-s03`, `x15-b04-s17` and `x15-b04-s10` reuse wide compositions and small bar, strip or ring details; the JSON gives no vertical crop or safe-area direction. The short headlines carry the essential figures, but their phone-size placement needs a vertical frame check.

**Short 2** also stands alone: it asks whether the car business still mattered when GPS watches appeared, answers that it still held over half in 2011, then shows the later Fitness/Outdoor share and the other three departments. Its nine beats total 191 characters, so its 25–55-second fit is near the upper edge until audio is measured. The 9:16 reading is **at risk** at `x15-b05-s04` (runner, cyclist and swimmer spread across one frame) and `x15-b06-s21` (five dividers and bars); `2011：GPS 運動錶` and `2025：約 60.9%` are also the longest headlines at 12 characters. These comparisons need vertical crops and legible text checked at phone size.

The repository timeline estimator gives `25,093 / 30 = 836.4` seconds (about 13:56) for the scripted scenes. This is a planning estimate, not TTS or finished-film duration, but it is substantially beyond the series' approximately ten-minute target. No rendered Short, vertical frame, TTS, or final video was available to this review.
