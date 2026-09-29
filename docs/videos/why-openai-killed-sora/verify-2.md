# Verification round 2: why-openai-killed-sora

Verifier: claude-opus-5-5, a session separate from the writer's and from round 1's, 2026-09-28. Scope, as assigned: every claim round 1 changed; a seeded random third of the claims round 1 confirmed; every quote attributed to OpenAI (word for word, and whether the zh-TW rendering is faithful); every piece of arithmetic; rulings on round 1's five "suspected but not changed" points. Each page was fetched today with `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`, following redirects and recording the final HTTP status. Requests were at least 1.5 s apart. `<!-- -->` comments were stripped first, then scripts and tags. Script-loaded pages (Kling, BytePlus, Runway API) were read from the data embedded in the served page. News outlets count only for what they report, and third-party pages confirm nothing. Web searches used: 0 of 5. No personal data is recorded here; people appear only by role.

Helper files are in `/tmp/claude-0/-home-user-travel-scanner/674d9bf2-c3b1-5d19-bf6c-31efd377fe1e/scratchpad/videowork/why-openai-killed-sora/why-openai-killed-sora/_tools/verify2/`: plan.md (written before any fetch), sample.py and sample.txt (the draw), fields.txt (every text field of video.json), fetch.sh, urls.txt and pages/ (raw pages, text dumps, status.log), and arith.mjs and arith.txt.

## Sample

Round 1's table has 83 claims: 6 CHANGED, 75 CONFIRMED and 2 OUT OF SCOPE. The seed is **20260928**, and the draw was `random.Random(20260928).sample(confirmed, 25)` over round 1's CONFIRMED numbers (sample.py reads them from verify-1.md). It picked **#3, 5, 6, 9, 15, 20, 29, 31, 38, 41, 42, 47, 48, 49, 50, 51, 57, 58, 62, 65, 72, 73, 74, 77, 80**.

On top of the draw, the mandatory scope brought in the other claims that carry an OpenAI quote, a media label or arithmetic: #13, 14, 16, 17, 19, 22, 24–28, 30, 32–36, 39, 43–46, 52, 54–56, 63, 64, 66, 69, 70, 76, 78 and 81.

Not re-checked as claims this round (round 1 confirmed them, the draw missed them, and they carry no quote or arithmetic): #2, 4, 7, 10, 11, 12, 21, 23, 53, 59, 60, 61, 67, 68, 75, 82. Pages read today for other claims show #7, 12, 21, 23, 53, 59, 60, 67, 68 and 75 unchanged, but they were not audited one by one.

## Pages fetched

