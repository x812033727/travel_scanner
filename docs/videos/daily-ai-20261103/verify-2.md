# daily-ai-20261103 查核第 2 輪

查核日 2026-11-03。第二位查核代理，不是撰稿人，也不是第 1 輪的查核代理。
第 1 輪改了 11 個事實（超過 3 個），所以照 `verifier-video.md` 再查一輪。本輪做了四件事：一是重查第 1 輪改過的每一行與卡片；二是用新的眼光把整份稿子再看一遍（超過「已確認項目隨機抽三分之一」的要求）；三是改掉協調者點名、第 1 輪標了但沒改的三處（標題的 must、ic4d、fbk7）；四是把唸起來太長的句子縮短。
今天重新打開的頁面有兩類。站上 13 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，間隔 1.5 秒）全部 HTTP 200、`status: published`、news_date 2026-11-02。`video.json` `sources` 的 14 個官方頁或報導，加上 TechCrunch 的 Trajectory 報導（TC3）與 Bugzilla 2087236、2087918 的 REST API（間隔超過 1 秒），也全部 HTTP 200，沒有轉址，也沒有被擋。
來源代號沿用 `verify-1.md`：站上文章是 S-*，官方頁與報導是 MODA、BZ1、BZ2、TC1、V1、DM、G10、CL、RN、GCB、V2、DC1、CH、TC2、V3、DC2、TC3。MODA 今天仍是「建立日期：2026-11-02」，GCB 的 datePublished 仍是 2026-11-03。

## 一、第 1 輪改過的 11 處與 ss4z（全部重查）

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Bugzilla 點名的是 TWCA 發出的「部分憑證」；co-report「TWCA certificates / flagged」；7o12「等等，憑證？」 | gpfe；co-report；7o12 | BZ1、BZ2、MODA | 200 | CONFIRMED。BZ1（2026-10-29 19:31:51Z 建立）：「The serial numbers of TWCA-issued CA certificates follow a fixed structure in which at most 24 bits appear to be random」；BZ2 是 subscriber 憑證，TWCA 回覆「Both incidents involve insufficient serial number entropy」並併入 BZ1。MODA：「TWCA所核發的部分憑證」。「部分憑證」兩邊都對。 | |
| R2 | 索引收費、點名五家 AI 公司、「Brave has never asked…」出自三家報紙的訴狀；hl-brave-claims 與 wp-complaint 的 source | m29b；q8s1；hl-brave-claims.source；wp-complaint.source | V1 | 200 | CONFIRMED。V1：「According to a complaint filed by the New York Daily News, the Chicago Tribune, and the Orlando Sentinel, Brave Software has monetized its index…」；「Update, November 2nd: Clarified that one lawsuit was filed by New York Daily News, the Chicago Tribune, and the Orlando Sentinel」；引句接著寫「…,” the complaint says」，就在同一段。 | |
| R3 | 「Anthropic 說」：50 萬–100 萬 token，TTFT 中位數少約 35% | tq4k；hl-threads-num | CL | 200 | CONFIRMED（「With message threads on by default for most Claude Code users, requests with 500k to 1M tokens see median TTFT drop by about 35%」，是 Anthropic 自己的數據） | |
| R4 | Google Cloud 外掛公告日期 11/3；lg3m 不說「昨天」；hl-agy kicker「Google Cloud blog」；兩張卡 Nov 3 | lg3m；hl-agy；hl-agy-what.source；hl-agy-install.caption | GCB | 200 | CONFIRMED（頁面「November 3, 2026」、`"datePublished":"2026-11-03"`；安裝指令逐字「agy plugin install google-cloud-developer」）。lg3m 本輪另外縮句，見〈三〉。 | 見〈三〉 |
| R5 | 「The Verge 報導說，大約夠七十萬戶人家開冷氣」 | pb84 | V2 | 200 | CONFIRMED（「the company promises to free up to 1,000 megawatts of power during extreme weather or emergencies, enough to power air conditioners in around 700,000 homes」） | |
| R6 | sd-inbox kicker「Early November」、key「A new certificate arrives」 | sd-inbox | MODA | 200 | CONFIRMED（新聞稿只寫 11/1 完成重製、「透過主動補發機制，由系統直接以電子郵件將新憑證檔寄送予原申請機關承辦人」，沒有寄信日期） | |
| R7 | sd-timeline 第三列「Then」、表名「From report to deadline」 | sd-timeline | MODA | 200 | CONFIRMED（五列 10/30、11/1、Then、11/2 晚間 926、11/6 都對得上新聞稿） | |
| R8 | Tether 凍結：Chainalysis 說九百多萬；Tether 執行長說 450 萬 USDT 以上；ms-freeze note | zkf5；ms-freeze.stats[1] | CH、DC1 | 200 | CONFIRMED。CH：「enabling Tether to take action and freeze over $9 million in stolen funds」；DC1：「Tether CEO Paolo Ardoino said the stablecoin issuer froze more than 4.5 million USDT tied to the incident」。zkf5 本輪縮句，見〈三〉。 | 見〈三〉 |
| R9 | Trajectory「會不會更快、更便宜，報導裡只有公司這邊的說法，沒有第三方評估」 | h79x | TC3 | 200 | CONFIRMED（「With Trajectory, lawyers, doctors, and other specialists can improve the models near automatically themselves, Malde said. That capability could make deploying specialized AI faster and cheaper.」報導裡沒有任何第三方評估） | |
| R10 | Try This 第二步「不要跳過警告，更不要在那種頁面輸入密碼、身分證字號」 | bdwl；tt-steps | MODA | 200 | CONFIRMED（節目建議，ovsd 已說明不是數發部指示；新聞稿沒有給民眾的操作指引，沒有衝突；不會叫人點過警告） | |
| R11 | 說明欄補上 Trajectory 文章，共 13 篇 | youtube.description | S-* | 200 | CONFIRMED（13 個網址都是今天 200、已發布的站上文章） | |
| R12 | ss4z「那如果公司的網站，憑證也是 TWCA 發的呢？」 | ss4z | MODA | 200 | CONFIRMED（MODA「籲請各機關及其他TWCA憑證的使用者」；不再替 Kai 編公司） | |

