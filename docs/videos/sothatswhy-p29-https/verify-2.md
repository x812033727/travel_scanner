# 查核報告 2（sothatswhy-p29-https）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿，也沒有寫 verify-1.md）
- 日期：2026-11-12
- 範圍：verify-1.md 之後，盲評改寫的 16 句台詞（現行 `video.json` 的 p002、p012、p013、p024、p041、p082、p147、p164、p165、p179、p180、p182、p183、p184、p185、p186），加上 `claims.md` 各列跟現行台詞對不對得上。其餘 176 句沒有重查，結論沿用 verify-1.md。
- 比對方法：把改寫前的 `video.json`（session 暫存的 p29-v0.json，193 句）跟現行版（192 句）逐句 diff。除了這 16 句，還有兩句**被刪掉**，任務單沒列出來：
  - 舊 p024（所長）「每個經手的人都能打開看，甚至改幾個字再傳下去。」
  - 舊 p185（小問）「寄給誰，要我自己看清楚！」
  - 舊 p148「規格寫得很直接：它不隱藏資料的長度」不是刪掉，是改寫成現行的 p147。
  - 結果：舊 p025–p184 的編號全部往前移一號（舊 p090 → 現 p089，以此類推）。`claims.md` 用的還是舊編號，見第三節。
- 來源：`claims.md` 只當線索，不採用它的引文。今天重新 curl GET，HTML 去標籤後 grep 並讀上下文：
  - RFC 8446 `.txt`（200，337,736 bytes）：§1 Confidentiality（不隱藏長度）、§5.2（紀錄是「plaintext header followed by an encrypted body」、TLSCiphertext 的 length 欄、additional_data）、附錄 E.3。
  - RFC 9849 `.txt`（200，112,500 bytes）：§1 全段。
  - RFC 9110 `.txt`（200，502,941 bytes）：§4.3.4。
  - RFC 5280 `.txt`（200，352,580 bytes）：這 16 句沒有用到，只確認打得開。
  - certificate.transparency.dev〈How CT works〉（200）。
  - Google Chrome 說明 answer/95617：`hl=en`（200）與 `hl=zh-Hant`（200）。
  - Google Chrome 說明 answer/99020〈Manage warnings about unsafe sites〉`hl=en`（200）：用來核對 p179 的「只能」。
  - MDN〈DNS〉詞彙頁（200）、〈How does the Internet work?〉（200）、〈HTTPS〉詞彙頁（200）。
  - Let's Encrypt〈How It Works〉（200）與 Chromium Blog 2023-05-02（200）：這 16 句沒有直接用到，只是重開確認 p184 的範圍。
- 結論統計（16 句）：**正確 14、需改 2、錯誤 0**。另外 `claims.md` 有 24 列（C02–C25）的行號或內容跟現行台詞對不上（見第三節），另有 3 處選修建議。
- verify-1 的兩項必改都已經照改：F01（p184 改成「也冒充不了那個網址！」）、F02（說明欄已寫「免費發證件的機構」）。
- 字數：建議句含標點計算（英文字母、空格各算一字），小問 ≤15、所長 ≤25。

## 一、需改的地方與理由

| # | 行 | 原句 | 結論 | 理由與讀到的原文 | 建議改法 |
| --- | --- | --- | --- | --- | --- |
| G01 | p024（所長） | Chrome 瀏覽器的說明就這樣寫：沒有私密連線的網站， | 需改（用字跟官方中文和片中 p089 不一致；另外 28 字，超過所長的 25 字） | 「就這樣寫」會被聽成照念說明頁。繁中 Chrome 說明的原句是「網站未使用**私人連線**，其他人或許可以查看及變更你與該網站之間的資訊」，英文是 "The site doesn't use a private connection. Someone may be able to view and change the information you send and get through this site."。片中 p089 的整頁警告也照官方寫「私人連線」，同一集一句「私密」、一句「私人」，小孩會以為是兩件事。內容本身沒錯：「可能看到、也可能改掉」對應 "may … view and change"。改寫加上「瀏覽器」三個字對第一次聽到 Chrome 的小孩有幫助，應該保留 | Chrome 瀏覽器說明寫：沒有私人連線的網站，（24 字） |
| G02 | p179（所長） | 沒錯，這種只能靠你自己看。 | 需改（「只能」說得太滿） | Chrome 說明 answer/99020："Phishing and malware detection is turned on by default in Chrome. When you encounter phishing … you may get a red warning that says "Dangerous site.""。也就是說，瀏覽器對**已知**的釣魚網站有時會另外警告，「只能靠你自己」不成立。本集要講的是 HTTPS（封條）管不到長得很像的名字，這點來源都支持：Chrome 說明 95617 "Check the site name in the address bar to make sure you're on the site you want to visit"，Chromium Blog "nearly all phishing sites use HTTPS"。把範圍限在封條就準確，接下一句「那多一個 S……」也更順 | 沒錯，這種封條管不到，要靠你自己看。（18 字） |

