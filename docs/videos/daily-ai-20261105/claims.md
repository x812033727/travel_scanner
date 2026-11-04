# daily-ai-20261105 主張與證據

每一行：編號｜主張（旁白或卡片上的說法）｜站上文章；原始來源｜來源查證日｜場景 id。
事實只用站上 news_date 2026-11-04 已發布的文章（`/api/travel/guides/life/<slug>?locale=zh-TW` 取得，2026-11-04，15 篇皆 HTTP 200）與它們列的來源。
撰稿人沒有另外打開原始來源：各則的事實與英文引句依站上文章的轉述（站上文章引用了原文英文句）；查核代理要再逐句對回原文。
「自述」＝公司自己公布、沒有第三方確認；「換算」＝節目依來源數字自己算的；「建議」＝節目的建議，不是來源的說法；「背景」＝一般常識，不出自來源。

站上文章簡稱：
- MID＝https://mokaair.com/zh-TW/life/ai-news-data-center-midterms-20261104 ；V1＝https://www.theverge.com/policy/1026365/data-centers-midterms-results
- VOT＝https://mokaair.com/zh-TW/life/ai-news-us-voters-data-center-restrictions-20261104 ；DC1＝https://decrypt.co/382556/us-voters-back-ai-data-center-restrictions
- QCOM＝https://mokaair.com/zh-TW/life/ai-news-qualcomm-data-center-20261104 ；V2＝https://www.theverge.com/ai-artificial-intelligence/1026867/qualcomm-earnings-data-centers
- GIF＝https://mokaair.com/zh-TW/life/ai-news-chatgpt-animated-gifs-images-26-20261104 ；V3＝https://www.theverge.com/ai-artificial-intelligence/1026474/openai-chatgpt-animated-gifs-images-2-6
- SIRI＝https://mokaair.com/zh-TW/life/ai-news-apple-siri-recaps-watch-beta-20261104 ；TC1＝https://techcrunch.com/2026/11/04/i-tried-apples-siri-recaps-theyre-surprisingly-useful-and-a-little-unsettling/
- COND＝https://mokaair.com/zh-TW/life/ai-news-meta-acquires-conductor-20261104 ；TC2＝https://techcrunch.com/2026/11/04/meta-acquires-ai-coding-startup-conductor/
- DDG＝https://mokaair.com/zh-TW/life/ai-news-duckduckgo-schools-google-ai-policy-20261104 ；TC3＝https://techcrunch.com/2026/11/04/duckduckgo-pitches-itself-to-schools-amid-backlash-over-googles-ai-policy/ ；GB1＝https://blog.google/products-and-platforms/products/education/google-chromebook-feature-update-september-2024/ ；GB2＝https://blog.google/products-and-platforms/products/education/google-classroom-anniversary-teachers/
- OAI＝https://mokaair.com/zh-TW/life/ai-news-openai-2028-election-20261104 ；TC4＝https://techcrunch.com/2026/11/04/openai-is-already-trying-to-shape-the-2028-election/
- UBER＝https://mokaair.com/zh-TW/life/ai-news-uber-ai-agents-rides-20261104 ；V4＝https://www.theverge.com/transportation/1026306/uber-ai-agents-q3-earnings-disintermediation
- OCC＝https://mokaair.com/zh-TW/life/ai-news-occ-bank-ai-framework-20261104 ；DC2＝https://decrypt.co/382560/us-bank-regulator-issues-first-ai-framework-banks-battle-rogue-agents
- MS＝https://mokaair.com/zh-TW/life/crypto-news-morgan-stanley-dtcc-tokenization-20261104 ；DC3＝https://decrypt.co/382513/wall-streets-plumbing-onchain-morgan-stanley-tokenizes-securities
- CRCL＝https://mokaair.com/zh-TW/life/crypto-news-circle-workforce-cut-20261104 ；DC4＝https://decrypt.co/382493/usdc-issuer-circle-quietly-cuts-5-of-staff-in-profitable-quarter
- CB＝https://mokaair.com/zh-TW/life/crypto-news-coinbase-cold-storage-binance-hack-20261104 ；DC5＝https://decrypt.co/382570/coinbase-99-percent-customer-crypto-offline-binance-hack
- RAM＝https://mokaair.com/zh-TW/life/ai-news-altman-ram-comments-20261104 ；V5＝https://www.theverge.com/ai-artificial-intelligence/1026292/sam-altman-ram-shortage-pcs-comments