| URL | HTTP | What it gave today |
| --- | --- | --- |
| https://developers.openai.com/api/docs/deprecations | 200 | "2026-03-24: Sora 2 video generation models and Videos API"; "On March 24th, 2026, we notified developers … removal from the API on September 24, 2026."; six rows, all 2026-09-24, all "—". Notice periods: "Generally available models: At least 6 months."; "Preview models … may be retired with much shorter notice, such as 2 weeks." |
| https://developers.openai.com/api/docs/pricing | 200 | No "sora" in the page or its source |
| https://web.archive.org/web/20260802044220/https://developers.openai.com/api/docs/pricing | 200 | OpenAI's page, "FILE ARCHIVED ON 04:42:20 Aug 02, 2026" (canonical developers.openai.com/api/docs/pricing). "Video generation models / Prices per second". Standard: sora-2 720p $0.10; sora-2-pro $0.30 / $0.50 / $0.70. Batch: sora-2 $0.05; sora-2-pro $0.15 / $0.25 / $0.35 |
| https://developers.openai.com/api/docs/guides/video-generation | 200 | "The Sora 2 models and Videos API were shut down on September 24, 2026 and are no longer available. No one-to-one replacement API is available." |
| https://web.archive.org/web/20260727175148/https://developers.openai.com/api/docs/guides/video-generation | 200 | Archived 17:51:48 Jul 27, 2026: Sora makes "clips with audio"; "Both sora-2 and sora-2-pro support 16- and 20-second generations"; the example request uses `seconds="8"` |
| https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation | 403 | Cloudflare challenge. The Help Center refuses scripts, so OpenAI's own page as archived is the record, labelled as an archive in `sources` |
| https://archive.org/wayback/available?url=help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation&timestamp=20260928 | 200 | Closest capture: 20260919081042 (still the newest) |
| https://web.archive.org/web/20260919081042/https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation | 200 (second try; the first was curl 35, a TLS reset. The proxy status lists tunnel closures to web.archive.org today) | og:site_name "OpenAI Help Center", archived 08:10:42 Sep 19, 2026, "Updated: 18 days ago". "The Sora web and app experiences were discontinued on April 26, 2026." "The Sora API will be discontinued on September 24, 2026." "If a final export window is offered, we’ll notify you by email before it begins." "After Sora is discontinued, and after the period of time of any final export window passes (if we are able to offer one), we will permanently delete any data associated with your use of Sora." No reason is given |
| https://web.archive.org/web/20260630192218/https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation | 200 (second try, same reset) | Same body text as the 09-19 capture. Only the breadcrumb and the summary line differ |
| https://sora.chatgpt.com/p/s_69c2ec89c7f081919a93f637f6b250c2 | 403 | Cloudflare challenge |
| https://web.archive.org/web/20260908090419/https://sora.chatgpt.com/p/s_69c2ec89c7f081919a93f637f6b250c2 | 200 | OpenAI's Sora site, archived 09:04:19 Sep 08, 2026. og:title "sora on Sora", posted by the account "sora", marked verified. og:description "An important update about Sora: Today, after careful internal discussion about our broader research priorities, we’ve made the difficult decision to discontinu…"; "uploadDate":"2026-03-24T19:56:57.781Z" |
| https://ai.google.dev/gemini-api/docs/pricing | 200 | Last updated 2026-09-24 UTC. "Paid Tier, per second in USD": Veo 3.1 Standard video with audio price (default) $0.40 (720p and 1080p), $0.60 (4k); Fast $0.10 / $0.12 / $0.30; Lite $0.05 (720p), $0.08 (1080p), "(4k output not supported)". No Batch tier for Veo. "You will only be charged if your video is successfully generated." Gemini Omni Flash, `gemini-omni-1.1-flash`, "now generally available": $17.50 (video) per 1M tokens, "5,792 tokens per second of 720p video … approximately $0.10 per second" |
| https://ai.google.dev/gemini-api/docs/veo | 200 | Last updated 2026-09-17 UTC. durationSeconds "4", "6", "8". Veo 3.1 and Fast: "Must be "8" when using extension, reference images or with 1080p and 4k resolutions"; Lite: "… or with 1080p"; "1080p (only supports 8s duration)"; "4k not available for Veo 3.1 Lite". Model versions: Veo 3.1 Preview, Veo 3.1 Fast Preview, Veo 3.1 Lite Preview |
| https://ai.google.dev/gemini-api/docs/deprecations | 200 | Last updated 2026-09-24 UTC. veo-3.0-generate-001: September 9, 2025 → June 30, 2026, replacement "veo-3.1-generate-preview or the GA models on the Gemini Enterprise Agent Platform". veo-3.1 lite / standard / fast previews: "No shutdown date announced". gemini-omni-flash-preview: June 30, 2026 → September 30, 2026, replacement gemini-omni-1.1-flash (released August 27, 2026, no shutdown date). The dates are "the earliest possible dates" |
| https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing | 200 | "Gemini Omni Flash, Gemini Omni 1.1 Flash": Video Output $17.50; "1931 tokens per second of 360p video, 5792 … 720p video, 8688 … 1080p video, and 17376 … 4k video for video outputs (with audio)" |
| https://kling.ai/dev/pricing | 200 | Embedded data: "Video API Pricing 1 Unit = $0.14 (list price)". Kling 3.0: 720P "No Native Audio" 0.6 Units ($0.084) /s, "With Native Audio x No Voice Control" 0.9 Units ($0.126) /s; 1080P $0.112 / $0.168; 4K 3.0 Units ($0.42). All Kling video rows at 720P are $0.084–$0.126. "Failed video generations will not deduct any unit." |
| https://docs.byteplus.com/en/docs/ModelArk/1544106 | 200 (one redirect, to /docs/modelark/model-pricing) | Last updated September 28, 2026 05:30:59. dreamina-seedance-2-0-260128: "For 480p and 720p outputs: Input without video: 7.0" (USD per M tokens, online inference). Price examples, input without video, 16:9, 5 s: Seedance 2.0 480p $0.07/s, 720p "0.76 per video, 0.15 per second", 1080p $0.37/s, 4K $0.78/s; Mini 480p $0.04/s. Discounts cover only 2.0 mini (60%) and fast (25%), until 14:00 (UTC+8) October 7, 2026. "You are only charged for successfully generated videos." Token formula as in claims.md c15. The minimum-token rule applies only when the input includes video |
| https://docs.byteplus.com/en/docs/modelark/create-video-generation-task-api | 200 (new this round) | Last updated September 28, 2026 05:31:02. Dreamina Seedance 2.0 series: `duration` "Default `5`; supports `[4, 15]` or `-1`"; at 720p 16:9 the output is 1280×720; "Number of frames = duration × frame rate (24)"; "returned duration = actual total frames / 24"; `generate_audio` defaults to true |
| https://docs.byteplus.com/en/docs/modelark/seedance-2-0 | 200 | The Seedance 2.0 tutorial. Nothing used |
| https://docs.x.ai/developers/pricing | 200 | Last updated: September 21, 2026. grok-imagine-video-1.5: 480p $0.08, 720p $0.14, 1080p $0.25 per second. The older grok-imagine-video: 480p $0.05, 720p $0.07 |
| https://docs.x.ai/developers/model-capabilities/video/generation | 200 | "The allowed range is 1–15 seconds."; "Generated videos include an audio track by default." |
| https://platform.minimax.io/docs/guides/pricing-paygo | 200 | List Price: MiniMax-H3 768P $0.08 / second, 2K $0.13; MiniMax-H3-Max 480P $0.05, 768P $0.08 |
| https://docs.dev.runwayml.com/guides/pricing/ | 200 | "Credits can be purchased for $0.01 per credit". gen4.5 12 credits per second; seedance2 (480p/720p) 36; veo3.1_fast (audio) 15 (no resolution given), (no audio) 10; veo3.1 (audio) 40; gen4_turbo 5 |
| https://docs.dev.runwayml.com/api/ | 200 | Embedded OpenAPI. Both gen4.5 schemas: duration "Must be an integer from 2 to 10"; ratio "1280:720", "720:1280" |
| https://higgsfield.ai/pricing | 200 | No "$" or "USD" followed by a digit anywhere in the served source |
| https://www.theverge.com/ai-artificial-intelligence/899850/openai-sora-ai-chatgpt | 200 | datePublished 2026-03-24T21:08:10Z. The note in full ("Update, March 25th: Added note from the Sora app"); "A report from Reuters says … running it required so much compute power that it left other teams working with less"; "OpenAI hasn’t responded to a request for comment or otherwise explained the shift" |
| https://www.cbsnews.com/news/sora-ai-openai-discontinues/ | 200 | Published 2026-03-24T16:32-04:00, modified 18:00:36-04:00. The spokesperson's statement and OpenAI's second statement (quoted in the claim table); "wanes in popularity among users, according to the Wall Street Journal" |
| https://techcrunch.com/2026/03/24/openais-sora-was-the-creepiest-app-on-your-phone-now-its-shutting-down/ | 200 | Published 2026-03-24T23:57:55Z: "OpenAI did not give a reason for the shut down". The embedded @soraofficialapp post (March 24, 2026) gives no reason and says "We’ll share more soon, including timelines for the app and API" |
| https://techcrunch.com/2026/03/29/why-openai-really-shut-down-sora/ | 200 | Published 2026-03-30T03:09:38Z (March 29 in US Pacific time): "According to a new WSJ investigation", the user count "peaked … and then collapsed" |
| https://www.businessinsider.com/openai-cfo-says-compute-crunch-is-forcing-tough-trade-offs-2026-4 | 200 | 2026-04-02. OpenAI's CFO, in an interview with ARK Invest's CEO: "We're making some very tough trades at the moment and things we're not pursuing because we don't have enough compute". BI's own sentence adds "including discontinuing its video app Sora" |
| https://mokaair.com/zh-TW/life/ai-video-tools-compared | 200 | 〈AI 影片工具比較：Veo、Sora、海螺、Kling 的方案與規格〉, 更新日期 2026-09-19: monthly fees, monthly credits and seconds per plan |

