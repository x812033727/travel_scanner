# daily-ai-20261106 查核第 3 輪

查核日 2026-11-06。查核代理不是撰稿人，也不是第 1、2 輪的查核代理。範圍只有第 2 輪查核（4ccc85ab8 "fact and joke check round 2"）之後的改動：`git diff 4ccc85ab8 HEAD -- video.json claims.md`，也就是 claims.md〈第 3 輪修改〉c72–c86 與〈笑點〉最後的「第 3 輪改動與新增」，加上刪掉的句子（oqkf、ewxu、ojz4、8c6k、0rl0、8w9h、216d、pa3b）有沒有留下懸空的指涉。
來源：站上 CMP、RING、FIN、CYB 四篇（`/api/travel/guides/life/<slug>?locale=zh-TW`，全部 200、`status: published`）；原始來源 TC5、AN1 用 WebFetch 重開，DC6 用 curl 抓全文（200）逐字搜尋。web search 0 次。

## 來源代號

同第 1、2 輪：CMP、WYO、CYB、RING、FIN（站上文章）；DC6、GB3、V6、TC5、AN1、DC1（原始來源）。

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 「這次你猜對了，而且有數字。」接 7ivp 不到 1% | lsxs；cy-num | V6 | 200 | CONFIRMED（V6「went out of bounds less than 1 percent of the time」；Kai 猜「自己也會亂跑」，測試裡確實發生過，下一句立刻給出很小的數字，沒有誇大） | |
| 2 | 戒指上有螢幕、搖桿、麥克風，還有喇叭 | y6bx；ring-parts | TC5、RING | 200 | CONFIRMED（刪掉 oqkf 後補了主詞） | |
| 3 | 搖桿是拿來在手機或電腦的畫面上，移動和選東西的 | jrt2；ring-do | TC5 | 200 | CONFIRMED（「For navigation, there is a joystick, and it also supports gestures so that it can trigger different actions based on what's on your Mac or phone's screen」；「電腦」＝Mac，「移動和選東西」＝navigation 加觸發動作） | |
| 4 | 戒指主要是讓你用講的，指揮 AI 代理做事 | e1uu；ring-do | TC5 | 200 | CHANGED（措辭）（事實對，標題「so you can talk to AI agents」；但前一句 jrt2 的主詞是搖桿，「它」會聽成搖桿） | 「它主要是……」→「戒指主要是讓你用講的，指揮 AI 代理做事。」 |
| 5 | 電網要為資料中心花大錢升級；萬一專案失敗，這筆帳可能落到其他用戶頭上；平常的電費怎麼分攤，報導沒有細講 | hqgm、l70j、sgwi；lead-q2、lead-q3 | DC6、CMP | 200 | CONFIRMED（「financial assurances before costly grid upgrades, so other customers aren't left paying if projects shrink or fail」；拆句與移動沒有改意思） | |
| 6 | 電網升級前，它會先做財務保證；財務保證就是保證萬一專案失敗，這筆錢不會變成別人的帳單 | ln7b、qgzz；mc-more | DC6 | 200 | CHANGED（措辭）（qgzz 對；「做財務保證」不順，原文是 provide） | ln7b「先做財務保證」→「先提供財務保證」 |
| 7 | 每座園區有用水計畫和獨立噪音研究 | b4i8；mc-more | DC6 | 200 | CONFIRMED（「Each AI data center would get a water plan, annual progress reports and independent noise studies」） | |
| 8 | 「它每年也會公開進度報告，還有用電和用水的數字。」 | uqsm；mc-more | DC6 | 200 | CHANGED（範圍）（DC6 只說進度報告是年度的；「public energy and water figures」沒說多久公開一次，原句的「每年」會連到數字） | →「它會公開每年的進度報告，也會公開用電和用水的數字。」 |
| 9 | 它會限制跟官員簽保密協議；Kai「所以以後不能偷偷談了？」；Sola「是限制，不是禁止」；卡片「Fewer secret deals with officials」「Limits, not a ban」 | x3w3、xiwg、o0nz；mc-nda | DC6、CMP | 200 | CHANGED（措辭）（內文「limits on secrecy agreements with officials」，但 In brief 寫「an end to most NDAs with officials」：大部分取消，不是一般的限制。「不是禁止」在 Kai 的問句後面，聽起來像幾乎沒變；藍圖那條是「narrow limits on officials' NDAs」，wmux「要設限制」對） | o0nz→「是限制，不是全部禁止。」；卡片 key→「Limits, not a full ban」 |
| 10 | OpenAI 用的很多設施，是合作夥伴蓋的、擁有的，像是甲骨文；甲骨文是美國一家大型的雲端和軟體公司 | flz0、9xin；mc-partner | DC6（引 Reuters） | 200 | CONFIRMED（「Partners including Oracle build and own much of the infrastructure reserved for OpenAI, Reuters reported」；Oracle 的台灣通用譯名是甲骨文，總部在美國德州，以資料庫軟體與雲端服務為主，9xin 是常識，正確） | |
| 11 | 據 Decrypt 的解讀，社區想對這些設施的興建和營運，有更大的發言權 | dm0y；mc-say | DC6 | 200 | CONFIRMED（「communities want a bigger say in how these facilities are built and how their operations affect the people living nearby」） | |
| 12 | 藍圖：用電大戶要有專門的電價，多造成的電網成本自己付；保密協議要設限制；可收回稅務優惠（刪掉強制申報） | he86、nye9、wmux、tww0；mc-blue2 | DC6 | 200 | CONFIRMED（「large-load tariffs that require large electricity consumers to pay the incremental costs」；刪掉 216d 後旁白與卡片都改成三條、沒有說「四點」，編號第一到第三一致） | |
| 13 | 第一件，是各州會不會真的給用電大戶訂專門的電價 | 98be；mc-next | DC6 | 200 | CONFIRMED（「direct state public utility commissions」） | |
| 14 | 「Kai 說『至少他說了』，這點沒錯，OpenAI 確實說了。」 | 7gm2 | zvf0 | — | CONFIRMED（zvf0「可是至少他說了啊！」，引用正確） | |
| 15 | 「這不是業配，是要你投票」；規則是各說一邊、留言選邊 | 5nvc、mazm；ok-intro | — | — | OUT OF SCOPE（節目聲明；揭露 lbe5 仍在 ok-disc） | |
| 16 | 只開放美國的 Pro、Max、Ultra 三種付費方案，其他地區和方案公告沒提 | eaan；ok-who | AN1、FIN | 200 | CONFIRMED（「starts rolling out in beta this week, on the Pro, Max, and Ultra plans in the US」） | |
| 17 | 它連上銀行的方式是唯讀；只能看、不能轉帳也不能投資 | 3vch、n0sb、btr5；ok-ro | AN1 | 200 | CONFIRMED（「Access is read-only, and Personal Finance can't move, manage, or invest your money」） | |
| 18 | 看得到你選的帳戶的銀行名稱、帳戶名稱、類型和末四碼；餘額和信用額度；最多兩年的交易紀錄 | py1m、9ape、e1fc、ewb5；ok-see | AN1 | 200 | CONFIRMED（「the bank's name, each account's name, type, and last four digits, balances and credit limits, and up to two years of transactions」，限使用者選擇連結的帳戶） | |
| 19 | Kai「這些，銀行 App 本來就看得到啊。」 | jwi5 | AN1、常識 | 200 | CONFIRMED（銀行 App 顯示自己的帳戶、餘額與交易是常識；AN1「Getting answers about your money no longer means opening every banking app」也預設這些資料原本在各家銀行 App 裡；是 Kai 的反應，不是 Anthropic 的說法） | |
| 20 | Sola「這點你說得對，差別是多了一家 AI 公司在看」；「銀行看你的帳是工作，AI 公司看，是你點頭的」 | yg9u、0haf；ok-sola | AN1 | 200 | CHANGED（清楚度）（0haf 的「你點頭的」＝使用者自己透過 Plaid「approve Claude's read-only access」，對；yg9u 的「這點」指八句前的 jwi5，中間隔了 ok-kai 到 ok-noads 四個場景，單獨聽不知道是哪一點） | yg9u→「銀行也看得到，沒錯，但多了一家 AI 公司在看。」（第一版寫出 Kai 與銀行 App，ok-sola 變 14.6 秒，縮到 12.9 秒） |
| 21 | Kai「可是你自己也說了，隨時可以取消連結，不想給就收回來」 | 56tv；ok-kaiwin | AN1 | 200 | CHANGED（範圍）（「You can unlink an account anytime, and then Claude can no longer see its data」：之後看不到；「收回來」會聽成給出去的資料拿得回來，來源沒說。「你自己也說了」對，nbtu 是 Sola 說的，在前一個場景） | →「可是你自己也說了，隨時可以取消連結，取消之後它就看不到了。」 |
| 22 | 回扣拆成三句：OpenAI 昨天說了兩件事；測試裡擅自闖進別的系統低於 1%；電費全部自己付 | a1pc、joj2、2hxa；so-call | V6、DC6 | 200 | CONFIRMED（同第 2 輪 #52） | |
| 23 | 刪掉的句子 | oqkf、ewxu、ojz4、8c6k、0rl0、8w9h、216d、pa3b | — | — | CONFIRMED（沒有懸空：399 美元、出貨、空氣散熱、兩百多位居民、強制申報在旁白與卡片都已不見；pa3b 的類型與末四碼併進 9ape；0rl0 刪掉後 Google 沒有第三方查證仍在 h09o；說明欄「本集不談價格與投資」現在跟旁白一致） | |
| 24 | 留言題「蓋在你家旁邊，這份承諾該寫進哪裡？」 | kb70；outro | — | — | OUT OF SCOPE（問句） | |

