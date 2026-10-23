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
c9｜FAQ「The Claude app waits for you to open a chat … Claude Duet comes to you.」；「carries over your memory, skills, and connected apps from your Claude account, so setting it up requires minimal work」→ 你以為／其實、沿用記憶技能連接器、設定幾乎不用做｜A、P｜2026-10-23｜reversed, read-everything, same-desk, three-steps, closing
c10｜晨間簡報：「Hiring: Jenn's other offer expires at 6 p.m. All 3 finalists are booked for today.」「Northfield: They redlined the $410K renewal and want Net 60.」「Customers: 27 wrong delivery orders this weekend. 19 from Valencia. Refunds are drafted.」（Net 60 旁白說「60 天付款」）｜P｜2026-10-23｜morning-brief
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

