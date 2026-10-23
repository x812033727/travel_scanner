# 查核第 1 輪：claude-duet-proactive-agent

查核日 2026-10-23。獨立查核代理，非撰稿者。所有頁面以 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 重新抓取，同一主機間隔至少 1 秒，去掉 `<!-- -->` 後比對原文；網頁搜尋 0 次。

| 代號 | URL | HTTP |
|---|---|---|
| A | https://claude.com/resources/articles/claude-duet （公告，October 21, 2026） | 200 |
| P | https://claude.com/product/claude-duet （產品頁：示範畫面＋FAQ） | 200 |
| T | https://techcrunch.com/2026/10/22/claude-duet-app-is-anthropics-bet-on-agents/ | 200 |
| M | https://mokaair.com/zh-TW/life/ai-news-claude-duet-20261022 | 200 |
| V | https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping （只為 Muse 一句） | 200 |

A 與 P 抓回的位元組數與撰稿時 `_tools/sources/` 的存檔完全相同（573,949／434,035），撰稿後頁面沒改版。比對用的腳本在 `<VIDEO_WORKDIR>/claude-duet-proactive-agent/_tools/verify/`（`grep.mjs` 逐句找原文、`listener.mjs` 聽感檢查）。

## 逐條表

| # | 主張 | 位置 | URL | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| 1 | 標題：付 640 美元與停下來等她的先後 | youtube.title | P | 200 | CHANGED | 「Claude Duet 付了 640 美元，然後停下來等她」→「Claude Duet 付 640 美元之前，先停下來等她」（示範是先等核准才付；付完它沒停） |
| 2 | 說明欄：Maya、Marlo 咖啡連鎖是示範；640 美元、41 項、52.8 萬 | youtube.description | P | 200 | CONFIRMED | |
| 3 | 說明欄：公告 2026-10-21〈Introducing Claude Duet〉；TechCrunch 2026-10-22 | youtube.description | A、T | 200 | CONFIRMED | |
| 4 | 說明欄：候補只收美國 Pro／Max；Team、Enterprise 還沒有；每幾個小時；額度共用 | youtube.description | A、P | 200 | CONFIRMED | FAQ「a research preview on a waitlist for Claude Pro and Max subscribers in the US」 |
| 5 | 說明欄：Shopify 視覺編輯器、1Password 登入「即將推出」 | youtube.description | A | 200 | CONFIRMED | 「Coming soon, a richer visual editor」「Coming soon … logins you've saved in 1Password」 |
| 6 | tags（Opus 5.5 等） | youtube.tags | A、P | 200 | CONFIRMED | |
| 7 | 縮圖「付錢前先問你」 | thumbnail.headline | A | 200 | CONFIRMED | makes a payment → waits for your approval |
| 8 | 縮圖「轉帳連核准都不做」 | thumbnail.sub | A、T | 200 | CONFIRMED | 原文是 moving money between accounts（見未改的疑點） |
| 9 | 副標：公告 2026-10-21、研究預覽 | hook.data.subtitle | A | 200 | CONFIRMED | |
| 10 | 星期一 9:41，Maya 的手機跳出訊息 | 7y97 | P | 200 | CONFIRMED | 「Monday, October 19」「9:41」「Claude Duet now」 |
| 11 | 早安，五件事在進行中，兩件需要你 | t5gp | P | 200 | CONFIRMED | 「Morning, Maya. 5 things in progress and 2 that need you.」 |
| 12 | 芝加哥新店衛生許可 640 美元，核准或等等，她按了核准 | iuiv | P | 200 | CONFIRMED | 「The health permit needs your OK and $640」「Approve／Not now」→「Paid」 |
| 13 | Claude 等你問，Duet 先找你 | tvfg, vuvp, reversed.data | P、A | 200 | CONFIRMED | FAQ「The Claude app waits for you to open a chat … Claude Duet comes to you.」 |
| 14 | 它在她「醒來前」讀完所有 app | uyam | P、A | 200 | CHANGED | 「她醒來前」→「她開口前」：示範沒寫她何時醒、在睡；對話串由 Duet 先開口 |
| 15 | 一位房仲的「簡報裡」，一場看房它沒被問就標出來 | vywz | A | 200 | CHANGED | 「一位房仲的簡報裡」→「一位房仲的行事曆上」：公告只寫 on her calendar for the wrong day，沒說是在 rundown 裡 |
| 16 | 檢查器，每則訊息送出前都要過 | 25tv, yx9s | A、T | 200 | CONFIRMED | 「checks each message and guards against leaks」 |
| 17 | 第 2 章章名：付完 640 美元，它自己去約驗收 | ch2.chapter／data | P | 200 | CONFIRMED | |
| 18 | 核准鍵八分鐘內有效 | tv2w | P | 200 | CONFIRMED | 「$640.00 Expires in 8 min」 |
| 19 | 下一關驗收，向郡政府要了 11 月 6 或 7 號 | zdvw | P | 200 | CONFIRMED | 「Paid. Inspection is the next gate. I asked the county for Nov 6 or 7.」 |
| 20 | 開幕清單 41 項，從前兩次開店整理 | qwrm, checklist.data | P | 200 | CONFIRMED | |
| 21 | 33 完成或在軌道上 | 8c53, checklist.data | P | 200 | CONFIRMED | |
| 22 | 7 項它盯著 | bwtx, checklist.data | P | 200 | CONFIRMED | |
| 23 | 1 項今天要她，就是這張許可 | ybty, checklist.data | P | 200 | CONFIRMED | 「1 needs you today. Health permit: … The fee is $640.」 |
| 24 | 咖啡機安裝延到 11 月 10 日，緊但來得及 | pakt | P | 200 | CONFIRMED | 「slipped to Nov 10. Tight, but it works.」 |
| 25 | 花錢之前一定先問 | wbhr, pay-rules.data | A | 200 | CONFIRMED | |
| 26 | 付完不停，自己接下一關 | qahu, pay-rules.data | P | 200 | CONFIRMED | |
| 27 | 延誤只告知，不問她 | v6xa, pay-rules.data | P | 200 | CONFIRMED | 由示範「FYI: … I'm watching it.」整理；卡片 source 有標示範 |
| 28 | 自己的雲端電腦和瀏覽器 | mdin | A、P | 200 | CONFIRMED | 「virtual machine with its own browser」；FAQ「its own computer in the cloud」 |
| 29 | 手機關了也照做，做完或要她看才通知 | yg84 | A | 200 | CONFIRMED | 「doesn't require your laptop or phone to be on」「notification when the task is complete or needs your review」 |
| 30 | 第 3 章章名「她醒來之前」 | ch3.chapter／data.title | P | 200 | CHANGED | 「她醒來之前」→「她開口之前」（同 #14） |
| 31 | 5:48 她還在睡，簡報的材料已改好 | 3fnd | P | 200 | CHANGED | 「她還在睡，簡報的材料已經改好」→「她還沒開口，募資簡報已經改好」：5:48 是 Series A deck 的時間戳，示範沒有她在睡 |
| 32 | 讀了她連上的每一個 app：信箱、行事曆、訂單、合約 | tiyx | A | 200 | CONFIRMED | 「brief … across your connected apps」「checks your connected accounts」 |
| 33 | Jenn 的 offer 下午六點到期，三位決選者今天都約好 | ndyw, morning-brief.data | P | 200 | CONFIRMED | |
| 34 | Northfield 41 萬美元續約改成 60 天付款 | pzwk, morning-brief.data | P | 200 | CONFIRMED | 「redlined the $410K renewal and want Net 60」 |
| 35 | 週末 27 筆送錯，19 筆 Valencia，退款擬好 | hvg8, morning-brief.data | P | 200 | CONFIRMED | |
| 36 | 每件事分三種：做掉的、盯著的、要她決定的 | b4qu | P | 200 | CONFIRMED | 取自清單「done or on track／watching／needs you」 |
| 37 | 設計繞著判斷：什麼需要你、什麼可以等、什麼先問 | qmxd | A、P | 200 | CONFIRMED | 「decide what needs you, what can wait, and when to check with you first」；P「Built for judgment」 |
| 38 | 能接的 app 超過 6,000 個 | gd58 | A、P | 200 | CHANGED | 「它能接的 app 超過 6,000 個，接上的就叫連接器」→「它能用的連接器和外掛超過 6,000 個，連接器就是接上 app 的接頭」 |
| 39 | 6,000+ 連接器與外掛，Claude Marketplace | reach.data | A | 200 | CONFIRMED | |
| 40 | 背後的模型 Opus 5.5 | 5ap2, reach.data | A、P | 200 | CONFIRMED | |
| 41 | 每隔幾個小時才再看一次 | mpj2, reach.data | A | 200 | CONFIRMED | 「checks your connected accounts every few hours」 |
| 42 | 用 Pro／Max 額度，背景每看一次都算 | rnbz, limits.data | A、P | 200 | CONFIRMED | |
| 43 | 一直看額度很快用光，平常的 Claude 也沒得用 | 3n3p | A | 200 | CONFIRMED | 「use up your plan's limits much faster」＋「shares … with the rest of Claude」的推論 |
| 44 | 可以告訴它要聽什麼、多久回報 | 9bu2, three-steps.data | A | 200 | CONFIRMED | |
| 45 | Anthropic 先交給一批小老闆試用 | nuzq | A | 200 | CONFIRMED | 「We gave small business owners and entrepreneurs early access」 |
| 46 | 房仲 Jess 每天早上收一份簡報 | 2zqd | A | 200 | CONFIRMED | 「Jess gets a rundown from Claude Duet each morning」 |
| 47 | Jess 引言逐字、Jess Provencher（Pro Homes） | jess-quote.data | A | 200 | CONFIRMED | 「[This is] exactly the kind of thing I want caught without having to ask」 |
| 48 | 看房日期排錯、她沒問過它 | emm7, 7sd4 | A | 200 | CONFIRMED | |
| 49 | 品牌策略顧問，行事曆上有一通潛在客戶的電話 | qbwk | A | 200 | CONFIRMED | 「Mya Dalton, a brand strategist」 |
| 50 | 先準備簡報，發現電話在班機前，主動提議改時間 | rxcy | A | 200 | CONFIRMED | |
| 51 | 南佛州烤肉串店老闆 Amin，約 110 名員工 | d3za | A | 200 | CONFIRMED | 「Shahs of Kabob in South Florida with about 110 employees」 |
| 52 | 會計、客服、行銷，一家店一家店過發票 | c4gk | A | 200 | CONFIRMED | |
| 53 | Amin 引言逐字、Amin Ebrahimi（Shahs of Kabob） | amin-quote.data, hbmy, yzpc | A | 200 | CONFIRMED | 「It brings it all together」「I don't need to open up 100 tabs.」 |
| 54 | 給投資人 Elena 的信 | sy85 | P | 200 | CONFIRMED | 「To: Elena, Harbor Ventures」 |
| 55 | 寄給 Harbor 的 Elena；擬好附資料室連結，從你這裡寄出？ | u85t, gqac, send-from-you.data | P | 200 | CONFIRMED | |
| 56 | 她按了送出 | nvj7 | P | 200 | CONFIRMED | 「Not now／Send」→「Sent」 |
| 57 | 一定先問的四件：寄訊息、付款、簽文件、刪除 | must-ask.data, vxnr, sr5u | A | 200 | CONFIRMED | |
| 58 | 寄之前把要寄的原樣給你看 | vxnr | A | 200 | CONFIRMED | 「shows you exactly what it's about to do」 |
| 59 | 連核准也沒用的「有兩件」 | tfpe | A、T | 200 | CHANGED | 「連核准也沒用的有兩件」→「連核准也沒用的，公告舉了兩件」：原文「A few things … like」 |
| 60 | 買賣證券、帳戶之間轉帳 | off-limits.data | A、T | 200 | CONFIRMED | |
| 61 | 健康、個人財務要你明確交代才送 | 2jdg, off-limits.data | A | 200 | CONFIRMED | |
| 62 | 分類器：信用卡號、政府證件號碼預設不給 | yjmq, classifier.data | A、T | 200 | CONFIRMED | A「reject … credit card numbers and government identification」；T「by default」 |
| 63 | 走 Stripe 的 Link，先確認品項 | gtie, link-steps.data | A | 200 | CONFIRMED | |
| 64 | Link 要你核准這筆錢 | cvcc, link-steps.data | A | 200 | CONFIRMED | |
| 65 | 虛擬卡付，真正的卡號不給店家 | 9tjm, link-steps.data | A | 200 | CONFIRMED | 「pays with a virtual card, so your real card number isn't shared」 |
| 66 | 紅隊與外部公司滲透測試，公開漏洞賞金 | ju3e | A | 200 | CONFIRMED | |
| 67 | Anthropic 自己寫了三件不行 | kymh, ch6 | A、P | 200 | CONFIRMED | 兩件在公告、一件在 FAQ（見 #68） |
| 68 | 三件不行寫在公告的最後一段 | idkx | A、P | 200 | CHANGED | 「寫在公告的最後一段」→「寫在公告最後一節和產品頁的問答裡」：「兩次檢查之間漏掉」只在 FAQ |
| 69 | 可能讀錯討論串，把不急的當成急的 | 2cwq | A、P | 200 | CHANGED | 「也可能把不急的當成急的」→「也可能看錯哪件事急」：miscalibrate what's urgent 兩個方向 |
| 70 | 跑腿、訂票「不強」，因為為工作做的 | tf3w | A | 200 | CHANGED | 「它自己說不強」→「它自己說沒那麼強」：aren't quite as strong |
| 71 | 卡片「跑腿、訂票這種個人雜事，不強」 | not-ready.data.items[0] | A | 200 | CHANGED | 「不強」→「沒那麼強」 |
| 72 | 還不能即時給你看瀏覽器 | bfkt, not-ready.data | A、T | 200 | CONFIRMED | 「can't yet show you its browser」 |
| 73 | 兩次檢查之間進來的可能漏掉 | ebb3, not-ready.data | P | 200 | CONFIRMED | FAQ「can miss something that arrives between checking in with you」 |
| 74 | Muse 要替你去買東西 | xg4i | V | 200 | CONFIRMED | 「successfully purchase tank tops from Amazon」 |
| 75 | Duet 自己說，它「不擅長」跑腿 | xg4i | A、T | 200 | CHANGED | 「它不擅長跑腿」→「它跑腿沒那麼強」：「不擅長」是 TechCrunch 轉述，句子掛在「Duet 自己說」 |
| 76 | 能排候補的只有美國 Pro 與 Max；Team、Enterprise 還沒有 | txf4, who-can.data | P、A | 200 | CONFIRMED | |
| 77 | iOS、Android 獨立 app，電腦上網頁版 | pkhi, who-can.data | A、P | 200 | CONFIRMED | |
| 78 | 額度共用，背景檢查也算 | 732w, who-can.data | A、P | 200 | CONFIRMED | |
| 79 | 財務模型、簡報這種大任務花更多 | xbgf, who-can.data | A、P | 200 | CONFIRMED | 「require more model turns and background work」 |
| 80 | 台灣的帳號現在排不進候補 | p2wi | A、P | 200 | CHANGED | 「排不進候補」→「還輪不到」：只寫 starting with US；表單擋不擋美國以外的人看不出來 |
| 81 | 片尾「台灣候補還沒開」 | closing.data.lines[2] | A、P | 200 | CHANGED | →「台灣還沒輪到」 |
| 82 | 她打了一句，要一頁每天早上能看的 | x98u, xxgv, one-page.data | P | 200 | CONFIRMED | 「Build me one page I can check every morning. Is the business healthy, and where should I look?」 |
| 83 | 做好了，叫 Marlo Pulse，每天早上 5 點半更新、比簡報早 | h54b, azkb, one-page.data | P | 200 | CONFIRMED | 「It refreshes at 5:30 every morning, before your brief.」 |
| 84 | 從收銀、Shopify、客服信箱、薪資和銀行拉資料 | 48f5 | P | 200 | CONFIRMED | 原文另有 CRM，旁白略去，不構成錯誤 |
| 85 | 本週營收 52.8 萬美元 | cxbi, pulse.data | P | 200 | CONFIRMED | 「Revenue this week $528K」 |
| 86 | 現金 210 萬，14 個月跑道 | iyue, pulse.data | P | 200 | CONFIRMED | 「Cash $2.1M 14 months of runway」 |
| 87 | 同店銷售 +11%，Valencia 週末 −8% | 5487, pulse.data | P | 200 | CONFIRMED | 「Cafés +11% Same-café sales. Valencia weekends −8%.」 |
| 88 | East Bay 訂閱流失率 2.6% → 3.4% | rry8, pulse.data | P | 200 | CONFIRMED | |
| 89 | 健康，但一個地方在漏水：Valencia 週末外送 | 2cae | P | 200 | CONFIRMED | 「Healthy, with one leak: weekend delivery at Valencia.」 |
| 90 | 流失是運費「漲價」之後的事；要不要往下挖 | ig2t | P | 200 | CHANGED | 「運費漲價之後」→「運費調整之後」：原文 after the shipping price change |
| 91 | 多數取消說運費；滿 40 美元免運約留住七成 | 88sr, dig-in.data | P | 200 | CONFIRMED | 「Free shipping over $40 would have kept about 7 in 10」 |
| 92 | 兩週測試；「設起來」 | r4wv, dig-in.data | P | 200 | CONFIRMED | 「Want a 2-week test?」「Set it up.」 |
| 93 | 從那一頁到測試，她只打了三句話 | ii9y | P | 200 | CONFIRMED | Build me one page…／Yes／Set it up（見疑點） |
| 94 | 說明欄文章存在 | pdzz, article-cta.data | M | 200 | CONFIRMED | 頁面 title「Anthropic 推出 Claude Duet：主動式 AI 代理鎖定專業人士與小企業」 |
| 95 | 沿用記憶、技能、連接器，設定幾乎不用做 | jjt4, 4c86, three-steps.data | A、P | 200 | CONFIRMED | 「carries over your memory, skills, and connected apps … requires minimal work」 |
| 96 | 接上的 app 都能隨時斷開 | mgnq, three-steps.data | A | 200 | CONFIRMED | 「disconnect any app Claude Duet has access to」 |
| 97 | 替你讀、擬、盯；寄出、付錢、簽名、刪除之前停下來 | tscq, closing.data | A | 200 | CONFIRMED | 「reads, drafts, and prepares work」＋四件 |
| 98 | 章名：房仲／信用卡號預設不給／三個不行／一頁儀表板 | ch4, draft-letter, ch6, one-page | A、P、T | 200 | CONFIRMED | |
| 99 | sources 的 checked_on | sources[] | A、P、T、M | 200 | CONFIRMED | 四筆都已是 2026-10-23，不用改 |
| 100 | 意見句 w24e、ffsd、k2un、p2wi 後半、4c86 | 見各句 | brief.md | — | OUT OF SCOPE | 與站主觀點一致（見下） |
| 101 | 問句 h2yp、we9p、xesi、w2qj、skzu、h6wf、dz4u 與轉場句 | 見各句 | — | — | OUT OF SCOPE | 不含事實 |