## Intro

c1｜2026-11-05 是星期四（曆法）｜—｜—｜intro
c2｜今天的主題：美國期中選舉裡的 AI 資料中心（問題「為什麼要用投票擋」，答案在 c25–c27、片尾 c96）｜MID；V1；VOT；DC1｜2026-11-04｜intro-kai, intro-q

## Headlines

c3｜快訊是 news_date 2026-11-04 的站上文章（「昨天，11 月 4 日的科技新聞」）；其中幾件事發生在週二 11/3（蘋果開始測試、Google 告知學校、摩根士丹利的說法），旁白照實說「週二」｜各站上文章｜2026-11-04｜hl-open
c4｜據 The Verge，ChatGPT 可用文字提示或上傳的照片生成 GIF；可調播放速度、編輯個別影格並分享｜GIF；V3｜2026-11-04｜hl-gif, hl-gif-how
c5｜隨 OpenAI 新的 Images 2.6 模型推出；正向所有 ChatGPT 與 Codex 使用者推出（網頁、桌面、行動 App）｜GIF；V3｜2026-11-04｜hl-gif-who
c6｜OpenAI 稱每週在 ChatGPT 與 API 生成超過 40 億張圖，9 月公布為 30 億張（自述）｜GIF；V3｜2026-11-04｜hl-gif-who
c7｜報導沒有提到 GIF 的長度、解析度、檔案大小限制；「先看 OpenAI 自己的說明」依站上文章的提醒｜GIF；V3｜2026-11-04｜hl-gif-limit
c8｜據 TechCrunch，Apple 週二開始在 iOS 27.3 與 watchOS 27.3 首批開發者測試版測試四項音訊 AI 功能，對象 Apple Watch Series 12｜SIRI；TC1｜2026-11-04｜hl-siri, hl-siri-when
c9｜四項：偵測重要聲音（警報、門鈴）、辨識歌曲（Shazam 技術）、Live Rewind（回看過去 15 秒）、Siri Recaps（摘要整天音訊存成筆記）；後兩項會錄音、轉錄或摘要身邊的對話｜SIRI；TC1｜2026-11-04｜hl-siri-what
c10｜TechCrunch 作者試用一天：替家中青少年的車送修時，店員講得很快，Siri Recaps 記下自付額與維修時程（也記了租車油量，旁白未提）｜SIRI；TC1｜2026-11-04｜hl-siri-good
c11｜它也記下不重要的閒聊；作者說談話更私人時可能覺得被侵犯、考慮晚上在家關閉；作者把功能設為隨時運作｜SIRI；TC1｜2026-11-04｜hl-siri-bad, hl-siri-privacy, tt-listen
c12｜Apple 的做法：盡可能在裝置上處理、不辨識說話者、不儲存原始音檔（另遮蔽證件號碼與帳戶資訊，旁白未提）；有人反感「科技隨時在聆聽」被常態化｜SIRI；TC1｜2026-11-04｜hl-siri-privacy, hl-siri-norm
c13｜目前只在開發者測試版；報導沒有正式推出時間｜SIRI；TC1｜2026-11-04｜hl-siri-when
c14｜據 TechCrunch，Meta 收購 AI 寫程式新創 Conductor；產品讓使用者在平行工作區部署多個代理建立軟體專案｜COND；TC2｜2026-11-04｜hl-meta, hl-meta-what
c15｜Conductor 部署的代理不是自行開發，來自 Anthropic、OpenAI 等大型實驗室｜COND；TC2｜2026-11-04｜hl-meta-src
c16｜創辦人 Charlie Holtz：雲端服務 11 月 20 日關閉，之後開始刪除使用者雲端資料；核心功能到明年初照常運作（卡片「Early 2027」＝換算：明年初）｜COND；TC2｜2026-11-04｜hl-meta-date
c17｜Meta 向 TechCrunch 確認收購，不提供金額與其他細節｜COND；TC2｜2026-11-04｜hl-meta-deal
c18｜據 TechCrunch，Google 11/3（週二）告訴學校可以關閉 Gemini，但關閉其他 AI 功能會失去 Google 搜尋；搜尋大量用 AI（AI Overviews、AI Mode）｜DDG；TC3｜2026-11-04｜hl-school, hl-school-all, hl-school-why
c19｜Google 在反彈後稱 Gemini、Gemini Notebook 與搜尋預設關閉，學校可個別啟用（Google 的說法，經 TechCrunch）｜DDG；TC3｜2026-11-04｜hl-school-reply
c20｜DuckDuckGo 執行長 Gabriel Weinberg 在 X 上指向切換預設搜尋引擎的文件；公司稱 AI 功能可在設定中關閉（DuckDuckGo 的說法）｜DDG；TC3｜2026-11-04｜hl-school-ddg, hl-school-ddg2
c21｜Google 先前公布：校園約 5,000 萬台 Chromebook、Classroom 逾 1.5 億使用者；不代表這次受影響人數｜DDG；TC3；GB1；GB2｜2026-11-04｜hl-school-scale
c22｜報導沒有分地區；實際設定由各校與管理員決定（站上文章的說法）｜DDG｜2026-11-04｜hl-school-tw
c23｜據 TechCrunch 報導，OpenAI 首席全球事務官 Chris Lehane 認為 2028 年總統大選可能是 AI 的關鍵時刻；文章發在民主黨期中選舉大勝之後；把 AI 比作新政、提出五項優先事項（勞工保護、教育、AI 安全、資料中心）｜OAI；TC4｜2026-11-04｜hl-oai, hl-oai-why, hl-oai-what
c24｜Lehane 警告支持暫停興建資料中心的政治人物可能危及美國對中國的領先；OpenAI 發稿前未回應 TechCrunch｜OAI；TC4｜2026-11-04｜hl-oai-dc, hl-oai-reply
c25｜Signal Number：Uber 高層 11/4 上午財報會議說，2026 年第三季只有 4 趟行程由第三方 AI 代理安排；Uber 首次公開此類數字｜UBER；V4｜2026-11-04｜hl-number, hl-number-what
c26｜Uber Eats 萬聖節當週約 500 筆訂單由 AI 代理完成；兩數字期間不同、不宜直接相比｜UBER；V4｜2026-11-04｜hl-number-eats
c27｜專家預測「去中介化」風險（顧客改用 AI 代理而不開平台 App）；The Verge 認為現階段風險很小｜UBER；V4｜2026-11-04｜hl-number-why, hl-number-small

