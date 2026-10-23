# 查核第 2 輪：claude-duet-proactive-agent

查核日 2026-10-23。獨立查核代理，不是撰稿者，也不是第 1 輪的查核者。範圍照規則：第 1 輪 CHANGED 的 15 列全部重查，加上第 1 輪 CONFIRMED 的 84 列隨機抽三分之一（28 列，`<VIDEO_WORKDIR>/claude-duet-proactive-agent/_tools/verify/round2/sample.mjs` 用 Math.random 抽，結果存在同資料夾 `sample.txt`），再加上第 1 輪留下的九個疑點所在、抽樣沒抽到的 5 列（#25、#29、#51、#56、#93）。

所有頁面以 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'` 重新抓取，同一主機間隔至少 1 秒，去掉 `<!-- -->`、`<script>`、`<style>` 後比對原文；網頁搜尋 0 次。比對與改檔用的腳本在 `<VIDEO_WORKDIR>/claude-duet-proactive-agent/_tools/verify/round2/`（`totext.mjs`、`sample.mjs`、`edit.mjs`、`edits.json`）。

| 代號 | URL | HTTP | 位元組 |
|---|---|---|---|
| A | https://claude.com/resources/articles/claude-duet （公告，October 21, 2026） | 200 | 573,949（與撰稿存檔、第 1 輪相同） |
| P | https://claude.com/product/claude-duet （產品頁：示範畫面＋FAQ） | 200 | 434,035（與撰稿存檔、第 1 輪相同） |
| T | https://techcrunch.com/2026/10/22/claude-duet-app-is-anthropics-bet-on-agents/ | 200 | 232,781 |
| M | https://mokaair.com/zh-TW/life/ai-news-claude-duet-20261022 | 200 | 460,937 |
| V | https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping | 200 | 428,943 |

## 逐條表

「第 1 輪 #」沿用 verify-1.md 的編號。

### 第 1 輪改過的 15 列（全部重查）

| 第 1 輪 # | 主張（現在的寫法） | 位置 | URL | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| 1 | 「Claude Duet 付 640 美元之前，先停下來等她」 | youtube.title | P | 200 | CONFIRMED | 「The health permit needs your OK and $640」→ Approve（data-tap="permit"）→ Paid |
| 14 | 「它在她開口前讀完所有 app，卻不一直看」 | uyam | P、A | 200 | CONFIRMED | 對話串由 Duet 的「Morning, Maya…」開頭；A「checks your connected accounts every few hours」 |
| 15 | 「一位房仲的行事曆上，一場看房它沒被問就標出來」 | vywz | A | 200 | CONFIRMED | 「without being asked, it flagged a property showing that was on her calendar for the wrong day」 |
| 30 | 章名「她開口之前，它已經讀完所有 app」 | ch3 | P | 200 | CONFIRMED | 同 #14 |
| 31 | 「早上五點四十八分，她還沒開口，募資簡報已經改好」 | 3fnd | P | 200 | CONFIRMED | 「Series A deck Updated 5:48 AM」「Deck: rebuilt with Q3, 12 slides」 |
| 38 | 「它能用的連接器和外掛超過 6,000 個」 | gd58 | A、P | 200 | CONFIRMED | 「can use the over 6,000 connectors and plugins in the Claude Marketplace」 |
| 59 | 「連核准也沒用的，公告舉了兩件：買賣證券、帳戶之間轉帳」 | tfpe | A、T | 200 | CONFIRMED | 「A few things are off-limits even with your approval, like trading securities or moving money between accounts」 |
| 68 | 「三件不行寫在公告最後一節和產品頁的問答裡，前面還有一句」 | idkx | A、P | 200 | CONFIRMED | 公告最後一節「Join the research preview」有跑腿、瀏覽器；FAQ「What isn't ready yet?」有兩次檢查之間漏掉；「前面那一句」＝misread a thread or miscalibrate what's urgent |
| 69 | 「它可能讀錯一條討論串，也可能看錯哪件事急」 | 2cwq | A、P | 200 | CONFIRMED | |
| 70 | 「跑腿、訂票這種個人雜事，它自己說沒那麼強，因為它是為工作做的」 | tf3w | A | 200 | CONFIRMED | 「We built its core functionality around work, so personal errands, such as booking tickets, aren't quite as strong」 |
| 71 | 卡片「跑腿、訂票這種個人雜事，沒那麼強」 | not-ready.data.items[0] | A | 200 | CONFIRMED | |
| 75 | 「Muse 要替你去買東西；Duet 自己說，它跑腿沒那麼強」 | xg4i | V、A | 200 | CONFIRMED | V「successfully purchase tank tops from Amazon」；A「aren't quite as strong」 |
| 80 | 「台灣的帳號現在還輪不到」 | p2wi | A、P | 200 | CONFIRMED | 「starting with US Pro and Max subscribers」 |
| 81 | 片尾「台灣還沒輪到」 | closing.data.lines[2] | A、P | 200 | CONFIRMED | |
| 90 | 「流失是運費調整之後的事。它問她：要不要我往下挖？」 | ig2t | P | 200 | CONFIRMED | 「after the shipping price change. Want me to dig in?」 |

