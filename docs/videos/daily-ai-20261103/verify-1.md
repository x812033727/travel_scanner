# daily-ai-20261103 查核第 1 輪

查核日 2026-11-03。查核代理不是撰稿人。每一條旁白（`text`，Sola 與 Kai 兩位都查；本片沒有 `say`）、每張卡片的 `data`（含 `source`、`caption`、`note`）、縮圖、`youtube.title`、`description`、`tags` 都抽出來逐條對照：
站上 13 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，1.5 秒一篇，全部 HTTP 200、`status: published`、news_date 2026-11-02）與 `video.json` `sources` 的 14 個官方頁或報導，2026-11-03 全部重新打開；另外用 Mozilla Bugzilla 的 REST API 找到並打開 TWCA 的兩則通報（站上文章沒有引用，數發部新聞稿只寫「國際社群 Bugzilla」）。

## 來源代號

站上文章（全部 200）：

| 代號 | slug |
| --- | --- |
| S-TWCA | tech-news-twca-certificate-20261102 |
| S-CHAT | ai-news-chatgpt-merge-chat-work-tabs-20261102 |
| S-BRAVE | ai-news-nyt-sues-brave-ai-scraping-20261102 |
| S-GENIE | ai-news-genie-4-research-preview-20261102 |
| S-MT1 | ai-news-claude-message-threads-20261102 |
| S-MT2 | ai-news-message-threads-20261102 |
| S-AGY | ai-news-google-cloud-antigravity-plugin-20261102 |
| S-GRID | ai-news-openai-grid-protectors-program-20261102 |
| S-MB1 | crypto-news-mercado-bitcoin-halts-withdrawals-20261102 |
| S-MB2 | crypto-news-mercado-bitcoin-hack-freeze-20261102 |
| S-SQ | tech-news-squarespace-layoffs-20261102 |
| S-TRAJ | ai-news-trajectory-series-a-20261102 |
| S-PROTON | tech-news-proton-ai-backlash-20261102 |

官方頁與報導（2026-11-03 重開，全部 HTTP 200，沒有轉址）：

