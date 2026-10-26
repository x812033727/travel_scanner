# 查核第 3 輪：claude-duet-proactive-agent（紙底版）

查核日 2026-10-23。對象是紙底版重寫的 `video.json`（47 景、73 句）。第 1、2 輪查的是前一版插圖稿，事實表（`verify-1.md`、`verify-2.md`）仍有效；這一輪把新稿的每一句旁白、每張卡片（`data` 含 `keys`／`key`／`numeral`、對話、表格、引言與翻譯）、縮圖、標題、說明欄、標籤重新逐條對原文。

來源（今天以 `curl -sSL -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)"` 重抓，每個 host 間隔 1 秒以上，請求裡沒有任何個人資料）：

- A＝https://claude.com/resources/articles/claude-duet ｜HTTP 200｜545,232 bytes；正文（Today, we… 到 Related articles）與撰稿存檔逐字相同，位元組差在頁尾相關文章
- P＝https://claude.com/product/claude-duet ｜HTTP 200｜434,035 bytes（與存檔同大小，內容差在頁面隨機值）
- T＝https://techcrunch.com/2026/10/22/claude-duet-app-is-anthropics-bet-on-agents/ ｜HTTP 200
- V＝https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping ｜HTTP 200（Muse 那一句）

腳本靠的 84 句原文用 `_tools/verify/round3/check.mjs` 逐句在今天的頁面上比對：84／84 找到。沒用網頁搜尋。

## 逐條表

