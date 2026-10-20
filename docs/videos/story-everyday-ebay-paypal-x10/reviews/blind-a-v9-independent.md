# X10 v9 independent blind narrative read — A

**Verdict: RETURN FOR NARRATIVE REVISION.** Ten of twelve required `NARRATIVE_PANEL` checks pass. `chapters_link` and `no_recap` fail on the exact spoken text. The optional `chapters_are_events` check passes. This is an independent read of only `video.json`, `shorts.json`, and the `NARRATIVE_PANEL` contract in `tools/video/core/narrative.mjs`; it is not a fact/source audit or a rendered-audio timing test.

## Frozen inputs

| File | SHA-256 at start | SHA-256 at end |
| --- | --- | --- |
| `docs/videos/story-everyday-ebay-paypal-x10/video.json` | `f5c7ec99142c4508d06ef58c8e5e0c136bd7e556a4254dba940d4328f804757c` | `f5c7ec99142c4508d06ef58c8e5e0c136bd7e556a4254dba940d4328f804757c` |
| `docs/videos/story-everyday-ebay-paypal-x10/shorts.json` | `27eb3c634095994f1f97dfbb549d2019d1c082257f28cbd59e1226c64fb7186b` | `27eb3c634095994f1f97dfbb549d2019d1c082257f28cbd59e1226c64fb7186b` |

## Required panel (12 of 12 scored)

| Check | Answer | Spoken evidence and reason |
| --- | --- | --- |
| `scene_first` | **YES** | `[x100101] 想像二〇一八年春天的一筆 eBay 訂單：買家按下付款，賣家等著收錢。` The first sentence gives a year, a buyer, a seller, and an action in a specific checkout moment. |
| `no_spoiler` | **YES** | `[x100106] 分拆那天，兩家公司還簽下一份營運協議；它留了什麼空間？` The opening gives the split as the premise and names the agreement, but withholds what it permits and what the 2018 effort becomes. `[x100102]` stops at a development priority, before rollout. |
| `one_line` | **YES** | `[x100301] 十二年後，PayPal 已不是只跟著 eBay 的成交走。` After the 2018 teaser, the account advances from 2002 acquisition through PayPal's wider business, 2015 separation, and 2018–21 payment migration. Later references to the opening are callbacks rather than a second timeline. |
| `no_toc` | **YES** | `[x100210] 股票換股票收購之後，eBay 原本的付款服務怎麼辦？` The forward cues are questions about events or decisions. No spoken line announces a list or the video's chapter plan. |
| `chapters_link` | **NO** | `[x100515] 當原本的期限結束，這條新路能接住多少人？` leads to `[x100501] 開頭那份二〇一八年季報，只把付款中介列為開發中的能力。` The first sentence of the next chapter restates the opening's 2018 development status (`[x100102]`), rather than answering or advancing the just-left question about capacity at the agreement's expiry. `[x100502]` and `[x100503]` move toward the agreement only afterward. The rule explicitly tests each chapter's **first** sentence. |
| `open_loops` | **YES** | `[x100217] 為 eBay 加速的工具，會不會長得比 eBay 還遠？`, `[x100315] 如果把支付公司拆開，eBay 上的收款要怎麼繼續？`, `[x100416] 這個期限還沒走完，eBay 會從哪裡把另一條路接起來？`, `[x100515] 當原本的期限結束，這條新路能接住多少人？`, and `[x100615] 但當時還有市場和交易，尚未完成遷移。` keep the central question active. Each body chapter also has closer local questions; no estimated body stretch reaches 90 seconds without a question, turn, or withheld result. |
| `payoffs` | **YES** | `[x100217]` is answered by `[x100303]`–`[x100307]` (the outside-eBay majority); `[x100315]` by `[x100401]` and `[x100407]` (the operating agreement and continued PayPal service); `[x100515]` by `[x100609]` (over one million active sellers); `[x100615]` by `[x100701]`–`[x100703]` (remaining markets and eventual platform-wide management). The longer returns name the same company, agreement, checkout, or remaining markets and add a new result. |
| `no_recap` | **NO** | `[x100415] 不過，合約並非完全不准它做小範圍測試。` and `[x100503] 協議的例外條款，容許第三年後在有限地區小規模測試。` state the same permission twice. The second line adds timing and geography, but repeats the already-given fact that small tests were allowed and does not explicitly call it back. This is an especially visible repeat across the 2015→2018 boundary. By contrast, `[x100501]` explicitly says `開頭那份`, which marks its repeated 2018 report fact as a callback. |
| `outro_no_next` | **YES** | `[x100719] 訂閱品牌故事，下一次結帳時，也看看背後是誰在設計這段路。` The phrase `下一次結帳時` means the viewer's next checkout, not a promised next video. The other two outro lines answer and invite a comment. |
| `opening_hooks` | **YES** | After `[x100101]`, the opening raises at least three distinct unresolved developments: `[x100102]` leaves whether the 2018 payment-intermediation priority reaches real transactions; `[x100106]` asks what space the operating agreement leaves; `[x100107]` asks who ultimately controls the payment path. `[x100108]` states the larger why-question. The script later resolves these through `[x100505]`/`[x100508]`, `[x100414]`/`[x100415]`, and `[x100703]`/`[x100704]`. |
| `one_thread` | **YES** | `[x100201] 二〇〇二年，買家在 eBay 拍下一件商品，賣家面前還放著待寄的包裹。` revisits the same buyer-to-seller payment problem introduced by `[x100101]`. `[x100714] 開頭那張結帳頁，eBay 先讓支付公司獨立。` explicitly returns to it near the end. The PayPal volume, agreement, migration, and final financial evidence all bear on ownership or operation of that checkout path. |
| `no_detour` | **YES** | `[x100707] 那麼，把流程接回來，財報裡有留下什麼？` ties the last financial section to the payment migration, and `[x100713]` bounds what the numbers can establish. The country names in `[x100603]` and `[x100610]` are brief migration milestones, not a separate product/score list. |

