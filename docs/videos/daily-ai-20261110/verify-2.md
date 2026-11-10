# daily-ai-20261110 查核第 2 輪

查核日 2026-11-10（台北時間）。查核代理不是撰稿人，也不是第 1 輪的查核代理。
範圍：只查第 1 輪之後改過的部分。這一輪是 `git diff 9918a48af HEAD`（「fact and joke check round 1」到 HEAD「clarity and balance revision from the blind read」）的 `video.json`，加上 claims.md〈盲聽修改第 2 輪〉的 c59–c74、拿掉的句子與笑點筆記。差異裡每一句新的或改過的旁白（Sola 與 Kai 都查），以及每張新的或改過的卡片 `data`（含 `kicker`、`key`、`keys`），都逐條對照了來源。`loops` 也一起查了。第 1 輪查過、這輪沒有動的句子不再重查。
來源：站上 4 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，間隔 1.2 秒）都是 HTTP 200、`status: published`、news_date 2026-11-09。`sources` 的 4 個原始來源用 `Mokaair-editorial/1.0` UA 以 curl 重新打開，去掉 `<!-- -->` 後讀全文，全部 HTTP 200、沒有轉址，內容與第 1 輪引的相同。沒有用 web search。
另有〈笑點檢查〉與〈清楚度檢查〉兩節。

## 來源代號

