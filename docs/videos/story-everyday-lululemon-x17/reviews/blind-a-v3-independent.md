# X17 v3 — independent blind review A

**Verdict: HOLD. First-reader score: 7.1/10.** The opening gives an immediate, concrete problem, and the black-pants path from swatch to finished garment, withdrawal box, and ledger is easy to recognize. The investigation and accounting distinction pay off. The strict narrative panel still fails Q2 and Q8: the opening gives away a later finding, and the body repeats a fact without a named callback. The middle and annual close also spend more lines restating implications than discovering new ones.

## Blind-reading record

I first read only the frozen `video.json` and `shorts.json`, then locked the 7.1/10 first impression. Their SHA-256 values were:

| File | SHA-256 |
| --- | --- |
| `video.json` | `bb9677cbbf9830be8a116c4edf7ff5743b1384a165f823b197e9ef76b176ebf5` |
| `shorts.json` | `089a8b37946f59d4fecd79bfaf470b5038088893abfb0caa881f921b1882fd8d` |

I then read the generic `AGENTS.md`, the brand-story skill, and `tools/video/core/narrative.mjs` and locked every Q1–Q13 answer below before opening any episode task, README, source matrix, prior review, or author note. This is a story/readability judgment, not an independent source audit or a rendered-video review.

## Locked narrative panel

Q9 is advisory. All other questions are required. The quoted line is the primary evidence for each answer; where a judgment rests on an absence or on structure, the accompanying note explains the broader reading.

| Question | Answer | Line evidence and reason |
| --- | --- | --- |
| Q1 `scene_first` | **Yes** | [x170101]「二〇一三年三月，店裡一排衣架突然少了黑色運動褲。」A dated, visible store event opens the script; [x170102] names the company's action. |
| Q2 `no_spoiler` | **No** | [x170105]「倉庫與運送途中也有受影響的貨，店裡要等多久？」The first clause states the affected-stock scope that [x170314] later presents as a discovery. The restock question remains open, but this part of the answer is already given. |
| Q3 `one_line` | **Yes** | [x170108]「衣架空掉以前，公司的日常檢驗先從布樣開始。」This clearly signals the one return from the opening preview to the earlier starting point. The body then proceeds through supply, withdrawal, investigation, quarterly accounts, and annual report. |
| Q4 `no_toc` | **Yes** | [x170108]「衣架空掉以前，公司的日常檢驗先從布樣開始。」It moves to an action in the story rather than announcing an outline; no spoken chapter menu interrupts the body. |
| Q5 `chapters_link` | **Yes** | [x170301]「公司說，涉事批次自三月一日起可在店內買到。」This directly answers [x170224]'s question about when the batch appeared. The subsequent chapter openings similarly take up the preceding question or consequence. |
| Q6 `open_loops` | **Yes** | [x170207]「一張布料檢驗單，能替最後穿上的透度作保嗎？」Questions and turns recur throughout the long body, including [x170321], [x170404], [x170428], [x170512], and [x170609]; no apparent 90-second dead stretch remains on a reading at the stated pace. |
| Q7 `payoffs` | **Yes** | [x170408]「公司發現，某些布料特性變數沒有測完整。」This answers the renewed inspection-gap question at [x170404], which recalls the opening's April question. The missing-stock, restocking, and cost questions likewise receive new answers. |
| Q8 `no_recap` | **No** | [x170402]「原來的 Luon 規格從二〇〇六年沿用，後來沒有重大修改。」[x170214] already said the Luon specification and inspection procedure were set in 2006. [x170402] supplies a nuance but repeats the central fact without 「還記得」 or another named callback. The adjacent seven-week lines [x170501]–[x170502] add to the repetitive feel. |
| Q9 `chapters_are_events` | **Yes (advisory)** | [x170401]「四月三日，公司說涉事布料可能符合舊測試，做好的褲子卻太透。」Its chapter, 「四月調查找到布料與版型的缺口」, names a dated finding; the other chapter labels name a withdrawal, return, test, or report. |
| Q10 `outro_no_next` | **Yes** | [x170632]「想看產品決定如何寫進財報，歡迎訂閱品牌故事。」The ending gives a reason to subscribe and does not advertise a next episode. |
| Q11 `opening_hooks` | **Yes** | [x170104]「四月，公司重新檢討沿用多年的檢驗標準；究竟漏看了什麼？」After the first scene, this, [x170105]'s restock question, and [x170106]'s cost-book question plant three later moments. Q2 concerns the prematurely stated scope inside one of them. |
| Q12 `one_thread` | **Yes** | [x170410]「公司認為幾個因素相疊，透度才無法接受；不是單靠布料一項就能解釋。」The same illustrative black-pants problem drives the swatch comparison, withdrawal, replacement, and accounting chapters. |
| Q13 `no_detour` | **Yes** | [x170506]「這筆是存貨準備，列進銷貨成本。」The accounting material resolves the opening's ledger question. The story spends too long on some linked material, but it does not switch to an unrelated storyline or a product list. |

