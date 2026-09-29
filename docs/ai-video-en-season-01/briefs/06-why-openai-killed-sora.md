# Why OpenAI Killed Sora

slug：`why-openai-killed-sora`｜第 6 支，建議 2026-11-10 上架｜英文旁白、8–12 分鐘｜企劃日 2026-09-28

## 觀眾

Creators, marketers and curious viewers who remember Sora's 2024 demos, noticed the app closed on 2026-04-26 and the API on 2026-09-24, and want to know what happened and what AI video costs now. Searches: "why did openai shut down sora", "sora shut down", "ai video generator cost per second 2026", "veo vs kling vs seedance".

## 觀眾看完能做到的事

- Compute the cost per second of video for any generator from its published price, and compare tools on one number.
- Run one check before paying for an AI video tool: does the price page, the terms page and the disclosure rule (YouTube's) allow what I plan to make.

## 站主觀點

套用立場：1、2

I follow the money, not the demo. The question "why did OpenAI kill Sora" has an official answer (whatever OpenAI's notices say, quoted) and an economic answer (what a second of generated video costs to make and to sell), and I keep the two apart on screen: quotes are quotes, my reading is labelled as mine. A tool that wins a demo but loses on cost per usable second does not survive, and the survivors in 2026 are the ones whose price pages I can actually read. That is also how I would pick one today.

## 示範或實算

Cost-per-second table on `table` and `stats` slides (chapter 3), built on writing day from official pricing pages: for each current generator (Google Veo 3.1 via the Gemini API, Kling 3.0, Seedance 2.0, Runway, Higgsfield, and any newer entrant) the list price of one clip at a stated resolution and length, divided into cost per second; then "cost per usable second" with an assumed retry factor the viewer can change (formula on a `code` slide). Optional: one real 5-second clip generated on writing day with its receipt on a `screenshot`-free `stats` slide (numbers only). Where a vendor publishes no price, the cell reads "not published".

## 大綱

### 選項 A：時間線，然後跟著錢走（建議）

Angle: two dates, then the economics; differs from B, which starts from the creators' side.

Hook: "On April 26, OpenAI shut down the Sora app. On September 24, it killed the API too. Two years ago Sora was the demo that made the whole internet gasp. So what happened? OpenAI gave its reasons, and I'll read them to you. But if you follow the cost of one second of video, from the demo to the bill, the answer gets a lot clearer, and it tells you which AI video tools will still be here next year."

| # | Chapter | s | Scenes |
| --- | --- | --- | --- |
| 1 | Two dates and one demo | 80 | `title`; `steps`: 2024 demo → 2025 app → 2026-04-26 app closed → 2026-09-24 API closed; `quote`: OpenAI's stated reason(s) |
| 2 | What OpenAI said, and what it didn't | 70 | `quote` ×2; `bullets`: the questions the notices leave open (labelled as questions) |
| 3 | The cost of one second of video, today | 140 | `code`: price ÷ seconds; `table`: per generator; `stats`: cheapest / most expensive / spread; `big`: cost per usable second with retries |
| 4 | Who is winning and why | 90 | `stats`: Higgsfield search growth (+8400% on Exploding Topics, September); `compare`: demo quality vs price page readability; `bullets`: convergence of Kling, Veo, Seedance, Sora 2 on production quality (per the 2026 trade write-ups) |
| 5 | What it means if you make videos | 90 | `compare`: generate vs license stock; `steps`: YouTube's disclosure rule for realistic synthetic content; `cta`: the Mokaair article on AI video tools if published |
| 6 | The one check before you pay | 60 | `steps`: price page / terms page / disclosure rule |
| 7 | So why did OpenAI kill Sora? | 40 | `outro`: "OpenAI's reasons are on the record; the economics say a demo isn't a product until a second of video costs less than it earns"; next step: comments: "what's the most you've paid for one usable clip?" |

Total ≈ 570 s; English narration ≈ 1,400 words.

### 選項 B：從創作者的帳單開始

Angle: start with a creator's real bill for a 60-second AI video, then the industry story.

Hook: "A sixty-second AI video can cost you four dollars or four hundred, depending on which button you press. Here's the price list nobody shows you, and why the most famous tool of all just disappeared from it."

Chapters: One minute, priced (120 s) → The Sora timeline (80 s) → What OpenAI said (70 s) → Who survives (90 s) → Disclosure and licensing (90 s) → The one check (60 s) → `outro` (40 s).

## 會過期的事實

| Fact | Re-check at |
| --- | --- |
| Sora app closure 2026-04-26 and API discontinuation 2026-09-24, and OpenAI's stated reasons | OpenAI's help-center or blog notices (the dates on planning day come from Wikipedia's 2026 timeline and trade press; confirm on OpenAI pages) |
| Every generator's price, resolution and clip length | each vendor's pricing page on writing day (Gemini API pricing for Veo; Kling; ByteDance/Seedance; Runway; Higgsfield) |
| Search-growth figure for Higgsfield | explodingtopics.com/ai-topics on writing day |
| YouTube's disclosure rule wording | support.google.com/youtube/answer/14328491 |

## 素材

- Original tables; `quote` slides for OpenAI's wording with dates.
- No Sora footage, no other generators' sample videos, no logos; if a clip is generated for the receipt, only its numbers appear.

## 不做的事

- No speculation stated as fact about OpenAI's finances or internal decisions; questions are labelled as questions.
- No tool ranking beyond cost per second; no affiliate links.
- No claims about lawsuits or copyright cases beyond a quoted official line, if any.

## 附錄：包裝與破百萬的理由

| Item | A (news) | B | C (evergreen) |
| --- | --- | --- | --- |
| Title | Why OpenAI Killed Sora | OpenAI Shut Down Sora. Here's the Real Cost of AI Video. | AI Video Was Supposed to Change Everything. Then OpenAI Pulled the Plug. |
| Thumbnail label / big / small | 2024 → 2026 / SORA IS DEAD / what a second of video really costs | — / $ PER SECOND / the price list nobody shows | — |

Why one million is plausible: a three-word curiosity title about the most famous AI product to be discontinued; the AI-video category holds the biggest single AI video on YouTube (Marques Brownlee, 9.2M in the planning snapshot, `sources.json` S13); the cost-per-second table is the shareable asset. Risk: motive speculation; handled by quoting and labelling.
