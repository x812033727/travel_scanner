# claims — gemini-student-offer

一行一個可查核的主張。查證日期一律 2026-09-25（今天，撰稿代理親自重新打開每個官方頁面）。

c1｜公告注腳排除地區為美國、玻利維亞、阿爾巴尼亞、加拿大、澳門、香港、突尼西亞（共 7 個，不含台灣）｜https://blog.google/innovation-and-ai/products/gemini-app/student-offer-google-ai/｜2026-09-25｜official-bullets, excluded-vs-supported

c2｜優惠條款另立一份排除清單：玻利維亞、阿爾巴尼亞、加拿大、香港、澳門、突尼西亞（共 6 個，不含美國與台灣）｜https://one.google.com/offer/studentoffer8｜2026-09-25｜official-bullets

c3｜Google One 說明頁「目前支援 Google AI Plus 的國家/地區」清單列有台灣，排在瑞士之後、塔吉克之前｜https://support.google.com/googleone/answer/16548195?hl=zh-TW｜2026-09-25｜official-bullets, excluded-vs-supported

c4｜優惠條款五項資格：18 歲以上；就讀方案有支援地區的高等教育機構；以第三方服務 SheerID 驗證學生身分；持個人 Google 帳戶；註冊時 Google Payments 已有可用的付款方式｜https://one.google.com/offer/studentoffer8｜2026-09-25｜four-gates-steps

c5｜兌換期限為 2026 年 12 月 31 日；優惠期是「從兌換當日起算的 12 個月」（The Offer Period 定義為 the 12-month period from the day you redeem the Offer）｜https://one.google.com/offer/studentoffer8｜2026-09-25｜four-gates-steps

c6｜到期未取消，除非適用法律另要求同意，系統會自動以綁定的付款方式收取所在國家的標準月費（原文：your form of payment will be automatically charged the standard monthly subscription price ... until you cancel）｜https://one.google.com/offer/studentoffer8｜2026-09-25｜real-math-table, my-approach-bullets

c7｜此優惠不適用於學校配發的 Workspace for Education 帳戶（原文：This offer is not available on your school-issued Workspace for Education account）｜https://one.google.com/offer/studentoffer8｜2026-09-25｜my-approach-bullets

c8｜台灣學生頁頁尾寫「兌換期限：2026年12月31日。註冊時必須提供有效的付款方式。如未提前取消 Google AI Plus，試用期結束後，系統將自動收取每月 $165。可隨時取消。」未標示幣別｜https://gemini.google/tw/students/?hl=zh-TW｜2026-09-25｜real-math-big

c9｜一般方案（非學生優惠）Google AI Plus 台灣月費 NT$165：Gemini 台灣訂閱頁的靜態文字寫「Google AI Plus … 每月 NT$ 165 元 … 400 GB」（同頁 Google AI Pro「每月 NT$ 650 元」），查核代理 2026-09-25 以 curl 讀到；one.google.com 的方案頁仍用 `<g1-localized-price variant="PRICE_GEN_AI_PLUS_MONTHLY" country="TW">` 前端元件、靜態 HTML 裡沒有數字。NT$165 × 12 = NT$1,980｜https://gemini.google/tw/subscriptions/?hl=zh-TW（另見 https://one.google.com/intl/zh-TW_tw/about/google-ai-plans/）｜2026-09-25｜real-math-big（fbh6）

c10｜台灣學生頁常見問題寫「18 歲以上符合資格的美國大學生，可免付費使用 Google AI Plus 學生方案」，還加了一句「每年都必須驗證資格，才能繼續使用」｜https://gemini.google/tw/students/?hl=zh-TW｜2026-09-25｜page-contradictions

c11｜台灣學生頁 `<meta name="description">` 與 `og:description` 都寫「立即訂閱 Google AI Pro 方案，享有更多 Gemini 功能！」，與頁尾主打的 Plus 方案不同｜https://gemini.google/tw/students/?hl=zh-TW｜2026-09-25｜page-contradictions

c12｜Gemini Notebook 企業端公告（9/18）原文：「Users 18 years or older can now have a real-time conversation with their notebooks ... in nearly 100 languages.」｜https://workspaceupdates.googleblog.com/2026/09/new-back-to-school-features-and-learning-tools-available-in-Gemini-Notebook.html｜2026-09-25｜my-approach-bullets

