# daily-ai-20261103 主張與證據

每一行：編號｜主張（旁白或卡片上的說法）｜站上文章；原始來源｜來源查證日｜場景 id。
事實只用站上 news_date 2026-11-02 已發布的文章（`/api/travel/guides/life/<slug>?locale=zh-TW` 取得，2026-11-03）與它們列的來源；
撰稿人 2026-11-03 逐頁重新打開下列 14 個原始來源（皆 HTTP 200），卡片上的英文引句都是當天頁面上的原文。
「自述」＝公司自己公布、沒有第三方確認；「指控」＝訴狀內容；「換算」＝節目依來源數字自己算的；「建議」＝節目的建議，不是來源的說法。

站上文章簡稱：
- TWCA＝https://mokaair.com/zh-TW/life/tech-news-twca-certificate-20261102 ；原始來源 MODA＝https://moda.gov.tw/press/press-releases/21226
- CHAT＝https://mokaair.com/zh-TW/life/ai-news-chatgpt-merge-chat-work-tabs-20261102 ；TC1＝https://techcrunch.com/2026/11/02/openai-is-finally-merging-chatgpts-chat-and-work-tabs/
- BRAVE＝https://mokaair.com/zh-TW/life/ai-news-nyt-sues-brave-ai-scraping-20261102 ；V1＝https://www.theverge.com/tech/1024588/brave-lawsuit-ai-scraping-new-york-times
- GENIE＝https://mokaair.com/zh-TW/life/ai-news-genie-4-research-preview-20261102 ；DM＝https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/ ；G10＝https://blog.google/innovation-and-ai/technology/ai/google-ai-updates-october-2026/
- MT1＝https://mokaair.com/zh-TW/life/ai-news-claude-message-threads-20261102 ；MT2＝https://mokaair.com/zh-TW/life/ai-news-message-threads-20261102 ；CL＝https://claude.com/resources/articles/message-threads ；RN＝https://platform.claude.com/docs/en/release-notes/overview（November 2, 2026）
- AGY＝https://mokaair.com/zh-TW/life/ai-news-google-cloud-antigravity-plugin-20261102 ；GCB＝https://cloud.google.com/blog/topics/developers-practitioners/google-cloud-developer-plugin-now-available-in-antigravity-marketplace/
- GRID＝https://mokaair.com/zh-TW/life/ai-news-openai-grid-protectors-program-20261102 ；V2＝https://www.theverge.com/ai-artificial-intelligence/1024604/openai-data-center-grid-protection-program
- MB1＝https://mokaair.com/zh-TW/life/crypto-news-mercado-bitcoin-halts-withdrawals-20261102 ；DC1＝https://decrypt.co/382341/mercado-bitcoin-halts-withdrawals-40-million-hack ；MB2＝https://mokaair.com/zh-TW/life/crypto-news-mercado-bitcoin-hack-freeze-20261102 ；CH＝https://www.chainalysis.com/blog/chainalysis-response-mercado-bitcoin/
- SQ＝https://mokaair.com/zh-TW/life/tech-news-squarespace-layoffs-20261102 ；TC2＝https://techcrunch.com/2026/11/02/web-host-squarespace-lays-off-19-of-its-employees/ ；V3＝https://www.theverge.com/tech/1024447/squarespace-layoffs-19-percent
- TRAJ＝https://mokaair.com/zh-TW/life/ai-news-trajectory-series-a-20261102 ；TC3＝https://techcrunch.com/2026/11/02/trajectory-raises-45m-to-make-ai-model-training-accessible-to-nontechnical-experts/（站上文章列的來源，本次未另開，事實照站上文章）
- PROTON＝https://mokaair.com/zh-TW/life/tech-news-proton-ai-backlash-20261102 ；DC2＝https://decrypt.co/382353/proton-users-revolt-ceo-calls-security-caution-loser-thinking-ai

## Cold Open、Intro