## Signal of the Day

c28｜場景：威斯康辛州 Janesville 的選民在 11/3 投票；措施為前通用汽車廠址的大型開發前須再次公投，該地與一項擬議資料中心有關，超過 60% 通過（「想像你」是節目設定的觀眾情境，不是真人訪談）｜VOT；DC1｜2026-11-04｜sd-scene, sd-scene-q, sd-scene-dc, sd-back
c29｜資料中心＝集中放置晶片與伺服器、訓練與運行 AI 的設施｜VOT；DC1；MID｜2026-11-04｜sd-def
c30｜Decrypt 引述華盛頓郵報：美國至少 29 個轄區的選民在 11/3 支持禁止或限制資料中心開發｜VOT；DC1｜2026-11-04｜sd-many, sd-wrap
c31｜反對原因：用電量大，推高電費、加重電網負擔；另有用水、噪音、缺乏公眾監督的協議｜VOT；DC1｜2026-11-04｜sd-why, sd-why-more
c32｜NBC News 選舉日調查（經 The Verge）：76% 受訪選民反對自己社區出現資料中心｜MID；V1｜2026-11-04｜sd-poll
c33｜Ballotpedia（經 Decrypt）：10 州共 41 項資料中心相關措施，28 項投贊成即限制，13 項允許或支持｜VOT；DC1｜2026-11-04｜sd-count, sd-flip
c34｜The Verge：45 項地方公投，依 Redbud Consulting 整理，截至週三早上 33 項結果將限制開發｜MID；V1｜2026-11-04｜sd-count
c35｜Hubbard（俄亥俄）超過四分之三支持禁止；Wells（緬因）大型資料中心 180 天暫停（追溯至 2026 年 6 月中，旁白未提）；El Dorado（堪薩斯）10 年內禁止尖峰用電超過 10MW 的資料中心（MW 唸「兆瓦」）｜VOT；DC1；MID；V1｜2026-11-04｜sd-examples
c36｜伊利諾州 Joliet Township 近 80% 選民否決支持 AI 資料中心的諮詢性提案｜VOT；DC1｜2026-11-04｜sd-joliet
c37｜部分措施只是諮詢性投票，通過後不會自動停工｜VOT；DC1｜2026-11-04｜sd-advisory
c38｜德州民主黨的 Gina Hinojosa 擊敗現任共和黨州長 Greg Abbott，競選時主張暫停新專案；Decrypt 認為這類勝選可能帶來更嚴格的州級規範（俄亥俄州當選州長 Amy Acton 支持暫停，旁白未提）｜VOT；DC1；MID；V1｜2026-11-04｜sd-texas, sd-state
c39｜The Verge：很難把資料中心反彈與任何一位候選人當選直接畫上等號，也有主張較有限限制的候選人勝選｜MID；V1｜2026-11-04｜sd-careful, tk-unsure
c40｜The Verge：開發商將面對更嚴格的建設環境｜MID；V1｜2026-11-04｜sd-money-q
c41｜佛羅里達共和黨當選人 Byron Donalds 提案要求開發商自行負擔能源與用水；愛荷華的 Rob Sand 與對手同意終止稅收優惠；賓州州長 Josh Shapiro 簽行政命令禁止資料中心開發案使用保密協議（卡片「What winners proposed」：三人在 The Verge 表中都列為當選者）｜MID；V1｜2026-11-04｜sd-terms
c42｜AI 公司加強遊說、做公關；OpenAI 試圖把資料中心改稱「compute campuses」（運算園區）｜VOT；DC1｜2026-11-04｜sd-industry
c43｜據 The Verge，智慧型手機銷量較 2025 年下滑約 20%，高通把成長押在 AI 資料中心；預測 2029 年資料中心營收 150 億美元、最終約占業務 30%（公司預測）｜QCOM；V2｜2026-11-04｜sd-qcom, sd-qcom-why
c44｜報導沒有說選民的限制會影響高通；旁白明說不推論。「資料中心總得蓋在某個地方」是節目的話｜QCOM｜2026-11-04｜sd-qcom-link
c45｜今天的來源都沒有提到台灣；亞洲供應鏈是否受影響，來源沒有答案｜各站上文章｜2026-11-04｜sd-taiwan, sd-ram-unknown
c46｜The Verge：AI 資料中心搶購全球 RAM，造成短缺、帶動科技產品漲價，讓許多人難以為電腦裝大量 RAM｜RAM；V5｜2026-11-04｜sd-ram, sd-ram-when, nd-end
c47｜英特爾預期短缺至少持續到明年（卡片「2027」＝換算）；SK Hynix 預測可能拖到 2030 年（「記憶體廠」是背景）｜RAM；V5｜2026-11-04｜sd-ram-when
c48｜接下來看什麼：哪些投票有約束力（c37）、新州長會不會立法（c38）、電費用水與稅收優惠誰付（c41）是節目依來源整理的三點；The Verge 說實際政策取決於後續立法與執行，沒有時間表｜MID；V1；VOT；DC1｜2026-11-04｜sd-next, sd-timeline
c49｜TechCrunch：可負擔性逐漸成為 2028 年大選關鍵；若選民擔心資料中心推高電費、AI 取代工作，AI 可能成為越來越大的議題｜OAI；TC4｜2026-11-04｜sd-2028, sd-2028-why

