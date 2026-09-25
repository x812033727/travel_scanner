# verify-1 — gemini-student-offer（第 1 輪查核，2026-09-25）

查核者：獨立查核代理（不是撰稿者）。對象：`_shelf/gemini-student-offer/gemini-student-offer/video.json`，外加 `claims.md`、`brief.md`（選項 A）。

方法：每個官方頁面都用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 重新抓取，同一主機間隔至少 1.5 秒，去掉 `<!-- -->`、script、style 後讀文字；請求裡沒有任何個人資料，沒有登入任何帳號。Web search 用了 0 次。原始頁面與文字檔在 `<VIDEO_WORKDIR>/gemini-student-offer/_tools/verify1/pages/`，抽出的清單在 `_tools/verify1/claims-list-before.md`（修改前）與 `claims-list-after.md`（修改後）。站內素材（`notebooklm-guide.json`、`diagram-1.svg`）直接讀 `<ROOT>` 的檔案。

網址代號（HTTP 皆為最終狀態）：

- U1 公告 https://blog.google/innovation-and-ai/products/gemini-app/student-offer-google-ai/ — 200（datePublished 2026-08-19T19:00Z）
- U2 優惠條款 https://one.google.com/offer/studentoffer8 — 200（英文，Last updated: August 19, 2026）；`?hl=zh-TW` — 200（繁中）
- U3 Google One 供應清單 https://support.google.com/googleone/answer/16548195?hl=zh-TW — 200（轉址到 hl=zh-Hant）
- U4 台灣學生頁 https://gemini.google/tw/students/?hl=zh-TW — 200
- U5 Google One 方案頁 https://one.google.com/intl/zh-TW_tw/about/google-ai-plans/ — 200（價格是空的 `<g1-localized-price>` 元件）
- U6 Gemini 台灣訂閱頁 https://gemini.google/tw/subscriptions/?hl=zh-TW — 200（靜態文字「每月 NT$ 165 元」）
- U7 讀書工具公告 https://blog.google/innovation-and-ai/products/gemini-notebook/new-study-tools-september-2026/ — 200（datePublished 2026-09-15T16:00Z）
- U8 Workspace 公告 https://workspaceupdates.googleblog.com/2026/09/new-back-to-school-features-and-learning-tools-available-in-Gemini-Notebook.html — 200（頁面日期 September 18, 2026）
- U9 改名公告 https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/ — 200（datePublished 2026-07-16T16:00Z）
- U10 Gemini Notebook 繁中說明 https://support.google.com/gemininotebook/answer/16206563?hl=zh-Hant — 200
- L1 `apps/api/app/guides/content/notebooklm-guide.json`（zh-TW，第一步、第二步）— 站內檔案
- L2 `apps/web/public/guides/ai-news-gemini-student-offer-20260820/diagram-1.svg` — 站內檔案

## 逐條表