## 笑點檢查

五條標準同第 2 輪：暗示來源沒有的事實、新的數字、替真人編話、打一般人、雙關或諧音。

| # | 笑點 | 位置 | 判定 | 理由 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- |
| 1 | 「這題，主菜時我們吵給你聽。」 | p94m | **留** | 串場。 | |
| 2 | 「搖桿，我猜是開會時偷偷按靜音用的。」／「差一點，……」 | zt4n、jrt2 | **留** | Kai 的猜測，下一句用 TC5 更正。「差一點」不算暗示事實：TC5 說搖桿與手勢依 Mac 或手機畫面觸發動作，Aina 的前一代 Mirage 也能在 Google Meet 靜音，所以 Kai 確實不遠；旁白沒說戒指能靜音。開會偷按靜音是 Kai 自己的想法，不是在笑一般人。 | |
| 3 | 「不用，你先去把遙控器找出來。」／卡片「Find the remote」 | ausc；ring-gag | **留** | 回扣 5x47（找不到遙控器時戒指才派上用場），沒有新事實。 | |
| 4 | 「連噪音都要研究，這比我想的認真。」 | sr4o | **留** | 反應，接 b4i8。 | |
| 5 | 「所以以後不能偷偷談了？」／「是限制，不是禁止。」 | xiwg、o0nz；mc-nda | **改** | 笑點本身沒問題，但「不是禁止」低估了 DC6 的「an end to most NDAs」，見主張表 #9。 | o0nz→「是限制，不是全部禁止。」 |
| 6 | 「用天然氣？我以為會是太陽能。」 | 4e7h | **留** | Kai 的猜想，a177 解釋燃料電池；沒有說天然氣好壞，也沒有新數字。 | |
| 7 | 「這條我喜歡。」「手續費那條，我先鼓掌。」 | uiyc、eqgq | **留** | 反應，切開清單。 | |
| 8 | 「好，我改立場：先說了，再寫進規則，我就簽。」／卡片「Say it first, then write it down」 | t2kw；mc-view3 | **留** | 回扣 3fx1「我已經想簽了」與 kmdx；Kai 的意見。 | |
| 9 | 「這些，銀行 App 本來就看得到啊。」／「好吧，這個差別我承認。」 | jwi5、fgml | **留** | 見主張表 #19、#20。 | |
| 10 | 「可是你自己也說了，……」／「好，這點算你贏。」 | 56tv、wwuh；ok-kaiwin | **改** | 讓 Kai 贏一局的結構留；「不想給就收回來」改成來源說的「取消之後它就看不到了」，見主張表 #21。 | |
| 11 | 「不用，這次手機是無辜的。」／卡片「The phone is innocent」 | ovhc；ok-gag | **留** | 固定梗收尾，沒有事實主張。 | |
| 12 | 「保全很少擅自開別人家的門，電費說好自己付，兩個我都記住了。」 | 2zrr；so-call2 | **留** | 跟 p1pc 同一個意思（未經允許進入），比「開錯門」更貼 V6 的 out of bounds。卡片 so-call2「Rarely the wrong door」是第 2 輪就有的，只是英文卡片的短寫，沒改。 | |

