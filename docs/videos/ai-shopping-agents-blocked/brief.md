# AI 代理已經會替你買東西了，店家為什麼反而把門關上？Muse 被 Amazon 擋下的那一天

企劃日期 2026-10-22。AI／科技時事，插圖說書（`format: "slides"`，`category: "ai-news"`），站內文章
`ai-news-shopping-agents-blocked-20261022`（`source_guide`），搭配 `ai-news-walmart-agent-gateway-20261021`。
事實全部來自 The Verge 2026-10-22 的報導（記者自己用 Meta 的 Muse 代理買東西的過程）、The Verge 2026-09-21
（Amazon 封鎖 Muse）、The Verge 與 TechCrunch 2026-10-21（沃爾瑪 Agent Gateway），以及站上查證過的兩篇文章。
影片裡沒有任何一次是本頻道自己的實測：每一次嘗試都是 The Verge 記者的，旁白要說清楚是誰試的。

## 觀眾

台灣已經在用 ChatGPT、Gemini 或 Meta AI，看到「AI 代理可以幫你比價、幫你下單」的廣告或新聞，想知道這件事現在到底能不能用的人；
也包括開網路商店、在想要不要讓 AI 代理進自己網站的小老闆。他們搜尋的是「AI 代理 購物」「Muse Amazon 封鎖」「AI 幫我買東西 安全嗎」。
他們知道「AI 代理」大概是會自己操作網站的 AI，不知道店家這一邊正在發生什麼：Amazon 把代理擋在外面、Target 的門時開時關、
沃爾瑪反而替代理開了一扇有規則的門。

## 觀眾看完能做到的事

- 看到任何「AI 代理幫你找最低價」的結果時，先問它一句「你進不去哪些店」，並判斷這份比價完不完整：Muse 替記者比穀物棒單價時，
  自己承認 Amazon 可能最便宜、但它被完全封鎖所以無法確認（第 2 章，`quote` 卡，出處 The Verge 2026-10-22）。
- 把一件購物任務交給代理之前，核對三個設定——購買前會不會先問你、能不能設消費上限、能不能隨時接手或關掉——並知道哪一家現在給得出
  哪一個：Meta 說 Muse 一律先徵求許可、使用者隨時可以接手（第 5 章，`quote` 卡）；沃爾瑪的 Agent Profiles 預設每筆核准、可改成在上限內自動買、
  可以隨時刪掉代理（第 6 章，`table` 卡，出處 The Verge／TechCrunch 2026-10-21）。
- 讀到「某某網站封鎖 AI 代理」的新聞時，分得出三種門，並說得出同一個代理在同一家店為什麼一天之內三種結果：全擋（Amazon 的使用條款彈窗）、
  機器人檢查時開時關（Target 發言人：看任務怎麼做、網站有哪些防護，代理可能進得了一部分、進不了另一部分）、正門加規則（沃爾瑪的 MCP 閘道與代理條款）
  （第 3、4、6 章，`compare`／`table` 卡）。

## 站主觀點

（頻道立場的文字沒有隨這次的啟動訊息帶進來，所以這一段是提案，請站主在選大綱時確認或改寫。）
我的看法是：現在讓 AI 代理替你買東西，最大的問題不是它會不會買錯，而是它看得到的店不完整。Amazon 關門的那一天起，
任何「幫你找最低價」的答案都少了一家最大的店，而代理不一定會主動告訴你。所以我把代理當成一個要交代很多事的跑腿：
只派它做我已經知道要買什麼、只差比價和下單的任務；每一筆購買前要它先問我；店家有給設定的，像沃爾瑪的消費上限，一定先設好。
店家這一邊，我認為沃爾瑪那種先把規則寫清楚、每一筆預設要本人核准的做法，比直接封鎖或完全放任都好；Amazon 的理由（代理應該公開運作、
尊重店家要不要參與）我覺得站得住，但它自己也在做代理，所以這是一場生意的攻防，不只是安全問題。

## 示範或實算

製作路線：插圖說書（主題是一個代理在幾家店門口的遭遇，成果是觀眾能作的判斷）。

- 主例（CITED，The Verge 記者的實測，2026-10-22 的報導）：記者在紐約指示 Muse 去 Target 找一罐特定的面霜，某天被 Target 的機器人檢查擋下、
  隔天通過；幾分鐘後問它某價位以下的床墊，又被擋。請它找穀物棒每片的最低價，它給了 Sam's Club、Walmart、Costco，並說 Amazon 可能更便宜但被完全封鎖；
  它還推薦過一家不送到紐約的西岸超市；記者算上等回覆、要它多搜幾家、再澄清送貨範圍的時間，認為自己搜還比較快。這幾段都是記者本人的經驗，
  旁白每一次都要說「The Verge 的記者」，不能說成「我」或「我們測過」。