## 摘要

- 查核：主張 101 條；CONFIRMED 84、CHANGED 15 列（10 個事實改動：標題先後、「醒來前／還在睡」、房仲「簡報裡」、6,000 個 app、「有兩件」、「最後一段」、「把不急的當成急的」、「不強／不擅長」、「運費漲價」、「台灣排不進候補」）、NOT FOUND 0（推論說不通的都已改成來源寫得出來的說法，沒有刪句）、OUT OF SCOPE 2 列。
- 會過期的事實：候補只開給美國 Pro 與 Max、Team 與 Enterprise 還沒有、研究預覽（A October 21, 2026；P FAQ 2026-10-23 看到）；每幾個小時檢查一次、額度共用、背景檢查計入（A 2026-10-21）；Shopify 視覺編輯器與 1Password 登入「coming soon」（A 2026-10-21）；6,000+ 連接器與外掛（A、P 2026-10-23）；示範畫面的每個數字（P 2026-10-23；位元組與撰稿存檔相同）。
- 意見不符：沒有。四句「我的看法是」都有標示，內容對得上 brief 的站主觀點；p2wi 事實半句改成「還輪不到」，與觀點「台灣現在還進不了候補，不用急」精神一致。4c86 「先把這三樣整理乾淨」是沒有標「我的看法是」的建議，但在 brief 是第 7 章的練習步驟。brief 的「運費漲價後」與來源不符，已依來源改。
- 聽感：沒有超過 40 字的句子、沒有查證式旁白、沒有括號或網址、所有拉丁字都在字典裡；唯一的聽感疑慮是「簡報」一詞同時指晨間簡報（brief）、Jess 的 rundown、Mya 的 brief 與 Series A 的 deck，3fnd 已改「募資簡報」，其他未動。
- lint：`node tools/video/cli.mjs lint --slug claude-duet-proactive-agent` → 0 errors、1 warning（closing 畫面約 16.6 秒，撰稿時就有，屬節奏）。
- 懷疑但沒改：(1) shorts.json 三處仍寫「她還在睡」「老闆還在睡」（第 52、55、59–60 行），超出本輪可改的檔案，需要撰稿方同步成「還沒開口」；(2) bedroom-first-light、tease-kitchen 的插圖 prompt 仍畫睡著的人，屬畫面；(3) yg84「她收起手機去開店」與 nvj7「她看了一眼」是示範沒畫的戲劇化動作；(4) ii9y「打了三句話」的 Yes 可能是點按鈕；(5) qbwk「品牌策略顧問」原文是 brand strategist，沒說是顧問；(6) d3za「一家烤肉串店」但下一句「一家店一家店」，Shahs of Kabob 有多家店；(7) 縮圖「轉帳」原文是帳戶之間轉帳；(8) wbhr「Duet 的第一條規則」是影片自己的編號，公告沒編號；(9) 說明欄「候補只收美國」依 FAQ 的寫法，表單實際擋不擋看不出來。
- 第二輪：需要（本輪 10 個事實改動，超過 3 個）。
