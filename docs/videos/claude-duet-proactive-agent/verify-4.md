# 查核第 4 輪：claude-duet-proactive-agent（紙底版）

查核日 2026-10-23。第 4 輪由不同於第 1–3 輪的代理執行。範圍：第 3 輪改動的 9 條全部重查；第 3 輪確認的 51 條（含 4 條意見）隨機抽 17 條（`_tools/verify/round4/random-pick.txt`：#1、2、3、11、12、14、17、24、28、31、40、44、51、54、55、58、60，編號照 `verify-3.md`）；協調者第 3 輪之後縮短的五句（s89f、5p54、pbw7、vt9x、is38）逐句對原文。

來源（今天以 `curl -sSL -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)"` 重抓，每個 host 間隔 1 秒以上，請求裡沒有任何個人資料；去掉 `<!-- -->`、script、style 後比對，腳本 `_tools/verify/round4/strip.mjs`）：

- A＝https://claude.com/resources/articles/claude-duet ｜HTTP 200｜545,232 bytes（與第 3 輪同大小）
- P＝https://claude.com/product/claude-duet ｜HTTP 200｜434,035 bytes（同上）；示範區塊的字在原始 HTML（Praw）裡比對
- T＝https://techcrunch.com/2026/10/22/claude-duet-app-is-anthropics-bet-on-agents/ ｜HTTP 200｜datePublished 2026-10-22T13:53:26+00:00
- V＝https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping ｜HTTP 200

沒用網頁搜尋。

## 一、第 3 輪改動的 9 條

| # | 主張（現在的寫法） | 位置 | 來源原文 | HTTP | 判定 | 前 → 後 |
|---|---|---|---|---|---|---|
| R1（3-#6） | 把該回的信、該催的帳先擬好；卡片「擬催帳」；說明欄「擬好回信和催帳提醒」 | t4jn；verbs-a.text；youtube.description | A「Check Intuit QuickBooks or Stripe for unpaid invoices and draft reminders」；P FAQ「draft replies for you to approve … finding unpaid invoices and drafting the reminders」 | 200 | CONFIRMED | |
| R2（3-#7） | 要用的簡報先準備好；卡片「備好簡報」；說明欄「備好簡報」 | um6i；verbs-b.text；youtube.description | P FAQ「It can put together a brief, deck, or dashboard too」；A「reads, drafts, and prepares work on its own」 | 200 | CONFIRMED | |
| R3（3-#16） | 新助理得從頭認識你，它第一則訊息就帶著你帳號裡的記憶、技能和連接器；副標「第一則訊息就接上」；key「它接上你帳號的記憶、技能、連接器」 | 5p54；same-account | P「Your memory, skills, and apps from the Claude app are there from the first message, all in one thread」；A「carries over your memory, skills, and connected apps from your Claude account」 | 200 | CONFIRMED（縮短後拿掉「Claude」兩字，「你帳號」仍是同一個 Claude 帳號，意思不變） | |
| R4（3-#18） | key「連接器和外掛，超過 6,000 個」 | connectors.key | A「over 6,000 connectors and plugins in the Claude Marketplace」；P「Works with more than 6,000 connectors and plugins」 | 200 | CONFIRMED | |
| R5（3-#32） | key「連核准也不做：證券、帳戶間轉帳」 | two.key | A「off-limits even with your approval, like trading securities or moving money between accounts」；T「won't trade securities or move money between accounts」 | 200 | CONFIRMED | |
| R6（3-#37） | 提醒是你先設好的；這一次，她什麼都沒交代；key 同 | c5bz；jess-quote.keys[1] | A「One day, without being asked, it flagged a property showing …」 | 200 | CONFIRMED | |
| R7（3-#43） | Anthropic 寫下三件還不行；卡片標題「Anthropic 寫下的三件還不行」 | is38；not-ready.title | A「This is an early version … misread a thread or miscalibrate what's urgent … personal errands, such as booking tickets, aren't quite as strong, and it can't yet show you its browser」 | 200 | CONFIRMED | |
| R8（3-#45） | key「Muse 替你買；Duet 跑腿沒那麼強」 | muse.key | V「We used it during testing to successfully purchase tank tops from Amazon」；A「aren't quite as strong」 | 200 | CONFIRMED | |
| R9（3-#46） | 現在先開給美國的 Pro 和 Max，要排候補；說明欄「候補先開給美國的 Pro 與 Max」 | nna4；youtube.description | A「available by waitlist today, starting with US Pro and Max subscribers」「We're starting today with Pro and Max users in the US」；P FAQ「a research preview on a waitlist for Claude Pro and Max subscribers in the US」 | 200 | CONFIRMED | |