c13｜Gemini Notebook 消費端公告（9/15）註腳原文：「Rolling out to Google AI Ultra subscribers (18+) this week and coming to Google AI Pro and others soon.」，同一項「即時語音對話」兩份官方公告寫法不同｜https://blog.google/innovation-and-ai/products/gemini-notebook/new-study-tools-september-2026/｜2026-09-25｜my-approach-bullets

c14｜NotebookLM 於 2026 年 7 月 16 日公告改名為 Gemini Notebook（頁面結構化資料 datePublished: 2026-07-16）｜https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/｜2026-09-25｜demo-code

c15｜公告甲／公告乙的練習文字與驗收答案，取自站上既有教學 notebooklm-guide 第一步、第二步；驗收答案是原教學裡「人依原文整理的答案」，不是本片今天向 Gemini Notebook 實際提問得到的模型輸出，旁白與字卡一律講成「核對後的答案」｜apps/api/app/guides/content/notebooklm-guide.json（站內既有教學文章，不是官方頁面，故不列官方網址）｜2026-09-25｜demo-code, demo-table
  - 查核第一輪對照原文：公告甲「暫定 10 月 10 日下午 2 點、預估 20 人、場地尚未確認、是否收費尚未決定」；公告乙「10 月 11 日下午 2 點、社區教室、免費、名額 24 人、未提供報名截止日期」。原教學的驗收答案只寫「日期 10→11、名額 20→24、兩份都沒給截止日期、時間兩份都是下午兩點」。地點與費用在公告甲是「尚未確認／尚未決定」，不是被改掉的舊值，所以表格改標「新補上」，旁白 bbi7、rdqg 同步；a435 原句「免費本來收費」與原文不符（公告甲沒說要收費），已改。qiiv 原句「引用會清楚標出來」與原教學「資料太短時工具可能引用整份來源」不合，已改成「點開引用就能核對」。

c16｜四道關卡圖（diagram-1.svg）是 Mokaair 自己畫的（圖上印「© Mokaair 製圖 2026」），不是 Google 公告畫的；版面是 2×2 四個方框、每格一行重點，沒有箭頭，也不是排成一列（文章的 alt 文字寫「排成一列並以箭頭相連」，與 SVG 本身不符）｜apps/web/public/guides/ai-news-gemini-student-offer-20260820/diagram-1.svg｜2026-09-25｜four-gates-chapter（xd2e）, four-gates-diagram（c92q, e4ju）, youtube.title

c17｜NotebookLM 的新名字，Google 繁中說明中心寫的是英文「Gemini Notebook」（例：「在 Gemini Notebook 建立筆記本」），「筆記本」只指單一筆記本；旁白原本說「改名叫 Gemini 筆記本」不是官方名稱，且容易和 Gemini App 裡的「筆記本」功能混淆｜https://support.google.com/gemininotebook/answer/16206563?hl=zh-Hant｜2026-09-25｜demo-code（86i3）

c18｜9 月 15 日的讀書工具公告：測驗與字卡原本就是既有的產出（原文 studio outputs like infographics, quizzes and flashcards；you can always customize your quizzes and flashcards），這次新增的是互動式學習總覽、即將加入的新測驗題型（short answer, multiple select, fill in the blank）、可就已完成的測驗與字卡向筆記本提問，以及約 60 秒的 Short Video Overviews（80 種以上語言）；改名公告寫「It's the same standalone product」｜https://blog.google/innovation-and-ai/products/gemini-notebook/new-study-tools-september-2026/、https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/｜2026-09-25｜demo-code（acc4）

c19｜付款方式是「註冊時」的條件：條款英文 Have a Google Payments account with a qualifying form of payment at sign-up；繁中「在訂閱時具備符合資格的付款方式」；公告注腳 Valid form of payment required at sign-up；台灣學生頁「註冊時必須提供有效的付款方式」。沒有任何一頁寫「優惠期間全程」，也沒有限定是信用卡｜https://one.google.com/offer/studentoffer8｜2026-09-25｜four-gates-steps（steps[1].detail, 4xph）, outro（lines[1]）

c20｜期間內取消：英文條款 your membership may remain active until the end of the Offer Period；繁中條款卻寫「取消後仍可保有會員資格，直到優惠期結束」（沒有「可能」）。旁白 9ttj 講「可能、不是保證」依的是英文版，已改成「英文條款的用詞是」｜https://one.google.com/offer/studentoffer8、https://one.google.com/offer/studentoffer8?hl=zh-TW｜2026-09-25｜real-math-table（9ttj）