## 二、逐句核對（正確的句子與依據）

| 行 | 現行台詞 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p002（小問） | 我要用平板連免費網路，登入遊戲。 | 正確 | — | 虛構情節。拿掉「店裡的」以後，「咖啡店」還在 p001，後面 p014「咖啡店的無線網路機器」仍接得上 |
| p012（小問） | 差在路上？ | 正確 | — | 問句，接所長 p008「你的密碼在路上，差的比你想的多」 |
| p013（小問） | 密碼不是直接飛到遊戲公司嗎？ | 正確 | — | 錯猜，p014–p016 立刻糾正（MDN 路由器與 ISP，verify-1 已核） |
| p024（所長） | Chrome 瀏覽器的說明就這樣寫：沒有私密連線的網站， | 需改 | Chrome 說明（英／繁中） | 見 G01 |
| p041（所長） | 而且出發前，平板先問查詢處「這個網址在哪裡」， | 正確（比喻） | MDN DNS；MDN Internet；RFC 9110 §4.3.4 | MDN："The most prominent function of DNS is the translation of human-friendly domain names (such as mozilla.org) to a numeric IP address … this process … is known as a DNS lookup"；"we can alias an IP address with a human-readable name called a domain name"。「查詢處」＝幫你查名字對應位址的地方（DNS 解析），比喻方向正確。它沒有被說成可信的權威，因為下一句 p042 馬上說「那一問的回答，也可能被路上的人動手腳」，對應 RFC 9110 "or by an attacker that controls name resolution"。咖啡店的機器在 p022 已經算「路上的同學」，所以查詢處本身就是咖啡店的也說得通。查的是網域名稱不是整個網址、有快取就不必每次問，屬可接受的簡化。p167 的回呼「問『這個網址在哪裡』那一問」沒提查詢處，仍接得上 |
| p082（所長） | 現在 Chrome、Safari 這些瀏覽器要求， | 正確（簡化） | CT〈How CT works〉 | "Some browsers, like Chrome and Safari, help enforce CT."；"Both Safari and Chrome user agents require at least 2 SCTs, depending on certificate lifetimes."。「Chrome、Safari 這些瀏覽器」是「像 Chrome、Safari 這樣的瀏覽器」，跟原文 "like Chrome and Safari" 一致：只舉例，沒說只有它們，也沒說所有瀏覽器都要求。要求的是 SCT、說成「要登記在公開帳本」的簡化，verify-1 已接受 |
| p147（所長） | 還看得到一些。還記得信封外面寫的長度嗎？ | 正確 | RFC 8446 §5.2、§1、附錄 E.3 | 回呼 p123「信封外面還寫著這封信有多長」。§5.2 "Each encrypted record consists of a plaintext header followed by an encrypted body"，標頭裡有 `uint16 length`，路上看得到，這正是「信封外面寫的長度」。§1 "TLS does not hide the length of the data it transmits"、E.3 "observing the length and timing of encrypted packets" 仍支持下一句 p148「信有多厚、多久寄一封，路上的人還是看得到」。見下方「刪掉長度那句的影響」 |
| p164（所長） | 信最後送到哪一台網站的機器，路上還是看得到； | 正確（簡化） | RFC 9849 §1；MDN Internet | "The target domain may also be visible through other channels, such as plaintext client DNS queries or visible server IP addresses."。路上看得到的其實是**位址**（IP），不是哪一台實體機器；MDN 給初學者也說 "using the domain name is the easiest way for us to reach a computer over the Internet"，把位址說成「一台電腦」是同一層次的簡化，沒有教錯方向。插圖還是舊版的大樓，見 S1 |
| p165（所長） | 不過很多網站常常共用同一台， | 正確（簡化） | RFC 9849 §1 | "many TLS servers host multiple domains on the same IP address. Private origins may also be deployed behind a common provider, such as a reverse proxy. In such environments, the SNI remains the primary explicit signal available to observers to determine the server's identity."。共用主機確實是一台機器放很多網站；大型服務商則是很多網站共用同一個位址、背後有很多台機器。「共用同一台」只講到前一種，但要表達的事（光看送到哪裡分不出是哪個網站，所以名字才是最明白的線索）跟原文一致，不會讓人誤會 HTTPS 或 ECH 的作用。「很多」「常常」對應 "many"，沒給比例 |
| p179（所長） | 沒錯，這種只能靠你自己看。 | 需改 | Chrome 說明 99020、95617 | 見 G02 |
| p180（所長） | 那多一個 S，你的密碼在路上差了什麼？ | 正確 | — | 問句。範圍限「在路上」，跟標題一致 |
| p182（小問） | 就像剛剛那封封好的信， | 正確（比喻） | — | 回收上課傳信的比喻 |
| p183（小問） | 同學照樣傳，卻讀不到， | 正確 | RFC 8446 §1 | "Data sent over the channel after establishment is only visible to the endpoints."。「讀不到」指信的內容；長度（p147–p148）和網站名字（p157–p168）看得到，片中前面已經交代，小孩用自己的話總結不必重講。舊句的「改不掉」拿掉了，少說一項性質但不是錯；完整性在 p122 已講 |
| p184（小問） | 也冒充不了那個網址！ | 正確 | RFC 9110 §4.3.4；Chromium Blog；Let's Encrypt | 主詞接上一句的「同學」（路上的人）。RFC 9110："Certificate verification is used to prevent server impersonation by an on-path attacker or by an attacker that controls name resolution"，且 "a client MUST verify that the service's identity is an acceptable match for the URI's origin server"：擋的正是路上的人冒充**同一個網址**。「那個網址」把範圍說清楚了，前一句 p179 又剛說長得很像的名字要自己看，所以不會被聽成 HTTPS 擋得住相似的冒牌網站（Chromium Blog "nearly all phishing sites use HTTPS"；Let's Encrypt 只驗網域控制權，騙子替自己的相似網址也領得到證件，p066）。verify-1 的 F01 已解決 |
| p185（所長） | 說得好。我覺得最妙的是，這個封條你每天都在用， | 正確（意見） | MDN HTTPS | 明說「我覺得」，是意見。「每天都在用」不是統計主張，對每天上網打遊戲的小孩是合理的說法；片中沒給 HTTPS 比例，也不需要 |
| p186（所長） | 卻從來沒有看見它。 | 正確（意見） | RFC 8446 §1 | 封條（加密）本身在畫面上看不到，鎖頭只是瀏覽器畫的標示（Chromium Blog "meant to indicate that the network connection is a secure channel"），而且 Chrome 已宣布換掉鎖頭（p072）。說法成立。小孩看過鎖頭（p068），可能會回嘴「我有看到鎖頭」，屬敘事問題，不影響事實 |

