# S50｜1666 年倫敦大火起火屋、烤爐與擴大條件

查核日期：2026-10-20 UTC；R2 修訂依 [R1 獨立覆核的 HOLD 清單](review/r1-source-independent.md)。這是作者前製研究，**不是修訂後的獨立來源覆核**。本機重新讀取並核對 Pepys 與兩份 17 世紀印刷品的固定文字，來源的原始位元組 SHA 如下。官方《London Gazette》和 London Museum 網站的連線在此雲端容器遭**代理 CONNECT 403**；官方頁的引句取自倉庫既有 [P17 題卡查核](../history-curiosity/topic-checks/P17.md)，因此本集的核心主張盡量落在可直接閱讀的原始文字，不能把這些網站記成當場重驗通過。

| 代號 | 原始文本、固定版與本機 SHA-256 | 證據位置／性質 |
| --- | --- | --- |
| D | [Samuel Pepys, *Diary*, 1666-09-02 至 09-06，Wheatley 編數位版](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65784-L66176)；`3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d` | 當事人近時代日記，但數位版含後出編輯插注；只引用日記正文，不把其聽聞當親見。 |
| A | [1667 年《A True and Faithful Account...》TCP 轉錄](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml)；`0a4b379b932fc331c9ff10bd217e6d8b2cc513388a3fd73d7f64f0b35447595e` | 事後出版的下議院委員會證詞選刊，含測量員數字、Farriner 本人的說法；選刊有宗教與政治立場，不等於完整中立裁判。 |
| V | [Thomas Vincent, *God's Terrible Voice in the City*，1667 年 TCP 轉錄](https://github.com/textcreationpartnership/A64990/blob/e15ce8bba340e6089deec4ff85b486842e568434/A64990.xml)；`36798f66f98c32482b09209d7acb0ed204bacae744b5eae7c40532ca7a093f29` | 同時代作者回述火行路線；他的宗教審判與反天主教推斷不作事實。 |
| G | [*London Gazette* issue 85 官方掃描](https://www.thegazette.co.uk/London/issue/85/data.pdf) | 官方公報的起火時間、強東風、緊密木屋等引句已記在 P17；代理 CONNECT 403，本次未收到來源網站回應，影片不逐字引用官方掃描。 |
| M | [London Museum〈Great Fire of London〉](https://www.londonmuseum.org.uk/collections/london-stories/great-fire-of-london/) | 博物館的現代解說，P17 記其「火星可能」和「無法確知」；代理 CONNECT 403，本次未收到來源網站回應，作語義界線及延後複核項。 |

## 逐項可說與界線

| ID | 可說的事 | 直接行段與不能跨越的推論 |
| --- | --- | --- |
| R01 | 9 月 2 日凌晨一至二點，火從布丁巷麵包師 Farryner/Farriner 的屋子開始；A 說燒到 9 月 6 日。 | [A L147–153](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L147-L153)。這是刊本對起點與時段的記載，**不記錄點火瞬間**。現代標準拼法用 Farriner。 |
| R02 | Vincent 也把起點放在布丁巷烘焙屋，寫火先往橋邊與泰晤士街去，風助其往城內擴。 | [V L2174–2206](https://github.com/textcreationpartnership/A64990/blob/e15ce8bba340e6089deec4ff85b486842e568434/A64990.xml#L2174-L2206)。這是作者事後修辭濃厚的回顧；不用「火征服城市」等比喻，也不採其歸罪說。 |
| R03 | 9 月 2 日約三點，女僕 Jane 叫醒 Pepys；他覺得火遠而睡回去。約七點再看，他主觀上覺得火較小。 | [D L65788–65804](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65788-L65804)。七點的判斷不是火確已減弱的全城測量。 |
| R04 | Jane 聽說三百多房屋已燒；Pepys 登塔親見橋附近著火，**下塔後**一位倫敦塔官員告訴他起火在國王麵包師的布丁巷屋子。 | [D L65804–65827](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65804-L65827)。三百是當下轉述，不作確切統計；他沒有站在起火屋目擊烤爐。 |
| R05 | Pepys **見國王之前的第一次船行**看見 Michell 屋已燒，火在約一小時內到鋼院，人們把物件搬上船；他看見強風推火、乾旱後許多東西易燃，附近一座教堂尖塔著火塌落，也說當時在他的視野裡人多忙搬財物。 | [D L65816–65857](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65816-L65857)。`to my sight` 是視野限制，不說「全倫敦無人滅火」；橋上下兩側起火與河上看不清城內的句子是**午後再乘船**，不能前移。 |
| R06 | Pepys 口頭向國王與約克公爵主張拆屋；國王要他轉告市長。市長在日記中的回話是人不聽命、火追得比拆屋快；附近房屋密、倉庫有焦油、油、酒。 | [D L65835–65877](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65835-L65877)。不能畫國王給了書面令，亦不能當逐字會議記錄。 |
| R07 | 9 月 2 日 Pepys **見過國王與市長後的下午船行**看見橋上下兩側仍有火、河上難知城內火況，稍後又從船上見強風中燃燒碎片飛越幾間屋子；人們把早晨搬進的財物再往遠處搬。 | [D L65891–65945](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65891-L65945)。飛火跨屋是他的觀察，不說下午才首次有飛火，也不倒推最初點火的火星。 |
| R08 | 9 月 4 日塔街火到兩側，Pepys 記當地以炸倒屋子使火停住；9 月 5 日見辦公室附近火被阻，從教堂高處仍看見大片火，稍後步行看見成灰的街道。 | [D L65990–66068](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65990-L66068)、[D L66070–66115](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L66070-L66115)。那是**局部止火**，不能說一處炸屋救了全城；S38 已詳細講他的撤物，本集省略。 |
| R09 | A 開篇引測量員 Jonas Moore、Ralph Gatrix 的燒毀房屋 13,200 棟、城牆內 373 英畝與牆外 63 英畝 3 roods 燒損，並列牆內尚有 75 英畝 3 roods 未燒。片中把後者說成「超過七十五英畝」。 | [A L153–170](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L153-L170)。數字是**散文段落**，不是表或欄，也沒有指出哪一片沒燒；不是「全倫敦每棟房屋」。教堂數來源有 87/89 差異，不口播精確數。 |
| R10 | A 記 9 月 25 日下議院任命委員會調查，1667 年 1 月 22 日報告，2 月 8 日休會前沒有作判斷。 | [A L168–183](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L168-L183)。[P17 的下議院日誌核對](../history-curiosity/topic-checks/P17.md#逐項查核)更支持「證詞收集而非意外結論」；本片只說刊本如此記錄，不把委員會說成正式裁定意外或縱火。 |
| R11 | A 印了 Robert Hubert 的自白，說自己點燃 Farriner 屋；這證明**有人說過此話**，不證明自白是真的。 | [A L413–437](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L413-L437)。不重現他所說的「火球」作火災現場畫面；後出資料對其行刑日期、行蹤有差異，本片不講。 |
| R12 | 受訊時 Farriner 說午夜後巡房，只在一處煙囪／壁爐留有餘火，**房間地面**鋪磚，他仔細把火撥進餘燼；委員問風吹動 `those Coals`（炭火／餘燼）的可能，他否認，並堅稱有人放火。 | [A L465–480](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L465-L480)。這是本人事後自辯，不是火場勘驗；不能從鋪磚**地面**推成磚造壁爐，也不能畫餘燼有蓋或把它等同後世「烤爐」的確定結構。 |
| R13 | 官方公報在既有 P17 研究中寫強東風、緊密木造上瀝青的房屋，也把全城災害說成不幸意外與神意；博物館說烤爐火星只是可能，實際點火方法不能確定。 | [官方 G](https://www.thegazette.co.uk/London/issue/85/data.pdf)、[M](https://www.londonmuseum.org.uk/collections/london-stories/great-fire-of-london/)、[P17 第 3、5、12 項](../history-curiosity/topic-checks/P17.md#逐項查核)。G/M 此次遭代理 CONNECT 403、未重開，僅作背景與待複核；腳本不引為「國會定案」。 |
| R14 | 9 月 3 日 Pepys 家與鄰居用車和小船轉移財物，塔丘放滿家當，擁擠使小門難通。 | [D L65956–65989](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65956-L65989)。本集只用兩句帶出撤物造成的街道壓力；S38 已完整講他的撤物故事。 |
| R15 | 官方《London Gazette》第 85 號將強東風及擁擠、覆瀝青的木屋列為火勢猛烈的條件。 | [官方掃描](https://www.thegazette.co.uk/London/issue/85/data.pdf)、[P17 第 5 項](../history-curiosity/topic-checks/P17.md#逐項查核)。本次代理 CONNECT 403，待獨立覆核重開；不是國會委員會的結論。 |
| R16 | 1667 年刊本的封面把大火調查證詞與針對天主教司鐸、耶穌會士的其他告發放在同一本書名裡；這是編輯呈現，不是議會最後判決。 | [A L120–137](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L120-L137)、[A L168–183](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L168-L183)。不重述仇恨指控為事實。 |
| R17 | A 記獄卒帶自白者 Hubert 到布丁巷，他指認一間已燒的屋；刊本把此當成支持供詞的材料。 | [A L452–468](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L452-L468)。他**事後**認出／指出地點不能證明起火夜在場，也不能證明放火。 |

## 語義與畫面邊界

- **屋址 ≠ 火源機制 ≠ 城市規模原因**。可以說火從 Farriner 屋開始、烤爐火星可能引燃物品；不能說有人目擊火星、Farriner 承認失火、單一烤爐自動「毀掉全部倫敦」。
- 時間按文本：9 月 2 日凌晨一至二點 A 述火起，約三點 Pepys 被叫醒；他登塔、**下塔聽官員說屋址 → 第一次船行見鋼院及教堂尖塔的火 → 見國王與市長 → 下午再乘船見飛火跨屋**。9 月 4–5 日他見塔街一帶止火，9 月 6 日 A 稱火燒到此日；9 月 25 日委員會成立，1667 年 1 月報告。Pepys 約七點看火較小是誤判，不把那時說成已滅。
- Pepys 的起火屋消息來自塔樓官員；Farriner 的巡房和蓋餘燼是委員會刊本轉錄；Vincent 的宗教和政治判斷只當時代背景，不採為事實。測量員統計的是燒毀房屋，未計沒有燒到的城區。
- 所有火屋、風與人像提示詞都是**可愛卡通示意**；不讓 AI 畫真實手稿、起火火星的「目擊重建」、被指控的放火者、傷亡或可靠地圖。原文與數字由後製來源卡呈現。