## 二、全片重看（第 1 輪標 CONFIRMED 的項目）

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10/30 Bugzilla 通報、數發部同一天接獲；序號亂數未達 64 bits；設計 128 bits、首尾各 12 bits、實際 24 bits | ef3u、iiqo、gtvb、hbcd、dik4、l0zw、3qyc、23j0、li4w；co-*、sd-serial、sd-bits、sd-lock、sd-found | MODA、BZ1 | 200 | CONFIRMED（逐字：「國際社群Bugzilla於10月30日通報」「64 bits 以上密碼學安全亂數要求」「設計為128 bits，但實際僅首尾各 12 bits 為有效隨機數、中間皆填補為定值，實際隨機亂數僅 24 bits」「於10月30日接獲通報」） | |
| 2 | TWCA 序號「看起來是標準的兩倍長」 | ic4d | MODA、BZ1 | 200 | CHANGED。標準（MODA「64 bits 以上密碼學安全亂數」；BZ1 引 BR 7.1「at least 64 bits of output from a CSPRNG」）規定的是序號裡的亂數位元，不是序號長度，所以 128 不是「標準的兩倍長」。改成只說長度、不跟標準比長度，後面 dik4、l0zw 照舊揭曉。 | 「TWCA 的序號，設計成 128 位元，看起來是標準的兩倍長。」→「TWCA 的序號，總長設計成 128 位元，光看長度，比 64 還多。」；claims.md c36 加註 |
| 3 | 962 個機關、9,772 張；兩日內產製；11/1 完成重製；主動補發寄承辦人；資訊主管聯繫；11/2 晚間 926 張；11/6 前；可能出現安全性警示；目前未造成具體資安危害；數發部持續追蹤 | k6z8、kr7t、vtyu、6be6、eu50、x50d、nwek、d76o、hwxm、dnyh 等 | MODA | 200 | CONFIRMED（新聞稿原文逐句對過） | |
| 4 | 數發部「已經委託獨立的第三方，對它做深入檢測」 | fbk7 | MODA | 200 | CHANGED。MODA：「數發部已委託獨立第三方專業機構，後續針對TWCA進行深入檢測，全面檢視相關憑證產製及管理機制，並將依檢測結果要求TWCA改善」。委託已經做了，檢測是「後續」才做；原句「對它做深入檢測」聽起來像正在做或做完了。sd-who 卡片「TWCA: third-party audit」「TWCA gets audited」沒有說時態，不改。 | 「再來是 TWCA。數發部已經委託獨立的第三方，對它做深入檢測。」→「再來是 TWCA。數發部已委託獨立的第三方，接下來要對它深入檢測。」；claims.md c40 加註 |
| 5 | 違約調查、依約罰款求償；採購提供各機關；也提供民間；民間數字與機關名單沒公布 | n7o2、iopm、k4s2、ds3a、lvsq、ebou | MODA | 200 | CONFIRMED | |
| 6 | 換算：9,772÷962≈10.2；2²⁴＝16,777,216；2⁴⁰≈1.1 兆；926÷9,772≈9.48%；8,846÷4≈2,212 | icuv、y0sv、np4m、gr9q、rcyb、dtn9 | 算術 | — | CONFIRMED（重新計算） | |
| 7 | 標題「Taiwan gov certificates must be renewed by Nov 6」 | youtube.title | MODA | 200 | CHANGED。MODA 是「籲請各機關及其他TWCA憑證的使用者，盡速於11月6日前完成憑證更新作業」，是呼籲不是強制；must 說過頭。 | →「Tech Signal 11/3｜Taiwan urges agencies to renew certificates by Nov 6」（69 字，YouTube 上限 100，lint 沒有標題警告）；claims.md c3 加註 |
| 8 | ChatGPT 合併 Chat 與 Work；寄信；檔案外掛；Codex 獨立；同一 token 額度池；多數不受影響；可能更常等重置；先給部分人；Anthropic 九月合併 | nzz5–m0j4、kpvy | TC1 | 200 | CONFIRMED（「according to an email sent to users」「select users for feedback」「Codex will remain a separate experience in the ChatGPT desktop app」「draw tokens from the same allowance pool」「Rival Anthropic merged Claude's chat and Cowork functions into one screen in September」） | kpvy 縮句，見〈三〉 |
| 9 | Brave：點名 Anthropic、Perplexity、Mistral、xAI、Cohere；付費牆阻擋功能；NYT 發言人；Perplexity 首席傳播長；Brave 未立即回應 | rlmd、v9cr、5hvj、fdd7、80c1、257x、x29q | V1 | 200 | CONFIRMED（引句逐字；「Brave, Anthropic, Mistral, SpaceXSI, and Cohere didn't immediately reply」） | |
| 10 | Genie 4：10/27；打字生場景、有聲音；鍵盤移動與鏡頭；改天氣加人物；受信任測試者；Ultra 訂閱者與早期合作夥伴；細節漂移；SynthID；G10 11/2 再提 | taej、1ixa–wbhp | DM、G10 | 200 | CONFIRMED（DM「October 27, 2026」「standard keyboard controls for navigation and camera control」「changing the weather … introducing a new person or object」「visual details and object permanence can still shift or drift over time」「all video and audio generated by Genie 4 will include SynthID」；G10 published_time 2026-11-02，「alongside our new world model Genie 4」「our new SynthID Detector」） | taej 縮句，見〈三〉 |
| 11 | 訊息串：11/2 公開測試版；只送新訊息；token 用量不變、標準費率；閒置 5 分鐘過期；記憶體加密不寫磁碟；最晚 1 小時刪除 | iuqx、r7p9–1pe4 | CL、RN | 200 | CONFIRMED（CL「November 2, 2026」「public beta」「token usage stays the same」「Standard Claude token rates and existing rate limits apply」「encrypted and not written to disk」；RN「deleted no more than 1 hour after its last use」） | iuqx 縮句，見〈三〉 |
| 12 | 外掛三項：官方文件、啟用收費 API 或改基礎設施前問你、最小權限；文件伺服器預先授權、不用設 API 金鑰 | hiuy、ubrh、fr7o、14xe | GCB | 200 | CONFIRMED（「requires your consent before it enables billable APIs or modifying cloud infrastructure」「least-privilege IAM」「pre-authorized by default. You don't need to configure API keys」） | |
| 13 | 喬治亞州 Effingham County 試辦；反對聲浪；猶他 Box Elder County 超過 2025 年全州尖峰兩倍；田納西、佛羅里達等州立法；compute campuses；引句 | d7ja–pfbg、r5yp、l2mc、97qy | V2 | 200 | CONFIRMED（引句逐字） | |
| 14 | Mercado Bitcoin：巴西最大；11/2 凌晨；存提款暫停引句；沒給恢復日期；客戶無損失；Chainalysis 約 4,900 萬、17 條鏈、協助凍結近 1,000 萬；Hypernative 4,000 萬以上未確認；凍結不等於歸還 | j8my–xv6u | DC1、CH | 200 | CONFIRMED | |
| 15 | Squarespace 約 19%、約 300 人；16 週基本薪資、醫療到 2027 年 5 月；簡化營運、聚焦優先；AI 工具大幅改變產業 | rdwc–nbtr | TC2、V3 | 200 | CONFIRMED（「approximately 19%, representing around 300 employees」「16 weeks of base pay and healthcare benefits into May 2027」「have largely upended the industry」） | |
| 16 | Trajectory 4,500 萬美元 A 輪、紅杉領投、輝達參與；律師醫師幾乎自己調好模型 | 6m6k、9tno、v5cm | TC3 | 200 | CONFIRMED（「raised $45 million in a Series A round … led by Sequoia, with participation from Nvidia」） | 6m6k 縮句，見〈三〉 |
| 17 | Proton：八月員工要幾天滲透測試（per 404 Media）；失敗者思維引句；2,020 票；憤怒不是查證的退訂數；10/30 取消重新面談；技術長宣言引句 | tewn–vj4e | DC2 | 200 | CONFIRMED（「A Proton employee asked the company in August for a few days to pentest new code … per 404 Media」「had 2,020 votes when reviewed」「Yen canceled the re-interviews on October 30」「Your job is to help the LLM write better code faster.」） | |
| 18 | 縮圖「Renew **certs**」「9,772 Taiwan gov certificates, Nov 6」 | thumbnail | MODA | 200 | CONFIRMED（祈使句是節目的呼籲，數字與日期對） | |