## Claim table

Numbers are round 1's. "Stands" means round 1's change was re-checked and holds.

| # | Claim | Where | URL | HTTP | Verdict | Before → after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 「官方公告只給一句理由」 | youtube.title; hook-title.chapter, data.subtitle; tt9u | theverge.com; web.archive.org/web/20260908090419/sora.chatgpt.com/…; techcrunch.com 3/24; cbsnews.com | 200 | CONFIRMED (round 1's change stands) | — The App note has one reason clause. The @soraofficialapp post, the Help Center page and the deprecations page give none. The two CBS items are statements to an outlet, not an announcement (公告) |
| 8 | 「每個價錢都寫了它假設的解析度；聲音會改變價錢的，也寫了有沒有聲音」 | youtube.description | ai.google.dev pricing; kling.ai; docs.byteplus.com; docs.x.ai; platform.minimax.io; docs.dev.runwayml.com; OpenAI pricing archive | 200 | CONFIRMED (stands) | — Rows whose price depends on audio say so: Kling 原生音訊, Veo 有聲, Grok 預設有聲. Seedance 2.0, MiniMax-H3, Gen-4.5, Omni Flash and Sora 2 have no audio split. One price has no resolution on its own page (Runway veo3.1_fast), and the slide says 頁面沒寫解析度 |
| 18 | Sora 2's $0.10 is the Standard price; Batch was half | hook-price.stats[0].note; table-google.rows[0][1]; price-range.stats[1].note; youtube.description | web.archive.org/web/20260802044220/…/pricing | 200 | CONFIRMED (stands) | — Standard $0.10, Batch $0.05 (0.05 ÷ 0.10 = 0.5). Google lists no Batch tier for Veo, so Standard against Standard holds |
| 37 | zbve 「當時 The Verge 和 TechCrunch 都寫，OpenAI 沒有另外解釋」 dropped | unanswered | theverge.com; techcrunch.com 3/24; cbsnews.com | 200 | CONFIRMED (the drop stands) | — Both outlets wrote it (21:08Z, 23:57Z). CBS had OpenAI's two statements out at 20:32Z (modified 22:00Z), and the script plays them just before this point. Nothing in video.json depends on the line |
| 71 | fwd5 「素材費差了八倍，差在你選哪個模型」 | short-table/fwd5 | ai.google.dev pricing | 200 | CONFIRMED (stands) | — $76.80 ÷ $9.60 = 8 (A50). Both rows are Google at 720p with audio |
| 83 | The Help Center source is the 2026-09-19 capture | sources[3] | archive.org availability API; web.archive.org …20260919081042; help.openai.com | 200; 200 (second try); 403 | CONFIRMED (stands) | — Still the newest capture; OpenAI Help Center; same body text as 06-30 |
| 3 | 「OpenAI 自己說過的話和三個日期」 | youtube.description | deprecations; Help Center capture | 200 | CONFIRMED | — 3/24, 4/26, 9/24 |
| 5 | Sora 2's price comes from OpenAI's own pricing page, August 2026 archive | youtube.description; hook-price; table-google.rows[0]; price-range.source; outro.lines[1] | OpenAI pricing archive; live pricing | 200; 200 | CONFIRMED | — Archived 2026-08-02 04:42:20 UTC; the live page has no Sora |
| 6 | Web and App stopped 2026-04-26 | youtube.description; timeline.steps[1]; tn22 | help.openai.com; Help Center 09-19 capture | 403; 200 | CONFIRMED | — "The Sora web and app experiences were discontinued on April 26, 2026." |
| 9 | Pages whose numbers cannot be read say 以官網為準 | youtube.description; table-others.rows[5]; bhxq | higgsfield.ai/pricing | 200 | CONFIRMED | — No price figure is served |
| 13 | 「一秒 $0.05–$0.40」 on the thumbnail | thumbnail.data.sub | as #20 | 200 | CHANGED | 「官方原話 vs 一秒 $0.05–$0.40」 → 「官方原話 vs 720p 一秒 $0.05–$0.40」 (ruling a) |
| 14 | The App announcement gives one reason sentence | hook-title; tt9u | theverge.com; Sora post archive; techcrunch.com 3/24 | 200 | CONFIRMED | — |
| 15 | "…after careful internal discussion about our broader research priorities, we've made the difficult decision…" is word for word | hook-quote.data.quote | theverge.com; Sora post archive | 200 | CONFIRMED | — Identical except that the pages use a curly apostrophe in "we’ve" |
| 16 | 「……經過內部對更廣的研究優先順序仔細討論，我們做了困難的決定……」 and tbe8 | hook-quote.data.translation; tbe8 | same | 200 | CONFIRMED | — Faithful, ellipses kept. tbe8's 「停掉 Sora」 renders "discontinue the Sora app" under the kicker 「Sora App 的停止公告」 |
| 17 | The note is OpenAI's, dated 2026-03-24, quoted by The Verge | hook-quote.data.kicker, source | Sora post archive; theverge.com | 200 | CONFIRMED | — uploadDate 2026-03-24T19:56:57.781Z (12:56 US Pacific; already 3/25 in Taiwan). OpenAI's deprecations page also dates it March 24th |
| 19 | Veo 3.1 Lite $0.05 at 720p with audio; 「表上最便宜」 | hook-price.stats[1]; 5kjd; price-range.stats[0]; qn2a | ai.google.dev pricing; the other price pages | 200 | CONFIRMED | — (ruling b) |
| 20 | 「各家一秒的價錢」 run from $0.05 to $0.40 | hook-range.data.kicker, data.text (jbpw names no range) | ai.google.dev pricing; docs.byteplus.com model-pricing; kling.ai | 200 | CHANGED | kicker 「各家一秒的價錢」 → 「各家 720p 一秒的價錢」. On these official pages Veo 3.1 is $0.60 a second at 4k, Kling 3.0 $0.42 at 4K, Seedance 2.0 $0.78 at 4K and Seedance 2.0 Mini $0.04 at 480p (BytePlus examples). Every 720p-class price on them lies within $0.05–$0.40 (ruling a) |
| 22 | 4/26 is 33 days after the announcement | timeline.steps[1]; tn22; notice-days.stats[1]; gewa | Help Center capture; deprecations | 200 | CONFIRMED | — A54 |
| 24 | Data is deleted once the final export window passes | timeline/h8a6; timeline.steps[3] | Help Center 09-19 and 06-30 captures; help.openai.com | 200; 403 | CHANGED | h8a6 「停止之後，最後的匯出期一過，資料會永久刪除。」 → 「停止之後，資料會永久刪除；如果有最後的匯出期，就等它結束再刪。」 The slide 「匯出期過後／資料永久刪除」 claims no final window and is unchanged (ruling d) |
| 25 | 「Sora 的最後六個月」 (3/24 to 9/24) | timeline chapter, data.title | deprecations | 200 | CONFIRMED | — A55 |
| 26 | Videos API, sora-2, sora-2-pro and three dated snapshots, all closing 2026-09-24 | deprecation-table.data.rows; qm8a; p4jh | deprecations | 200 | CONFIRMED | — |
| 27 | Every Recommended replacement is "—"; no replacement named | deprecation-table rows[*][2]; p7mt; xvcc; gxbt; shutdown-records.rows[0] | deprecations; video guide | 200 | CONFIRMED | — "No one-to-one replacement API is available." |
| 28 | "As we focus and compute demand grows, the Sora research team continues to focus on world simulation research to advance robotics…" is word for word | cbs-quote.data.quote | cbsnews.com | 200 | CONFIRMED | — The middle of: "We've decided to discontinue Sora in the consumer app and API. As we focus and compute demand grows, the Sora research team continues to focus on world simulation research to advance robotics that will help people solve real-world, physical tasks," |
| 29 | 「隨著我們聚焦、算力需求成長，Sora 研究團隊會繼續做世界模擬研究，推進機器人。」; s884; 3x7m | cbs-quote.data.translation; s884; 3x7m | cbsnews.com | 200 | CONFIRMED | — Faithful. 「推進機器人」 for "to advance robotics" is loose, and the translation ends in 「。」 where the quote is cut with "…"; neither is a fact error |
| 30 | A spokesperson's statement to CBS News, 2026-03-24 | cbs-quote.data.kicker, source; p8yy | cbsnews.com | 200 | CONFIRMED | — "an OpenAI spokesperson said in a statement to CBS News" |
| 31 | Left card: research priorities, from the App announcement | said-vs-reported.left.points[0]; pcc8 | theverge.com; Sora post archive | 200 | CONFIRMED | — |
| 32 | Left card: focus and growing compute demand, the spokesperson to CBS | said-vs-reported.left.points[1]; pcc8 | cbsnews.com | 200 | CONFIRMED | — |
| 33 | Left card and hv6h: compute trade-offs, highest-value uses | said-vs-reported.left.points[2]; hv6h | cbsnews.com | 200 | CONFIRMED | — "Every day we're making tradeoffs in how we apply compute across research, product launches and inference, and we're prioritizing the highest-value uses that best advance our mission," OpenAI said in its statement to CBS News. hv6h is a faithful paraphrase |
| 34 | Right card and ufsf: Sora took a lot of compute and other teams got less (Reuters via The Verge) | said-vs-reported.right.points[0]; ufsf | theverge.com | 200 | CONFIRMED | — Labelled with both outlets |
| 35 | Right card and 5n89: not enough compute, so some work is not pursued (the CFO, Business Insider) | said-vs-reported.right.points[1]; 5n89 | businessinsider.com | 200 | CONFIRMED | — The CFO said it to ARK Invest's CEO, and BI reported it. The quote does not name Sora; BI's own sentence does, so the right-hand (reported) side fits. 「算力不夠，有些事先不做」 is faithful |
| 36 | Right card and 5n89: users fell sharply from the peak (WSJ via TechCrunch) | said-vs-reported.right.points[2]; 5n89 | techcrunch.com 3/29; cbsnews.com | 200 | CONFIRMED | — No figures are used |
| 38 | OpenAI has not published the cost per second, how many still use Sora, or why it named no replacement | unanswered.data.items; m4uq; xftc; r26r | deprecations; video guide; Help Center capture; CBS; The Verge; Sora post archive | 200 | CONFIRMED | — None of them does |
| 39 | OpenAI never said "too expensive"; it cited research priorities and compute | too-expensive.data; xrtu; fmz4; answer-chat.messages[1]; q8iy | same | 200 | CONFIRMED | — |
| 41 | Four forms: per second, tokens, credits, units | four-ways.data.code; jvfw | Google, Kling, Runway, BytePlus pages | 200 | CONFIRMED | — |
| 42 | Omni Flash at 720p: 5,792 × $17.50 ÷ 1M ≈ $0.10 | four-ways.data.code; table-google.rows[4]; r4w6 | ai.google.dev pricing; cloud.google.com pricing | 200 | CONFIRMED | — A5, A53; Google's own figure is "approximately $0.10 per second" |
| 43 | Gen-4.5 at 1280:720: 12 credits × $0.01 = $0.12 | four-ways.data.code; table-others.rows[4]; uxum | docs.dev.runwayml.com pricing and api | 200 | CONFIRMED | — A14, A15 |
| 44 | Kling 3.0 at 720p with audio: 0.9 × $0.14 = $0.126 (spoken 「大約零點一三」) | four-ways.data.code; table-others.rows[0]; pnnk | kling.ai | 200 | CONFIRMED | — A7, A8, A51 |
| 45 | One 8-second clip = per-second price × 8, in every 「一支 8 秒」 cell | four-ways; k98p; table-google; table-others | arith.mjs | — | CONFIRMED | — A1–A15 |
| 46 | Veo 3.1 $0.40 at 720p or 1080p with audio; $3.20 | table-google.rows[1]; 46dv; price-range.stats[2]; 7iae | ai.google.dev pricing | 200 | CONFIRMED | — |
| 47 | Veo 3.1 Fast $0.10 at 720p with audio; $0.80, the same as Sora | table-google.rows[2]; qhzt | ai.google.dev pricing; OpenAI archive | 200 | CONFIRMED | — |
| 48 | Veo 3.1 Lite $0.40 per 8 s | table-google.rows[3]; ftpn | ai.google.dev pricing | 200 | CONFIRMED | — A4 |
| 49 | The "Gemini Omni Flash" row is the GA model: ≈ $0.10 a second, ≈ $0.81 per 8 s | table-google.rows[4] | ai.google.dev pricing and deprecations | 200 | CONFIRMED | — gemini-omni-1.1-flash, "now generally available", no shutdown date |
| 50 | Seedance 2.0 at 720p 16:9 by tokens: ≈ $0.15 a second, ≈ $1.21 per 8 s | table-others.rows[1]; m6en; resale.left.points[0]; cddp | docs.byteplus.com model-pricing; create-video-generation-task-api | 200 | CONFIRMED | — A9–A11. The API page states the assumptions: 1280×720 at 720p 16:9, frame rate 24, durations 4–15 s (ruling c) |
| 51 | Grok Imagine Video 1.5: 720p, audio by default, $0.14 a second, $1.12 | table-others.rows[2]; ctak | docs.x.ai pricing and video | 200 | CONFIRMED | — |
| 52 | MiniMax-H3 at 768P: $0.08 a second, $0.64 | table-others.rows[3]; gkn6 | platform.minimax.io | 200 | CONFIRMED | — A13 |
| 54 | 8x at the same 720p with audio | price-range.stats[3]; u9xn | ai.google.dev pricing | 200 | CONFIRMED | — A19 |
| 55 | Veo 3.1 Fast from 720p to 4k: $0.10 → $0.30, both with audio | conditions.stats[0]; pu77 | ai.google.dev pricing | 200 | CONFIRMED | — |
| 56 | Kling 3.0 at 720p: silent $0.084, audio $0.126, silent one third cheaper | conditions.stats[1]; cesc | kling.ai | 200 | CONFIRMED | — A22, A23 |
| 57 | Veo 3.1 Lite at 1080p: $0.08, 8 s only | conditions.stats[2]; rhah | ai.google.dev pricing; veo doc | 200 | CONFIRMED | — |
| 58 | Veo 3.1: 4, 6 or 8 s; 8 s only from 1080p | clip-length.data.items[0]; wcet | ai.google.dev veo doc | 200 | CONFIRMED | — |
| 62 | Runway resells seedance2 at 36 credits = $0.36 (480p or 720p) | resale.right.points[0]; stcw | docs.dev.runwayml.com pricing | 200 | CONFIRMED | — A26 |
| 63 | Runway resells veo3.1_fast (audio) at 15 credits = $0.15, resolution not given | resale.right.points[1]; stcw | same | 200 | CONFIRMED | — A27 |
| 64 | Runway: 1 credit = $0.01 | resale.data.verdict; four-ways.data.code | same | 200 | CONFIRMED | — |
| 65 | The article exists, gives seconds per month, and is the description's first link | article-cta; yhr3; nkc3 | mokaair.com article; tools/video/core/metadata.mjs (`composeDescription` puts the article first) | 200 | CONFIRMED | — |
| 66 | 60 ÷ 8 = 7.5, so 8 clips; × 3 = 24 generations | short-steps; d23s; vv6q | arith.mjs | — | CONFIRMED | — A28–A30 |
| 69 | 24 × one clip: $9.60, $19.20, ≈ $24.19, $76.80 (spoken 不到十、大約十九、大約二十四、將近七十七) | short-table.data.rows; ykna; h3mi; na3m; 84pm | arith.mjs | — | CONFIRMED | — A31–A46 |
| 70 | Per usable second = price × 3; keep 1 in 10 means × 10 | short-table.rows[*][4]; usable-second; vrhs; 6bey; hmnm | arith.mjs | — | CONFIRMED | — A34, A38, A42, A46–A49 |
| 72 | App users should read the Help Center's discontinuation article | two-pages.data.steps[1]; nfcf | Help Center 09-19 capture | 200 | CONFIRMED | — |
| 73 | Veo 3.0: 2025-09-09 → 2026-06-30, replaced by the Veo 3.1 preview or the cloud GA models | shutdown-records.rows[1]; 6sz5 | ai.google.dev deprecations | 200 | CONFIRMED | — |
| 74 | Omni Flash preview: 2026-06-30 → 2026-09-30, three months, replaced by the GA 1.1 Flash | shutdown-records.rows[2]; 9udt | ai.google.dev deprecations and pricing | 200 | CONFIRMED | — 92 days (A56) |
| 76 | 184 days, about six months | notice-days.stats[0]; quc9 | deprecations | 200 | CONFIRMED | — A55 |
| 77 | That equals OpenAI's minimum notice for GA models | 489v; notice-days.data.source | deprecations | 200 | CONFIRMED | — "At least 6 months"; 3/24 → 9/24 is exactly six calendar months |
| 78 | Preview models may get as little as 2 weeks | notice-days.stats[2]; cj7s; notice-days.data.source | deprecations | 200 | CONFIRMED | — "such as 2 weeks"; the slide calls it the page's example |
| 80 | The outro's source lines | outro.data.lines | as #4 and #5 | 200 | CONFIRMED | — |
| 81 | 「Sora 當年的零點一，落在中間，並不貴」 | price-range/r5wh | arith.mjs (table) | — | CONFIRMED as an evaluation | — Supported by the table (A20). Unlabelled; see ruling e |
| 40, 79 | Opinion lines: my-reading, zcjd, pay-reason, three-lines, outro title | my-reading; answer-chat; pay-reason; three-lines; outro | brief.md | — | OUT OF SCOPE | — Labelled (我的讀法, 我付錢的理由, or first person) and in line with 站主觀點 |

