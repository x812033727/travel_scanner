# 查核清單：claude-duet-proactive-agent

撰稿 2026-10-23。每一行一個可查的主張：編號｜主張（旁白或畫面怎麼說）｜出處網址｜查證日｜用到它的場景 id。
片中沒有任何一次是本頻道的實測：Maya、Marlo、640 美元、41 項清單、Marlo Pulse 的每個數字都是 Anthropic 產品頁上的示範畫面（旁白說「示範畫面」，卡片 `source` 標「Anthropic 產品頁示範 2026-10-23」）；
三位使用者的事是 Anthropic 2026-10-21 公告引用的早期測試者（旁白說「公告裡引用的」「第二位」「第三位」）；「我的看法是」那幾句是 brief.md 站主觀點的提案，不是事實主張。
公告、產品頁、TechCrunch 的全文存在 `<VIDEO_WORKDIR>/claude-duet-proactive-agent/_tools/sources/`（`claude-duet-article.txt`、`claude-duet-product.txt`、`techcrunch-duet.txt`，2026-10-23 存）；Mokaair 文章的 JSON 存在同資料夾 `mokaair-article.json`（HTTP 200，2026-10-23）。
公告＝A https://claude.com/resources/articles/claude-duet ；產品頁＝P https://claude.com/product/claude-duet ；TechCrunch＝T https://techcrunch.com/2026/10/22/claude-duet-app-is-anthropics-bet-on-agents/ ；Mokaair＝M https://mokaair.com/zh-TW/life/ai-news-claude-duet-20261022

