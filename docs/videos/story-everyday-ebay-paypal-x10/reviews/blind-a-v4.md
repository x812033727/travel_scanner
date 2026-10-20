# X10 v4 blind narrative review — reader A

**Verdict: FAIL.** Two required `NARRATIVE_PANEL` checks are No: `no_spoiler` and `payoffs`. This is a read of the current narration and both Shorts, without prior reviews or revision history. No manuscript was edited.

Binding: `video.json` SHA-256 `3898814710b0a480835505521beb0faca7a8303c7da9d4079d5d09141c0062b3`; `shorts.json` SHA-256 `4b007288aa79d10ef2b90749f9fd4b349230f8c40b52d45f4c18f9c4b899e70d`; panel rules SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`. The 13 IDs and required flags come from `tools/video/core/narrative.mjs`. The estimated runtime is 10:14; its 45-second cadence check reports no gaps.

| ID | Required | Yes/No | Evidence and judgment |
| --- | --- | --- | --- |
| `scene_first` | Yes | **Yes** | `[x100101]`「一張網路購物結帳頁，買家按下付款，賣家等著收錢。」The next line dates the moment to spring 2018. |
| `no_spoiler` | Yes | **No** | `[x100105]`「分家以後，結帳並沒有立刻換成一條全新的路。」This gives away the interim outcome that chapter four later reveals at `[x100406–x100407]`: PayPal remains in eBay checkout under the agreement. The later contract detail adds *how*, but the opening has already supplied *what happened*. |
| `one_line` | Yes | **Yes** | `[x100301]`「十二年後，PayPal 已不是只跟著 eBay 的成交走。」The story moves from the 2002 payment problem through the separation and the later rollout, with one checkout thread. |
| `no_toc` | Yes | **Yes** | `[x100416]`「這個期限還沒走完，eBay 會從哪裡把另一條路接起來？」This is a story question, not an announcement of the next section. No narration lists the forthcoming chapters. |
| `chapters_link` | Yes | **Yes** | `[x100401]`「二〇一五年，股權分派和付款協議在同一天落地。」It answers the preceding chapter's question about how checkout would continue after separation. The later chapter openings likewise pick up the preceding contract or migration state. |
| `open_loops` | Yes | **Yes** | `[x100507]`「這條路真的跑起來了，還是只停在工程清單上？」Specific unresolved questions or turns recur throughout the body; the estimated 45-second hook-gap check has no warnings. |
| `payoffs` | Yes | **No** | `[x100108]`「eBay 已把 PayPal 拆出去，為什麼又要自己接手收款？」is the title's central question. `[x100717]` finally gives eBay's product claim—more buyer choices and simpler seller operations—but the story never explains why those benefits required *eBay-managed* payments instead of the continuing partner arrangement. The 2018–2021 rollout answers **when and how**; `[x100708–x100710]` describes a later revenue change and explicitly limits attribution. Neither supplies the missing decision cause. |
| `no_recap` | Yes | **Yes** | `[x100501]`「開頭那份二〇一八年季報，只把付款中介列為開發中的能力。」This names the opening document as a callback, then distinguishes a development priority from the actual start of mediation at `[x100505]`. The spoken 2018 reprise meets the panel's callback exception. |
| `chapters_are_events` | No | **Yes** | The title「二〇二〇年，付款合作合約到期」marks the event spoken at `[x100601]`, and the other chapter names similarly use dated changes or discoveries rather than generic functions. |
| `outro_no_next` | Yes | **Yes** | `[x100719]`「訂閱品牌故事，下一次結帳時，也看看背後是誰在設計這段路。」“下一次結帳” means the viewer's next checkout, not a later video. |
| `opening_hooks` | Yes | **Yes** | `[x100106]` asks what room the operating agreement left, `[x100107]` asks who controls the route, and `[x100108]` asks why eBay takes payments back. These are three questions after the opening checkout moment. |
| `one_thread` | Yes | **Yes** | `[x100714]`「開頭那張結帳頁，eBay 先讓支付公司獨立。」The same buyer-to-seller checkout difficulty connects the acquisition, separation, contract and migration. |
| `no_detour` | Yes | **Yes** | `[x100506]`「這不是再買回 PayPal，而是替自家市集建立收款流程。」The no-buyback clarification is brief and relevant to separating company ownership from payment routing. The cash-distribution explanation likewise serves that distinction. |

The 2018 development fact still appears in both the opening chapter title and the fifth chapter title. This is a repeated **card-level heading**, although the spoken `[x100501]` is an explicit callback and therefore passes `no_recap`. The 2020 expiry card's label,「不等於付款選項立刻消失」at `x10-b06-s01`, also reveals the later clarification at `[x100706]` ahead of its narration. The opening prompt for `x10-b01-s05` depicts two payment paths already connected by a bridge; it reinforces the spoken spoiler at `[x100105]`. I found no opening title, card or prompt that reveals the final 2021 migration result.

**Short 2 needs a standalone opening and connective tissue.** Its first beat starts with the technical filing fact「把付款中介能力列進產品開發重點」; the split-with-PayPal contradiction only appears in beat two. Later,「這之後，自管付款繼續往更多市場擴張」has no stated antecedent for the expired 2020 agreement because that event was omitted from the Short. Its alternate “為何” title promises a cause, while the cut ends with the distinction between share ownership and checkout design. Short 1's cash-sale question and answer work on their own.

The outro has exactly three lines: `[x100717]` offers an answer, `[x100718]` asks a viewer-answerable comment question, and `[x100719]` gives a story-related reason to subscribe. Its structure passes; the first line's causal answer is the unresolved narrative issue above.
