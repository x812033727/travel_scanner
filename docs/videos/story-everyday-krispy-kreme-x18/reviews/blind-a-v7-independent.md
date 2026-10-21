# Krispy Kreme × McDonald’s X18 v7 — independent blind reader A

I read the frozen narration and Shorts before any earlier Krispy Kreme review, author note, or source audit. The input SHA-256 values matched `b62883b6acc5d486c7a329e8458f03b0e070b04b51f547f1fb410abafeb2100f` (`video.json`) and `53423ea2bed98681476de0cff436ff1543c3ac9a98a479c1baff410cc84acfd9` (`shorts.json`). I applied the panel's rule that a single break makes the answer no.

**Long narrative: 88/100. Strict required verdict: FAIL — 11 of 12 required checks are yes.** Q8 fails on a repeated date without a named callback. Q9 is advisory and passes. The pilot-to-exit question gets a clear answer.

## Q1–Q13 ballot

Each evidence field quotes one spoken line with its line ID. The notes below the ballot explain the whole-script judgments.

```json
{
  "answers": [
    {"id":"scene_first","yes":true,"evidence":"[x180101] 想像二〇二四年三月的肯塔基：店員把當天送來的甜甜圈擺上早餐櫃台。"},
    {"id":"no_spoiler","yes":true,"evidence":"[x180107] 六月二十三日，又有一份兩家公司聯名公告；地圖要怎麼改？"},
    {"id":"one_line","yes":true,"evidence":"[x180312] 從十月芝加哥開線到十二月二十九日，年末日曆翻開，這回有實數了。"},
    {"id":"no_toc","yes":true,"evidence":"[x180224] 計畫可以拉得很長，第一個實際開線的城市是哪裡？"},
    {"id":"chapters_link","yes":true,"evidence":"[x180301] 開頭那條十月新線，落在芝加哥。"},
    {"id":"open_loops","yes":true,"evidence":"[x180320] 從店數到整體車線投資，開頭那本帳仍沒揭開：每店需求撐得起每日配送嗎？"},
    {"id":"payoffs","yes":true,"evidence":"[x180513] 還記得那本沒揭開的帳嗎？Krispy Kreme 說，每店需求撐不起每天配送的成本。"},
    {"id":"no_recap","yes":false,"evidence":"[x180610] 七月二日，雙方宣布的終止正式生效。"},
    {"id":"chapters_are_events","yes":true,"evidence":"[x180401] 二〇二五年三月三十日，公司記錄的是超過兩千四百家。"},
    {"id":"outro_no_next","yes":true,"evidence":"[x180682] 訂閱品牌故事，一起看清熟悉品牌背後的生意。"},
    {"id":"opening_hooks","yes":true,"evidence":"[x180107] 六月二十三日，又有一份兩家公司聯名公告；地圖要怎麼改？"},
    {"id":"one_thread","yes":true,"evidence":"[x180680] 還記得那張逾兩千四百家的地圖嗎？這盤能上架，卻沒讓供貨者算得過來。"},
    {"id":"no_detour","yes":true,"evidence":"[x180519] 對一方是菜單一角，對另一方卻是要負擔的配送模式。"}
  ]
}
```

## Six-chapter story trace

1. **Kentucky, March 2024:** A breakfast-counter tray makes the trial concrete. The opening discloses strong pilot demand, then withholds whether daily delivery scales economically (`x180104`), which city begins the wider rollout (`x180105`), why the 2025 timetable changes (`x180106`), what the June joint announcement does (`x180107`), and which account stops the tray (`x180109`). None of those later outcomes is given away.
2. **Pilot to national plan:** The tray is a daily fresh-delivery job in McDonald’s restaurants, not new Krispy Kreme stores. The March agreement sets a phased national target for 2026; route density and capacity are the hoped-for gains, while store-level volume and costs are still unknown. The closing question asks for the first newly opened city (`x180224`).
3. **Chicago to more than 1,900 locations:** Chicago answers that question immediately (`x180301`). The story distinguishes proposed routes from operating ones, and an expected near-2,000 store count from the later actual count. Startup costs and network capital spending appear, but no per-store economics are disclosed. The chapter asks why expansion stops despite a fuller spring map (`x180323`).
4. **More than 2,400, then a pause:** The March 2025 count grows, but the May announcement jointly re-evaluates rollout timing and expects no additional restaurants in Q2. It still supplies existing stores and does not announce termination. The unresolved profitable-model question is carried into the coming joint announcement (`x180416`, `x180422`).
5. **June joint decision:** Both sides decide to end the partnership. McDonald’s says the product and franchise result met its expectations, but Krispy Kreme says per-store demand could not cover daily delivery costs (`x180513`–`x180514`). This directly resolves the opening paradox and the longer-running per-store question. The chapter then asks how the June quarter-end map records stores before the effective exit (`x180520`).
6. **Quarter end to actual exit:** June 29 still includes the collaboration, July 2 is the effective end, and the following quarter records about 2,400 exits and later removal of associated costs. The tray remains a useful closing image because daily delivery continues to other, targeted retail points (`x180613`–`x180614`).

The chapter openings pick up a specific prior object or question: the tray returns to Kentucky, the first new city becomes Chicago, the fuller map gets a March count, the awaited joint announcement states the decision, and the quarter-end map gets its date. Questions also recur before 90 seconds elapse. The largest delayed payoff, the per-store economics, explicitly names its earlier unopened account before providing Krispy Kreme's new answer. The brief third-party-carrier and vehicle-claims material stays attached to the distribution network and separates other costs from this partnership; it does not become a second storyline.

**Q8's break is narrow but real.** `x180502` already gives July 2 as the effective termination date. `x180610` says July 2 again without naming that earlier disclosure. The second line confirms the planned end actually took effect, which advances the chronology and lets Q7 pass, but the date itself is repeated as a fresh answer to `x180608`'s “which day?” question. Under the panel's absolute no-recap rule, that one repeated date makes Q8 no.

## Shorts judged standalone

| Short | Score | Assessment |
| --- | ---: | --- |
| `story-everyday-krispy-kreme-x18-short-1` | **91/100** | The opening states the pilot-success paradox, then supplies the 160-store trial, national plan, daily delivery duty, later 2,400-store scale, and the two companies' different economic views. The supplier's per-store demand-versus-delivery-cost answer resolves the hook without the long video. The 2026 target is clearly a plan rather than a completed rollout. |
| `story-everyday-krispy-kreme-x18-short-2` | **88/100** | The announced-stop-versus-still-counted hook stands on its own: June 29 is the reporting date, July 2 the effective exit. The later global total and explicit warning against treating the whole difference as McDonald’s exits prevent a tempting false subtraction; the Q3 footnote gives the specific exit count. It is number-dense, but the date sequence makes its final answer clear. |

Both Shorts provide their own setup, evidence, and payoff; neither needs the long video's tray metaphor to be understood.