c1｜10 月 30 日國際社群 Bugzilla 通報 TWCA 核發的部分憑證序號亂數長度未達國際標準｜TWCA；MODA｜2026-11-03｜co-report, sd-found, sd-bugzilla
c2｜涉及 962 個政府機關、9,772 張網站憑證（數發部盤點）｜TWCA；MODA｜2026-11-03｜co-scale, sd-not-alone, sd-recap, sd-taiwan
c3｜數發部籲請 11 月 6 日前完成更新；2026-11-06 是星期五、2026-11-03 是星期二（曆法）｜TWCA；MODA｜2026-11-03｜co-date, intro, intro-kai, sd-timeline
c4｜「問題出在序號裡，少了一樣東西」＝序號的有效隨機亂數不足（揭曉在 sd-bits）｜MODA｜2026-11-03｜co-flaw
c74｜快訊都是 news_date 2026-11-02 的站上文章（Genie 4 為 10/27 發表、11/2 Google 彙整再提，旁白照實說）｜各站上文章｜2026-11-03｜hl-open
c5｜「11 月 2 日晚上的數字，聽了會嚇一跳」＝截至 11/2 晚間 926 張完成更新（揭曉在 sd-progress）｜MODA｜2026-11-03｜co-count

## Headlines

c6｜據 TechCrunch，OpenAI 寄信給使用者：ChatGPT 桌面版的 Chat 與 Work 分頁將合併｜CHAT；TC1｜2026-11-03｜hl-chat
c7｜TechCrunch 認為是為了改善分頁太多、使用者忘記自己在哪工作的混淆；合併後可帶入自己的檔案與外掛；Codex 維持獨立｜CHAT；TC1｜2026-11-03｜hl-chat-why
c8｜郵件舉例：建立網站、製作簡報、在網路上代為處理事務，並在過程中審閱、引導它｜CHAT；TC1｜2026-11-03｜hl-chat-do
c9｜TechCrunch：Anthropic 已在 9 月把 Claude 的聊天與 Cowork 合到同一個畫面｜CHAT；TC1｜2026-11-03｜hl-chat-claude
c10｜ChatGPT 與 Codex 從同一個 token 額度池扣；OpenAI 稱多數使用者不受影響，部分人可能更常等額度重置；起初只給部分使用者試用、蒐集意見後廣泛推出（單一媒體報導）｜CHAT；TC1｜2026-11-03｜hl-chat-quota
c11｜據 The Verge（11/2），紐約時報與其他媒體對 Brave 瀏覽器的開發公司提告｜BRAVE；V1｜2026-11-03｜hl-brave
c12｜指控：未經許可爬取新聞網站內容、把索引收費提供給 AI 公司、讓使用者繞過付費牆（皆原告指控）｜BRAVE；V1｜2026-11-03｜hl-brave-claims
c13｜訴狀點名 Anthropic、Perplexity、Mistral、xAI、Cohere（卡片列五家，旁白唸兩家）｜BRAVE；V1｜2026-11-03｜hl-brave-named
c14｜Brave 在瀏覽器中宣傳「Paywall blocker」功能；報導未說明它與指控的關係｜BRAVE；V1（"Brave also promotes "hundreds of top publishers" as being accessible through its "Paywall blocker" feature"）｜2026-11-03｜hl-brave-paywall
c15｜報導未提及法院裁決；Brave 未立即回應置評。「目前不用動手」是節目建議｜BRAVE；V1｜2026-11-03｜hl-brave-status, wp-react
c16｜Google DeepMind 10 月 27 日發表世界模型 Genie 4；Google 11 月 2 日的十月 AI 彙整再提｜GENIE；DM；G10｜2026-11-03｜hl-genie
c17｜打字產生有畫面、有聲音的場景；鍵盤控制移動與鏡頭；文字指令即時改天氣、加人物或物件（「像遊戲世界」是 Kai 的比喻）｜GENIE；DM｜2026-11-03｜hl-genie-how
c18｜研究預覽、只給受信任測試者；之後先開放給 Project Genie 中的 Google AI Ultra 訂閱者與 Gemini API、AI Studio 的早期存取夥伴（旁白簡化成「早期合作的開發者」）｜GENIE；DM｜2026-11-03｜hl-genie-who
c19｜長時間執行或多次修改時，畫面細節與物件恆存性可能漂移（DeepMind 自述）；「台灣一般人現在用不到」依研究預覽的開放對象推論｜GENIE；DM｜2026-11-03｜hl-genie-limit
c20｜Genie 4 的影片與音訊都含 SynthID 浮水印；Google 另有 SynthID Detector（以英語向全球擴大提供）｜GENIE；DM；G10｜2026-11-03｜hl-genie-mark
c21｜Anthropic 11/2 推出 Messages API 的 message threads（訊息串）公開測試版，給打造 AI 代理的開發者｜MT1；MT2；CL；RN｜2026-11-03｜hl-threads
c22｜過去每輪重送完整對話；開啟後對話保存在伺服器端，之後只送新訊息（Kai 的「對話越長，重送越多」依 CL「當對話達數十萬 token，重送全部內容會增加開始回應前的時間」）｜MT1；MT2；CL；RN｜2026-11-03｜hl-threads-how
c23｜500k–1M token 的請求，TTFT 中位數下降約 35%（條件：多數 Claude Code 使用者預設啟用；旁白未唸條件，卡片 note 寫請求大小）；token 用量不變，適用標準費率；最後一次請求後 5 分鐘到期，之後需重送完整對話（自述）｜MT1；CL（"requests with 500k to 1M tokens see median TTFT drop by about 35%"）｜2026-11-03｜hl-threads-num
c24｜兩輪之間保存在記憶體、加密、不寫入磁碟（CL）；最後使用後最晚 1 小時內刪除（RN）｜MT1；MT2；CL；RN｜2026-11-03｜hl-threads-store
c25｜Google Cloud 宣布 google-cloud-developer 外掛可從 Antigravity Marketplace 安裝｜AGY；GCB｜2026-11-03｜hl-agy
c26｜三項好處：依官方文件回答、啟用計費 API 或修改基礎設施前要求同意、最小權限 IAM（Google 自述，非獨立測試）｜AGY；GCB｜2026-11-03｜hl-agy-what, hl-agy-claim
c27｜安裝指令 `agy plugin install google-cloud-developer`（卡片原樣）；內建 Developer Knowledge MCP 伺服器預先授權，不需設 API 金鑰｜AGY；GCB｜2026-11-03｜hl-agy-install
c28｜「頭幾次自己盯著它做了什麼」是節目建議｜—｜—｜hl-agy-claim
c29｜Signal Number：OpenAI 將在喬治亞州 Effingham County 預定興建的資料中心試辦 Grid Protectors Program，極端天氣或緊急情況最多釋出 1,000 百萬瓦，約夠 70 萬戶的冷氣（The Verge 的換算）｜GRID；V2（"free up to 1,000 megawatts … enough to power air conditioners in around 700,000 homes"）｜2026-11-03｜hl-number, hl-number-what
c30｜宣布正值美國各地反對資料中心的聲浪擴大；報導沒有成效、時程或協議內容｜GRID；V2｜2026-11-03｜hl-number-what
c31｜猶他州 Box Elder County 批准的資料中心預期用電超過該州 2025 年尖峰需求兩倍、居民抗議；田納西、佛羅里達等州立法防止能源成本轉嫁居民｜GRID；V2｜2026-11-03｜hl-number-ctx