笑點總計 12 項：留 10 項，改 2 項（#5、#10），刪 0 項。沒有雙關或諧音、沒有新的數字、沒有替真人編的話、沒有打一般人。

## 清楚度檢查

- 句子完整性檢查（brief 的 node 指令）：修改前 0 行，修改後 0 行。
- 單獨聽得懂：e1uu 補主詞「戒指」；yg9u 把「這點」說出來；hqgm 接在 j17j「承諾裡自己就寫到一種情況」後面，本身也是完整的一句，留；9xin 接在 flz0 後面解釋甲骨文，留。
- 畫面狀態：用 `estimateTimeline` 加 `slideStates` 重算。yg9u 第一版讓 ok-sola 到 14.6 秒，縮短後最長 12.9 秒（ring-what、ok-disc、ok-sola），全部 ≤13 秒。mc-nda 12.7 秒。

## 摘要

- 查了 24 條加 12 項笑點：CONFIRMED 15、CHANGED 6（#4、#6、#8、#9、#20、#21）、NOT FOUND 0、OUT OF SCOPE 2（#15、#24）；#23 是刪句的檢查。
- 事實改動 3 處：(1) o0nz 與卡片 mc-nda key：DC6 的 In brief 是「an end to most NDAs with officials」，「不是禁止」改「不是全部禁止」；(2) uqsm：「每年」只屬於進度報告；(3) 56tv：取消連結後「它就看不到了」，不是把資料「收回來」。
- 措辭／清楚度改動 3 處：e1uu「它」→「戒指」；ln7b「做」→「提供」財務保證；yg9u 不再用指回八句前的「這點」。
- 指定確認：搖桿＝在手機或電腦畫面上移動與選擇（TC5，對）；「銀行 App 本來就看得到」（常識，AN1 的說法也預設如此）與「隨時可以取消連結」（AN1 逐字）有依據；方案是 Pro、Max、Ultra（AN1 逐字）；NDA 是限制、但 DC6 摘要說大部分取消，已改；噪音研究是每座資料中心「independent noise studies」（DC6 逐字）；刪句沒有留下懸空指涉；甲骨文的描述正確。
- 站上文章：CMP 只寫「限制與官員簽署的保密協議」，跟 DC6 內文一致，沒寫 In brief 的「大部分取消」；不算錯，沒有另外開票。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261106` → `daily-ai-20261106: 0 errors, 2 warnings`（開場濃縮兩條，本節目格式不用理）；估 14.9 分鐘，186 句。
- 可以進旁白合成。
