# claims — google-vids-free-ai-video-omni-1-1

一行一個可查證的說法：`id｜說法｜官方來源｜查核日｜出現的場景`。本站沒有實測生成效果。

2026-09-30 依站主 2026-09-28 選定的大綱 B（免費 AI 影片工具實測前，先讀懂它的限制）整份重寫。四份官方頁與語言支援頁都在 2026-09-30 重新用 `curl` 抓（HTTP 200，無重新導向），原文抽取存於 `<VIDEO_WORKDIR>/google-vids-free-ai-video-omni-1-1/_tools/text0N.txt`（不進 git）。2026-09-29 的更正（verify-1、verify-p1-20260929、verify-p1-20260929-round2）全部保留，沒有重新放回被更正掉的說法：不寫「整個流程不到一分鐘」、不寫「這種不一致不常見」、不把 50／6／500 說成互相矛盾的免費額度、虛擬化身當素材的「限英文與列名方案」保留。

URL 簡寫：G1＝https://blog.google/products-and-platforms/products/workspace/gemini-omni-in-google-vids/　G2＝https://workspaceupdates.googleblog.com/2026/09/gemini-omni-11-flash-now-in-vids-with-improved-extension-quality-1080p-and-duration-control.html　G3＝https://support.google.com/docs/answer/16143507（生成說明頁）　G4＝https://support.google.com/docs/answer/15609411（用量說明頁）　G5＝https://support.google.com/docs/answer/14925782（語言支援頁，G3 連過去的那一頁）