## Signal of the Day

c32｜TWCA 已於 11 月 1 日完成 9,772 張憑證重新產製，透過主動補發機制由系統以電子郵件寄給原申請機關承辦人（旁白「11 月初，信箱裡來了一封系統寄的信」是想像情境；新聞稿沒有寫寄信的確切日期，所以不說 11 月 1 日寄出）｜TWCA；MODA｜2026-11-03｜sd-inbox, sd-why-me, sd-worklist, sd-timeline, sd-back
c33｜平均每個機關約 10 張（9,772 ÷ 962 ≈ 10.2，換算）｜MODA｜2026-11-03｜sd-not-alone
c34｜TLS 憑證用於建立安全通訊；TLS 全名 Transport Layer Security（新聞稿寫法）；「通道的鎖」是節目的比喻｜TWCA；MODA｜2026-11-03｜sd-what, sd-tls, sd-what2
c35｜國際標準要求序號含 64 bits 以上的密碼學安全亂數（「猜不到」「用專門方法產生、讓人推算不出來」是對「密碼學安全亂數」的白話說明）｜TWCA；MODA｜2026-11-03｜sd-serial, sd-random
c36｜TWCA 序號設計為 128 bits，實際僅首尾各 12 bits 為有效隨機數、中間填補定值，實際隨機亂數僅 24 bits；中間 104 bits＝128−24（換算）；「128 格密碼鎖」是比喻｜TWCA；MODA｜2026-11-03｜sd-bits, sd-lock, sd-think
c37｜24 bits 約 1,677 萬種組合（2²⁴＝16,777,216）；64 bits 是它的 2⁴⁰ ≈ 1.1 兆倍（換算）；1、2、3 位元分別 2、4、8 種（算術）｜—｜2026-11-03｜sd-scale, sd-double
c38｜數發部 10 月 30 日接獲通報，立即要求業者兩日內產製符合規定的新憑證，並啟動跨機關聯繫通知；啟動資訊主管聯繫機制請各機關資訊主管督促｜TWCA；MODA｜2026-11-03｜sd-found, sd-timeline
c39｜截至 11 月 2 日晚間 926 張完成更新；926 ÷ 9,772 ≈ 9.5%（不到一成，換算）；距 11/6 尚有四天；剩 8,846 張、每天約 2,212 張（換算）｜TWCA；MODA｜2026-11-03｜sd-timeline, sd-progress, sd-percent, sd-pace, tk-unsure
c40｜數發部已委託獨立第三方專業機構對 TWCA 深入檢測、檢視憑證產製及管理機制；另將調查違約，依約罰款及求償；罰款金額未公布｜TWCA；MODA｜2026-11-03｜sd-who, sd-next, sd-buyer
c41｜「源頭的反應不慢」「兩天內做完」：10/30 通報、11/1 完成重製（評語是節目的看法）｜MODA｜2026-11-03｜sd-speed, sd-timeline
c42｜TWCA 的網站 TLS 憑證除提供民間作為網站憑證，也經由數發部採購提供各政府機關申請使用｜TWCA；MODA｜2026-11-03｜sd-why-twca, sd-buyer, sd-private
c43｜數發部籲請各機關及其他 TWCA 憑證的使用者於 11 月 6 日前完成更新；新聞稿只盤點政府機關，沒有民間數量、沒有機關名單｜TWCA；MODA｜2026-11-03｜sd-private, sd-private-n, sd-list, tt-owner
c44｜更新的目的是避免影響網站正常瀏覽｜MODA｜2026-11-03｜sd-goal
c45｜若未於 11 月 6 日前更新，民眾瀏覽時「可能」出現安全性警示；此事目前並未造成具體資安危害（「目前不是一件被駭的事」依後者）｜TWCA；MODA｜2026-11-03｜sd-harm, sd-harm2, sd-may, sd-recap, outro
c46｜資料只講台灣，不推論亞洲其他地方｜—｜—｜sd-asia
c47｜「機關要在期限前裝好新憑證、一般民眾不用安裝任何東西」：新聞稿的呼籲對象是各機關與其他 TWCA 憑證使用者；「留意警告」是節目建議｜TWCA；MODA｜2026-11-03｜sd-todo
c48｜數發部表示將持續追蹤，確保所有機關盡速完成更新；「期限過後會不會公布最後張數」是節目要觀察的事，不是數發部的承諾｜MODA｜2026-11-03｜sd-watch2
c49｜「九千多張憑證要在一週內換掉」：11/1 重製到 11/6 期限｜MODA｜2026-11-03｜sd-wrap

