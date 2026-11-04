# daily-ai-20261104 查核第 2 輪

查核日 2026-11-03。這是第二位查核代理，不是撰稿人，也不是第 1 輪的查核代理。
第 1 輪改了 4 個事實（超過 3 個），所以照 `verifier-video.md` 再查一輪。本輪做了四件事：

1. 重查第 1 輪改過的每一行與卡片。
2. 用新的眼光把整份稿子再看一遍，範圍超過「已確認項目隨機抽三分之一」的要求：每一行旁白與每張卡片都抽出來，對照今天重新打開的原文。
3. 處理協調者點名、第 1 輪留下沒解決的三件事：峰值在哪一季、sd-loss-why 的 kicker、oclb 的「Decrypt 先前報導」。
4. 確認第 1 輪的標示改動：三句「我們的建議」。

今天重新打開的頁面有三類，全部用 `Mokaair-editorial/1.0` UA、間隔 1.2 秒：

- 站上 16 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`）：全部 HTTP 200。
- `video.json` `sources` 的 17 個原始來源：全部 HTTP 200，沒有轉址。
- DC4：DC2 裡「reported on Monday」連到的 Decrypt 週一報導，HTTP 200。

本輪沒有用網路搜尋。來源代號沿用 `verify-1.md`，新增一個：

| 代號 | URL（頁面上的日期） |
| --- | --- |
| DC4 | https://decrypt.co/382355/north-korea-laundering-binance-hack-loot-new-wallet-every-25-seconds （datePublished 2026-11-02T18:46:03，週一） |

## 一、協調者點名的三件事

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| Q1 | 每 1 美元算力帶回的營收：從 2025 年初一路往上，高峰略高於兩倍，現在回到 1.72 倍；卡片「Just over 2× / now 1.72×」 | mex6、pcca；sd-ratio | TC1 | 200 | CONFIRMED。TC1 原文：「Since the start of 2025, it's been steadily growing, peaking at just over 2x this past quarter, then falling back down to 1.72x.」旁白與卡片都**沒有說高峰在哪一季**，也沒有說高峰之後過了多久才回落，沒有超出 TechCrunch 的說法。「現在回到」對應的是「falling back down to」，也就是最新的數字。站上文章 ANT 寫的是「上一季峰值」，比 TC1 多說了一點，但影片沒有用這個說法。 | |
| Q2 | 營運虧損擴大的原因：卡片 kicker | sd-loss-why.kicker | TC1 | 200 | CHANGED。TC1 原文是「the operating loss grew at the same time, thanks in large part to growing compute costs」，意思是「很大一部分是因為」，不是唯一或最主要的原因。旁白 c6qv 說「主因之一」是準的，卡片說「The main reason」比原文強。 | 「The main reason」→「In large part」 |
| Q3 | 「Decrypt 先前報導，其中大約二十八億五千萬，已被凍結或查扣」；卡片 note「earlier Decrypt report」 | oclb；ms-fbi.stats[1].note | DC2、DC4 | 200 | CONFIRMED。DC2（11/3）在「*Decrypt* reported on Monday」連到 DC4，下一句是「About $2.85 billion of the $6.43 billion stolen has been frozen or seized」。DC4 是 Decrypt 11/2 週一的報導，引用 Elliptic：「$2.85 billion of the $6.43 billion stolen from Binance has been frozen or seized」「About $2.85 billion, or 44% of the haul」。這個數字確實出自 Decrypt 較早的報導，所以「先前報導」是對的，旁白不改。claims.md c57 補上 DC4 的網址。 | 旁白不改；claims.md c57 補上出處 |

## 二、第 1 輪改過的地方（全部重查）

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Valve 後來發文承認審核落後，最多要十二個工作天；怪 AI，仍是開發者的猜測。卡片「Running behind / up to 12 business days」，key「Valve: up to 12 days now」（24 字元） | 4nba；nd-valve | V4 | 200 | CONFIRMED。V4：「In a new post from Valve published after we first ran this story … it's "running a little behind right now" and taking "up to 12 business days" for reviews, saying that much of the delay is "having to re-review games."」Valve 沒有把延誤歸因於 AI；開發者那邊是「Kamon and 2 Left Thumbs suspect…」。 | |
| R2 | 「據 The Verge，OpenAI 這週一說，ChatGPT 的搜尋量，已經是 Google 的五分之一。」 | iz00；hl-search kicker「OpenAI · via The Verge」 | V2 | 200 | CONFIRMED。V2：「the volume of search queries run through ChatGPT now equals 20 percent of the volume run through Google」，是 Adam Fry 週一在記者會上說的；「Fry did not specify the source of the Google search volume number」。 | |
| R3 | 「TechCrunch 也這樣說，更值得注意的，是 AI 伴侶 App。」 | 90kq | TC4 | 200 | CONFIRMED。TC4：「While most major dating services typically restrict their platform to adults…」對應 Kai 的「約會 App 本來就是成人用的吧」；「It's perhaps more interesting how this rule could impact AI companion apps」。用「更值得注意」，強度跟原文相當。 | |
| R4 | 「公司三十天內書面反對，平台就不能上架別人代做的代幣版。」 | fehm | DC3 | 200 | CONFIRMED。DC3：「a venue must notify a company before offering a version of its shares tokenized by an unaffiliated third party. If the company objects in writing within 30 days, the venue can't make that stock available for trading」；「A timely objection bars the venue from listing a third-party tokenized version of a stock, though the venue can still list shares that issuers tokenize themselves」。 | |
| R5 | ahuo「我們的建議：在 ChatGPT 查東西時，看清楚哪段是回答、哪段是廣告。」卡片 kicker「Our advice」 | ahuo；hl-search-tw | V2、SRCH | 200 | CONFIRMED。已標成節目建議，跟 V2「images of sponsored products and services」不衝突。 | |
| R6 | zt5n「還不行。報導沒說蘋果怎麼執行；我們建議，家長控制還是自己設。」 | zt5n | TC4 | 200 | CONFIRMED。TC4 確實沒寫蘋果怎麼執行；後半句已標成節目建議。 | |
| R7 | plgd「我們的建議：交易所出事的時候，看它有沒有給你自己能檢查的證明。」卡片 kicker「Our advice」 | plgd；ms-lesson | DC2 | 200 | CONFIRMED。已標成節目建議；依據是 DC2 寫幣安有零知識備付證明。 | |

## 三、全片重看（第 1 輪標 CONFIRMED 的項目）

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 月 4 日星期三 | 5yxg；intro | 曆法 | — | CONFIRMED | |
| 2 | 季度營收：前一季 115 億、這一季 170 億美元；快五成 | aqr1、t181、gnzv；sd-revenue | TC1 | 200 | CONFIRMED（「revenue reached $17 billion, up from $11.5 billion in the previous quarter」；+47.8%） | |
| 3 | 運算占營收：48%→58%；十個百分點；每 100 美元有 58 美元；縮圖「Compute 58%」 | 7nny、y11g、os5p、4fv9；sd-share、hl-number*、thumbnail | TC1 | 200 | CONFIRMED（「compute took up 58% of the company's revenue, up from 48% the quarter before」） | |
| 4 | 算力帳單 100 億美元，其中一半是短期合約，比多年合約貴得多；需求太快只好付高價 | tt6k、bmua、eu8k、bs8p；sd-bill、sd-short、sd-rush | TC1 | 200 | CONFIRMED（「$10 billion for the quarter」「$5.0 billion of compute under short-term commitments, which currently costs significantly more…」） | |
| 5 | SpaceX 每月 12.5 億美元；Nscale、Akamai、Volta 有數十億美元合約；neocloud，較彈性、費率較高；Anthropic Direct 跟不上 | kv8c、bthn、a2ft、xa1v、qojx、d0x8 | TC1 | 200 | CONFIRMED | |
| 6 | 支出還會增加、仍是最大營運支出；比較像短暫波動；債市或地方反對可能讓建設放慢；營收每季成長將近五成；沒有上市日期 | z6e4、f2xh、8qns、9reg、zcc6 | TC1 | 200 | CONFIRMED（「more of a blip than a long-term problem」「nearly 50% a quarter」「inches towards it IPO」） | |
| 7 | Brandom 的引句 | wp-tc.quote；368b | TC1 | 200 | CONFIRMED（逐字比對） | |
| 8 | 週一提交新文件、更新前一週的 S-1；舊版到 6/30，新版到 9/30 | n1w1、026w | TC1 | 200 | CONFIRMED | |
| 9 | AMD 資料中心 85 億美元、+97%；遊戲 −40%；五家公司在首批 Helios 上；沒有金額 | bh69、ybob、y4j8、lvm1、71n3 | AMDPR | 200 | CONFIRMED（「Data Center segment revenue was a record $8.5 billion, up 97%」「Gaming business revenue was $773 million, down 40%」；Helios 那句逐字對到） | |
| 10 | AMD 風險因素：出口管制、關稅、記憶體供應、第三方製造；沒有點名、沒有提到台灣 | 2oz0、e0hq、vqdu、d3b7；sd-risk | AMDPR | 200 | CONFIRMED（「export regulations」「import tariffs」「memory supply」「third party manufacturers」；全文沒有 Taiwan） | |
| 11 | Fal 募 13 億美元；據 Bloomberg 估值是四月的兩倍；這類公司毛利薄 | irzo、993g | TC2 | 200 | CONFIRMED | |
| 12 | 噴射引擎；IEA 估北維吉尼亞約七年；24 個月；效率低、污染多；微軟退出 Nscale 英國案，2030 年代初到中期才有電；Rystad 的引句 | 7yb2、zujv、egf8、41ju、vhse、gcwr | TC3 | 200 | CONFIRMED | |
| 13 | 只算觸發網路搜尋的問題；Bing 約 3%；廣告放產品圖片；Fry 的引句 | rzxg、cqwh、g62g、srca、we58、9fxy | V2 | 200 | CONFIRMED | |
| 14 | Google：Fake Call Detection、Pixel 詐騙警示、今年稍後擴大、600 萬美元、沒有列出機型與地區、Be Scam Ready 台灣已有 | 2tqk、a9go、j1c6、b0xe、3myb、wul6、9qnc | GB | 200 | CONFIRMED（見〈懷疑但沒改〉的 3myb） | |
| 15 | 蘋果 11/16 起補內容描述；AI 伴侶 App 下載 2.2 億次 | 0klx、4foc | TC4 | 200 | CONFIRMED | |
| 16 | FlashProve：Anthropic 說的換模型與竄改；開源原型；權重不公開；一張 H100 每秒約 110 token；1,024 token 約 19 MB；沒有部署計畫 | nnfb、9aan、lux8、t9dy、prva | AR、TC5 | 200 | CONFIRMED（AR「around 110 tokens/second」「~19 MB per 1,024-token request」；TC5「no plans to deploy it at Anthropic or any other lab」） | |
| 17 | Claude 浮水印：三個模型、只限所列平台、Sonnet 4.6 改了生成設定時可能不帶 | mktx、m7jx | RN | 200 | CONFIRMED（November 3, 2026 條目逐字比對） | |
| 18 | GitBook：11/2 晚上 7 點 CET（週一晚上）被攻擊；可能外洩的項目；API 權杖已失效、要求更換；內容沒有被改的證據；細節未說明 | 52k2、e7fb、1klv、d67c、etvc、5g0v、pngi、14fs、54rb | DC1 | 200 | CONFIRMED | |
| 19 | Netflix AI Discover：主題推薦、會記住不喜歡、美國英文支援電視逐步推出 | ypdj、h2mc、jv1a、jfmp | V3 | 200 | CONFIRMED | |
| 20 | OpenAI 改叫運算園區；Conner 的引句；OpenAI 沒回應 | dnrp、darw、xft7 | V1 | 200 | CONFIRMED | |
| 21 | 北韓否認（據 Decrypt 引述韓聯社）；金與正說「嚴重的政治挑釁」；FBI 上週六說超過 60 億；補足約 95%；前十大代幣、10/31 快照、零知識證明 | ihg8、wllv、hxx2、7wne、7nw3、x68d | DC2 | 200 | CONFIRMED | |
| 22 | OKX-ICE：合資、56 家、新增六家、還在計畫階段 | 4eoy、r5as、z8ye | DC3 | 200 | CONFIRMED | |
| 23 | 金管會申請對象：「銀行、金控、銀行轉投資的公司」 | lgku | FSCPR | 200 | CHANGED。新聞稿把對象分成三款：「(1)銀行、(2)金融控股公司或銀行轉投資之股份有限公司及(3)其他經金管會公告得申請許可之機構」。第 (2) 款是一項，指的是由金控或銀行轉投資的股份有限公司，不是把金控本身列為申請對象。原句把金控和轉投資公司並列成兩種對象。 | 「銀行、金控、銀行轉投資的公司，…」→「銀行、金控或銀行轉投資的公司，…」 |
| 24 | 金管會：實收資本 3 億；一比一；準備資產；身分確認；會計師查核；40 日；施行日期由行政院另定 | cg1t、edyq、lk0k、bgww、28m1 | FSCPR | 200 | CONFIRMED | |
| 25 | Steam：3–5 個工作天；Food Devils 10/12 送審、原定 11/3；Wheel Make It 晚了快兩週；7,240 款、+65.2%；49.9% | d4n5、9sru、5l7t、5y7k、nxdo；nd-wait、nd-numbers | V4 | 200 | CONFIRMED | |
| 26 | 說明欄 16 個站上網址 | youtube.description | 站上 16 篇 | 200 | CONFIRMED | |

## 摘要

- 查了 36 條：協調者點名 3 條（Q1–Q3）、第 1 輪改過的 7 處（R1–R7），以及全片重看 26 條。CONFIRMED 34 條，CHANGED 2 條，NOT FOUND 0 條。
- 事實改動 2 處：
  1. sd-loss-why 的卡片 kicker「The main reason」改成「In large part」。TC1 原文是「thanks in large part to」。
  2. lgku「銀行、金控、銀行轉投資的公司」改成「銀行、金控或銀行轉投資的公司」。金管會新聞稿第 (2) 款是金控或銀行轉投資的公司。
- claims.md 跟著改 c31、c65，c57 補上 DC4 的出處。
- 協調者點名的三件事：
  - Q1：影片沒有說峰值在哪一季，不必改。
  - Q2：已改。
  - Q3：28.5 億出自 Decrypt 11/2 週一的報導（DC4，引用 Elliptic），「先前報導」正確，不必改。
- 第 1 輪的 4 處事實修改與 3 處標示：全部對照今天的原文確認正確，沒有退回任何一處。
- `sources` 17 個網址 2026-11-03 全部 HTTP 200，`checked_on` 維持 2026-11-03。DC4 只寫進 claims.md，沒有加進 `sources`。
- 會過期的事實：
  - Valve「up to 12 business days」（V4，11/3 更新）。
  - 幣安補足約 95%，週三（11/4）會拍更大的快照（DC2 11/3）；凍結 28.5 億（DC4 11/2）。
  - OKX-ICE 56 家（11/2 通知）。
  - 金管會「近日內預告」與 40 日意見期（FSCPR 11/3）。
  - Anthropic S-1 可能再更新。
  - Pixel 詐騙偵測的擴大是「later this year」。
- 觀點：7qsr、d9ls、so1l、kzi0、z02r 都已標成觀點，跟 brief.md〈站主觀點〉一致，沒有不一致的地方。
- 聽眾檢查（只報告）：
  - 本輪改的 lgku 是 28 字。沒有「經查證」「根據官方文件」「本影片」，沒有括號或網址，也沒有新的拉丁詞。
  - 超過 40 字的句子跟第 1 輪報告的一樣，沒有動。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261104` → `0 errors, 3 warnings`。三條警告是開場濃縮兩條，加上 Headlines 開頭是標籤，撰稿時就有。估計 21.4 分鐘，268 句。沒有改任何 key 或 slide 的狀態數。
- 懷疑但沒改：
  - 3myb、hl-scam-what「$6M for scam education」：GB 說這筆錢除了社區培訓，還用在孵化 AI 防禦原型、提供資料給政策制定者，「防詐教育」是窄一點的概括。原文標題寫的是「community training」，不算錯，沒改。
  - hl-apple 卡片「AI companion apps: rated 18+」：規則針對的是有約會或浪漫關係功能的 App，不是所有 AI 伴侶 App。TC4 標題也是這樣寫，旁白 z2ua 講得精確，沒改。
  - t9dy「一千多個 token 的回答」：AR 說的是「per 1,024-token request」，是請求不是回答，差別不大，沒改。
  - 站上文章 ANT 的「上一季峰值」與 STM 的「Valve 未立即回覆」都比 TC1 或 V4 現在的寫法舊或強，不在本輪可改的範圍，第 1 輪已報告。
- 需要第三輪：否。本輪改了 2 個事實（不超過 3 個）。在第二輪的範圍內，這份稿子已經查核完成。