| # | 主張 | 位置 | 來源 | HTTP | 判定 | 前 → 後 |
|---|---|---|---|---|---|---|
| 1 | 10 月 21 日 Anthropic 公告 Claude Duet 研究預覽 | s89f；open.subtitle | A「October 21, 2026」「opening a research preview」 | 200 | CONFIRMED | |
| 2 | 不等你開口、自己先找上門 | s89f；open.title；縮圖 sub | A「comes to you first」；P FAQ「Claude Duet comes to you」 | 200 | CONFIRMED | |
| 3 | 不是推播：先替你把事做了再來找你 | naive.sub | A「reads, drafts, and prepares work on its own」「notification when the task is complete or needs your review」 | 200 | CONFIRMED | |
| 4 | 每天早上先讀你的信箱和行事曆 | t4jn；verbs-a | A「Each morning, it sends you a short brief … across your connected apps」；P FAQ「flag what needs you in your inbox and calendar」 | 200 | CONFIRMED | |
| 5 | 把該回的信擬好 | t4jn；verbs-a.text | P FAQ「draft replies for you to approve」 | 200 | CONFIRMED | |
| 6 | 把該退的款擬好（一般寫法） | t4jn；verbs-a.text；說明欄 | 只有 P 示範「Refunds are drafted」 | 200 | CHANGED | 「該退的款」「擬退款」→「該催的帳」「擬催帳」；說明欄「回信和退款」→「回信和催帳提醒」（A「Check Intuit QuickBooks or Stripe for unpaid invoices and draft reminders」、P FAQ「finding unpaid invoices and drafting the reminders」；c32） |
| 7 | 簡報用最新的數字重做好（一般寫法） | um6i；verbs-b.text；說明欄 | 只有 P 示範「The deck is rebuilt with Q3」 | 200 | CHANGED | 「簡報用最新的數字重做好」→「要用的簡報先準備好」；卡片「重做簡報」→「備好簡報」；說明欄「重做簡報」→「備好簡報」（P FAQ「It can put together a brief, deck, or dashboard too」、A「prepares work on its own」；c32） |
| 8 | 錢要出去之前停下來問你 | um6i；verbs-b；縮圖；標題 | A「before it … makes a payment … waits for your approval」 | 200 | CONFIRMED | |
| 9 | 它碰得到你的信和你的錢 | 7c87；stakes | A「An agent that reads email and sends messages」；付款需核准 | 200 | CONFIRMED | |
| 10 | 承諾：四件先問、兩件連核准也不做、吃額度的規則、三件 | 3vzx、jfhc；promise | A（見 #29、#33、#22） | 200 | CONFIRMED | |
| 11 | Claude 等你打開對話、你跟它一起做一件事 | jptr；reversed.left | P FAQ「waits for you to open a chat, and you work on something alongside Claude」 | 200 | CONFIRMED | |
| 12 | Duet 先來找你、做完或要你決定才通知 | ygmf；reversed.right | P FAQ「Claude Duet comes to you … reaches out when one is done or needs your approval」；A「messages you only when something needs your attention」 | 200 | CONFIRMED | |
| 13 | 「不是更聰明，是方向反過來」 | jptr | 撰稿框架；P FAQ 的差別題講的是方向 | — | OUT OF SCOPE | |
| 14 | 示範畫面：咖啡連鎖老闆 Maya 星期一早上 9:41 收到「五件事在進行中，兩件需要你」 | r85j、tjfh；demo-page；morning-msg | P「Monday, October 19」「9:41」「Morning, Maya. 5 things in progress and 2 that need you.」；Marlo 有 Cafés | 200 | CONFIRMED | |
| 15 | 自己的雲端電腦和瀏覽器，手機關了照做 | bv74；cloud | A「virtual machine with its own browser, so it doesn't require your laptop or phone to be on」；P「its own computer in the cloud」 | 200 | CONFIRMED | |
| 16 | 比喻不像的一點：助理記得昨天，它每次對話都從帳號接上 | 5p54；same-account.sub | P「Your memory, skills, and apps … are there from the first message, all in one thread」；FAQ「Your history is in one thread. It remembers what you said before.」 | 200 | CHANGED | 原句等於說它不記得昨天、每次對話重接，跟原文相反 →「新助理得從頭認識你，它第一則訊息就帶著你 Claude 帳號的記憶、技能和連接器」；副標「每次對話都接上」→「第一則訊息就接上」（c9） |
| 17 | 連接器和外掛超過 6,000 個 | pitf；connectors.text | A「over 6,000 connectors and plugins」；P「more than 6,000 connectors and plugins」 | 200 | CONFIRMED | |
| 18 | 關鍵句「接得上的連接器超過 6,000 個」 | connectors.key | 同上：6,000 數的是連接器加外掛 | 200 | CHANGED | →「連接器和外掛，超過 6,000 個」（c13，同第 1 輪 gd58 的理由） |
| 19 | 你帳號裡接了什麼，它早上就讀什麼 | pitf | A「brief on the most important items across your connected apps」 | 200 | CONFIRMED | |
| 20 | 一早三十則通知；自己開信箱、行事曆、QuickBooks | k4py、hkyv；thirty、today | brief.md 的共同經驗與觀眾現在做法 | — | OUT OF SCOPE（不是來源事實） | |
| 21 | 示範便條：Jenn 另一份錄取通知今天下午到期；Northfield 續約要改付款條件；週末送錯的訂單退款擬好；募資簡報用最新一季數字重做、幾頁要她看 | mhhe、qbit、p4md、i3s4；brief | P「Jenn's other offer expires at 6 p.m.」「redlined the $410K renewal and want Net 60」「Refunds are drafted」「The deck is rebuilt with Q3. 2 slides need your eye.」 | 200 | CONFIRMED（i3s4 原本沒有 c-id 涵蓋，c10 補 Series A 那條） | |
| 22 | 每幾個小時看一次你的 app | shfd；quiet | A「checks your connected accounts every few hours」 | 200 | CONFIRMED | |
| 23 | 為什麼不一直看：一直看額度很快用光 | 8ez6、8dii；why-not、limits | A「checking nonstop would use up your plan's limits much faster」 | 200 | CONFIRMED | |
| 24 | 用的是 Pro 或 Max 的額度，背景每看一次都算；跟平常的 Claude 共用 | 8dii；limits | A「shares your plan's usage limits with the rest of Claude … Its background checks count toward those limits」 | 200 | CONFIRMED | |
| 25 | 告訴它要聽什麼、多久回報一次 | 6cba、c3kc；tell-it、three-steps | A「tell it what you want to hear about and how often」 | 200 | CONFIRMED | |
| 26 | 兩次檢查之間進來的可能漏掉 | 2vty；tell-it.sub | P FAQ「it can miss something that arrives between checking in with you」 | 200 | CONFIRMED | |
| 27 | 示範：芝加哥新店衛生許可 640 美元，表格填好，核准鍵八分鐘內有效 | pbw7；permit | P「the county form is filled. The fee is $640.」「$640.00 Expires in 8 min」「Approve」 | 200 | CONFIRMED | |
| 28 | 示範：付好了、向郡政府要 11 月 6 或 7 日驗收；咖啡機安裝延到 11 月 10 日、緊但來得及、我盯著 | tftz、fxxr；paid | P「Paid. Inspection is the next gate. I asked the county for Nov 6 or 7.」「FYI: the espresso machine install slipped to Nov 10. Tight, but it works. I'm watching it.」 | 200 | CONFIRMED | |
| 29 | 寄訊息、付款、簽文件、刪除前一定先問、把要做的原樣給你看 | vt9x、nhmc；four、answer-stop | A「before it sends a message, makes a payment, signs a document, or deletes anything, it shows you exactly what it's about to do and waits for your approval」 | 200 | CONFIRMED | |
| 30 | 示範：寄簡報給 Harbor 的 Elena、附資料室連結、「從你這裡寄出？」、她按送出 | x8ym、6qss；send-from-you | P「Send the deck to Elena at Harbor.」「Drafted with the data room link. Send from you?」「Not now／Send」「Sent」 | 200 | CONFIRMED | |
| 31 | 有幾件連核准也不做：買賣證券、帳戶間轉帳 | msk3；two.text/sub | A「A few things are off-limits even with your approval, like trading securities or moving money between accounts」；T 同 | 200 | CONFIRMED | |
| 32 | 關鍵句「連核准也不做：買賣證券、轉帳」 | two.key | 同上：只有帳戶之間的轉帳；付款經核准可以 | 200 | CHANGED | →「連核准也不做：證券、帳戶間轉帳」（c20，同第 2 輪縮圖的理由） |
| 33 | 每則訊息送出前一道檢查：信用卡號、證件號碼預設不給；健康與個人財務明確交代才送 | chwb、nvym；classifier；說明欄 | A「checks each message … reject requests to share … credit card numbers and government identification … health or personal finances, are let through only when you've explicitly instructed」；T「by default」 | 200 | CONFIRMED | |
| 34 | 替公司買東西走 Stripe 的 Link：先確認品項、Link 要你核准這筆錢、虛擬卡付、真卡號不會到店家手上 | kaj8、4uwf、6j7g；link | A「purchase things for your business using Link, Stripe's digital wallet … confirms the item with you, and Link asks you to approve the spend. It then pays with a virtual card, so your real card number isn't shared.」 | 200 | CONFIRMED（「不會到店家手上」是 isn't shared 的自然讀法，見下） | |
| 35 | 公告引用的房仲 Jess 每天早上收一份簡報；沒被問就標出行事曆上排錯日期的看房 | 4ds2、aviw；jess、showing | A「Jess gets a rundown from Claude Duet each morning. One day, without being asked, it flagged a property showing that was on her calendar for the wrong day.」 | 200 | CONFIRMED | |
| 36 | Jess 引言原文與翻譯 | jess-quote | A「"[This is] exactly the kind of thing I want caught without having to ask," she said.」「Jess Provencher, broker and owner, Pro Homes」 | 200 | CONFIRMED | |
| 37 | 提醒是你先設好的；這一次她什麼都沒設 | c5bz；jess-quote.keys[1] | A 只有「without being asked」，沒說她有沒有設提醒 | 200 | CHANGED | 「什麼都沒設」→「什麼都沒交代」（旁白、關鍵句、emotion；c16） |
| 38 | Amin：南佛州幾家烤肉串店老闆、早期測試者、約 110 名員工、會計客服行銷、一家店一家店過發票 | wejr、x4fs；amin | A「Amin owns Shahs of Kabob in South Florida with about 110 employees … accounting, customer support, and marketing, and has worked through his invoices store by store」「small business owners and entrepreneurs early access」 | 200 | CONFIRMED | |
| 39 | Amin 引言原文與翻譯 | x4fs、vhag；amin-quote | A「"It brings it all together," … "I don't need to open up 100 tabs."」「Amin Ebrahimi, owner, Shahs of Kabob」 | 200 | CONFIRMED | |
| 40 | 整個設計繞著一個判斷：需要你、可以等、先問你 | 6xjk；judgment | A「What makes Claude Duet so helpful is its judgment … decide what needs you, what can wait, and when to check with you first」；P「Built for judgment」 | 200 | CONFIRMED | |
| 41 | Anthropic 自己先認：可能讀錯討論串 | 767y；misread | A「it still might misread a thread」 | 200 | CONFIRMED | |
| 42 | 三件還不行：跑腿訂票沒那麼強（為工作做的）、還不能即時給你看瀏覽器、可能看錯哪件事急 | is38、jtv5、6tzv；not-ready | A「misread a thread or miscalibrate what's urgent … built its core functionality around work, so personal errands, such as booking tickets, aren't quite as strong, and it can't yet show you its browser」；T「can't show you its browser use as it happens」 | 200 | CONFIRMED（內容） | |
| 43 | 「它（自己）寫下三件還不行」 | is38；not-ready.title | 寫下的是 Anthropic 的公告；前一句的「它」是 Duet | 200 | CHANGED | 「它寫下」→「Anthropic 寫下」；標題「它自己寫下的」→「Anthropic 寫下的」（c24；前版聽稿修正也把「它自己說」改成 Anthropic） |
| 44 | 前一支講的 Muse 要替你去買東西 | sfua；muse | V「We used it during testing to successfully purchase tank tops from Amazon」（c25 有引，muse 場景 claims 列了 c25） | 200 | CONFIRMED | |
| 45 | 關鍵句「Muse 替你買東西；Duet 不跑腿」 | muse.key | A「aren't quite as strong」：不是不跑腿 | 200 | CHANGED | →「Muse 替你買；Duet 跑腿沒那麼強」（c24／c25，同第 1 輪 xg4i 的理由） |
| 46 | 現在能排候補的，只有美國的 Pro 和 Max | nna4；說明欄「候補只收」 | A「available by waitlist today, starting with US Pro and Max subscribers」；P FAQ「a research preview on a waitlist for Claude Pro and Max subscribers in the US」 | 200 | CHANGED | 第 1 輪已確認看不出候補表單擋不擋美國以外的人，能說的只有「先開給」→「現在先開給美國的 Pro 和 Max，要排候補」；說明欄「候補只收」→「候補先開給」（c29） |
| 47 | 表格：美國 Pro、Max 研究預覽排候補；Team、Enterprise 還沒有；台灣還輪不到 | who；f2er、kn7c；縮圖標題「台灣還輪不到」 | P FAQ「Team and Enterprise plans are not included yet」；A「We're starting today with Pro and Max users in the US」（台灣是推論，c29） | 200 | CONFIRMED | |
| 48 | 手機上是獨立 app，電腦上用網頁 | wdy6 | P FAQ「standalone app for iOS and Android. On a computer, you can open it on the web at claude.ai」 | 200 | CONFIRMED | |
| 49 | 財務模型、簡報這種大任務要更多回合和背景工作、花得更多 | mf5d；big-tasks | A「larger tasks, like building a financial model or a deck, require more model turns and background work」 | 200 | CONFIRMED | |
| 50 | 候補會不會開到台灣、什麼時候：公告沒寫，我不知道 | q2vq；taiwan | A、P 沒有任何一處寫台灣或開放時程 | 200 | CONFIRMED（不確定句保持不確定） | |
| 51 | 沿用同一帳號的記憶、技能、連接器 | bcyx；three-steps；closing | A「carries over your memory, skills, and connected apps from your Claude account」 | 200 | CONFIRMED | |
| 52 | 接上的 app 隨時可以斷開 | aizg；three-steps | A「You're also able to disconnect any app Claude Duet has access to」 | 200 | CONFIRMED | |
| 53 | 替你讀、替你擬、替你盯，做到你點頭之前 | a3ie；answer | A「reads, drafts, and prepares work on its own」「keeps tabs on those apps」 | 200 | CONFIRMED（answer 加列 c32） | |
| 54 | 說明欄：示範畫面全來自產品頁、Maya／Marlo 是示範、Jess 是公告引用的早期測試者、TechCrunch 補個人代理分別、本頻道沒試用 | youtube.description | P、A、T | 200 | CONFIRMED | |
| 55 | 說明欄：Team／Enterprise 還沒有、每幾個小時、額度共用、背景檢查算、大任務花更多 | youtube.description | A、P FAQ | 200 | CONFIRMED | |
| 56 | 說明欄：Shopify 視覺編輯器與 1Password 登入「即將推出」、目前還沒有 | youtube.description | A「Coming soon, a richer visual editor …」「Coming soon, with your permission, it will be able to sign in … 1Password」 | 200 | CONFIRMED | |
| 57 | 說明欄：前一支講 Meta 的 Muse 被 Amazon 擋下來 | youtube.description | V | 200 | CONFIRMED | |
| 58 | 標籤「Opus 5.5」 | youtube.tags | P「Powered by Opus 5.5」；A | 200 | CONFIRMED | |
| 59 | 我的看法：先看它多久看一次再決定要不要讓它盯信箱 | 5fxi；my-rule | brief.md 站主觀點第 3 句 | — | 意見，相符 | |
| 60 | 我最在意的是它在哪裡停：兩張清單比功能表重要 | 3v75；two-lists | brief.md 站主觀點第 1–2 句 | — | 意見，相符 | |
| 61 | 兩家把線畫在不同地方 | sfua；muse | brief.md 站主觀點第 5 句 | — | 意見，相符 | |
| 62 | 我的看法是不用急；我會先整理記憶、技能、連接器 | q2vq、bcyx | brief.md 站主觀點第 4 句 | — | 意見，相符 | |
| 63 | 對照（助理、便條、紅標籤、工時、印章和存摺、不讓你看他在哪） | feb5、kuea、ahbj、8ez6、un3y、jtv5 等 | 對照的部位，各自對應 c12／c14／c15／c20／c24 | — | OUT OF SCOPE（機制與原文一致，#16 除外已改） | |

