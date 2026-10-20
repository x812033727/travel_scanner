# X10 eBay／PayPal v7 — narrative review (diagnostic)

**Verdict: FAIL — 11/12 required `NARRATIVE_PANEL` checks are Yes.** `no_recap` is No. The optional `chapters_are_events` check is Yes. This is a read of narration and supplied scene/Shorts metadata, not a source audit or rendered-video/TTS check.

Binding: `video.json` SHA-256 `d0e77292c9b3547c8a34c19a034d1d400b18a157af8ecd846136019c6c398d6d`; `shorts.json` SHA-256 `15fa00305f4ad52d79b05fd9bbf4e0743923330a23f37792d1963c5ed9216a22`. Both hashes matched the files reviewed. The 105 narration lines in `script.md` match the ordered `video.json` line IDs and text exactly. I used the current `NARRATIVE_PANEL` in `tools/video/core/narrative.mjs`, the `brand-story` skill, and its story/script-writing guidance.

**Blinding caveat:** Before reading the frozen script, my search for `NARRATIVE_PANEL` accidentally returned short search-result snippets from several earlier review files because the nested `reviews/` directory was not excluded by the glob. Those snippets included some prior verdict/check labels. I did not open a prior receipt or source audit and did not use those snippets to score v7, but this is **not a clean blind receipt** for the formal two-reader gate.

| Panel ID | Result | Evidence from this script | Reason |
| --- | --- | --- | --- |
| `scene_first` | Yes | `x100101`「想像二〇一八年春天的一筆 eBay 訂單：買家按下付款，賣家等著收錢。」 | The first sentence gives a year, buyer, seller, and action at checkout. |
| `no_spoiler` | Yes | `x100106`「分拆那天，兩家公司還簽下一份營運協議；它留了什麼空間？」 | The opening names the agreement but withholds its terms and the later migration outcome. |
| `one_line` | Yes | `x100301`「十二年後，PayPal 已不是只跟著 eBay 的成交走。」 | After the 2018 teaser, the story advances from the 2002 purchase through the 2014 scale, 2015 separation, and 2018–21 payment migration. |
| `no_toc` | Yes | `x100416`「這個期限還沒走完，eBay 會從哪裡把另一條路接起來？」 | Transitions pose story questions; none announces a chapter plan or list of coming sections. |
| `chapters_link` | Yes | `x100701`「二〇二一年，eBay 把新收款流程帶到前一年尚未覆蓋的市場。」 | This directly continues `x100615`'s unfinished-market question; the other chapter openings likewise pick up the prior consequence or question. |
| `open_loops` | Yes | `x100507`「這條路真的跑起來了，還是只停在工程清單上？」 | The script records 21 setup/payoff pairs. The longest gap between recorded setups is 163 non-punctuation characters, about 39 seconds at 250 characters/minute, well under 90 seconds on a script estimate. |
| `payoffs` | Yes | `x100715`「多年後，它把市集收款流程逐步接回手裡。」 | `x100714` names the opening checkout page before this answer; `x100612`–`x100614` also supply and qualify eBay's stated reason for taking on the flow. The other posed questions receive later particulars, such as the five-year term (`x100410`) and over one million sellers (`x100609`). |
| `no_recap` | **No** | `x100413`「所以分拆的是公司所有權；付款合作還按合約接著走。」 | `x100406` already says separation first changed the shareholder register while PayPal stayed at checkout, and `x100407` says the agreement kept PayPal payment service on eBay. `x100413` repeats that same conclusion without a named callback or new fact. |
| `chapters_are_events` *(optional)* | Yes | Scene `x10-b06-s01` chapter「二〇二〇年，付款合作合約到期」; narration `x100601` states the expiry. | The seven headings identify a dated action, change, or disclosure rather than generic functions such as background or conclusion. |
| `outro_no_next` | Yes | `x100719`「訂閱品牌故事，下一次結帳時，也看看背後是誰在設計這段路。」 | “下一次結帳” is the viewer's next purchase, not a promise about another video. |
| `opening_hooks` | Yes | `x100106`「分拆那天，兩家公司還簽下一份營運協議；它留了什麼空間？」 | After the first checkout scene, `x100105` leaves the split-day payment problem open, `x100106` asks about the agreement, `x100107` asks who controls the route, and `x100108` asks why eBay took it on. These are later answers, not an announced outline. |
| `one_thread` | Yes | `x100716`「股權由誰持有，和結帳流程由誰設計，原來是兩種不同決策。」 | The same eBay checkout-to-seller-payment problem drives the acquisition, separation, contract, and migration. |
| `no_detour` | Yes | `x100713`「所以這集能驗到流程和收入結構改變，不能宣稱分拆讓交易暴增。」 | The business figures test the consequence of changing the checkout flow. The cash-sale clarification distinguishes separation mechanics and stays within the central question. |

The opening contains 169 Han characters and 194 non-punctuation characters including Latin names/numbers. At the script guideline's roughly 250 characters/minute, that is about **41–47 seconds**, inside the 30–60 second target. This is an estimate; there is no TTS measurement. In the eight opening scenes (`x10-b01-s01`–`x10-b01-s08`), the image prompts use generic checkout, folders, and routes with unreadable interfaces. They do not put the contract's terms or final answer on screen early. The opening chapter title at `x10-b01-s01` mentions the 2018 development-list clue that narration gives in `x100102`; whether and when that title is displayed needs a render check.

Both Shorts read as standalone scripts and fit the requested 25–55 second window on the same rough estimate:

| Short | Script estimate | Standalone assessment |
| --- | --- | --- |
| `story-everyday-ebay-paypal-x10-short-1` | 161 non-punctuation characters, about **39 seconds** at 250/minute. | Yes. It asks whether eBay received cash, explains the shareholder distribution, answers no, and explains why PayPal still appeared at checkout. Its first headline asks the question rather than revealing the answer. |
| `story-everyday-ebay-paypal-x10-short-2` | 158 non-punctuation characters, about **38 seconds** at 250/minute. | Yes. It states the split/self-payment puzzle, gives the 2018 start and later rollout, provides eBay's stated product rationale with a caveat, then reaches the 2021 platform-wide status. Its hook headline also remains a question. |

These Shorts reuse main-video scene IDs, but neither requires a viewer to have watched the main video to understand its question and answer. Actual running time and on-screen timing remain unverified until narration and video are rendered.