c1｜示範畫面：Monday, October 19、9:41、「Morning, Maya. 5 things in progress and 2 that need you.」；Maya 經營 Marlo（咖啡連鎖，Pulse 頁有 Cafés、Wholesale、Subscriptions）。旁白說「星期一早上九點四十一分」「示範畫面上」，不說日期（示範的 10 月 19 日在公告前兩天，講出來會混淆）｜P｜2026-10-23｜hook, phone-buzz, question-door, counter-customers
c2｜Chicago location：「The health permit needs your OK and $640.」；付款卡「$640.00 Expires in 8 min」「Approve／Not now」→「Paid」。旁白：費用 640 美元、核准或等等、她按了核准、核准鍵八分鐘內有效｜P｜2026-10-23｜thumb-approve, ch2
c3｜「Paid. Inspection is the next gate. I asked the county for Nov 6 or 7.」→ 旁白「下一關：驗收，向郡政府要了 11 月 6 號或 7 號」｜P｜2026-10-23｜county-counter, pay-rules
c4｜開幕清單：「I built the opening checklist from your last two openings: 41 items. 33 are done or on track. 7 I'm watching. 1 needs you today.」（開幕 26 天後＝Nov 14，旁白不講）｜P｜2026-10-23｜checklist, sorting-trays
c5｜「FYI: the espresso machine install slipped to Nov 10. Tight, but it works. I'm watching it.」→ 旁白「延到十一月十號，緊，但來得及」；pay-rules 第三條「延誤只告知，不問你」是從這句示範整理的（它用 FYI 告知、沒有要她決定），不是公告寫的規則｜P｜2026-10-23｜espresso-crate, pay-rules
c6｜「before it sends a message, makes a payment, signs a document, or deletes anything, it shows you exactly what it's about to do and waits for your approval.」→ 四件一定先問；「花錢之前一定先問」｜A｜2026-10-21（2026-10-23 重看）｜pay-rules, seal-envelope, must-ask, closing
c7｜「Claude Duet has a virtual machine with its own browser, so it doesn't require your laptop or phone to be on … You'll receive a notification when the task is complete or needs your review.」→ 自己的雲端電腦和瀏覽器、手機關了也照做、做完或要她看才通知｜A｜2026-10-23｜apron-phone, cloud-desk
c8｜研究預覽、候補、美國 Pro 與 Max；iOS、Android 獨立 app，電腦上 claude.ai 網頁；Team 與 Enterprise 還沒有（FAQ「Team and Enterprise plans are not included yet.」）；公告日期 October 21, 2026｜A、P｜2026-10-23｜hook（副標）, who-can
c9｜FAQ「The Claude app waits for you to open a chat … Claude Duet comes to you.」；「carries over your memory, skills, and connected apps from your Claude account, so setting it up requires minimal work」→ 你以為／其實、沿用記憶技能連接器、設定幾乎不用做。產品頁「Your memory, skills, and apps from the Claude app are there from the first message, all in one thread.」、FAQ「Your history is in one thread. It remembers what you said before.」：查核第 3 輪，紙底版 5p54 原寫「助理記得昨天，它是每次對話都從你 Claude 帳號的記憶、技能和連接器接上」，等於說它不記得昨天、每次對話重新接上，跟「one thread」「remembers what you said before」相反，改「新助理得從頭認識你，它第一則訊息就帶著你 Claude 帳號的記憶、技能和連接器」，卡片副標「每次對話都接上」改「第一則訊息就接上」｜A、P｜2026-10-23｜reversed, read-everything, same-desk, same-account, three-steps, closing
c10｜晨間簡報：「Hiring: Jenn's other offer expires at 6 p.m. All 3 finalists are booked for today.」「Northfield: They redlined the $410K renewal and want Net 60.」「Customers: 27 wrong delivery orders this weekend. 19 from Valencia. Refunds are drafted.」「Series A: Harbor meets Thursday at 10. The deck is rebuilt with Q3. 2 slides need your eye.」（Net 60 旁白說「60 天付款」；Series A 那條是查核第 3 輪補進來的，紙底版 brief 場景 i3s4「簡報用最新一季的數字重做好了，有幾頁要她看」靠它，原本沒有任何 c-id 引這句）｜P｜2026-10-23｜morning-brief, brief
c11｜示範時間戳：Series A deck「Updated 5:48 AM」、Partner meeting prep「Updated 5:52 AM」→ 旁白「早上五點四十八分，她還沒開口，募資簡報已經改好」；「它在她開口前讀完所有 app」是把 5:48 的更新、9:41 才傳來的早安訊息與公告「Each morning, it sends you a short brief on the most important items across your connected apps」連起來的講法。查核第 1 輪：原寫「她還在睡」「她醒來前」（第 3 章章名同），示範沒有任何一處寫她幾點醒、在睡覺，改成畫面上確實成立的「她開口前」（對話串由 Duet 先開口）；「簡報的材料」聽起來像 9:41 的晨間簡報，5:48 是 Series A 募資簡報（deck）的時間戳，改「募資簡報」。插圖 prompt（bedroom-first-light、tease-kitchen 畫睡著的人）沒動，屬畫面｜P、A｜2026-10-23｜tease-kitchen, ch3, bedroom-first-light
c12｜「We designed it around Claude Opus 5.5 … to decide what needs you, what can wait, and when to check with you first.」「Each morning, it sends you a short brief … messages you only when something needs your attention.」→ Anthropic 說它整個設計繞著一個判斷；三種分法（做掉的、盯著的、要她的）取自 c4 清單的三類｜A｜2026-10-23｜read-everything, sorting-trays, kitchen-pass, reach
c13｜「over 6,000 connectors and plugins in the Claude Marketplace」；產品頁「Works with more than 6,000 connectors and plugins」→ 連接器和外掛超過 6,000 個；「連接器就是接上 app 的接頭」是撰稿的白話解釋。查核第 1 輪：gd58 原寫「它能接的 app 超過 6,000 個」，6,000 數的是連接器和外掛，不是 app，改「它能用的連接器和外掛超過 6,000 個，連接器就是接上 app 的接頭」（卡片 label 原本就寫「連接器與外掛」）｜A、P｜2026-10-23｜reach
c14｜「Claude Duet checks your connected accounts every few hours, because checking nonstop would use up your plan's limits much faster … You can also tell it what you want to hear about and how often.」｜A｜2026-10-23｜tease-kitchen, reach, quiet-pocket, limits, tell-barista, three-steps
c15｜「shares your plan's usage limits with the rest of Claude … Its background checks count toward those limits, and larger tasks, like building a financial model or a deck, require more model turns and background work.」→ 額度共用、背景檢查算、大任務花更多；「她平常的 Claude 也跟著沒得用」是「shares limits」的直白說法｜A、P FAQ｜2026-10-23｜limits, coin-purse, who-can
c16｜Jess Provencher（broker and owner, Pro Homes）：「gets a rundown from Claude Duet each morning. One day, without being asked, it flagged a property showing that was on her calendar for the wrong day.」引言「[This is] exactly the kind of thing I want caught without having to ask」（卡片照原文含方括號）。查核第 1 輪：vywz 原寫「一位房仲的簡報裡，一場看房它沒被問就標出來」，公告沒說是在早晨簡報裡標出的，只說那場看房「on her calendar for the wrong day」，改「一位房仲的行事曆上」｜A｜2026-10-23｜tease-broker, ch4, broker-car, jess-quote
c17｜Mya Dalton（brand strategist）：「had a call coming up with a potential client. Claude Duet saw it on her calendar and prepared a brief. It also noticed the call fell right before her flight and offered to move it.」旁白不唸她的名字（Mya 與 Maya 同音會混）｜A｜2026-10-23｜airport-gate, brief-folder
c18｜Amin Ebrahimi（owner, Shahs of Kabob, South Florida, about 110 employees）：accounting, customer support, marketing；invoices store by store；「It brings it all together. I don't need to open up 100 tabs.」旁白說「南佛州幾家烤肉串店」，店名只在卡片。查核第 2 輪：d3za 原寫「南佛州一家烤肉串店的老闆」，公告寫他「worked through his invoices store by store」，店不只一家（下一句旁白也說「一家店一家店」），改「幾家烤肉串店」｜A｜2026-10-23｜kebab-office, kebab-counter, amin-quote
c19｜示範對話：「Much. Send the deck to Elena at Harbor.」→「Drafted with the data room link. Send from you?」→ Email To: Elena, Harbor Ventures →「Not now／Send」→「Sent」｜P｜2026-10-23｜draft-letter, send-from-you, seal-envelope
c20｜「A few things are off-limits even with your approval, like trading securities or moving money between accounts. You're also able to disconnect any app」；TechCrunch「Duet won't trade securities or move money between accounts」。查核第 1 輪：tfpe 原寫「連核准也沒用的有兩件」，原文是「A few things … like」，這兩件是舉例、不是完整清單，改「連核准也沒用的，公告舉了兩件」；corkboard 的意見句與片尾「兩件事核准也不做」指的是這兩件、沒有說只有兩件，保留。查核第 2 輪：縮圖副標原寫「轉帳連核准都不做」，原文只禁「moving money between accounts」，付款（makes a payment）經核准是可以的（示範就付了 640 美元），單寫「轉帳」會把付給別人的錢也算進去，改「帳戶間轉帳連核准都不做」｜A、T｜2026-10-23｜thumbnail, off-limits, three-steps, closing
c21｜「a new dedicated classifier and safety system prompt that checks each message and guards against leaks of sensitive information … designed to reject requests to share the strictest tier of information, including credit card numbers and government identification. Other sensitive information, such as health or personal finances, are let through only when you've explicitly instructed Claude Duet to send it.」；TechCrunch「by default, the agent would turn down requests asking for credit card numbers and government identification」→「預設一律不給」。「分類器就是只做一件事的檢查程式」是撰稿的白話解釋｜A、T｜2026-10-23｜tease-mailroom, letter-door, off-limits, mailroom-palm, parcel-inspector, classifier
c22｜「purchase things for your business using Link, Stripe's digital wallet. Claude Duet confirms the item with you, and Link asks you to approve the spend. It then pays with a virtual card, so your real card number isn't shared.」（Shop Pay 與 1Password「coming soon」只在說明欄）｜A｜2026-10-23｜wallet-card, link-steps
c23｜「Red teams and an external firm penetration tested Claude Duet, and it's covered by our public bug bounty program.」→「找得到洞的人有賞金」｜A｜2026-10-23｜red-team
c24｜「it still might misread a thread or miscalibrate what's urgent. We built its core functionality around work, so personal errands, such as booking tickets, aren't quite as strong, and it can't yet show you its browser.」；FAQ「it can miss something that arrives between checking in with you」→ 三件不行＝跑腿訂票沒那麼強、不能即時看瀏覽器、兩次檢查之間漏掉；誤判急不急是前面那一句。查核第 1 輪三處：(1) idkx 原寫「三件不行寫在公告的最後一段」，第三件（兩次檢查之間漏掉）只在產品頁 FAQ「What isn't ready yet?」，公告沒有，改「寫在公告最後一節和產品頁的問答裡」；(2) 2cwq 原寫「也可能把不急的當成急的」，原文 miscalibrate what's urgent 兩個方向都算（也可能把急的當不急），改「也可能看錯哪件事急」；(3) 原文是「aren't quite as strong」，tf3w 與 not-ready 卡片原寫「不強」，改「沒那麼強」｜A、P FAQ｜2026-10-23｜closing-brief, notice-board, ch6, wrong-table, not-ready
c25｜TechCrunch：「making a distinction from personal agents such as Instinct, by noting that Duet isn't good at handling errands or booking tickets」；競品名單 Meta Muse、OpenAI Dots、Hark、Instinct、Grok Bot、Fo 只在說明欄／不唸。「Muse 要替你去買東西」是前一支影片（ai-shopping-agents-blocked，The Verge 2026-10-22）的事實，這裡只當對照的一句；查核第 1 輪重看 https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping （HTTP 200）：「We used it during testing to successfully purchase tank tops from Amazon」，成立。xg4i 原寫「Duet 自己說，它不擅長跑腿」：「不擅長」是 TechCrunch 的轉述（isn't good at handling errands），Anthropic 自己的字是「aren't quite as strong」，句子又掛在「Duet 自己說」，改「它跑腿沒那麼強」｜T、A｜2026-10-23｜ticket-counter, runner-bags
c26｜Marlo Pulse：「Build me one page I can check every morning. Is the business healthy, and where should I look?」→「On it. Pulling from your point of sale, Shopify, CRM, support inbox, payroll and bank.」→「Here's Marlo Pulse. It refreshes at 5:30 every morning, before your brief.」（旁白的清單略去 CRM）｜P｜2026-10-23｜maya-types, one-page, ledgers-cart, dawn-table, packing-table
c27｜Pulse 數字：「Revenue this week $528K」「Cash $2.1M / 14 months of runway」「Cafés +11% Same-café sales. Valencia weekends −8%.」「Healthy, with one leak: weekend delivery at Valencia.」｜P｜2026-10-23｜pulse, valencia-door
c28｜「East Bay churn went from 2.6% to 3.4% after the shipping price change. Want me to dig in?」→ Yes →「Most cancels cite shipping cost. Free shipping over $40 would have kept about 7 in 10. Want a 2-week test?」→「Set it up.」；「她自己只回了三句話」＝Build me one page…、Yes、Set it up。查核第 2 輪：產品頁原始碼裡 Yes 是 Yes／No／Not now 三個快速回覆鈕（chip，data-tap="chip"）之一，是點的不是打的，ii9y 原寫「只打了三句話」，改「只回了三句話」（三則都是她送出的訊息）。查核第 1 輪：ig2t 原寫「流失是運費漲價之後的事」，示範原文是「after the shipping price change」，沒寫漲價，改「運費調整之後」（brief 寫「運費漲價後」，來源優先）｜P｜2026-10-23｜pulse, returned-box, dig-in, packing-table
c29｜「台灣的帳號現在還輪不到」：公告「A research preview is available by waitlist today, starting with US Pro and Max subscribers」「We're starting today with Pro and Max users in the US」、FAQ「a research preview on a waitlist for Claude Pro and Max subscribers in the US」，台灣不在其中（推論，沒有一句直接寫台灣）。查核第 1 輪：原寫「台灣的帳號現在排不進候補」，片尾卡寫「台灣候補還沒開」；候補表單是 HubSpot 表單，頁面原始碼看不出會不會擋美國以外的人，公告的寫法是「starting with」美國，所以能確定的只有「還沒輪到」，p2wi 改「台灣的帳號現在還輪不到」、片尾卡改「台灣還沒輪到」｜A、P｜2026-10-23｜taipei-office, closing
c30｜站主觀點（brief.md 提案，非事實）：先看它多久看一次再決定讓不讓它盯信箱；兩張清單比功能表重要；跟 Muse 比兩家把線畫在不同地方；台灣進不了候補不用急；先整理記憶技能連接器｜brief.md｜2026-10-23｜weigh-beans, corkboard, ticket-counter, taipei-office, three-steps
c31｜Mokaair 文章存在且已發布：「Anthropic 推出 Claude Duet：主動式 AI 代理鎖定專業人士與小企業」，news_date 2026-10-22，status published｜M｜2026-10-23｜article-cta
c32｜（查核第 3 輪補）產品功能的一般寫法，不是示範：FAQ「Claude Duet can send a morning brief, flag what needs you in your inbox and calendar, and draft replies for you to approve. It also takes on some of the work of running a business, like finding unpaid invoices and drafting the reminders … It can put together a brief, deck, or dashboard too.」；公告「Claude Duet reads, drafts, and prepares work on its own.」「Check Intuit QuickBooks or Stripe for unpaid invoices and draft reminders.」；產品頁「briefs you every morning, drafts next steps」→ 開場「每天早上先讀你的信箱和行事曆，把該回的信、該催的帳先擬好；要用的簡報先準備好」、片尾「替你讀、替你擬、替你盯」。開場原寫「該退的款」「簡報用最新的數字重做好」：退款（Refunds are drafted）與 Q3 重做的簡報只在產品頁示範裡，開場沒說「示範畫面裡」、又掛在「它每天早上」的一般寫法下，改用公告與 FAQ 的一般功能（催帳提醒＝brief 原本要的「找出沒付的發票」；簡報＝put together a deck）｜A、P｜2026-10-23｜verbs-a, verbs-b, answer

