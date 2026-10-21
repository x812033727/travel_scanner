# Uber X19 v6 — blind reader A

I read the frozen narration as one zh-TW story, then judged each panel question under the rule that one break is a **no**. I did not consult prior reviews, a treatment, sources, or other readers. The input SHA-256 values were `a3149c4904182bf473a7d452c3e5a80de790402c4b240e10da4b2610e1dfbaf8` (`video.json`) and `b6b0212372d776c96572450baa8e9c4350499c72923d088ad0bd6833e8681d95` (`shorts.json`).

**Long-form narrative score: 84/100. Strict panel verdict: FAIL (12 yes, 1 required no).** The chronology and question/payoff chain work. The failure is a repeated, uncued deal-status fact, not an unanswered opening promise. Q9 is advisory.

## Panel ballot

Each evidence field quotes one spoken line with its line ID. The explanatory notes below the ballot address the checks that require more than one line to assess.

```json
{
  "answers": [
    {"id":"scene_first","yes":true,"evidence":"[x190101] 二〇二〇年春，路邊一輛車停下；司機拿起手機，改等一只餐袋。"},
    {"id":"no_spoiler","yes":true,"evidence":"[x190107] 年底，兩張配送地圖挪到同一張桌上，中間那條接線被遮住。"},
    {"id":"one_line","yes":true,"evidence":"[x190401] 開場桌上那張還沒接入的外送網，是 Postmates；七月六日優步才簽約，六月季度早已結束。"},
    {"id":"no_toc","yes":true,"evidence":"[x190222] 司機開始改接餐袋，整個平台的金額真會換位嗎？"},
    {"id":"chapters_link","yes":true,"evidence":"[x190301] 六月季報揭曉：外送訂單額真的高過載客。"},
    {"id":"open_loops","yes":true,"evidence":"[x190413] 車回來一截，兩條路哪邊先留下部門利潤？"},
    {"id":"payoffs","yes":true,"evidence":"[x190317] 開場那只餐袋雖跑在前，外送部門調整後 EBITDA 仍虧兩點三二億美元。"},
    {"id":"no_recap","yes":false,"evidence":"[x190421] 收購仍只是紙上的約定，另一套 App 還沒有接進來。"},
    {"id":"chapters_are_events","yes":true,"evidence":"[x190501] 開場還留在桌上的第二張網，十二月一日才因 Postmates 收購完成進到優步。"},
    {"id":"outro_no_next","yes":true,"evidence":"[x190627] 想看熟悉品牌的轉折究竟由哪筆帳撐住，歡迎訂閱品牌故事。"},
    {"id":"opening_hooks","yes":true,"evidence":"[x190107] 年底，兩張配送地圖挪到同一張桌上，中間那條接線被遮住。"},
    {"id":"one_thread","yes":true,"evidence":"[x190613] 回到路邊，那位示意司機又接到乘客；同一支手機另一側仍有餐袋取件路線。"},
    {"id":"no_detour","yes":true,"evidence":"[x190616] 外送也增加百分之六；兩條路都長大，車道長得更快。"}
  ]
}
```

## Six-chapter trace

1. **April 2020:** A driver waits for a meal instead of a rider. The opening withholds whether delivery overtakes rides, earns money, how a second network joins, and whether rides recover. Its later-moment hooks are the June profit question (`x190105`), July's unnamed network (`x190106`), the hidden year-end connection (`x190107`), and a possible ride recovery (`x190108`).
2. **The earlier baseline:** The narration steps back to 2019 after that teaser, when ride bookings dominate, then follows 2020 Q1 toward a shrinking ride market. Driver access, restaurants, and market exits make the two-sided delivery network concrete. The last question asks whether its *platform bookings* really switch places (`x190222`).
3. **2020 Q2 crossing:** The very next line answers yes (`x190301`). The script separates gross bookings from revenue, shows that overall demand shrank, and answers the opening profit question with a negative delivery adjusted EBITDA (`x190317`). It ends by asking whether the second delivery network caused the crossover (`x190323`).
4. **July agreement and 2020 Q3:** The first line identifies Postmates and dates the agreement after June (`x190401`), so it cannot account for the Q2 crossover. Q3 bookings still favor delivery before the acquisition closes. The chapter shows ride recovery and delivery's continuing loss, then asks whether the two networks finally join at year-end (`x190422`).
5. **December close, later migration:** The acquisition closes, but the consumer apps still run separately; 2021 Q2 brings the cited user, courier, and merchant migration. Delivery still leads in bookings and remains negative on its department measure. The close asks when that measure turns positive (`x190522`).
6. **2021–22 outcomes:** 2021 Q4 delivery adjusted EBITDA turns positive (`x190601`). By 2022 Q4 ride gross bookings regain the lead (`x190611`), while both businesses have grown and both department measures are positive (`x190625`). The road/phone image from the opening returns (`x190613`).

All explicit opening promises receive a distinct answer: the June delivery lead is **not** June delivery profit; the second network is Postmates, signed in July and closed in December; migration is later than closing; and ride bookings lead again in 2022 Q4. The film does not claim an unsupported exact contribution from driver switching or Postmates. That restraint makes the answer to its title more credible: ride bookings collapsed while an existing delivery network grew, and the later acquisition cannot be retroactive cause.

Chapter handoffs have a specific object or answer: the opening phone/meal leads to the earlier network, Q2 answers the bookings question, July answers the Postmates-causation question, December answers the joining question in stages, and 2021 Q4 answers the department-profit question. I found no 90-second stretch without a live question or turn. The iOS and grocery passage is brief and still concerns the delivery path on the same platform; it is not a separate storyline or a readout of an unrelated list.

The strict Q8 failure is local but clear. `x190412` already says July's deal had not closed during Q3; `x190421` says again that the acquisition is only a paper agreement. `x190405` had also said signing was not integration. `x190421` adds the separate-App detail, but its first clause repeats the pending-deal fact without a named callback. The other repeated mentions either supply a new quarter/result or explicitly recall an opening object.

## Shorts, judged standalone

| Short | Score | Standalone verdict |
| --- | ---: | --- |
| `story-everyday-uber-x19-short-1` | **89/100** | Complete. Its opening asserts the 2020 Q2 bookings crossover; it then distinguishes platform bookings, company revenue, and the two departments' adjusted EBITDA. The negative delivery figure gives the promised answer. The last line is memorable, although the word “獲利” depends on the earlier explicit adjusted-EBITDA label to keep the metric precise. |
| `story-everyday-uber-x19-short-2` | **92/100** | Complete. The Q2 crossover precedes the July 6 Postmates agreement, Q3 still favors delivery before closing, and December 1 closing and separate apps make the chronology unambiguous. It answers its acquisition-causation hook without needing the long video. “六月季度結束時” should be heard as a completed quarter's bookings, as the narration's surrounding dates indicate. |

Both Shorts supply their own setup, turn, evidence, and payoff. Neither relies on the long video's opening metaphor or an unstated future segment to answer its hook.
