# Independent blind narrative read — eBay/PayPal X10 v8

Scope: I read only `video.json`, `shorts.json`, and the `NARRATIVE_PANEL` questions and instructions in `tools/video/core/narrative.mjs`. I did not read prior reviews, receipts, sources, or production history, and I did not edit either script. This is a reading of the spoken narration; factual claims have not been independently checked.

## Frozen inputs

| Script | SHA-256 at start | SHA-256 at end |
| --- | --- | --- |
| `video.json` | `3f20fbcf4fa8143b21b227ea12a629c39d6ec2929999c95bffde67a57392a73d` | `3f20fbcf4fa8143b21b227ea12a629c39d6ec2929999c95bffde67a57392a73d` |
| `shorts.json` | `dde413de5eac00fd74c6ab6b200a60f92e05bc454ce29de7ce6453552ea17ff1` | `dde413de5eac00fd74c6ab6b200a60f92e05bc454ce29de7ce6453552ea17ff1` |

## NARRATIVE_PANEL

The verdict is **FAIL: 10 of 12 mandatory answers are YES**. The optional chapter-title check is YES. The two mandatory NO answers concern the transition into the 2018 chapter and repeated exposition. I treated the panel literally: a single counterexample makes a check NO. Line quotations below are exact spoken text.

| ID | Required | Verdict | Exact line evidence and reason |
| --- | --- | --- | --- |
| `scene_first` | Yes | **YES** | `[x100101] 想像二〇一八年春天的一筆 eBay 訂單：買家按下付款，賣家等著收錢。` The first sentence already has a year, an order, a buyer acting, and a seller waiting. |
| `no_spoiler` | Yes | **YES** | `[x100106] 分拆那天，兩家公司還簽下一份營運協議；它留了什麼空間？` The opening names the agreement but withholds its terms, later disclosed at `x100407`–`x100415`. The split itself is the premise in the title; the opening does not give away the later share-distribution mechanics, migration result, or financial result. |
| `one_line` | Yes | **YES** | `[x100202] 成交只是第一步；那筆款項還得另走一段路才會抵達。` The same buyer-to-seller payment problem carries the 2002 acquisition, 2015 split, and 2018–2021 migration. After the 2018 teaser, the body moves from 2002 to 2014, 2015, 2018, 2020, and 2021; the return to 2018 is the advertised payoff, not a second full telling. |
| `no_toc` | Yes | **YES** | `[x100108] eBay 已把 PayPal 拆出去，為什麼又要自己接手收款？` The opening asks a story question rather than announcing chapter order. `x100603` names actual markets in the migration; it is a fact in the event, not a list of forthcoming sections. |
| `chapters_link` | Yes | **NO** | `[x100501] 開頭那份二〇一八年季報，只把付款中介列為開發中的能力。` The preceding chapter ends `[x100416] 這個期限還沒走完，eBay 會從哪裡把另一條路接起來？` The new chapter's *first* sentence restates `x100102`'s opening development-list fact; it neither identifies where the path starts nor advances the specific contract constraint left hanging. `x100502`–`x100505` eventually do that work, but the panel tests the first sentence. Other handoffs are stronger: `x100401` answers `x100315`, and `x100701` follows `x100615`. |
| `open_loops` | Yes | **YES** | `[x100515] 當原本的期限結束，這條新路能接住多少人？` The body keeps making concrete unresolved questions and turns (`x100217`, `x100302`, `x100315`, `x100507`, `x100608`, `x100707`, `x100711`). Even counting only explicit question marks, the longest intervening span is about 244 Chinese/Latin/digit speech units (`x100612` through `x100707`), roughly 70 seconds at 3.5 units/second; `x100615` and the chapter turn also create tension inside it. Exact rendered timing was not supplied by these three inputs. |
| `payoffs` | Yes | **YES** | `[x100609] 年底，活躍於自管付款的賣家超過一百萬。` This supplies a new, quantified answer to `x100515` and the nearby `x100608`. The delayed opening hooks also resolve with specific named material: contract/testing at `x100401` and `x100415`, real payment processing at `x100505`, and platform payment management at `x100703`–`x100704`. The FY2014 question at `x100302` gets 26% at `x100305`; the revenue-versus-volume question at `x100711` gets flat merchandise volume at `x100712`. |
| `no_recap` | Yes | **NO** | `[x100502] 那時原本的營運協議，仍在初始期限裡。` The prior chapter already says `[x100416] 這個期限還沒走完，eBay 會從哪裡把另一條路接起來？` At the chapter boundary, the script restates that the five-year agreement had not expired, without a named callback or new result. The opening also states the split twice: `[x100103] 但三年前，它才把 PayPal 分拆成另一家上市公司。` and `[x100108] eBay 已把 PayPal 拆出去，為什麼又要自己接手收款？` The latter adds the central question, but repeats its premise. The deliberate callback at `x100501` is exempt under this check, yet it does not remove these other repeats. |
| `chapters_are_events` | **No** | **YES** | `[x100601] 二〇二〇年七月，兩家公司那份 PayPal 營運協議到期。` The seven titles name a development-list event, acquisition, report finding, share distribution, development priority, agreement expiry, and final market migration. The two 2018 titles are close in meaning, but both describe an occurrence rather than a section function. |
| `outro_no_next` | Yes | **YES** | `[x100719] 訂閱品牌故事，下一次結帳時，也看看背後是誰在設計這段路。` “下一次結帳” refers to the viewer's next checkout, not a forthcoming video. Neither the outro's other lines (`x100717`–`x100718`) nor its card names another episode. |
| `opening_hooks` | Yes | **YES** | `[x100106] 分拆那天，兩家公司還簽下一份營運協議；它留了什麼空間？` After the first scene, `x100105` stops at the buyer/seller awaiting payment on split day; `x100106` withholds the agreement's latitude; `x100107` asks who controls payment; and `x100108` asks why eBay returns to its own collection flow. These point to later moments without revealing their outcomes. |
| `one_thread` | Yes | **YES** | `[x100716] 股權由誰持有，和結帳流程由誰設計，原來是兩種不同決策。` The closing resolves the opening's specific issue (`x100101`, `x100107`, `x100108`): who controls the route from buyer checkout to seller payment after the ownership split. Each intervening chapter changes what eBay can do with that route. |
| `no_detour` | Yes | **YES** | `[x100713] 所以這集能驗到流程和收入結構改變，不能宣稱分拆讓交易暴增。` The closing financial passage tests the outcome of taking the flow in house, while the 2002 and 2014 material explains why PayPal joined and why it separated. The named-country sentence at `x100603` is brief and describes actual rollout, rather than a freestanding roll call. |

