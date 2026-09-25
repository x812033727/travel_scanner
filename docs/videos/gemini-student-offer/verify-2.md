# verify-2 — gemini-student-offer（第 2 輪查核，2026-09-25）

查核者：第二位獨立查核代理（不是撰稿者，也不是第一輪查核者）。對象：`_shelf/gemini-student-offer/gemini-student-offer/video.json`，外加 `claims.md`、`brief.md`、`verify-1.md`。

範圍：① 第一輪改過的 19 條全部重查；② 第一輪 CONFIRMED 的 50 條，用固定種子隨機抽三分之一（17 條）重查；③ 了結第一輪留下的懷疑（「搜尋摘要」、9q5n 的「只有」、898w 的「最容易」、dipd／hqj8 的出處）。聽眾檢查清單上的句子（iyph、938u、9m3b、tnez、2jya，以及近重複的 qjpw／dipd、tigk／d4k5）照指示一律沒改，由統籌處理。

方法：所有官方頁面今天重新抓一次，`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔至少 1.5 秒，去掉 `<!-- -->`、script、style 後讀文字；請求裡沒有任何個人資料，沒有登入任何帳號。Web search 用了 0 次。頁面與文字檔在 `<VIDEO_WORKDIR>/gemini-student-offer/_tools/verify2/pages/`，修改前後的主張清單是 `_tools/verify2/claims-list-before.md`、`claims-list-after.md`，抽樣腳本是 `_tools/verify2/sample.py`（結果在 `sample.txt`）。站內素材直接讀 `<ROOT>` 的檔案。

網址代號（HTTP 皆為跟隨轉址後的最終狀態，2026-09-25 抓取）：

- U1 公告 https://blog.google/innovation-and-ai/products/gemini-app/student-offer-google-ai/ — 200（datePublished 2026-08-19T19:00Z，dateModified 2026-08-21）
- U2 優惠條款 https://one.google.com/offer/studentoffer8 — 200（Last updated: August 19, 2026）；`?hl=zh-TW` — 200（上次更新日期：2026年8月19日）
- U3 Google One 供應清單 https://support.google.com/googleone/answer/16548195?hl=zh-TW — 200（轉址到 hl=zh-Hant）
- U4 台灣學生頁 https://gemini.google/tw/students/?hl=zh-TW — 200
- U5 Google One 方案頁 https://one.google.com/intl/zh-TW_tw/about/google-ai-plans/ — 200
- U6 Gemini 台灣訂閱頁 https://gemini.google/tw/subscriptions/?hl=zh-TW — 200
- U7 讀書工具公告 https://blog.google/innovation-and-ai/products/gemini-notebook/new-study-tools-september-2026/ — 200（datePublished 2026-09-15T16:00Z）
- U8 Workspace 公告 https://workspaceupdates.googleblog.com/2026/09/new-back-to-school-features-and-learning-tools-available-in-Gemini-Notebook.html — 200（September 18, 2026）
- U9 改名公告 https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/ — 200（datePublished 2026-07-16T16:00Z）
- U10 Gemini Notebook 繁中說明 https://support.google.com/gemininotebook/answer/16206563?hl=zh-Hant — 200
- U11 Google 搜尋中心〈如何撰寫中繼說明〉https://developers.google.com/search/docs/appearance/snippet?hl=zh-tw — 200（英文版 `?hl=en` — 200）
- L1 `apps/api/app/guides/content/notebooklm-guide.json`（zh-TW 第一步、第二步）— 站內檔案
- L2 `apps/web/public/guides/ai-news-gemini-student-offer-20260820/diagram-1.svg` — 站內檔案

「R1-#n」是 verify-1.md 表格的編號。

## 一、第一輪改過的 19 條（全部重查）

| # | 主張 | 位置 | 網址 | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | R1-#11「這七個地區裡，並沒有台灣。」 | 5y8q | U1 | 200 | CONFIRMED：注腳「except for in the U.S., Bolivia, Albania, Canada, Macau, Hong Kong, and Tunisia」，七個裡沒有台灣 | — |
| 2 | R1-#16 四關圖是站上文章畫的、整理的 | xd2e、c92q | L2 | 檔案 | CONFIRMED：SVG 右下角「© Mokaair 製圖 2026」 | — |
| 3 | R1-#17 四個方框排成兩排 | c92q | L2 | 檔案 | CONFIRMED：四個 rect 座標 (110,180)(850,180)(110,500)(850,500)，2×2，沒有箭頭 | — |
| 4 | R1-#17「每個方框底下，都寫了一行這一關的重點」 | e4ju | L2 | 檔案 | CHANGED：重點那行小字在方框「裡」、關卡名底下（y=348／668，方框範圍 180–425／500–745），不在方框下面；觀眾看著圖聽到「方框底下」會找錯位置 | 「每個方框底下，都寫了一行這一關的重點。」→「每個方框裡，都寫了一行這一關的重點。」 |
| 5 | R1-#19「地區先看到這裡，接下來三關才是真正的考驗。」 | yaz7 | U1–U4 | 200 | CONFIRMED：不再替觀眾判定地區過關 | — |
| 6 | R1-#24 註冊時就要有付款方式 | 4xph、four-gates-steps.steps[1].detail | U2、U2 繁中、U1、U4 | 200 | CONFIRMED：條款「Have a Google Payments account with a qualifying form of payment at sign-up」；繁中「在訂閱時具備符合資格的付款方式」；公告「Valid form of payment required at sign-up」；U4「註冊時必須提供有效的付款方式」 | — |
| 7 | R1-#25「帳號：個人帳戶，註冊時綁好付款方式」 | outro.lines[1] | U2 | 200 | CONFIRMED | — |
| 8 | R1-#27 學校配發的帳號不能兌換 | 2k4m | U2 | 200 | CONFIRMED：「This offer is not available on your school-issued Workspace for Education account」；繁中「不適用於學校提供的 Workspace for Education 帳戶」 | — |
| 9 | R1-#30「2026年12月31日前兌換，兌換日起算12個月」 | steps[2].detail | U2 | 200 | CONFIRMED：「12 month period from the day you redeem the Offer」「must be redeemed by December 31, 2026」 | — |
| 10 | R1-#33 Gemini 方案頁寫一般 Plus 每月新台幣 165 元 | fbh6 | U6 | 200 | CONFIRMED：伺服器端 HTML 就有 `每月 <span class="price-symbol">NT$</span><span class="price-amount">165</span> 元`，在「台灣」區塊的 Google AI Plus 卡片；同頁 Pro NT$650 | — |
| 11 | R1-#35「英文條款的用詞是，…可能維持到期滿，不是保證」 | 9ttj | U2、U2 繁中 | 200 | CONFIRMED：英文「your membership may remain active until the end of the Offer Period」；繁中仍寫「取消後仍可保有會員資格」，點明英文版有必要 | — |
| 12 | R1-#37「頁尾這句，講的是試用期結束後怎麼收費。」 | hwep | U4 | 200 | CONFIRMED：「如未提前取消 Google AI Plus，試用期結束後，系統將自動收取每月 $165」 | — |
| 13 | R1-#46 NotebookLM 改名，換上 Gemini 的名字 | 86i3 | U9、U10 | 200 | CONFIRMED：「Today, we're renaming NotebookLM to Gemini Notebook」；繁中說明中心也寫英文「Gemini Notebook」 | — |
| 14 | R1-#49「改名之後功能延續，九月又替測驗、字卡加了新功能，還有短影片摘要」 | acc4 | U9、U7、U8 | 200 | CONFIRMED：U9「It remains a standalone product」；U8（9/18）「We're expanding exam prep tools」：新題型、就最近完成的測驗與字卡向筆記本提問、可自訂題目；U7 把測驗、字卡當既有的 studio outputs；Short Video Overviews 約 60 秒、80 種以上語言，列在同一批更新。注意新題型 U7 注腳 4 寫「in the next few weeks」 | — |
| 15 | R1-#59「改一天而已，很容易被忽略，點開引用就能核對。」 | qiiv | L1 | 檔案 | CONFIRMED：原教學「引用…的功能是讓你追查支持內容」「若資料太短，工具可能引用整份來源…仍應打開來源查看」 | — |
| 16 | R1-#61 地點「社區教室，新補上」；「到公告乙才補上社區教室」 | demo-table.rows[2]、bbi7 | L1 | 檔案 | CONFIRMED：公告甲「場地尚未確認」，公告乙「地點為社區教室」 | — |
| 17 | R1-#63 費用「免費，新補上」；「到公告乙才寫明免費」 | demo-table.rows[4]、rdqg | L1 | 檔案 | CONFIRMED：公告甲「是否收費也尚未決定」，公告乙「免費參加」 | — |
| 18 | R1-#64「未定不等於要收費，這種欄位最容易被記錯。」 | a435 | L1 | 檔案 | CHANGED：前半成立（公告甲沒說要收費）。「最容易」是最高級比較，原教學沒有；原教學只提醒「對數字、否定詞和條件要多看前後句，例如『未提供日期』不能簡化成『沒有截止期限』」，支持「容易記錯」，不支持「最」 | 「…這種欄位最容易被記錯。」→「…這種欄位很容易被記錯。」 |
| 19 | R1-#67「這段示範不用登入帳號，看完你也能自己做一次。」 | 56f4 | L1、U8 | 200 | CONFIRMED：只說這段示範不用登入；自己做需要帳號，句子沒有否認（U8：個人 Google 帳戶也可用） | — |
| 20 | R1-#68 片名「…四道關卡全解析」、「免費一年」 | youtube.title | U1、L2 | 200 | CONFIRMED：「one year of a Google AI plan free of charge」；四道關卡是站上框架，片名沒說是官方的 | — |

## 二、第一輪 CONFIRMED 的隨機三分之一

抽法：`random.Random(20260925).sample(50 條, 17)`，種子 **20260925**；抽中 R1-#1、6、8、9、20、21、23、29、36、39、43、44、45、50、53、56、58。

| # | 主張 | 位置 | 網址 | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 21 | R1-#1 公告注腳七個排除地區，沒有台灣 | official-bullets.items[0]、8hpd、hbgv、nyb8 | U1（U7 同一注腳） | 200 | CONFIRMED | — |
| 22 | R1-#6 供應清單上找得到台灣 | official-bullets.items[2]、ytv8、bkd5 | U3 | 200 | CONFIRMED：「目前支援 Google AI Plus 的國家/地區」清單有「台灣」 | — |
| 23 | R1-#8 條款看就讀學校所在地 | 2qfp、awap、steps[0].detail、outro.lines[0] | U2 | 200 | CONFIRMED：「enrolled at a higher education institution in a country or region where the subscription plan … is supported」 | — |
| 24 | R1-#9 兩份排除名單合起來七個：美國、加拿大、港澳、另外三個國家 | y5d9、i823、excluded-vs-supported.left.points | U1、U2 | 200 | CONFIRMED：條款六個都在公告七個之內；另三個是玻利維亞、阿爾巴尼亞、突尼西亞 | — |
| 25 | R1-#20 年滿 18 歲 | 2ivg、steps[0].detail、outro.lines[0] | U2 | 200 | CONFIRMED：「Be 18 years of age or older」 | — |
| 26 | R1-#21 第三方驗證學生身分 | awap、dstq、steps[0].detail | U2 | 200 | CONFIRMED：「third-party verification service, SheerID」 | — |
| 27 | R1-#23 個人 Google 帳戶 | f8th、steps[1].detail | U2 | 200 | CONFIRMED：「Have a personal Google Account」 | — |
| 28 | R1-#29 12 個月從兌換當天起算，兌換期限不是到期日 | zj9u、rxhm、nm7d、zijq、real-math-table.rows[0] | U2 | 200 | CONFIRMED | — |
| 29 | R1-#36 頁尾主打 Plus 方案、每月 165 | page-contradictions.items[0]、ic7q | U4 | 200 | CONFIRMED | — |
| 30 | R1-#39 英文公告：美國以外的學生拿另一個方案 | unu4 | U1 | 200 | CONFIRMED：美國「Google AI Pro」，美國以外「Google AI Plus」 | — |
| 31 | R1-#43 企業端：滿 18 歲現在就能即時語音對話 | ikea | U8 | 200 | CONFIRMED：「Users 18 years or older can now have a real-time conversation with their notebooks」 | — |
| 32 | R1-#44 消費端：你很快就可以 | wths | U7 | 200 | CONFIRMED：「You can soon have a real-time conversation…」，注腳「Rolling out to Google AI Ultra subscribers (18+) this week and coming to Google AI Pro and others soon」 | — |
| 33 | R1-#45 兩份是同一批公告 | 93u7、y4ux | U7、U8 | 200 | CONFIRMED：U8「started on September 15, 2026」，Resources 連回 U7 | — |
| 34 | R1-#50 短影片摘要 | acc4 | U7、U8 | 200 | CONFIRMED：Short Video Overviews，~60 秒，80 種以上語言 | — |
| 35 | R1-#53 公告甲 9/1 初稿、公告乙 9/8 修正版、差一週 | fhzt、nr8m、demo-code.code | L1 | 檔案 | CONFIRMED | — |
| 36 | R1-#56 提示詞：只根據甲乙、六個欄位、附引用、標出更正與未提供 | demo-code.code、heg3、22ic | L1 | 檔案 | CONFIRMED | — |
| 37 | R1-#58 日期 10 日→11 日，已更正 | demo-table.rows[0]、pddy | L1 | 檔案 | CONFIRMED | — |

## 三、第一輪留下的懷疑

| # | 主張 | 位置 | 網址 | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 38 | 「搜尋結果的摘要，又叫你去訂閱另一個更貴的方案」 | tgmj | U4、U11 | 200 | CHANGED：這句在 U4 的 `<meta name="description">` 與 og:description（「立即訂閱 Google AI Pro 方案，享有更多 Gemini 功能！」）。U11：「Google 主要會使用網頁上的內容，自動決定適用的摘要」，中繼說明只是「也會」用，且「可能會根據不同筆搜尋，為同一個網頁顯示不同摘要」。不能說搜尋結果就是這句；「更貴」成立（U6：Pro NT$650、Plus NT$165） | 「搜尋結果的摘要，又叫你去訂閱另一個更貴的方案。」→「網頁寫給搜尋引擎的摘要，又叫你去訂閱另一個更貴的方案。」 |
| 39 | 「搜尋結果的摘要，通常是最多人第一眼看到的文字」 | yu5p | U11 | 200 | CHANGED：同上，Google 不保證顯示中繼說明；「通常」「最多人」沒有來源。第一輪列為觀點，但它是事實句，而且和 #38 同一個問題 | 「搜尋結果的摘要，通常是最多人第一眼看到的文字。」→「這段摘要，可能就是你在搜尋結果裡第一眼看到的文字。」 |
| 40 | 字卡「搜尋摘要又推另一個更貴的方案」 | page-contradictions.items[2] | U4、U11 | 200 | CONFIRMED（當成中繼說明的簡稱）：U11 自己把中繼說明描述成「做為網頁在 Google 搜尋結果中顯示的摘要」；旁白 tgmj 已說清楚是寫給搜尋引擎的摘要 | — |
| 41 | 「常見問題卻寫，只有美國大學生才符合資格」 | 9q5n | U4 | 200 | CHANGED：常見問題問「誰可以免付費使用學生方案？」，答「18 歲以上符合資格的美國大學生，可免付費使用 Google AI Plus 學生方案。」頁面沒有「只有」「才」；旁白說「卻寫」，就該是頁面寫的字。「只回答了美國大學生」的意思保留在一問一答的結構裡 | 「常見問題卻寫，只有美國大學生才符合資格。」→「常見問題問誰能免費用，答案寫的卻是美國大學生。」（reveal 不變） |
| 42 | 字卡「常見問題卻寫美國大學生才符合」 | page-contradictions.items[1] | U4 | 200 | CHANGED：「才」等於「只有」，同 #41 | 「常見問題卻寫美國大學生才符合」→「常見問題卻寫美國大學生可免費用」 |
| 43 | 「這一列最容易被誤判成也有更正」 | 898w | L1 | 檔案 | CHANGED：原教學只寫「若回答把時間也說成更改，應點回兩份來源確認都是下午兩點」，沒說時間是「最」容易誤判的一列；brief 也只寫「容易被誤判」 | 「這一列最容易被誤判成也有更正，…」→「這一列很容易被誤判成也有更正，…」 |
| 44 | 「接下來這張表，就是核對後的正確答案」 | hqj8 | L1 | 檔案 | CONFIRMED：六列的值都和公告甲／乙原文一致；這句沒有說出處是原教學 | — |
| 45 | 「先講清楚，這是原教學裡人工整理的驗收答案」 | dipd | L1 | 檔案 | 需要改，但照指示沒改（聽眾檢查的近重複句，歸統籌）：原教學的驗收答案只有日期、名額、截止日三欄，加上「時間都是下午兩點」的檢查，共四欄；地點、費用兩列是照原教學的公告原文整理的，值正確，但不是原教學的驗收答案。建議與 qjpw 合成一句：「這張表是照兩份公告原文人工整理的，不是今天真的問過模型。」 | 未改 |
| 46 | 「這個答案是原教學裡人工比對過的，不是今天真的問過模型」 | qjpw | L1 | 檔案 | 同 #45：「不是今天問過模型」成立（原教學「這是人依原文整理的驗收答案，不是模型測試結果」），「原教學裡人工比對過的」只對四欄成立；照指示沒改 | 未改 |
| 47 | 第一輪其餘懷疑：adye「從一句沒有講清楚」 | adye | L1 | 檔案 | OUT OF SCOPE：公告甲寫「場地尚未確認」，說「沒有講清楚是哪一間」大致成立，屬口語描述，不改 | — |
| 48 | 第一輪其餘懷疑：kgji「真正決定你能不能領，是另外四道關卡」 | kgji | U2 | 200 | OUT OF SCOPE：Google 保留最終認定權（「sole discretion」），已由 iyw2 講明；這句是章節引子 | — |
| 49 | 第一輪其餘懷疑：ik8j「比事後申訴退費輕鬆多了」 | ik8j | U6 | 200 | OUT OF SCOPE（觀點）：沒有承諾能退費；U6 條款小字「若在帳單週期屆滿前取消訂閱，剩餘時間恕不退費，除非適用法律另有規定」，和「事後申訴很麻煩」的意思一致 | — |

## 摘要

- 查核主張 49 條（第一輪改過的 20 列＝19 條事實、隨機抽樣 17 條、懷疑 12 條）：CONFIRMED 37、CHANGED 7、需要改但依指示留給統籌 2（dipd、qjpw）、OUT OF SCOPE 3、NOT FOUND 0。
- 落到 video.json 的修改：旁白 6 句（e4ju、a435、898w、9q5n、tgmj、yu5p，id 都沒變），字卡 1 格（page-contradictions.items[1]）。沒有數字變動，sources 不需要改（全部 checked_on 2026-09-25）。claims.md 新增 c22–c25，進度加一行。
- 第一輪 19 條改動：17 條今天仍成立；e4ju 與 a435 是第一輪改寫時留下的小問題，本輪已修。NT$165（U6 靜態 HTML）、「註冊時」付款方式（U2 英繁、U1、U4）、改名 Gemini Notebook（U9、U10）、測驗字卡是既有功能而九月再擴充（U7、U8）、公告甲乙與示範表（L1）都已確認。
- 隨機抽樣（種子 20260925）17 條全部 CONFIRMED。
- 會過期的事實：兌換期限 2026-12-31（條款 Last updated 2026-08-19）；U6 價格 NT$165／NT$650，同頁橫幅寫學生方案「優惠活動即將結束」；U4 三處說法今天仍在，錄製與上架前要再看一次；即時語音對話 U7「soon」、Ultra 本週、Pro 之後；新題型與互動式學習總覽寫「in the next few weeks」（U7 注腳 3、4），acc4 的「九月又替測驗、字卡加了新功能」靠的是 U8 的清單與已上線的「就測驗字卡向筆記本提問」。
- 觀點：本輪沒有碰觀點句；yu5p 第一輪歸為觀點，但它是事實句，已依來源加上「可能」。第一輪報告的 brief 衝突仍然成立，本輪沒有新的衝突；brief 大綱第 7 節寫「常見問題卻寫『美國大學生』」，和本輪 9q5n 的改法一致。
- 聽眾檢查（只回報）：本輪改的句子都在 40 字內（最長 tgmj 27 字，含標點），沒有括號、網址、查證口吻，沒有新的拉丁詞；reveal 位置不變。第一輪列的 iyph、938u、9m3b、tnez、2jya、qjpw／dipd、tigk／d4k5 照指示未動。
- lint：`node TOOL/tools/video/cli.mjs lint --file …/video.json` → 0 errors、1 warning（估計 12.8 分鐘，是已知的 250 字／分鐘估算，不處理）。
- 懷疑但沒改：字卡「搜尋摘要」保留為中繼說明的簡稱（#40）；Google 搜尋結果實際顯示哪段摘要沒有查，也查不到固定答案；U5 仍列在 sources，價格是空元件，但它是官方方案頁，留著無害；站外問題同第一輪：文章 ai-news-gemini-student-offer-20260820 圖一的 alt 寫「排成一列並以箭頭相連」，和 SVG 不符。
- 未了結：dipd、qjpw 的出處說法（#45、#46）要統籌改，建議句見上表；改完前這支稿不能算查核完畢。
- 需要第三輪嗎：照規則需要，本輪事實修改 7 處，超過三處。建議只做窄範圍覆核：本輪改的 7 格，加上統籌改完的 dipd／qjpw。
