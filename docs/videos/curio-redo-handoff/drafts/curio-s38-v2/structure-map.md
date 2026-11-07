# curio-s38-v2 重做：10 步對照表

lint 估 13.5 分鐘（2,793 字）；原片 lint 估 13.2 分鐘（2,691 字）。下表秒數以每秒 3.45 字（照 lint 反推，含停頓）估。比例欄是 `heimao/STRUCTURE.md` 共通模板的建議。

| 步 | 名稱 | 開始 | 秒數 | 占比 | 模板建議 | scene id |
|---|---|---|---|---|---|---|
| 1 | 鉤子 | 0:00 | 46 | 5.7% | 3–5% | open-you、open-london、open-dig、open-wine、open-cheese、open-sleep、open-2am |
| 2 | 承諾句 | 0:46 | 8 | 1.0% | 1–2% | open-promise |
| 3 | 時代與起源 | 0:53 | 133 | 16.5% | 8–20% | origin-ada、origin-objects、origin-home、origin-office、jane、gown、mark-lane、back-to-bed、you-bed、smaller、jane-news、hearsay、tower、bridge、pudding、not-seen、by-boat、boat-load、friend-burned、into-river、last-minute、no-one、wind |
| 4 | 第一次起落 | 3:07 | 89 | 11.0% | 10–15% | whitehall、before-king、pull-down、king-says、duke、hopeful、mayor、complaint、walks-off、left-alone、church-goods、carts、thames-st、lesson、home-when |
| 5 | 升級關卡 | 4:35 | 192 | 23.7% | 25–35% | guests、dinner、batelier、moved-again、twice、to-river、both-ways、virginal、virginal-ada、sparks、jump、arc、wept、tom、packing、garden、cellar、which-first、cart、robe-cart、funny、bethnal、full-house、rest-of-it、lighter、tower-hill、postern、neighbour、admire、carries、office-quilt、leftovers、what-left |
| 6 | 最大危機 | 7:47 | 116 | 14.4% | 8–12% | last-box、tower-st、gutter、batten、pit-one、papers、archive-joke、own-wine、pit-two、cheese-in、no-size、you-treasure、office-q、afternoon-talk、dockyard、pen-goes、letter、no-reply、mutton、sky |
| 7 | 翻身與揭曉 | 9:43 | 93 | 11.5% | 8–12% | blast、stopped、half-relief、own-lane、wake、church-alarm、up-now、downriver、look-back、lock-money、goes-back、deptford、still-stands、office-ok、church-scorched、credit |
| 8 | 尾聲：故事還沒結束 | 11:16 | 78 | 9.6% | 8–12% | climb、ruin、embers、moorfields、glass、watch、sleeps、dawn-q、new-fire、put-out、riverbank、unload、nothing-missed、fears |
| 9 | 主題收束 | 12:34 | 42 | 5.2% | 6–8% | cheese-q、why-again、my-guess、rewind、answer、last-line |
| 10 | 提問與訂閱 | 13:16 | 13 | 1.6% | 1.5–2.5% | close-outro、close-subscribe |

步 5 稍短、步 6 稍長：九月四日兩個坑和起司入土是全片的主角，所以放進「最大危機」，沒有硬切。

## 章節

| 章 | 開始（lint 估） | 步 |
|---|---|---|
| 大火燒到第三天，有人在院子裡埋起司 | 0:00 | 1–2 |
| 九月二日凌晨，他看了一眼火，又回去睡 | 0:52 | 3 |
| 他把拆屋的辦法帶進宮裡，國王點了頭 | 3:06 | 4 |
| 中午照樣請客，黃昏他在對岸看著火哭了 | 4:35 | 5 前半 |
| 九月三日天沒亮，他穿著睡袍押著一車錢出城 | 6:23 | 5 後半 |
| 九月四日，院子裡先後挖了兩個坑 | 7:47 | 6、7 開頭（炸屋） |
| 九月五日凌晨兩點，妻子又把他叫醒 | 10:05 | 7、8 開頭（登塔） |
| 九月六日，他卸下貨物，寫下「我們的恐懼過了」 | 11:54 | 8 |
| 那塊起司，後來呢？ | 12:35 | 9–10 |