### Chapter handoffs and repetition

The transition `x100217` → `x100301` brings the platform-external PayPal question into the 2014 figures; `x100315` → `x100401` turns the agreement question into the 2015 contract; `x100515` → `x100601` reaches the contract expiry; `x100615` → `x100701` reaches the remaining markets. The weak handoff is `x100416` → `x100501`: the chapter opens by returning to a fact already spoken in the teaser, and only subsequently discusses what the agreement allowed (`x100503`) and what real processing began (`x100505`). The immediately following `x100502` also repeats the unexpired-term status from `x100416`, which is why the separate `no_recap` check fails.

### Opening, length, and Shorts

The opening has 193 Chinese/Latin/digit speech units. It is about 43–55 seconds at 4.5–3.5 units/second, so a 30–60 second hook is plausible with normal pacing. It does not state the contract's answer or the final 2021 payment outcome. Its first sentence is a staged 2018 order, while the later 2002 return is clearly marked by the year.

The body excluding the 193-unit opening and 88-unit outro has **1,992 speech units**. At four units/second it is about **8.3 minutes** before pauses; at 3.8 it is about 8.7 minutes, and at a brisk 4.2 it is about 7.9 minutes. Thus an at-least-eight-minute body is plausible at a measured read, but the actual duration requires the generated narration or edit. The full spoken text has 2,273 such units, about 9.5 minutes at four units/second.

| Short | Estimated spoken length | Standalone | Hook answered | Evidence |
| --- | --- | --- | --- | --- |
| 1, cash from split | 166 units; about 37–47 seconds at 4.5–3.5 units/second, with brief scene pauses still plausibly under 55 seconds | **NO** | **YES** | The `hook` at shot `x10-b04-s04` asks whether eBay received sale cash; `proof` at `x10-b04-s05` explicitly says it did not. But the later `payoff` narration at `x10-b04-s07` begins “那份協議，讓 PayPal 的付款服務繼續留在 eBay 市集。” No prior spoken sentence introduces *an agreement*. Its following scene (`x10-b04-s08`) uses “協議” again, so this segment depends on context outside the Short's narration. |
| 2, who controls payment | 166 units; about 37–47 seconds at 4.5–3.5 units/second, with brief scene pauses still plausibly under 55 seconds | **YES** | **YES** | The `hook` at `x10-b01-s07` asks “誰能決定收款要怎麼走？” The middle names PayPal and eBay and tracks eBay's 2018 start and subsequent expansion (`x10-b04-s06`, `x10-b05-s05`, `x10-b06-s02`); the `payoff` at `x10-b07-s03` says eBay managed payments for all platform transactions from late 2021. |

The read-only verdict is therefore **not ready as a clean narrative-panel pass**. The decisive long-form fixes are to make the first sentence of the 2018 chapter answer the previous contract question and to remove the repeated agreement-status exposition; Short 1 needs the agreement introduced inside its own spoken sequence. These are suggested changes, not script edits in this review.
