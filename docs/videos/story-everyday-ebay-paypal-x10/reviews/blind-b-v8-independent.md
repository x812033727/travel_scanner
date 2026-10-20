# X10 v8 independent blind narrative read — B

Read 2026-10-20. Scope: the spoken `video.json` and `shorts.json` scripts, judged against `NARRATIVE_PANEL` in `tools/video/core/narrative.mjs`. I did not consult earlier reviews, production receipts, or sources, and did not change either script. The estimates below are readings of text, not measured voice or rendered runtimes.

## Frozen input

| Input | SHA-256 at start | SHA-256 at end |
|---|---|---|
| `video.json` | `3f20fbcf4fa8143b21b227ea12a629c39d6ec2929999c95bffde67a57392a73d` | `3f20fbcf4fa8143b21b227ea12a629c39d6ec2929999c95bffde67a57392a73d` |
| `shorts.json` | `dde413de5eac00fd74c6ab6b200a60f92e05bc454ce29de7ce6453552ea17ff1` | `dde413de5eac00fd74c6ab6b200a60f92e05bc454ce29de7ce6453552ea17ff1` |

## Long video panel

**Verdict: YES on all 12 mandatory questions; YES on the optional chapter-title question.** This is a text-only narrative verdict. Short 1 has a separate standalone defect below, so the two-Short package needs a small script revision.

| Panel ID | Verdict | Spoken evidence and reading |
|---|---|---|
| `scene_first` | YES | `[x100101]` “想像二〇一八年春天的一筆 eBay 訂單：買家按下付款，賣家等著收錢。” The first sentence supplies a year, an order, two participants and an action. |
| `no_spoiler` | YES | `[x100102]` “就在那個春天，eBay 把付款中介能力列進產品開發重點。” Development is planted before the later question of whether it processed real payments; `[x100106]` asks what the 2015 agreement allowed without saying the answer. The split itself is the premise, while its mechanism and the later control of payments remain unrevealed. |
| `one_line` | YES | `[x100201]` “二〇〇二年，買家在 eBay 拍下一件商品，賣家面前還放著待寄的包裹。” After the 2018 teaser, the story returns to the earlier version of the same buyer-to-seller payment problem, then proceeds through 2002, 2014, 2015, 2018, 2020 and 2021. |
| `no_toc` | YES | `[x100416]` “這個期限還沒走完，eBay 會從哪裡把另一條路接起來？” This points to a concrete contractual interval and unresolved payment route. The narration does not announce an upcoming section plan. |
| `chapters_link` | YES | `[x100401]` “開頭那份營運協議，隨著股權分派成了兩家獨立公司的付款契約。” This answers the prior chapter's `[x100315]` question about how eBay payments would continue after separation. See the chapter handoff audit below. |
| `open_loops` | YES | `[x100515]` “當原本的期限結束，這條新路能接住多少人？” A consequential question remains open across the 2020 turn. Other open turns appear at `[x100217]`, `[x100315]`, `[x100416]`, `[x100615]` and `[x100707]`; none of the body reads as a 90-second stretch with no question, escalation, or chapter turn at plausible narration speed. |
| `payoffs` | YES | `[x100609]` “年底，活躍於自管付款的賣家超過一百萬。” This supplies a new magnitude for `[x100515]`, after the contract expiration and phased migration. The other significant questions receive new facts, as mapped below. |
| `no_recap` | YES | `[x100501]` “開頭那份二〇一八年季報，只把付款中介列為開發中的能力。” Its explicit “開頭那份” calls back to `[x100102]` and adds the distinction between a development priority and live processing. The closing `[x100714]` likewise names the opening checkout before summarizing the completed route. I find no unmarked reuse of the same figure or fact that adds nothing. |
| `outro_no_next` | YES | `[x100719]` “訂閱品牌故事，下一次結帳時，也看看背後是誰在設計這段路。” “下一次結帳” means the viewer's next checkout, not the next video. |
| `opening_hooks` | YES | After the opening scene, `[x100105]` suspends the split-day buyer/seller payment; `[x100106]` asks what room the agreement kept; `[x100107]` asks who could decide the payment route. `[x100102]` also plants the 2018 development-to-live-payment question. These are at least three later moments/questions, rather than a list of coming chapters. |
| `one_thread` | YES | `[x100202]` “成交只是第一步；那筆款項還得另走一段路才會抵達。” The payment route from checkout to seller persists through acquisition, separation, the operating agreement and eBay's managed-payments rollout. `[x100716]` closes on the same distinction between owning PayPal and designing checkout. |
| `no_detour` | YES | `[x100607]` “商家與個人賣家的遷移，是兩個不同節點。” The market and seller details explain how the payment route was migrated; the figures later distinguish processed volume, revenue and marketplace transaction value. The country names at `[x100603]` and `[x100610]` are slightly list-like and could be compressed for pace, but they remain part of the rollout rather than a separate topic. |
| `chapters_are_events` (optional) | YES | `[x100601]` “二〇二〇年七月，兩家公司那份 PayPal 營運協議到期。” Its chapter title, “二〇二〇年，付款合作合約到期,” names an event. The other titles likewise name the acquisition, split, reporting disclosure, development milestone or migration. |

