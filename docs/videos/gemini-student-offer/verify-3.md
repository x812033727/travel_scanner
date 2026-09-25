# verify-3 — gemini-student-offer（第 3 輪查核，窄範圍，2026-09-25）

查核者：第三位獨立查核代理（不是撰稿者，也不是第一、二輪的查核者）。對象：`_shelf/gemini-student-offer/gemini-student-offer/video.json`，外加 `claims.md`、`brief.md`、`verify-1.md`、`verify-2.md`。

範圍（照統籌指示，只查這些）：① 第二輪改過的 7 格：e4ju、a435、tgmj、yu5p、9q5n 與字卡 page-contradictions.items[1]、898w；② 統籌聽眾檢查的改寫：iyph、2jya、qjpw，938u 與 9m3b 只看能不能順接下一句，以及刪掉的 dipd、tnez、d4k5 有沒有東西還指著它們。

方法：官方頁面今天重新抓，`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔至少 1.5 秒，去掉 `<!-- -->`、script、style 後讀文字；請求裡沒有個人資料，沒有登入任何帳號。Web search 0 次。頁面與文字檔在 `<VIDEO_WORKDIR>/gemini-student-offer/_tools/verify3/pages/`；聽眾檢查前後的差異由 `_tools/verify3/diff_listener.py` 對 `_tools/video.before-listener.json` 比出來（`diff-listener.md`），確認統籌只動了 iyph、2jya、qjpw、938u、9m3b 五句並刪了 dipd、tnez、d4k5，字卡、sources、youtube、thumbnail 都沒動。站內素材直接讀 `<ROOT>` 的檔案。

網址代號（HTTP 皆為跟隨轉址後的最終狀態，2026-09-25 抓取）：

- U2 優惠條款 https://one.google.com/offer/studentoffer8 — 200（Last updated: August 19, 2026）；`?hl=zh-TW` — 200（上次更新日期：2026年8月19日）
- U4 台灣學生頁 https://gemini.google/tw/students/?hl=zh-TW — 200
- U6 Gemini 台灣訂閱頁 https://gemini.google/tw/subscriptions/?hl=zh-TW — 200
- U11 Google 搜尋中心〈如何撰寫中繼說明〉https://developers.google.com/search/docs/appearance/snippet?hl=zh-tw — 200（英文 `?hl=en` — 200）
- L1 `apps/api/app/guides/content/notebooklm-guide.json`（zh-TW blocks[8]–[14]）— 站內檔案
- L2 `apps/web/public/guides/ai-news-gemini-student-offer-20260820/diagram-1.svg` — 站內檔案

## 主張表

| # | 主張 | 位置 | 網址 | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 「每個方框裡，都寫了一行這一關的重點。」 | e4ju | L2 | 檔案 | CONFIRMED：四個 rect（110,180）（850,180）（110,500）（850,500），各 640×245；32px 灰字「年滿 18 歲的大專生」「台灣在供應名單上」「個人帳號並綁付款」「12 月 31 日前兌換」在 y=348／668，落在方框範圍 180–425／500–745 之內，x 也在框內 | — |
| 2 | 「未定不等於要收費，這種欄位很容易被記錯。」 | a435 | L1 | 檔案 | CONFIRMED：公告甲「是否收費也尚未決定」，沒說要收費；原教學提醒「對數字、否定詞和條件要多看前後句，例如『未提供日期』不能簡化成『沒有截止期限』」，支持「容易記錯」這個提醒；已沒有「最」 | — |
| 3 | 「網頁寫給搜尋引擎的摘要，又叫你去訂閱另一個更貴的方案。」 | tgmj | U4、U11、U6 | 200 | CONFIRMED：U4 的 `meta name="description"`（og:description、twitter:description 相同）今天仍是「…立即訂閱 Google AI Pro 方案，享有更多 Gemini 功能！」；U11「由於中繼說明不會顯示在使用者看到的網頁上」「Google 有時候會使用網頁的 <meta name="description"> 標記來產生搜尋結果摘要」，所以「寫給搜尋引擎的摘要」成立；頁尾主打 Plus，「另一個」成立；U6 Pro 每月 NT$650、Plus 每月 NT$165，「更貴」成立 | — |
| 4 | 「這段摘要，可能就是你在搜尋結果裡第一眼看到的文字。」 | yu5p | U11 | 200 | CONFIRMED：U11「有時候會使用」中繼說明、「可能會根據不同筆搜尋，為同一個網頁顯示不同摘要」（英文 "Google sometimes uses…"、"might show different snippets for different searches"），句子已用「可能」。小註：搜尋結果裡標題那一行在摘要上面；「第一眼」照口語理解成「點進網頁之前看到的」，不算錯，沒改 | — |
| 5 | 字卡「搜尋摘要又推另一個更貴的方案」 | page-contradictions.items[2] | U4、U11、U6 | 200 | CONFIRMED：第二輪保留為中繼說明的簡稱；U11 自己的中繼說明就寫「做為網頁在 Google 搜尋結果中顯示的摘要」 | — |
| 6 | 「常見問題問誰能免費用，答案寫的卻是美國大學生。」 | 9q5n | U4 | 200 | CONFIRMED：問「誰可以免付費使用學生方案？」，答「18 歲以上符合資格的美國大學生，可免付費使用 Google AI Plus 學生方案。…」；旁白沒有「只有」「才」 | — |
| 7 | 字卡「常見問題卻寫美國大學生可免費用」 | page-contradictions.items[1] | U4 | 200 | CONFIRMED：同 #6，「可免付費使用」照原文 | — |
| 8 | 「這一列很容易被誤判成也有更正，這才是要抓的錯。」 | 898w | L1 | 檔案 | CONFIRMED：原教學特地點名這個錯：「若回答把時間也說成更改，應點回兩份來源確認都是下午兩點」；公告乙把時間寫在「日期改為 2026 年 10 月 11 日下午 2 點」這個「改為」句裡，也說得通為什麼容易被當成一起改了；已沒有「最」 | — |
| 9 | 「台灣學生頁上寫的，是每月一百六十五元。」 | iyph | U4 | 200 | CONFIRMED：頁尾「如未提前取消 Google AI Plus，試用期結束後，系統將自動收取每月 $165」。「$165」唸成「一百六十五元」，和 mxkt、ic7q 的唸法相同；「元」沒有指定幣別，前面 mxkt、423c 已講「沒有標示幣別」，說這句時畫面也顯示「$165／沒標幣別」；下一句 fbh6「方案頁倒是寫明…新台幣」的對比仍成立 | — |
| 10 | 「這是寫在優惠條款裡的規定。」（接在 d8ij「沒提前取消，就自動收費」之後） | 2jya | U2、U2 繁中 | 200 | CONFIRMED：優惠條款〈Recurring billing & cancellations〉「your form of payment will be automatically charged the standard monthly subscription price … To avoid being charged …, you must cancel before the end of the Offer Period」；繁中〈週期性帳單和取消訂閱〉「系統會…自動透過您設定的付款方式按月收費…請務必在優惠期結束前取消訂閱」。U2 的標題就是「Student Offer Terms／學生優惠條款」 | — |
| 11 | 「這張表是照兩份公告原文人工整理的，不是今天真的問過模型。」 | qjpw | L1 | 檔案 | CHANGED：六欄的值都能在原文找到：日期 10/10→10/11、時間兩份都是下午 2 點、地點「場地尚未確認」→「社區教室」、名額「預估 20 人」→「名額改為 24 人」、費用「是否收費也尚未決定」→「免費參加」、截止日兩份都沒有（乙「目前未提供報名截止日期」）；「不是今天真的問過模型」與 c15、brief 一致。但「人工整理」只有原教學那四欄有出處（原教學：「這是人依原文整理的驗收答案」，涵蓋日期、名額、截止日與時間檢查）；地點、費用兩欄沒有任何來源說是人工整理的，而這支稿的表格是自動產線寫的。這正是第二輪對「原教學」的同一個四欄對六欄問題，所以拿掉「人工」這個沒有出處的修飾，其餘不動 | 「…原文人工整理的，…」→「這張表是照兩份公告原文整理的，不是今天真的問過模型。」 |
| 12 | 「說結論之前，先講一件我注意到的事。」→ 67z6「這件事跟今天的示範，其實是同一個道理。」 | 938u | — | — | 順接 OK：「一件…事」由下一句的「這件事」接住；沒有事實主張。遠距離的問題見摘要的聽眾檢查 | — |
| 13 | 「第三件事，跟 AI 筆記有關。」→ 93u7「同一批公告裡，Google 自己對即時語音對話，寫了兩種答案。」 | 9m3b | — | — | 順接 OK：即時語音對話是 Gemini Notebook 的功能（第二輪今天抓的 U7「a real-time conversation with your notebooks」、U8「a real-time conversation with their notebooks」），和「AI 筆記」接得上；第三件事的 reveal 在 62qa，介紹在前、reveal 在後，順序正確 | — |
| 14 | 刪掉的 dipd、tnez、d4k5 | video.json、claims.md、brief.md、lexicon.json、approvals.json | — | 檔案 | video.json 裡沒有任何句子、字卡或 claims 陣列指著它們；三句都沒有 reveal，刪掉不影響字卡出現時機；前後句順接：hqj8→qjpw→pddy、9m3b→93u7、tigk→62qa。claims.md c24 的位置欄還列著 dipd，已拿掉並補記；brief.md、lexicon.json、approvals.json 沒有這三個 id。verify-1.md、verify-2.md 是歷史報告，照原樣留著 | c24 位置欄「demo-table（dipd, qjpw, 898w, a435）」→「demo-table（qjpw, 898w, a435）」 |

## 摘要

- 查核 14 列：第二輪改過的 7 格全部重查，加上字卡 items[2]；統籌改寫的 iyph、2jya、qjpw；938u、9m3b 的順接；刪掉的三句。CONFIRMED 10、CHANGED 1（qjpw，拿掉「人工」）、順接 OK 2、claims.md 整理 1、NOT FOUND 0。沒有數字變動，sources 不用改（全部 checked_on 2026-09-25）。
- 落到 video.json 的修改只有一句：qjpw「這張表是照兩份公告原文整理的，不是今天真的問過模型。」（id 不變，26 字）。claims.md：新增 c26，c24 位置欄拿掉 dipd，進度加一行。
- 第二輪的 7 格今天都成立：e4ju 的小字確實在方框裡；a435、898w 的「很容易」有原教學的提醒撐著；tgmj、yu5p 對得上 U4 的中繼說明與 U11 的說明；9q5n 和字卡照原文，沒有「只有」。
- 會過期的事實：U4 的頁尾「每月 $165」、常見問題「美國大學生」、中繼說明「立即訂閱 Google AI Pro」今天仍在，錄製與上架前要再看一次；優惠條款 Last updated 2026-08-19，兌換期限 2026-12-31；U6 價格 NT$165／NT$650。
- 觀點：本輪沒碰觀點句，沒有新的衝突。
- 聽眾檢查（只回報）：
  - 938u 說「說結論之前，先講一件我注意到的事」，但接下來的場景先講 kma3「我的看法是…」和第一、二件事，這件事到 93u7 才出現。原本 9m3b 用「我查證時發現一件事」回扣 938u，tnez 也銜接；兩處拿掉後，聽眾不一定會把 93u7 和 938u 的預告連起來。可以考慮讓 9m3b 回扣一下，例如「第三件事，就是我剛才說注意到的那件事」，要不要改由統籌決定（這是順序、節奏的問題，不在查核範圍）。
  - iyph 幾乎是 mxkt「頁面寫的是，每個月一百六十五元」的重複；2jya 和前一句 d8ij 的「官方條款自己寫的是」意思重複。下一句 63sp「把這句話拆成三個時間點」的「這句話」現在要跨過 2jya 回指 d8ij，仍聽得懂，但比原本的「這句話，官方寫在…」鬆一點。
  - 本輪看過的句子都在 40 字內，沒有查證口吻、括號或網址；拉丁詞只有 AI、Plus、Gemini、Google，都在發音字典裡。
- lint：`node TOOL/tools/video/cli.mjs lint --file …/video.json` → 0 errors、1 warning（估計 12.4 分鐘，是已知的 250 字／分鐘估算，不處理）；改之前與改之後相同。
- 懷疑但沒改：yu5p 的「第一眼」（標題那一行在摘要上面，口語上說得通）；d8ij 沒提條款的例外「except where consent is required under applicable laws」（第一輪已接受，不在本輪範圍）；qjpw 拿掉「人工」如果站主認為審核關卡就算人工核對，可以改回，但目前沒有來源撐得住六欄都是人工整理的。
- 範圍內的主張全部有結論，沒有未了結項。
- 需要第四輪嗎：不需要。本輪只改了 1 處事實，沒有超過三處。