站上文章與原始來源的代號跟 verify-1.md 相同：TRUMP／TV、APPLE／AV、JET／DJ、NYSE／DN。

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 川普上了美國電視新聞節目《60 分鐘》，談 AI 安全（c59） | hk01 | TV | 200 | CONFIRMED（TV 標題「Trump's 60 Minutes interview touched on AI safety」；「新聞節目」是對節目的一般說明） | |
| 2 | 他說，政府警告過一位 AI 公司老闆「準備坐牢」（c59） | hk02；mo-topic | TV | 200 | CONFIRMED（TV 副標「Trump claims the DOJ told a top AI executive, 'get ready to go to jail.'」；句子掛「他說」） | |
| 3 | 用量上限會受你跟 Logic Pro 內建 AI 助理對話的複雜度影響（c60） | a011；ap-complex | AV | 200 | CONFIRMED（「It has a built-in AI assistant」；「impacted by the complexity of conversations you have with the assistant」） | |
| 4 | 川普說，有人向政府舉報某人用 AI 做壞事，政府那邊就很強硬地打電話給對方（c61） | m003；mc-call | TV | 200 | CONFIRMED，留「政府」（原話是「reported to us」「We called them very strongly」。TV 自己把這段的「we」寫成司法部：「He claimed the DOJ is managing that risk, saying, 'We had a situation…'」。「政府」比司法部寬，又掛在「川普說」底下，所以沒有說得比來源多。hk02、m001、q001 也都說「政府」，全片一致。至於是哪個單位，由 #7 標明是 The Verge 的說法） | |
| 5 | 他說，政府跟對方講：「準備去坐牢吧。請給你太太一個晚安吻。」（c61） | m004 | TV | 200 | CONFIRMED（引號裡照第 1 輪的直譯；「政府」同 #4） | |
| 6 | 卡片 mc-quote1：kicker「Trump on 60 Minutes」，key「Trump: 'go to jail'」 | mc-quote1.data | TV | 200 | **CHANGED**（引句是川普轉述「我們」對那位老闆說的話，不是他自己對誰說的。原本的 kicker 與 key 單獨看，會讀成川普在節目上叫人去坐牢） | kicker →「Trump, retelling the call」；key →「Retold: 'go to jail'」 |
| 7 | 他說，現在管這個風險的，是美國司法部；卡片「The Justice Dept., he says」 | m010；mc-doj | TV | 200 | **CHANGED**（TV 引的川普原話裡只有「we」「us」，沒有說出司法部。「He claimed the DOJ is managing that risk」是 The Verge 的轉述，報導沒有引出他說「DOJ」的原話，所以要標成 The Verge 的說法） | m010 →「據 The Verge 的報導，他的意思是，現在管這個風險的是美國司法部。」；卡片第二行「he says」→「per The Verge's report」；key「DOJ manages it, he says」→「DOJ, per The Verge」 |
| 8 | 風險遠沒有那些 AI 主管說的那麼真實……（c62） | m009 | TV | 200 | CONFIRMED（「Asked about AI executives' warnings…」之後「as they talk」，they 就是那些主管） | |
| 9 | 台灣，報導完全沒提到；亞洲只提到中國。那是川普自己的說法：中國沒有護欄，他們的護欄就是習近平說了算（c63） | m043、m069；mc-asia | TV | 200 | CONFIRMED（全文沒有 Taiwan；亞洲只有 China／Xi；「China has no guardrails … They have the guardrails that whatever President Xi says goes」） | |
| 10 | 據 Decrypt，紐交所的母公司 ICE 在規劃新平台，要交易記在區塊鏈上的股票；卡片「NYSE's parent plans / on-chain shares」、key「On-chain stock venue」（c64） | f002；fm-intro | DN | 200 | CONFIRMED（「The platform, which the NYSE's parent Intercontinental Exchange previously said it was developing, is designed to allow 24/7 trading … of tokenized securities」；「tokenized equities」也有出現） | |
| 11 | Avalanche 的開發公司說，這個平台的帳會記在 Avalanche 上；卡片 kicker「Ava Labs says」（c65） | f042；fm-books | DN | 200 | CONFIRMED（「Ava Labs, the company behind Avalanche, said Monday that the blockchain will serve as the "core ledger technology" for the clearing firm」；「Running on Avalanche」） | |
| 12 | 成交後要確定錢和股票真的換手，這一步叫清算和結算；區塊鏈這次被放進的就是這一步，Decrypt 叫它市場的管線（c66） | f043、f003；fm-plain、fm-why | DN、NYSE | 200 | CONFIRMED（「puts a blockchain beneath the clearing-and-settlement layer—the market's core plumbing」；解釋照 NYSE 的 callout） | |
| 13 | Kai：Avalanche 管的是對帳跟交割那兩段？Sola：對，清算公司會拿 Avalanche 當核心帳本（c65） | f010、f011；fm-ledger | DN | 200 | CONFIRMED（「core ledger technology for the clearing firm」） | |
| 14 | Kai 說區塊鏈的解釋；股票還是那張股票，只是記帳的地方換了，Sola 說「差不多」（c67） | f041、f015、f016 | — | — | OUT OF SCOPE（解釋，內容與第 1 輪相同；「差不多」已經標明是簡化） | |
| 15 | 他說，平台會支援在好幾條區塊鏈上市的股票；記錄和結算交易的那本帳有條件（c68） | f049、f021；fm-needs | DN | 200 | CONFIRMED（「its planned platform will support equities listed across a range of blockchains, the ledger recording and settling trades needs to be fast, reliable and able to control who participates」） | |
| 16 | Decrypt 說，這是華爾街老牌機構把核心設施搬上公有區塊鏈的跡象（c69） | f026；fm-sign | DN | 200 | CONFIRMED（「one of the clearest signs yet that Wall Street's oldest institutions are moving core market infrastructure onto public blockchains」） | |
| 17 | 公有，就是誰都看得到帳上的紀錄，不像銀行的帳只放在自己家裡；卡片「Public blockchain: Anyone can see it」對「A bank's ledger: Kept in-house」（c69） | f047；fm-public | DN | 200 | **CHANGED**（緊接在 #16 後面，聽起來像這個平台的交易紀錄人人都看得到，DN 沒有這樣說。#15 的 Lee 說這本帳要「able to control who participates」，兩句一起聽會打架。「銀行的帳放在自己家裡」也是來源沒有的對照。改成一般說法加上限定，並把卡片右邊換成這個平台） | f047 →「公有區塊鏈一般誰都看得到紀錄，但 NYSE 主管說，這本帳仍要控管誰能參與。」；卡片左「Usually open to view」，右「This platform's ledger / Controls who joins」；key →「Public, but gated entry」 |
| 18 | Kai：放進交易的底層，比只把一檔股票包成代幣實在（c70） | f040；fm-kai3 | DN | 200 | OUT OF SCOPE（意見；比較的兩邊照「rather than just wrapping a single fund or stock in a token」） | |
| 19 | 不過這筆合作誰付誰多少錢，報導沒寫 | f027 | DN | 200 | CONFIRMED（DN 沒有金額，只加了「不過」） | |
| 20 | ICE 還跟 OKX 在規劃另一個代幣化股票平台；美股七巨頭是包括 Apple 和 Meta 在內的七家大型科技股統稱；這七家全都選擇不讓股票在 ICE 和 OKX 的平台上代幣化；卡片 keys（c71） | f029、f036、f048；fm-catch | DN | 200 | CONFIRMED（「ICE and crypto exchange OKX are planning a 24/7 tokenized stock venue」；「Every Magnificent Seven stock, including Apple and Meta, opted out of having its shares tokenized on the venue」；keys 4 個，對 4 個畫面狀態） | |
| 21 | 國際貨幣基金的研究發現，代幣化股票確實有人要，但還不容易順利買賣；卡片 kicker「Per an IMF study」，「Real demand, hard to trade」（c72） | f030；fm-imf | DN、NYSE | 200 | CONFIRMED（「An IMF study found tokenized stocks show genuine demand yet remain volatile and illiquid」。genuine demand 對「確實有人要」，illiquid 對「不容易順利買賣」，NYSE 文章也這樣解釋流動性不足。兩點都出自 IMF 研究，所以 kicker 的歸屬是對的。第 1 輪擔心的「uneven」是 Decrypt 自己的概括，這一版已經不用。volatile 刻意不念，以免談到價格，不構成誤導） | |
| 22 | 等一下，Decrypt 還有一個提醒：管線蓋好的速度，可能比需求跟上還快 | f032；fm-early | DN | 200 | CONFIRMED（「the infrastructure may be arriving faster than the markets to fill it」） | |
| 23 | 卡片 fm-catch、fm-imf、fm-books、fm-plain、fm-intro 的英文 | 各 data | DN | 200 | CONFIRMED（同 #10–#12、#20、#21） | |
| 24 | Kai：這招聰明，飛機退役的引擎，換個地方繼續上班（c73） | j010 | DJ | 200 | CONFIRMED（擬人；「retired aircraft engines that can be rebuilt for stationary power production」） | |
| 25 | Kai：我可以接受，至少還能自己決定要不要加買 | a004 | AV | 200 | OUT OF SCOPE（意見；「加買」是自願的，跟 a002 一致） | |
| 26 | outro：我說靠規則，Kai 說先讓產業跑，出事再依法罰；你站哪一邊？卡片「Rules first, or speed?」（c74） | o001、o002；outro | — | — | OUT OF SCOPE（兩位主持人的立場，跟 m063、m066 一致；loop q001 → o001 的說明也跟著更新了） | |
| 27 | 拿掉的句子：a013、j013（je-hot）、m006、m067、m042、m044、m068、m059、m038–m041（mc-si、mc-joke3）、f024、f037 | — | — | — | OUT OF SCOPE（拿掉的句子沒有在說明欄、縮圖、標題或 loops 裡留下引用；`loops` 的 setup／payoff id 都還在） | |