### 第 1 輪確認過、本輪隨機抽到的 28 列

| 第 1 輪 # | 主張 | 位置 | URL | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| 4 | 說明欄：候補只收美國 Pro／Max；Team、Enterprise 還沒有；每幾個小時；額度共用 | youtube.description | A、P | 200 | CONFIRMED | FAQ「a research preview on a waitlist for Claude Pro and Max subscribers in the US. Team and Enterprise plans are not included yet.」 |
| 6 | tags（Opus 5.5 等） | youtube.tags | P | 200 | CONFIRMED | 「Powered by Opus 5.5」 |
| 8 | 縮圖副標「轉帳連核准都不做」 | thumbnail.data.sub | A、T | 200 | CHANGED | 「Claude Duet：轉帳連核准都不做」→「Claude Duet：帳戶間轉帳連核准都不做」：原文只禁 moving money between accounts，付款經核准可以做（示範就付了 640 美元），單寫「轉帳」會把付給別人的錢也算進去 |
| 18 | 核准鍵八分鐘內有效，她按下去，付掉了 | tv2w | P | 200 | CONFIRMED | 「$640.00 Expires in 8 min」→「Paid」 |
| 22 | 7 項它盯著 | bwtx, checklist.data | P | 200 | CONFIRMED | 「7 I'm watching」 |
| 24 | 咖啡機安裝延到十一月十號，緊但來得及 | pakt | P | 200 | CONFIRMED | 「slipped to Nov 10. Tight, but it works.」 |
| 26 | 付完不停，自己接下一關 | qahu, pay-rules.data | P | 200 | CONFIRMED | 「Paid. Inspection is the next gate.」 |
| 37 | 設計繞著判斷：什麼需要你、什麼可以等、什麼先問 | qmxd | A | 200 | CONFIRMED | |
| 41 | 每隔幾個小時才再看一次 | mpj2, reach.data | A | 200 | CONFIRMED | |
| 45 | Anthropic 先交給一批小老闆試用 | nuzq | A | 200 | CONFIRMED | 「We gave small business owners and entrepreneurs early access」 |
| 46 | 房仲 Jess 每天早上收一份簡報 | 2zqd | A | 200 | CONFIRMED | 「gets a rundown from Claude Duet each morning」；「broker and owner」 |
| 47 | Jess 引言逐字、Jess Provencher（Pro Homes） | jess-quote.data | A | 200 | CONFIRMED | |
| 48 | 日期排錯、她沒問過它 | emm7, 7sd4 | A | 200 | CONFIRMED | |
| 49 | 品牌策略顧問，行事曆上有一通潛在客戶的電話 | qbwk | A | 200 | CONFIRMED | 「a brand strategist」「had a call coming up with a potential client」（見疑點 4） |
| 52 | 會計、客服、行銷，一家店一家店過發票 | c4gk | A | 200 | CONFIRMED | 「worked through his invoices store by store」 |
| 58 | 寄之前把要寄的原樣給你看 | vxnr | A | 200 | CONFIRMED | |
| 61 | 健康、個人財務要你明確交代才送 | 2jdg, off-limits.data | A | 200 | CONFIRMED | |
| 67 | Anthropic 自己寫了三件不行 | kymh, ch6 | A、P | 200 | CONFIRMED | |
| 72 | 還不能即時給你看瀏覽器 | bfkt, not-ready.data | A、T | 200 | CONFIRMED | A「can't yet show you its browser」；T「as it happens」 |
| 73 | 兩次檢查之間進來的可能漏掉 | ebb3, not-ready.data | P | 200 | CONFIRMED | |
| 83 | Marlo Pulse，每天早上 5 點半更新，比簡報早 | h54b, azkb, one-page.data | P | 200 | CONFIRMED | 「It refreshes at 5:30 every morning, before your brief.」 |
| 85 | 本週營收 52.8 萬美元 | cxbi, pulse.data | P | 200 | CONFIRMED | 「Revenue this week $528K」 |
| 87 | 同店銷售 +11%，Valencia 週末 −8% | 5487, pulse.data | P | 200 | CONFIRMED | |
| 89 | 健康，但一個地方在漏水：Valencia 週末外送 | 2cae | P | 200 | CONFIRMED | |
| 94 | 說明欄文章存在 | pdzz, article-cta.data | M | 200 | CONFIRMED | title「Anthropic 推出 Claude Duet：主動式 AI 代理鎖定專業人士與小企業」 |
| 97 | 替你讀、擬、盯；四件之前停下來 | tscq, closing.data | A | 200 | CONFIRMED | |
| 98 | 章名（房仲／信用卡號預設不給／三個不行／一頁儀表板） | ch4, draft-letter, ch6, one-page | A、P、T | 200 | CONFIRMED | |
| 99 | sources 的 checked_on | sources[] | A、P、T、M | 200 | CONFIRMED | 四筆都已是 2026-10-23；本輪的改動都依 A／P，日期不用動 |