| # | 主張 | 位置 | 網址 | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 公告注腳列七個排除地區：美國、玻利維亞、阿爾巴尼亞、加拿大、澳門、香港、突尼西亞，沒有台灣 | official-bullets.items[0]、8hpd、hbgv、nyb8 | U1 | 200 | CONFIRMED：注腳 3「except for in the U.S., Bolivia, Albania, Canada, Macau, Hong Kong, and Tunisia」 | — |
| 2 | 優惠條款另列六個排除地區，沒有美國、沒有台灣 | official-bullets.items[1]、z82n、7uv4、6k4q | U2 | 200 | CONFIRMED：「except for Bolivia, Albania, Canada, Hong Kong, Macau, and Tunisia」；繁中版同 | — |
| 3 | 條款少了美國，是因為美國學生走另一套方案 | aup8 | U1、U2 | 200 | CONFIRMED（推論與兩頁一致）：條款寫「The subscription plan included in your Offer depends on the country or region of your eligible higher education institution」，公告寫美國給 Google AI Pro；兩頁都沒明寫「因為」 | — |
| 4 | 公告與條款是兩份不同文件、各有一份排除名單 | gt38、z82n | U1、U2 | 200 | CONFIRMED | — |
| 5 | 三份文件都沒寫台灣不能領 | b2gs | U1、U2、U3 | 200 | CONFIRMED | — |
| 6 | 供應清單上找得到台灣 | official-bullets.items[2]、ytv8、hc9u 前後、bkd5 | U3 | 200 | CONFIRMED：清單今天 168 筆，台灣第 145 筆 | — |
| 7 | 供應清單看的是居住地 | k72y、2qfp | U3 | 200 | CONFIRMED：「您目前居住的國家/地區，必須支援 Google AI Plus 會員方案」 | — |
| 8 | 條款看的是就讀學校所在地 | 2qfp、awap、four-gates-steps.steps[0].detail、outro.lines[0] | U2 | 200 | CONFIRMED：「enrolled at a higher education institution in a country or region where the subscription plan … is supported」 | — |
| 9 | 兩份排除名單合起來七個：美國、加拿大、港澳，另外三個國家 | y5d9、i823、excluded-vs-supported.left.points | U1、U2 | 200 | CONFIRMED：條款六個都在公告七個之內；另外三個是玻利維亞、阿爾巴尼亞、突尼西亞 | — |
| 10 | 官方沒解釋為什麼排除 | 7p2h | U1、U2 | 200 | CONFIRMED（兩頁都沒寫原因） | — |
| 11 | 「這七個地區裡，唯獨沒有台灣」 | 5y8q | U1、U2 | 200 | CHANGED：「唯獨沒有台灣」字面是「七個裡只缺台灣」，不成立 | 「這七個地區裡，唯獨沒有台灣。」→「這七個地區裡，並沒有台灣。」 |
| 12 | 台灣排在瑞士之後、塔吉克之前 | excluded-vs-supported.right.points[1]、f7k9 | U3 | 200 | CONFIRMED | — |
| 13 | 香港、澳門、美國也在供應清單上，但被學生優惠排除 | b4f2、ijhv | U1、U2、U3 | 200 | CONFIRMED | — |
| 14 | 官方沒有一句說台灣可以 | qqrx、sxpz、t9mk、hqxf、k9nf、outro.title、excluded-vs-supported.verdict | U1–U4 | 200 | CONFIRMED：四頁都沒有「台灣學生符合資格」這類句子；U1 的「台灣」只出現在語系選單 | — |
| 15 | 最終資格由 Google 自己認定 | iyw2 | U2 | 200 | CONFIRMED：「Google reserves the right to determine eligibility in its sole discretion」 | — |
| 16 | 四關圖是官方公告自己畫的 | xd2e、c92q | L2 | 檔案 | CHANGED：SVG 印「© Mokaair 製圖 2026」，是站上文章的原創圖 | xd2e「這張圖，官方公告自己就畫了出來。」→「這張圖，是站上文章整理出來的。」；c92q「這是公告自己畫的圖，…」→「這是站上文章畫的圖，…」 |
| 17 | 四個方框排成一列、用箭頭連起來 | c92q、e4ju | L2 | 檔案 | CHANGED：SVG 是 2×2 四格、每格一行重點，沒有箭頭（撰稿者抄了文章 alt 文字，那段 alt 本身與 SVG 不符） | c92q「…四個方框排成一列。」→「…四個方框排成兩排。」；e4ju「四個方框排成一列，中間用箭頭連起來。」→「每個方框底下，都寫了一行這一關的重點。」 |
| 18 | 四關是身分、地區、帳號、期限 | four-gates-diagram.data.caption、g9j2、6yaa | L2 | 檔案 | CONFIRMED | — |
| 19 | 「地區已經過關」 | yaz7 | U1–U4 | 200 | CHANGED：沒有官方頁面說台灣過了地區這關；原句等於替觀眾判定資格 | 「地區已經過關，接下來三關才是真正的考驗。」→「地區先看到這裡，接下來三關才是真正的考驗。」 |
| 20 | 年滿 18 歲 | 2ivg、steps[0].detail、outro.lines[0] | U2 | 200 | CONFIRMED：「Be 18 years of age or older」 | — |
| 21 | 通過第三方驗證學生身分 | awap、dstq、steps[0].detail | U2 | 200 | CONFIRMED：「third-party verification service, SheerID」 | — |
| 22 | 官方文件沒寫要準備什麼資料、審核多久 | x8u5 | U1、U2、U4 | 200 | CONFIRMED：條款只寫「Google may request certain information for verification purposes」 | — |
| 23 | 個人 Google 帳戶 | f8th、steps[1].detail、outro.lines[1] | U2 | 200 | CONFIRMED | — |
| 24 | 優惠期間全程要綁有效付款方式 | 4xph、steps[1].detail | U2、U1、U4 | 200 | CHANGED：條款「with a qualifying form of payment at sign-up」（繁中「在訂閱時」），公告「required at sign-up」，台灣學生頁「註冊時必須提供」；沒有「全程」 | 4xph「優惠期間，這個帳戶全程要綁一張有效的付款方式。」→「註冊的時候，這個帳戶就要先綁好有效的付款方式。」；steps[1].detail「…全程要有付款方式」→「…註冊時要有付款方式」 |
| 25 | 綁一張自己的卡 | outro.lines[1] | U2 | 200 | CHANGED：條款只寫 qualifying form of payment，沒限定卡，也沒限定是本人的 | 「帳號：個人帳戶，綁一張自己的卡」→「帳號：個人帳戶，註冊時綁好付款方式」 |
| 26 | 家庭群組成員、企業採購者被排除 | tvip | U2 | 200 | CONFIRMED（條款列五種：family group、enterprise purchaser、Pixel bundle、third party/affiliate 如 Google Fi、supervised account） | — |
| 27 | 用學校配發帳號的人不符合 | 2k4m | U2 | 200 | CHANGED：條款是「not available on your school-issued Workspace for Education account」，限制帳號不是人 | 「透過學校配發帳號的人，也一樣不符合這項優惠。」→「學校配發的帳號，也一樣不能拿來兌換這項優惠。」 |
| 28 | 今年 12 月 31 日前兌換 | jve6、steps[2].detail、outro.lines[2]、diagram | U1、U2、U4 | 200 | CONFIRMED：「must be redeemed by December 31, 2026」；U4「兌換期限：2026年12月31日」 | — |
| 29 | 12 個月從兌換當天起算；兌換期限不是到期日 | zj9u、rxhm、nm7d、zijq、real-math-table.rows[0] | U2 | 200 | CONFIRMED：「12 month period from the day you redeem the Offer」 | — |
| 30 | 字卡「12月31日前兌換，之後才起算12個月」 | steps[2].detail | U2 | 200 | CHANGED：「之後」可讀成 12/31 之後才起算，與條款不符 | 「2026年12月31日前兌換，之後才起算12個月」→「2026年12月31日前兌換，兌換日起算12個月」 |
| 31 | 台灣學生頁頁尾寫每月 $165、沒標幣別、沒有新台幣字樣 | real-math-big.kicker/text/sub、f9az、mxkt、423c、iyph | U4 | 200 | CONFIRMED：「如未提前取消 Google AI Plus，試用期結束後，系統將自動收取每月 $165。」整頁 HTML 沒有「新台幣」「NT$」「TWD」 | — |
| 32 | 一般 Plus 方案台灣月費 NT$165；一年 NT$1,980、約兩千元 | real-math-big.sub、z2kk、kma3、vgjs | U6 | 200 | CONFIRMED：U6 靜態文字「Google AI Plus … 每月 NT$ 165 元」；165×12=1,980，「大約兩千」成立 | — |
| 33 | 一般方案月費頁面的數字是載入後才代入、今天讀不到 | fbh6 | U5、U6 | 200 | CHANGED：U5 確實是空元件，但 U6 今天就用靜態文字寫出 NT$165；原句也在講查證過程 | 「一般方案的月費頁面，數字是網頁載入後才代進去的，今天讀不到。」→「Gemini 的方案頁倒是寫明，一般的 Plus 方案每月新台幣一百六十五元。」；sources 新增 U6 |
| 34 | 沒提前取消就自動收標準月費 | d8ij、2jya、hnby、yttg、sr3p、weqg、real-math-table.rows[2] | U2 | 200 | CONFIRMED：「your form of payment will be automatically charged the standard monthly subscription price … until you cancel」（除非當地法律要求先徵得同意） | — |
| 35 | 期間內取消，會員資格「可能」維持到期滿，不是保證 | 9ttj | U2 英文、U2 繁中 | 200 | CHANGED：英文是「may remain active」，繁中條款卻寫「取消後仍可保有會員資格」；台灣觀眾打開繁中版會對不上，改成點明是英文條款 | 「官方的用詞是，…」→「英文條款的用詞是，…」 |
| 36 | 頁尾主打 Plus 方案 | page-contradictions.items[0]、ic7q | U4 | 200 | CONFIRMED | — |
| 37 | 頁尾這句是使用者實際會看到的收費依據 | hwep | U2、U4 | 200 | CHANGED：沒有來源支持；扣款依據是條款的「standard monthly subscription price … for your country」 | 「頁尾這句，是使用者實際會看到的收費依據。」→「頁尾這句，講的是試用期結束後怎麼收費。」 |
| 38 | 常見問題寫美國大學生才符合 | page-contradictions.items[1]、9q5n | U4 | 200 | CONFIRMED：問「誰可以免付費使用學生方案？」答「18 歲以上符合資格的美國大學生，可免付費使用 Google AI Plus 學生方案」；「只有」是轉述，見懷疑但沒改 | — |
| 39 | 英文公告寫美國以外的學生拿另一個方案 | unu4 | U1 | 200 | CONFIRMED：美國 Google AI Pro，美國以外 Google AI Plus | — |
| 40 | 搜尋摘要推 Google AI Pro | page-contradictions.items[2]、tgmj | U4 | 200 | CONFIRMED：meta description 與 og:description「立即訂閱 Google AI Pro 方案，享有更多 Gemini 功能！」 | — |
| 41 | Pro 比 Plus 貴 | page-contradictions.items[2]、tgmj | U6 | 200 | CONFIRMED：Pro 每月 NT$650、Plus 每月 NT$165 | — |
| 42 | 同一頁三處說法對不上 | hook.amsk、r7mx、47yj、3t34、7z8x | U4 | 200 | CONFIRMED | — |
| 43 | 企業端公告：滿 18 歲的使用者現在就能即時語音對話 | ikea | U8 | 200 | CONFIRMED：「Users 18 years or older can now have a real-time conversation with their notebooks」 | — |
| 44 | 消費端原文：你很快就可以 | wths | U7 | 200 | CONFIRMED：「You can soon have a real-time conversation…」，注腳「Rolling out to Google AI Ultra subscribers (18+) this week…」 | — |
| 45 | 兩份是同一批公告 | 93u7、y4ux | U7、U8 | 200 | CONFIRMED：U8 的 Rollout 寫「started on September 15, 2026」，與 U7 同一批開學工具 | — |
| 46 | NotebookLM 改名叫「Gemini 筆記本」 | 86i3 | U9、U10 | 200 | CHANGED：官方名稱是 Gemini Notebook，繁中說明中心也用英文原名，「筆記本」指單一筆記本（也和 Gemini App 的筆記本功能撞名）；詞典沒有 Notebook，暫不唸出全名 | 「這個工具原本叫 NotebookLM，現在改名叫 Gemini 筆記本。」→「這個工具原本叫 NotebookLM，現在改名，換上了 Gemini 的名字。」 |
| 47 | 改名日期 2026-07-16 | claims c14（旁白未講日期） | U9 | 200 | CONFIRMED | — |
| 48 | 改名後功能延續 | acc4 | U9 | 200 | CONFIRMED：「It's the same standalone product」 | — |
| 49 | 改名後「多了」測驗、字卡 | acc4 | U7、U1 | 200 | CHANGED：U7 把測驗、字卡當既有產出（studio outputs like … quizzes and flashcards；you can always customize…），U1（8 月）已寫「create flashcards, take a practice quiz」；9 月新增的是互動式學習總覽、新題型（即將）、可就已完成的測驗字卡提問 | 「改名之後功能延續，多了測驗、字卡跟短影片摘要。」→「改名之後功能延續，九月又替測驗、字卡加了新功能，還有短影片摘要。」 |
| 50 | 可做短影片摘要 | acc4 | U7、U8 | 200 | CONFIRMED：Short Video Overviews，約 60 秒、80 種以上語言 | — |
| 51 | 讀書工具公告 2026-09-15 | claims c13 | U7 | 200 | CONFIRMED | — |
| 52 | 示範用站上教學的兩份虛構公告 | ydf6、6bsa、byrd、demo-code.caption | L1 | 檔案 | CONFIRMED：「這些文字是本文編寫的練習素材，不是實際活動公告」 | — |
| 53 | 公告甲 9/1 初稿、公告乙 9/8 修正版、差一週 | fhzt、nr8m、demo-code.code | L1 | 檔案 | CONFIRMED | — |
| 54 | 公告甲：10/10 下午 2 點、約 20 人、場地與收費未定 | demo-code.code | L1 | 檔案 | CONFIRMED（原文「暫定…預估參加人數 20 人」，濃縮成「約20人」可接受） | — |
| 55 | 公告乙：10/11 下午 2 點、社區教室、免費、24 人、未給截止日 | demo-code.code | L1 | 檔案 | CONFIRMED | — |
| 56 | 提示詞：只根據甲乙、六個欄位、附引用、標出更正與未提供 | demo-code.code、heg3、6b4h、22ic | L1 | 檔案 | CONFIRMED（原文另有「使用繁體中文」「不要替活動推算報名截止日期」，字卡省略） | — |
| 57 | 表格是原教學人工核對的答案，不是今天問模型的輸出 | hqj8、qjpw、dipd | L1 | 檔案 | CONFIRMED：「這是人依原文整理的驗收答案，不是模型測試結果」；全片沒有一句說 AI 實際這樣回答 | — |
| 58 | 日期 10 日→11 日，已更正 | demo-table.rows[0]、pddy | L1 | 檔案 | CONFIRMED | — |
| 59 | 引用會清楚標出更正 | qiiv | L1 | 檔案 | CHANGED：原教學寫「若資料太短，工具可能引用整份來源而不是其中某一句」 | 「改一天而已，很容易被忽略，但引用會清楚標出來。」→「改一天而已，很容易被忽略，點開引用就能核對。」 |
| 60 | 時間兩份都是下午 2 點、沒變，是要抓的誤判 | demo-table.rows[1]、rdvu、898w、aucr | L1 | 檔案 | CONFIRMED：「若回答把時間也說成更改，應點回兩份來源確認都是下午兩點」 | — |
| 61 | 地點：未定→社區教室「已更正」 | demo-table.rows[2]、bbi7 | L1 | 檔案 | CHANGED：公告甲是「場地尚未確認」，不是被改掉的舊值；原教學的驗收答案也沒把地點列為更正 | rows[2]「社區教室，已更正」→「社區教室，新補上」；bbi7「地點從未定，改成社區教室，也是真的被更正。」→「地點從未定，到公告乙才補上社區教室。」 |
| 62 | 名額約 20→24，已更正 | demo-table.rows[3]、9ege | L1 | 檔案 | CONFIRMED：「名額從預估二十人改為二十四人」 | — |
| 63 | 費用：未定→免費「已更正」 | demo-table.rows[4]、rdqg | L1 | 檔案 | CHANGED：公告甲是「是否收費也尚未決定」；同 #61 | rows[4]「免費，已更正」→「免費，新補上」；rdqg「費用從未定，改成免費，一樣是更正過的。」→「費用從未定，到公告乙才寫明免費。」 |
| 64 | 「免費本來收費」 | a435 | L1 | 檔案 | CHANGED：公告甲沒說要收費 | 「免費本來收費，這種欄位最容易被使用者記錯。」→「未定不等於要收費，這種欄位最容易被記錯。」 |
| 65 | 截止日兩份都沒寫，AI 不該自己編 | demo-table.rows[5]、umgz、vaaq | L1 | 檔案 | CONFIRMED：「兩份都沒給出截止日期」「不要替活動推算報名截止日期」 | — |
| 66 | 有引用編號不代表內容一定對 | nmn8、8p2f | L1 | 檔案 | CONFIRMED：「引用…不代表每個結論自動正確」 | — |
| 67 | 不用登入帳號，在家也能跟著做一次 | 56f4 | L1、U10 | 200 | CHANGED：要在 Gemini Notebook 裡做這個練習得登入 Google 帳號（原教學「再登入自己的帳號」）；只有「這段示範」不需要登入 | 「不用真的登入帳號，你在家也能跟著做一次。」→「這段示範不用登入帳號，看完你也能自己做一次。」 |
| 68 | 片名「官方四關」 | youtube.title | L2、U2 | 200 | CHANGED：四道關卡是站上文章的整理框架，條款本身列的是五個條件，不是 Google 的「四關」 | 「…官方四關全解析」→「…四道關卡全解析」 |
| 69 | 說明欄有完整文章與四份官方文件連結 | eh8h、pdyi、youtube.description | 工具 composeDescription | — | CONFIRMED：描述會自動附上 source_guide 文章網址與 `sources`（含 U1–U4） | — |
| 70 | 站主觀點相關句與建議 | kma3、vcp3、zxjt、umse、abrn、ik8j、tigk、d4k5、g4zn、5bdj、yu5p、real-math-table 第三欄 | — | — | OUT OF SCOPE（觀點，與站主觀點一致） | — |
| 71 | 縮圖、tags | thumbnail.data、youtube.tags | U1、U7、U9 | 200 | OUT OF SCOPE（產品名稱都正確） | — |

