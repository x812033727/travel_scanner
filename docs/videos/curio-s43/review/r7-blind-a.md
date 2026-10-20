# S43 R7 independent narrative cold read (reader A)

Source freeze: `video.json` SHA-256 `bcc662192de31052c4477236044b57f22c40e1c4691cca2579dfefabd68ae925`; `script.md` SHA-256 `5e9304251d8d99766859099e199ae1815e15879f566f9d696b7dd8baf3fc8b13`. Read the S43 brief, these two files, the 13 questions and panel rules in `tools/video/core/narrative.mjs`, and the general history-curiosity guidance. No earlier S43 reviews or verification files were consulted. I judged the narration as written, independently of the brief's desired result.

**Verdict: No (3 required questions fail: `payoffs`, `no_recap`, `no_detour`).** `chapters_are_events` is advisory and passes. A Yes below means the full question appears met; a No identifies a breaking line.

| # | Panel id | Yes/No | Scene quote | Reason |
| --- | --- | --- | --- | --- |
| 1 | `scene_first` | **Yes** | `[dn001] 一八三一年八月底，達爾文從北威爾斯的地質旅行回家。他後來回憶，家裡已有亨斯洛的信。` | A dated return and a waiting letter begin the story immediately. |
| 2 | `no_spoiler` | **Yes** | `[dn007] 九月五日，伍德收到船長回信；達爾文得知內容後，寫給姊姊的是好消息嗎？` | The opening previews the later letter but withholds Darwin's reaction and the final outcome. The nose teaser in dn008 likewise stops before the trait and result. |
| 3 | `one_line` | **Yes** | `[dn087] 十二月二十七日，它終於從德文波特出海。達爾文也在船上。` | The body advances the same boarding decision from invitation, refusal, renewed chance, meeting, decision, to departure. The first chapter's flashes are teasers, then the body runs forward. |
| 4 | `no_toc` | **Yes** | `[dn010] 不能。當時皮科克正在替船長找自然研究者，就找亨斯洛推薦人選。` | The next chapter answers a story question directly. No spoken line announces a list of sections or what the video will cover next. |
| 5 | `chapters_link` | **Yes** | `[dn066] 面談時，船長沒有只講好處。他說兩人在小船上會被迫常常相處。` | This chapter starts with the meeting and answers dn065's question about what difficulties the captain would disclose. Other chapter starts similarly pick up dn009, dn023, dn036, dn053, and dn078. |
| 6 | `open_loops` | **Yes** | `[dn073] 達爾文能接受這樣直接的相處方式嗎？` | Questions and turns recur through the body; `hookCadenceProblems(doc, estimateTimeline(doc), 90)` returns no gap. |
| 7 | `payoffs` | **No** | `[dn074f] 他卻仍在等南太平洋航線定案，才肯作最後決定。` | The earlier question in dn071 is whether the ship **will sail toward the South Pacific islands**. dn074f leaves that route pending. dn077b later gives Darwin's changed intention, and dn087 confirms departure, but neither says whether the route was settled or that he decided to go without that answer. The route question lacks a clear new answer. |
| 8 | `no_recap` | **No** | `[dn063] 達爾文說，兩人見面前約五分鐘，船長才得知切斯特不能成行。` | dn061 already says the intended friend could not go, and dn062 names him. dn063 adds valuable timing but repeats the inability to go without an explicit callback. |
| 9 | `chapters_are_events` | **Yes** | `[dn054] 亨斯洛幫他商量準備工作，卻叫他先別做最後決定。` | Chapter titles name a letter arriving, a recommendation, refusal, uncle's visit, captain's reply, London meeting, and the later nose revelation. They describe events or discoveries. |
| 10 | `outro_no_next` | **Yes** | `[dn999a] 鼻子沒讓達爾文落選；「差點」見於他晚年自傳，所引當年信沒有鼻形退件。` | The three outro lines answer the title, ask a neutral viewer question, and point to sources. None names a future video. |
| 11 | `opening_hooks` | **Yes** | `[dn008] 多年後，達爾文寫下：船長連他的鼻形都注意過。船長從中看出什麼？` | After dn001 the opener plants at least four later moments: the answer letter (dn005), father's response (dn006), captain's letter (dn007), and nose judgment (dn008). dn009 adds the appointment question. |
| 12 | `one_thread` | **Yes** | `[dn077b] 回來後，他在續寫的信裡改口：「你可以把我會去看作已定。」但仍承認意外可能改變計畫。` | Darwin's ability and willingness to board remains the same concrete difficulty across every chapter, even when the evidence shifts from contemporaneous letters to memoir. |
| 13 | `no_detour` | **No** | `[dn074d2] 九月九日，家裡寄的包裹送到了；達爾文在給姊姊的信裡道謝。` | The parcel's arrival and thanks neither change the boarding decision nor resolve the preceding question about the ship's list. It is a full, separate scene inserted between the captain-letter recovery and the consequential mess-list news. |

The title gets a calibrated answer: dn079–dn083 attribute the near-rejection story to Darwin's later recollection; dn087 proves he sailed; dn999a says the cited contemporary letters do not show a nose-based rejection. The closing question remains neutral.

Timing under `estimateTimeline(doc)` at 250 spoken units/minute, including the built-in pauses: first chapter dn001–dn009 **56.57 s** (within 30–60 s); body dn010 up to the outro **574.87 s = 9:34.87** (over 8 minutes); outro **18.50 s**; total **649.93 s = 10:49.93**. These are estimates, not recorded speech. The 45-second heuristic also returns no flagged hook gaps, although the panel itself asks for 90 seconds.

For a revision, clarify the South Pacific issue using only what the cited letters support: say whether they record a final route answer, and tie Darwin's later “I will go” to that unresolved condition. Condense dn061–dn063 so the friend's inability is said once while preserving the five-minute timing. Remove or connect dn074d2 directly to a meaningful consequence. The brief requests `intro_at: after_first_chapter` and an end screen; those are production settings outside this narrative verdict and are not evident as top-level fields of the current `video.json`.
