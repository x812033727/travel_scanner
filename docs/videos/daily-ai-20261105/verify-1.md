# daily-ai-20261105 查核第 1 輪

查核日 2026-11-04。查核代理不是撰稿人。每一條旁白（`text`，Sola 與 Kai 兩位都查；本片沒有 `say`）、每張卡片的 `data`（含 `source`、`note`、`keys`）、縮圖、`youtube.title`、`description`、`tags` 都抽出來逐條對照（清單在 `_tools/claims_raw.txt`）：
站上 14 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，1.2 秒一篇，全部 HTTP 200、`status: published`、news_date 2026-11-04），`video.json` `sources` 的 13 個原始來源，加上 `sources` 漏列的 Decrypt Coinbase 一篇，2026-11-04 全部用 `Mokaair-editorial/1.0` UA 以 curl 重新打開。
撰稿人只用了站上文章的轉述；這一輪每個數字、引句都對回原文。站上文章 CRCL 有一句原文沒有的說法（「最大收入來源、因利率下降」），另外對 Circle 在 SEC 的第三季財報 8-K 查證（web search 1 次）。

## 來源代號

站上文章（全部 200，published，news_date 2026-11-04）：

| 代號 | slug |
| --- | --- |
| MID | ai-news-data-center-midterms-20261104 |
| VOT | ai-news-us-voters-data-center-restrictions-20261104 |
| QCOM | ai-news-qualcomm-data-center-20261104 |
| GIF | ai-news-chatgpt-animated-gifs-images-26-20261104 |
| SIRI | ai-news-apple-siri-recaps-watch-beta-20261104 |
| COND | ai-news-meta-acquires-conductor-20261104 |
| DDG | ai-news-duckduckgo-schools-google-ai-policy-20261104 |
| OAI | ai-news-openai-2028-election-20261104 |
| UBER | ai-news-uber-ai-agents-rides-20261104 |
| OCC | ai-news-occ-bank-ai-framework-20261104 |
| MS | crypto-news-morgan-stanley-dtcc-tokenization-20261104 |
| CRCL | crypto-news-circle-workforce-cut-20261104 |
| CB | crypto-news-coinbase-cold-storage-binance-hack-20261104 |
| RAM | ai-news-altman-ram-comments-20261104 |

原始來源（2026-11-04 重開，全部 HTTP 200，沒有轉址）：