## 與企劃不同的地方

- 開場濃縮丟三個預告（讀完 app 卻不一直看、房仲的看房、檢查器），不是四個：第四個「Anthropic 自己寫下三件不行」拿掉，才能讓開場在 lint 估計的 60 秒以內（現在 52 秒）；第 6 章改由第 5 章最後一句「Anthropic 自己卻寫了三件它不行的事」埋設，loops 表照舊有回收。
- 第 3 章章名從「早上 5 點半，它先讀完了所有 app」改成「她醒來之前，它已經讀完所有 app」（查核第 1 輪再改成「她開口之前」，見 c11）：示範畫面上 5 點半是 Marlo Pulse 的更新時間（第 7 章揭曉），簡報材料的時間戳是 5:48，章名照示範的時間說。
- 第 1 章拿掉「手機上的兩個按鈕（不畫字）」那張：畫面規則不畫螢幕，兩個按鈕沒有字就看不出是按鈕；許可表格那張併進「拇指按下去」的鏡頭（縮圖用這張，手機正面背對鏡頭）。
- 第 2 章的 `big`「自己的雲端電腦」改成兩張 shot（圍裙口袋、後台辦公室），插圖比例才過半。
- 第 3 章晨間簡報的 `bullets` 只放她沒看過的三條（Jenn、Northfield、27 筆錯單）：芝加哥第 1、2 章講過，Series A 第 5 章用 Elena 的信帶出，不重講。
- 第 5 章 `big`「新的分類器」拆成一張 shot（海關開包裹，定義分類器）加一張 `big`（信用卡號、證件號碼預設不給），原來兩句在一張卡上估計 12 秒。
- 第 5 章 `steps` 前多一句問句「那替公司買東西的時候，錢怎麼付？」，不然 5:22–6:53 之間 90 秒沒有鉤子。
- 第 7 章 `cta` 放在示範結束（「她自己只回了三句話」）之後、`steps` 之前，照啟動訊息「主例之後一張 cta」；企劃排在 steps 之後。
- 第 6 章 `bullets` 三條（跑腿訂票、看不到瀏覽器、兩次檢查之間漏掉），企劃列四條：「可能誤判急不急」放在章首句，因為它在公告裡是前一句、不是「不行」清單的一項。
- 三位測試者只有 Jess 和 Amin 有 `quote` 卡；Mya 用兩張 shot 帶過、旁白不唸她的名字（跟 Maya 同音）。Anthropic 內部員工（Claude Code 負責人散步講待辦等）整段不用。
- 競品名單、八個連接器清單都不出現在旁白，也沒放卡片（企劃說「卡片可放」）：第 6 章已經有 `table`，再加一張名單卡會變成唸目錄。
- 片尾第一句沒有數字：開場的問題是「替你做了什麼、在哪裡停下來」，答案是動作（讀、擬、盯／寄出付錢簽名刪除之前停）不是數字；數字（640、四件、兩件）正文都講過，不重播。