## What People Are Saying

c50｜訴狀："Brave has never asked for the Publishers' permission to access their websites, much less to copy the material and provide it to users or other AI companies"（卡片只引前半句）｜BRAVE；V1｜2026-11-03｜wp-complaint
c51｜紐約時報發言人 Graham James："Brave has flouted established copyright law and ignored repeated requests by The Times to stop its infringing conduct"（卡片引中段）｜BRAVE；V1｜2026-11-03｜wp-nyt
c52｜Perplexity 首席傳播長 Jesse Dwyer："The New York Times is overpaying its attorneys and underpaying its journalists."（原文接著括號一句說訴狀有不實資訊，卡片與旁白未引）；Brave、Anthropic、Mistral、SpaceXSI、Cohere 未立即回應｜BRAVE；V1｜2026-11-03｜wp-perplexity, wp-react
c53｜案件牽涉新聞內容能否未經同意被用於 AI｜BRAVE｜2026-11-03｜wp-question
c54｜OpenAI 把為資料中心供電的發電廠說成 "a resource that utilities can call on when communities need it most."｜GRID；V2｜2026-11-03｜wp-openai
c55｜OpenAI 把 AI 資料中心改稱 "compute campuses"；The Verge 稱此舉是為了與其不佳的公眾形象切割（"in an effort to separate from their poor public reputation"）｜GRID；V2｜2026-11-03｜wp-campus