原第 1 章「一六六六年九月四日傍晚，院子裡挖開第二個坑」改名，因為開場不再演九月四日的完整場景；第 2–8 章章名不變（第 2 章改成「…看了一眼火，又回去睡」），新增第 9 章收尾。

## 原本每一段去了哪裡

| 原段落（原 scene id） | 新位置 | 怎麼改 |
|---|---|---|
| 第 1 章開場五步：open-you、open-third-day、open-dig、open-second、open-wine、open-cheese、open-face、open-2am、open-promise | 步 1 鉤子、步 2 承諾句 | 原開場先演完九月四日傍晚的院子（第二個坑、先放酒、起司、火到附近），再用「兩天前」倒回去，是濃縮劇情加跳時間。現在鉤子只講：你會藏什麼 → 一六六六年倫敦大火、有個人寫日記 → 他叫佩皮斯，第三天在院子挖坑 → 放進酒和自己的東西 → 起司 → 「更怪的是」起火那天他回去睡（起點）→ 凌晨兩點被叫醒（一個高潮標籤）。「第二個坑」、「火到附近卻蹲著挖土」不在開場講，留到步 6。承諾句改成固定句型，由 Ada 說。原承諾句「把大火最初那五天走一遍」併進 origin-ada。 |
| 第 2 章（maid-window…wind） | 步 3 時代與起源 | 前面加四景先鋪梗：Ada 自我介紹、代表物（棕色小日記＝佩皮斯）、他的家（妻子、女僕珍妮）、他的辦公室與帳冊文件（埋梗，步 6 回收）。原「那把火，兩天前的凌晨就燒起來了」拿掉（不再倒敘），改成「一六六六年九月二日凌晨，女僕珍妮看見城裡起了火」。為了鉤子密度：smaller 加「真的變小了嗎？」、by-boat 把問句放到句尾。 |
| 第 3 章（whitehall…home-when） | 步 4 第一次起落 | 起：拆屋的辦法、國王點頭；落：市長走掉。加一句 Ada 小結（lesson）「這就是這五天的第一課：國王點了頭，火可不會等人」。原 rest 與 walks-off 併成一景。 |
| 第 4 章（guests…which-first）＋第 5 章（cart…what-left） | 步 5 升級關卡 | 搬一次、再搬一次、上船、地窖、押車、平底貨船、睡辦公室，一關一關升級。刪 you-dinner、you-wept、you-moving 三句「你」（長度）；boats 併進 both-ways；no-sleep 併進 which-first；jump 改成「答案是：…」接住火星的問句。 |
| 第 6 章（last-box…own-lane） | 步 6 最大危機＋步 7 前段 | 兩個坑、起司入土、辦公室危急、回信沒來是谷底；夜裡塔街炸屋、火停住是翻身的開始（步 7）。papers 改成回收步 3 的辦公室文件。cheese-in 拿掉「還有一些別的東西」；you-treasure 改短。 |
| 第 7 章（wake…dawn-q） | 步 7 後段＋步 8 前段 | 凌晨兩點回收開場預告；up-now 改成回收九月二日那張床。房子還站著、辦公室還在是步 7 的揭曉。they-came（「這一段，我讀得很痛快」）刪掉；登塔起是「故事還沒結束」（步 8），由 Ada 說。stairs 併進 ruin，watch 與 sleeps 拆兩景。 |
| 第 8 章（new-fire…outro） | 步 8 後段、步 9、步 10 | 九月六日主教門、卸貨、「我們的恐懼過了」留在步 8。步 9：起司的下落 → 為什麼埋 → 我的推測 → 新加倒帶句（rewind：先送走錢、再送走箱子、最後才是酒和起司）→ 結檔句 → 新加金句（last-line）回扣開場「你會藏什麼」。原 diary-page 與 fears 併成一景；原 answer-card、outro 卡片改成 Ada 插圖；outro 拆成兩景。 |

