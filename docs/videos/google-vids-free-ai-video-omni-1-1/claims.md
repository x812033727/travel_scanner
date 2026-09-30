# claims — google-vids-free-ai-video-omni-1-1

一行一個可查證的說法：`id｜說法｜官方來源｜查核日｜出現的場景`。本站沒有實測生成效果。

2026-09-30 依站主 2026-09-28 選定的大綱 B（免費 AI 影片工具實測前，先讀懂它的限制）整份重寫。四份官方頁與語言支援頁都在 2026-09-30 重新用 `curl` 抓（HTTP 200，無重新導向），原文抽取存於 `<VIDEO_WORKDIR>/google-vids-free-ai-video-omni-1-1/_tools/text0N.txt`（不進 git）。2026-09-29 的更正（verify-1、verify-p1-20260929、verify-p1-20260929-round2）全部保留，沒有重新放回被更正掉的說法：不寫「整個流程不到一分鐘」、不寫「這種不一致不常見」、不把 50／6／500 說成互相矛盾的免費額度、虛擬化身當素材的「限英文與列名方案」保留。

URL 簡寫：G1＝https://blog.google/products-and-platforms/products/workspace/gemini-omni-in-google-vids/　G2＝https://workspaceupdates.googleblog.com/2026/09/gemini-omni-11-flash-now-in-vids-with-improved-extension-quality-1080p-and-duration-control.html　G3＝https://support.google.com/docs/answer/16143507（生成說明頁）　G4＝https://support.google.com/docs/answer/15609411（用量說明頁）　G5＝https://support.google.com/docs/answer/14925782（語言支援頁，G3 連過去的那一頁）　G6＝https://support.google.com/docs/answer/13952129（Gemini 入門頁）　G7＝https://support.google.com/docs/answer/15082958（Vids 入門頁）　G8＝https://workspaceupdates.googleblog.com/2026/09/create-more-natural-expressive-ai-voiceovers-in-Google-Vids-with-upgraded-Gemini-3.8-Flash-Lite-TTS.html

