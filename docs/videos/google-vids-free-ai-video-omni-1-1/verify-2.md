# Verify round 2 (2026-09-30): google-vids-free-ai-video-omni-1-1, outline B rewrite

Independent second-round check by a different agent than round 1 (`verify-r1-20260930.md`). Scope: every claim round 1 changed, plus a sample of more than a third of the claims it confirmed (quotas and their scopes, the usage-scope sentence, the three eligibility wordings, avatars, clip specs, region limits, save-it, check-yourself, what-is, three controls, SynthID, policy), plus round 1's open items. Every page was fetched again today with curl (Mokaair-editorial UA, 1 s+ apart), comments, scripts and styles stripped. All answered HTTP 200 with no redirect. Raw pages, text extractions, the claim list (`claims-list.txt`, 159 items) and the edit script are in `<VIDEO_WORKDIR>/google-vids-free-ai-video-omni-1-1/_tools/verify-r2/`. Web search: 0 calls.

Sources (same ids as round 1): G1 blog.google announcement (2026-09-23); G2 Workspace Updates Omni 1.1 post (2026-09-23); G3 support.google.com/docs/answer/16143507; G4 /answer/15609411; G5 /answer/14925782; G6 /answer/13952129; G7 /answer/15082958; G8 Workspace Updates 2026-09-29 Flash Lite TTS post; B-TTS blog.google "Gemini 3.8 Flash TTS and Gemini 3.8 Flash-Lite TTS" (2026-09-23); H-VO /answer/15070345 (AI voiceovers); H-AV /answer/16334946 (AI avatars).

## Round 1's five fact changes, re-checked today

| # | Round 1 change | Official page today | Verdict |
|---|---|---|---|
| 1 | Chinese prompt: language table has no AI-video row; unlisted features are English-only | G5 Vids section lists image generation, AI voiceovers, AI avatars and Slides to Vids, no video-generation row; last section: "For other Google Workspace with Gemini features, English is the only supported language. To use Google Workspace with Gemini features that are supported in English only, set your Google Account language to English." G4: "Many AI features in Vids are only available in English at this time." G3 links G5 ("Learn about supported languages ..." → /docs/answer/14925782). | CONFIRMED |
| 2 | Age: Gemini get-started page says 18+ | G3 "Learn about Gemini features and plans" links /docs/answer/13952129 (G6). G6 "What you need to use Google Workspace with Gemini": "Be 18 or over." G1 and G3 say nothing about age. | CONFIRMED |
| 3 | Mobile: watch only, no editing | G7: "You can watch processed videos on your mobile device but you can't edit or add comments to videos." Every G3 flow starts "on your computer"; G1 "vids.new on your desktop". | CONFIRMED |
| 4 | New AI voiceover: 09-29 update says available now, listed plans only | G1: "Coming soon, Gemini 3.8 Flash-Lite text-to-speech in Google Vids will turn any script into a natural-sounding voiceover across 100+ languages." G8 (September 29, 2026): upgrading "the underlying text-to-speech (TTS) engine powering AI voiceovers and avatar narration"; "Rapid Release and Scheduled Release domains: Available now"; Availability lists Business, Enterprise, Education Plus, Consumer "Google AI Pro and Ultra", Essentials, Individual, Nonprofits, education add-ons. No free personal accounts. B-TTS (Sep 23): "Gemini 3.8 Flash-Lite TTS is rolling out starting today: ... For everyone: In Google Vids". Existing voiceover confirmed by G4 (personal: "Cost: 1 credit per voiceover"). | CONFIRMED (date conflict with B-TTS still stands; see suspicions) |
| 5 | 500-second default has no stated reset time | G4 default block ("unless otherwise specified in the tables below ... AI video clips: Up to 500 video clip seconds per month") has no reset sentence. "12:00 AM PT on the first day of each month" appears only in the Personal, Individual and AI Plus credit footnotes. | CONFIRMED |

Round 1's dependants of these five (hook frame 「公告沒寫清楚」, hook-proof sub, chza, jm3a, chapter, table title and column, unclear-ask, unclear-lang, unclear-mobile, voiceover, recap-five, wrap line 1, description, thumbnail "5 catches", 42a3, quota-table row 3) all read correctly against the pages above. G1 was re-read: it has no wording on prompt language, age, phones or upload regions, so 「公告沒寫清楚的五件事」 holds for all five.

## Round 1's open items, settled where an official page can