## Money Signal

c56｜巴西最大加密貨幣交易所 Mercado Bitcoin 11 月 2 日凌晨發現資安事件、暫停存提款；聲明 "As a preventive protection measure, deposits and withdrawals are temporarily suspended."；未給恢復日期｜MB1；DC1｜2026-11-03｜ms-open, ms-quote
c57｜交易所稱沒有客戶損失、資料沒有外洩｜MB1；DC1｜2026-11-03｜ms-who
c58｜Chainalysis 稱約 4,900 萬美元被盜、分布於 17 條區塊鏈（Chainalysis 說法，它自己參與應對）｜MB2；CH｜2026-11-03｜ms-who
c59｜Hypernative 初步分析標記超過 4,000 萬美元可疑轉帳，交易所未確認｜MB1；DC1｜2026-11-03｜ms-who
c60｜Chainalysis 稱協助凍結近 1,000 萬美元，其中 Tether 凍結逾 900 萬美元被盜 USDT；穩定幣由特定機構集中發行，發行方可凍結｜MB2；CH｜2026-11-03｜ms-freeze
c61｜凍結會讓代幣無法移動，但不會把資金歸還所有人（Decrypt）；「放在交易所的資產可能一夕之間領不出來」是節目從這次暫停提款得出的提醒｜MB1；DC1｜2026-11-03｜ms-not, ms-lesson
c62｜Squarespace 發言人：裁減全球約 19% 員工、約 300 人；目的在簡化營運、聚焦優先事項、加快速度｜SQ；TC2；V3｜2026-11-03｜ms-sq, ms-sq-ai
c63｜The Verge：受影響者獲 16 週基本薪資、醫療福利延續到 2027 年 5 月｜SQ；V3｜2026-11-03｜ms-sq-facts
c64｜TechCrunch：AI 與 vibe coding 網站建置工具大幅改變產業；報導並未證明 AI 是裁員直接原因｜SQ；TC2｜2026-11-03｜ms-sq-ai, ms-sq-link
c65｜據 TechCrunch，Trajectory 完成 4,500 萬美元 A 輪，Sequoia 領投，Nvidia 等參與｜TRAJ；TC3｜2026-11-03｜ms-traj
c66｜後訓練平台：從開源模型出發，以使用回饋持續再訓練；共同創辦人稱律師、醫師等專家可近乎自動地自行改進模型；「更快、更便宜」是創辦人說法，無第三方評估｜TRAJ；TC3｜2026-11-03｜ms-traj-what