c21｜學校配發帳號：條款 This offer is not available on your school-issued Workspace for Education account，限制的是帳號，不是人；有學校帳號的學生仍可用個人帳戶申請。2k4m 已改成「學校配發的帳號，也一樣不能拿來兌換」｜https://one.google.com/offer/studentoffer8｜2026-09-25｜four-gates-steps（2k4m）

c22｜（查核第二輪）台灣學生頁常見問題原文是一問一答：問「誰可以免付費使用學生方案？」，答「18 歲以上符合資格的美國大學生，可免付費使用 Google AI Plus 學生方案。」頁面沒有「只有」「才」這類字。9q5n 原句「常見問題卻寫，只有美國大學生才符合資格」把推論當成原文，改成「常見問題問誰能免費用，答案寫的卻是美國大學生」；字卡 page-contradictions.items[1]「常見問題卻寫美國大學生才符合」改成「常見問題卻寫美國大學生可免費用」｜https://gemini.google/tw/students/?hl=zh-TW｜2026-09-25｜page-contradictions（9q5n, items[1]）

c23｜（查核第二輪）「立即訂閱 Google AI Pro 方案」這句在台灣學生頁的 `<meta name="description">`（Google 稱為「中繼說明」）與 og:description。Google 搜尋中心說明：摘要「主要會使用網頁上的內容」自動決定，中繼說明只是「也會」使用，且同一網頁可能依搜尋顯示不同摘要。所以不能說搜尋結果一定顯示這句：tgmj 改成「網頁寫給搜尋引擎的摘要，又叫你去訂閱…」，yu5p「通常是最多人第一眼看到的文字」改成「可能就是你在搜尋結果裡第一眼看到的文字」。字卡「搜尋摘要」當成中繼說明的簡稱保留（Google 自己的說明頁把中繼說明寫成「做為網頁在 Google 搜尋結果中顯示的摘要」）｜https://gemini.google/tw/students/?hl=zh-TW、https://developers.google.com/search/docs/appearance/snippet?hl=zh-tw｜2026-09-25｜page-contradictions（tgmj, yu5p）

c24｜（查核第二輪）示範表六欄的出處：原教學的驗收答案只寫日期 10→11、名額 20→24、兩份都沒給截止日，並提醒「若回答把時間也說成更改，應點回兩份來源確認都是下午兩點」，共四欄；地點與費用兩欄是照原教學的公告甲／乙原文直接整理的，數值都對。hqj8「核對後的正確答案」沒有說出處，成立；dipd「這是原教學裡人工整理的驗收答案」與 qjpw「這個答案是原教學裡人工比對過的」把六欄都算成原教學的答案，只有四欄成立。這兩句在聽眾檢查的近重複清單上，由統籌處理，第二輪沒改，建議的說法寫在 verify-2.md。原教學沒有說時間欄「最」容易誤判，也沒有說費用欄「最」容易記錯：898w、a435 的「最容易」改成「很容易」。（第三輪補記：統籌在聽眾檢查時刪了 dipd，qjpw 改成「這張表是照兩份公告原文人工整理的…」；第三輪再拿掉「人工」，見 c26）｜apps/api/app/guides/content/notebooklm-guide.json（第一步、第二步）｜2026-09-25｜demo-code（hqj8）, demo-table（qjpw, 898w, a435）

c25｜（查核第二輪）diagram-1.svg 每個方框裡是一行大字（關卡名）加一行小字（重點），小字在方框之內、不在方框下面；e4ju「每個方框底下」改成「每個方框裡」｜apps/web/public/guides/ai-news-gemini-student-offer-20260820/diagram-1.svg｜2026-09-25｜four-gates-diagram（e4ju）

c26｜（查核第三輪）統籌改寫的三句：iyph「台灣學生頁上寫的，是每月一百六十五元」對得上學生頁頁尾「系統將自動收取每月 $165」（沒有幣別，畫面同時顯示「$165／沒標幣別」，前面 mxkt、423c 已講沒有幣別）；2jya「這是寫在優惠條款裡的規定」對得上優惠條款 Recurring billing & cancellations 一節（繁中「週期性帳單和取消訂閱」）；qjpw 的六欄數值都能在公告甲／乙原文逐字找到，「不是今天真的問過模型」與 c15 一致，但「人工整理」只有原教學那四欄有出處（原教學自稱「人依原文整理」），地點、費用兩欄沒有任何來源說是人工整理的，這支稿的表格也是自動產線寫的，所以拿掉「人工」：「這張表是照兩份公告原文整理的，不是今天真的問過模型。」｜https://gemini.google/tw/students/?hl=zh-TW、https://one.google.com/offer/studentoffer8、apps/api/app/guides/content/notebooklm-guide.json｜2026-09-25｜real-math-big（iyph, 2jya）, demo-table（qjpw）