## Arithmetic

Recomputed by `arith.mjs` from the official inputs above. The script also reads what video.json shows, so every comparison is mechanical. The Sora rank row checks whether 「落在中間，並不貴」 holds against the table; it tests no number.

| # | Expression | My result | What the script says | Verdict |
| --- | --- | --- | --- | --- |
| A1 | Sora 2: 0.10 x 8 | 0.8 | $0.80 | CONFIRMED |
| A2 | Veo 3.1: 0.40 x 8 | 3.2 | $3.20 | CONFIRMED |
| A3 | Veo 3.1 Fast: 0.10 x 8 | 0.8 | $0.80 | CONFIRMED |
| A4 | Veo 3.1 Lite: 0.05 x 8 | 0.4 | $0.40 | CONFIRMED |
| A5 | Omni Flash per s: 5792 x 17.50 / 1e6 | 0.10136 | ≈ $0.10 | CONFIRMED |
| A6 | Omni Flash 8 s: 0.10136 x 8 | 0.81088 | ≈ $0.81 | CONFIRMED |
| A7 | Kling 3.0 per s: 0.9 x 0.14 | 0.126 | $0.126 | CONFIRMED |
| A8 | Kling 3.0 8 s: 0.126 x 8 | 1.008 | ≈ $1.01 | CONFIRMED |
| A9 | Seedance 5 s: 5x1280x720x24/1024 tok x 7.0/1e6 (vs official 0.76 example) | 108000 tok = 0.7560 | 0.76 | CONFIRMED |
| A10 | Seedance per s: 21,600 tok x 7.0/1e6 | 0.1512 | ≈ $0.15 | CONFIRMED |
| A11 | Seedance 8 s: 172,800 tok x 7.0/1e6 | 1.2096 (alt: 0.76/5x8 = 1.216; 0.15x8 = 1.20) | ≈ $1.21 | CONFIRMED |
| A12 | Grok Imagine Video 1.5: 0.14 x 8 | 1.12 | $1.12 | CONFIRMED |
| A13 | MiniMax-H3: 0.08 x 8 | 0.64 | $0.64 | CONFIRMED |
| A14 | Runway Gen-4.5 per s: 12 x 0.01 | 0.12 | $0.12 | CONFIRMED |
| A15 | Runway Gen-4.5 8 s: 0.12 x 8 | 0.96 | $0.96 | CONFIRMED |
| A16 | Range min over both tables | 0.05 (Veo 3.1 Lite) | $0.05 | CONFIRMED |
| A17 | Range max over both tables | 0.4 (Veo 3.1) | $0.40 | CONFIRMED |
| A18 | Thumbnail / hook range | $0.05-$0.40 | 官方原話 vs 720p 一秒 $0.05–$0.40 / **$0.05** 到 $0.40 | CONFIRMED |
| A19 | Gap: 0.40 / 0.05 | 8 | 8 倍 | CONFIRMED |
| A20 | Sora 2 rank among the 10 per-second prices (ascending) | 3 of 10 (tied with Fast); median 0.1107 (Veo 3.1 Lite 0.0500, MiniMax-H3 0.0800, Sora 2 0.1000, Veo 3.1 Fast 0.1000, Omni Flash 0.1014, Gen-4.5 0.1200, Kling 3.0 0.1260, Grok 1.5 0.1400, Seedance 2.0 0.1512, Veo 3.1 0.4000) | Sora 當年的零點一，落在中間，並不貴。 | SUPPORTED (see ruling e) |
| A21 | Veo 3.1 Fast 720p -> 4k | 0.1 -> 0.3 | $0.10 → $0.30 | CONFIRMED |
| A22 | Kling 720p silent: 0.6 x 0.14 | 0.084 | $0.084 → $0.126 | CONFIRMED |
| A23 | Kling silent saving: 1 - 0.084/0.126 | 0.3333 | Kling 3.0 關掉聲音，一秒便宜三分之一。 | CONFIRMED |
| A24 | Veo 3.1 Lite 720p -> 1080p | 0.05 -> 0.08 | $0.05 → $0.08 | CONFIRMED |
| A25 | Sora 2 Batch / Standard | 0.5 | description: 同頁的 Batch 價是一半 | CONFIRMED |
| A26 | Runway seedance2: 36 x 0.01 | 0.36 (vs BytePlus 0.1512: x2.38) | Seedance 2.0：36 點＝$0.36 | CONFIRMED |
| A27 | Runway veo3.1_fast (audio): 15 x 0.01 | 0.15 (vs Gemini API 0.10: x1.50) | Veo 3.1 Fast 有聲：15 點＝$0.15 | CONFIRMED |
| A28 | 60 / 8 | 7.5 | 每支 8 秒 60 ÷ 8 = 7.5 | CONFIRMED |
| A29 | ceil(7.5) clips | 8 | 8 支 | CONFIRMED |
| A30 | 8 clips x 3 generations | 24 | 生成 24 次 | CONFIRMED |
| A31 | Veo 3.1 Lite: 8 s clip | 0.400 | $0.40 | CONFIRMED |
| A32 | Veo 3.1 Lite: 24 x clip | 9.600 | $9.60 | CONFIRMED |
| A33 | Veo 3.1 Lite: spoken total | 9.600 | 照官方價，Veo 3.1 Lite 生成二十四次，不到十美元。 | CONFIRMED |
| A34 | Veo 3.1 Lite: per usable second = 24 x clip / (8 x 8 s) = 3 x price | 0.1500 | $0.15 | CONFIRMED |
| A35 | Veo 3.1 Fast: 8 s clip | 0.800 | $0.80 | CONFIRMED |
| A36 | Veo 3.1 Fast: 24 x clip | 19.200 | $19.20 | CONFIRMED |
| A37 | Veo 3.1 Fast: spoken total | 19.200 | Veo 3.1 Fast 大約十九美元。 | CONFIRMED |
| A38 | Veo 3.1 Fast: per usable second = 24 x clip / (8 x 8 s) = 3 x price | 0.3000 | $0.30 | CONFIRMED |
| A39 | Kling 3.0: 8 s clip | 1.008 | ≈ $1.01 | CONFIRMED |
| A40 | Kling 3.0: 24 x clip | 24.192 | ≈ $24.19 | CONFIRMED |
| A41 | Kling 3.0: spoken total | 24.192 | Kling 3.0 有聲，大約二十四美元。 | CONFIRMED |
| A42 | Kling 3.0: per usable second = 24 x clip / (8 x 8 s) = 3 x price | 0.3780 | ≈ $0.38 | CONFIRMED |
| A43 | Veo 3.1: 8 s clip | 3.200 | $3.20 | CONFIRMED |
| A44 | Veo 3.1: 24 x clip | 76.800 | $76.80 | CONFIRMED |
| A45 | Veo 3.1: spoken total | 76.800 | 最貴的 Veo 3.1，將近七十七美元。 | CONFIRMED |
| A46 | Veo 3.1: per usable second = 24 x clip / (8 x 8 s) = 3 x price | 1.2000 | $1.20 | CONFIRMED |
| A47 | usable-second Lite: 0.05 x 3 | 0.15 | $0.15 ($0.05 × 3) | CONFIRMED |
| A48 | usable-second Veo 3.1: 0.40 x 3 | 1.2 | $1.20 ($0.40 × 3) | CONFIRMED |
| A49 | keep 1 in 10 -> x 10 (hmnm) | per usable second = 10 x price | 如果你十支才留一支，就乘以十。 | CONFIRMED |
| A50 | Short totals: 76.80 / 9.60 | 8.0000 | 同一支六十秒的短片，素材費差了八倍，差在你選哪個模型。 | CONFIRMED |
| A51 | Kling spoken: 0.126 -> 大約零點一三 | 0.13 | 其他家一樣換算：Kling 3.0 有聲，一秒大約零點一三美元。 | CONFIRMED |
| A52 | Seedance spoken: 0.1512 -> 大約零點一五 | 0.15 | BytePlus 賣的 Seedance 2.0 用 token 算，一秒大約零點一五。 | CONFIRMED |
| A53 | Omni spoken: 0.10136 -> 大約零點一 | 0.1 | Gemini Omni Flash 用 token 計價，換算下來一秒大約零點一。 | CONFIRMED |
| A54 | 2026-03-24 -> 2026-04-26 | 33 days | 33 天; 網頁與 App 離宣布 33 天 | CONFIRMED |
| A55 | 2026-03-24 -> 2026-09-24 | 184 days = 6 calendar months | 184 天; quc9 大約六個月 | CONFIRMED |
| A56 | 2026-06-30 -> 2026-09-30 (Omni preview) | 92 days = 3 calendar months | Gemini Omni Flash 的預覽版，從上線到關閉日只有三個月，替代是正式版。 | CONFIRMED |
| A57 | 2 weeks | 14 days | 2 週 | CONFIRMED |
| A58 | Weekday of 2026-03-24 | Tue | The Verge: "On Tuesday afternoon" | CONFIRMED |

