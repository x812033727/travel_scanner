# Verify round 1 (2026-09-30): google-vids-free-ai-video-omni-1-1, outline B rewrite

Independent fact check of the video.json rewritten on 2026-09-30 for the owner's outline B. Earlier reports (verify-1.md, verify-p1-20260929*.md) checked the old draft and were used only as background. Every page below was fetched today with curl (Mokaair-editorial UA), comments and scripts stripped; all answered HTTP 200 with no redirect. Raw pages, text extractions, the extracted claim list (`claims-list.txt`, 159 items) and the edit scripts are in `<VIDEO_WORKDIR>/google-vids-free-ai-video-omni-1-1/_tools/verify-r1/`.

Sources: G1 blog.google announcement (2026-09-23); G2 Workspace Updates Omni 1.1 post (2026-09-23); G3 support.google.com/docs/answer/16143507 (generation help); G4 /answer/15609411 (usage/availability); G5 /answer/14925782 (supported languages); G6 /answer/13952129 (Get started with Google Workspace with Gemini, linked from G3's "Learn about Gemini features and plans"); G7 /answer/15082958 (Get started with Google Vids); G8 Workspace Updates 2026-09-29 "Create more natural, expressive AI voiceovers in Google Vids with upgraded Gemini 3.8 Flash Lite TTS". Also read: /answer/15070345 (AI voiceovers), /answer/16334946 (AI avatars), /answer/16970930 (personal avatar), /answer/15067819, /answer/16286470, policies.google.com generative-AI use policy, blog.google "Gemini 3.8 text-to-speech says hello" (2026-09-23). Web search: 4 calls.

## Main finding: three of the "five unclear things" are answered on official pages, and the fifth has shipped

| Item | Script before | Official page today |
|---|---|---|
| Chinese prompt | the language page has no AI-video row, so nothing is written | G5 ends: "For other Google Workspace with Gemini features, English is the only supported language. ... set your Google Account language to English." G4: "Many AI features in Vids are only available in English at this time." |
| Age | announcement and help pages never mention it | G6 (linked from G3's availability box), first requirement: "Be 18 or over." Personal-avatar page also says 18 or over. G1-G5 themselves are silent. |
| Mobile | steps start on a computer, phone not mentioned | G7: "You can watch processed videos on your mobile device but you can't edit or add comments to videos." |
| Upload region | only excluded regions are listed | CONFIRMED (G3 verbatim). Note G4 "Supported countries & regions: ... all countries and regions where Google Workspace accounts are available" (general, not upload-specific). |
| AI voiceover | coming soon, no date | AI voiceover already exists (G4 lists it for every plan; personal accounts pay 1 credit per voiceover). G1 called only the Gemini 3.8 Flash-Lite TTS upgrade "coming soon". G8 (2026-09-29): "Available now", availability lists Business, Enterprise, Education Plus, Essentials, Individual, Nonprofits, Google AI Pro and Ultra (no free personal accounts). The 09-23 TTS blog says Flash-Lite TTS is "rolling out starting today ... For everyone: In Google Vids", so the two official pages differ on the date; the script cites only the 09-29 page. |

Fix applied (rule 9, source wins): the frame is narrowed from "the official pages don't make five things clear" to "the announcement doesn't make five things clear". That is true of G1 for all five. The table and recap now give what the help pages say. Line ids are kept, and no scenes or lines were added. **Brief conflict for the owner:** outline B's premise ("有五件事官方頁還沒寫清楚", 中文提示／年齡／手機 as open questions, 旁白 coming soon) no longer holds. The owner should decide whether B still stands with this narrower frame.

Other change: G4 gives no reset time for the 500-second default (the "12:00 AM PT on the first day of each month" sentence sits only in the credits footnotes of the Personal, Individual and AI Plus tables). quota-table row 3 reset → 「頁面沒寫」, and 42a3 now says 「前兩個」.

## Focus checks requested by the lead

- Quota: G3 "Most users can generate up to 50 videos per month. The monthly limit resets at 12 AM PT on the first day of the month." CONFIRMED verbatim. G4 Personal Google Account and Workspace Individual both show "6 video clips/month combined with AI avatars" (Google AI Plus also 6). G4 default "AI video clips: Up to 500 video clip seconds per month" applies "unless otherwise specified in the tables below". Explicit 500 s rows: Business/Enterprise Standard and Plus, Essentials, Google AI Pro. 200 s: the Starter plans, Nonprofits and Education. The script's row labels (概括多數使用者／個人與 Individual／未另列時的預設) are CONFIRMED.
- Usage-scope sentence: "Generated images and videos are for use only within Vids." CONFIRMED verbatim on G3.
- Eligibility wordings: G1 "anyone with a Google or Google Workspace account can generate high-quality videos at no cost"; G3 "This feature requires an eligible Google Workspace subscription."; G4 "You can use basic Google Vids features with your Google Account. To use Gemini features in Vids, you can check your account type in the table below." (with a Personal table). G2 lists "Consumer: Users with personal Google accounts". who-can is CONFIRMED.
- Avatars for personal accounts: G4 "^Personal Google accounts only have access to preset AI avatars". G3 "You can only use avatars as ingredients in EN and in the following accounts" (no personal accounts). CONFIRMED.
- Supported-languages page: Vids sections for image generation (includes Chinese), AI voiceovers (23 languages, no Chinese), avatars (same 23), Slides to Vids (8), no AI-video row, and an English-only fallback for unlisted features (see above).
- Desktop only: G1 "vids.new on your desktop", every G3 flow starts "on your computer", G7 mobile = watch only. The claim now rests on G7.

## Claim table

| # | claim | where | source | HTTP | verdict | before → after / note |
|---|---|---|---|---|---|---|
| 1 | 用 Google 帳號免費做 AI 影片：Google Vids 的 Gemini Omni 1.1 能做什麼、額度到底多少 | youtube.title | G1, G3, G4 | 200 | CONFIRMED |  |
| 2 | Google Vids 開放任何 Google 帳號免費用 Gemini Omni 1.1 生成 AI 影片。這支示範怎麼做一段，並講清楚公告沒寫清楚的五件事，說明頁怎麼回答。 給想用 AI 做影片、不想付費也不想學剪輯的人。  涵蓋：電腦上怎麼做一段、關分頁前要先插進 Vid、中文提示與年齡條件、手機能不能生成、上傳影片的地區限制、新版 AI 旁白何時上線；兩份說明頁的額度為什麼寫得不一樣、SynthID 浮水印與「只供在 Vids 內使用」。本站沒有實測生成效果。 | youtube.description | G1, G3, G7, G8 | 200 | CHANGED | Google Vids 開放任何 Google 帳號免費用 Gemini Omni 1.1 生成 AI 影片。這支示範怎麼做一段，並講清楚官方頁沒寫清楚的五件事。 給想用 AI 做影片、不想付費也不想學剪輯的人。  涵蓋：電腦上怎麼做一段、關分頁前要先插進 Vid、中文提示與年齡條件、手機能不能生成、上傳影片的地區限制、AI 旁白何時上線；兩份說明頁的額度為什麼寫得不一樣、SynthID 浮水印與「只供在 Vids 內使用」。本站沒有實測生成效果。 → Google Vids 開放任何 Google 帳號免費用 Gemini Omni 1.1 生成 AI 影片。這支示範怎麼做一段，並講清楚公告沒寫清楚的五件事，說明頁怎麼回答。 給想用 AI 做影片、不想付費也不想學剪輯的人。  涵蓋：電腦上怎麼做一段、關分頁前要先插進 Vid、中文提示與年齡條件、手機能不能生成、上傳影片的地區限制、新版 AI 旁白何時上線；兩份說明頁的額度為什麼寫得不一樣、SynthID 浮水印與「只供在 Vids 內使用」。本站沒有實測生成效果。 |
| 3 | Google Vids, Gemini Omni, free AI video, AI 影片, Omni 1.1, SynthID, Google Vids limits, 免費 AI 工具, AI video generator | youtube.tags | G1, G3, G4 | 200 | CONFIRMED |  |
| 4 | {"tag": "FREE AI VIDEO", "headline": "Free, but\n**5 catches**", "sub": "Google Vids · Omni 1.1"} | thumbnail | G5, G6, G7, G8 | 200 | CHANGED | Free, but **5 unknowns** → Free, but **5 catches** (three of five are no longer unknowns) |
| 5 | 免費 AI 影片 ／ 免費 AI 影片 **五件事**沒寫清楚 ／ Google Vids 的 Gemini Omni 1.1 | hook.data (unchanged fields) | G1 | 200 | CONFIRMED |  |
| 6 | 這個免費的 AI 影片工具，有五件事，Google 的公告沒有寫清楚。 | hook:wchu | G1 | 200 | CHANGED | 這個免費的 AI 影片工具，有五件事，Google 的官方頁沒有寫清楚。 → 這個免費的 AI 影片工具，有五件事，Google 的公告沒有寫清楚。; frame narrowed: the ANNOUNCEMENT leaves five things unclear; help pages answer three of them |
| 7 | 你以為公告寫了免費，就什麼都講清楚了。 | hook:gqa7 | G1 | 200 | CHANGED | 你以為免費的意思，就是官方頁什麼都寫好了。 → 你以為公告寫了免費，就什麼都講清楚了。; follows the reframed hook |
| 8 | 這兩件事，公告裡一句都沒提 | hook-proof.data.sub | G1 | 200 | CHANGED | 這兩件事，官方頁都沒有一句話 → 這兩件事，公告裡一句都沒提 |
| 9 | 其實 ／ 中文？手機？ | hook-proof.data (unchanged fields) | G1 | 200 | CONFIRMED |  |
| 10 | 其實連中文提示能不能用、手機能不能做，公告都沒寫。 | hook-proof:chza | G1 | 200 | CHANGED | 其實連中文提示能不能用、手機能不能做，都沒寫。 → 其實連中文提示能不能用、手機能不能做，公告都沒寫。; G1 has no language or phone wording (only 'vids.new on your desktop') |
| 11 | 動手之前先知道，才不會白做工。 | hook-proof:yvre | G1 | 200 | OUT OF SCOPE |  |
| 12 | 先從頭講起，它到底是什麼？ | hook-proof:yfab | G1 | 200 | OUT OF SCOPE |  |
| 13 | 先講它是什麼 ／ Google Vids 裡的 AI 影片生成 ／ 模型：Gemini Omni 1.1 Flash ／ 9 月 23 日開始推出 ／ Google 的說法：免費、任何人 | what-is.data (unchanged fields) | G1, G2 | 200 | CONFIRMED |  |
| 14 | 先用一句話講清楚。 | what-is:rn39 | G1, G2 | 200 | OUT OF SCOPE |  |
| 15 | 它是 Google Vids 裡的 AI 影片生成功能。 | what-is:5wgf | G1, G2 | 200 | CONFIRMED |  |
| 16 | 背後的模型叫 Gemini Omni 1.1 Flash。 | what-is:ezrk | G1, G2 | 200 | CONFIRMED |  |
| 17 | 九月二十三日開始推出。 | what-is:v46f | G1, G2 | 200 | CONFIRMED |  |
| 18 | Google 的說法是，免費，而且任何人都能用。 | what-is:ueaj | G1, G2 | 200 | CONFIRMED |  |
| 19 | Google 官方部落格的標題 ／ Anyone can make stunning HD videos with Gemini Omni in Google Vids ／ 任何人都能在 Google Vids 用 Gemini Omni 做出高畫質影片 ／ Google 官方部落格，2026-09-23 | twist.data (unchanged fields) | G1 | 200 | CONFIRMED |  |
| 20 | 先看 Google 怎麼宣布的。 | twist:a3e7 | G1 | 200 | OUT OF SCOPE |  |
| 21 | 公告的標題寫，任何人都能做高畫質影片。 | twist:rkgw | G1 | 200 | CONFIRMED |  |
| 22 | Google 自己的宣傳用語 ／ 免費・任何人 ／ 內文寫：有 Google 或 Workspace 帳號，就能免費生成 | promo-words.data (unchanged fields) | G1 | 200 | CONFIRMED |  |
| 23 | 內文補了一句，有 Google 或 Workspace 帳號，就能免費生成。 | promo-words:8p6r | G1 | 200 | CONFIRMED |  |
| 24 | 免費和任何人，都是 Google 的宣傳用語。 | promo-words:zbyy | G1 | 200 | CONFIRMED |  |
| 25 | 那實際動手，要怎麼做一段？ | promo-words:gjup | G1 | 200 | OUT OF SCOPE |  |
| 26 | 動手做一段 ／ 開 vids.new ／ 在電腦上 ／ Create AI videos ／ 再選側欄的 Create ／ 寫提示 ／ 主題、地點、動作、鏡頭 ／ 選比例與長度 ／ 16:9 或 9:16、3 到 10 秒 ／ 生成 ／ 等它做完 | how-to.data (unchanged fields) | G1, G3 | 200 | CONFIRMED |  |
| 27 | 照 Google 說明頁的步驟，一共五步。 | how-to:dfmy | G1, G3 | 200 | CONFIRMED |  |
| 28 | 第一步，在電腦打開 Vids 的網址。 | how-to:uhab | G1, G3 | 200 | CONFIRMED |  |
| 29 | 第二步，開始畫面選建立 AI 影片。 | how-to:rrkk | G1, G3 | 200 | CONFIRMED |  |
| 30 | 第三步，寫提示，主題、地點、動作、鏡頭都寫進去。 | how-to:9i94 | G1, G3 | 200 | CONFIRMED |  |
| 31 | 第四步，選畫面比例和長度，橫的直的，三到十秒。 | how-to:qfwd | G1, G3 | 200 | CONFIRMED |  |
| 32 | 第五步，按生成，然後等它做完。 | how-to:q9te | G1, G3 | 200 | CONFIRMED |  |
| 33 | 第一次做，先挑一個簡單的畫面練手。 | how-to:skjm | G1, G3 | 200 | OUT OF SCOPE |  |
| 34 | 提示怎麼寫差很多 ／ 做一段很美的海邊影片 ／ 黃昏海邊，一隻狗沿著浪花奔跑，低角度慢慢跟拍，暖色光線，海浪聲 | prompt-tips.data (unchanged fields) | G3 | 200 | CONFIRMED |  |
| 35 | 提示怎麼寫，差別很大。 | prompt-tips:pzf6 | G3 | 200 | OUT OF SCOPE |  |
| 36 | Google 說明頁建議，連對白、聲音和語氣也寫進去。 | prompt-tips:csj2 | G3 | 200 | CONFIRMED |  |
| 37 | 「做一段很美的海邊影片」，太模糊，模型只能亂猜。 | prompt-tips:fe7c | G3 | 200 | CONFIRMED |  |
| 38 | 換成黃昏、一隻狗、低角度跟拍、暖色光線和海浪聲，就具體多了。 | prompt-tips:nz9d | G3 | 200 | CONFIRMED |  |
| 39 | 我的看法是，寫提示就像跟攝影師講分鏡。 | prompt-tips:rnw8 | - | 200 | OUT OF SCOPE (opinion) |  |
| 40 | 一段片段的規格 ／ 3–10 秒 ／ 每段長度 ／ 1080p ／ 最高解析度 ／ 24 fps ／ 影格率 ／ 7 張 ／ 參考圖上限 ／ Google 說明頁，2026-09 | specs.data (unchanged fields) | G3 | 200 | CONFIRMED |  |
| 41 | 每一段片段的規格是這樣。 | specs:x6hs | G3 | 200 | OUT OF SCOPE |  |
| 42 | 長度三到十秒。 | specs:fk7e | G3 | 200 | CONFIRMED |  |
| 43 | 最高是全高清一〇八〇。 | specs:3d6b | G3 | 200 | CONFIRMED |  |
| 44 | 影格率每秒二十四格。 | specs:tw82 | G3 | 200 | CONFIRMED |  |
| 45 | 參考圖的上限是七張。 | specs:nqwj | G3 | 200 | CONFIRMED |  |
| 46 | 十秒很短，想做長一點，還有新的控制可以用。 | specs:xfxp | G3 | 200 | OUT OF SCOPE |  |
| 47 | 參考圖與虛擬化身 ／ 參考圖：讓畫面照你的素材走 ／ 個人帳號只能用預設虛擬化身 ／ 化身當影片素材：限英文與列名方案 | reference-images.data (unchanged fields) | G3, G4 | 200 | CONFIRMED |  |
| 48 | 參考圖是讓畫面照你的素材走的方法。 | reference-images:ruqj | G3, G4 | 200 | CONFIRMED |  |
| 49 | 個人帳號的虛擬化身功能只提供預設角色，不能自訂。 | reference-images:ikef | G3, G4 | 200 | CONFIRMED |  |
| 50 | 把虛擬化身當影片素材，目前另限英文及列名方案，要先查資格。 | reference-images:24vb | G3, G4 | 200 | CONFIRMED |  |
| 51 | 這次新增的三個控制 ／ 延長場景 ／ 光線、角色外觀保持一致 ／ 指定秒數 ／ 對上故事和旁白 ／ 1080p ／ 新生成或把舊片段升頻 | three-controls.data (unchanged fields) | G1, G2 | 200 | CONFIRMED |  |
| 52 | 這次多了三個控制。 | three-controls:7ia3 | G1, G2 | 200 | OUT OF SCOPE |  |
| 53 | 第一，延長場景，Google 說光線和角色外觀會保持一致。 | three-controls:9meb | G1, G2 | 200 | CONFIRMED |  |
| 54 | 第二，可以指定確切秒數，對上你的故事和旁白。 | three-controls:xep9 | G1, G2 | 200 | CONFIRMED |  |
| 55 | 第三，直接生成全高清，或把舊片段升上去。 | three-controls:r44r | G1, G2 | 200 | CONFIRMED |  |
| 56 | 延長之後好不好看，還是要自己看過才知道。 | three-controls:krnz | - | 200 | OUT OF SCOPE (opinion) |  |
| 57 | 最不能漏的一步 ／ 先插進 Vid ／ 關掉分頁，生成紀錄就消失 | save-it.data (unchanged fields) | G3 | 200 | CONFIRMED |  |
| 58 | 做完一段，有一步千萬不能漏。 | save-it:33ji | G3 | 200 | OUT OF SCOPE |  |
| 59 | 生成紀錄只存在這一次的工作階段裡。 | save-it:hsue | G3 | 200 | CONFIRMED |  |
| 60 | 你一關掉分頁，剛剛生成的片段就不見了。 | save-it:itua | G3 | 200 | CONFIRMED |  |
| 61 | 存下來的習慣 ／ 做好一段，先插進自己的 Vid ／ 事後要編輯或取用，靠這一步 ／ 滿意一段，就插進一段 | save-habit.data (unchanged fields) | G3 | 200 | CONFIRMED |  |
| 62 | 所以做好一段，先把它插進你自己的 Vid，才算存下來。 | save-habit:s7f6 | G3 | 200 | CONFIRMED |  |
| 63 | 說明頁也寫，事後想再編輯或取用，都得先插進 Vid。 | save-habit:tred | G3 | 200 | CONFIRMED |  |
| 64 | 養成習慣：滿意一段，就插進一段。 | save-habit:n9n5 | G3 | 200 | OUT OF SCOPE |  |
| 65 | 做得出來很簡單，那官方到底哪些事沒說清楚？ | save-habit:mrxt | G3 | 200 | OUT OF SCOPE |  |
| 66 | 公告沒寫清楚的五件事 | unclear-table.data.title | G1, G3, G5, G6, G7, G8 | 200 | CHANGED | 官方頁沒寫清楚的五件事 → 公告沒寫清楚的五件事 |
| 67 | 說明頁怎麼寫 | unclear-table.data.columns[1] | G1, G3, G5, G6, G7, G8 | 200 | CHANGED | 官方頁現況 → 說明頁怎麼寫 |
| 68 | 語言表沒列；沒列的只支援英文 | unclear-table.data.rows[0][1] | G1, G3, G5, G6, G7, G8 | 200 | CHANGED | 語言支援頁沒有 AI 影片這一列 → 語言表沒列；沒列的只支援英文 |
| 69 | Gemini 入門頁：滿 18 歲 | unclear-table.data.rows[1][1] | G1, G3, G5, G6, G7, G8 | 200 | CHANGED | 公告與說明頁都沒提 → Gemini 入門頁：滿 18 歲 |
| 70 | 手機只能看，不能編輯 | unclear-table.data.rows[2][1] | G1, G3, G5, G6, G7, G8 | 200 | CHANGED | 步驟從電腦開始，沒說手機 → 手機只能看，不能編輯 |
| 71 | 新版 AI 旁白 | unclear-table.data.rows[4][0] | G1, G3, G5, G6, G7, G8 | 200 | CHANGED | AI 旁白 → 新版 AI 旁白 |
| 72 | 9 月 29 日更新：已上線，限列名方案 | unclear-table.data.rows[4][1] | G1, G3, G5, G6, G7, G8 | 200 | CHANGED | 寫著即將推出，沒有日期 → 9 月 29 日更新：已上線，限列名方案 |
| 73 | 事項 ／ 中文提示 ／ 年齡條件 ／ 手機能不能生成 ／ 上傳影片來改 ／ 只列出不能用的地區 | unclear-table.data (unchanged fields) | G1, G3, G5, G6, G7, G8 | 200 | CONFIRMED |  |
| 74 | Google Vids AI 影片公告沒寫清楚的五件事 | unclear-table.chapter | G1, G3, G5, G6, G7, G8 | 200 | CHANGED | Google Vids AI 影片官方沒寫清楚的五件事 → Google Vids AI 影片公告沒寫清楚的五件事 |
| 75 | 先把五件事列出來。 | unclear-table:xi4n | G1, G3, G5, G6, G7, G8 | 200 | OUT OF SCOPE |  |
| 76 | 第一，中文提示能不能用。 | unclear-table:u66y | G1, G3, G5, G6, G7, G8 | 200 | OUT OF SCOPE |  |
| 77 | 第二，有沒有年齡條件。 | unclear-table:47u8 | G1, G3, G5, G6, G7, G8 | 200 | OUT OF SCOPE |  |
| 78 | 第三，手機能不能生成。 | unclear-table:hyqa | G1, G3, G5, G6, G7, G8 | 200 | OUT OF SCOPE |  |
| 79 | 第四，上傳影片來改的地區限制。 | unclear-table:mksp | G1, G3, G5, G6, G7, G8 | 200 | OUT OF SCOPE |  |
| 80 | 第五，新版 AI 旁白什麼時候上線。 | unclear-table:hqkj | G1, G3, G5, G6, G7, G8 | 200 | CHANGED | 第五，AI 旁白什麼時候上線。 → 第五，新版 AI 旁白什麼時候上線。; AI voiceover already exists (G4); only the upgraded engine was 'coming soon' |
| 81 | 一件一件來看。 | unclear-table:qfzs | G1, G3, G5, G6, G7, G8 | 200 | OUT OF SCOPE |  |
| 82 | 語言表沒有 AI 影片；沒列的功能只支援英文 | unclear-ask.data.messages[1].text | G5, G4 | 200 | CHANGED | 支援語言表沒有列 AI 影片生成 → 語言表沒有 AI 影片；沒列的功能只支援英文 |
| 83 | 中文提示，能用嗎？ ／ 我可以用中文寫提示嗎？ | unclear-ask.data (unchanged fields) | G5, G4 | 200 | CONFIRMED |  |
| 84 | 先問第一件，中文提示。 | unclear-ask:x24z | G5, G4 | 200 | OUT OF SCOPE |  |
| 85 | 你會想問的是，可以用中文寫提示嗎？ | unclear-ask:tnsk | G5, G4 | 200 | OUT OF SCOPE |  |
| 86 | 官方頁的回應是，語言表沒有 AI 影片，沒列的只支援英文。 | unclear-ask:7xnu | G5, G4 | 200 | CHANGED | 官方頁的回應是，支援語言表沒有列 AI 影片生成。 → 官方頁的回應是，語言表沒有 AI 影片，沒列的只支援英文。; G5 'For other ... features, English is the only supported language' |
| 87 | 語言表 | unclear-lang.data.left.heading | G5, G6, G3 | 200 | CHANGED | 頁面有寫 → 語言表 |
| 88 | 列了圖片、旁白、虛擬化身 | unclear-lang.data.left.points[0] | G5, G6, G3 | 200 | CHANGED | 圖片生成的語言 → 列了圖片、旁白、虛擬化身 |
| 89 | AI 影片生成不在表上 | unclear-lang.data.left.points[1] | G5, G6, G3 | 200 | CHANGED | AI 旁白的語言 → AI 影片生成不在表上 |
| 90 | 沒列的功能：只支援英文 | unclear-lang.data.left.points[2] | G5, G6, G3 | 200 | CHANGED | 虛擬化身的語言 → 沒列的功能：只支援英文 |
| 91 | 年齡 | unclear-lang.data.right.heading | G5, G6, G3 | 200 | CHANGED | 頁面沒寫 → 年齡 |
| 92 | Gemini 入門頁：滿 18 歲 | unclear-lang.data.right.points[0] | G5, G6, G3 | 200 | CHANGED | AI 影片生成的語言 → Gemini 入門頁：滿 18 歲 |
| 93 | 影片生成頁本身沒寫 | unclear-lang.data.right.points[1] | G5, G6, G3 | 200 | CHANGED | 年齡條件 → 影片生成頁本身沒寫 |
| 94 | 語言表與年齡 | unclear-lang.data (unchanged fields) | G5, G6, G3 | 200 | CONFIRMED |  |
| 95 | 說明頁連到一張支援語言的表。 | unclear-lang:ixne | G5, G6, G3 | 200 | CONFIRMED |  |
| 96 | 表上有圖片、旁白和虛擬化身，沒列的功能寫明只支援英文。 | unclear-lang:vzju | G5, G6, G3 | 200 | CHANGED | 上面列了圖片、旁白和虛擬化身的語言。 → 表上有圖片、旁白和虛擬化身，沒列的功能寫明只支援英文。; G5 lists Vids image, voiceover, avatar, Slides-to-Vids; no video-generation row |
| 97 | 年齡則在生成頁連到的 Gemini 入門頁，寫要滿十八歲。 | unclear-lang:fsf9 | G5, G6, G3 | 200 | CHANGED | AI 影片生成的語言，還有年齡條件，這幾頁都沒寫。 → 年齡則在生成頁連到的 Gemini 入門頁，寫要滿十八歲。; G6 'What you need ...: Be 18 or over.' (G3 links it); G1-G5 silent |
| 98 | 官方的建議是，功能只支援英文時，把帳號語言改成英文。 | unclear-lang:3gje | G5, G6, G3 | 200 | CHANGED | 能不能用中文寫提示、有沒有年齡條件，只能以登入後的畫面為準。 → 官方的建議是，功能只支援英文時，把帳號語言改成英文。; G5 'set your Google Account language to English' |
| 99 | Vids 入門頁：手機只能看，不能編輯 | unclear-mobile.data.sub | G3, G7 | 200 | CHANGED | 官方步驟都從電腦開始，沒說手機能生成 → Vids 入門頁：手機只能看，不能編輯 |
| 100 | 第三件：手機 ／ 電腦 | unclear-mobile.data (unchanged fields) | G3, G7 | 200 | CONFIRMED |  |
| 101 | 第三件事，手機能不能生成。 | unclear-mobile:z7mj | G3, G7 | 200 | OUT OF SCOPE |  |
| 102 | 官方的步驟全部從電腦開啟 Google Vids 開始。 | unclear-mobile:nrat | G3, G7 | 200 | CONFIRMED |  |
| 103 | Vids 入門頁還寫，手機只能看影片，不能編輯。 | unclear-mobile:chsh | G3, G7 | 200 | CHANGED | 手機或平板能不能生成影片，官方沒有說明。 → Vids 入門頁還寫，手機只能看影片，不能編輯。; G7 'You can watch processed videos on your mobile device but you can't edit' |
| 104 | 上傳影片來改：地區限制 ／ 歐洲經濟區、英國、瑞士不行 ／ 美國伊利諾州、德州也不行 ／ 超過 10 秒只改最後 10 秒 | region-limits.data (unchanged fields) | G3 | 200 | CONFIRMED |  |
| 105 | 第四件，上傳自己的影片來改，有地區限制。 | region-limits:g9ei | G3 | 200 | OUT OF SCOPE |  |
| 106 | 歐洲經濟區、英國、瑞士不能用。 | region-limits:9zm2 | G3 | 200 | CONFIRMED |  |
| 107 | 美國伊利諾州和德州，也不能用。 | region-limits:pcqq | G3 | 200 | CONFIRMED |  |
| 108 | 上傳的影片超過十秒，只會修改最後十秒。 | region-limits:tjxx | G3 | 200 | CONFIRMED |  |
| 109 | 官方只列了不能用的地方，沒有列出哪些地方一定能用。 | region-limits:nqbw | G3 | 200 | CONFIRMED |  |
| 110 | 新版 AI 旁白：已上線 | voiceover.data.title | G1, G8 | 200 | CHANGED | AI 旁白：即將推出 → 新版 AI 旁白：已上線 |
| 111 | 公告說一百多種語言 | voiceover.data.items[1] | G1, G8 | 200 | CHANGED | 一百多種語言 → 公告說一百多種語言 |
| 112 | 9 月 29 日更新：已上線，限列名方案 | voiceover.data.items[2] | G1, G8 | 200 | CHANGED | 沒有給上線日期 → 9 月 29 日更新：已上線，限列名方案 |
| 113 | Gemini 3.8 Flash-Lite 文字轉語音 | voiceover.data (unchanged fields) | G1, G8 | 200 | CONFIRMED |  |
| 114 | 第五件，新版的 AI 旁白。 | voiceover:wga7 | G1, G8 | 200 | CHANGED | 第五件，AI 旁白。 → 第五件，新版的 AI 旁白。;  |
| 115 | 公告寫，Gemini 3.8 Flash-Lite 的文字轉語音即將推出。 | voiceover:cysz | G1, G8 | 200 | CONFIRMED |  |
| 116 | 公告說它會支援一百多種語言。 | voiceover:bp5e | G1, G8 | 200 | CHANGED | 它會支援一百多種語言。 → 公告說它會支援一百多種語言。; 100+ is G1's future-tense promise; G5 voiceover table lists 23 languages, no Chinese |
| 117 | 九月二十九日，更新公告寫已經上線，限列名的方案。 | voiceover:u2gj | G1, G8 | 200 | CHANGED | 旁白上線的日期，公告沒有給。 → 九月二十九日，更新公告寫已經上線，限列名的方案。; G8 2026-09-29 'Available now'; plans listed, no free personal accounts |
| 118 | 先確認自己的帳號 ／ 先登入對的 Google 帳號 ／ 沒有這項功能，開始畫面就不顯示選項 ／ 工作或學校帳號，管理員可以關掉 | check-yourself.data (unchanged fields) | G4 | 200 | CONFIRMED |  |
| 119 | 公告沒寫的地方，最實際的辦法，是看自己的畫面。 | check-yourself:jm3a | G4 | 200 | CHANGED | 官方頁沒寫的地方，最實際的辦法，是看自己的畫面。 → 公告沒寫的地方，最實際的辦法，是看自己的畫面。; follows the reframed hook |
| 120 | 用量頁說，要先登入對的 Google 帳號。 | check-yourself:radj | G4 | 200 | CONFIRMED |  |
| 121 | 帳號沒有某項功能，開始畫面就不會出現那個選項。 | check-yourself:p83d | G4 | 200 | CONFIRMED |  |
| 122 | 工作或學校帳號，管理員還可以把生成式 AI 功能關掉。 | check-yourself:y76w | G4 | 200 | CONFIRMED |  |
| 123 | 那官方有寫的部分，兩份頁面說得一樣嗎？ | check-yourself:263x | G4 | 200 | OUT OF SCOPE |  |
| 124 | 連誰能用，寫法也不同 ／ 公告：任何 Google 或 Workspace 帳號 ／ 生成說明頁開頭：需要合格的 Workspace 訂閱 ／ 用量頁：個人帳號也有專用的一格 | who-can.data (unchanged fields) | G1, G3, G4 | 200 | CONFIRMED |  |
| 125 | 先看誰能用，三個頁面的寫法就不一樣。 | who-can:iyr4 | G1, G3, G4 | 200 | OUT OF SCOPE |  |
| 126 | 公告說，有 Google 或 Workspace 帳號就能免費用。 | who-can:cdjf | G1, G3, G4 | 200 | CONFIRMED |  |
| 127 | 生成說明頁的開頭則寫，這功能需要合格的 Workspace 訂閱。 | who-can:ifi6 | G1, G3, G4 | 200 | CONFIRMED |  |
| 128 | 用量頁則替個人 Google 帳號，單獨列了一格額度。 | who-can:cyxg | G1, G3, G4 | 200 | CONFIRMED |  |
| 129 | 兩份頁面的原文 ／ 生成說明頁 ／ Most users can generate up to 50 videos per month. ／ 用量說明頁，個人帳號 ／ 6 video clips/month combined with AI avatars | two-pages.data (unchanged fields) | G3, G4 | 200 | CONFIRMED |  |
| 130 | 再看額度，先把兩份頁面的原文並排。 | two-pages:itx5 | G3, G4 | 200 | OUT OF SCOPE |  |
| 131 | 生成說明頁寫，多數使用者每月最多生成五十部影片。 | two-pages:3x75 | G3, G4 | 200 | CONFIRMED |  |
| 132 | 用量頁的個人帳號表格寫，每月六部，跟虛擬化身合計。 | two-pages:i84s | G3, G4 | 200 | CONFIRMED |  |
| 133 | 兩個數字，都是官方寫的。 | two-pages:k25s | G3, G4 | 200 | CONFIRMED |  |
| 134 | 頁面沒寫 | quota-table.data.rows[2][2] | G3, G4 | 200 | CHANGED | 每月 1 日 → 頁面沒寫 |
| 135 | 依帳號類型查額度（2026 年 9 月） ／ 官方說明頁 ／ 每月上限 ／ 重設時間 ／ 生成說明頁：概括多數使用者 ／ 多數使用者 50 部 ／ 每月 1 日 ／ 用量說明頁：個人／Individual ／ 6 部，與虛擬化身合計 ／ 每月 1 日 ／ 用量說明頁：未另列限制時的預設 ／ 500 秒 | quota-table.data (unchanged fields) | G3, G4 | 200 | CONFIRMED |  |
| 136 | 把三個數字排在一起看，前兩個寫每月一號太平洋時間午夜重設。 | quota-table:42a3 | G3, G4 | 200 | CHANGED | 把三個數字排在一起看，都是每月一號太平洋時間午夜重設。 → 把三個數字排在一起看，前兩個寫每月一號太平洋時間午夜重設。; G4 states no reset time for the 500-second default |
| 137 | 第一列，生成說明頁的概括，多數使用者五十部。 | quota-table:us6x | G3, G4 | 200 | CONFIRMED |  |
| 138 | 第二列，用量頁的個人帳號，六部，跟虛擬化身合計。 | quota-table:jdpm | G3, G4 | 200 | CONFIRMED |  |
| 139 | 第三列，用量頁沒有另外列限制時的預設，是五百秒。 | quota-table:bgex | G3, G4 | 200 | CONFIRMED |  |
| 140 | 三個數字的對象和單位不同，不能直接拿來互相比。 | quota-table:yuft | G3, G4 | 200 | OUT OF SCOPE |  |
| 141 | 我怎麼查自己的額度 ／ 確認帳號類型 ／ 個人、Workspace、Google AI ／ 找用量頁那一格 ／ 看是部數還是秒數 ／ 登入後看實際顯示 ／ 以畫面上的為準 | quota-steps.data (unchanged fields) | G4 | 200 | CONFIRMED |  |
| 142 | 所以我的做法是，不挑一個數字當答案，照三步查。 | quota-steps:pesn | G4 | 200 | OUT OF SCOPE |  |
| 143 | 第一步，先確認自己是哪一種帳號。 | quota-steps:artk | G4 | 200 | OUT OF SCOPE |  |
| 144 | 第二步，到用量頁找自己那一格，看它算部數還是秒數。 | quota-steps:3z47 | G4 | 200 | OUT OF SCOPE |  |
| 145 | 第三步，登入後看畫面上顯示的額度。 | quota-steps:xii4 | G4 | 200 | OUT OF SCOPE |  |
| 146 | 額度與功能，Google 也寫之後都可能調整。 | quota-steps:z9hj | G4 | 200 | CONFIRMED |  |
| 147 | 完整整理 ／ 兩份額度頁的原文 ／ 說明欄第一行就是文章連結 | cta.data (unchanged fields) | - | 200 | OUT OF SCOPE |  |
| 148 | 兩份頁面的原文和完整限制，都整理在說明欄第一行的文章。 | cta:7b7c | - | 200 | OUT OF SCOPE |  |
| 149 | 那做出來的東西，到底能拿去哪裡用？ | cta:ta5k | - | 200 | OUT OF SCOPE |  |
| 150 | Google 說明頁原文 ／ Generated images and videos are for use only within Vids. ／ 生成的圖片與影片只供在 Vids 內使用 ／ Google 說明中心 | watermark.data (unchanged fields) | G3 | 200 | CONFIRMED |  |
| 151 | 說明頁最底下，有一句話。 | watermark:9t34 | G3 | 200 | OUT OF SCOPE |  |
| 152 | 說明頁寫，生成的圖片和影片只供在 Vids 裡使用。 | watermark:ynjh | G3 | 200 | CONFIRMED |  |
| 153 | 這句話對匯出後的影片效力如何，頁面沒有進一步說明。 | watermark:mcdr | G3 | 200 | CONFIRMED |  |
| 154 | 使用前的兩個提醒 ／ 受生成式 AI 禁止使用政策約束 ／ 內容可能不代表真實世界 | policy.data (unchanged fields) | G3 | 200 | CONFIRMED |  |
| 155 | 要拿去別的地方用之前，先看清楚使用政策。 | policy:yw2i | G3 | 200 | OUT OF SCOPE |  |
| 156 | 這項功能還有兩個提醒。 | policy:hihz | G3 | 200 | OUT OF SCOPE |  |
| 157 | 第一，使用它要遵守 Google 的生成式 AI 禁止使用政策。 | policy:vrq8 | G3 | 200 | CONFIRMED |  |
| 158 | 官方也提醒，生成的內容可能不代表真實世界的情況。 | policy:t46a | G3 | 200 | CONFIRMED |  |
| 159 | SynthID 浮水印 ／ 每段都有，肉眼看不到 ／ 用來辨識是不是 AI 生成 ／ 不等於符合各地標示法規 | synthid.data (unchanged fields) | G1 | 200 | CONFIRMED |  |
| 160 | SynthID 是每一段都有的隱形浮水印。 | synthid:vavj | G1 | 200 | CONFIRMED |  |
| 161 | Google 說它讓人能驗證內容是不是 AI 做的，但怎麼驗，公告沒寫。 | synthid:w386 | G1 | 200 | CONFIRMED |  |
| 162 | 但這不代表它就符合各國的 AI 標示規定。 | synthid:vvpv | - | 200 | OUT OF SCOPE (opinion) |  |
| 163 | 看完這些，這個免費工具到底值不值得試？ | synthid:xtsm | G1 | 200 | OUT OF SCOPE |  |
| 164 | 帶走這三件事 ／ 插進 Vid ／ 關分頁前先存 ／ 依帳號 ／ 部數、秒數、點數分開看 ／ 只在 Vids ／ 使用範圍與浮水印 ／ 依 Google 官方頁整理，2026-09 | recap.data (unchanged fields) | G3, G4, G1 | 200 | CONFIRMED |  |
| 165 | 那值不值得試？我的看法是，值得先做一段，但要記住三件事。 | recap:jzhk | - | 200 | OUT OF SCOPE (opinion) |  |
| 166 | 第一，做好一段，先插進 Vid。 | recap:nkvm | G3, G4, G1 | 200 | CONFIRMED |  |
| 167 | 第二，額度依你的帳號看，不拿別人的數字當保證。 | recap:7d88 | G3, G4, G1 | 200 | CONFIRMED |  |
| 168 | 第三，官方寫生成的東西只供 Vids 內使用，還帶浮水印。 | recap:qqjw | G3, G4, G1 | 200 | CONFIRMED |  |
| 169 | 中文提示：沒列的功能只支援英文 | recap-five.data.items[0] | G3, G5, G6, G7, G8 | 200 | CHANGED | 中文提示：語言表沒列，看你的畫面 → 中文提示：沒列的功能只支援英文 |
| 170 | 年齡條件：Gemini 入門頁寫滿 18 歲 | recap-five.data.items[1] | G3, G5, G6, G7, G8 | 200 | CHANGED | 年齡條件：這幾頁都沒寫 → 年齡條件：Gemini 入門頁寫滿 18 歲 |
| 171 | 手機：只能看，不能編輯 | recap-five.data.items[2] | G3, G5, G6, G7, G8 | 200 | CHANGED | 手機：官方只寫電腦 → 手機：只能看，不能編輯 |
| 172 | 新版 AI 旁白：9 月 29 日更新寫已上線 | recap-five.data.items[4] | G3, G5, G6, G7, G8 | 200 | CHANGED | AI 旁白：即將推出，沒有日期 → 新版 AI 旁白：9 月 29 日更新寫已上線 |
| 173 | 那五件事，現在的答案 ／ 上傳影片來改：有不能用的地區 | recap-five.data (unchanged fields) | G3, G5, G6, G7, G8 | 200 | CONFIRMED |  |
| 174 | 另外，開頭那五件事，現在你手上有答案了。 | recap-five:i3s3 | G3, G5, G6, G7, G8 | 200 | OUT OF SCOPE |  |
| 175 | 中文提示，語言表沒列，沒列的功能只支援英文。 | recap-five:3yjx | G3, G5, G6, G7, G8 | 200 | CHANGED | 中文提示，語言表沒列，只能看你自己的畫面。 → 中文提示，語言表沒列，沒列的功能只支援英文。; G5 |
| 176 | 年齡條件，Gemini 入門頁寫要滿十八歲。 | recap-five:is5i | G3, G5, G6, G7, G8 | 200 | CHANGED | 年齡條件，這幾頁都沒有寫。 → 年齡條件，Gemini 入門頁寫要滿十八歲。; G6 |
| 177 | 手機，只能看，不能編輯。 | recap-five:js58 | G3, G5, G6, G7, G8 | 200 | CHANGED | 手機，官方只寫了電腦。 → 手機，只能看，不能編輯。; G7 |
| 178 | 上傳影片來改，有幾個地方不能用。 | recap-five:ew36 | G3, G5, G6, G7, G8 | 200 | CONFIRMED |  |
| 179 | 新版 AI 旁白，九月二十九日的更新寫已上線，限列名方案。 | recap-five:y9fj | G3, G5, G6, G7, G8 | 200 | CHANGED | AI 旁白，寫著即將推出，沒有日期。 → 新版 AI 旁白，九月二十九日的更新寫已上線，限列名方案。; G8 |
| 180 | 最後提醒 ／ 以官方頁為準 ／ 本站沒有實測生成效果 | caveat.data (unchanged fields) | - | 200 | OUT OF SCOPE |  |
| 181 | 這支只整理官方說法，我沒有實測生成效果。 | caveat:ri3w | - | 200 | OUT OF SCOPE |  |
| 182 | 額度和使用範圍，以官方最新的頁面為準。 | caveat:knpp | - | 200 | OUT OF SCOPE |  |
| 183 | 用電腦做，手機只能看 | wrap.data.lines[0] | G3, G7 | 200 | CHANGED | 用電腦做，手機沒寫能生成 → 用電腦做，手機只能看 |
| 184 | 先插進 Vid，再看那五件事 ／ 完整限制與兩份額度原文在說明欄的文章裡 ／ 做好一段先插進 Vid ／ 額度與使用範圍以官方頁為準 | wrap.data (unchanged fields) | G3, G7 | 200 | CONFIRMED |  |
| 185 | 完整的整理，在說明欄第一行的文章。 | wrap:xqza | G3, G7 | 200 | OUT OF SCOPE |  |
| 186 | 免費是真的，但那五件事，動手之前先知道，就不會白做工。 | wrap:cmwf | - | 200 | OUT OF SCOPE (opinion) |  |
| 187 | 3 sources added (G6, G7, G8), checked_on 2026-09-30 | sources | G6, G7, G8 | 200 | CHANGED |  |

## Summary

- Claims checked: 187 table rows from 159 extracted items (title, description, tags, thumbnail, every slide's data, 124 narration lines). CONFIRMED 91, CHANGED 48 rows, NOT FOUND 0 (the one unsupported figure, the reset time for the 500 s default, was replaced by 「頁面沒寫」), OUT OF SCOPE 48 (transitions, opinions, CTA).
- FACT changes (groups): 5. (1) Chinese prompt: English-only fallback on G5/G4. (2) Age: 18+ on G6. (3) Mobile: watch only, no editing, on G7. (4) New AI voiceover: G8 says available now on 09-29 for listed plans; existing voiceover already exists. (5) Reset time for the 500 s default is not on G4. Dependants changed: hook frame (wchu, gqa7, hook-proof sub, chza, jm3a, chapter, table title and column), description, thumbnail "5 unknowns" → "5 catches", three sources added (G6, G7, G8, checked_on 2026-09-30), claims.md c7/c8/c9/c11/c12 and progress.
- Facts that expire soon: G8's voiceover availability (dated 2026-09-29) and its date conflict with the 09-23 TTS blog; G2's rollout "starting on September 23, 2026"; all G4 quota numbers ("subject to change"); G6 is partly stale (it still says Veo 3 and "at least through May 31, 2026"), so its 18+ line could change without notice.
- Opinion mismatches against the brief's 站主觀點: none. The quota figures are listed side by side and "不挑一個" is kept; insert-before-closing, SynthID and the prohibited-use policy are all present. Opinions marked with 我的看法是: rnw8 and jzhk. vvpv (「不代表符合各國 AI 標示規定」) and krnz are site statements without a marker (report only). Brief conflict: outline B's "five unknowns" premise (see the main finding) needs the owner's decision.
- Listener pass (report only): no line over 40 characters, no 經查證／根據官方文件／本影片, no parentheses or URLs in narration. Latin term not in the lexicon: `Flash-Lite` (cysz, pre-existing, not added by this round; lint does not warn). Reveal order: unclear-table rows show each answer when the item is named, before its own scene explains it (same pattern as the writer's table).
- Lint: `node tools/video/cli.mjs lint --slug google-vids-free-ai-video-omni-1-1` gives 0 errors, 0 warnings, estimated 9.4 min, 124 lines.
- Suspected but not changed: quota-table row 2's "每月 1 日" relies on the G4 credits footnote attached to the Personal table heading. nqbw 「沒有列出哪些地方一定能用」 stands, but G4 has a general "all countries and regions where Google Workspace accounts are available". itua 「片段就不見了」 paraphrases "the history disappears". The "7 張" figure applies to Create (Edit allows 3). The title card 「五件事沒寫清楚」 is kept (now read as the announcement). Personal free accounts may still get the older voiceover (G4: 1 credit), while G8 does not list them for the upgrade. G3's "requires an eligible Google Workspace subscription" conflicts with G1/G4, and the script only juxtaposes them. One `sed` with non-ASCII text was run on claims.md (the result was checked).
- SECOND ROUND REQUIRED: yes (5 fact changes, more than 3). Old TTS audio is invalid.
