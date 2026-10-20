# X10 v5 independent blind narrative review

**Verdict: PASS — 12/12 required NARRATIVE_PANEL checks; optional chapter-title check also passes.** This is a script and metadata review, not a rendered-audio timing measurement. I read only the frozen `video.json`, `shorts.json`, `script.md`, and the `NARRATIVE_PANEL` rubric in `tools/video/core/narrative.mjs`; I did not consult earlier reviews or other readers.

| Frozen file | SHA-256 | Match |
| --- | --- | --- |
| `video.json` | `f3d24233b82f41379b5126a06fcec8f9ec7759a17b403b2fa5a58a27b80f9bb4` | Yes |
| `shorts.json` | `b7a3d36dc11ec780b65089b2fca1167893e06ba771ed912e578ae94a30a49d6e` | Yes |

## Panel verdict

| Criterion | Verdict | Line evidence and reason |
| --- | --- | --- |
| `scene_first` | YES | [x100101]「一張網路購物結帳頁，買家按下付款，賣家等著收錢。」The first sentence puts the buyer and seller in a concrete checkout action; [x100102] dates the moment to spring 2018, within the first four sentences. |
| `no_spoiler` | YES | [x100106]「分拆那天，兩家公司還簽下一份營運協議；它留了什麼空間？」The opening names the agreement but withholds its terms. It also withholds whether the new route worked and why eBay chose it. The stated separation is the premise, not the later answer. |
| `one_line` | YES | [x100501]「開頭那份二〇一八年季報，只把付款中介列為開發中的能力。」After the preview, the account runs 2002 → 2014 → 2015 → 2018 → 2020 → 2021 and explicitly rejoins the preview here. It follows the same buyer-to-seller payment route. |
| `no_toc` | YES | [x100514]「新路已上線，舊協議卻還沒走到終點。」This sets up an unresolved event, rather than announcing a coming section or enumerating the video's structure. The script has no chapter itinerary or numbered preview. |
| `chapters_link` | YES | [x100615]「但當時還有市場和交易，尚未完成遷移。」→ [x100701]「二〇二一年，eBay 把新收款流程帶到前一年尚未覆蓋的市場。」The other first-line links are audited below. |
| `open_loops` | YES | [x100507]「這條路真的跑起來了，還是只停在工程清單上？」Questions, turns, and consequences recur well inside the rubric's 90-second ceiling. The tighter 30–45-second cadence is estimated below. |
| `payoffs` | YES | [x100106] asks what the agreement left open; [x100414]「條文也限制 eBay 何時能自己擔當收款交易角色。」and [x100415]「不過，合約並非完全不准它做小範圍測試。」provide new terms. The other delayed and adjacent payoffs are identified below. |
| `no_recap` | YES | [x100714]「開頭那張結帳頁，eBay 先讓支付公司獨立。」This is an explicit callback to the opening; [x100715] advances it to eBay's later control of the checkout route. The 2014 figures are a total, its subset, and a derived percentage, not repeated measures. |
| `outro_no_next` | YES | [x100719]「訂閱品牌故事，下一次結帳時，也看看背後是誰在設計這段路。」“下一次結帳” means the viewer's next checkout, not a next episode. |
| `opening_hooks` | YES | [x100105]「分拆生效那天，買家還要付款，賣家還在等著收錢。」After the first scene, [x100105], [x100106], [x100107], and [x100108] each leave a distinct later question open; their payoffs appear below. |
| `one_thread` | YES | [x100202]「成交只是第一步；那筆款項還得另走一段路才會抵達。」The difficulty of moving a buyer's payment to a seller carries through acquisition, separation, contract, self-managed checkout, and completed migration. |
| `no_detour` | YES | [x100307]「它只說明：PayPal 處理的付款，多數已發生在 eBay 交易之外。」The three adjacent 2014 numbers establish this single change in the payment route; the later financial figures test its outcome. There is no unrelated product or opinion list. |
| `chapters_are_events` (optional) | YES | [x100401]「二〇一五年，股權分派和付款協議在同一天落地。」The chapter titles likewise name actions or reveals: purchase, payment-flow disclosure, share distribution, development, contract expiry, and migration. |