## 埋梗與回收（loops，28 個）

| 埋 | 收 | 內容 |
|---|---|---|
| lf101（open-you） | lf906（last-line） | 你會藏什麼 |
| lf104（open-wine） | lf105（open-cheese） | 他放進坑裡的自己的東西 |
| lf106（open-sleep） | lf208（back-to-bed） | 看了一眼又回去睡 |
| lf107（open-2am） | lf702（church-alarm） | 埋完起司的隔天凌晨兩點被叫醒 |
| lf108（open-promise） | lf903（my-guess） | 全片的問題：為什麼把起司埋進土裡 |
| lf204（origin-office） | lf606（papers） | 辦公室的帳冊與文件後面用得上 |
| lf208（back-to-bed） | lf703（up-now） | 他回去睡的那張床 |
| lf213（tower） | lf214（bridge） | 塔樓上看到什麼 |
| lf217（by-boat） | lf219（friend-burned） | 熟人的家還在嗎 |
| lf223（wind） | lf622（stopped） | 誰能讓火停下來 |
| lf303（pull-down） | lf622（stopped） | 拆屋的辦法 |
| lf307（mayor） | lf308（complaint） | 市長帶不帶得動人 |
| lf313（thames-st） | lf609（pit-two） | 他自己家裡的酒 |
| lf315（home-when） | lf401（guests） | 什麼時候燒到他家 |
| lf406（to-river） | lf407（both-ways） | 火線推到哪 |
| lf410（sparks） | lf411（jump） | 火星能飛多遠 |
| lf415（packing） | lf416（garden） | 家當先搬到哪 |
| lf418（which-first） | lf501（cart） | 先送走哪一批 |
| lf507（lighter） | lf510（neighbour） | 船上還載誰的東西 |
| lf515（what-left） | lf601（last-box） | 搬不走的東西 |
| lf613（office-q） | lf710（office-ok） | 辦公室躲不躲得過 |
| lf618（no-reply） | lf621（blast） | 有沒有人先動手拆屋 |
| lf624（own-lane） | lf711（church-scorched） | 他自己那條巷子 |
| lf705（look-back） | lf707（goes-back） | 他還回不回去 |
| lf708（deptford） | lf805（unload） | 德普特福德船上的貨物 |
| lf713（climb） | lf714（ruin） | 塔上看到的倫敦 |
| lf801（dawn-q） | lf802（new-fire） | 火停了沒 |
| lf901（cheese-q） | lf905（answer） | 起司後來挖出來了沒 |


## 畫面代表物（真人不入畫）

| 誰 | 畫面 |
|---|---|
| 佩皮斯 | 一本素面棕色小皮面日記（diary 景）；動作景只畫一雙有白色蕾絲袖口的手 |
| 妻子 | 淡藍袖子的手（敲門）；和他一起搬箱子的另一雙手 |
| 女僕珍妮 | 捲起亞麻袖子的手 |
| 國王 | 紅絲絨墊上的金王冠 |
| 約克公爵 | 插白羽毛的寬邊黑帽 |
| 市長 | 一條金色官鍊（掛在空椅背、放在長椅上） |
| 潘爵士、巴頓爵士、巴特利爾太太、湯姆、考文垂爵士、卡特雷特爵士 | 不入畫；用他們的東西（酒箱、手帕的手、包袱的手、封蠟信、倉庫） |
| 一般人（鄰居母子、搬運工、船廠工人、看守的水手、街上人群、現代的「你」） | 普通卡通人 |

拆屋的辦法用「一排木頭玩具房子，中間抽掉一間」表示（pull-down），火停住時用同一排玩具房子、煙停在空隙前（stopped），credit 景 Ada 手上拿一間玩具房子。

回呼景用同一套提示詞：open-cheese／cheese-in（坑底的起司和酒瓶）、open-sleep／back-to-bed（空床），up-now 是同一張床、被子掀到地上；open-2am／wake（敲房門的手）。