- 對照（CITED，沃爾瑪官方新聞稿 2026-10-21）：同一週，沃爾瑪宣布 Agent Gateway（用 MCP 讓代理連線，先對企業與開發者開測試版）、
  一個月內推出的 Agent Profiles，與給 AI 代理的條款：預設每一筆購買都要顧客核准，也可以改成在顧客設的上限內自動買（新聞稿的例子是 50、100、200 美元），
  代理的購買分開看、設定檔隨時可以刪掉；條款：不能做超出購物者意圖的事、拿不到付款卡資料、不能新增或改付款方式、只拿得到任務需要且顧客允許的資料、
  違反就封鎖；退貨流程照用，包括代理沒照預期行動的情況；代理看到的價格跟人看到的一樣。TechCrunch 另外寫不用 Walmart+ 會員、Sam's Club 也適用。
  第 6 章一張 `table` 卡把 Amazon（全擋）、Target（看情況）、沃爾瑪（正門加規則）並排，`source` 標「沃爾瑪新聞稿、The Verge 2026-10-21／22」。
- 練習（依報導整理，不是本頻道實測）：第 7 章一張 `table` 卡「交給代理之前先問三件事」——購買前會不會問你、能不能設上限、它進不去哪些店——
  每一列填目前查得到的答案（Muse：一律先問、可接手；沃爾瑪：預設每筆核准、可設上限；Amazon：Muse 完全進不去），`source` 標報導與日期。

## 大綱

### 選項 A：跟著一個 Muse 代理跑一天的腿（推薦）

一行說明：主角是 The Verge 記者的 Muse 代理，照它在幾家店門口的遭遇走：Target 時開時關 → 比價少了 Amazon → 為什麼 Amazon 關門 →
門開著的店它會做什麼 → 沃爾瑪的另一種門 → 觀眾自己要不要把錢包交出去。跟 B 的差別是不從 Amazon 的事件講起，而是從代理被擋的那一刻講起；
跟 C 的差別是不把二手網站那一段當主線。
故事線：實測（記者的，不是本頻道的）
主角：The Verge 記者在紐約派出去買東西的那一個 Muse 代理
主線：這個代理從被 Target 擋下的那一天開始，一路碰到 Amazon 的封鎖、Target 的半開門、二手網站上一件合法卻讓人不安的事，走到沃爾瑪替它這種代理
開的那扇有規則的門，收在觀眾該怎麼決定要不要讓代理替自己買東西。
轉折：
1. 同一家店、同一個代理，一天之內三種結果（第 1 章停在這裡；第 4 章 Target 發言人解釋為什麼）
2. 它比出來的最低價少了一家店，而且是它自己說的（第 2 章）
3. Amazon 在 9 月 21 日對 Muse 跳出一行字，而 Amazon 自己也有代理（第 3 章）
4. 門開著的時候更讓人不安：購物車每 20 分鐘重填一次、填了一整天（第 5 章）
5. 隔天沃爾瑪宣布：代理從正門進，但每一筆預設要本人核准、可以設上限、退貨照退（第 6 章）
開場鉤子：「2026 年 10 月，紐約，一位記者請 Meta 的 AI 代理 Muse 去 Target 找一罐面霜。」
開場濃縮（一個場景）：記者把面霜的名字交給 Muse，Muse 開到 Target 的網站，在門口被機器人檢查擋下來；隔天同一個指令，它進去了；幾分鐘後記者改問
某個價位以下的床墊，它又被擋在外面（停在這裡，不講 Target 怎麼解釋）。轉一句「但這還不是最怪的」，丟四個時刻：它去比穀物棒的價錢，回來的清單少了一家店；
9 月的一個星期天，Amazon 對所有 Muse 使用者跳出一行字；記者讓它去一個二手精品網站做一件規則允許的事，做了一整天；同一個星期，沃爾瑪替代理開了另一扇門。
最後一句：「AI 代理已經會買東西了，店家為什麼反而把門關上？」
鉤子：
- 比價清單少了哪一家、為什麼 → 第 2 章回收
- Amazon 跳出的那一行字 → 第 3 章回收
- 二手網站上做了一整天的那件事 → 第 5 章回收
- 沃爾瑪開的那扇門長什麼樣 → 第 6 章回收
- 同一家店為什麼一天三種結果 → 第 4 章回收
- 門開著的時候代理會做什麼 → 第 5 章回收
- 回到紐約那位記者，面霜值不值得交給它 → 第 7 章回收
你以為／其實：「你以為 AI 代理買不到東西是它太笨 → 其實是店家不讓它進門：Amazon 完全封鎖、Target 時開時關，Muse 比穀物棒價錢時自己承認少了 Amazon」