## 笑點檢查

這一輪逐句看新的或改過的笑點，以及接梗的卡片。用的是六條標準：有沒有暗示來源沒有的事實、新的數字、替真人編話、打一般人、黨派立場而不是笑政策本身、雙關或諧音。

| # | 笑點 | 位置 | 判定 | 理由 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- |
| 1 | 「等一下，這種事不是應該走正式程序嗎？一通電話就算數？」 | m005 | **留** | 用問句質疑做法，對象是程序，不是川普本人。沒有新的事實，m019、m020 也會再說明這只是他的說法。 | |
| 2 | 「同一段話裡，風險沒那麼真實，處理方法卻是坐牢警告。」 | m012；mc-joke1 | **改** | 「處理方法」會讓人以為整套管法就是坐牢警告。來源裡那通電話只是他舉的一個例子。 | →「同一段話裡，風險沒那麼真實，他舉的例子卻是坐牢警告。」 |
| 3 | 「對做 AI 的公司來說，最可怕的是不知道風險算大還是算小。」 | m013 | **留** | Kai 的立場，沒有事實主張。 | |
| 4 | 「護欄就是……我同意要有，只是不要多到跑不動。」「你要的護欄，最好都裝在別人的車道上。」 | m032、m033；mc-rails2 | **留** | 解釋照 TRUMP 文章；m033 是 Sola 吐槽 Kai，不涉及任何真人或政黨。 | |
| 5 | 「就像考試範圍還沒公布，被當的通知已經先寄出來了。」「對想創業的人來說，這種課根本不敢選。」；卡片「Fail notice: sent」 | m036、m037；mc-joke2 | **留** | 比的是「規則還沒寫，警告先到」這個順序；拿掉「老師打電話」後，不指向任何人。 | |
| 6 | 「罰則寫清楚最重要，罰多少都比一通電話好猜，不是嗎？」 | m047 | **留** | Kai 的意見，沒有數字。 | |
| 7 | 「所以照報導，這套管法目前沒有一條寫下來的規則，只有一通電話。」；卡片 key「Written rules: not yet」 | m051；mc-cost | **改** | 「沒有一條寫下來的規則」把「報導沒寫」說成「沒有」，這是來源沒有的事實；而且坐牢要依法，總有寫下來的刑法。這一點第 1 輪已經提醒過。 | →「所以照報導，這套管法只講到一通電話，沒提到寫下來的規則。」；key →「Written rules: not cited」（卡片正文「none reported」本來就是講報導，留著） |
| 8 | 「而且公司連下一通會打給誰都不知道，這最嚇人。」 | m052 | **留** | Kai 的立場。 | |
| 9 | 「我一直以為成交就結束了」「老牌交易所跟區塊鏈，我本來以為是兩個世界」 | f004、f045 | **留** | 反應，沒有事實。 | |
| 10 | 「差不多，Kai 今天難得一次講對。」「難得，你這次沒有先問要不要換手機。」 | f016、f050 | **留** | 主持人互相吐槽，回扣固定梗。 | |
| 11 | 「那我先幫它準備工作服。」 | f046 | **留** | 接 f019 的擬人，沒有新日期。 | |
| 12 | 「這招聰明，飛機退役的引擎，換個地方繼續上班。」 | j010 | **留** | 擬人，事實見主張表 #24。 | |
| 13 | 「我還是支持先蓋，等乘客到齊才開工，就來不及了。」 | f034 | **留** | Kai 的意見，接捷運的類比；不是投資看法。 | |