| Item | Official page | Result |
|---|---|---|
| "7 images" (specs slide 「7 張 參考圖上限」, nqwj) | G3 Create flow: "select Ingredients and upload up to 7 images". Edit flow (uploaded video): "select Add and upload up to 3 images". | CONFIRMED as the maximum, which is the Create flow the video demonstrates. Not changed; the Edit flow's lower limit of 3 is not mentioned in the script (owner may add 「新生成」 to the slide label if wanted). |
| nqbw vs G4 regions sentence | G3 lists only excluded regions for upload-and-edit. G4 "Supported countries & regions: You can use these features in all countries and regions where Google Workspace accounts are available." | CHANGED. 「官方只列了不能用的地方，沒有列出哪些地方一定能用。」 → 「其他地區，用量頁只概括寫，Workspace 有開放的地方都能用。」 (id kept). unclear-table row 4 「只列出不能用的地區」 → 「列了不能用的地區」 (slide only). recap-five 「有不能用的地區」 and ew36 unchanged (still true). claims.md c10 and the writer's note updated. |
| Do free personal accounts get the older voiceover? | G4 Personal table: "AI voice-over: Cost: 1 credit per voiceover" (so personal accounts do have AI voiceover). H-VO: "This feature requires an eligible Google Workspace or Google AI plan." G8 lists no free personal accounts for the engine upgrade. No page says which engine unlisted accounts use. | NOT SETTLED by an official page. Script only says 「限列名方案」 for the new version, which matches G8. No change. |
| Flash-Lite in the lexicon | cysz still says 「Gemini 三點八 Flash-Lite」 in `say`. `lint` gives 0 warnings; the lexicon has `"Flash": null`. | Lint does not need it. Not added. |

## Claim table (re-checked rows)