## 我懷疑但沒動的事

- 示範畫面的日期是 10 月 19 日星期一，公告是 10 月 21 日：示範的「今天」在公告前兩天。旁白只說「星期一早上」，不說日期；副標寫公告日期。查核時可考慮要不要在說明欄點明。
- 「它在她醒來前讀完所有 app」：示範只有 5:48／5:52 的更新時間戳和 9:41 的簡報，沒有一句寫「它讀完了所有 app」；這是把公告「Each morning, it sends you a short brief on the most important items across your connected apps」套在示範上。查核若覺得太強，可改成「它在她醒來前就把簡報準備好」。
- pay-rules 第三條「延誤只告知，不問你」是從 FYI 那一句示範整理的，公告沒有這條規則；卡片 source 寫了「示範」。
- 「連接器就是讓它接上某個 app 的接頭」「分類器就是只做一件事的檢查程式」是白話解釋，公告沒有定義句。
- 「找得到洞的人有賞金」對應 public bug bounty program，沒講金額（公告沒寫）。
- 第 6 章「Muse 要替你去買東西」引的是前一支影片的事實（The Verge），本片 sources 沒列 The Verge；說明欄提了前一支。
- 片尾 outro 三句在一個畫面上估計 16.6 秒（lint 警告）：規則要求結尾三句共用一個畫面，姊妹片一樣；合計 64 字已經比規則的「約 45 個口語單位」長，再砍就只剩訂閱句。
- Jess 引言卡片保留原文的「[This is]」方括號：公告原文如此，旁白不唸它。
- Marlo Pulse 旁白略去 CRM（示範寫 point of sale, Shopify, CRM, support inbox, payroll and bank）：CRM 在旁白會多一個要進字典的縮寫，卡片也沒放；若查核要求完整，加「客戶名單」三個字。

