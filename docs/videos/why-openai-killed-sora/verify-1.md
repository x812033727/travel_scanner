# Verification round 1: why-openai-killed-sora

Verifier: claude-opus-5-5, a separate session from the writer's, 2026-09-28. Every number, name, date and quote was re-read today on the official page with the editorial user agent (curl, comments, scripts and tags stripped; at least 1.5 s between requests). Script-loaded pages (Kling, BytePlus, Runway API) were read from the data embedded in the served page. News outlets were used only for what they report, and third-party pages confirm nothing. Web searches used: 1 of 5. Helper files are in `/tmp/claude-0/-home-user-travel-scanner/674d9bf2-c3b1-5d19-bf6c-31efd377fe1e/scratchpad/videowork/why-openai-killed-sora/why-openai-killed-sora/_tools/verify1/`: claims-list.md and fields.txt were written before checking, plus pages/ (raw pages and status.log), arith.mjs/arith.txt and listener.mjs.

## Pages fetched

| URL | HTTP | What it gave |
| --- | --- | --- |
| https://developers.openai.com/api/docs/deprecations | 200 | "2026-03-24: Sora 2 video generation models and Videos API"; "On March 24th, 2026, we notified developers … removal from the API on September 24, 2026"; six rows (Videos API, sora-2, sora-2-pro, sora-2-2025-10-06, sora-2-2025-12-08, sora-2-pro-2025-10-06), all 2026-09-24, all "—". Notice periods: GA "At least 6 months"; specialized variants "At least 3 months"; preview "may be retired with much shorter notice, such as 2 weeks" |
| https://developers.openai.com/api/docs/pricing | 200 | No "sora" anywhere |
| https://web.archive.org/web/20260802044220/https://developers.openai.com/api/docs/pricing | 200 | OpenAI's own page ("FILE ARCHIVED ON 04:42:20 Aug 02, 2026"). "Video generation models / Prices per second". Standard: sora-2 720p $0.10; sora-2-pro $0.30 / $0.50 / $0.70. Batch: sora-2 $0.05; sora-2-pro $0.15 / $0.25 / $0.35 |
| https://developers.openai.com/api/docs/guides/video-generation | 200 | "The Sora 2 models and Videos API were shut down on September 24, 2026 and are no longer available. No one-to-one replacement API is available." Sora makes "clips with audio" |
| https://web.archive.org/web/20260727175148/https://developers.openai.com/api/docs/guides/video-generation | 200 (second try; the first was a connection reset) | Deprecation banner; "Generate videos up to 20 seconds" |
| https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation | 403 | Cloudflare challenge, as the writer found. Tried once |
| https://web.archive.org/web/20260630192218/https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation | 200 (second try) | og:site_name "OpenAI Help Center", archived 2026-06-30 19:22:18 UTC: "The Sora web and app experiences were discontinued on April 26, 2026." "The Sora API will be discontinued on September 24, 2026." Deletion "after the period of time of any final export window passes (if we are able to offer one)"; credits usable for Codex; no reason given |
| https://archive.org/wayback/available?url=help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation&timestamp=20260928 | 200 | The newest capture is 2026-09-19 08:10:42 |
| https://web.archive.org/web/20260919081042/https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation | 200 | Same wording as the 06-30 copy ("Updated: 18 days ago"); still no reason, and a final export window still "if … offered" |
| https://web.archive.org/cdx/search/cdx?url=help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation&output=json&from=2026&filter=statuscode:200 | 503 | Internet Archive "Temporarily Offline" (not used) |
| https://sora.chatgpt.com/p/s_69c2ec89c7f081919a93f637f6b250c2 | 403 | Cloudflare challenge; the web search found this OpenAI post |
| https://web.archive.org/web/20260908090419/https://sora.chatgpt.com/p/s_69c2ec89c7f081919a93f637f6b250c2 | 200 | "sora on Sora" (the official account): "An important update about Sora: Today, after careful internal discussion about our broader research priorities, we've made the difficult decision to discontinu…"; page data "uploadDate":"2026-03-24T19:56:57.781Z" |
| https://ai.google.dev/gemini-api/docs/pricing | 200 | Last updated 2026-09-24 UTC. Paid Tier, per second, "video with audio price (default)": Veo 3.1 $0.40 (720p and 1080p), $0.60 (4k); Fast $0.10 / $0.12 / $0.30; Lite $0.05 / $0.08, "(4k output not supported)". "You will only be charged if your video is successfully generated." "Gemini Omni Flash" is gemini-omni-1.1-flash, "now generally available": $17.50 (video) per 1M tokens, "5,792 tokens per second of 720p video … approximately $0.10 per second" (only a Standard table) |
| https://ai.google.dev/gemini-api/docs/veo | 200 | Last updated 2026-09-17 UTC. durationSeconds "4", "6", "8"; must be "8" with 1080p and 4k (Veo 3.1 and Fast) or with 1080p (Lite); "4k not available for Veo 3.1 Lite"; all three Veo 3.1 variants are "Preview" with output "Video with audio" |
| https://ai.google.dev/gemini-api/docs/deprecations | 200 | Last updated 2026-09-24 UTC. veo-3.0-generate-001: released September 9, 2025, shut down June 30, 2026, replaced by "veo-3.1-generate-preview or the GA models on the Gemini Enterprise Agent Platform". The three Veo 3.1 previews: "No shutdown date announced". gemini-omni-flash-preview: June 30, 2026 to September 30, 2026, replaced by gemini-omni-1.1-flash. The dates are "the earliest possible dates" |
| https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing | 200 | "Gemini Omni Flash, Gemini Omni 1.1 Flash": Video Output $17.50 per 1M tokens; "1931 … 360p …, 5792 … 720p …, 8688 … 1080p …, and 17376 … 4k video for video outputs (with audio)" |
| https://kling.ai/dev/pricing | 200 | Loaded by script; the embedded price data: "Video API Pricing 1 Unit = $0.14 (list price)". Kling 3.0 at 720P: "No Native Audio" 0.6 Units ($0.084) /s, "With Native Audio x No Voice Control" 0.9 Units ($0.126) /s; at 1080P 0.8 / 1.2 Units; at 4K 3.0 Units. "Failed video generations will not deduct any unit." No clip lengths |
| https://docs.byteplus.com/en/docs/ModelArk/1544106 | 200 (one redirect, to /docs/modelark/model-pricing) | Loaded by script; the embedded doc was updated 2026-09-28T05:30:59Z. dreamina-seedance-2-0-260128 "For 480p and 720p outputs: Input without video: 7.0" USD per M tokens. Example at 720p, 16:9, 5 s: "0.76 per video, 0.15 per second". "You are only charged for successfully generated videos." Token formula given. No audio split for Seedance 2.0. Discounts for mini and fast only, until 2026-10-07 14:00 (UTC+8) |
| https://docs.x.ai/developers/pricing | 200 | Last updated: September 21, 2026. grok-imagine-video-1.5: 480p $0.08, 720p $0.14, 1080p $0.25 per second |
| https://docs.x.ai/developers/model-capabilities/video/generation | 200 | "The allowed range is 1–15 seconds." (one range, not split by model); "Generated videos include an audio track by default." |
| https://platform.minimax.io/docs/guides/pricing-paygo | 200 | List Price: MiniMax-H3 768P $0.08 / second, 2K $0.13 / second; the output price has no audio condition |
| https://docs.dev.runwayml.com/guides/pricing/ | 200 | "Credits can be purchased for $0.01 per credit". gen4.5 12 credits per second; seedance2 (480p/720p) 36; veo3.1_fast (audio) 15; veo3.1 (audio) 40; hailuo3 (768P) 10; grok_imagine_1_5 (720p) 16; gemini_omni_flash (text to video) 10 |
| https://docs.dev.runwayml.com/api/ | 200 | Embedded OpenAPI: gen4.5 duration "Must be an integer from 2 to 10"; ratio includes "1280:720"; no audio parameter |
| https://higgsfield.ai/pricing | 200 | No "$" figure anywhere in the served source; the plans load by script |
| https://www.theverge.com/ai-artificial-intelligence/899850/openai-sora-ai-chatgpt | 200 | datePublished 2026-03-24T21:08:10Z. Reuters: "running it required so much compute power that it left other teams working with less". "OpenAI hasn't responded to a request for comment or otherwise explained the shift". The Sora app note in full ("Update, March 25th: Added note from the Sora app") |
| https://www.cbsnews.com/news/sora-ai-openai-discontinues/ | 200 | Published 2026-03-24 16:32 EDT, updated 18:00 EDT. Both OpenAI statements, word for word. "wanes in popularity among users, according to the Wall Street Journal" |
| https://techcrunch.com/2026/03/24/openais-sora-was-the-creepiest-app-on-your-phone-now-its-shutting-down/ | 200 | Published 2026-03-24T23:57:55Z: "OpenAI did not give a reason for the shut down". Embeds the @soraofficialapp post of March 24 ("timelines for the app and API") |
| https://techcrunch.com/2026/03/29/why-openai-really-shut-down-sora/ | 200 | Posted 2026-03-29 8:09 PM PDT: "According to a new WSJ investigation", the user count "peaked … and then collapsed" |
| https://www.businessinsider.com/openai-cfo-says-compute-crunch-is-forcing-tough-trade-offs-2026-4 | 200 | 2026-04-02. The CFO's interview quote "… because we don't have enough compute". BI's own sentence ties it to "discontinuing its video app Sora" |
| https://the-decoder.com/openai-sets-two-stage-sora-shutdown-with-app-closing-april-2026-and-api-following-in-september/ | 200 | 2026-03-28: April 26, 2026 and September 24, 2026 (cross-check only) |
| https://mokaair.com/zh-TW/life/ai-video-tools-compared | 200 | Live article, 更新日期 2026-09-19: monthly fees, monthly credits and seconds per plan (content pack `apps/api/app/guides/content/ai-video-tools-compared.json`, kind life) |