**Panel result: HOLD** because Q2 and Q8 are required failures. Q9 passes as an advisory judgment.

## Story and Shorts notes

The empty rack at [x170101] works as the first image. The opening's seven scenes are roughly 178 written characters, so its three questions arrive quickly. The small repair with the greatest value is [x170105]: ask what happens to goods outside the shop without asserting that warehouse and transit inventory were affected. That preserves the later [x170314] reveal.

The visual thread is coherent: the swatch and finished trousers share the table at `x17-b02-s06`, a finished leg is compared with a flat swatch at `x17-b04-s09`, boxed pants span the store and warehouse at `x17-b03-s11`, and the cost token reaches the ledger at `x17-b05-s06`. The recurring plain black pants are an illustrative object, not a claim that a photographed physical pair survived all four locations. Most prompts describe only generic black pants, so the production must maintain a consistent silhouette if the viewer is meant to track that visual object across generated stills.

The chronology is intelligible once [x170108] announces the move to before the March withdrawal. March's affected batch and removal lead to the April finding; the first-quarter booked cost and June return follow; the next March's FY2013 announcement comes last. The investigation's strongest passage is [x170401]–[x170410]: “possibly met” the old test, lower end of tolerance, untested variables, and a subtle pattern change are kept separate before the company draws its combined explanation. The later tests and factory presence give that finding a consequence. The financial passage also carefully distinguishes the March US$57–67m **forecast** from the US$17.5m **booked inventory provision**, and it does not turn companywide revenue or gross-margin movement into a black-pants sales figure.

The cost of that care is pace. B02 uses 24 scenes before the March batch arrives; several lines restate the swatch/finished-garment difference ([x170203], [x170204], [x170206], [x170207]). B04 uses 26 scenes, with multiple question-to-answer steps around the changed tests and factory process. B06 uses 13 scenes to make the annual-report limit: [x170604], [x170607], and [x170608] all say the total revenue cannot isolate lost black-pants sales, while [x170611]–[x170613] repeat the parallel limit for annual gross margin. These sections remain on the story's line, which is why Q13 passes, but they weaken the sense of fresh discovery. Removing duplicate statements or making a real named callback where a fact must recur would help Q8 and the overall pace. Any cut should still be checked against the required eight minutes of substantive narration.

The outro answers the fabric-versus-garment issue and names the booked cost [x170630], then asks a relevant viewer question [x170631] and invites subscription for a clear reason [x170632]. Its answer is sound, though its final fact-and-number recap has less dramatic force than the swatch-to-finished-leg reveal.

Both Shorts stand alone. Short 1 states the affected subset and the company's multi-factor explanation without overstating the test result. Its final “inspect the finished pants” takeaway is clear. Short 2 carries its own forecast-versus-booked-cost distinction and explains how companywide sales could rise while this inventory cost was recorded. One copy correction is worthwhile before release: 「店裡與網站，第一季後七週都缺這批貨。」can mean seven weeks *after* Q1; the intended fact is the final seven weeks *of* Q1. A phrase such as 「第一季最後七週」would remove that ambiguity.