### Chapter handoffs and promised answers

- Opening 2018 checkout → 2002 origin: `[x100201]` returns to a buyer, seller and unfinished payment, so the flashback has an intelligible connection to `[x100101]` and `[x100108]`.
- 2002 → 2014: `[x100217]` asks whether the eBay payment tool grew beyond eBay; `[x100301]` answers that twelve years later PayPal was no longer carried only by eBay transactions. `[x100303]`–`[x100307]` gives the proportion and its meaning.
- 2014 → 2015: `[x100315]` asks how payment would continue if PayPal were split; `[x100401]` names the operating agreement as the new contract, and `[x100406]`–`[x100408]` says PayPal service continued.
- 2015 → 2018: `[x100416]` asks where a second payment route could start before the five-year term ended. `[x100501]` points back to the 2018 development disclosure; `[x100503]` explains limited testing room, and `[x100505]` establishes that eBay began intermediating payments in 2018. The first line is a deliberate callback with a new qualification (“only” in development), not a bare label.
- 2018 → 2020: `[x100515]` asks how many sellers the new route could carry at the end of the initial agreement. `[x100601]` supplies the expiration event, then `[x100609]` gives the new answer: more than one million active sellers.
- 2020 → 2021: `[x100615]` leaves markets and transactions unfinished; `[x100701]` continues into uncovered markets, `[x100702]` says market migration was complete, and `[x100703]` says eBay managed payments for platform transactions by the end of 2021.
- Later financial question: `[x100707]` asks what appears in the accounts; `[x100708]`–`[x100710]` gives a revenue increase and expressly limits attribution. `[x100711]` asks whether merchandise volume grew along with revenue; `[x100712]` answers that it was roughly flat.

The delayed opening hooks receive identifiable callbacks: `[x100103]` is developed through the share distribution at `[x100402]`–`[x100403]`; `[x100105]` receives the agreement mechanism at `[x100407]`; `[x100106]` receives the limited-test answer at `[x100414]`–`[x100415]`; `[x100107]` receives eBay's later control at `[x100703]`–`[x100704]`. The core “why split, then self-manage?” question at `[x100108]` is answered in stages by the 2014 separation rationale `[x100312]`–`[x100313]`, eBay's 2020 product rationale `[x100612]`–`[x100614]`, and the ownership-versus-checkout distinction `[x100716]`.

### Length and opening

The opening has eight spoken lines and 169 Han characters before the 2002 chapter. With the repeated English brand names, its questions and pauses, about **45–58 seconds** is a plausible read; it fits a 30–60 second hook, though a particularly slow performance should be timed. It states the 2015 split as premise but withholds how payment continued and who later controlled the flow.

The body after the opening and before the outro has 94 spoken lines, 1,754 Han characters, and 238 Latin letters. At roughly 220–230 spoken Han characters per minute, those Han characters alone take 7.6–8.0 minutes; brand names, punctuation, transitions and number delivery can put the body beyond **8 minutes**. Thus ≥8 minutes is plausible, not certified without timed narration. The 2020 country enumerations `[x100603]` and `[x100610]` are the clearest potential pace drag.

## Shorts as standalone narration

| Short | Verdict | Length and narrative judgment |
|---|---|---|
| `short-1` | **NO — standalone referent** | Six spoken lines, 106 Han characters: roughly 30–42 seconds at ordinary narration pace, within 25–55. The cash-sale hook is answered. But its fifth narration line, shot `x10-b04-s07`, copied from long-script `[x100407]`, says “那份協議，讓 PayPal 的付款服務繼續留在 eBay 市集。” No preceding spoken Short line has introduced **any agreement**. The prior line, shot `x10-b04-s05` / `[x100405]`, answers the cash question; the third line, shot `x10-b04-s06` / `[x100406]`, says only that PayPal stayed in checkout. The fifth card's headline names an operating agreement at the same moment, but the spoken “那份” still has no prior referent. The sixth line repeats “協議” without repairing the missing antecedent. Name the 2015 operating agreement in the fifth spoken line, or introduce it before that line. |
| `short-2` | **YES** | Seven spoken lines, 140 Han characters: roughly 40–52 seconds, within 25–55. The first question about control is answered by the 2018 start and the 2021 completion (`[x100505]`, `[x100703]` in the long script). “這些好處” in its sixth line clearly points to the buyer/seller claims in its fifth. Its first line omits company names, but the second supplies PayPal and eBay before any company-dependent answer. |

## Disposition

The long narration passes the 12 required panel questions on this independent text read, with the optional titles also passing. The package is **revise** because Short 1 uses an unintroduced “那份協議.” This is a one-line clarity fix; the estimated lengths need measured narration for final duration confirmation.