## 查核第 1 輪（2026-10-23）

公告、產品頁、TechCrunch、Mokaair 文章、The Verge（Muse）重新以 curl 抓取，全部 HTTP 200；公告與產品頁的位元組數與撰稿時存檔相同。逐句表在 `verify-1.md`。
除上面 c11、c13、c16、c20、c24、c25、c28、c29 記下的改動外：

- youtube.title 原寫「Claude Duet 付了 640 美元，然後停下來等她」，順序反了：示範是先停下來等她按核准、才付，付完它沒有停（第 2 章自己就說「付完它不停在那裡」），改「Claude Duet 付 640 美元之前，先停下來等她」。
- 「我懷疑但沒動的事」逐條結論：示範日期 10 月 19 日不唸，維持；「醒來前讀完所有 app」已改（c11）；「延誤只告知，不問你」由示範 FYI 那句支持、卡片 source 有標示範、旁白主詞是「她」，保留；兩句白話解釋不是事實主張，保留；賞金沒講金額，保留；Muse 一句已用 The Verge 重新核對（c25）；outro 16.6 秒是 lint 警告、屬節奏，不動；Jess 引言方括號照原文，保留；Pulse 略去 CRM 不構成錯誤，保留。

## 進度

- 2026-10-23：video.json 全部 71 個場景、102 句寫完，lint 0 錯誤、1 警告（outro 16.6 秒）；估計 9.7 分鐘、2,076 個口語單位；開場章 52 秒；shorts.json 兩支寫好；lexicon.json 加了 19 個詞。
- 待：查核代理逐條核對 c1–c31；站主核准大綱門（status 顯示 outline 尚未 approve）；試聽字典裡 null 的人名。