## What People Are Saying

c50｜貝萊德執行長 Larry Fink 上月："If we have a moratorium of some sort in this country, we will be in a recession."｜VOT；DC1｜2026-11-04｜wp-fink
c51｜AI Now Institute 的 Kate Brennan 評 Lehane 文章：「ahistorical at best and harmful at worst」；她認為這是私人公司為自身利益倡議政策｜OAI；TC4｜2026-11-04｜wp-brennan, wp-brennan-why
c52｜Uber 執行長 Dara Khosrowshahi："It is just very, very early, and we want to make sure we are not dependent on any one player."（卡片只引前半）｜UBER；V4｜2026-11-04｜wp-uber

## Money Signal

c53｜據 Decrypt，美國通貨監理署 OCC 2026-11-04 發布首份銀行業 AI 監理框架，共 22 頁，寫給檢查人員｜OCC；DC2｜2026-11-04｜ms-occ, ms-occ-who
c54｜框架少看 AI 多強、多看出錯的後果；三項考量：失敗後果、行動能否撤回、人類保有多少控制權｜OCC；DC2｜2026-11-04｜ms-occ, ms-occ-how
c55｜示例最高風險層級：完全自主的付款代理、即時信用決策系統；能發起金融交易的簡單代理風險可能高於只寫內部文件的先進模型｜OCC；DC2｜2026-11-04｜ms-occ-top, ms-occ-simple
c56｜建議保護：斷路器、速率限制、受限權限、緊急關閉機制（「像家裡的總開關」是 Kai 的比喻）｜OCC；DC2｜2026-11-04｜ms-occ-guard
c57｜Decrypt 引述 Axios 10/22：銀行發現未經授權的第三方 AI 代理在客戶帳戶內運作；摩根士丹利阻擋外部代理，摩根大通、美國銀行、花旗限制存取；OCC 未將框架與這些事件直接連結｜OCC；DC2｜2026-11-04｜ms-occ-axios, ms-occ-banks
c58｜OCC 強調文件不創設新的法規要求，讓檢查人員在既有風險類別下評估 AI｜OCC；DC2｜2026-11-04｜ms-occ-rule
c59｜摩根士丹利週二（11/3）表示已透過 DTCC Tokenization Service 把美股與美國公債代幣化；服務 10/28 上線，由 DTC 營運，DTC 託管逾 114 兆美元｜MS；DC3｜2026-11-04｜ms-ms, ms-dtc
c60｜DTCC 稱代幣保有與原證券相同的所有權、投資人保護與經濟權益，可換回原證券｜MS；DC3｜2026-11-04｜ms-twin
c61｜使用者是符合資格的金融機構，20 家 DTC 參與者報名（含美國銀行、花旗、摩根大通）；一般散戶無法直接使用；銀行主導，不同於加密原生業者的代幣化股票｜MS；DC3｜2026-11-04｜ms-who, ms-contrast
c62｜據 Decrypt，USDC 發行商 Circle 在週三第三季財報揭露裁員約 5%；持續經營淨利 2.26 億美元、年增 5%；準備金收入因利率下降減少 8%（旁白只講百分比）｜CRCL；DC4｜2026-11-04｜ms-circle, ms-circle-why
c63｜Circle 稱調整是為讓組織結構更符合營運模式與策略重點；未說明人數與團隊｜CRCL；DC4｜2026-11-04｜ms-circle-unknown
c64｜Decrypt 列出今年其他加密企業裁員：Coinbase 5 月 14%、以太坊基金會 6 月 20%、Bitwise 8 月 14%（另有 BitGo、Luno，卡片未列）；理由包括市場轉弱、AI 或兩者｜CRCL；DC4｜2026-11-04｜ms-circle-wave
c65｜Coinbase 週三部落格稱未受上週幣安駭客事件影響；超過 99% 客戶資產在冷儲存；冷錢包私鑰分割、簽署時不完全重組；提領異常暴增時先暫扣待審（Coinbase 自述，經 Decrypt）｜CB；DC5｜2026-11-04｜ms-cb, ms-cb-how, ms-cb-note
c66｜「AI 代理碰到錢的規則正在成形；工作在被重新安排」是節目的整理；本段不談價格｜OCC；CRCL｜2026-11-04｜ms-you