## Rulings on round 1's suspicions

**(a) The $0.05–$0.40 range: CHANGED.** The thumbnail's 「官方原話 vs 一秒 $0.05–$0.40」 and the hook-range slide's 「各家一秒的價錢」 over 「$0.05 到 $0.40」 name no resolution. On the vendors' own pages, prices outside the range exist at other resolutions: Veo 3.1 at 4k is $0.60 a second (Google), Kling 3.0 at 4K is $0.42 (Kling), Seedance 2.0 at 4K is $0.78 and Seedance 2.0 Mini at 480p is $0.04 (BytePlus's price examples). Every 720p-class price on the pages read today lies inside the range: Google, Kling, BytePlus (2.0, Fast, Mini), xAI (1.5 and the older model), MiniMax (H3 and H3-Max at 768P), Runway, and OpenAI's archived sora-2 and sora-2-pro. So the range is true only as a 720p range. Now: thumbnail.data.sub 「官方原話 vs 720p 一秒 $0.05–$0.40」, hook-range.data.kicker 「各家 720p 一秒的價錢」. The hook line jbpw speaks no range and is unchanged. The price-range slide already says 「同樣 720p 有聲」. `render` redrew the hook-range state and the thumbnail, with no layout problem; I looked at both.

**(b) 「表上最便宜」: precise enough, no change.** The narration (qn2a 「表上最便宜的」) and the slide title (「表上的一秒，差多少」) both limit the claim to the table. Off the table, nothing at 720p-class is cheaper than $0.05 on the pages read. Runway's gen4_turbo is $0.05, a tie. Cheaper prices exist only at 480p (Seedance 2.0 Mini $0.04).