## 說故事關卡之後的改動（2026-10-23，協調者）

- 聽稿修正（兩輪查核後）：tv2w 不再重講按核准、idkx／tf3w／xg4i 把「它自己說」改成 Anthropic 說、x98u／xxgv 只講一次她打的那句、xg4i 與 k2un 之後整段刪掉。
- 第一輪盲評 63 分、過六題（開場 uyam 講掉第三章、第四章三位試用者像見證清單、第六章像規格表、片尾重述規則）。改動：uyam 改成「它早上五點多就動過她的募資簡報」、刪 airport-gate／brief-folder（品牌策略顧問）、kebab-office／kebab-counter／amin-quote（Amin；c20 仍在上表，影片不再講）、ticket-counter／runner-bags（Muse 對照，站主觀點那句移到說明欄）、red-team（ju3e，紅隊與賞金只留在說明欄）、wrong-table（2cwq 併進 idkx）；reach 卡拿掉 Opus 5.5 那一列（標題卡副標仍有）、who-can 表改成兩張 shot（waitlist-queue：txf4；coin-stacks：732w 改成點名回呼），pkhi（平台）與 xbgf 刪；第 5、6 章章名改成事件；片尾 tscq 改成「你點頭之前的全部」；2cae 把 Valencia 週末與 East Bay 流失分開講。
- 補兩個示範細節撐長度與插圖占比（都在產品頁示範的 Series A 段）：data-room（kytd：資料室 26 份進 23 份、缺的拉兩份、董事會紀錄要她簽）、partner-bios（bpad：讀了 Harbor 六位合夥人簡介、擬好兩題答案）。來源同 c-series 的產品頁示範，查看日 2026-10-23。
- 第二輪盲評 70 分（過八題）、第三輪 72 分（過八題；三位讀者各自要的不一樣：第六章的限制清單與 Jess 那一章被兩位判為岔路，但那是企劃要的內容）。第三、四輪改動：twih 不再指向開場、data-room／partner-bios 移到第三章（五點多它做的事）、第五章從那封信開場、kymh 不再預告「三件」、wi95 不說「第三步」、sr5u／vxnr 不重講花錢規則、b4qu（sorting-trays）刪、2cae 把 Valencia 的漏水交代清楚、7y97 第一句就介紹 Marlo、tv2w 補「過了就失效」、pay-rules 卡改成兩張 shot（coins-tray、next-door）讓插圖占比回到一半。之後直接合成旁白，沒有再評第四次；三次裁決都在工作區 `review/narrative.json`，交給站主在後台判。


## 紙底版（2026-10-23）

照 brief.md「新規則版（2026-10-23）」重做：`theme: "paper"`、沒有 `shot`、一個概念（主動式代理）、一個對照（每天早上先把東西放到你桌上的助理）、章名是觀眾的問題。事實全部沿用上表 c1–c31，沒有新增事實；示範數字每章最多唸兩個，其餘留在卡片。每個場景的 `claims` 照舊列 c-id。

### 每章用到的 c-id