## 與企劃不同的地方

- 大綱把section 5「實算」與 section 7「同一頁自己都講不清楚」都沒有標 `chapter`，本稿照原樣沒加，兩節分別併入「要過四道關卡」與「示範：AI 筆記會不會抄錯」兩個 YouTube 章節。
- outro 場景額外補了 `"chapter": "結論"`（大綱沒寫，但試作片 `ai-model-choice` 的 outro 也開了「結論」章節）；純粹是多一個章節標記，不影響任何口播或字卡內容，也讓最後一段在說明欄的章節清單裡看得出來。
- 大綱的 compare 場景左側列了完整 7 個排除地區；`compare` 版型每側最多 5 點，故濃縮成「美國、加拿大、港澳、另外三個國家」四點，口播裡仍講出「加起來一共七個」，數字沒有省略。
- 大綱沒有指定 `four-gates-steps` 的三個 detail 文字，本稿依 `會過期的事實` 表與官方條款頁原文自己濃縮寫成；`SheerID`、`Workspace for Education` 這兩個官方名詞只放在字卡的 `data`（不需要發音字典），口播一律講中文意思，避免要额外處理這兩個生字的唸法。

## 我懷疑但沒動的事

- Google One 供應清單「共 168 筆、台灣第 145 筆」是來源文章 2026-09-23 的計數結果；本片今天只核對了「台灣列在清單上、排在瑞士之後塔吉克之前」這件事本身，沒有重新逐筆數過 168 這個總數，所以口播和字卡都沒有講出 168 這個數字，只在 `docs/videos` 這份 claims 裡留給查核代理核對用。
- （查核第一輪補記）2026-09-25 查核代理重新清點：清單仍是 168 筆，台灣第 145 筆，前後為瑞士、塔吉克；旁白與字卡仍不講總數。
- （查核第一輪補記）NT$165 已找到今天可讀的官方靜態文字：gemini.google/tw/subscriptions 寫「每月 NT$ 165 元」，見 c9；fbh6 已改為引用這一頁。以下是撰稿時的原始說明。
- 一般方案 NT$165／月這個數字，今天用純文字擷取工具重新打開 `one.google.com/intl/zh-TW_tw/about/google-ai-plans/` 仍然讀不到渲染後的價格（`<g1-localized-price>` 元件沒有文字內容），和 brief 描述的限制一致；`real-math-big` 場景改用台灣學生頁頁尾「每月 $165」這個直接寫在靜態文字裡、今天可以確認的數字，字卡仍標「以官網為準」，因為頁面本身沒有標示幣別，也沒有第二個獨立來源可以核對「等於 NT$165」這件事。
- 即時語音對話「現在可以」vs「你很快就可以」這兩句官方原文，是英文公告；查證時我自己重新打開兩個網址確認了原句，但字卡與口播用的是中文轉述，沒有逐字翻譯，怕逐字翻譯的句子唸起來太長太繞口；如果查核代理覺得需要更貼近逐字翻譯，claims c12／c13 已經附上英文原句可以核對。

## 進度

- video.json：16 個場景、156 句旁白，`lint --file` 跑過，0 errors、1 warning（估計 12.7 分鐘，是 lint 內建每分鐘 250 字的已知低估；換算撰稿代理實測的每分鐘 360 字，約 9.1 分鐘，落在 8–12 分鐘目標內，warning 屬預期內、不用改）。
- claims.md：15 個可查核主張，全部標今天日期，全部今天重新打開官方頁面確認；c15 例外標明是站內既有教學，不是官方頁面。
- 尚未做：查核代理覆核（下一階段）、試聽、成片。
- （查核第二輪，2026-09-25）第一輪改的 19 條全部重查、另抽 17 條第一輪確認過的（種子 20260925），結果見 verify-2.md；本輪新增 c22–c25。dipd／qjpw 的出處說法仍待統籌改。
- （查核第三輪，2026-09-25）窄範圍覆核：第二輪改的 7 格與統籌的聽眾檢查改寫（iyph、2jya、qjpw、938u、9m3b，刪 dipd、tnez、d4k5），結果見 verify-3.md；qjpw 拿掉「人工」，新增 c26；c24 的位置欄拿掉已刪的 dipd。