**(c) Seedance ≈ $1.21 per 8 s: stated well enough, no change.** The slide shows 「720p 16:9，token 換算」 with 「≈」. BytePlus's own API page confirms every assumption behind the number: the Seedance 2.0 series renders 720p 16:9 at 1280×720, the frame rate is 24, and `duration` accepts 4 to 15 seconds, so 8 s is allowed. With the pricing page's formula, 8 s is 172,800 tokens × $7.0/M = $1.2096. The pricing page itself calls the formula an estimate, which the 「≈」 covers. claims.md c15 now cites the API page. Optional for the owner: ux5y 「其他家的秒數，我在原廠頁沒讀到」 is still true as a statement of what the writer read, but BytePlus does publish 4–15 s.

**(d) h8a6 and the final export window: CHANGED.** OpenAI's page, in the 2026-09-19 capture, says "If a final export window is offered, we’ll notify you by email before it begins." and deletes data "after the period of time of any final export window passes (if we are able to offer one)". h8a6 presented the window as certain (「最後的匯出期一過」). It now reads 「停止之後，資料會永久刪除；如果有最後的匯出期，就等它結束再刪。」 (30 characters, no `say`, same id and reveal). The slide step 「匯出期過後／資料永久刪除」 does not say a final window exists and stays.

**(e) 「並不貴」 in r5wh: reported, no change.** It is an evaluation, not labelled as 我的讀法 on screen, although brief.md's 站主觀點 puts exactly this judgement inside 我的讀法. Presented as a reading of the table, it holds: Sora 2's $0.10 is third of the ten per-second prices, tied with Veo 3.1 Fast. Two are lower, six are higher, and the median is about $0.111 (A20). 「落在中間」 is loose, since Sora sits in the lower middle, but it is not false.