### 刪掉「規格寫得很直接：它不隱藏資料的長度」的影響

- 沒有留下沒根據的主張。p148「信有多厚、多久寄一封，路上的人還是看得到」本來就由 RFC 8446 §1 與 E.3 支持，跟片中有沒有說「規格寫」無關；後面 p151「規格提醒：看長度和時間……」仍把 E.3 交代成規格的話。
- 意思沒有變，反而更準確：改寫後的 p147 回呼 p123 的「信封外面寫的長度」，對應 §5.2 紀錄標頭的 length 欄，標頭是明文、長度在路上看得到。p153 塞空白「撐成一樣厚」也接得上：標頭寫的是含填充的長度（§5.2 TLSInnerPlaintext 的 zeros）。
- 少了一句「規格自己承認」的語氣，觀眾聽不到「這是設計上就沒打算藏」；這是敘事選擇，不是事實問題。p154「要塞多少，規格沒有規定」仍是規格的話（§5.4）。
- 另外兩句被刪掉的也查過：舊 p024「打開看，甚至改幾個字」拿掉後，「看得到、改得掉」仍由 p024–p025 轉述的 Chrome 說明交代；舊 p185「寄給誰，要我自己看清楚！」的意思移到新 p179 與 p189「下次打密碼，我先看名字！」，「HTTPS 不等於網站可信」的紅線沒有斷。

## 三、claims.md 跟現行台詞對不上的地方

`claims.md` 的行號是改寫前的第一版。舊 p024 刪掉以後，舊 p025–p184 全部往前移一號；舊 p185 刪掉、新增 p179，結尾又重寫。逐列：