## Try This

c67｜四步（停下來看清楚、不在跳過警告的頁面輸入密碼或身分證字號、確認網址、晚點再試或打機關電話）與「點網址列左邊的圖示看憑證發行者」都是節目建議，不是數發部的指示；旁白第一句就說明｜—（警示的可能性見 c45）｜—｜tt-open, tt-steps, tt-owner

## Noise of the Day

c68｜據 Decrypt 引述 404 Media：員工 8 月要求幾天做滲透測試，執行長 Andy Yen 回覆 "…loser thinking. Of course it's possible to be fast and secure."（卡片略去前面的粗話）｜PROTON；DC2｜2026-11-03｜nd-quote
c69｜用戶表示取消訂閱；意見回饋論壇要求 Yen 下台的提案有 2,020 票；Decrypt 指出這是憤怒情緒，不是經查證的流失客戶數｜PROTON；DC2｜2026-11-03｜nd-react, nd-open
c70｜10 月 30 日（上週五）取消員工 AI 重新面談｜PROTON；DC2｜2026-11-03｜nd-react
c71｜技術長 Bart Butler 11 月 1 日發表工程宣言："Your job is to help the LLM write better code faster."；Proton 堅持路線（"Doubling on its stance"）｜PROTON；DC2｜2026-11-03｜nd-manifesto

## Sola's Take、片尾

c72｜「今天最重要的是 TWCA」「我不確定來不來得及」是節目的看法；依據 c3、c39｜—｜—｜tk-main, tk-unsure
c75｜每則的完整整理在 Mokaair 文章，連結在說明欄（說明欄列 12 篇站上文章）｜各站上文章｜2026-11-03｜tk-site
c73｜片尾答案：沒換好的網站在 11/6 之後可能跳警告（c45）｜MODA｜2026-11-03｜outro

## 與企劃不同的地方

- 企劃把 Trajectory 列為 Money Signal 的「錢流進來的一邊」，但〈不選〉沒有提；撰稿時照〈選題〉表放進 Money Signal（ms-traj、ms-traj-what）。
- Brave 的 What People Are Saying 另外加了 OpenAI 兩個說法（wp-openai、wp-campus），章節名改成「Brave and OpenAI」。

## 我懷疑但沒動的事

- The Verge 的 Brave 報導 11/2 更新：其中一件訴訟是由 New York Daily News、Chicago Tribune、Orlando Sentinel 三家報社自己提起，不是經營它們的公司；站上文章寫的是「經營這三家的公司」。本集旁白只說「紐約時報和其他媒體」，沒有用到這個細節，但站上文章可能需要修正（交給站主或內容產線）。
- Tether 凍結的數字兩家說法不同：Decrypt 引述 Tether 執行長「逾 450 萬 USDT」，Chainalysis 稱 Tether 凍結「逾 900 萬美元」。卡片與旁白用 Chainalysis 的數字並標明是 Chainalysis 說的；可能是時間點不同。
- 「11 月初，信箱裡來了一封系統寄的信」是情境：新聞稿說 11/1 完成重製並以主動補發機制寄送，沒有寫寄出日期。
- Bugzilla 的白話說明（「國際社群拿來回報問題的平台」）來源沒有寫，是一般說明；新聞稿只寫「國際社群 Bugzilla」。
- Try This 的「點網址列左邊的圖示」：各瀏覽器圖示不同（鎖頭或設定圖示），所以沒有說是鎖頭。
- 訊息串 35% 的條件（多數 Claude Code 使用者預設啟用）旁白沒有唸，只在這裡記。

## 進度

- 全部 105 個場景已寫完（sd-open、wp-open 是串場，沒有事實主張）；`lint` 0 錯誤（剩下的警告見撰稿回報）。
- 待做：另派查核代理照 `prompts/verifier-video.md` 逐則對回來源；Whisper 第二意見與試聽（新加的發音字典詞）；配樂與音效由協調者處理。