章節（估計）：
1. 同一家店，一天三種結果（00:00，約 55 秒）— title：報導日期與 Muse；shot：紐約公寓裡一個人把一張寫著名字的紙條遞給跑腿的少年（不畫字）；shot：商店門口的保全攔下
   揹著購物袋的少年；shot：第二天同一道門打開；shot：床墊店門口再次被攔；四個預告各用回收那一章的畫面。收尾：「AI 代理已經會買東西了，店家為什麼反而把門關上？」
2. 比出來的最低價，少了一家店（00:55，約 85 秒）— chapter；shot：少年拿著三張不同超市的收據回來；quote：Muse 自己說 Amazon 可能最便宜但被擋（The Verge 2026-10-22）；
   shot：一箱寄不到紐約的穀物棒；big：記者的結論「自己搜還比較快」（意見，標出處）。收尾：「Amazon 為什麼把它擋在外面？」
3. 9 月 21 日，Amazon 跳出一行字（02:20，約 100 秒）— chapter；shot：星期天早上，手機上跳出一張告示（不畫字）；quote：彈窗原文「未經授權的 AI 代理持續存取違反使用條款」
   （The Verge 2026-09-21）；bullets：Amazon 的三個理由（Meta 沒先通知、Muse 瀏覽時不表明身分、疑似擷取顧客登入資料）；shot：Amazon 自家的跑腿在店內替顧客補貨；
   stats：Amazon 去年 11 月告 Perplexity、法官今年 8 月站在 Perplexity 那一邊、7 月起確認信拿掉品名與圖片；shot：銀行櫃台把代理擋在外面（JPMorgan 執行長說太冒險）。
   收尾：「那門沒鎖的店呢？」
4. Target 的門，看它怎麼進來（04:00，約 70 秒）— chapter；shot：保全對少年說「看你怎麼走」；bullets：Target 發言人的三句（看任務怎麼做與有哪些防護、可能只進得了一部分、
   有防護擋未授權的代理動帳號和交易）；compare：Target 跟 OpenAI、Google、Microsoft 合作 vs 擋 Muse；shot：一道一般的防火牆把所有自動程式都擋下。
   收尾：「門真的開著的時候，它會做什麼？」
5. 購物車每 20 分鐘重填一次，填了一整天（05:10，約 100 秒）— chapter；shot：二手精品店的櫃台，一個人把十件衣服一次抱進試衣間；stats：12 美元月費搶先看、放進購物車保留 20 分鐘、
   10 件最新上架；shot：時鐘走到 20 分鐘，衣服又被抱回試衣間；shot：門外排隊的人；quote：The RealReal 技術長「對第三方代理開放，同時保留防護」；quote：Meta 發言人「Muse 一律在購買前
   徵求許可、使用者隨時可以接手」；big：Meta 說它會拒絕人做不到的事，例如買光一場活動的票。收尾：「有沒有店家乾脆把規則寫清楚，讓代理從正門進？」
6. 沃爾瑪替代理開了正門，但每一筆都要你點頭（06:50，約 100 秒）— chapter；shot：一家大賣場門口新開一道專門的入口，門邊站著發號碼牌的店員；steps：Agent Profiles 的三步
   （第一次用就建立設定檔、連到自己的帳號、設核准方式或上限）；table：Amazon／Target／沃爾瑪三種門並排（`source` 標兩篇報導與日期）；bullets：代理條款四條與退貨照退；
   shot：店員把一袋固定會買的酸種麵包和牛奶交給跑腿，不給他翻購物紀錄。收尾：斷在事件前「回到紐約的那位記者，她最後還是派了 Muse 去找一件東西。」
7. 錢包要不要交給它（08:30，約 75 秒，含 cta 與片尾）— chapter；shot：記者把一疊舊照片交給跑腿，請他找一件古董洋裝；shot：跑腿帶回一張拍賣會的傳單（找不到洋裝，但找到同品牌的拍賣）；
   table：交給代理之前先問三件事；cta：說明欄的文章；outro：三句。
結尾（outro）：「開頭那個問題：門開不開是店家決定的，Amazon 關、Target 看情況、沃爾瑪下個月開，而少了 Amazon 的比價，就不算完整。」「你最想交給 AI 代理買的一樣東西是什麼？」
「訂閱頻道，每一支都給你一個看完就能做的判斷。」