| 代號 | URL（頁面上的日期） |
| --- | --- |
| MODA | https://moda.gov.tw/press/press-releases/21226 （建立日期 2026-11-02，數位政府司） |
| BZ1 | https://bugzilla.mozilla.org/show_bug.cgi?id=2087236 （REST API 讀取；建立 2026-10-29 19:31 UTC＝台灣 10/30 03:31；「TWCA: CA certificate serial numbers contain fewer than 64 bits of CSPRNG output」） |
| BZ2 | https://bugzilla.mozilla.org/show_bug.cgi?id=2087918 （建立 2026-11-02 00:16 UTC；subscriber 憑證 63 bits；TWCA 說合併到 BZ1） |
| TC1 | https://techcrunch.com/2026/11/02/openai-is-finally-merging-chatgpts-chat-and-work-tabs/ （2026-11-02 05:57 PST） |
| V1 | https://www.theverge.com/tech/1024588/brave-lawsuit-ai-scraping-new-york-times （Nov 2, 2026, 5:51 PM UTC；有「Update, November 2nd」） |
| DM | https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/ （October 27, 2026） |
| G10 | https://blog.google/innovation-and-ai/technology/ai/google-ai-updates-october-2026/ （published_time 2026-11-02） |
| CL | https://claude.com/resources/articles/message-threads （November 2, 2026） |
| RN | https://platform.claude.com/docs/en/release-notes/overview （November 2, 2026 條目） |
| GCB | https://cloud.google.com/blog/topics/developers-practitioners/google-cloud-developer-plugin-now-available-in-antigravity-marketplace/ （**November 3, 2026**，datePublished 2026-11-03） |
| V2 | https://www.theverge.com/ai-artificial-intelligence/1024604/openai-data-center-grid-protection-program （Nov 2, 2026, 6:01 PM UTC） |
| DC1 | https://decrypt.co/382341/mercado-bitcoin-halts-withdrawals-40-million-hack （2026-11-02 16:46Z，更新 20:29Z） |
| CH | https://www.chainalysis.com/blog/chainalysis-response-mercado-bitcoin/ （November 2, 2026） |
| TC2 | https://techcrunch.com/2026/11/02/web-host-squarespace-lays-off-19-of-its-employees/ （2026-11-02 11:25 PST） |
| V3 | https://www.theverge.com/tech/1024447/squarespace-layoffs-19-percent （2026-11-02 16:50 UTC） |
| DC2 | https://decrypt.co/382353/proton-users-revolt-ceo-calls-security-caution-loser-thinking-ai （2026-11-02 18:16Z） |
| TC3 | https://techcrunch.com/2026/11/02/trajectory-raises-45m-to-make-ai-model-training-accessible-to-nontechnical-experts/ （2026-11-02 15:13 PST；撰稿人沒開，本輪開了） |

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10 月 30 日國際社群 Bugzilla 上出現一則通報 | ef3u；co-report.kicker；e8o9–li4w；sd-found | MODA、BZ1 | 200 | CONFIRMED（MODA「國際社群Bugzilla於10月30日通報」；BZ1 建立於 10-29 19:31 UTC＝台灣 10/30；數發部「於10月30日接獲通報」，所以 li4w「同一天」成立） | |
| 2 | 被點名的是 TWCA 發出的網站憑證 | gpfe；co-report.text；7o12 | BZ1、MODA | 200 | CHANGED（BZ1 點名的是 TWCA 的 **CA 憑證**；MODA 只說「TWCA所核發的部分憑證」，政府網站憑證受影響是數發部之後盤點的） | gpfe「…發出的網站憑證。」→「…發出的部分憑證。」；co-report.text「Taiwan gov websites / certificates flagged」→「TWCA certificates / flagged」；7o12「等等，網站憑證？牽連到多少個網站？」→「等等，憑證？牽連到多少個網站？」 |
| 3 | 問題出在序號裡，少了一樣東西 | iiqo；co-flaw | MODA | 200 | CONFIRMED（伏筆，揭曉在 l0zw） | |
| 4 | 數發部盤點：962 個政府機關、9,772 張憑證 | k6z8；co-scale；sd-not-alone；sd-recap；縮圖 sub；說明欄 | MODA | 200 | CONFIRMED（「經盤點，本次事件共涉及962個政府機關、9,772張網站憑證」） | |
| 5 | 11 月 2 日晚上的數字會嚇一跳 | buyx；co-count | MODA | 200 | CONFIRMED（伏筆，揭曉 926） | |
| 6 | 期限 11 月 6 日、這個星期五 | 7sfr、mzc4、mrgu、jrr2、8mtr、x0sf；co-date；intro-kai；標題 | MODA；曆法 | 200 | CONFIRMED（「未於11月6日前完成憑證更新」；2026-11-06 是星期五） | |
| 7 | 今天是 11 月 3 日星期二 | eius；intro | 曆法 | — | CONFIRMED | |
| 8 | 先看昨天 11 月 2 日的科技新聞 | v7on；hl-open | S-* | 200 | CONFIRMED（13 篇 news_date 都是 11-02；GCB 例外見 #33） | |
| 9 | 據 TechCrunch，OpenAI 寄信：ChatGPT 桌面版 Chat 和 Work 分頁合併 | nzz5、o214；hl-chat | TC1、S-CHAT | 200 | CONFIRMED（「according to an email sent to users」） | |
| 10 | 分頁太多、忘記自己在哪；TechCrunch 也這樣解讀；可帶自己的檔案和外掛；Codex 獨立 | ukeq、mzba、514p；hl-chat-why | TC1 | 200 | CONFIRMED（「In an apparent effort to address this」；「Codex will remain a separate experience」） | |
| 11 | 信裡的例子：做網站、做簡報、在網路上替你處理事情、你審閱引導 | ka6r、zrrd；hl-chat-do | TC1 | 200 | CONFIRMED（「build a website, create a presentation, or do things for you on the web, while reviewing and guiding its work」） | |
| 12 | Anthropic 九月把 Claude 聊天和 Cowork 放在同一個畫面 | kpvy；hl-chat-claude | TC1 | 200 | CONFIRMED（「Rival Anthropic merged Claude's chat and Cowork functions into one screen in September」） | |
| 13 | ChatGPT 和 Codex 同一個 token 額度池；多數不受影響；用量大的可能更常等重置；先部分人試用、蒐集意見再全面推出 | s2w2、a0s2、zndh、l28k、ikue、m0j4；hl-chat-quota | TC1 | 200 | CONFIRMED（「based on usage and model, some folks might need to wait for resets more frequently」；「select users for feedback before it is rolled out widely」） | |
| 14 | 據 The Verge，紐約時報和其他媒體告 Brave 的開發公司 | nf8a；hl-brave | V1、S-BRAVE | 200 | CONFIRMED（「The New York Times and a group of other publications have filed lawsuits」，複數） | |
| 15 | 指控：未經許可抓內容、索引收費給 AI 公司、讓使用者繞過付費牆 | m29b、viek、toml；hl-brave-claims | V1 | 200 | CHANGED（三項都是原告指控，事實對；但 V1 11/2 更新後寫明索引與 AI 公司那份訴狀是 New York Daily News、Chicago Tribune、Orlando Sentinel 三家報紙自己提的，紐約時報另告一案。原稿沒有掛名，聽起來像紐約時報的訴狀） | m29b「第一，沒經過許可…」→「其中三家報紙的訴狀說，第一，沒經過許可，用程式大量抓新聞網站的內容。」；source「The Verge, Nov 2, 2026 · allegations」→「The Verge, Nov 2, 2026 · 3 papers' complaint」 |
| 16 | 訴狀點名五家：Anthropic、Perplexity、Mistral、xAI、Cohere | rlmd；hl-brave-named | V1 | 200 | CONFIRMED（同一份三家報紙的訴狀；#15 改後「訴狀」指得清楚） | |
| 17 | Brave 在瀏覽器宣傳付費牆阻擋功能；跟指控的關係報導沒說 | v9cr、y95p；hl-brave-paywall | V1 | 200 | CONFIRMED（「promotes "hundreds of top publishers" as being accessible through its "Paywall blocker"」） | |
| 18 | 都是原告指控，沒有法院裁決；用 Brave 的人目前不用動手（節目建議） | x79m、4nj9；hl-brave-status | V1 | 200 | CONFIRMED | |
| 19 | DeepMind 10 月 27 日發表 Genie 4；昨天的十月整理又提 | taej；hl-genie | DM、G10 | 200 | CONFIRMED（DM October 27, 2026；G10 published 2026-11-02） | |
| 20 | 打一句話生出有畫面有聲音的場景；鍵盤走動轉鏡頭；打字改天氣、加人物 | 1ixa、rmb4、c7xv；hl-genie-how | DM | 200 | CONFIRMED（native audio；「standard keyboard controls for navigation and camera control」；「changing the weather … introducing a new person or object」） | |
| 21 | 研究預覽、只給受信任測試者；之後先開放 Ultra 訂閱者和早期合作開發者 | 4hqo、kh8c；hl-genie-who | DM | 200 | CONFIRMED（「Google AI Ultra subscribers in Project Genie and early access partners of the Gemini API and Google AI Studio」） | |
| 22 | DeepMind 承認跑久了細節和物件會走樣；台灣一般人現在玩不到 | d6uj、24id；hl-genie-limit | DM | 200 | CONFIRMED（「visual details and object permanence can still shift or drift over time」；第二句是依開放對象推論，DM 沒有地區） | |
| 23 | 影片和聲音都有 SynthID；肉眼看不到；Google 有偵測工具 | gbk6、wbhp；hl-genie-mark | DM、G10 | 200 | CONFIRMED（「imperceptible digital watermarking」；SynthID Detector expanding globally in English） | |
| 24 | Anthropic 昨天推出訊息串公開測試版，給做 AI 代理的開發者 | iuqx；hl-threads | CL、RN | 200 | CONFIRMED（CL November 2, 2026「public beta」） | |
| 25 | 以前每輪重送整段對話；現在對話留伺服器，只送新訊息 | r7p9、vkiq、nxiw；hl-threads-how | CL、RN | 200 | CONFIRMED | |
| 26 | 50 萬–100 萬 token，TTFT 中位數少約 35% | tq4k、g7ke；hl-threads-num.stats[0] | CL | 200 | CHANGED（數字對，但是 Anthropic 自己的數據，條件是「message threads on by default for most Claude Code users」；旁白沒掛名） | tq4k「效果呢？五十萬…」→「效果呢？Anthropic 說，五十萬到一百萬 token 的長對話，」 |
| 27 | 不省錢：每輪仍讀完整段對話，token 用量和費率不變 | 7j9q；stats[1] | CL | 200 | CONFIRMED（「token usage stays the same」「Standard Claude token rates … apply」） | |
| 28 | 閒置五分鐘就過期，要重送整段 | jrm6；stats[2] | CL、RN | 200 | CONFIRMED（「expires 5 minutes after its last request」） | |
| 29 | 兩輪之間存記憶體、加密、不寫磁碟；最晚最後使用後一小時內刪除 | qzhk、1pe4；hl-threads-store | CL、RN | 200 | CONFIRMED（RN「deleted no more than 1 hour after its last use」） | |
| 30 | Google Cloud 在 Antigravity 外掛市集上架官方外掛（原稿「昨天」） | lg3m；hl-agy.kicker「Nov 2 · Google Cloud」 | GCB | 200 | CHANGED（GCB 頁面日期與 datePublished 都是 **2026-11-03**；站上文章 2026-11-02 21:30Z 已經引用它，所以 11/2 美國時間已上線，但官方日期是 11/3） | lg3m 拿掉「昨天」；kicker →「Google Cloud blog」 |
| 31 | 三項：查最新官方文件、啟用收費服務或改設定前先問、只拿需要的權限 | hiuy、ubrh、fr7o；hl-agy-what | GCB | 200 | CONFIRMED（「requires your consent before it enables billable APIs or modifying cloud infrastructure」；least-privilege IAM） | source「Google Cloud blog, Nov 2, 2026」→「…Nov 3, 2026」（依 #30） |
| 32 | 安裝指令 `agy plugin install google-cloud-developer`；文件伺服器預先授權、不用設 API 金鑰 | 53j2、14xe；hl-agy-install | GCB | 200 | CONFIRMED（指令逐字相同；「pre-authorized by default. You don't need to configure API keys」） | caption 日期 Nov 2 → Nov 3（依 #30） |
| 33 | 都是 Google 自己的說法，沒有獨立測試；頭幾次自己盯著（節目建議） | kj6x、kwp3；hl-agy-claim | GCB、S-AGY | 200 | CONFIRMED | |
| 34 | 訊號數字 1,000 百萬瓦 | 9uxd；hl-number | V2 | 200 | CONFIRMED（「free up to 1,000 megawatts」） | |
| 35 | 「The Verge 換算」大約夠七十萬戶開冷氣 | pb84 | V2 | 200 | CHANGED（V2：「the company promises to free up to 1,000 megawatts … enough to power air conditioners in around 700,000 homes」，沒說是 The Verge 自己算的，比較像轉述 OpenAI） | 「The Verge 換算，…」→「The Verge 報導說，大約夠七十萬戶人家開冷氣。」 |
| 36 | 喬治亞州預定興建的資料中心試辦；極端天氣或緊急時；反對聲浪；沒有成效與時程 | d7ja、hnnd、47c4；hl-number-what | V2、S-GRID | 200 | CONFIRMED（Effingham County；S-GRID「報導未提供實際成效、時程」） | |
| 37 | 猶他州一個郡批准的資料中心，預估用電超過全州 2025 年尖峰兩倍；田納西、佛羅里達等州立法 | wc9b、qr0z、pfbg；hl-number-ctx | V2 | 200 | CONFIRMED（Box Elder County；「more than double the state's peak electricity demand in 2025」；Tennessee, Florida, Oklahoma, Oregon） | |
| 38 | 從一封信講起；11 月初信箱來一封系統寄的信、附新憑證 | lfuc；sd-inbox | MODA | 200 | CHANGED（旁白「11 月初」與情境說法成立；但卡片 kicker「Nov 1」與 key「Nov 1: a new certificate arrives」把寄信日寫死，新聞稿只說 11/1 完成重製、以主動補發機制寄送，沒寫寄出日） | kicker「Nov 1」→「Early November」；key →「A new certificate arrives」 |
| 39 | 原本那張出問題，TWCA 主動補發；寄到各機關承辦人 | 3ul9、br47、pdxn；sd-why-me、sd-worklist | MODA | 200 | CONFIRMED（「透過主動補發機制，由系統直接以電子郵件將新憑證檔寄送予原申請機關承辦人」） | |
| 40 | 平均一個機關大約十張 | icuv；sd-not-alone.stats[2]「~10, our calculation」 | 換算 | — | CONFIRMED（9,772 ÷ 962 = 10.16；卡片標 our calculation） | |
| 41 | 網站憑證是用來建立安全通訊的電子憑證；TLS＝傳輸層安全性；「通道的鎖」是比喻 | qfgy、mdc4、2ttq；sd-what、sd-tls、sd-what2 | MODA | 200 | CONFIRMED（「TLS憑證（Transport Layer Security Certificate）用於建立安全通訊」） | |
| 42 | 國際標準：序號至少 64 位元密碼學安全亂數 | gtvb、hbcd；sd-serial、sd-random | MODA、BZ1 | 200 | CONFIRMED（MODA「64 bits 以上密碼學安全亂數」；BZ1 引 CA/B Forum BR 7.1「at least 64 bits of output from a CSPRNG」，2016-09-30 起） | |
| 43 | 設計成 128 位元；中間填固定值；只有頭尾各 12 位元、合計 24 位元是亂的；中間 104 格 | ic4d、dik4、l0zw、3qyc；sd-bits、sd-lock | MODA | 200 | CONFIRMED（「設計為128 bits，但實際僅首尾各 12 bits 為有效隨機數、中間皆填補為定值，實際隨機亂數僅 24 bits」；128−24＝104。BZ1 描述 CA 憑證的結構不同，見「懷疑但沒改」） | |
| 44 | 24 位元約一千六百多萬種；64 位元是它的一兆倍以上；每多一位元翻倍；1、2、3 位元＝2、4、8 | c7a9、y0sv、np4m、j1tm、9a4v；sd-scale、sd-double | 算術 | — | CONFIRMED（2²⁴＝16,777,216 ≈ 16.8M；2⁴⁰＝1,099,511,627,776 ≈ 1.1 兆，「一兆倍以上」成立；卡片 source「Our calculation from MODA's figures」「Basic arithmetic」） | |
| 45 | Bugzilla 是國際社群回報問題的平台 | wo02；sd-bugzilla | BZ1 | 200 | CONFIRMED（一般說明；BZ1 是外部研究者提出的公開事件報告） | |
| 46 | 10/30 通報，數發部要業者兩天內做出新憑證；兩天後 TWCA 全部重做好 | kti4、kr7t、vtyu、eo9z、o44n；sd-timeline rows 0–1；sd-speed | MODA | 200 | CONFIRMED（「要求業者於兩日內產製」；「已於11月1日完成政府機關9,772張TLS憑證重新產製」） | |
| 47 | 接著系統寄給承辦人；數發部找各機關資訊主管催 | 6be6、eu50；sd-timeline row 2 | MODA | 200 | CHANGED（事實對；但表格第三列日期寫「Nov 1」，新聞稿沒有寄信日期；表名「Five days, so far」也不對：10/30 到 11/2 是四天，表上排到 11/6） | row 2「Nov 1」→「Then」；title「Five days, so far」→「From report to deadline」 |
| 48 | 11 月 2 日晚上完成更新 926 張 | x50d；sd-timeline row 3「Nov 2 pm」；sd-progress | MODA | 200 | CONFIRMED（「截至11月2日晚間，已有926張憑證完成更新」） | |
| 49 | 不到一成；926 ÷ 9,772 ≈ 9.5%；離期限還有四天 | mbdm、gr9q；sd-progress.sub；sd-percent | 換算 | — | CONFIRMED（9.476%；11/2→11/6 四天；sd-percent kicker「The math」） | |
| 50 | 剩 8,846 張；一天約 2,200 張 | rcyb、dtn9、2c43；sd-pace | 換算 | — | CONFIRMED（9,772−926＝8,846；÷4＝2,211.5；卡片 source「Our calculation from MODA's figures」） | |
| 51 | 誰買單：機關資訊人員幾天內裝；數發部已委託第三方深入檢測；調查違約、依約罰款和求償 | 06jg、fbk7、n7o2；sd-who | MODA | 200 | CONFIRMED（「已委託獨立第三方專業機構，後續針對TWCA進行深入檢測」；「針對違約情事進行調查，並依約罰款及求償」） | |
| 52 | 憑證由數發部採購再提供各機關申請；數發部同時是買方和要求改善的人；合約與罰款細節未公布 | iopm、4hnr、bkhe、i4rz；sd-why-twca、sd-buyer | MODA | 200 | CONFIRMED（新聞稿沒有金額） | |
| 53 | TWCA 也賣給民間；數發部也請其他 TWCA 憑證使用者期限前更新；民間數字、機關名單都沒公布 | k4s2、ds3a、lvsq、ebou；sd-private、sd-private-n、sd-list | MODA | 200 | CONFIRMED（「籲請各機關及其他TWCA憑證的使用者，盡速於11月6日前完成」） | |
| 54 | 全部在台灣；資料只講台灣，不猜亞洲 | q27j、391w、nf95；sd-taiwan、sd-asia | MODA | 200 | CONFIRMED | |
| 55 | 目的是不影響網站正常瀏覽 | 7onc；sd-goal | MODA | 200 | CONFIRMED | |
| 56 | 沒換好的網站，瀏覽時「可能」看到安全性警示；目前沒有具體資安危害；不是網站被入侵 | nwek、d76o、y7n0、r13g、hwxm、ilw7、ep6d；sd-harm、sd-harm2、sd-may、sd-recap、outro | MODA | 200 | CONFIRMED（「可能出現安全性警示訊息」「目前並未造成具體資安危害」；「不是被入侵」是依後者，加了「目前」） | |
| 57 | 機關要裝新憑證；一般人不用安裝任何東西，留意警告（節目建議） | iq7a、1mxe；sd-todo | MODA | 200 | CONFIRMED（呼籲對象是機關與 TWCA 憑證使用者；卡片 source 標 Tech Signal advice） | |
| 58 | 接下來看三件事：能否換完、第三方檢測、罰多少；數發部說會持續追蹤確保盡快換好 | x0sf、2drw、t2k4、x127、dnyh；sd-next、sd-watch2 | MODA | 200 | CONFIRMED（「數發部將持續追蹤，確保所有機關盡速完成更新」） | |
| 59 | 九千多張要在一週內換掉；國際社群先抓到 | wf3r、9v5q；sd-wrap | MODA、BZ1 | 200 | CONFIRMED（11/1 重製到 11/6；BZ1「filed by external researchers, not by the CA」） | |
| 60 | 裝上就不在可能跳警告的那批 | byh4；sd-back | MODA | 200 | CONFIRMED | |
| 61 | 訴狀引句「Brave has never asked…」 | q8s1、ow7l；wp-complaint | V1 | 200 | CHANGED（引句逐字相符，但出自三家報紙的訴狀，見 #15） | q8s1「先聽訴狀：…」→「先聽那三家報紙的訴狀：…」；source「Complaint, quoted by The Verge, Nov 2, 2026」→「3 papers' complaint · The Verge, Nov 2, 2026」 |
| 62 | 紐約時報發言人：無視既有著作權法、不理一再要求停止 | 5hvj、fdd7；wp-nyt | V1 | 200 | CONFIRMED（Graham James；卡片引句逐字） | |
| 63 | 多數沒立即回應；Perplexity 首席傳播長：付律師太多、付記者太少；Brave 刊出時未回應 | 80c1、257x、x29q；wp-perplexity、wp-react | V1 | 200 | CONFIRMED（「Brave, Anthropic, Mistral, SpaceXSI, and Cohere didn't immediately reply」；引句逐字） | |
| 64 | 這場官司問的是新聞能不能不經同意給 AI 用 | aq3c；wp-question | S-BRAVE | 200 | CONFIRMED（站上文章的框架） | |
| 65 | OpenAI 把發電廠說成社區最需要時能調用的資源；改稱 compute campuses；The Verge 解讀是想甩掉壞名聲 | r5yp、l2mc、97qy；wp-openai、wp-campus | V2 | 200 | CONFIRMED（「in an effort to separate from their poor public reputation」） | |
| 66 | 巴西最大加密貨幣交易所 Mercado Bitcoin 11/2 凌晨發現資安事件；存提款暫停；沒給恢復日期 | j8my、akcz、dgf6；ms-open、ms-quote | DC1、CH | 200 | CONFIRMED（引句逐字；「has not given a date for resuming them」） | |
| 67 | 交易所：客戶沒損失、資料沒外洩；Chainalysis：約 4,900 萬美元、17 條鏈；另一家資安公司標記 4,000 萬以上、交易所沒確認 | m2kz、bn9b、gn7y；ms-who | DC1、CH | 200 | CONFIRMED（CH「approximately $49 million」「17 blockchains」；DC1 Hypernative「more than $40 million」） | |
| 68 | Chainalysis 說協助凍結將近一千萬美元 | jc2x；ms-freeze.stats[0] | CH | 200 | CONFIRMED（「help freeze nearly $10 million」） | |
| 69 | 其中九百多萬是 Tether 發行的穩定幣 USDT | zkf5；ms-freeze.stats[1] | CH、DC1 | 200 | CHANGED（CH：Tether「freeze over $9 million in stolen funds」；但 DC1 引 Tether 執行長本人在 X 上說「frozen more than 4.5 million USDT」。原句沒有掛名，也沒交代 Tether 自己的數字，而說明欄連到的 S-MB1 標題就是「Tether 凍結逾 450 萬 USDT」） | zkf5 →「它說其中九百多萬是 Tether 凍結的 USDT；Tether 執行長自己說的是四百五十萬以上。」；stats[1] 加 note「Tether CEO: 4.5M+ USDT」 |
| 70 | 穩定幣由特定公司發行，發行方可凍結；凍結不等於還給原主 | acj7、xv6u；ms-not | CH、DC1 | 200 | CONFIRMED（DC1「a freeze does not by itself return the funds to their owner」） | |
| 71 | 放在交易所的資產可能一夕之間領不出來（節目提醒） | 7rdp、173g；ms-lesson | DC1 | 200 | CONFIRMED（由這次暫停提款推論；不談價格與買賣） | |
| 72 | Squarespace 證實裁全球約 19%、約 300 人 | rdwc；ms-sq；ms-sq-facts.items[0] | TC2、V3 | 200 | CONFIRMED | |
| 73 | 16 週基本薪資；醫療福利到 2027 年 5 月 | 8u6s、4wc0；ms-sq-facts | V3 | 200 | CONFIRMED（「16 weeks of base pay and healthcare benefits into May 2027」） | |
| 74 | 公司說簡化營運、聚焦優先事項；TechCrunch 說 AI 工具大幅改變產業；報導沒證明因果 | n3sb、am2z、nbtr；ms-sq-ai、ms-sq-link | TC2、V3 | 200 | CONFIRMED（「have largely upended the industry」；兩篇都沒把裁員歸因於 AI） | |
| 75 | 據 TechCrunch，Trajectory 募 4,500 萬美元，紅杉領投、輝達參與 | 6m6k；ms-traj | TC3 | 200 | CONFIRMED（「$45 million in a Series A … led by Sequoia, with participation from Nvidia」） | |
| 76 | 從開源模型出發用回饋持續再訓練；律師醫師幾乎可以自己把模型調好 | 9tno、v5cm；ms-traj-what | TC3 | 200 | CONFIRMED（Malde：「can improve the models near automatically themselves」） | |
| 77 | 「更快、更便宜是創辦人的說法」 | h79x | TC3 | 200 | CHANGED（TC3 原文是 TechCrunch 接在 Malde 說法後寫「That capability could make deploying specialized AI faster and cheaper」，不是創辦人原話；沒有第三方評估這點成立） | →「不過會不會更快、更便宜，報導裡只有公司這邊的說法，沒有第三方評估。」 |
| 78 | Try This 四步：停下來看清楚、不急著按繼續前往；不在跳過警告的頁面輸入密碼身分證；確認網址；晚點再試或打機關公布的電話 | ovsd、k6k9、bdwl、z0vl、8ed8；tt-steps | MODA | 200 | CHANGED（安全檢查：開頭已說是節目建議、不是數發部指示；跟新聞稿不衝突，新聞稿沒有給民眾的操作指引。但 bdwl「在跳過警告的頁面上，不要輸入…」預設觀眾會跳過警告，等於默許點過去） | bdwl →「第二，不要跳過警告，更不要在那種頁面輸入密碼、身分證字號。」 |
| 79 | 自家網站：點網址列左邊的圖示看發行者；是 TWCA 的，數發部也請你星期五前更新；找管網站的人確認 | ss4z、wynu、pn0t、nd6o；tt-owner | MODA | 200 | CHANGED（事實成立：數發部請「其他TWCA憑證的使用者」11/6 前更新。ss4z「如果我公司的網站」替 AI 主持人編了一家公司） | ss4z「那如果我公司的網站…」→「那如果公司的網站，憑證也是 TWCA 發的呢？」 |
| 80 | Proton 執行長的一句話被用戶抗議；據 Decrypt 引述其他媒體，八月員工想多花幾天做滲透測試；回說失敗者思維 | tewn、4vux、mhti；nd-open、nd-quote | DC2 | 200 | CONFIRMED（引句逐字，粗話省略；「per 404 Media」） | |
| 81 | 用戶說要退訂；要他下台的提案 2,020 票；Decrypt 提醒是憤怒不是查證過的退訂數 | tidx、lac2；nd-react | DC2 | 200 | CONFIRMED（「had 2,020 votes when reviewed」「anger, rather than a verified count of departing customers」） | |
| 82 | 上週五取消員工 AI 重新面談 | rpad；nd-react.items[2] | DC2 | 200 | CONFIRMED（「Yen canceled the re-interviews on October 30」，10-30 是上週五） | |
| 83 | 技術長發宣言：你的工作是幫 LLM 更快寫出更好的程式碼；路線沒改 | vj4e；nd-manifesto | DC2 | 200 | CONFIRMED（11/1；引句逐字） | |
| 84 | 我的看法：今天最重要的是 TWCA；我不確定來不來得及 | fsiy、b8py、d3a6；tk-main、tk-unsure | brief.md | — | OUT OF SCOPE（觀點，見摘要） | |
| 85 | 每則的完整整理都在 Mokaair 文章，連結在說明欄 | 3u58；tk-site；說明欄 | S-* | 200 | CHANGED（說明欄只列 12 篇，漏了 Money Signal 用到的 S-TRAJ） | 說明欄補上 https://mokaair.com/zh-TW/life/ai-news-trajectory-series-a-20261102 |
| 86 | 縮圖「Renew **certs**」「9,772 Taiwan gov certificates, Nov 6」 | thumbnail.data | MODA | 200 | CONFIRMED | |
| 87 | 標題「Tech Signal 11/3｜Taiwan gov certificates must be renewed by Nov 6」 | youtube.title | MODA | 200 | CONFIRMED（新聞稿是「籲請」，標題的 must 偏強但與 11/6 期限一致，沒改） | |
| 88 | 說明欄主題句、各則來源性質、Try This 是節目建議、不談價格投資 | youtube.description | MODA、各來源 | 200 | CONFIRMED（為了補 S-TRAJ 網址又不超過 5,000 bytes，句尾的免責說明縮寫，意思不變） | |
| 89 | tags | youtube.tags | — | — | OUT OF SCOPE | |
| 90 | 串場與 Kai 的反應句（4woq、b2bl、zft1、r4hb、ijr6、jxcv、dma7、64p6、cvl4、gker、6b7x、fep5、obsw 等） | 各處 | — | — | OUT OF SCOPE（不含新事實；Kai 的反應都是替觀眾問，沒有私人經驗，ss4z 已改） | |