| # | claim | where | URL | HTTP | verdict | before → after |
|---|---|---|---|---|---|---|
| 1 | 這個免費的 AI 影片工具，有五件事，Google 的公告沒有寫清楚。 | hook:wchu | G1 | 200 | CONFIRMED | |
| 2 | 你以為公告寫了免費，就什麼都講清楚了。 | hook:gqa7 | G1 | 200 | CONFIRMED | |
| 3 | 這兩件事，公告裡一句都沒提 | hook-proof.data.sub | G1 | 200 | CONFIRMED | |
| 4 | 其實連中文提示能不能用、手機能不能做，公告都沒寫。 | hook-proof:chza | G1 | 200 | CONFIRMED | |
| 5 | Free, but **5 catches** | thumbnail | G1, G5–G8 | 200 | CONFIRMED | |
| 6 | description (公告沒寫清楚的五件事，說明頁怎麼回答; 新版 AI 旁白何時上線) | youtube.description | G1, G3–G8 | 200 | CONFIRMED | |
| 7 | 九月二十三日開始推出 / 模型 Gemini Omni 1.1 Flash | what-is:v46f, ezrk | G1, G2 | 200 | CONFIRMED | G2 "starting on September 23, 2026" |
| 8 | Google 的說法是，免費，而且任何人都能用。 | what-is:ueaj | G1 | 200 | CONFIRMED | |
| 9 | 第一步，在電腦打開 Vids 的網址／第二步，開始畫面選建立 AI 影片 | how-to:uhab, rrkk | G1, G3 | 200 | CONFIRMED | |
| 10 | 3–10 秒 / 1080p / 24 fps / 7 張 | specs.data; fk7e, 3d6b, tw82, nqwj | G3 | 200 | CONFIRMED | 7 = Create; Edit allows 3 |
| 11 | 個人帳號的虛擬化身功能只提供預設角色，不能自訂。 | reference-images:ikef | G4 | 200 | CONFIRMED | "^Personal Google accounts only have access to preset AI avatars" |
| 12 | 把虛擬化身當影片素材，目前另限英文及列名方案 | reference-images:24vb | G3 | 200 | CONFIRMED | "You can only use avatars as ingredients in EN and in the following accounts" |
| 13 | 延長場景、指定秒數、1080p 或升頻 | three-controls:9meb, xep9, r44r | G1, G2 | 200 | CONFIRMED | |
| 14 | 生成紀錄只存在這一次的工作階段裡／關掉分頁就不見 | save-it:hsue, itua | G3 | 200 | CONFIRMED | "When you close the Vids tab, the history disappears." |
| 15 | 事後想再編輯或取用，都得先插進 Vid | save-habit:tred | G3 | 200 | CONFIRMED | |
| 16 | 公告沒寫清楚的五件事 / 說明頁怎麼寫 | unclear-table.data title, columns | G1, G3–G8 | 200 | CONFIRMED | |
| 17 | 語言表沒列；沒列的只支援英文 | unclear-table.data.rows[0][1] | G5 | 200 | CONFIRMED | |
| 18 | Gemini 入門頁：滿 18 歲 | unclear-table.data.rows[1][1] | G6 | 200 | CONFIRMED | |
| 19 | 手機只能看，不能編輯 | unclear-table.data.rows[2][1] | G7 | 200 | CONFIRMED | |
| 20 | 只列出不能用的地區 | unclear-table.data.rows[3][1] | G3, G4 | 200 | CHANGED | 只列出不能用的地區 → 列了不能用的地區 |
| 21 | 新版 AI 旁白 / 9 月 29 日更新：已上線，限列名方案 | unclear-table.data.rows[4] | G8 | 200 | CONFIRMED | |
| 22 | 第五，新版 AI 旁白什麼時候上線。 | unclear-table:hqkj | G1, G8 | 200 | CONFIRMED | |
| 23 | 語言表沒有 AI 影片；沒列的功能只支援英文 | unclear-ask.data, 7xnu | G5, G4 | 200 | CONFIRMED | |
| 24 | 語言表: 列了圖片、旁白、虛擬化身 / AI 影片生成不在表上 / 沒列的功能：只支援英文 | unclear-lang.data.left | G5 | 200 | CONFIRMED | |
| 25 | 年齡: Gemini 入門頁：滿 18 歲 / 影片生成頁本身沒寫 | unclear-lang.data.right | G6, G3 | 200 | CONFIRMED | |
| 26 | 說明頁連到一張支援語言的表。 | unclear-lang:ixne | G3 | 200 | CONFIRMED | link to /answer/14925782 |
| 27 | 表上有圖片、旁白和虛擬化身，沒列的功能寫明只支援英文。 | unclear-lang:vzju | G5 | 200 | CONFIRMED | |
| 28 | 年齡則在生成頁連到的 Gemini 入門頁，寫要滿十八歲。 | unclear-lang:fsf9 | G3, G6 | 200 | CONFIRMED | |
| 29 | 官方的建議是，功能只支援英文時，把帳號語言改成英文。 | unclear-lang:3gje | G5, G6 | 200 | CONFIRMED | |
| 30 | Vids 入門頁：手機只能看，不能編輯 | unclear-mobile.data.sub | G7 | 200 | CONFIRMED | |
| 31 | 官方的步驟全部從電腦開啟 Google Vids 開始。 | unclear-mobile:nrat | G3 | 200 | CONFIRMED | |
| 32 | Vids 入門頁還寫，手機只能看影片，不能編輯。 | unclear-mobile:chsh | G7 | 200 | CONFIRMED | |
| 33 | 歐洲經濟區、英國、瑞士／伊利諾州、德州不能用 | region-limits.data; 9zm2, pcqq | G3 | 200 | CONFIRMED | |
| 34 | 上傳的影片超過十秒，只會修改最後十秒。 | region-limits:tjxx | G3 | 200 | CONFIRMED | |
| 35 | 官方只列了不能用的地方，沒有列出哪些地方一定能用。 | region-limits:nqbw | G3, G4 | 200 | CHANGED | → 其他地區，用量頁只概括寫，Workspace 有開放的地方都能用。 |
| 36 | 新版 AI 旁白：已上線 / 公告說一百多種語言 / 9 月 29 日更新：已上線，限列名方案 | voiceover.data | G1, G8 | 200 | CONFIRMED | |
| 37 | 第五件，新版的 AI 旁白。 | voiceover:wga7 | G8 | 200 | CONFIRMED | |
| 38 | 公告寫，Gemini 3.8 Flash-Lite 的文字轉語音即將推出。 | voiceover:cysz | G1 | 200 | CONFIRMED | |
| 39 | 公告說它會支援一百多種語言。 | voiceover:bp5e | G1 | 200 | CONFIRMED | |
| 40 | 九月二十九日，更新公告寫已經上線，限列名的方案。 | voiceover:u2gj | G8 | 200 | CONFIRMED | |
| 41 | 公告沒寫的地方，最實際的辦法，是看自己的畫面。 | check-yourself:jm3a | G4 | 200 | CONFIRMED | |
| 42 | 先登入對的帳號／沒有功能就不顯示選項／管理員可以關掉生成式 AI | check-yourself:radj, p83d, y76w | G4 | 200 | CONFIRMED | |
| 43 | 公告：任何 Google 或 Workspace 帳號 | who-can.data, cdjf | G1 | 200 | CONFIRMED | "anyone with a Google or Google Workspace account can generate high-quality videos at no cost" |
| 44 | 生成說明頁開頭：需要合格的 Workspace 訂閱 | who-can.data, ifi6 | G3 | 200 | CONFIRMED | "This feature requires an eligible Google Workspace subscription." |
| 45 | 用量頁：個人帳號也有專用的一格 | who-can.data, cyxg | G4 | 200 | CONFIRMED | "Personal use accounts / Personal Google Account" table |
| 46 | Most users can generate up to 50 videos per month. | two-pages.data; 3x75; quota-table row 1; us6x | G3 | 200 | CONFIRMED | verbatim; resets "12 AM PT on the first day of the month" |
| 47 | 6 video clips/month combined with AI avatars | two-pages.data; i84s; quota-table row 2; jdpm | G4 | 200 | CONFIRMED | verbatim (Personal, Individual; AI Plus also 6) |
| 48 | 500 秒 / 頁面沒寫 | quota-table row 3; bgex | G4 | 200 | CONFIRMED | |
| 49 | 前兩個寫每月一號太平洋時間午夜重設 | quota-table:42a3 | G3, G4 | 200 | CONFIRMED | row 2 rests on the credits footnote on the table heading |
| 50 | 額度與功能，Google 也寫之後都可能調整。 | quota-steps:z9hj | G4 | 200 | CONFIRMED | "subject to change" |
| 51 | Generated images and videos are for use only within Vids. | watermark.data; ynjh | G3 | 200 | CONFIRMED | verbatim |
| 52 | 生成式 AI 禁止使用政策／可能不代表真實世界 | policy:vrq8, t46a | G3 | 200 | CONFIRMED | |
| 53 | SynthID 隱形浮水印，讓人能驗證 | synthid:vavj, w386 | G1 | 200 | CONFIRMED | |
| 54 | 中文提示／18 歲／手機只能看／有不能用的地區／新版旁白 9 月 29 日已上線 | recap-five.data; 3yjx, is5i, js58, ew36, y9fj | G4–G8 | 200 | CONFIRMED | |
| 55 | 用電腦做，手機只能看 | wrap.data.lines[0] | G7 | 200 | CONFIRMED | |
| 56 | sources G1–G8 checked_on 2026-09-30 | sources | all | 200 | CONFIRMED | no source added; G4 already cited |