| 列 | claims.md 寫的 | 現行台詞 | 問題 |
| --- | --- | --- | --- |
| C01 | p007、p014–p016、p021–p022 | 同 | 對得上 |
| C02 | p023–p026；「p024『打開看，甚至改幾個字再傳下去』是比喻裡的說法」 | p023–p025 | **指向已刪掉的句子**（舊 p024 不存在了）；範圍要改成 p023–p025。「沒有私密連線」也要配合 G01 |
| C03 | p029–p031；注意欄的 p029 | p028–p030；p028 | 行號差一 |
| C04 | p030、p034–p036；注意欄的 p036 | p029、p033–p035；p035 | 行號差一 |
| C05 | p039–p043，回呼 p168 | p038–p042，回呼 p167 | 行號差一；p041 新加的「查詢處」比喻沒寫進注意欄（建議補「查詢處＝DNS 解析，比喻」） |
| C06 | p044–p049 | p043–p048 | 行號差一 |
| C07 | p050–p056；p056 抽屜小卡 | p049–p055；p055 | 行號差一 |
| C08 | p057–p060、p067 | p056–p059、p066 | 行號差一 |
| C09 | p064–p066；注意欄的 p066 | p063–p065；p065 | 行號差一 |
| C10 | p010、p068–p074 | p010、p067–p073 | 行號差一 |
| C11 | p075–p080 | p074–p079 | 行號差一 |
| C12 | p081–p087 | p080–p086 | 行號差一；p082 改成「Chrome、Safari 這些瀏覽器」，內容仍符合 "browsers like Chrome and Safari" |
| C13 | p088–p091 | p087–p090 | 行號差一 |
| C14 | p095–p105；注意欄的 p103、p105 | p094–p104；p102、p104 | 行號差一 |
| C15 | p106–p110 | p105–p109 | 行號差一 |
| C16 | p111–p119 | p110–p118 | 行號差一 |
| C17 | p120–p121 | p119–p120 | 行號差一 |
| C18 | p122–p125；「p094 的『信要怎麼封』在 p122 回收」 | p121–p124；p093 在 p121 回收 | 行號差一 |
| C19 | p126–p134；p134 小問 | p125–p133；p133 | 行號差一 |
| C20 | p135–p142 | p134–p141 | 行號差一 |
| C21 | p143–p144 | p142–p143 | 行號差一 |
| C22 | p145–p155 | p144–p154 | 行號差一；片中已不再直接說「規格不隱藏長度」，p147 改成回呼信封外的長度（§5.2 明文標頭），注意欄宜補一句 |
| C23 | p156–p169；p158「很可能」；簡化清單第 5 條「送到哪一棟大樓＝伺服器 IP」 | p155–p168；p157；現行是「哪一台網站的機器」「共用同一台」 | 行號差一；比喻已從「大樓」改成「機器」，簡化清單第 5 條與 C23 標題要跟著改，並註明 IP 位址不一定等於一台機器（RFC 9849 "behind a common provider, such as a reverse proxy"） |
| C24 | p170–p179；「p009 在 p172 回收」「寶石連結在 p179 回收」「p174 是撰稿推論」「p179 名字多了一個字母」 | p169–p179；p171；p178；p173；p178 | 行號差一；新 p179「這種只能靠你自己看」沒有列（配合 G02） |
| C25 | p180–p187；p182–p185「同學還是幫我傳、拆不開、改不掉、冒充不了、寄給誰要自己看清楚」；p186–p187 意見「最厲害的是……不用靠他們守密」 | p180–p186；p182–p184「封好的信、同學照樣傳卻讀不到、也冒充不了那個網址」；p185–p186 意見「最妙的是，這個封條你每天都在用，卻從來沒有看見它」 | **指向已不存在的句子**：p185「寄給誰」已刪，p186–p187 的意見整句換掉，「改不掉」也拿掉了；「改成冒充不了」要更新成「冒充不了那個網址」（verify-1 F01）；新意見沒有對應的說明 |

另外：`brief.md` 第 69 列的收尾台詞也還是舊版（「同學還是幫我傳……寄給誰，要我自己看清楚！」），不在本次範圍，只提一下。

## 建議修改

必改：

- G01 p024（所長）：Chrome 瀏覽器的說明就這樣寫：沒有私密連線的網站， → Chrome 瀏覽器說明寫：沒有私人連線的網站，（24 字）
- G02 p179（所長）：沒錯，這種只能靠你自己看。 → 沒錯，這種封條管不到，要靠你自己看。（18 字）
- `claims.md`：C02–C25 行號全部減一（C24 的範圍止於 p179）；刪掉 C02 對舊 p024 的說明；改寫 C25 對收尾與所長意見的描述；C05 補「查詢處」、C22 補長度回呼、C23 與簡化清單第 5 條把「大樓」改成「機器／位址」。

選修（不影響本輪結論）：

- S1 p164 的插圖（場景 `tall-building`）還是「一棟公寓大樓」，p165（`chief-same-building`）的手勢是屋頂。台詞已改成「哪一台網站的機器」「共用同一台」，畫面跟話對不上；可把插圖換成一台機器，或把台詞改回大樓的比喻（舊句「哪一棟大樓」「住同一棟」verify-1 已核為正確）。
- S2 p164–p165：若想更貼近「位址」又不換插圖，可改成「信最後送到哪一棟大樓，路上還是看得到；」「不過很多網站常常住同一棟，」（就是舊句）。現行句子不算錯，可留。
- S3 p186：小孩看過鎖頭（p068），「從來沒有看見它」可能被回嘴。若要避開，可改「卻從來沒有看清楚它。」（10 字）。屬敘事選擇，原句可留。