c1｜任何 Google 或 Workspace 帳號可在 Google Vids 免費用 Gemini Omni 1.1 Flash 生成影片（「anyone with a Google or Google Workspace account can generate high-quality videos at no cost」）；公告日 2026-09-23；標題原文「Anyone can make stunning HD videos with Gemini Omni in Google Vids」；「免費」「任何人」是 Google 自己的用語｜G1｜2026-09-30｜what-is, twist, promo-words, who-can
c2｜Workspace Updates 公告日 2026-09-23；適用個人 Google 帳號、Google AI Pro 與 Ultra、列名的 Workspace 版本；「This feature does not have an admin control」｜G2｜2026-09-30｜what-is, who-can
c3｜「Visit vids.new on your desktop」；G3 每一組步驟都從「Open Google Vids on your computer」開始｜G1、G3｜2026-09-30｜how-to, unclear-mobile
c4｜生成規格 24fps、720p 與 1080p、16:9 或 9:16、長度 3 到 10 秒、Ingredients 最多 7 張參考圖；步驟 Create AI videos → Create → 提示 → 比例 → 長度 → Generate；提示寫主題、地點、動作、鏡頭、光線、對白、聲音、語氣｜G3｜2026-09-30｜how-to, prompt-tips, specs, reference-images
c5｜「To access and edit the generated video clip after each session, insert it into your Vid.」；「When you close the Vids tab, the history disappears.」｜G3｜2026-09-30｜save-it, save-habit, recap
c6｜三個控制：延長場景（保持視覺脈絡、光線、角色外觀、環境一致）、指定秒數、1080p 生成或升頻｜G1、G2｜2026-09-30｜three-controls
c7｜中文提示：G3 連到語言支援頁（G5）；G5 有 Vids 的圖片生成、AI 旁白、AI 虛擬化身、Slides 轉 Vids 的語言表，沒有「AI 影片生成」這一列（頁面只在相關文章連結出現「Use AI to generate video clips in Google Vids」字樣）。本影片只說「這些頁沒寫」，不說不能用中文｜G3、G5｜2026-09-30｜hook, unclear-table, unclear-ask, unclear-lang, recap-five
c8｜年齡條件：G1、G2、G3、G4、G5 五頁都搜不到年齡限制的字（age、minor、under 18、18+ 都沒有）。這是「五頁都沒寫」的缺席說法，範圍限於這五頁｜G1–G5｜2026-09-30｜unclear-table, unclear-lang, recap-five
c9｜手機：G1 只寫 vids.new on desktop，G3 步驟全從電腦開始；沒有任何一頁說手機或平板能不能生成｜G1、G3｜2026-09-30｜hook, unclear-table, unclear-mobile, recap-five
c10｜「Users of this feature in the European Economic Area, United Kingdom, Switzerland, Illinois, and Texas cannot upload and edit videos using this feature. Users in these regions may only use this feature to edit AI generated videos in their generation history.」；上傳超過 10 秒只改最後 10 秒；官方只列不能用的地區，沒有列可用名單｜G3｜2026-09-30｜unclear-table, region-limits, recap-five
c11｜「Coming soon, Gemini 3.8 Flash-Lite text-to-speech in Google Vids will turn any script into a natural-sounding voiceover across 100+ languages」；未給日期｜G1｜2026-09-30｜unclear-table, voiceover, recap-five
c12｜額度：G3「Most users can generate up to 50 videos per month. The monthly limit resets at 12 AM PT on the first day of the month.」；G4 的 Personal Google Account 表格「6 video clips/month combined with AI avatars」，Workspace Individual 表格同樣是 6；Google AI Plus 也列 6 部合計；每月 1 日太平洋時間 12 AM 重設；另有 50 credits 是其他功能點數，不是 50 部影片。三個數字對象和單位不同，不寫成互相矛盾｜G3、G4｜2026-09-30｜two-pages, quota-table, quota-steps, recap
c13｜G3 開頭「This feature requires an eligible Google Workspace subscription.」；G1 與 G4 把個人 Google 帳號列入（G1 結尾另說個人帳號想要更多用量可看 Google AI 方案）。三頁寫法不同，影片只如實並列，不判斷哪一個對｜G1、G3、G4｜2026-09-30｜who-can, quota-table
c14｜G4：未另外指定的預設「AI video clips: Up to 500 video clip seconds per month」；Business Starter 200 秒、Standard／Plus 500 秒；「The limits and exact features that will continue to be available are subject to change.」｜G4｜2026-09-30｜quota-table, quota-steps
c15｜「Generated images and videos are for use only within Vids.」；「Omni video clips are created through generative AI. Usage of this feature is subject to the Generative AI Prohibited Use Policy.」；頁面沒有說明匯出後的影片效力｜G3｜2026-09-30｜watermark, policy, recap
c16｜「Gemini generated images and videos … may not represent real-world situations.」｜G3｜2026-09-30｜policy
c17｜「Every clip generated with Omni 1.1 in Google Vids includes an imperceptible SynthID digital watermark embedded into the video frames. This allows viewers to verify that content was generated with AI.」；公告沒寫怎麼驗證；「不代表符合各地標示法規」是本站限縮，不是官方說法｜G1｜2026-09-30｜synthid, recap
c18｜G4：「Make sure you sign in with the correct Google Account that can access the feature. If your account doesn't have access to a Google Vids feature, the associated option won't display in the "Getting started" screen.」；工作或學校帳號「your admin controls access to Google Vids and can turn off access to generative AI features」｜G4｜2026-09-30｜check-yourself
c19｜虛擬化身：G4「Personal Google accounts only have access to preset AI avatars」；G3 Check Avatar availability：「You can only use avatars as ingredients in EN and in the following accounts」，名單含 Business／Enterprise／Nonprofits／Education 版本與 Google AI Pro、Ultra（僅美國）｜G3、G4｜2026-09-30｜reference-images

## 場景對照

hook（c7、c9）→ hook-proof（c7、c9）→ what-is（c1、c2）→ twist（c1）→ promo-words（c1）→ how-to（c3、c4）→ prompt-tips（c4）→ specs（c4）→ reference-images（c4、c19）→ three-controls（c6）→ save-it（c5）→ save-habit（c5）→ unclear-table（c7–c11）→ unclear-ask（c7）→ unclear-lang（c7、c8）→ unclear-mobile（c3、c9）→ region-limits（c10）→ voiceover（c11）→ check-yourself（c18）→ who-can（c1、c2、c12、c13）→ two-pages（c12）→ quota-table（c12、c13、c14）→ quota-steps（c12、c14）→ cta → watermark（c15）→ policy（c15、c16）→ synthid（c17）→ recap（c5、c12、c15、c17）→ recap-five（c7–c11）→ caveat → wrap