### 選項 B：Muse 上市 44 天，三家店三種門

一行說明：事件型，主角是 Muse 這個產品從 9 月 8 日上市到 10 月 22 日的 44 天：先成功在 Amazon 買到東西，9 月 21 日被封鎖，10 月碰上 Target 的檢查，
10 月 21 日沃爾瑪點名邀請它。跟 A 的差別是照日期走、從 Amazon 事件講起，記者的實測只當第 4、5 章的證據；跟 C 的差別是不把公平性當主題。
故事線：事件
主角：Meta 的 Muse 代理（一個產品）
主線：從 Muse 上市那一天開始，看三家店各自怎麼回應它，走到觀眾該怎麼讀「封鎖 AI 代理」這類新聞。
轉折：The Verge 自己曾用 Muse 在 Amazon 買到背心（第 2 章）→ 9 月 21 日彈窗（第 3 章）→ Amazon 告 Perplexity 卻輸了、自己也在做代理（第 4 章）→ 記者在 Target 與二手網站的經驗（第 5 章）→
沃爾瑪的正門（第 6 章）。
開場鉤子：「2026 年 9 月 8 日，Meta 推出一個會替你上網買東西的 AI 代理，叫 Muse。」
開場濃縮：Muse 上市，The Verge 試用時成功在 Amazon 買到背心；十三天後，同一個代理打開 Amazon，看到的是一張告示（停在這裡）。轉句後丟四個時刻：
一家法院在 8 月對 Amazon 的另一場官司作了判決；一個記者的代理在 Target 門口一天三種結果；一個二手網站的購物車被同一個代理填了一整天；沃爾瑪在 10 月 21 日宣布一件事。
最後一句：「一個代理，為什麼三家店給它三種門？」
你以為／其實：「你以為封鎖 AI 代理是因為它會亂買 → 其實 Amazon 的理由是它不表明身分、沒先通知，而 Amazon 自己平台裡就有代理」
章節（估計）：1. 上市十三天後的那張告示（00:00，50 秒）；2. 它在 Amazon 買到過背心（00:50，70 秒）；3. 彈窗上的那一行字與三個理由（02:00，90 秒）；
4. 告 Perplexity 的那場官司輸了（03:30，80 秒）；5. Target 的門與穀物棒的比價（04:50，100 秒）；6. 購物車填了一整天（06:30，80 秒）；7. 沃爾瑪點名邀請它（07:50，90 秒）；
8. 怎麼讀下一則「封鎖代理」的新聞（09:20，60 秒，含 cta 與 outro）。
結尾：答案同 A（三種門），留言題「你用過哪一個 AI 代理買東西？結果怎麼樣？」

### 選項 C：當代理真的能用，麻煩才開始

一行說明：抉擇型，從二手網站那個「規則允許、卻讓所有人都吃虧」的實驗講起，主角是那一個把購物車填了一整天的 Muse 代理；封鎖與開門是後面才進來的解釋。
跟 A、B 的差別是主題不是「店家擋不擋」，而是「如果每個人都派代理，購物會變成什麼」。
故事線：抉擇
主角：記者在 The RealReal 上那個每 20 分鐘重填購物車的 Muse 代理
主線：從代理成功替記者「合法霸占」十件衣服的那一天開始，走到店家為什麼要擋代理（Amazon、Target），再到沃爾瑪用規則而不是封鎖來處理，
收在觀眾自己要不要派代理、以及店家該用哪一種門。
開場鉤子：「紐約，一個記者叫 AI 代理把一家二手精品店最新上架的十件衣服全放進購物車，然後每 20 分鐘再放一次。」
開場濃縮：購物車保留 20 分鐘、代理整天重填、記者根本不打算買（停在這裡）。轉句後丟四個時刻：同一個代理在 Target 門口的遭遇；Amazon 在 9 月的一個星期天做的事；
Meta 發言人對「人做不到的事」的回答；沃爾瑪的新規則。最後一句：「如果每個人都派代理去搶，店家該把門關上，還是改規則？」
你以為／其實：「你以為店家擋代理是怕它亂買 → 其實是怕它做人做不到的事：整天霸占購物車、買光一場活動的票」
章節（估計）：1. 購物車填了一整天（00:00，55 秒）；2. 門外排隊的是人，門內搶的是程式（00:55，80 秒）；3. Target 的門為什麼時開時關（02:15，80 秒）；
4. Amazon 的那一行字與它自己的代理（03:35，100 秒）；5. Meta 的答案：先問、可接手、拒絕人做不到的事（05:15，80 秒）；6. 沃爾瑪的答案：正門、上限、退貨照退（06:35，100 秒）；
7. 你是買家還是店家（08:15，75 秒，含 cta 與 outro）。
結尾：答案「店家不用二選一：沃爾瑪的做法是門開著、但每一筆預設要本人核准」，留言題「如果你開網路商店，你會讓 AI 代理進來嗎？」