- 開場「Claude Duet 是什麼？」（open、naive、verbs-a、verbs-b、stakes、promise）：c8（公告日期、研究預覽）、c9（方向反過來）、c32（讀信箱和行事曆、擬回信、擬催帳提醒、備好簡報；查核第 3 輪由 c10／c19／c11 的示範改成一般功能）、c12（每天早上一份簡報）、c6（付款前先問）、c7（碰得到你的信和錢的理由）、c20、c14（承諾句點名的兩件、額度規則）。
- 「它跟 Claude 差在哪？」（reversed、assistant、demo-page、morning-msg、cloud、same-account、connectors）：c9（Claude 等你開對話、Duet 先來找你；同一帳號的記憶、技能、連接器）、c7（做完或要你看才通知；自己的雲端電腦和瀏覽器、手機關了也照做）、c12（助理對照：便條＝簡報，是把公告的「brief」套在對照上，不是事實主張）、c1（示範畫面 9:41「Morning, Maya. 5 things in progress and 2 that need you.」；`demo-page` 是產品頁示範區塊的真實擷圖，`morning-msg` 的中文是這句的翻譯）、c13（6,000 多個連接器與外掛）。
- 「它什麼時候會來煩你？」（thirty、today、brief、quiet、why-not、limits、my-rule、tell-it）：c14（每幾個小時看一次；一直看會用光額度；你可以告訴它要聽什麼、多久一次）、c15（共用 Pro／Max 額度、背景檢查算進去）、c10（晨間簡報三條：Jenn 的 offer 下午六點到期、Northfield 續約要 Net 60、27 筆錯單退款擬好——旁白不唸數字，卡片也只寫「要改付款條件」）、c11（募資簡報用第三季數字重做、兩頁要她看——旁白說「有幾頁」）、c24（FAQ：兩次檢查之間進來的可能漏掉）、c30（我的看法：先看它多久看一次再決定讓不讓它盯信箱）、c12（「貼紅標籤的才要你動手」是 c4／c12 三分法套在對照上）。「一早三十則通知」「自己開信箱、行事曆、QuickBooks 三個 app」是觀眾生活的對照與玩笑，不是來源事實。
- 「錢會不會被它花掉？」（money-q、permit、paid、four、send-from-you、two、classifier、link、two-lists）：c2（640 美元、核准鍵八分鐘內有效）、c3（付完向郡政府要 11 月 6 或 7 日驗收）、c5（咖啡機延到 11 月 10 日，FYI 只告知）、c6（四件一定先問、把要做的原樣給你看）、c19（寄給 Harbor 的 Elena、「從你這裡寄出？」、她按送出）、c20（連核准也不做：買賣證券、帳戶間轉帳——旁白用「有幾件…像」，不說只有兩件；卡片 numeral 02 指這兩件）、c21（分類器：信用卡號、政府證件預設不給；健康、個人財務要明說才送）、c22（Link 三步、虛擬卡）、c30（兩張清單比功能表重要）。
- 「真的有人在用嗎？」（jess、showing、jess-quote、amin、amin-quote、judgment）：c16（Jess、每天早上一份簡報、沒被問就標出排錯日期的看房、引言原文）、c18（Amin、約 110 名員工、會計客服行銷、一家店一家店過發票、「不用再開一百個分頁」）、c12（整個設計繞著一個判斷：需要你、可以等、先問你）。c5bz「提醒是你先設好的」是觀眾現在做法的對照（§三），不是對任何產品的事實主張。
- 「它不行的三件事，誰能用？」（misread、not-ready、muse、who、big-tasks、taiwan）：c24（可能讀錯討論串、看錯哪件事急；跑腿訂票沒那麼強、看不到瀏覽器）、c25（Muse 要替你去買東西；兩家把線畫在不同地方）、c8（美國 Pro／Max 候補、Team／Enterprise 還沒有、手機 app 與網頁）、c29（台灣的帳號還輪不到）、c15（財務模型、簡報這種大任務花更多）、c30（不確定候補會不會開到台灣：公告沒寫；不用急）。
- 「現在先做什麼？」（three-steps、answer、answer-stop、ask、closing）：c9（沿用同一帳號的記憶、技能、連接器）、c20（接上的 app 隨時可以斷開）、c14（告訴它要聽什麼、多久一次）、c30（我會先整理乾淨）、c6（寄出、付錢、簽名、刪除之前停下來）。

### 這一版沒用到的 c-id 與原因

- c4（開幕清單 41／33／7／1）：數字多，每章只唸兩個，640 和四件優先；三分法（做掉的、盯著的、要你的）改用對照的紅標籤講。
- c17（Mya）：跟 Maya 同音，企劃新規則版第 4 章只點名 Jess；Amin 補進來是為了長度與「你早上那三個 app」的對照。
- c23（紅隊、滲透測試、賞金）：只在說明欄。
- c26、c27、c28（Marlo Pulse 那一頁與數字、East Bay 流失、免運測試）：短片一個概念，Pulse 那一段是第二個例子，整段不用；說明欄也不提。
- c31（Mokaair 文章）：沒有 `cta` 卡（短片版型沒有中段 cta），文章連結照舊由工具加在說明欄第一行。
- c1 的「Monday, October 19」：只在產品頁擷圖上，旁白與卡片都不寫日期。

### 與新規則版企劃不同的地方