## 與企劃不同的地方

- 站主選了大綱 B。結構照 B：一句話講它是什麼 → 動手做一段 → 官方沒寫清楚的五件事 → 兩份官方頁的額度 → 浮水印與使用範圍 → 答案。開場鉤子照 B（五件事官方頁還沒寫清楚）。示範放第 2 章（steps 流程與規格）和第 4 章（額度怎麼查，steps）。
- 為了「開場鉤子在 30 秒內落地」的 lint，B 的第 1 章「一句話講清楚它是什麼」前面多了一個 27 秒的開場章（鉤子加「你以為…其實…」）；所以章節是七個，不是 B 寫的六個。「答案」章（B 的第 6 章）在稿裡叫「值得試嗎」，含三件事摘要、五件事回顧、收尾。
- B 的第 4 章原名「兩份官方頁的額度不一致」。2026-09-29 第二輪查核已證明 50、6、500 是不同帳號範圍和單位，不是矛盾，所以這章改成「兩份官方頁怎麼讀」：只並列原文、說明對象和單位不同，「不挑一個當答案」的立場保留。B 的 `quote` 換成 `compare` 並排兩份頁面的原文。
- B 的第 3 章「五件事」裡，「上傳影片的地區限制」官方其實有寫（列了不能用的地區）；沒寫的是可用名單，所以表格與旁白寫成「只列出不能用的地區」，不說官方沒寫。
- 多加三個場景讓五件事有憑據與出口：`unclear-ask`（中文提示的一問一答）、`check-yourself`（G4 教你怎麼確認自己的帳號，c18）、`who-can`（三頁對「誰能用」的寫法不同，c13）。`three-controls` 和 `reference-images` 是 A 稿留下來、B 的第 2 章也需要的內容。
- 縮圖文字改成 `Free, but 5 unknowns`（舊的是 4 limits，跟 B 不符）；說明欄與標籤同步改成 B 的內容。
- 站內文章：B 的結尾說「站內文章同上」，仍是 `ai-news-google-vids-omni-free-20260924`（`source_guide` 沒動）；B 沒有指定別的結尾文章。

## 我懷疑但沒動的事

- 五件事裡兩件是「缺席」說法（c7 語言表沒有影片生成列、c8 五頁都沒寫年齡）。範圍已限在我讀的五頁；如果有別的官方頁（例如 Workspace 的 Gemini 使用條款、年齡政策）寫了，這兩句要改。校對者請用瀏覽器再開一次 G5 和搜尋整頁。
- G3 開頭寫「requires an eligible Google Workspace subscription」，與 G1 公告的「任何 Google 帳號」及 G4 的個人帳號表格並存（c13）。可能只是說明頁沿用舊的 Workspace 範本，我沒有推斷原因，只如實並列。
- 生成頁的「50 部」和用量頁預設的「500 秒」，如果每部都是 10 秒剛好相同。這是算術上的巧合，官方沒有這樣寫，影片沒有用它。
- 用量頁的 Google AI Plus、Pro、Ultra 各有不同秒數或部數，欄位對照在頁面抽取後有錯位可能（Plus 出現兩欄），所以影片只講個人帳號的 6、預設的 500、生成頁的 50，沒有講 AI 方案的數字。
- 「每月一號太平洋時間午夜重設」G3 與 G4 都寫 12 AM PT；沒有寫夏令時間的處理。
- 發音：`Vid` 與 `Vids` 在字典裡是 null（照字讀），Gemini 語音可能讀成「維德」「維茲」，聽稿時請留意；`Gemini Omni 1.1 Flash` 與 `Gemini 3.8 Flash-Lite` 已用 `say` 寫成「一點一」「三點八」。
- 本稿改動幅度大（整份重排），舊的 verify 紀錄不再對得上；需要重新獨立查核，並重跑 tts。

## 進度

- 2026-09-30：video.json 依 B 全部重寫完成（31 個場景、124 句、7 章、估計 9.2 分鐘），lint 0 錯誤 0 警告；claims.md 完成。字典沒有新增詞。
- 待做：獨立事實查核（新版）、聽眾審稿、tts。