## Try This（皆為建議）

c67｜三件都是節目建議，不是蘋果、Conductor 或銀行的指示（旁白、卡片 kicker「our advice」、steps 的 source「Our advice」）｜—｜—｜tt-open
c68｜建議：會錄音、會摘要的 AI 功能，先搞清楚何時在聽；私下談話時關掉、先告知身邊的人（依 c11、c12；作者考慮晚上在家關閉）｜SIRI；TC1｜2026-11-04｜tt-listen, tt-listen-off
c69｜建議：用 Conductor 雲端的人，在 11/20 前把要留的資料存下來（依 c16；Try This 用「剛剛那個日期」回扣，卡片寫 Nov 20）｜COND；TC2｜2026-11-04｜tt-export, tt-export-why
c70｜建議：讓 AI 工具碰帳戶前，先看能不能設上限、隨時收回權限（思路依 c55–c57 的交易限額與撤銷存取）｜OCC；DC2｜2026-11-04｜tt-pay

## Noise of the Day

c71｜據 The Verge，Sam Altman 在選舉夜於 X 上替自己對個人電腦 RAM 的立場辯護（改名「Ram Altman」一事旁白不提，免得同音字）｜RAM；V5｜2026-11-04｜nd-open, nd-what
c72｜起點是 Cheeky Pint podcast：讓大家把有限的 DRAM 放在自己電腦、只用 5% 的時間「quite terrible」（卡片「his figure」）｜RAM；V5｜2026-11-04｜nd-podcast
c73｜Altman 稱被斷章取義，並回覆："i want you to have so much ram lets build more."｜RAM；V5｜2026-11-04｜nd-clarify