## 摘要

- 查核主張 71 條：CONFIRMED 50、CHANGED 19、NOT FOUND 0、OUT OF SCOPE 2。落到 video.json 的修改：旁白 17 句（id 都沒變）、字卡 5 格（steps 兩格、demo-table 兩格、outro 一行）、片名 1 處、sources 新增 U6。claims.md 改寫 c9，補 c15 註記，新增 c16–c21。
- NT$165：今天確認的官方靜態文字在 U6「Google AI Plus … 每月 NT$ 165 元」（Pro「每月 NT$ 650 元」）。U5 的價格仍是空的前端元件。U4 頁尾只寫「每月 $165」、沒有幣別。
- 資格：18 歲以上、SheerID、個人帳戶、「註冊時」要有付款方式（不是全程）、自動續扣、2026-12-31 前兌換都已確認。七個排除地區（公告）與六個（條款）也已確認。沒有任何一句承諾台灣學生符合資格；只有 yaz7 原句「地區已經過關」有這個問題，已經改掉。
- 會過期的事實：兌換期限 2026-12-31（條款 Last updated 2026-08-19）；NT$165／NT$650（U6，2026-09-25，同頁橫幅寫學生方案「優惠活動即將結束」）；台灣學生頁三處矛盾（2026-09-25 仍在，Google 隨時可能修，錄製與上架前再看一次 U4）；即時語音對話「很快」對「現在」（9/15 與 9/18），推到 Pro 之後這組對比就會過時；新題型與互動式學習總覽寫的是「未來幾週」；供應清單 168 筆、台灣第 145 筆（旁白沒用）。
- 與 brief 衝突（以官方為準，請站主決定）：①「會過期的事實」表寫「優惠期間全程要有一個有效付款方式」，官方是 at sign-up；② 站主觀點「所有人都得綁一張自己的卡」：條款只寫付款方式，沒限定卡，outro 已改；③ brief 說 NT$165 今天讀不到，U6 讀得到；④ 觀眾段把「測驗、字卡、短影片摘要」當成新工具，U7 把測驗、字卡當既有功能；⑤ 四關圖是 Mokaair 畫的，brief 寫得對，是撰稿時誤寫成公告畫的。
- 觀點：標成觀點的句子都和站主觀點一致。vcp3、zxjt 沒有標成觀點，但內容和站主觀點一致。
- 聽眾檢查（只回報）：講查證過程的句子有 iyph「靜態文字」、938u、9m3b、tnez「來自另一篇查證」、2jya，都不在 lint 的清單裡；沒有超過 40 字的句子，旁白裡沒有括號或網址；每個 reveal 都和介紹它的句子同句或在後面；qjpw 與 dipd、tigk 與 d4k5 幾乎重複。
- 詞典：lint 沒有抓到未收錄的拉丁詞。86i3 想唸出官方全名「Gemini Notebook」，要先在 shelf 的 lexicon.json 加 `"Notebook"`（聽過後填 null）；查核代理不能改詞典，所以先用不唸全名的寫法。
- lint：`node TOOL/tools/video/cli.mjs lint --file …/video.json` → 0 errors、1 warning（估計 12.7 分鐘，這是已知的 250 字／分鐘估算，不處理）。
- 懷疑但沒改：「搜尋摘要」實際上是頁面的 meta description，Google 搜尋結果是否真的顯示這段沒有查；9q5n 的「只有」是轉述；898w「最容易被誤判」原教學沒說「最」；dipd、hqj8 說整張表都是原教學答案，但原教學只涵蓋日期、名額、截止日、時間四欄，地點與費用是直接讀原文；adye「一句沒有講清楚」（公告甲其實明寫尚未確認）；kgji「真正決定你能不能領」，實際上 Google 保留最終認定權，由 outro 的 iyw2 補上；ik8j 暗示可以申訴退費，沒有查；U5 仍列在 sources。站外問題：文章 ai-news-gemini-student-offer-20260820 圖一的 alt 文字寫「排成一列並以箭頭相連、最後一格虛線」，和 SVG 不符，要修文章（不在本輪可寫範圍）。
- 需要第二輪嗎：需要。本輪事實修改超過三處（19 條）。