## 二、協調者縮短的五句

| 句 | 現在的旁白 | 來源原文 | HTTP | 判定 |
|---|---|---|---|---|
| s89f | 10 月 21 日，Anthropic 公告了 Claude Duet：一個不等你開口、自己先找上門的 AI。 | A「Date October 21, 2026」「Today, we're opening a research preview of Claude Duet, a new app where Claude works as a proactive agent. It comes to you with what needs your attention」「Claude Duet comes to you first」 | 200 | CONFIRMED（研究預覽留在 open.subtitle） |
| 5p54 | 只有一點不像：新助理得從頭認識你，它第一則訊息就帶著你帳號裡的記憶、技能和連接器。 | 見 R3 | 200 | CONFIRMED |
| pbw7 | 示範畫面裡，芝加哥新店的衛生許可六百四十美元：它填好表，像把請款單拿到她面前等她簽。 | P 示範「Chicago location: Opens Nov 14. The health permit needs your OK and $640.」「Health permit: the county form is filled. The fee is $640.」「$640.00」「Expires in 8 min」 | 200 | CONFIRMED（「新店」＝Opens Nov 14 的新據點；「等她簽」是對照，核准鍵在示範上） |
| vt9x | 這是它的規矩：寄訊息、付款、簽文件、刪除，做之前一定先問你，把原樣給你看。 | A「before it sends a message, makes a payment, signs a document, or deletes anything, it shows you exactly what it's about to do and waits for your approval」 | 200 | CONFIRMED |
| is38 | Anthropic 寫下三件還不行：跑腿、訂票這種個人雜事沒那麼強，它是為工作做的； | A「We built its core functionality around work, so personal errands, such as booking tickets, aren't quite as strong」 | 200 | CONFIRMED |

## 三、第 3 輪確認項目的隨機抽查（17／51）

| 3-# | 主張 | 位置 | 來源原文 | HTTP | 判定 |
|---|---|---|---|---|---|
| 1 | 10 月 21 日公告研究預覽 | s89f；open.subtitle | A「October 21, 2026」「opening a research preview of Claude Duet」 | 200 | CONFIRMED |
| 2 | 不等你開口、自己先找上門 | s89f；open.title；縮圖 sub | A「comes to you first」；P FAQ「Claude Duet comes to you」 | 200 | CONFIRMED |
| 3 | 先替你把事做了再來找你 | naive.sub | A「reads, drafts, and prepares work on its own」「You'll receive a notification when the task is complete or needs your review」 | 200 | CONFIRMED |
| 11 | Claude 等你打開對話、你跟它一起做 | jptr；reversed.left | P FAQ「The Claude app waits for you to open a chat, and you work on something alongside Claude」 | 200 | CONFIRMED |
| 12 | Duet 先來找你，做完或要你決定才通知 | ygmf；reversed.right | P FAQ「reaches out when one is done or needs your approval」；A「messages you only when something needs your attention」 | 200 | CONFIRMED |
| 14 | 示範：咖啡連鎖老闆 Maya，星期一 9:41，五件進行中兩件需要你 | r85j、tjfh；demo-page；morning-msg | P「Monday, October 19」「9:41」「Morning, Maya. 5 things in progress and 2 that need you.」；Marlo、Cafés | 200 | CONFIRMED |
| 17 | 連接器和外掛超過 6,000 個 | pitf；connectors.text | 見 R4 | 200 | CONFIRMED |
| 24 | 用 Pro／Max 額度、背景每看一次都算、跟平常的 Claude 共用 | 8dii；limits | A「shares your plan's usage limits with the rest of Claude … Its background checks count toward those limits」 | 200 | CONFIRMED |
| 28 | 付好了、向郡政府要 11 月 6 或 7 日驗收；咖啡機延到 11 月 10 日，緊但來得及 | tftz、fxxr；paid | P「Paid. Inspection is the next gate. I asked the county for Nov 6 or 7.」「FYI: the espresso machine install slipped to Nov 10. Tight, but it works. I'm watching it.」 | 200 | CONFIRMED |
| 31 | 有幾件連核准也不做：買賣證券、帳戶間轉帳 | msk3；two.sub | 見 R5 | 200 | CONFIRMED |
| 40 | 整個設計繞著一個判斷：需要你、可以等、先問你 | 6xjk；judgment | A「decide what needs you, what can wait, and when to check with you first」；P「Built for judgment」 | 200 | CONFIRMED |
| 44 | Muse 要替你去買東西 | sfua；muse.sub | V「successfully purchase tank tops from Amazon」 | 200 | CONFIRMED |
| 51 | 沿用同一帳號的記憶、技能、連接器 | bcyx；three-steps | A「carries over your memory, skills, and connected apps from your Claude account」 | 200 | CONFIRMED |
| 54 | 說明欄：示範來自產品頁、Maya／Marlo 是示範、Jess 是公告引用的早期測試者、TechCrunch 2026-10-22 補個人代理分別、本頻道沒試用 | youtube.description | P 示範區塊；A「We gave small business owners and entrepreneurs early access」「Jess gets a rundown …」；T「6:53 AM PDT · October 22, 2026」「making a distinction from personal agents such as Instinct」 | 200 | CONFIRMED |
| 55 | 說明欄：Team／Enterprise 還沒有、每幾個小時、額度共用、背景檢查算、大任務花更多、Shopify 編輯器與 1Password「即將推出」 | youtube.description | P FAQ「Team and Enterprise plans are not included yet」；A「every few hours」「background checks count toward those limits」「building a financial model or a deck, require more model turns and background work」「Coming soon, a richer visual editor」「Coming soon … 1Password」 | 200 | CONFIRMED |
| 58 | 標籤「Opus 5.5」 | youtube.tags | P「Powered by Opus 5.5」；A「designed it around Claude Opus 5.5」 | 200 | CONFIRMED |
| 60 | 我最在意的是它在哪裡停：兩張清單比功能表重要 | 3v75；two-lists | brief.md 站主觀點第 1–2 句 | — | 意見，相符 |