### 第 1 輪疑點所在、抽樣沒抽到的列

| 第 1 輪 # | 主張 | 位置 | URL | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| 25 | 「這是 Duet 的第一條規則：花錢之前，一定先問她」 | wbhr | A | 200 | CONFIRMED | 「makes a payment … waits for your approval」；「第一條」是影片自己的卡片編號（見疑點 7） |
| 29 | 「手機關了也照做。她收起手機去開店，它做完或要她看，才通知她」 | yg84 | A | 200 | CONFIRMED | 「doesn't require your laptop or phone to be on」「notification when the task is complete or needs your review」；「收起手機去開店」見疑點 2 |
| 51 | 「第三位是南佛州一家烤肉串店的老闆 Amin，大約 110 名員工」 | d3za | A | 200 | CHANGED | 「南佛州一家烤肉串店的老闆」→「南佛州幾家烤肉串店的老闆」：公告寫他「worked through his invoices store by store」，店不只一家，下一句旁白也說「一家店一家店」 |
| 56 | 「她看了一眼，按了送出」 | nvj7 | P | 200 | CONFIRMED | Email 預覽卡＋「Not now／Send」（data-tap="deck-mail"）→「Sent」；「看了一眼」見疑點 2 |
| 93 | 「從那一頁到這個測試，她自己只打了三句話」 | ii9y | P | 200 | CHANGED | 「只打了三句話」→「只回了三句話」：產品頁原始碼裡 Yes 是 Yes／No／Not now 三個快速回覆鈕（`data-tap="chip"`）之一，是點的不是打的；她送出的三則訊息（Build me one page…、Yes、Set it up.）都還在，所以說「回了」 |

## 第 1 輪留下的疑點：本輪判定