c1｜任何 Google 或 Workspace 帳號可在 Google Vids 免費用 Gemini Omni 1.1 Flash 生成影片（「anyone with a Google or Google Workspace account can generate high-quality videos at no cost」）；公告日 2026-09-23；標題原文「Anyone can make stunning HD videos with Gemini Omni in Google Vids」；「免費」「任何人」是 Google 自己的用語｜G1｜2026-09-30｜what-is, twist, promo-words, who-can
c2｜Workspace Updates 公告日 2026-09-23；適用個人 Google 帳號、Google AI Pro 與 Ultra、列名的 Workspace 版本；「This feature does not have an admin control」｜G2｜2026-09-30｜what-is, who-can
c3｜「Visit vids.new on your desktop」；G3 每一組步驟都從「Open Google Vids on your computer」開始｜G1、G3｜2026-09-30｜how-to, unclear-mobile
c4｜生成規格 24fps、720p 與 1080p、16:9 或 9:16、長度 3 到 10 秒、Ingredients 最多 7 張參考圖；步驟 Create AI videos → Create → 提示 → 比例 → 長度 → Generate；提示寫主題、地點、動作、鏡頭、光線、對白、聲音、語氣｜G3｜2026-09-30｜how-to, prompt-tips, specs, reference-images
c5｜「To access and edit the generated video clip after each session, insert it into your Vid.」；「When you close the Vids tab, the history disappears.」｜G3｜2026-09-30｜save-it, save-habit, recap
c6｜三個控制：延長場景（保持視覺脈絡、光線、角色外觀、環境一致）、指定秒數、1080p 生成或升頻｜G1、G2｜2026-09-30｜three-controls
c7｜中文提示（2026-09-30 查核更正）：G1 公告沒提語言；G3 連到語言支援頁（G5）；G5 有 Vids 的圖片生成、AI 旁白、AI 虛擬化身、Slides 轉 Vids 的語言表，沒有「AI 影片生成」這一列，而 G5 最後寫「For other Google Workspace with Gemini features, English is the only supported language. To use Google Workspace with Gemini features that are supported in English only, set your Google Account language to English.」；G4 也寫「Many AI features in Vids are only available in English at this time.」所以影片改說「沒列的功能只支援英文、官方建議把帳號語言改成英文」，不再說官方頁沒寫｜G1、G3、G4、G5｜2026-09-30｜hook, unclear-table, unclear-ask, unclear-lang, recap-five
c8｜年齡條件（2026-09-30 查核更正）：G1–G5 都沒有年齡字樣，但 G3「Learn about Gemini features and plans」連到的 G6（Get started with Google Workspace with Gemini）在「What you need to use Google Workspace with Gemini」第一條寫「Be 18 or over.」；個人化身頁（docs/answer/16970930）也寫建立個人化身要「Be 18 or over」。影片改說「Gemini 入門頁寫要滿十八歲，影片生成頁本身沒寫」｜G1–G6｜2026-09-30｜unclear-table, unclear-lang, recap-five
c9｜手機（2026-09-30 查核更正）：G1 只寫「vids.new on your desktop」，G3 步驟全從「on your computer」開始；G7（Get started with Google Vids）寫「To access Google Vids on your mobile device, you can use a compatible web browser. You can watch processed videos on your mobile device but you can't edit or add comments to videos.」影片改說「Vids 入門頁寫手機只能看、不能編輯」，不再說官方沒說明｜G1、G3、G7｜2026-09-30｜hook, unclear-table, unclear-mobile, recap-five, wrap
c10｜「Users of this feature in the European Economic Area, United Kingdom, Switzerland, Illinois, and Texas cannot upload and edit videos using this feature. Users in these regions may only use this feature to edit AI generated videos in their generation history.」；上傳超過 10 秒只改最後 10 秒；G3 只列不能用的地區；G4 另有概括句「Supported countries & regions: You can use these features in all countries and regions where Google Workspace accounts are available.」（查核第 2 輪：nqbw 改成「用量頁只概括寫，Workspace 有開放的地方都能用」，表格第四列改成「列了不能用的地區」；聽稿時 nqbw 移到地區清單之後，前面加 f57c「那其他地區呢？」，句子改成「講用量的說明頁只概括寫，Workspace 有開放的地方都能用」）｜G3、G4｜2026-09-30｜unclear-table, region-limits, recap-five
c11｜新版 AI 旁白（2026-09-30 查核更正）：G1（9/23）「Coming soon, Gemini 3.8 Flash-Lite text-to-speech in Google Vids will turn any script into a natural-sounding voiceover across 100+ languages」，未給日期；但 G8（Workspace Updates，2026-09-29）寫把 Vids 的 AI 旁白與虛擬化身旁白引擎升級為 Gemini 3.8 Flash Lite TTS，「Rapid Release and Scheduled Release domains: Available now」，Availability 列 Business、Enterprise、Education Plus、Essentials、Individual、Nonprofits、Google AI Pro 與 Ultra 等，沒列免費個人帳號；另 Google 部落格〈Gemini 3.8 text-to-speech says hello〉（9/23）寫 Flash-Lite TTS「rolling out starting today… For everyone: In Google Vids」。現有 AI 旁白本來就有（G4 個人帳號 1 credit 一次）。影片改說「9 月 29 日的更新公告寫新版 AI 旁白已上線、限列名方案」（9/23 的 TTS 部落格另寫當天起在 Vids 推出，兩頁日期不同，影片只引 9/29 那頁）；「一百多種語言」標明是公告說法（說明頁的旁白語言表只列 23 種、沒有中文）｜G1、G8｜2026-09-30｜unclear-table, voiceover, recap-five
c12｜額度：G3「Most users can generate up to 50 videos per month. The monthly limit resets at 12 AM PT on the first day of the month.」；G4 的 Personal Google Account 表格「6 video clips/month combined with AI avatars」，Workspace Individual 表格同樣是 6；Google AI Plus 也列 6 部合計；G4 的「12:00 AM PT on the first day of each month」重設句寫在個人、Individual、AI Plus 表格的 credits 註腳裡；未另列時的預設 500 秒，G4 沒有寫重設時間（2026-09-30 查核：表格第三列的重設時間改成「頁面沒寫」，42a3 改成「前兩個」；聽稿時 42a3 拆開，重設句移到第二列之後的 evm7「這兩列都寫，每月一號太平洋時間午夜重設」）；另有 50 credits 是其他功能點數，不是 50 部影片。三個數字對象和單位不同，不寫成互相矛盾｜G3、G4｜2026-09-30｜two-pages, quota-table, quota-steps, recap
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
- B 的第 3 章「五件事」裡，「上傳影片的地區限制」官方其實有寫（列了不能用的地區）；沒寫的是可用名單，所以表格與旁白寫成「只列出不能用的地區」，不說官方沒寫。（查核第 2 輪更正：G4 有概括的可用範圍句，表格改成「列了不能用的地區」，nqbw 改說用量頁的概括寫法。）
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
- 2026-09-30：獨立查核第 1 輪（verify-r1-20260930.md）：c7、c8、c9、c11 與 c12 的重設時間更正；五件事改成「公告沒寫清楚、說明頁怎麼寫」；縮圖改成 5 catches。需要第 2 輪。
- 2026-09-30：獨立查核第 2 輪（verify-r2-20260930.md）：第 1 輪的五項更正在官方頁重看都成立；抽查的已確認項目都成立；c10 更正一處（nqbw 與表格第四列依 G4 的地區句）。不需第 3 輪。
- 待做：聽眾審稿、tts。