The chapter first lines connect as follows: opening checkout and the “why take payments back?” question [x100101, x100108] → the earlier buyer/seller payment problem [x100201]; PayPal's possible growth beyond eBay [x100217] → its position twelve years later [x100301]; how payment would continue after separation [x100315] → the same-day payment agreement [x100401]; where the new route would begin during the contract [x100416] → the opening's 2018 filing [x100501]; what happens at the original term's end [x100515] → the July 2020 expiry [x100601]; unfinished markets [x100615] → the 2021 rollout [x100701]. Each first sentence supplies the prior question's next event or a recognizable earlier cause.

The opening's deferred moments pay off with new information: the 2018 development item [x100102] becomes actual payment intermediation [x100505]; the separation-day payment need [x100105] is met by PayPal continuing on the marketplace under the agreement [x100407]; the agreement's room [x100106] becomes the restriction and limited-test exception [x100414–x100415]; who manages checkout [x100107] becomes eBay's platform-wide management by the end of 2021 [x100703–x100704]; and why eBay took it on [x100108] gets eBay's stated full-flow, buyer-choice, and seller-convenience rationale, with its evidentiary limit [x100612–x100614]. The opening's “three years ago” separation [x100103] also gains the share-distribution mechanism and completion date [x100402–x100403].

The remaining questions have visible answers: email-based payment [x100206→x100207–x100208], old eBay payment service [x100210→x100211–x100212], PayPal's reach outside eBay [x100217→x100303–x100307], the on-eBay share [x100302→x100303–x100305], the board's change [x100308→x100310–x100313], post-separation payment [x100315→x100401–x100407], cash from separation [x100404→x100405], agreement duration [x100409→x100410], 2018 route during the original term [x100416→x100501–x100505], working adoption [x100507→x100508–x100513], scale after expiry [x100515→x100609], sellers on the new route [x100608→x100609], remaining markets [x100615→x100701–x100703], financial result [x100707→x100708–x100710], and merchandise volume [x100711→x100712]. Some `video.json` loop payoff IDs mark the **start** of a multi-line answer; the immediately following lines supply the answer rather than merely restating the question.

## Cadence, spoilers, and Shorts

The body has a question, consequential turn, or chapter turn about every 3–7 scenes. A reading-speed proxy of 3.5–4 spoken Chinese character units per second plus about 0.8 seconds per scene puts the longest clear spans at roughly **38–42 seconds**: [x100302→x100308], [x100501→x100507], and [x100701→x100707]. The stretch after [x100507] is interrupted by the old-agreement/new-route tension at [x100514] before the next question [x100515]. This supports the requested 30–45-second hook cadence as well as the panel's 90-second limit. The script states there is no measured TTS, so these are estimates, not certified runtimes.

The opening's eight scenes use `shot` prompts without result-bearing text cards; its thumbnail asks “又收款？” The later chapter titles announce the current event, not the withheld reason or result. The statistic cards appear alongside the lines that disclose their numbers. The opening and Short hooks show an unresolved checkout or separated offices; no prompt or early headline gives away the cash, contract, product-reason, or migration answer ahead of its spoken beat.

**Short 1: PASS, standalone.** Its spoken hook asks whether the separation gave eBay sale cash [x100404]. The share distribution [x100402] and explicit “沒有…出售現金” [x100405] answer it, then the agreement [x100413, x100407] explains why payment continued. The cash-drawer prompt and “eBay 沒收到出售現金” headline occur on the proof beat, where the answer is spoken. Six beats contain about 124 normalized spoken character units, an estimated **29–40 seconds** under the same pacing range.

**Short 2: PASS, standalone.** The spoken hook asks why eBay self-managed after separation [x100108]. It says the work **began in 2018** [x100505], adoption increased in **2019** [x100508], expansion continued after the original agreement expired [x100602], and eBay managed payments across platform transactions by **the end of 2021** [x100703]. The stated reason is more buyer payment choice and simpler seller operations [x100613]; [x100614] correctly limits that to eBay's product claim, without asserting that a partner could not do it. The contract-expiry beat leaves the exact expiry year implicit, but the start and platform-wide endpoint answer the “when” title. Seven beats contain about 158 normalized spoken character units, an estimated **37–51 seconds**. Its hook image and headline pose the question; answer-bearing cards arrive with their narration.