- 開場動詞清單的「找出沒付的發票」改成「擬退款」「重做簡報」：claims 裡沒有「沒付的發票」這條事實，退款（c10）與簡報（c11）有。查核第 3 輪改回：公告（Check Intuit QuickBooks or Stripe for unpaid invoices and draft reminders）與產品頁 FAQ（finding unpaid invoices and drafting the reminders）都有這條，退款與 Q3 重做的簡報只在示範裡，開場是一般寫法、沒說「示範畫面裡」；現在是「擬催帳」「備好簡報」（c32）。
- 第 5 章的三件不行照企劃寫「跑腿訂票、看不到瀏覽器、看錯哪件事急」；FAQ 的「兩次檢查之間漏掉」挪到第 2 章當概念卡的「坑」。
- 第 4 章加了 Amin（c18）一張 big、一張 quote：只有 Jess 時這一章 41 秒、全片 6.9 分鐘，不到 8 分鐘下限。
- 結尾：答案與留言題各一張 `big`（answer、answer-stop、ask），`outro` 只剩訂閱句，每個狀態才壓得進 8 秒；lint 因此警告 outro 只有一句。
- 承諾句是 brief 寫的那一句（四件、兩件、一條規則、三件），lint 在前 60 秒報「像目錄」一次，照任務說明保留。
- 縮圖 `capture` 用 `demo-page` 那張產品頁示範擷圖；render 若擷不到就改回純字 `thumb`。

### 我懷疑但沒動的事

- `demo-page` 的 `focus` 用 `[data-part="screen"]`（產品頁示範手機的螢幕），產品頁改版就會失效；`mask` 的同意橫幅用 `[class*="ConsentContainer"]`、`optional: true`。
- 「這個助理的工時算你的」「他沒有你的印章和存摺」「不讓你看他現在在哪裡」是對照的部位，對應 c14／c15、c20、c24，卡片 `source` 標的是公告。
- 「Link 要你親自核准，不是它替你點頭」：原文「Link asks you to approve the spend」，「不是它替你點頭」是這句的反面說法。
- 「貼紅標籤的才要你動手」：示範的 2 that need you 與清單的 1 needs you today 都是「要她的」那一類，紅標籤是對照的畫法。

### 進度

- 2026-10-23 紙底版：video.json 47 景、73 句、66 個狀態，lint 0 錯誤、2 警告（開場承諾句被判像目錄、outro 只有一句）；估計 8.3 分鐘、1,836 個口語單位；開場章 49 秒；shorts.json 兩支重寫（validate 0 錯誤）；lexicon.json 加 QuickBooks（null）。render（`--channel msedge`）第一輪報 5 個版面問題（four／two 的 numeral 卡字太長、three-steps 標題放不下），改短後第二、三輪 exit 0：66 個狀態、`demo-page` 擷到產品頁示範手機的晨間簡報（screencast key ed6f9ee4b83810cb）、縮圖右側就是那張擷圖。

### 查核第 3 輪（2026-10-23，紙底版）

公告、產品頁、TechCrunch、The Verge 重新以 curl 抓取，全部 HTTP 200；腳本靠的 84 句原文逐句在今天的頁面上找到（公告位元組數比存檔少，差在頁尾的相關文章，正文沒變）。逐句表在 `verify-3.md`。改動（旁白句 id 不變）：

- 開場 t4jn／um6i 與 verbs-a／verbs-b 卡片、說明欄第一段：退款與「用最新的數字重做」的簡報是示範，改一般功能（c32）。
- 5p54 與 same-account 副標：比喻停下來的那一點寫反了（c9）。
- nna4 與說明欄：「現在能排候補的，只有美國的 Pro 和 Max」「候補只收」改「先開給」：公告寫 starting with，第 1 輪已確認看不出候補表單擋不擋美國以外的人（c29）。
- is38 與 not-ready 標題：「它（自己）寫下三件還不行」改「Anthropic 寫下」：前一句的「它」是 Duet，寫下這三件的是 Anthropic 的公告（c24）。
- c5bz 與關鍵句：「她什麼都沒設」改「她什麼都沒交代」：原文只有 without being asked，沒說她有沒有設提醒（c16）。
- 關鍵句三處：connectors「接得上的連接器超過 6,000 個」改「連接器和外掛，超過 6,000 個」（c13）；two「買賣證券、轉帳」改「證券、帳戶間轉帳」（c20，同第 2 輪縮圖的理由）；muse「Duet 不跑腿」改「Duet 跑腿沒那麼強」（c24／c25，aren't quite as strong）。

### 查核第 4 輪（2026-10-23，紙底版）

公告、產品頁、TechCrunch、The Verge 重新以 curl 抓取，全部 HTTP 200（公告與產品頁位元組數與第 3 輪相同）。第 3 輪改動的 9 條、協調者縮短的 s89f／5p54／pbw7／vt9x／is38、第 3 輪確認項目隨機抽 17 條，共 31 條全部在今天的頁面上找到原文，沒有改動。逐句表在 `verify-4.md`。two 卡大字「證券、轉帳」只靠同卡副標限定成帳戶間，記在 verify-4 的懷疑事項，沒動。
- 紙底版旁白（2026-10-23）：第一次合成 7:45 正文（成片含片頭片尾 8:11），聽檢 4 句被標（核准→和潤、擬好、她／他、像／想）改措辭後第二次 0 句被標；qa 9／11（旁白等站主、policy：Jev 符合立場 0.57、有示範 0.46）。成片關卡已重送。