| 代號 | URL（頁面上的日期） |
| --- | --- |
| V1 | https://www.theverge.com/policy/1026365/data-centers-midterms-results （Lauren Feiner，2026-11-04T16:05Z） |
| DC1 | https://decrypt.co/382556/us-voters-back-ai-data-center-restrictions （Jose Antonio Lanz，2026-11-04T18:46） |
| V2 | https://www.theverge.com/ai-artificial-intelligence/1026867/qualcomm-earnings-data-centers （2026-11-04T22:42Z） |
| V3 | https://www.theverge.com/ai-artificial-intelligence/1026474/openai-chatgpt-animated-gifs-images-2-6 （2026-11-04T18:00Z） |
| TC1 | https://techcrunch.com/2026/11/04/i-tried-apples-siri-recaps-theyre-surprisingly-useful-and-a-little-unsettling/ （Sarah Perez，8:51 AM PST, November 4, 2026） |
| TC2 | https://techcrunch.com/2026/11/04/meta-acquires-ai-coding-startup-conductor/ （Lucas Ropek，1:10 PM PST, November 4, 2026） |
| TC3 | https://techcrunch.com/2026/11/04/duckduckgo-pitches-itself-to-schools-amid-backlash-over-googles-ai-policy/ （2026-11-04T19:29Z） |
| TC4 | https://techcrunch.com/2026/11/04/openai-is-already-trying-to-shape-the-2028-election/ （Rebecca Bellan，2026-11-04T21:25Z） |
| V4 | https://www.theverge.com/transportation/1026306/uber-ai-agents-q3-earnings-disintermediation （Andrew J. Hawkins，2026-11-04T15:58Z） |
| DC2 | https://decrypt.co/382560/us-bank-regulator-issues-first-ai-framework-banks-battle-rogue-agents （2026-11-04T19:57） |
| DC3 | https://decrypt.co/382513/wall-streets-plumbing-onchain-morgan-stanley-tokenizes-securities （2026-11-04T16:29） |
| DC4 | https://decrypt.co/382493/usdc-issuer-circle-quietly-cuts-5-of-staff-in-profitable-quarter （2026-11-04T12:44） |
| DC5 | https://decrypt.co/382570/coinbase-99-percent-customer-crypto-offline-binance-hack （2026-11-04T20:46；**原本不在 `sources`，本輪補上**） |
| 8K | https://www.sec.gov/Archives/edgar/data/0001876042/000187604226000309/finalq3epr-110326.htm （Circle 第三季財報 8-K；**本輪補進 `sources`**） |
| V5 | https://www.theverge.com/ai-artificial-intelligence/1026292/sam-altman-ram-shortage-pcs-comments （Stevie Bonifield，2026-11-04T14:46Z） |

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 今天是 11 月 5 日星期四 | k8gk；intro | 曆法 | — | CONFIRMED（2026-11-05 是星期四） | |
| 2 | 主題：美國期中選舉裡的 AI 資料中心 | 32a2；intro-kai | V1、DC1 | 200 | CONFIRMED | |
| 3 | 昨天 11 月 4 日的科技新聞 | cvea；hl-open | 站上 14 篇 | 200 | CONFIRMED（news_date 皆 2026-11-04） | |
| 4 | 據 The Verge，ChatGPT 能做 GIF；文字或照片；可調速度、逐格改、分享 | czez、p33d、2cd0、y8lz；hl-gif、hl-gif-how | V3 | 200 | CONFIRMED（「using a prompt or a photo」「adjust the GIF's animation speed, edit individual frames, and share it」） | |
| 5 | 隨新圖像模型推出；開放給所有 ChatGPT 和 Codex 使用者（web、desktop、mobile） | wg8u；hl-gif-who | V3 | 200 | CONFIRMED（「Images 2.6 is rolling out to all ChatGPT and Codex users across web, desktop, and mobile apps」） | |
| 6 | OpenAI 說每週超過 40 億張圖，九月 30 億 | tww7；hl-gif-who | V3 | 200 | CONFIRMED（公司自述，旁白「OpenAI 也說」；across ChatGPT and its API） | |
| 7 | 報導沒提長度、解析度、檔案大小 | hobm；hl-gif-limit | V3 | 200 | CONFIRMED（全文沒有） | |
| 8 | 據 TechCrunch，蘋果週二在開發者測試版測 Apple Watch 音訊 AI 功能 | 7spw；hl-siri | TC1 | 200 | CONFIRMED（「On Tuesday … first developer beta versions of iOS 27.3 and watchOS 27.3」；旁白沒唸版本號） | |
| 9 | 四項：重要聲音（門鈴、警報）、辨識歌曲、Live Rewind 過去 15 秒、Siri Recaps 一整天摘要存成筆記；後兩項會錄音 | uv3k、ydfk、6lr8；hl-siri-what | TC1 | 200 | CONFIRMED | |
| 10 | 作者試了一天；送修車時店員講很快，記下自付額和維修時程 | sa4f；hl-siri-good | TC1 | 200 | CONFIRMED（「After just a day」「the deductible, the repair time frame」） | |
| 11 | 也記下閒聊；談話更私人會覺得被侵犯 | nwlu；hl-siri-bad | TC1 | 200 | CONFIRMED（「could feel invasive … if the subject being discussed was more personal」） | |
| 12 | 設成隨時運作就一直在聽；盡量裝置上處理、不辨認說話者、不存原始錄音 | siria、h8e0；hl-siri-privacy | TC1 | 200 | CONFIRMED（「Because I configured Siri Recaps to run at all times」；「on-device, when possible … not identifying speakers, storing raw audio files」） | |
| 13 | 有人反感科技隨時在聽變常態 | ra54；hl-siri-norm | TC1 | 200 | CONFIRMED | |
| 14 | 只在開發者測試版、Apple Watch Series 12；正式時間沒說 | hh4z；hl-siri-when | TC1 | 200 | CONFIRMED | |
| 15 | 據 TechCrunch，Meta 收購 Conductor；多個代理在獨立工作區分工 | 56da、ajeb；hl-meta、hl-meta-what | TC2 | 200 | CONFIRMED（「deploying multiple agents into parallel workspaces」） | |
| 16 | 代理來自 Anthropic、OpenAI 等大實驗室 | 1qd0；hl-meta-src | TC2 | 200 | CONFIRMED | |
| 17 | 創辦人說雲端 11/20 關閉後開始刪雲端資料；核心功能到明年初照常 | 4jol、f3o4、sope；hl-meta-date、tt-export-why | TC2 | 200 | CONFIRMED（Holtz：「cloud service, which will shut down on November 20, after which the company will begin deleting user cloud data」；「until early next year」→ 卡片 Early 2027 換算成立） | |
| 18 | Meta 確認收購，金額條件沒說 | ccjq；hl-meta-deal | TC2 | 200 | CONFIRMED | |
| 19 | 據 TechCrunch，Google 週二告訴學校 Gemini 可關，但關其他 AI 功能會失去搜尋 | 9s0f、wxj7；hl-school、hl-school-all | TC3 | 200 | CONFIRMED（kicker Nov 3＝週二） | |
| 20 | 搜尋有 AI 摘要與對話式 AI Mode | z66e；hl-school-why | TC3 | 200 | CONFIRMED | |
| 21 | Google 被批評後說 Gemini 和搜尋預設關閉，學校自選 | pt89；hl-school-reply | TC3 | 200 | CONFIRMED（Gemini、Gemini Notebook、Search OFF by default；Google 的說法，卡片 key「it says」） | |
| 22 | DuckDuckGo 執行長貼說明教學校換預設；自己的 AI 可關（它自己的說法） | 14z5、5u57；hl-school-ddg* | TC3 | 200 | CONFIRMED（Weinberg on X；「the company says」） | |
| 23 | Google 以前公布：約 5,000 萬台 Chromebook、Classroom 逾 1.5 億 | vt5z、eid1；hl-school-scale | TC3 | 200 | CONFIRMED（「According to figures Google has published in previous years」） | |
| 24 | 報導沒有分地區 | kzgt；hl-school-tw | TC3 | 200 | CONFIRMED | |
| 25 | 據 TechCrunch 報導，OpenAI 全球事務長發文說 2028 大選可能是 AI 關鍵時刻 | 4fhs；hl-oai | TC4 | 200 | CONFIRMED（有「據 TechCrunch 報導」，卡片 kicker「Reported · TechCrunch」、key「Reported:」） | |
| 26 | 發在民主黨期中選舉大勝之後 | uvh3；hl-oai-why | TC4 | 200 | CONFIRMED（「on the heels of a stunning Democratic victory in the midterm elections」） | |
| 27 | 比作 1930 年代新政；五個方向：勞工保護、教育、AI 安全、資料中心 | w6mf、3o19；hl-oai-what | TC4 | 200 | CONFIRMED（「five policy priorities, spanning worker protections and education to AI safety and data center development」） | |
| 28 | 據報導，他警告支持暫停的政治人物可能危及對中國的領先 | 0i9h；hl-oai-dc | TC4 | 200 | CONFIRMED | |
| 29 | OpenAI 發稿時沒回應 TechCrunch | v9p7；hl-oai-reply | TC4 | 200 | CONFIRMED（「it did not respond by the time of publication」） | |
| 30 | 訊號數字 4：Uber 昨天財報會議說第三季第三方 AI 代理只叫了 4 趟 | 5032、numa；hl-number、hl-number-what | V4 | 200 | CONFIRMED（「Only four rides were arranged by third-party AI agents during the third quarter of 2026 … earnings call this morning」，11/4） | |
| 31 | Uber Eats 萬聖節那一週約 500 筆；期間不同不能直接比 | cbj0；hl-number-eats | V4 | 200 | CONFIRMED（「"around 500" during the week of Halloween」；期間確實不同） | |
| 32 | 專家擔心去中介化；The Verge 認為風險還很小 | csbh、q4fg；hl-number-why、hl-number-small | V4 | 200 | CONFIRMED（「it seems like the risk is still very small」） | |
| 33 | Janesville 週二選票：前通用汽車廠址大型開發前要不要再投一次 | i2a5、vota；sd-scene、sd-scene-q | DC1 | 200 | CONFIRMED（「a requirement for another public vote before major development at a former General Motors site」；kicker Tuesday, Nov 3） | |
| 34 | 據 Decrypt，那塊地跟一座擬議中的資料中心有關；超過六成贊成 | 4dqz；sd-scene-dc | DC1 | 200 | CONFIRMED（「more than 60% approved … linked to a proposed data center」） | |
| 35 | 資料中心＝放晶片、伺服器的大樓，AI 在這裡算 | w24t；sd-def | DC1 | 200 | CONFIRMED（「house the chips and servers used to train and run AI systems」） | |
| 36 | Decrypt 引述華郵：週二至少 29 個地方的選民支持禁止或限制 | gslf、dum4；sd-many、sd-wrap | DC1 | 200 | CONFIRMED（「Voters in at least 29 U.S. jurisdictions backed bans or restrictions … according to The Washington Post」） | |
| 37 | 縮圖「Voted down」「Data centers, in 29+ US places」 | thumbnail | DC1 | 200 | CHANGED（29 處是「backed bans or restrictions」，有的只是要求再一次公眾表決、有的只是諮詢性；「voted down」說成資料中心被否決，違反 brief〈不做的事〉「不說被禁了」） | headline「Voted **down**」→「Voted **limits**」（「Voted to limit」三個拉丁詞，qa 會擋） |
| 38 | 用電推高電費、電網負擔；還有用水、噪音、協議缺公眾監督 | wggb、v4fe、g6az、4qk5；sd-why、sd-why-more | DC1 | 200 | CONFIRMED（「utility bills and grid capacity … water use, noise and deals struck without public scrutiny」） | |
| 39 | The Verge 引 NBC News 選舉日調查：76% 反對自己社區出現資料中心 | hkoq；sd-poll | V1 | 200 | CONFIRMED | |
| 40 | Ballotpedia：10 州 41 項，28 項投贊成即限制；另 13 項允許或支持 | nfom、dov8；sd-count、sd-flip | DC1 | 200 | CONFIRMED | |
| 41 | The Verge 引另一份整理：45 項地方公投，到週三早上 33 項會限制開發 | olgz；sd-count | V1 | 200 | CONFIRMED（Redbud Consulting） | |
| 42 | Hubbard 超過四分之三支持禁止；Wells 大型資料中心暫停 180 天；El Dorado 十年內禁超過 10 MW | atya、oq86、9snz；sd-examples | DC1、V1 | 200 | CONFIRMED（El Dorado 是「peak electrical load over 10MW for 10 years」） | |
| 43 | Joliet 近八成否決支持 AI 資料中心的諮詢提案 | 0xoa；sd-joliet | DC1 | 200 | CONFIRMED（原文 Joliet Township；卡片 kicker 寫對，旁白「Joliet」見懷疑但沒改） | |
| 44 | 有些只是諮詢性投票，通過也不會自動停工 | adva；sd-advisory | DC1 | 200 | CONFIRMED（「nonbinding advisory votes, meaning their passage does not automatically stop construction」） | |
| 45 | 德州民主黨候選人擊敗現任州長，主張暫停新資料中心；Decrypt 認為可能帶來更嚴格州級規範 | mrdo、y4hj、rd7c；sd-texas、sd-state | DC1、V1 | 200 | CONFIRMED（Hinojosa defeated Gov. Greg Abbott；「could bring tougher statewide rules」） | |
| 46 | The Verge：很難歸因；也有主張溫和限制的人勝選 | 5zz0；sd-careful | V1 | 200 | CONFIRMED | |
| 47 | The Verge：開發商要面對更難蓋的環境 | 8mfi；sd-money-q | V1 | 200 | CONFIRMED（「poised to face a more restrictive building environment」） | |
| 48 | 佛州共和黨當選人提案開發商自付能源用水；愛荷華當選人與對手同意停稅收優惠；賓州州長行政命令禁保密協議 | su43、e351、fcxn、m1tz；sd-terms | V1 | 200 | CONFIRMED（Donalds 的 Protecting Ratepayers Act；Sand 與 Lahn「both agreed on ending tax breaks」；Shapiro executive order） | |
| 49 | Decrypt：加強遊說、做公關；OpenAI 想改叫運算園區 | ifrg；sd-industry | DC1 | 200 | CONFIRMED（「compute campuses」） | |
| 50 | 高通把成長押在資料中心；手機銷量比 2025 少約兩成；2029 年 150 億美元；最後約三成；公司預測 | c25g、24fy、k5se、ncun；sd-qcom* | V2 | 200 | CONFIRMED（「$15 billion by 2029」「around 30 percent of its business」） | |
| 51 | 報導沒說選民會擋到高通 | mona；sd-qcom-link | V2 | 200 | CONFIRMED（原文沒有） | |
| 52 | 今天這幾篇都沒提到台灣 | twna；sd-taiwan | 全部原文 | 200 | CONFIRMED（14 篇原文都沒有 Taiwan／TSMC） | |
| 53 | The Verge：資料中心搶購全球記憶體造成短缺、漲價；很多人更難裝大量記憶體 | o8a8、28yk；sd-ram | V5 | 200 | CONFIRMED | |
| 54 | 英特爾預期至少到明年；SK 海力士說可能拖到 2030 | bbfv、yb2l；sd-ram-when | V5 | 200 | CONFIRMED（「Intel's expecting it to last through at least next year, and SK Hynix predicted it could drag on until 2030」；卡片 2027＝換算） | |
| 55 | 美國少蓋會不會改變供應，來源沒說 | omt0；sd-ram-unknown | V5 | 200 | CONFIRMED | |
| 56 | 接下來看三件事（約束力、州規定、誰付） | 9dal、9965、v8ir；sd-next | DC1、V1 | 200 | CONFIRMED（節目依來源整理） | |
| 57 | The Verge 說實際政策要看後續立法和執行，報導沒給時間表 | 2a7u；sd-timeline | V1、MID | 200 | CHANGED（V1 沒有這句；「實際政策仍取決於後續立法與執行」是站上文章 MID 自己的話。V1 只說當選人會持續面對壓力） | 「The Verge 說，實際政策要看後續的立法和執行，報導沒有給時間表。」→「實際政策，要看後續的立法和執行；The Verge 沒有給時間表。」 |
| 58 | TechCrunch：選民擔心電費、工作被取代，AI 會變成更大的議題 | yqj3；sd-2028-why | TC4 | 200 | CONFIRMED（「AI could become an increasingly large part of that conversation as voters stress about data centers hiking up electricity bills, AI replacing their jobs」） | |
| 59 | 三句都是原始報導裡的原話 | mg2t；wp-open | DC1、TC4、V4 | 200 | CONFIRMED | |
| 60 | Larry Fink 上個月："If we have a moratorium of some sort in this country, we will be in a recession." | lbw1、k97z；wp-fink | DC1 | 200 | CONFIRMED（逐字；「BlackRock CEO Larry Fink said last month」） | |
| 61 | Kate Brennan："…ahistorical at best and harmful at worst."；評 Lehane 文章；私人公司為自己利益倡議政策 | wvgr、sy2z、ymgf；wp-brennan、wp-brennan-why | TC4 | 200 | CONFIRMED（逐字：「This is written by a private company that is trying to advocate for policies for its own benefit. It is ahistorical at best and harmful at worst.」） | |
| 62 | Dara Khosrowshahi："It is just very, very early…"；不依賴任何單一業者 | syf4、8tfq；wp-uber | V4 | 200 | CONFIRMED（逐字：「It is just very, very early, and we want to make sure we are not dependent on any one player」） | |
| 63 | 據 Decrypt，OCC 昨天發布第一份銀行業 AI 監理框架；22 頁、寫給檢查人員 | jg1n、zrmc；ms-occ、ms-occ-who | DC2 | 200 | CONFIRMED（「issued its first supervisory framework for artificial intelligence in banking today」；「22-page framework」） | |
| 64 | 看出錯後果、能否撤回、人類控制權；不是看多強 | o5cu、w7us、oqrx；ms-occ-how | DC2 | 200 | CONFIRMED | |
| 65 | 最高風險：完全自主的付款代理、即時信用決策系統；簡單付款代理可能比只寫內部文件的先進模型風險高 | mt7a、ofxn；ms-occ-top、ms-occ-simple | DC2 | 200 | CONFIRMED（「Fully autonomous payment agents and real-time credit decision systems fall into the highest category」） | |
| 66 | 保護：斷路器、速率限制、縮小權限、緊急關閉 | x0l1、61wf、8vru；ms-occ-guard | DC2 | 200 | CONFIRMED | |
| 67 | Decrypt 引 Axios：未經授權第三方 AI 代理在客戶帳戶運作；摩根士丹利擋、摩根大通美銀花旗限制；OCC 沒直接連結 | yqdl、tvdn、5l7f；ms-occ-axios、ms-occ-banks | DC2 | 200 | CONFIRMED（Axios report on October 22） | |
| 68 | 不是新規定，用既有風險類別評估 | c2tl；ms-occ-rule | DC2 | 200 | CONFIRMED | |
| 69 | 據 Decrypt，摩根士丹利週二說透過 DTCC 新服務把美股與公債代幣化 | xk39、suq6；ms-ms | DC3 | 200 | CONFIRMED（「The bank said Tuesday」） | |
| 70 | DTC 負責成交後保管交割，託管逾 114 兆美元 | ftzx；ms-dtc | DC3 | 200 | CONFIRMED（「post-trade backbone … more than $114 trillion in assets under custody」） | |
| 71 | DTCC 說代幣權利與投資人保護相同，可換回 | jk7p；ms-twin | DC3 | 200 | CONFIRMED（「and back again」「according to DTCC」） | |
| 72 | 符合資格的金融機構用；20 家報名，含美銀、花旗、摩根大通；一般人目前不行 | lwdi；ms-who | DC3 | 200 | CONFIRMED（「eligible firms」「20 DTC participants」；散戶不能用是從「eligible firms」推得，見懷疑但沒改） | |
| 73 | Decrypt：銀行主導，跟加密業者的代幣化股票不同 | r6no；ms-contrast | DC3 | 200 | CONFIRMED（「The bank-led approach contrasts with crypto-native efforts」） | |
| 74 | 據 Decrypt，Circle 第三季財報揭露裁約 5% | t7ie；ms-circle | DC4、8K | 200 | CONFIRMED（8K：「a workforce reduction of approximately 5%」） | |
| 75 | 淨利比去年多 5%；最大收入來源（準備金利息）因利率下降少 8% | to9e、oaq5；ms-circle-why | DC4、8K | 200 | CONFIRMED（DC4 只有副標「reserve income fell 8%」，沒寫「最大」與「利率」；8K：「Reserve Income of $658 million decreased 8% year-over-year, primarily from a 61 bps decline in the Reserve Return Rate」，總營收與準備金收入 8.65 億中占 6.58 億＝最大來源） | 卡片 source「Decrypt, citing Circle, Nov 4, 2026」→「Circle Q3 release; Decrypt, Nov 4, 2026」（出處標示，不是事實改動）；`sources` 補 8K |
| 76 | 為了讓組織更符合營運模式和策略重點；沒說人數、團隊 | elrc；ms-circle-unknown | DC4、8K | 200 | CONFIRMED | |
| 77 | Decrypt 列出今年 Coinbase 5 月 14%、以太坊基金會 6 月 20%、Bitwise 8 月 14%；理由市場轉弱、AI 或兩者 | 7kus；ms-circle-wave | DC4 | 200 | CONFIRMED | |
| 78 | 據 Decrypt，Coinbase 昨天在部落格說，上週幣安遭駭沒影響到它 | 952e；ms-cb | DC5 | 200 | CONFIRMED（「In a blog post Wednesday … wasn't affected by last week's hack of Binance」） | `sources` 補 DC5 |
| 79 | 超過 99% 在冷儲存；私鑰切成好幾份、簽交易也不拼回；提領暴增先暫扣待審；是 Coinbase 自己的說法 | 4dbk、8w63、0eaj、dp9t；ms-cb-how、ms-cb-note | DC5 | 200 | CONFIRMED（公司自述已標：「這些都是 Coinbase 自己的說法，經 Decrypt 轉述」；卡片 title「Coinbase's own account」） | |
| 80 | 這段不談任何價格 | 7duu；ms-you；全片 | — | — | CONFIRMED（全片沒有價格、報酬、漲跌或買賣） | |
| 81 | Try This 三件都是節目建議；每句有「我們的建議／我們建議」，卡片 kicker「our advice」 | bcyl、8ijm、12sb、9nmu、2grf；tt-* | TC1、TC2、DC2 | 200 | CONFIRMED（與來源不衝突；Kai bxwm「作者想在晚上關掉」＝TC1「considering turning off the Recap feature while at home in the evening」） | |
| 82 | 據 The Verge，Altman 選舉夜在 X 上替記憶體說法辯護 | rjvu、6r21；nd-open、nd-what | V5 | 200 | CONFIRMED（「spent election night defending his position on PC RAM purchases」） | |
| 83 | 訪談節目裡說，大家把有限的記憶體放在自己電腦、只用 5% 的時間，相當糟糕 | 5ivw；nd-podcast | V5 | 200 | CONFIRMED（Cheeky Pint：「quite terrible … being used five percent of the time」） | |
| 84 | 說被斷章取義；回網友 "i want you to have so much ram lets build more." | ynxd；nd-clarify | V5 | 200 | CONFIRMED（逐字，含小寫與無撇號） | |
| 85 | 我的看法：今天最重要的是選舉裡的資料中心；我不確定會不會放慢 | 1bip、ctww、txb8；tk-* | brief.md | — | OUT OF SCOPE（觀點，見摘要） | |
| 86 | 完整整理在 Mokaair，連結在說明欄 | qftg；tk-site；description | MID、VOT | 200 | CONFIRMED（兩個網址 200、published） | |
| 87 | 片尾：電費、用水、噪音把雲端的 AI 帶到家門口 | qans；outro | DC1 | 200 | CONFIRMED | |
| 88 | 標題「Data centers on the ballot」；說明欄；tags | youtube.* | — | — | CONFIRMED／OUT OF SCOPE | |
| 89 | 串場與 Kai 的反應句（jd2t、7iv8、a35h、j9ct、yvbf、qckq、12ah、b8ht、z2uw、pdn6、d2yl、3wb1、9dp7、7m5u、g105、hpwf 等） | 各處 | — | — | OUT OF SCOPE（不含新事實；沒有編主持人的私人經驗） | |