## Claim table

| # | Claim | Where | URL | HTTP | Verdict | Before → after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 「官方只給一句理由」 | youtube.title | cbsnews.com; theverge.com; sora.chatgpt.com (archive) | 200 | CHANGED | 「OpenAI 為什麼收掉 Sora？官方只給一句理由｜…」 → 「OpenAI 為什麼收掉 Sora？官方公告只給一句理由｜…」. The same day, OpenAI gave CBS two more statements that cite compute; only the App announcement has a single reason clause |
| 2 | Veo 3.1, Kling 3.0 and Seedance 2.0 have official prices today | youtube.title; tags | ai.google.dev pricing; kling.ai/dev/pricing; docs.byteplus.com | 200 | CONFIRMED | — |
| 3 | 「OpenAI 自己說過的話和三個日期」 | youtube.description | deprecations; Help Center archives | 200 | CONFIRMED | — |
| 4 | Prices are the official list prices of 2026-09-28 | youtube.description; outro.data.lines[0] | every price page above | 200 | CONFIRMED | — (Kling "list price", MiniMax "List Price", BytePlus undiscounted for Seedance 2.0, Google Paid Tier) |
| 5 | Sora 2's price comes from OpenAI's own pricing page, August 2026 archive | youtube.description; hook-price.stats[0].note; table-google.rows[0]; price-range.source; outro.data.lines[1] | web.archive.org …20260802044220/developers.openai.com/api/docs/pricing | 200 | CONFIRMED | — (a capture of developers.openai.com at 2026-08-02 04:42:20 UTC; the live page has no Sora) |
| 6 | Sora web and App stopped on 2026-04-26 | youtube.description; timeline.steps[1]; tn22 | help.openai.com; Wayback 06-30 and 09-19; the-decoder.com | 403 / 200 / 200 | CONFIRMED | — (from OpenAI's archived page; the live page refuses scripts) |
| 7 | Sora API closed on 2026-09-24 | youtube.description; timeline.steps[2]; tvf2; deprecation-table; shutdown-records.rows[0] | deprecations; guides/video-generation (live) | 200 | CONFIRMED | — |
| 8 | 「每個價錢都寫了它假設的解析度和有沒有聲音」 | youtube.description | docs.byteplus.com; platform.minimax.io; docs.dev.runwayml.com; OpenAI pricing archive | 200 | CHANGED | → 「每個價錢都寫了它假設的解析度；聲音會改變價錢的，也寫了有沒有聲音」. The Seedance 2.0, MiniMax-H3, Gen-4.5 and Sora 2 prices have no audio condition, and their rows state none. Kling's audio split is stated |
| 9 | Pages whose numbers cannot be read say 以官網為準 | youtube.description; table-others.rows[5]; bhxq | higgsfield.ai/pricing | 200 | CONFIRMED | — |
| 10 | No reported costs, revenue or user counts are quoted | youtube.description; unanswered.data.note; hr36 | video.json read in full | — | CONFIRMED | — |
| 11 | The product names in the tags exist (Veo 3.1 Lite, Grok Imagine, MiniMax H3, Runway API, Seedance 2.0, Kling 3.0) | youtube.tags | Google, xAI, MiniMax, Runway, BytePlus and Kling pages | 200 | CONFIRMED | — |
| 12 | 「Sora 已停止服務」 | thumbnail.data.tag; hook-title.data.tag | guides/video-generation (live); Help Center 09-19 archive | 200 | CONFIRMED | — |
| 13 | 「一秒 $0.05–$0.40」 | thumbnail.data.sub; hook-range.data.text | ai.google.dev pricing and the other table pages | 200 | CONFIRMED | — (true of the table's 720p-class rows; see suspicion a) |
| 14 | The App announcement gives one reason sentence | hook-title.chapter; hook-title.data.subtitle; tt9u | theverge.com; sora.chatgpt.com archive | 200 | CONFIRMED | — (the X post embedded by TechCrunch gives none) |
| 15 | "…after careful internal discussion about our broader research priorities, we've made the difficult decision…" is word for word | hook-quote.data.quote | theverge.com; sora.chatgpt.com archive | 200 | CONFIRMED | — |
| 16 | The translation 「……經過內部對更廣的研究優先順序仔細討論，我們做了困難的決定……」 and the paraphrase in tbe8 | hook-quote.data.translation; tbe8 | same | 200 | CONFIRMED | — |
| 17 | The note is dated 2026-03-24 and quoted by The Verge | hook-quote.data.kicker/source | sora.chatgpt.com archive (uploadDate 2026-03-24T19:56:57.781Z); theverge.com | 200 | CONFIRMED | — |
| 18 | Sora 2 costs $0.10 a second at 720p (tier) | hook-price.stats[0]; 2bmt; table-google.rows[0]; 7crj; price-range.stats[1]; r5wh | OpenAI pricing archive 2026-08-02 | 200 | CHANGED | The number stands, but $0.10 is the Standard price and Batch was $0.05, the same as Veo 3.1 Lite. The notes 「720p｜OpenAI 官方價目頁」 → 「720p，Standard 價｜OpenAI 官方價目頁」 (hook-price, table-google), and 「720p｜已停止」 → 「720p，Standard 價\n已停止」 (price-range). The description adds 「是 Standard 價（同頁的 Batch 價是一半）」 |
| 19 | Veo 3.1 Lite costs $0.05 a second at 720p with audio (spoken 「九月底」) | hook-price.stats[1]; 5kjd; four-ways.code; table-google.rows[3]; price-range.stats[0]; qn2a | ai.google.dev pricing | 200 | CONFIRMED | — |
| 20 | 「各家一秒的價錢」 run from $0.05 to $0.40 | hook-range.data.kicker; jbpw | as #13 | 200 | CONFIRMED | — (suspicion a) |
| 21 | On 3/24 the App and the API were announced to stop, the same day | timeline.steps[0]; whhz | deprecations; cbsnews.com ("consumer app and API"); techcrunch 3/24 (the @soraofficialapp post) | 200 | CONFIRMED | — |
| 22 | 4/26, 33 days after the announcement | timeline.steps[1]; tn22; notice-days.stats[1]; gewa | Help Center archives; arith.mjs | 200 | CONFIRMED | — |
| 23 | On 9/24 the developers' Videos API closed | timeline.steps[2]; tvf2 | deprecations; guides/video-generation | 200 | CONFIRMED | — |
| 24 | Data is deleted permanently once the final export window passes | timeline.steps[3]; h8a6 | Help Center archives | 200 | CONFIRMED | — (OpenAI makes the final window conditional; suspicion f) |
| 25 | 「Sora 的最後六個月」 (3/24 to 9/24) | timeline chapter and data.title | deprecations; arith.mjs | 200 | CONFIRMED | — |
| 26 | The rows: Videos API, sora-2, sora-2-pro and three dated snapshots, all closing 2026-09-24 | deprecation-table.data.rows; qm8a; p4jh | deprecations | 200 | CONFIRMED | — |
| 27 | Every Recommended replacement cell is "—", so no replacement is named | deprecation-table.data.rows[*][2]; p7mt; xvcc; gxbt; shutdown-records.rows[0] | deprecations; guides/video-generation ("No one-to-one replacement API is available") | 200 | CONFIRMED | — |
| 28 | The CBS quote is word for word | cbs-quote.data.quote | cbsnews.com | 200 | CONFIRMED | — |
| 29 | Its translation, and s884 and 3x7m | cbs-quote.data.translation; s884; 3x7m | cbsnews.com | 200 | CONFIRMED | — (「推進機器人」 for "to advance robotics" is loose, not wrong) |
| 30 | A spokesperson's statement to CBS News on 2026-03-24 | cbs-quote.data.kicker/source; p8yy | cbsnews.com | 200 | CONFIRMED | — |
| 31 | Left card: research priorities, from the App announcement | said-vs-reported.left.points[0]; pcc8 | theverge.com; Sora archive | 200 | CONFIRMED | — |
| 32 | Left card: focus and growing compute demand, the spokesperson to CBS | said-vs-reported.left.points[1]; pcc8 | cbsnews.com | 200 | CONFIRMED | — |
| 33 | Left card: compute trade-offs and the highest-value uses, from OpenAI's statement to CBS | said-vs-reported.left.points[2]; hv6h | cbsnews.com ("OpenAI said in its statement to CBS News") | 200 | CONFIRMED | — (OpenAI's own words, so it belongs on the left) |
| 34 | Right card: Sora used a lot of compute and other teams got less (Reuters via The Verge) | said-vs-reported.right.points[0]; ufsf | theverge.com | 200 | CONFIRMED | — |
| 35 | Right card: not enough compute, so some work is not pursued (the CFO's interview, via Business Insider) | said-vs-reported.right.points[1]; 5n89 | businessinsider.com | 200 | CONFIRMED | — (the quote does not name Sora; BI's own sentence does) |
| 36 | Right card: users fell sharply from the peak (the WSJ, via TechCrunch) | said-vs-reported.right.points[2]; 5n89 | techcrunch 3/29; cbsnews.com | 200 | CONFIRMED | — |
| 37 | 「當時 The Verge 和 TechCrunch 都寫，OpenAI 沒有另外解釋。」 | unanswered/zbve | theverge.com (21:08Z); techcrunch 3/24 (23:57Z); cbsnews.com (20:32Z, updated 22:00Z) | 200 | CHANGED | Line dropped. Both reports say this, but "no reason given" contradicts OpenAI's same-day statements to CBS, which the script plays just before it. TechCrunch ran three hours after CBS |
| 38 | OpenAI has not published the cost per second, how many people still use Sora, or why it named no replacement | unanswered.data.items; m4uq; xftc; r26r | deprecations; video guide; Help Center archives; CBS; The Verge; Sora archive | 200 | CONFIRMED | — (none of them does; the guide says only "No one-to-one replacement API is available") |
| 39 | OpenAI never said "too expensive"; it cited priorities and compute | too-expensive.data; xrtu; fmz4; answer-chat.messages[1]; q8iy | same | 200 | CONFIRMED | — |
| 40 | 「影片每一秒都在燒算力」 (my reading) | my-reading; hzcz; n7bn | brief.md | — | OUT OF SCOPE | — (labelled as an opinion; matches 站主觀點) |
| 41 | Price lists use four forms: per second, tokens, credits and units | four-ways.data.code; jvfw | Google, Kling, Runway and BytePlus pages | 200 | CONFIRMED | — |
| 42 | Omni Flash at 720p: 5,792 × $17.50 ÷ 1M ≈ $0.10 | four-ways.data.code; table-google.rows[4]; r4w6 | ai.google.dev pricing; cloud.google.com pricing | 200 | CONFIRMED | — ($0.10136) |
| 43 | Gen-4.5 at 1280:720: 12 credits × $0.01 = $0.12 | four-ways.data.code; table-others.rows[4]; uxum | docs.dev.runwayml.com pricing and api | 200 | CONFIRMED | — |
| 44 | Kling 3.0 at 720p with audio: 0.9 × $0.14 = $0.126 (spoken 「大約零點一三」) | four-ways.data.code; table-others.rows[0]; pnnk | kling.ai/dev/pricing | 200 | CONFIRMED | — |
| 45 | An 8-second clip = the per-second price × 8, in every 「一支 8 秒」 cell | four-ways.data.code; k98p; table-google; table-others | arith.mjs | — | CONFIRMED | — |
| 46 | Veo 3.1: $0.40 a second at 720p or 1080p with audio; $3.20 per 8 s | table-google.rows[1]; 46dv; price-range.stats[2]; 7iae | ai.google.dev pricing | 200 | CONFIRMED | — |
| 47 | Veo 3.1 Fast: $0.10 a second at 720p with audio; $0.80, the same as Sora | table-google.rows[2]; qhzt | ai.google.dev pricing; OpenAI archive | 200 | CONFIRMED | — |
| 48 | Veo 3.1 Lite: $0.40 per 8 s | table-google.rows[3]; ftpn | arith.mjs | — | CONFIRMED | — |
| 49 | The "Gemini Omni Flash" row is the GA model: ≈ $0.10 a second, ≈ $0.81 per 8 s | table-google.rows[4] | ai.google.dev pricing (the display name of gemini-omni-1.1-flash); cloud.google.com | 200 | CONFIRMED | — ($0.811; the price outlives the preview's 9/30 shutdown) |
| 50 | Seedance 2.0 at 720p 16:9, by tokens: ≈ $0.15 a second, ≈ $1.21 per 8 s (spoken 「大約零點一五」) | table-others.rows[1]; m6en; resale.left.points[0]; cddp | docs.byteplus.com | 200 | CONFIRMED | — (the formula at 1280×720 and 24 fps reproduces the official $0.76 example; 8 s = $1.2096; suspicion c) |
| 51 | Grok Imagine Video 1.5: 720p, audio by default, $0.14 a second, $1.12 | table-others.rows[2]; ctak | docs.x.ai pricing and video | 200 | CONFIRMED | — |
| 52 | MiniMax-H3 at 768P: $0.08 a second, $0.64 | table-others.rows[3]; gkn6 | platform.minimax.io | 200 | CONFIRMED | — |
| 53 | Higgsfield's numbers cannot be read, so 以官網為準 | table-others.rows[5]; bhxq | higgsfield.ai/pricing | 200 | CONFIRMED | — |
| 54 | An 8x gap at the same 720p with audio | price-range.stats[3]; u9xn | ai.google.dev pricing; arith.mjs | 200 | CONFIRMED | — |
| 55 | Veo 3.1 Fast from 720p to 4k: $0.10 → $0.30, both with audio | conditions.stats[0]; pu77 | ai.google.dev pricing | 200 | CONFIRMED | — |
| 56 | Kling 3.0 at 720p: silent $0.084 vs audio $0.126, one third cheaper | conditions.stats[1]; cesc | kling.ai/dev/pricing; arith.mjs | 200 | CONFIRMED | — |
| 57 | Veo 3.1 Lite at 1080p: $0.08, 8 s only | conditions.stats[2]; rhah | ai.google.dev pricing and veo doc | 200 | CONFIRMED | — |
| 58 | Veo 3.1: 4, 6 or 8 s; 8 s only from 1080p | clip-length.data.items[0]; wcet | ai.google.dev/gemini-api/docs/veo | 200 | CONFIRMED | — |
| 59 | Grok Imagine 1.5: 1 to 15 s | clip-length.data.items[1]; 32i6 | docs.x.ai video | 200 | CONFIRMED | — (the page gives one range, not one per model) |
| 60 | Runway Gen-4.5: 2 to 10 s | clip-length.data.items[2]; p956 | docs.dev.runwayml.com/api | 200 | CONFIRMED | — |
| 61 | Other vendors' clip lengths: 以原廠官網為準 | clip-length.data.items[3]; ux5y | Kling, BytePlus, MiniMax and Gemini pricing pages | 200 | CONFIRMED | — (none of those pages gives clip lengths) |
| 62 | Runway resells seedance2 at 36 credits = $0.36 (480p or 720p) | resale.right.points[0]; stcw | docs.dev.runwayml.com pricing | 200 | CONFIRMED | — |
| 63 | Runway resells veo3.1_fast (audio) at 15 credits = $0.15, resolution not stated | resale.right.points[1]; stcw | same | 200 | CONFIRMED | — |
| 64 | Runway: 1 credit = $0.01 | resale.data.verdict; four-ways.data.code | same | 200 | CONFIRMED | — |
| 65 | The article 〈AI 影片工具比較〉 exists, gives seconds per month, and is the first link in the description | article-cta; yhr3; nkc3 | mokaair.com article; content pack | 200 | CONFIRMED | — |
| 66 | 60 ÷ 8 = 7.5, so 8 clips; × 3 = 24 generations | short-steps; d23s; vv6q | arith.mjs | — | CONFIRMED | — |
| 67 | "You will only be charged if your video is successfully generated." and its translation | charged-quote.data; dp63 | ai.google.dev pricing | 200 | CONFIRMED | — |
| 68 | Google, Kling and BytePlus charge only for successful generations | tuki; en7w | ai.google.dev; kling.ai; docs.byteplus.com | 200 | CONFIRMED | — |
| 69 | 24 × one clip: $9.60, $19.20, ≈ $24.19, $76.80 (spoken 不到十、大約十九、大約二十四、將近七十七) | short-table.data.rows; ykna; h3mi; na3m; 84pm | arith.mjs | — | CONFIRMED | — (the Kling total uses the unrounded $1.008) |
| 70 | Per usable second: $0.15, $0.30, ≈ $0.38, $1.20 = price × 3; keep 1 in 10 means × 10 | short-table.data.rows[*][4]; usable-second; vrhs; 6bey; hmnm | arith.mjs | — | CONFIRMED | — |
| 71 | 「素材費差了八倍，差在你選哪一家、幾 P」 | short-table/fwd5 | arith.mjs; ai.google.dev pricing | 200 | CHANGED | → 「同一支六十秒的短片，素材費差了八倍，差在你選哪個模型。」 The 8x is Veo 3.1 vs Veo 3.1 Lite, from the same vendor at the same 720p |
| 72 | App users should read the Help Center's discontinuation article | two-pages.data.steps[1]; nfcf | Help Center 09-19 archive | 200 | CONFIRMED | — |
| 73 | Veo 3.0: released 2025-09-09, shut down 2026-06-30, replaced by the Veo 3.1 preview or GA models on the cloud | shutdown-records.rows[1]; 6sz5 | ai.google.dev deprecations | 200 | CONFIRMED | — |
| 74 | The Omni Flash preview: released 2026-06-30, shut down 2026-09-30 (three months), replaced by the GA Omni 1.1 Flash | shutdown-records.rows[2]; 9udt | ai.google.dev deprecations and pricing ("now generally available") | 200 | CONFIRMED | — (92 days) |
| 75 | Veo 3.1, Fast and Lite are previews on the Gemini API with no shutdown date | shutdown-records.rows[3]; fxq5 | ai.google.dev deprecations and veo doc | 200 | CONFIRMED | — |
| 76 | 184 days, about six months | notice-days.stats[0]; quc9 | arith.mjs | — | CONFIRMED | — |
| 77 | That equals OpenAI's minimum notice for GA models ("At least 6 months") | 489v; notice-days.data.source | deprecations | 200 | CONFIRMED | — |
| 78 | Preview models may get as little as 2 weeks | notice-days.stats[2]; cj7s | deprecations | 200 | CONFIRMED | — |
| 79 | Opinions and advice: 一秒影片的帳排不到前面; 先寫三行; 用得到、付得起、搬得走; 先算一秒，再看 demo | answer-chat.messages[1]; zcjd; three-lines; pay-reason; outro | brief.md | — | OUT OF SCOPE | — (labelled; matches 站主觀點) |
| 80 | The outro's source lines | outro.data.lines | as #4 and #5 | 200 | CONFIRMED | — |
| 81 | 「Sora 當年的零點一，落在中間，並不貴」 | r5wh | arith.mjs (third of ten on the table) | — | CONFIRMED | — (an evaluation; see the opinion check) |
| 82 | The slides are dated 「2026 年 9 月 28 日」 (tables, captions, the shutdown table) | table-google.data.title; table-others.data.columns[0]; short-table.data.title; four-ways.data.caption; price-range.data.source; conditions.data.source; resale.data.verdict; shutdown-records.data.title; charged-quote.data.source | every page read today | 200 | CONFIRMED | — |
| 83 | sources[].checked_on and the Help Center source | sources | Help Center 09-19 archive | 200 | CHANGED (source, not a fact) | The Help Center source moves from the 2026-06-30 capture to the 2026-09-19 one (same text, newer). Every checked_on stays 2026-09-28 |

Price assumptions behind the per-second tables, as the official pages give them:

| Price | Tier | Resolution | Audio | Length behind 「一支 8 秒」 |
| --- | --- | --- | --- | --- |
| Sora 2 $0.10 | Standard (Batch $0.05); now on the slides | 720p (1280×720) | Clips carry audio; the price has no audio split | Up to 20 s (archived guide) |
| Veo 3.1 $0.40 / Fast $0.10 / Lite $0.05 | Paid Tier (the only one) | 720p (Veo 3.1: 720p and 1080p) | "with audio (default)" | 4, 6 or 8 s |
| Gemini Omni Flash ≈ $0.10 | Standard (the only table) | 720p (5,792 tokens/s) | Rate is "(with audio)" (Cloud page); no split | Not on the price pages → 以官網為準 |
| Kling 3.0 $0.126 | List price; units come in prepaid packages | 720P | "With Native Audio x No Voice Control" | Not on the page → 以官網為準 |
| Seedance 2.0 ≈ $0.15 | Online-inference list price (discounts cover only mini and fast) | 720p 16:9, no video input | No audio split | Not on the page (the example is 5 s) → 以官網為準 |
| Grok Imagine Video 1.5 $0.14 | List | 720p | Audio track by default; no split | 1 to 15 s |
| MiniMax-H3 $0.08 | List Price | 768P | No audio split | Not on the page → 以官網為準 |
| Runway Gen-4.5 $0.12 | $0.01 per credit | 1280:720 | No audio parameter | 2 to 10 s |
| Higgsfield | — | — | — | 以官網為準 (no numbers served) |

## Summary

**Verdicts (83 claims):** CONFIRMED 75, CHANGED 6 (5 facts, plus 1 source link), NOT FOUND 0, OUT OF SCOPE 2. No claim is unresolved.

**Fact changes to video.json (five):**

1. `youtube.title`: 「官方只給一句理由」 → 「官方公告只給一句理由」. OpenAI's spokesperson gave CBS two more statements, about compute, on the same day. The chapter title and the subtitle already said 公告.
2. The Sora 2 tier. The $0.10 is the Standard price; Batch was $0.05, the same as Veo 3.1 Lite. hook-price, table-google and price-range now say 「Standard 價」, and the description says Batch was half.
3. `youtube.description`: 「每個價錢都寫了…有沒有聲音」 was not true of Seedance 2.0, MiniMax-H3, Gen-4.5 or Sora 2. It now reads 「聲音會改變價錢的，也寫了有沒有聲音」.
4. `unanswered/zbve` is dropped. TechCrunch's "did not give a reason" and The Verge's "hasn't … explained" contradict OpenAI's same-day statements to CBS, which play right before the line.
5. `short-table/fwd5`: 「差在你選哪一家、幾 P」 → 「差在你選哪個模型」. The 8x is Veo 3.1 vs Veo 3.1 Lite, from one vendor at the same 720p.

The Help Center source now points to the newer 2026-09-19 capture. claims.md c1, c4, c7, c9 (the name was removed), c10 and c22 match, and a round-1 entry was added under 進度. No `say` needed changing.

**Items the orchestrator flagged:**

- Help Center: the live page still returns 403. Both archives (2026-06-30 and 2026-09-19) are captures of OpenAI's own help.openai.com page, with identical text, and the description's source line labels the capture. The API dates match the live deprecations page, and the live guide says the API "were shut down on September 24, 2026". That archive holds the dates and the deletion wording, but not the App quote. The quote is from The Verge, and OpenAI's own Sora post (archived 2026-09-08, uploadDate 2026-03-24T19:56:57Z) carries the same words.
- Sora 2 $0.10: the archive is OpenAI's page, and the tier is now on the slides.
- Vendor prices: every tier, resolution, audio condition and clip length is in the table above. 以官網為準 is used for Higgsfield and for the clip lengths of Kling, Seedance, MiniMax and Omni Flash.
- CBS and TechCrunch: the script never says "only two sentences", and the contradictory "no reason" line is gone.

**Conflicts with brief.md (the source wins; brief.md not edited):** 站主觀點 says OpenAI's public reasons are 「只有兩句」, but CBS prints a third OpenAI statement ("Every day we're making tradeoffs in how we apply compute …"). 會過期的事實 says TechCrunch and The Verge wrote that OpenAI gave no explanation, which the same-day CBS statements contradict. The script follows the sources in both cases.

**Facts that expire soon (official dates seen):**

- The Omni Flash preview shuts down 2026-09-30 (Google deprecations page, last updated 2026-09-24), before the 2026-11-10 upload. The slide is dated, and the narration stays true.
- The Veo 3.1 previews have "No shutdown date announced" (2026-09-24). fxq5 limits this to 「到九月底」.
- Price pages: Gemini, last updated 2026-09-24; Veo doc, 2026-09-17; xAI pricing and video docs, September 21, 2026; BytePlus, updated 2026-09-28 05:30 UTC (discounts, not used, end 2026-10-07). Kling, MiniMax and Runway show no date. Re-check every price in the upload week.
- Help Center: if a final export window is announced, h8a6 still holds.

**Opinion check (report only):** every opinion line is labelled (我的讀法, 我付錢的理由, or lines starting with 我) and agrees with 站主觀點. `price-range/r5wh` 「並不貴」 is unlabelled; the brief puts it inside 我的讀法, but the table supports it (Sora is third of ten). `three-lines` is unlabelled advice that matches the brief.

**Listener pass (report only):** no line is over 40 units (the longest is conditions/pu77, 28). There is no process narration, no Latin term missing from the lexicon, no parentheses and no URL. None of 這個月, 上週, 今天, 最近 or 剛剛 appears. 九月底 appears twice, as a fixed date. 「當年」 is used twice (7crj, r5wh) for a price listed until September 2026; that is style. Some cards appear before the line that names them:

- said-vs-reported: the left card at pcc8 shows 「算力先給價值最高的用途」 before hv6h names it, and the right card at ufsf shows the BI and WSJ items before 5n89.
- resale: the left card appears at 8zb5, before cddp.
- answer-chat: the reply bubble that contains 「我的讀法是…」 appears at q8iy, before zcjd.

**Lint after edits:** `node tools/video/cli.mjs lint --slug why-openai-killed-sora` → 0 errors, 0 warnings (101 lines, about 8.5 min). `render` into the scratchpad workdir drew 79 states with 0 layout problems; I looked at the three edited slides.

**Suspicions left alone:**

- (a) 「$0.05–$0.40」 (thumbnail and hook-range, with the kicker 「各家一秒的價錢」) holds only for the table's 720p-class rows. At 4k, Veo 3.1 is $0.60 and Kling 3.0 is $0.42; at 480p, BytePlus lists Seedance 2.0 Mini at $0.04 a second. The owner could add 「720p」 to the kicker.
- (b) 「表上最便宜」 is true of the table only. MiniMax-H3-Max is $0.05 at 480P, and the old grok-imagine-video is $0.05 at 480p and $0.07 at 720p.
- (c) Seedance's ≈ $1.21 per 8 s assumes 1280×720 at 24 fps, inferred from the $0.76 example (0.15 × 8 = $1.20; 0.76 ÷ 5 × 8 = $1.216). The BytePlus page does not say whether 8 s is allowed.
- (d) Kling's 「原生音訊」 leaves out "No Voice Control"; 「推進機器人」 is a loose rendering of "robotics"; the Grok 1–15 s range is not given per model.
- (e) The quote source could also cite OpenAI's own Sora post (archive) as well as The Verge.
- (f) h8a6 「最後的匯出期一過」 presumes a final window; OpenAI says "if we are able to offer one".
- (g) A person should open the live Help Center page in a browser before upload.

**SECOND ROUND required: yes.** This round made five fact changes, more than three.