## Summary

- Re-checked: 56 table rows (about 95 of the 159 extracted items): all of round 1's CHANGED rows and more than a third of its CONFIRMED rows. CONFIRMED 54 rows, CHANGED 2 rows (one fact), NOT FOUND 0.
- FACT changes this round: 1. nqbw and unclear-table row 4 now reflect G4's general sentence "all countries and regions where Google Workspace accounts are available". claims.md c10, the writer's note and the progress log were updated. All five of round 1's fact changes hold on today's pages.
- Facts that expire soon: G8's voiceover availability (2026-09-29) and its conflict with B-TTS (2026-09-23, "For everyone: In Google Vids"); G2's rollout "starting on September 23, 2026"; all G4 quota numbers ("subject to change"); G6 is partly stale (still says Veo 3 and "at least through May 31, 2026"), so its "Be 18 or over" line could move without notice.
- Opinion mismatches against brief §站主觀點: none. Both quota figures are listed and none is chosen; insert-before-closing, SynthID and the prohibited-use policy are present. The brief's outline B premise conflict that round 1 reported is unchanged: it is for the owner.
- Listener pass (report only): no line over 40 characters, no verification narration, no parentheses or URLs. The new nqbw follows tjxx (「只會修改最後十秒」), so 「其他地區」 comes one sentence after the region list; a listener may want the link to be clearer. `Flash-Lite` is still not in the lexicon, but lint does not ask for it.
- Lint: `node tools/video/cli.mjs lint --slug google-vids-free-ai-video-omni-1-1` gives 0 errors, 0 warnings, 9.4 min, 124 lines.
- Suspected but not changed: the "7 張" figure is Create only (Edit: 3). G8 lists no free personal accounts, but B-TTS says "For everyone: In Google Vids", and no page says which voice engine unlisted accounts get. H-VO says voiceover "requires an eligible Google Workspace or Google AI plan", while G4 gives personal accounts voiceover at 1 credit. G4 and G5 disagree on AI-avatar languages (G4 lists 29 including Chinese; G5 lists 23 without Chinese); the script names no avatar languages. G3's Animate section says both "between 3 and 10 seconds" and "an 8-second clip"; the script does not cite Animate. The personal 6-clip reset date rests on the credits footnote.
- SECOND ROUND (third round) REQUIRED: no (1 fact change). nqbw's audio must be regenerated; round 1 already invalidated the old TTS.