## 摘要

- 查了 90 條（同一事實在多處出現時合為一條）：CONFIRMED 74（#31、#32 事實確認，只隨 #30 改了卡片日期）、CHANGED 13、NOT FOUND 0、OUT OF SCOPE 3。事實改動 11 處：(1) Bugzilla 點名的是 TWCA 的「部分憑證」不是網站憑證（gpfe、7o12、co-report 卡）；(2) Brave 的訴狀與引句改掛「三家報紙的訴狀」（m29b、q8s1、兩張卡的 source）；(3) Anthropic 35% 加掛名（tq4k）；(4) Google Cloud 外掛公告日期是 11/3，拿掉「昨天」、卡片改 Nov 3（lg3m、hl-agy、hl-agy-what、hl-agy-install）；(5) 七十萬戶不是「The Verge 換算」（pb84）；(6) sd-inbox 卡片拿掉沒根據的「Nov 1」寄信日；(7) sd-timeline 第三列「Nov 1」→「Then」、表名「Five days, so far」改掉；(8) Tether 凍結數字兩方各自掛名（zkf5、ms-freeze note）；(9) Trajectory「更快更便宜」不是創辦人原話（h79x）；(10) Try This 第二步不再預設觀眾會跳過警告（bdwl）；(11) 說明欄補上漏掉的 Trajectory 文章。另：ss4z 拿掉 Kai 的「我公司」（不是事實，是不編主持人經驗的規則）。
- TWCA 的數字：962、9,772、926、11/6、128 位元、首尾各 12、24 位元、64 位元以上、兩日內產製、11/1 完成重製、主動補發寄給承辦人、資訊主管聯繫機制、第三方深入檢測、依約罰款及求償，全部與 MODA 新聞稿逐字相符。節目自算的四個數（16,777,216≈一千六百多萬、2⁴⁰≈1.1 兆倍、926/9,772≈9.48%、8,846/4≈2,212、9,772/962≈10.2）算術都對；卡片都標了 Our calculation / Basic arithmetic / The math，旁白用「大約」「平均下來」「怎麼算的」帶出。
- Try This：建議安全，第一句就說「不是數發部的指示」；沒有叫人點過警告（k6k9 明說不要急著按繼續前往，bdwl 已改成不要跳過警告）；新聞稿沒有給民眾的操作指引，所以沒有衝突。
- Brave：V1 的 11/2 更新確認撰稿人的懷疑——一案由 New York Daily News、Chicago Tribune、Orlando Sentinel 三家報紙自己提起（律師 Steven Lieberman 代表三家），紐約時報另告。站上文章 S-BRAVE 仍寫「由經營…的公司所提出」，**站上文章需要修正**（不在本輪可改的範圍）。
- 加密貨幣：全片沒有價格、報酬、漲跌或買賣；ms-lesson 只談存取風險。
- 唸出來的日期：10/30（Bugzilla 與數發部接獲通報）、10/27（Genie 4）、11/1（重製完成）、11/2（各則報導、926 張）、11/6（期限）都與官方頁相符；GCB 例外，已改。
- `sources` 14 個網址 2026-11-03 全部 HTTP 200，`checked_on` 2026-11-03；Bugzilla 沒有加進 `sources`（加了會讓說明欄超過 5,000 bytes，而且旁白的事實都以 MODA 為準）。來源標題「Claude by Anthropic: …」縮成「Anthropic: …」以騰出說明欄空間。
- 會過期的事實：TWCA 更新進度（926，MODA 11/2 晚間）、11/6 期限是否延長、第三方檢測與罰款（MODA 2026-11-02）；BZ1 的完整事件報告 TWCA 承諾 2026-11-12 19:00 UTC 前提出；Brave 訴訟與 Brave 回應（V1 2026-11-02 已更新一次）；Mercado Bitcoin 恢復日期與金額（DC1 2026-11-02 20:29Z 更新）；ChatGPT 合併分頁、Genie 4 開放對象、訊息串測試版狀態。
- 觀點：fsiy、b8py、d3a6 以「我的看法是」「老實說，我不確定」標明，與 brief.md〈站主觀點〉一致（TWCA 最重要、不講成被駭、不確定 11/6 能否換完）。沒有不一致。
- 聽眾檢查（只報告）：超過 40 字的句子 11 句：kpvy 57、taej 57、6m6k 56、lg3m 54、zkf5 49、iuqx 46、j8my 46、s2w2 45、am2z 44、nf8a 43、rdwc 42（zkf5、lg3m 是本輪改的；lg3m 改短了）。沒有「經查證」「根據官方文件」「本影片」、括號或網址；揭曉都在介紹句之後。本輪加進旁白的拉丁詞只有 Anthropic、Tether、USDT，原稿其他句子已經在唸，lint 沒有新增字典警告。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261103` → `daily-ai-20261103: 0 errors, 7 warnings`（重複數字「10」「11」「24」「64」「九百」「九千」與 Headlines 開頭是標籤，都是撰稿時就有的寫作警告；估計 23.5 分鐘，307 句）。中途兩次 error 已解決：hl-brave-claims 的 source 超過 48 字、說明欄超過 5,000 bytes。
- 懷疑但沒改：
  - BZ1 描述的是 TWCA **CA 憑證**的序號結構（`40 | YYYYMMDD | 0…0 | counter | random 3 bytes`，亂數在尾端 24 bits），和 MODA 說的「首尾各 12 bits」不同；BZ2 說 TWCA 的一般 SSL 用戶憑證是 63 bits。政府那 9,772 張的結構只有 MODA 有說，影片照 MODA，卡片 source 也是 MODA，沒改。站主若要更精確，可在 sd-bits 加「數發部說明」。
  - ic4d「設計成 128 位元，看起來是標準的兩倍長」：標準要求的是 64 bits 亂數，不是序號長度；「看起來」有保留，沒改。
  - 標題「must be renewed」：MODA 用「籲請」；但期限是真的，警示可能出現，沒改。
  - fbk7「已經委託第三方，對它做深入檢測」：MODA 是「已委託…後續…進行」，檢測還沒做；句子沒說做完了，沒改。
  - GCB 日期：頁面寫 11/3，但站上文章 11/2 21:30Z 已引用，可能是 Google 部落格以發布後的日期顯示；卡片照官方頁寫 Nov 3。站上文章 S-AGY 的 news_date 11-02 與來源日 2026-11-02 也可能要對一下。
  - tidx「用戶說要退訂」：DC2 是「saying they had canceled subscriptions or would not renew」，大致相符，沒改。
  - meem、ewcf、ebui 是 Kai 用「我」替觀眾問或照 Sola 的「想像你是」演情境，不是私人經驗，沒改。
- 需要第二輪：**是**。本輪改了 11 個事實（超過 3 個），要由另一個代理寫 `verify-2.md`。第二輪完成前，這份稿子不能稱為已查核。