## 會過期的事實

- 沃爾瑪 Agent Profiles「一個月內推出」（launching in the next month，2026-10-21 的說法）與 Agent Gateway「先對企業與開發者開測試版」：撰稿日重查沃爾瑪新聞稿
  https://corporate.walmart.com/news/2026/10/Making-It-Possible-for-Agents-to-Shop-on-Behalf-of-Customers ；The Verge 與 TechCrunch 的報導只當補充
  （不用 Walmart+ 會員、Sam's Club 也適用、執行長在 Masters of Scale Summit 談到）。
- Amazon 是否仍封鎖 Muse、Meta 是否已把 Amazon 從 Muse 移除：https://www.theverge.com/report/1015811/ai-shopping-agents-blocked-amazon-the-realreal-target-meta-muse
- The RealReal 的 12 美元月費搶先看與購物車保留 20 分鐘：同上一篇報導（記者的說法；The RealReal 官網若查得到就改標官網）。
- Amazon 告 Perplexity 的時間（去年 11 月）與法官 8 月的判決：https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping
- Muse 上市日期（2026-09-08 前後，The Verge 寫 earlier this month 相對於 9 月 21 日）：選 B 才需要，撰稿日找 Meta 的官方頁。

## 素材

- The Verge 2026-10-22〈AI agents are ready to shop. Some retailers are wary.〉
  https://www.theverge.com/report/1015811/ai-shopping-agents-blocked-amazon-the-realreal-target-meta-muse （主來源；全文存在
  `<VIDEO_WORKDIR>/ai-shopping-agents-blocked/_tools/sources/verge-shopping.txt`）
- The Verge 2026-09-21〈Amazon blocks Meta's Muse AI agent〉 https://www.theverge.com/tech/998078/amazon-blocks-meta-muse-ai-agent-shopping （`verge-amazon-muse.txt`）
- The Verge 2026-10-21〈Walmart is inviting AI agents to shop for you〉 https://www.theverge.com/ai-artificial-intelligence/1015715/walmart-ai-shopping-agents （`verge-walmart.txt`）
- 沃爾瑪新聞稿 2026-10-21〈Walmart Makes It Possible for Agents to Shop on Behalf of Customers, While Keeping Customers in Control〉
  https://corporate.walmart.com/news/2026/10/Making-It-Possible-for-Agents-to-Shop-on-Behalf-of-Customers （`walmart-corporate.txt`；第 6 章的唯一官方來源）
- TechCrunch 2026-10-21〈While Amazon blocks AI agents, Walmart rolls out the welcome mat〉
  https://techcrunch.com/2026/10/21/while-amazon-blocks-ai-agents-walmart-rolls-out-the-welcome-mat/ （`techcrunch-walmart.txt`）
- Mokaair 文章（查證 2026-10-22）：https://mokaair.com/zh-TW/life/ai-news-shopping-agents-blocked-20261022 ；（查證 2026-10-21）：
  https://mokaair.com/zh-TW/life/ai-news-walmart-agent-gateway-20261021
- 圖：全部由 `shot` 的 AI 插圖提供，不用任何一家公司的 logo、截圖或真人照片；縮圖用最強的一張 shot（建議第 1 章商店門口被攔那一張）。

## 不做的事

- 不講 1Password for Agents、Cloudflare 與 Commerce.com 的 WebMCP：是同一週的新聞，但不是這個代理碰到的事，講了就是岔路。
- 不介紹 OpenAI、Google 的購物代理功能，不比較哪一家的代理比較好：先介紹再比較，而這支片只認識 Muse 一個主角。
- 不評論 Amazon 告 Perplexity 的法律對錯，不給任何購買、投資或法律建議；只講發生了什麼與誰說了什麼。
- 不講 Muse 的其他新聞（下載量、Marketplace 地址外洩、隱私事件）：跟它在店門口的遭遇無關。
- 不把 The Verge 記者的實測講成本頻道的；不說「我們測過」；旁白裡的「我」只用在站主觀點那幾句。
- 不唸各方說法的對照表：Target、Amazon、Meta、The RealReal、沃爾瑪的回應各自在它推進故事的那一章講，誰說的就說是誰說的。