## 摘要

- 查了 89 條（同一事實在多處出現時合為一條）：CONFIRMED 85、CHANGED 2、NOT FOUND 0、OUT OF SCOPE 2（#85、#89；#88 部分）。
- 事實改動 2 處：(1) 縮圖「Voted down」→「Voted limits」：29 處是支持禁止「或限制」，不是否決（thumbnail）；(2) 「實際政策要看後續立法和執行」不是 The Verge 說的，是站上文章的話，拿掉掛名（2a7u）。出處標示 1 處：Circle 卡片 source 加上 Circle 財報（「最大收入來源、因利率下降」原文 Decrypt 沒有，Circle 8-K 有）。`sources` 補 2 個：DC5（Coinbase，原本漏列）、8K。
- 指定重點全部對到原文：Janesville 前 GM 廠址、與擬議資料中心有關、超過 60% 贊成（DC1）；至少 29 個轄區（華郵，經 DC1）、Ballotpedia 10 州 41 項／28／13、Redbud 45 項中 33 項、NBC 76%；Uber 第三季 4 趟、Uber Eats 萬聖節那一週約 500 筆（期間不同，旁白有講）；Siri Recaps 在 iOS 27.3／watchOS 27.3 首個開發者測試版、Series 12；Conductor 雲端 11/20 關閉後刪資料、核心功能到明年初；OpenAI 2028 那則每處都有「據 TechCrunch 報導／據報導」，卡片「Reported」；DTCC／DTC 114 兆、20 家；Circle 約 5%（8-K 證實）；OCC 22 頁、自主付款代理最高風險；Coinbase 99% 冷儲存標為公司自述；Altman 5% 與 X 引句逐字；Fink、Brennan、Khosrowshahi 三句英文逐字；英特爾「至少到明年」、SK 海力士「可能到 2030」。
- 「據報導」：單一媒體的各則都有掛名（據 The Verge／TechCrunch／Decrypt、Decrypt 引述華郵與 Axios、The Verge 引述 NBC）。公司自述都有標：OpenAI 圖像量（「OpenAI 也說」）、高通（「公司自己的預測」）、Google（「Google 被批評之後說」）、DuckDuckGo（「它自己的說法」）、DTCC（「DTCC 說」）、Coinbase（dp9t）。
- 節目建議：Try This 三件都有「我們的建議／我們建議」，kicker「our advice」，tt-open source「Our advice」。
- 加密貨幣：全片沒有價格、報酬、漲跌或買賣；ms-you 明說不談價格。
- 唸出來的日期：週二 11/3（Janesville、29 處、蘋果測試、Google 告知學校、摩根士丹利）、昨天 11/4（Uber 財報會議、OCC、Coinbase 部落格、高通報導）、11/20（Conductor）、Axios 10/22，都與原文相符。
- `sources` 15 個網址 2026-11-04 全部 HTTP 200，`checked_on` 2026-11-04。
- 會過期的事實：Redbud 計票「截至週三早上」33/45（V1 2026-11-04）；29 個轄區（華郵，DC1 2026-11-04）；Siri Recaps 仍在 27.3 開發者測試版（TC1 2026-11-04）；Conductor 雲端 11/20 關閉、核心功能到明年初（TC2 2026-11-04）；Google 學校 AI 預設值（TC3 2026-11-04）；OCC 框架會隨技術更新（DC2 2026-11-04）；DTCC 2027 加入更多區塊鏈（DC3 2026-11-04）；記憶體短缺預測（V5 2026-11-04）。
- 觀點：1bip、ctww、txb8 以「我的看法是」「老實說，我不確定」標明，與 brief.md〈站主觀點〉一致（選舉裡的資料中心最重要、AI 有房子要用電、不確定會不會放慢、不說選舉因資料中心輸贏）。沒有不一致。
- 聽眾檢查（只報告）：超過 40 字的句子 19 句，最長 7kus 55、nfom 51、hkoq 50、4fhs 50、t7ie 49、7spw 49、yqdl 47。沒有「經查證」「根據官方文件」「本影片」、括號或網址；揭曉都在介紹句之後。本輪改的 2a7u 沒有新增拉丁詞以外的字（The Verge 已在字典中、全片多處在唸）。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261105` → `daily-ai-20261105: 0 errors, 2 warnings`（開場濃縮兩條，本節目格式沒有開場濃縮；估 21.5 分鐘，257 句）。縮圖改成「Voted to limit」時 lint 警告三個拉丁詞（qa 會擋），所以用兩個詞的「Voted limits」，警告消失。
- 懷疑但沒改：
  - **站上文章 CRCL**：寫「Decrypt 指出，準備金收入……是 Circle 最大的營收來源，本季因利率下降減少 8%，為 6.58 億美元」，Decrypt 原文沒有這些（只有副標「reserve income fell 8%」）；數字對（Circle 8-K），但歸給 Decrypt 不對。不在本輪可改的範圍。
  - **站上文章 MID**：「實際政策仍取決於後續立法與執行」緊接在 The Verge 的段落裡，讀起來像 The Verge 的話。
  - **站上文章 CB** 沒列在 `sources`，撰稿人漏的，本輪已補 DC5。
  - 0xoa「伊利諾州的 Joliet」：原文是 Joliet Township（鎮區，不是 Joliet 市）。卡片 kicker 寫對，旁白簡稱不算錯，沒改。
  - lwdi「一般人目前不行」：DC3 只說「eligible firms」「DTC participants」，沒明說散戶不能用；推論合理，卡片「Banks, yes / retail, no」偏強，沒改。
  - 24fy「智慧型手機銷量比 2025 年少了大約兩成」：V2 沒說是高通的晶片出貨還是整體手機市場；旁白也沒說是誰的，沒改。
  - ms-circle-why 左欄「Net income up 5%」是持續經營淨利（continuing operations），沒改。
  - sd-ram-when「Intel: at least into next year」：原文「through at least next year」，稍弱但方向一致，沒改。
- 需要第二輪：**否**。本輪改了 2 個事實（不超過 3 個）。所有主張都已判定，沒有懸而未決的。