政治語氣：Main Course 新的笑點打的是做法（電話對比程序、規則對比警告），不打川普本人、政黨或支持者。川普的每一句話都掛著「川普說」「他說」「他回答」「那是川普自己的說法」，司法部的說法現在標成「據 The Verge」。mc-quote1 改過以後，卡片看得出是他轉述的話。全片沒有雙關或諧音，沒有新的數字，引號裡沒有替真人編的話，也沒有打一般人的笑點。

## 清楚度檢查

照 daily-brief.md §一之〇。

- 句子完整性檢查（任務給的 node 指令，含 key 長度與 keys 數量）：修改後 0 行。`big`、`quote`、`outro` 都沒有 `reveal`。新的 key「DOJ, per The Verge」18 字，「Retold: 'go to jail'」20 字，「Written rules: not cited」24 字，「Public, but gated entry」23 字。mc-doj 第二行「per The Verge's report」22 字。
- 改過的句子都能單獨聽懂：m010 自己說出「美國司法部」與出處；f047 說「公有區塊鏈」，不再只說「公有」，並說出「NYSE 主管」，不用往回指。m069 的「那是川普自己的說法」指的是同一場景前一句的「中國」，緊接著就重說內容，可以接受。f010「那兩段」緊接在三步驟的說明後面，是 Kai 的確認句，沒有改。
- 每則前兩句：NYSE 段 f002 先說發生什麼，f042 說是誰宣布、帳記在哪；hk01／hk02 拆成兩句以後，各自都是完整的一句。
- 畫面狀態：用 `estimateTimeline` 加 `slideStates` 重算。第一版改動讓 mc-joke1 變成 13.3 秒、mc-cost 變成 13.1 秒，已經縮短 m012、m051。改完全片最長 12.8 秒（ap-complex、tr-lead、mc-joke1），其次 12.7 秒（mc-changed、fm-kai）；outro 12.0 秒。

