# X08 v12 — independent blind narrative read A

Scope: `video.json`, `shorts.json`, and the `NARRATIVE_PANEL` in `tools/video/core/narrative.mjs` only. I did not consult prior reviews, receipts, briefs, sources, or peers. This judges the spoken story and the two Short scripts, not factual source accuracy or rendered audio.

Verdict: **FAIL under the mandatory narrative panel: 9 YES / 3 NO**. The optional event-title check is YES. The story is substantially stronger than a collection of sections, but the strict delayed-payoff, no-repetition, and no-detour checks do not fully pass.

| Panel ID | Required | Answer | Script evidence and judgment |
| --- | --- | --- | --- |
| `scene_first` | Yes | **YES** | `[x080101] 二〇一五年一月十五日，Target Canada 向多倫多法院遞出保護申請。` The first sentence puts a named actor, date, place, and action on screen; the next three remain at that moment. |
| `no_spoiler` | Yes | **YES** | `[x080109] 公司還想用年底購物季測試一輪調整。` The opening stops before the holiday result, profitability forecast, and final closure date. |
| `one_line` | Yes | **YES** | `[x080502] 隔天，開場那份法院保護申請由加拿大子公司遞出。` One opening flash-forward is followed by the 2011–15 store-network sequence and an explicit return to the opening day. |
| `no_toc` | Yes | **YES** | `[x080443] 董事會會繼續等嗎？` Turns are phrased as story questions, not a list of sections to come. `[x080234] 門已經開了；現在要看誰把商品帶走。` is a somewhat visible narrator pivot, but it points to the unresolved sales consequence rather than enumerating the video's structure. |
| `chapters_link` | Yes | **YES** | `[x080443] 董事會會繼續等嗎？` → `[x080501] 董事會在一月十四日批准停止加拿大門店營運。` This is a real question and answer at a chapter boundary. The lease-rights opening at `[x080201]` picks up `[x080107]`; `[x080301]` answers `[x080234]`; `[x080401]` answers `[x080318]`; `[x080601]` answers `[x080512]`. |
| `open_loops` | Yes | **YES** | `[x080421] 下一季樣本擴大後，同店銷售會怎樣？` Questions, reversals, and forward turns recur through the longest 2014 chapter. Given the number and distribution of spoken lines, a 90-second empty stretch is implausible at the stated natural delivery; this remains an estimate, not an audio timing measurement. |
| `payoffs` | Yes | **NO** | `[x080104] 全國當時有一百三十三間店。` together with `[x080110] …為什麼連加拿大這一關都過不了？` plants the central delayed paradox. `[x080438]` establishes the margin/expense gap and `[x080441]` gives management's 2021 forecast, but neither points back to the **133-store network** when answering why scale did not save it. Under the panel's explicit rule that a payoff after several minutes must name the original concrete person, object, or question, this one is incomplete. The earlier hooks about first-quarter margin and the holiday season *do* get named callbacks at `[x080304]` and `[x080439]`. |
| `no_recap` | Yes | **NO** | `[x080615] 毛利蓋不住營運開支；管理層當時看不到近年獲利，於是退出。` repeats both the margin/expense conclusion at `[x080438]` and the no-near-term-profit judgment at `[x080441]` without an explicit callback. It is a tidy outro answer, but the panel's once-per-fact rule has no general outro exception. |
| `chapters_are_events` | No | **YES** | `[x080501] 董事會在一月十四日批准停止加拿大門店營運。` All six chapter titles describe an action or revealed outcome: application while stores trade; lease purchase; weak sales; 2014 adjustment; board resolution; exit expense appearing in accounts. |
| `outro_no_next` | Yes | **YES** | `[x080617] 想繼續看熟悉品牌為什麼改變方向，歡迎訂閱。` The close does not name the subject of a later video. |
| `opening_hooks` | Yes | **YES** | After the initial court scene, `[x080107]` withholds what the lease rights cost, `[x080108]` withholds whether the promising early margin survived, and `[x080109]` withholds the holiday result. `[x080103]` also leaves the open stores' fate unresolved. These are concrete later moments, not a spoken contents list. |
| `one_thread` | Yes | **YES** | `[x080201] 二〇一一年，Target 買下 Zellers 一百八十九個據點的租約權利。` The Canadian store project remains the identifiable subject from premises and opening through sales, decision, closure, and financial aftermath. |
| `no_detour` | Yes | **NO** | `[x080610] 那兩年的營運虧損，也算在這筆退出費裡嗎？` starts a separate accounting classification lesson after the causal answer and exit decision. `[x080611]`–`[x080614]` resolve that new question, but do not advance the opening question of why a 133-store chain withdrew. This also places the promised actual-closure answer `[x080510]` after the accounting aside. Earlier `[x080213]`–`[x080215]` briefly list footprint and distribution arrangements without showing how those particular arrangements affected the eventual failure. |

The chapter handoffs themselves mostly pay off: `[x080318]` → `[x080401]` gives the first reported improvement; `[x080443]` → `[x080501]` gives the board's decision; `[x080512]` → `[x080601]` gives the stated expense. The opening's store-fate loop eventually gets a concrete outcome at `[x080510]` (all Canadian stores closed by May 2), but the intervening accounting lesson weakens that return. The store-count paradox is the clearest missing explicit long-range callback.

Timing and format assessment: the opening is 205 written characters across ten spoken sentences, plausibly about **40–55 seconds** at normal Taiwanese Mandarin narration with short pauses. It opens in the first sentence, plants at least three loops, and does not disclose their results. The body contains about **2,644 written characters** after the opening and before the three-sentence outro; a natural 240–300 written-character-per-minute reading gives about **8.8–11.0 minutes** of body. This is a plausibility estimate because no audio or generated timeline was within scope. It has substantive store-launch, sales, margin, management-decision, and wind-down material, though the quarterly figures in the 2014 chapter are dense.

Both Shorts appear standalone and within **25–55 seconds** at natural delivery. Short 1 has eight narration sentences / 183 written characters: it introduces the 133-store puzzle, dates the Canadian filing, distinguishes announcement from actual closure, then states the by-May-2 outcome and the document's limit. Short 2 has ten narration sentences / 190 written characters: it states the exit expense, distinguishes noncash impairment from cash, explains near-zero equity value, and separates operating loss. Rough spoken-duration estimates are approximately **35–50 seconds** for each, depending on pauses and numeral pronunciation. Neither needs the long video to understand its answer.

SHA-256 at start of read:

| Exact input | SHA-256 |
| --- | --- |
| `video.json` | `b0b91c300c35e64bf0345dc3c9a91b027937f36068b75ec2ed32ff7ae914bdbc` |
| `shorts.json` | `060ddf682a17307c0747aa560916a2a0b8bcb151ffca60cccdc695fc231b862c` |
| `tools/video/core/narrative.mjs` | `63b631cea2c01f2a94b69252fdae7160253e906881b4fb37a4502603455cc387` |

SHA-256 at end of read:

| Exact input | SHA-256 |
| --- | --- |
| `video.json` | `b0b91c300c35e64bf0345dc3c9a91b027937f36068b75ec2ed32ff7ae914bdbc` |
| `shorts.json` | `060ddf682a17307c0747aa560916a2a0b8bcb151ffca60cccdc695fc231b862c` |
| `tools/video/core/narrative.mjs` | `63b631cea2c01f2a94b69252fdae7160253e906881b4fb37a4502603455cc387` |

The reviewed inputs remained unchanged.