## Summary

- **Re-checked:** 65 claims, plus the opinion-label row. They are round 1's 6 changes, the 25 drawn with seed 20260928, and 34 claims that carry OpenAI quotes, media labels or arithmetic. Arithmetic: 58 expressions, all matching (arith.txt).
- **Results:** 62 CONFIRMED, including all 6 of round 1's changes, which stand. 3 CHANGED, which are **2 FACT changes**: the 720p range (#13 thumbnail and #20 hook-range kicker) and the conditional final export window (#24, h8a6). 0 NOT FOUND. OpenAI quotes: all word for word (The Verge and OpenAI's own Sora post; CBS), translations faithful. Media reports are labelled with their outlets, and the owner's reading is labelled as his.
- **Edits:** video.json has 3 strings changed and no line ids, scenes, lines or reveals changed. claims.md has notes on c7, c15 and c19, round-2 notes on three suspicions, and a round-2 progress entry. No number changed, so every `sources[].checked_on` stays 2026-09-28. brief.md is not touched.
- **Lint:** `node tools/video/cli.mjs lint --slug why-openai-killed-sora` → 0 errors, 0 warnings (101 lines, about 8.5 min). `render` into the scratchpad workdir redrew 1 state and the thumbnail, with no layout problems.
- **Still unresolved:** none of the claims. Before upload, a person should open the live Help Center page in a browser. It returns 403 to scripts, and the record is OpenAI's own page as archived on 2026-09-19. Re-check all prices in the upload week; the Omni Flash preview shuts down on 2026-09-30 and the slide is dated.
- **Report only:** cbs-quote's translation ends in 「。」 where the English is cut with "…". 「推進機器人」 is a loose rendering of "advance robotics". The description's 「每個價錢都寫了它假設的解析度」 has one exception, Runway's veo3.1_fast, and the slide itself says 頁面沒寫解析度.
- **Third round needed: no.** This round made 2 fact changes, not more than three.