## 三、縮短的句子（不改事實，id 與講者不變，沒有刪句，reveal 與 keys 數不變）

| id | 修改前（字數） | 修改後（字數） |
| --- | --- | --- |
| taej | Google DeepMind 在 10 月 27 日，發表了世界模型 Genie 4，昨天的十月整理又提了一次。（57） | DeepMind 10 月 27 日發表了世界模型 Genie 4，昨天 Google 的十月整理又提到。（53）；「Google DeepMind」全名在 hl-genie 卡片 kicker；順便講清楚十月整理是 Google 的（G10 在 blog.google，不是 DeepMind） |
| kpvy | TechCrunch 也提到，Anthropic 九月就把 Claude 的聊天和 Cowork 放在同一個畫面。（57） | TechCrunch 也提到，Claude 九月就把聊天和 Cowork 放在同一個畫面了。（46）；「Anthropic」在卡片 kicker「Meanwhile at Anthropic」 |
| 6m6k | 據 TechCrunch 報導，AI 新創 Trajectory 募到四千五百萬美元，紅杉資本領投，輝達也參與。（56） | 據 TechCrunch，AI 新創 Trajectory 募到四千五百萬美元，紅杉領投、輝達參與。（50） |
| lg3m | 同樣給寫程式的 AI，Google Cloud 在 Antigravity 的外掛市集，上架了一個官方外掛。（54） | 同樣給寫程式的 AI：Google Cloud 在 Antigravity 外掛市集上架了官方外掛。（50） |
| zkf5 | 它說其中九百多萬是 Tether 凍結的 USDT；Tether 執行長自己說的是四百五十萬以上。（49） | 它說其中九百多萬是 Tether 凍結的 USDT；Tether 執行長自己說四百五十萬以上。（47）；兩個數字與各自掛名都留著 |
| iuqx | Anthropic 昨天推出訊息串的公開測試版，給用 Claude 做 AI 代理的開發者。（46） | Anthropic 昨天推出訊息串公開測試版，給用 Claude 做 AI 代理的開發者。（45） |