## 摘要

- 查了 63 條：確認 50 條（含 4 條意見相符），改 9 條（#6、#7、#16、#18、#32、#37、#43、#45、#46），查無 0 條，其餘 4 條不在查核範圍（框架、玩笑、對照）。
- c-id 引用沒涵蓋句子的：verbs-a（c10、c19 不涵蓋讀信箱與行事曆、擬回信）、verbs-b（c11 是時間戳，不是簡報重做）、brief 的 i3s4（c10 原本沒有 Series A 那條）、answer（c6 沒有 reads／drafts）。處理：新增 c32（一般功能），verbs-a 改列 c32＋c12、verbs-b 改列 c32＋c6、answer 加列 c32；c10 補 Series A 原文；c9 補「from the first message」「one thread」。
- 快過期的事實：研究預覽、只先開給美國 Pro 與 Max 的候補、Team／Enterprise「not included yet」、每幾個小時檢查一次、額度共用、Shopify 編輯器與 1Password「Coming soon」，都是公告（October 21, 2026）與產品頁（今天 2026-10-23 查看，頁面沒有日期）研究預覽期間的狀態。
- 意見不符：沒有。四句意見都標了「我的看法是／我最在意的／我會先」，跟 brief.md 站主觀點一致；「公告沒寫，我不知道」保持不確定。
- 聽稿：超過 40 字的句子 5 句（s89f 52、5p54 45 上下、pbw7 41、vt9x 42、is38 43，listener 把拉丁字母逐字算）；沒有查證式旁白（經查證、根據官方文件、本影片）；沒有括號或網址；片中拉丁字詞都在字典裡（多數 null，照字面念）。
- 每個示範項目旁白都說了「示範畫面裡」（demo-page、brief、permit、send-from-you）；paid 與 morning-msg 接在前一句的示範之後；測試者都說「公告裡引用的」「一樣是早期測試者」；沒有任何一句說成本頻道的實測。
- lint：`node tools/video/cli.mjs lint --slug claude-duet-proactive-agent` 0 錯誤、2 警告（開場承諾句被判像目錄、outro 只有一句；都屬結構，不動）。
- 懷疑但沒改：(1) 6j7g「真正的卡號不會到店家手上」：原文只說 isn't shared，沒說對誰，虛擬卡的用途就是不給店家，保留；(2) jtv5「像一個不讓你看他現在在哪裡的助理」：產品頁另有「You can see what Claude Duet has done and is doing for you」，不行的是即時看瀏覽器，卡片寫「看不到它的瀏覽器在做什麼」是對的，比喻稍寬，屬對照，保留；(3) 「你點頭之前的，它都做」（answer 卡）偏寬（證券與帳戶轉帳點頭也不做），是開場問題的答案框架，前一版也有，保留；(4) Jenn 的 offer「6 p.m.」寫「今天下午」，台灣口語的下午六點，保留；(5) 說明欄「Maya 和她的 Marlo 咖啡連鎖是示範，不是真實顧客」：產品頁沒有明寫虛構，示範的人物，保留；(6) two 卡 numeral「02」與承諾句「兩件」：原文是 A few things … like，旁白用「有幾件…」，同第 1 輪結論保留。
- 第 4 輪：需要。本輪事實改動 9 條，超過三條。