## Sola's Take、片尾

c74｜「今天最重要的是選舉裡的資料中心」「AI 有房子、要用電，住旁邊的人用選票說話」「我不確定會不會蓋得比較慢」是節目的看法；依 c28–c49｜—｜—｜tk-main, tk-why, tk-unsure
c75｜主題的完整整理在 Mokaair 文章，說明欄列主題的兩篇站上文章（MID、VOT）｜MID；VOT｜2026-11-04｜tk-site
c76｜片尾答案：電費、用水和噪音讓資料中心成了地方投票的題目（c31）｜VOT；DC1｜2026-11-04｜outro

## 我懷疑但沒動的事

- 29 個轄區（華盛頓郵報，經 Decrypt）、41 項（Ballotpedia，經 Decrypt）、33/45 項（Redbud，經 The Verge）是三個不同的算法；旁白說「看誰算」，沒有把它們加在一起。查核代理要對回 DC1、V1。
- Janesville「超過 60% 通過」與「與擬議資料中心有關」都依 VOT 的表格；查核代理要對 DC1 原文。
- 高通的站上文章寫「2026 年總營收 104 億美元」，跟高通的年營收規模對不上（疑為單季），旁白不用；也沒寫財報會議的日期，旁白只說「昨天的新聞裡」。
- 「Hinojosa 擊敗 Abbott」：Decrypt（VOT）這樣寫；The Verge（MID）表中寫她當選、Abbott 是現任。旁白只說「擊敗了現任州長」。
- 英特爾「至少到明年」，卡片寫 2027；站上文章另提 Samsung 的預期只出自相關報導標題，沒用。
- Uber 的「3.2 億筆」站上文章沒寫期間，沒用。

## 沒有放進來的

- Nexus Mods 的 AI 揭露規定（ai-news-nexus-mods-ai-disclosure-20261104）：選了 Altman 當 Noise。
- 台灣或亞洲供應鏈與美國資料中心投票的直接關聯：今天的來源都沒有，旁白明說不猜。
- Lehane 把支持暫停比作 2002 年伊拉克戰爭授權投票、OpenAI 與 SB 1047 的歷史：細節太多。
- Circle 的營收、EBITDA、USDC 流通量與市占；Coinbase 過往資安事件；Binance 竊案金額：與主線無關或屬財報數字。

## 進度

- 116 個場景、257 句；`lint` 0 錯誤（剩下兩條是開場濃縮的警告，對本節目不適用）；估 21.5 分鐘，最長的畫面狀態估 13.0 秒（outro）。
- 新加的發音字典詞（Conductor、Janesville、Hubbard、Joliet、Ballotpedia、Lehane、Brennan 等 null；DTC、DTCC、OCC、NBC、USDC、SK、GIF 照字母念）要試聽。
- 待做：另派查核代理照 `prompts/verifier-video.md` 逐則對回來源；Whisper 第二意見與試聽；配樂已綁 `techsignal-bed.mp3`。