字數照 `[...text].length` 計，空格與拉丁字母逐字算；taej、6m6k、lg3m 剩下的長度大多是英文專有名詞與數字兩旁的空格，唸起來比字數短。ic4d（31→35）、fbk7（31→33）因事實修改變長，都在 40 字以內。沒有改 slide 的狀態數，lint 沒有新的停留時間警告。

## 摘要

- 查了 30 條：第 1 輪改過的 11 處加 ss4z（R1–R12），以及全片重看的 18 條。CONFIRMED 27 條，CHANGED 3 條，NOT FOUND 0 條。
- 事實改動 3 處（都是第 1 輪標了沒改、協調者點名的）：(1) youtube.title「must be renewed」→「Taiwan urges agencies to renew certificates by Nov 6」（數發部是籲請）；(2) ic4d 不再說 128 位元是「標準的兩倍長」（標準規定的是 64 bits 亂數，不是長度）；(3) fbk7 不再說檢測已在做（數發部已委託，檢測是後續）。claims.md c3、c36、c40 跟著加註。
- 第 1 輪的 11 處事實修改與 ss4z：全部對照今天的官方頁確認是對的，沒有退回任何一處。
- 縮句 6 句（見〈三〉），都不改事實；超過 45 字的句子從 7 句降到 5 句（taej 53、6m6k 50、lg3m 50、zkf5 47、kpvy 46），超過 40 字的仍有 11 句（另有 j8my 46、iuqx 45、s2w2 45、am2z 44、nf8a 43、rdwc 42，沒動）。
- `sources` 14 個網址 2026-11-03 全部 HTTP 200，`checked_on` 已是 2026-11-03，不用改。
- 會過期的事實：TWCA 更新進度（926 張，MODA 11/2 晚間）、11/6 期限是否延長、第三方檢測與罰款（MODA 2026-11-02）；BZ1 TWCA 的完整事件報告還沒交；Brave 訴訟與 Brave 回應（V1 11/2 已更新一次）；Mercado Bitcoin 恢復日期與金額（DC1 11/2）；ChatGPT 合併分頁、Genie 4 開放對象、訊息串測試版狀態。影片晚於 11/6 上架時，「這個星期五」與「期限前」都要重看。
- 觀點：fsiy、b8py、d3a6 標成觀點，與 brief.md〈站主觀點〉一致；沒有不一致。
- 聽眾檢查（只報告）：沒有「經查證」「根據官方文件」「本影片」，沒有括號或網址，揭曉都在介紹句之後；本輪沒有加進新的拉丁詞（kpvy、taej 少唸了 Anthropic、Google）。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261103` → `daily-ai-20261103: 0 errors, 7 warnings`（Headlines 開頭是標籤，與重複數字「10」「11」「九百」「64」「24」「九千」，都是撰稿時就有的寫作警告；「64」從 3 句變 4 句，多的是改過的 ic4d，它在 sd-bits 回頭對照剛剛 gtvb 講的標準，是有意的回呼；警告數不變；估計 23.4 分鐘，307 句）。
- 懷疑但沒改：
  - rlmd「訴狀點名五家」：V1 寫的是「"many" AI companies including Anthropic, Perplexity, Mistral, xAI, and Cohere」，訴狀可能點名不只五家；影片的五家都在報導上，卡片 key「Five AI companies named」沒說只有五家，沒改。站主若要更嚴謹可改「點名的包括」。
  - BZ1 描述的是 TWCA CA 憑證的序號結構（亂數在尾端），和 MODA 說的「首尾各 12 bits」不同；政府那 9,772 張的結構只有 MODA 有說，影片照 MODA，與第 1 輪的判斷相同。
  - 站上文章 S-BRAVE 仍寫訴訟「由經營…的公司」提出，與 V1 的更新不同（第 1 輪已報告，不在本輪可改的範圍）。
  - mrgu「要在這個星期五前換新」與 intro-kai、outro 卡片「Renew by Nov 6」用的是節目的呼籲語氣；新聞稿是籲請，但期限是數發部給的，沒改。
- 需要第三輪：否。本輪改了 3 個事實（不超過 3 個）。在第二輪範圍內，這份稿子已經查核完成。