## Optional chapter-title check

`chapters_are_events`: **YES.** The seven chapter titles name acquisitions, a payment-flow reveal, a share distribution, intermediation becoming a development priority, agreement expiry, and migration into the last markets. The closest case is `二〇一四年，年報攤開付款流向`; it describes the reveal of PayPal's on-eBay share, rather than a generic “background” or “what the file says” section. The 2018 titles overlap in subject, but each names a dated event or status, not a chapter function.

## Chapter handoffs checked individually

| Boundary | Read |
| --- | --- |
| `[x100108]` → `[x100201]` | Acceptable teaser reset: the 2002 buyer and waiting seller instantiate the checkout difficulty from `[x100101]`. |
| `[x100217]` → `[x100301]` | Clear payoff: the question about PayPal growing beyond eBay becomes its 2014 wider payment volume. |
| `[x100315]` → `[x100401]` | Clear continuation: the question about post-split payments reaches the named operating agreement. |
| `[x100416]` → `[x100501]` | **Fails:** the prior question asks where the new path begins during the agreement term; the next first line repeats the opening's product-list status before the agreement or live rollout advances. |
| `[x100515]` → `[x100601]` | Acceptable: the agreement's July 2020 expiry begins the answer, followed by migration and the active-seller count at `[x100609]`. |
| `[x100615]` → `[x100701]` | Clear continuation: the remaining markets become the next year's migration target. |

## Opening, body, and Shorts

The opening has eight spoken lines (`[x100101]`–`[x100108]`). A text-only pace estimate gives **about 47–52 seconds**, inside 30–60 seconds. It starts in a concrete checkout moment, raises the 2018 development, agreement-space, and control questions, and withholds their outcomes. The split itself is stated early because it is the episode's premise; the mechanics and continuing payment arrangement arrive later.

The body has 1,880 approximate spoken syllable units after substituting two Mandarin syllables for each “eBay” and “PayPal,” plus about 62 seconds of conservative punctuation pauses. At 4.0–4.5 units per second this is **about 8:52–8:00** before visual transitions. An **eight-minute body is plausible**, particularly with the specified slower delivery of dates and dollar figures, but this is not a measured voice render. The full narration including opening and outro is roughly 9:07–10:07 by the same method.

| Short | Estimated spoken duration | Standalone antecedent and payoff |
| --- | --- | --- |
| `story-everyday-ebay-paypal-x10-short-1` | About 34–38 seconds at 4.0–4.5 units/s, with punctuation; about 43 seconds at 3.5 units/s. | **PASS.** The hook names PayPal, eBay, independent listing, and a cash-sale question. The one-for-one stock distribution explains the mechanism; the direct answer says eBay received no sale cash. The agreement line supplies the immediate checkout consequence. |
| `story-everyday-ebay-paypal-x10-short-2` | About 39–44 seconds at 4.0–4.5 units/s; about 49 seconds at 3.5 units/s. | **PASS.** The title names the companies and the first two beats identify platform, payment company, and continued checkout. The 2018 start and wider migration lead to a 2021-end payoff that eBay managed platform payments. The benefit claim is clearly marked as eBay's claim and then qualified. |

The timing model counts spoken Chinese characters and treats brand names as their two-syllable Mandarin readings; it adds small pauses for punctuation. It is a plausibility check only. No script, source receipt, or production asset was edited, and no paid service was called.