## 摘要

- 查了 27 條（第 1 輪之後新增或改過的部分）加 13 項笑點：CONFIRMED 19、CHANGED 3（#6、#7、#17）、NOT FOUND 0、OUT OF SCOPE 5（#14、#18、#25、#26、#27）。笑點表另有 2 處帶事實的改動（m012、m051 與 mc-cost key），合計事實改動 5 處。
- 事實改動 5 處：(1) mc-quote1 的 kicker 與 key 標明是川普轉述；(2) m010 與 mc-doj 改成「據 The Verge」，因為川普的原話沒有說出司法部；(3) f047 與 fm-public 改成「公有區塊鏈一般誰都看得到紀錄」，加上「這本帳仍要控管誰能參與」，不再跟 Lee 的說法打架，也拿掉「銀行」的對照；(4) m051 與 mc-cost key 從「沒有寫下來的規則」改成「沒提到寫下來的規則」；(5) m012 從「處理方法」改成「他舉的例子」。
- 撰稿人點名的疑問：c61 的「政府」留著（TV 自己把「we」寫成司法部，「政府」更寬，又掛在「川普說」底下）；c69 改（見上）；c72 確認，kicker 的歸屬正確。
- 笑點：改 2 項（m012、m051），刪 0 項。
- 唸出來的日期：這一輪沒有新的日期。
- `sources` 的 4 個網址 2026-11-10 重新打開，全部 HTTP 200，內容與第 1 輪相同；沒有數字改動，`checked_on` 不變。
- 會過期的事實：跟第 1 輪相同（NYSE／Avalanche 平台待核准，DN 2026-11-09；川普的電話沒有其他來源證實，TV 2026-11-09）。
- 觀點：m021、m063 是 Kai 的立場，m065、m066 是 Sola 的看法，o001 照兩人的立場總結，都跟 brief.md 一致，沒有不一致的地方。
- 聽眾檢查（只報告）：改過的句子都在 40 字以內。沒有「經查證」之類的字眼，也沒有括號或網址。新出現的拉丁詞只有 The Verge、NYSE、ICE、OKX，原稿都已經用過。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261110` → `0 errors, 1 warnings`（開場章節長度：照 daily-brief.md，本節目沒有開場濃縮，不用理）；估 14.1 分鐘，147 句。
- 懷疑但沒改：
  - m005「一通電話就算數？」：用問句暗示電話取代了程序。報導沒說有沒有其他程序，但這是 Kai 的提問，後面 m019、m020 也會交代只有他的說法，所以留著。
  - f011 Sola 對 Kai 說「對」，確認 Avalanche「管」清算和結算。DN 的說法是 Avalanche 當清算公司的核心帳本技術，Sola 這句說的也是這個，算可以接受的簡化。
  - f030 沒唸「價格波動大」（volatile）：照節目不談價格的規矩省略，不構成誤導。
- 需要第三輪：**照規則是**（本輪事實改動 5 處，超過 3 處）。這 5 處都是把說法收窄、補上出處，沒有新的數字、名字或事實，所以第三輪只需要另一個代理對這 5 處（m010／mc-doj、mc-quote1、f047／fm-public、m051／mc-cost、m012）再看一次，其他部分可以照常進行；要不要省掉這一輪，由站主決定。所有主張都已判定，沒有懸而未決的。