## 摘要

- 重查 31 條（第 3 輪改動 9＋縮短五句 5＋抽查 17）：確認 31（含 1 條意見相符；5p54、is38 同時在改動與縮短兩組，各算一次），改動 0，查無 0。`video.json` 沒有改。
- 快過期的事實：研究預覽、候補先開給美國 Pro／Max、Team／Enterprise「not included yet」、每幾個小時檢查一次、額度共用與背景檢查計入、Shopify 視覺編輯器與 1Password「Coming soon」：公告日期 October 21, 2026；產品頁沒有日期，今天 2026-10-23 查看；TechCrunch 2026-10-22。
- 意見不符：沒有。3v75、5fxi、q2vq、bcyx、sfua 的意見都標了「我的看法是／我最在意的／我會先」，跟 brief.md 站主觀點一致；「公告沒寫，我不知道」保持不確定。
- 聽稿：超過 40 字的句子 3 句（s89f 47、pbw7 41、is38 41，拉丁字母逐字算，s89f 實際念起來約 35 個口語單位）；5p54、vt9x 縮短後已在 40 字內；沒有查證式旁白、括號或網址；拉丁字詞都在字典裡。
- lint：`node tools/video/cli.mjs lint --slug claude-duet-proactive-agent` 0 錯誤、2 警告（開場承諾句像目錄、outro 只有一句；結構，不動）；估計 8.2 分鐘、73 句。
- 懷疑但沒改：(1) two 卡大字 `text`「證券、轉帳」只寫「轉帳」，同卡副標「買賣證券、帳戶之間轉帳」、key 與旁白都寫帳戶間，同一畫面就有限定；拉長大字有第 3 輪 render 報過的 numeral 卡版面風險，保留，交協調者決定；(2) t4jn 把「擬催帳」掛在「每天早上先讀你的信箱和行事曆」之後，原文的催帳是查 QuickBooks／Stripe 的功能，不一定每天早上、也不是從信箱讀，屬一般功能的濃縮說法，保留；(3) answer 卡「你點頭之前的，它都做」偏寬（證券與帳戶間轉帳點頭也不做），第 3 輪已記，保留。
- 第 5 輪：不需要。本輪事實改動 0 條。
