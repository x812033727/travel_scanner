# Blind narrative review B, v11

Scope: I read only the current `docs/videos/story-everyday-target-x08/video.json`, `shorts.json`, and the `NARRATIVE_PANEL` checklist in `tools/video/core/narrative.mjs`. I did not inspect peer reviews, history, receipts, or source filings. I made no script edits and used no paid calls. Judgments below concern the narration as written, not independent fact checking.

Opening SHA-256:

| File | SHA-256 |
| --- | --- |
| `video.json` | `41bc67de909571a37bf4ae7a843d6dec0b4e1ed735bcae4bfc6fd5eed01e7001` |
| `shorts.json` | `704e07f972b24b7d79c2660e830d69d85cd7087a1fda26db6f8c1fe31ef7b4e3` |

## Long-video panel

**Verdict: FAIL, 11/12 mandatory checks pass.** The blocking check is `payoffs`. The optional chapter-title check passes. I used the panel's strict rule: a question needs a later clear answer, and uncertainty counts as no.

| Check | Required | Answer | Line evidence and reasoning |
| --- | --- | --- | --- |
| `scene_first` | Yes | **Yes** | [x080101] “二〇一五年一月十五日，Target Canada 向多倫多法院遞出保護申請。” A dated legal action at a specific court starts the story; [x080102] immediately shows operating stores. |
| `no_spoiler` | Yes | **Yes** | [x080103] “這個店網接下來會怎樣？” The opening leaves the network's fate unresolved. Its lease, margin, and holiday teases also stop before outcomes. |
| `one_line` | Yes | **Yes** | [x080201] “二〇一一年，Target 買下 Zellers 一百八十九個據點的租約權利。” After the dated 2015 cold open, the account tracks the same venture from lease purchase through opening, losses, decision, accounting, and closure. |
| `no_toc` | Yes | **Yes** | [x080317] “下一財年，將是加拿大店網第一個全年營業的財年。” This advances story time. No spoken line announces an outline of the video or enumerates forthcoming sections. |
| `chapters_link` | Yes | **Yes** | [x080601] “二〇一四會計年度的退出費用，稅前共五十一點零五億美元。” This answers the preceding chapter's [x080512] question about the exit decision's charge. Similarly, [x080301] follows the sales question and [x080501] follows the board question. |
| `open_loops` | Yes | **Yes** | [x080421] “開得久的店掉下去，下一季會怎樣？” At the project timeline estimate, consecutive spoken questions are at most about 51 seconds apart, below the panel's 90-second threshold. |
| `payoffs` | Yes | **No** | [x080208] “回租契約最晚到二〇一三年三月底；店能準時開嗎？” Later [x080225] says the first 24 opened in FY2013 Q1, and [x080231] says the planned annual store count was reached. Neither establishes whether those leasehold sites opened *on schedule* relative to the stated March handover; Q1 spans dates on both sides of that deadline, and annual quantity is different from schedule. [x080210] asks *when* the sites welcome customers and [x080225] answers that separate question. The earlier on-time question lacks a literal yes/no payoff. |
| `no_recap` | Yes | **Yes** | [x080433] “記得前一年新店分批開張嗎？總銷售變大，不等於老店也成長。” The prior fact is brought back as an explicit callback to make a new distinction. [x080404] likewise identifies the first opening quarter as a comparator when repeating its sales figure; [x080615] synthesizes the financial cause and decision as the central answer. I found no unmarked repeat of the same fact serving as a new segment. |
| `chapters_are_events` | No | **Yes** | [x080501] “董事會在一月十四日批准停止加拿大門店營運。” Its chapter title, “一月十四日，董事會作出決議,” names an event. The other chapter titles likewise name actions or discoveries: filing, lease acquisition, sales disappointment, operations adjustment, and reported exit charges. |
| `outro_no_next` | Yes | **Yes** | [x080617] “想繼續看熟悉品牌為什麼改變方向，歡迎訂閱。” It asks for a subscription but promises no next episode or file. |
| `opening_hooks` | Yes | **Yes** | [x080109] “公司還想用年底購物季測試一輪調整。” After scene one, [x080103] asks what happens to the network, [x080107] sets up the leases, [x080108] teases initially good margins, and [x080109] plants the unresolved holiday test. |
| `one_thread` | Yes | **Yes** | [x080206] “買到的是開店權利，並非已開門的 Target。” The continuing concrete problem is whether Target's Canadian store network can earn enough to justify its buildout. The lease, launch, inventory, comparable sales, decision, and exit all develop that problem. |
| `no_detour` | Yes | **Yes** | [x080509] “這是為員工設的過渡保障，卻無法讓店繼續營業。” The employee-trust passage answers the opening employee stake [x080105] and advances the liquidation consequences. The later accounting passage separates exit charges from operating losses needed to understand the cost of withdrawal. |

The large-gap payoffs mostly work: [x080439] explicitly returns to the holiday test before [x080440] reports no needed surge; [x080504] recalls the stores that remained open on announcement day before [x080510] reports that all had closed by May 2. These do not repair the distinct scheduling question at [x080208].

Project `estimateTimeline(video.json)` gives 22,371 frames at 30 fps, **12:25.7**, above the declared 8–11 minute target. The narration contains 2,518 Chinese characters across 143 spoken lines and 137 scenes. Delivery could vary, but the project estimate is a concrete length risk.

## Shorts

| Item | Independent narrative result | Timing estimate |
| --- | --- | --- |
| Short 1 | **Fails stand-alone closure.** The hook/title question—whether all 133 stores closed on announcement day—is answered by the turn (stores remained open) and proof ([x080510], all closed by May 2). The final `loop` beat then borrows [x080110], “這家擅長開店的美國零售商，為什麼連加拿大這一關都過不了？” This newly opens the broader cause-of-failure question. The earlier Cornell profit forecast says management saw no near-term profit; it does not explain the operational and margin causes that the final question requests. The clip ends with that answer deferred to the long video. | 149 Chinese characters, four Latin words, eight narration units, six scenes: approximately **42–50 seconds** at normal zh-TW delivery with short pauses. Within 25–55 seconds. |
| Short 2 | **Passes stand-alone closure.** It establishes the US$5.105b pretax exit charge, identifies US$4.766b as noncash impairment, and answers the near-zero valuation question with loss of control and estimated liabilities exceeding distributable assets ([x080605], [x080607], [x080608]). Its penultimate question [x080610] asks whether operating losses are included; the final beat answers directly with [x080611], “不算。營運虧損要放在另一張帳。” No newly opened question remains. | 165 Chinese characters, one Latin word, ten narration units, six scenes: approximately **45–53 seconds** with natural pauses. Within 25–55 seconds, close to the upper limit at a slow read. |

The first Short's alternate title, “Target 加拿大 133 店宣布退出，何時才全關？”, can sound like a promise of the exact last closure date. Its narration and description establish only the upper bound, *by* 2015-05-02. The event-driven long-video chapter titles are acceptable under the panel's optional check.

Closing SHA-256: `video.json` `41bc67de909571a37bf4ae7a843d6dec0b4e1ed735bcae4bfc6fd5eed01e7001`; `shorts.json` `704e07f972b24b7d79c2660e830d69d85cd7087a1fda26db6f8c1fe31ef7b4e3`. Both match the opening hashes.