1. bedroom-first-light、tease-kitchen 的插圖 prompt 畫睡著的人：不改。對應的旁白（3fnd「她還沒開口」、uyam「在她開口前」）都沒有說她在睡；示範也沒寫她幾點醒，畫面與旁白沒有衝突。shorts.json 仍寫「她還在睡」「老闆還在睡」，超出本輪可改的檔案，撰稿方要同步（第 1 輪已報）。
2. yg84「她收起手機去開店」、nvj7「她看了一眼」：不改。示範沒畫這兩個動作，但也沒有任何一處與它們矛盾；yg84 的事實部分（手機關了也照做、做完或要她看才通知）公告寫得出來，nvj7 的事實部分（看到原樣的信、按 Send、Sent）產品頁寫得出來。屬敘事上的串場。
3. ii9y「打了三句話」：改，見 #93。Yes 是快速回覆鈕。
4. qbwk「品牌策略顧問」vs「brand strategist」：不改。原文沒說顧問，但她的行事曆上是「a potential client」，替客戶做品牌策略，說顧問沒有與來源矛盾。
5. d3za「一家烤肉串店」：改，見 #51。「store by store」與「一家」矛盾。
6. 縮圖「轉帳」：改，見 #8。
7. wbhr「第一條規則」：不改。是影片自己 pay-rules 卡片三條的第一條，卡片 source 標了公告與示範；公告沒有編號，但旁白也沒有說是公告的編號。
8. 說明欄「候補只收美國」：不改。產品頁 FAQ 原文「a research preview on a waitlist for Claude Pro and Max subscribers in the US」，說明欄並註明是 2026-10-23 看到的。

## 摘要

- 查核：重查 48 列（第 1 輪改過的 15 列＋隨機抽到的 28 列＋疑點所在 5 列）；CONFIRMED 45、CHANGED 3、NOT FOUND 0。三個事實改動：縮圖「轉帳」→「帳戶間轉帳」、d3za「一家烤肉串店」→「幾家烤肉串店」、ii9y「打了三句話」→「回了三句話」；claims.md 的 c18、c20、c28 與「與企劃不同的地方」一處引述同步改。
- 第 1 輪的 15 個改動全部成立，沒有被本輪推翻。
- 會過期的事實：候補只開給美國 Pro 與 Max、Team 與 Enterprise 還沒有（P FAQ，2026-10-23 看到；A「starting with」，October 21, 2026）；每幾個小時檢查一次、額度與平常的 Claude 共用、背景檢查計入（A October 21, 2026；P FAQ 2026-10-23）；Shopify 視覺編輯器與 1Password 登入「Coming soon」（A October 21, 2026）；6,000+ 連接器與外掛（A、P 2026-10-23）；示範畫面的數字（P 2026-10-23，位元組與撰稿存檔相同）。
- 意見不符：沒有。w24e、ffsd、k2un、p2wi、4c86 都對得上 brief 的站主觀點；brief 寫「台灣現在還進不了候補」「Duet 自己說它不擅長跑腿」，旁白已依來源寫成「還輪不到」「沒那麼強」（第 1 輪已報，站主決定是否改 brief）。
- 聽感：`listener.mjs` 沒有任何發現（無超過 40 字的句子、無查證式旁白、無括號網址、拉丁字都在字典裡）；lint 也沒有揭曉順序的錯誤。
- lint：`node tools/video/cli.mjs lint --slug claude-duet-proactive-agent` → 0 errors、1 warning（closing 畫面約 16.6 秒，撰稿時就有，屬節奏）。
- 懷疑但沒改：片尾卡「兩件事核准也不做」與 ffsd「連核准也不做的兩件」沒有說只有兩件，保留（公告是「A few things … like」）；tf3w、xg4i、not-ready 卡的「它自己說」說話的其實是 Anthropic 的公告，不是 Duet 本身，屬說法；7y97「咖啡店老闆 Maya」，示範的 Marlo 是 85 人的咖啡連鎖，她是不是老闆是從她拍板付款、募資、署名推出來的；shorts.json 的「還在睡」三處待撰稿方同步。
- 第三輪：不需要（本輪 3 個事實改動，沒有超過 3 個）。
