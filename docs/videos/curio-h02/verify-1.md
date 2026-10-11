# H02 獨立事實覆核：第 1 輪

日期：2026-10-12（Asia/Taipei）。覆核者沒有參與撰稿。**PASS_FACTS_ROUND_1**：完整稿及主張表已讀回，首輪必修全部套用，沒有未解決的稿件事實。超過三項事實修正，**仍須由另一名 reviewer 完成第二輪**；此處不核准大綱、付費、旁白或成片。

最終本輪核對：`video.json` SHA-256 `7b8d066cbb42ad7ee621171fcaedcda7c5eeafb9acf9bf8dc6c7d287b08c482d`；`claims.md` SHA-256 `6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`。109 景、134 句；72 個查核／範圍項，71 個事實或方法項均已在最終版本解決，1 個純包裝項 OUT OF SCOPE。下面保留前四章及後三章的初審、修訂歷程；其中 PARTIAL／待驗文字均為當時狀態，以本段及文末最终收據為準。

讀入稿件 SHA-256：`d90ed31393968d2f54b59db61602e33258eed6ceb3ff7f73b509e2680ba959d5`。62 景、76 句。全字串與逐句清單先存於 `<VIDEO_WORKDIR>/curio-h02/_audit/reviewer-claim-inventory-20261012.json`；322 個字串含畫面提示、字卡、縮圖及 YouTube 欄位。後續版本須重產清單並補本報告。

本輪權限只允許寫此報告及 `listener-review.md`，因此以下 CHANGED 均指**必須由協調者套用的修正**，不是已改稿。沒有編輯 `brief.md`、`video.json`、`claims.md`，沒有付費、approve 或 Git 動作。

## 來源與重開紀錄

| 代碼 | 來源 URL | 當天可讀結果 |
| --- | --- | --- |
| W | [懷特 1587、1590 記述，Hakluyt 卷十三](https://www.gutenberg.org/cache/epub/25645/pg25645-images.html) | web 當天重開可讀；同一出版物全文以 editorial User-Agent 直接 GET：HTTP 200。再讀研究快照核對上下文。|
| N87 | [NPS 1587 航程](https://www.nps.gov/fora/learn/historyculture/1587-the-lost-colony.htm) | web 當天重開可讀，來源刷新收據 HTTP 200；末尾更新日 2026-09-20。 |
| N90 | [NPS 1590 航程](https://www.nps.gov/fora/learn/historyculture/1590-rescue-voyage.htm) | web 當天重開可讀，來源刷新收據 HTTP 200；末尾更新日 2026-08-14。 |
| NT | [NPS 主要假說](https://www.nps.gov/fora/learn/historyculture/major-theories-of-the-lost-colony.htm) | web 當天重開可讀，來源刷新收據 HTTP 200；末尾更新日仍 2025-07-11。 |
| EV | [Encyclopedia Virginia：Roanoke Colonies](https://encyclopediavirginia.org/entries/roanoke-colonies-the/) | 直接 GET 為 HTTP 202、挑戰頁，不能當證據；另以 web 當天重開完整正文可讀。 |
| NH | [懷特記述現代拼字 PDF](https://nationalhumanitiescenter.org/pds/amerbegin/exploration/text6/white.pdf) | web 當天重開，4 頁正文可讀。此為同一份懷特記述，不能算第二個目擊者。 |
| SM20 | [Smithsonian 2020：內陸線索](https://www.smithsonianmag.com/smart-news/new-evidence-roanoke-colonys-disappearance-180976248/) | 本部分暫沿用 H02 2026-10-10 的覆核；完整稿階段必須當天重開，尚不計當天確認。 |
| C | [Commons 採用圖片](https://commons.wikimedia.org/) | 四個來源的 imageinfo API 逐個 editorial GET：HTTP 200；每 host 間隔至少 1 秒。授權、日期、SHA-1 與本機 SHA-256 全部吻合，詳下表。 |

史料是懷特對自己的行程、殖民地現場及所作推測的記述；不能把他的「我很高興／相信人平安」變成對全員命運的獨立證明。NPS、EV 及現代拼字版轉述同一段時，不另加目擊來源票數。

## 前四章逐項判定

| # | 主張 | where | URL／狀態 | 判定 | before → after／核對理由 |
| --- | --- | --- | --- | --- | --- |
| 1 | 一百多人／一百一十多人 | `530240f0`、`bd947762`、`c2450101`；YouTube description | N87、NT：當天可讀；刷新 HTTP 200 | CONFIRMED | NPS 出航 118、另一頁 117；稿子未聲稱精確 115。人數是近似概述，不把不同階段混為確數。 |
| 2 | 懷特看到留言很高興 | `530240f0`、`ddac8184`；description | W：HTTP 200 | CONFIRMED | 原文寫 I greatly ioyed；`ddac8184` 已明示「寫道／認為」。開場較晚才揭署名來源，列入聽眾建議。 |
| 3 | CROATOAN 是去處而非無法解讀暗號；不等於已解案 | `c396bf52`、`f8974907`、`abb7999e`、`37eb7619`；hook compare；title、thumbnail | W：HTTP 200；NT：當天可讀 | CONFIRMED | 這是約定留言及懷特的解讀。卡片已分「知道去處／未確定下落」，縮圖「不是咒語」屬故事包裝，未認定所有人平安。 |
| 4 | 1587 年七月，一艘船把家庭送上島 | `ad443391`；`farewell-landfall.data.prompt` | W：HTTP 200；EV：web 正文可讀、直接 GET 202 | CHANGED | →「一五八七年七月，船隊把英格蘭家庭帶到這裡。」旗艦、pinnesse 及其後到達的 Flyboat 分開；7 月 25 日才有其餘殖民者安全抵達，不能把整段只剩單一艘船。單艘示意畫可以保留，但旁白應說船隊。 |
| 5 | de Bry 到訪版畫 1590 年出版、不是 1587 現場紀錄 | `0378a93d`；`farewell-arrival-print.data` | C：該檔 API HTTP 200 | CONFIRMED | 日期 1590、作者 de Bry 依 White；字幕已排除現場紀錄。但「非抵達實拍」不如「版畫，非現場紀錄」精確，屬聽眾文字建議。 |
| 6 | 原定乞沙比克灣；羅阿諾克為找先前留下的人之中途停站 | `7d3976ee`、`de9770ac`；`farewell-destination-compare.data` | W：HTTP 200；N87：當天可讀 | CONFIRMED | 北／南是兩處相對方位，原文確有向 Chesepiok 建立聚落之指令。 |
| 7 | 領航員拒絕北上、要求留下 | `e8e1f755` | W：HTTP 200；N87：當天可讀 | CONFIRMED | 這是懷特記述及 NPS 敘述；EV 提及學者對懷特敘述的解釋有爭議，本稿不替領航員杜撰內心動機。 |
| 8 | 前一批英格蘭人曾住過、房屋待修 | `609abd25`、`bd947762` | W：HTTP 200 | CONFIRMED | 原文房屋仍立、並命令修屋及建新小屋。 |
| 9 | 1587 年舊屋無屋頂、光從缺失屋頂照入 | `farewell-old-dwelling.data.prompt`、`farewell-deer-melon.data.prompt` | W：HTTP 200 | CHANGED | roofless／missing roof／open roof → 完整但荒廢的木屋，日光由門窗照入。原文是房屋 standing unhurt，倒的是 fort；不可把堡壘拆平嫁接成住宅塌頂。 |
| 10 | 下層長瓜、鹿在屋裡吃瓜 | `cb08d4da`；`farewell-deer-melon.data.prompt` | W：HTTP 200 | CONFIRMED | 原文明列 melons 及 deer feeding。畫面屋頂須依 #9 修。 |
| 11 | 曼提歐為克羅托安人、協助語言溝通 | `07721bae`；`farewell-manteo.data.prompt` | W：HTTP 200；N87：當天可讀 | CONFIRMED | 懷特 1587 記述中 Manteo 向當地人用其語言說話，再向英格蘭人傳遞消息；NPS 補其學英文並與殖民者工作。 |
| 12 | 懷特稱島人為朋友，但英格蘭人曾誤襲克羅托安人 | `f6e27da0`、`069ea2a2` | W：HTTP 200；N87：當天可讀 | CONFIRMED | 「朋友」已署為他的稱呼。不能推成毫無嫌隙的永久同盟；稿子已留反例。 |
| 13 | 食物、冬季和補給壓力 | `1ff46026` | N87：當天可讀；W：HTTP 200 | CONFIRMED | 三项均符合派懷特回英格蘭背景，未說補給短缺已造成全員死亡。 |
| 14 | 1876 年受洗想像圖、距事件二百多年 | `86a65e1b`；`farewell-baptism-print.data` | C：該檔 API HTTP 200 | CONFIRMED | 1876−1587＝289 年；作者 Sheppard。不是 NPS 的 1893 年上色版。 |
| 15 | 懷特女兒 1587-08-18 生下 Virginia Dare | `51dcd3dc`、`9950a707` | W：HTTP 200；EV：當天 web 正文可讀 | CONFIRMED | 人名及關係吻合；稿子未誇張成第一個在美洲出生的歐洲人。 |
| 16 | 8 月 22 日請求、25 日聯名文件、27 日清晨離開 | `55c9e647`、`385bc548`、`be38542e`；`farewell-august-dates.data` | W：HTTP 200 | CONFIRMED | 原記述三個日子分明；27−18＝9 天。 |
| 17 | 懷特先拒絕、最後受託回去 | `ea6f1c25` | W：HTTP 200 | CONFIRMED | 是他對自己的記述，稿子未捏造對話或拒绝的新原因。 |
| 18 | 臨行約好刻目的地、若困境則地名上加十字 | `1b1b3b7d`、`e86ab0b4`、`369cdc7d`；`return-message-rule.data.rows[0:2]` | W：HTTP 200；NH：當天正文可讀 | CONFIRMED | 只有懷特留下的原記述；十字未指定馬爾他十字。 |
| 19 | 殖民者原先準備搬往內陸約 50 英里 | `421fe082`、`d37cb405`；`route-two-fifties.data.left` | W：HTTP 200 | CONFIRMED | 此為內陸計畫，與刻字所指的南方島不同，已分開。 |
| 20 | 原先希望 1588 年春返航，無敵艦隊耽擱、本土船舶留守 | `e4b5d68e`、`5a4ea7a7`、`deafa764`；delay steps | N90：當天可讀；EV：當天 web 正文可讀 | CONFIRMED | 船舶留守是命令；EV 又交代兩艘補給船仍於 4 月出航，稿子隨後有例外，不暗示毫無船隻出港。 |
| 21 | 1588 年補給船與法國人交戰折返；1590 年搭私掠船 | `590718a5`、`384b98db`；delay steps | EV：當天 web 正文可讀；N90：當天可讀 | CONFIRMED | 私掠船本來有自己的航程；不把它說成滿载殖民地補給的專船。 |
| 22 | 1590-08-18 登岸；前夜吹號唱歌，清晨登岸 | `53923c71`、`6387c813`、`c8106dd9`；三景 prompts | W：HTTP 200；N90：當天可讀 | CONFIRMED | 夜尋岸與清晨登岸分開，未把整場画成夜間。 |
| 23 | 樹上 CRO、入口去皮木樁 CROATOAN | `6abe644b`、`8697084e`、`01e14e26`；return compare；description | W：HTTP 200；N90：當天可讀 | CONFIRMED | 两處已分。兩個 shot 的字須後期卡片疊上，不能信任 AI 自動拼字。 |
| 24 | CRO 所在樹是「活樹」 | `return-two-carvings.data.left.heading` | W：HTTP 200 | NOT FOUND | 活／死没有原文判定；「活樹的樹幹」→「樹幹」。原文 vpon a tree 不能自行加 alive。 |
| 25 | 刻字離地約一個成人身高 | `527830a9` | W：HTTP 200 | CHANGED | →「木樁上的刻字很高，離地約一點五公尺。」原文 5 英尺，換算 1.524 公尺；成人身高不是明確量尺。這是把既有數據準確口語化，非新增考古量測。 |
| 26 | 房屋被拆、高大木柵欄與堡壘形突出部分 | `543e602a`、`3ee52e06`；相關 prompts | W：HTTP 200 | CONFIRMED | 未擅自說柵欄新建於懷特離開之後；房屋場景須與 1587 intact 舊屋區分。 |
| 27 | 鐵條、鉛等重物仍散置且草覆 | `d30453cd`；`return-heavy-metal.data.prompt` | W：HTTP 200 | CONFIRMED | 不可畫成所有物品搬空；source 還有重炮，不等於沿溪尋的小炮。 |
| 28 | 找不到船艇與先前留下的小炮，未證明被誰帶走 | `86b291b5`、`9e5b48ba` | W：HTTP 200 | CONFIRMED | 未把缺船推成有船航行，或把小炮缺失說成聚落不存在任何炮。 |
| 29 | 壕溝末有五箱、三箱為懷特所有；挖開損毀 | `c11d2375`、`435e5db2`；damage stats[0] | W：HTTP 200 | CONFIRMED | 数字與位置吻合。 |
| 30 | 書封被扯、畫框地圖雨損、盔甲鏽蝕 | `3f471fa8`、`a1530843` | W：HTTP 200 | CONFIRMED | 旁白有分開撕毀、雨損及鏽蝕，因果沒有混用。 |
| 31 | 雨水造成書封、畫框及地圖受損 | `return-chests-and-damage.data.stats[1]` | W：HTTP 200 | CHANGED | 「雨水｜書封、畫框與地圖受損」→「受損｜書封遭撕；畫框與地圖雨損」。原文 books torne from the couers 與 frame/map spoiled with raine 分開；不能用雨水總括因果。 |
| 32 | 箱子損壞不等於遭攻擊；敵人挖箱是懷特推測 | `344d40fb`、`ecc48106` | W：HTTP 200 | CONFIRMED | 推測有署名，沒有改成證實攻擊。 |
| 33 | 找到「克羅托安」，沒有遇難十字 | `d510fc74` | W：HTTP 200 | CHANGED | →「木樁刻著克羅托安，沒有看見約好的十字。」原句「他們找到克羅托安」可能被聽成已抵達島；實際當場找到的是刻字。這是保住事实的語義修正。 |
| 34 | 他認為人已到朋友的島，但不是全員結局證明 | `ddac8184`、`e3138e28`；return table row[2] | W：HTTP 200；NT：當天可讀 | CONFIRMED | 已把當時信念與後來命運區分。 |
| 35 | 留下文字的現場目擊者只有懷特 | `4b1ee5e0`；description | W：HTTP 200；NH：同文 | CONFIRMED | 說的是現存文字記述，不是說登岸者只有一人；稿子「後人多轉述」正確。 |
| 36 | Croatoan 族名也是地名；今日哈特拉斯島一帶、南方 | `f842d461`、`948e50c0` | NT：當天可讀 | CONFIRMED | 「一帶」保留島範圍變遷，未認定族人只在整座現代島。 |
| 37 | 島位在羅阿諾克以南約 50 英里 | `route-two-fifties.data.right.points[1]` | SM20：本輪尚未當天重開 | NOT FOUND（本輪待驗） | 保留待完整稿階段重開；不能把原卡的核對算成 reviewer 當天已確認。旁白只說另一方向，未复述此現代測距。 |
| 38 | 兩個五十英里不可合成同一搬家計畫 | `9ee17073`、`ced77e9e`；route compare | W：HTTP 200；NT：當天可讀 | CONFIRMED | 計画去內陸、留言指向南島；不是約好直接去南島。 |
| 39 | 懷特準備去克羅托安、斷錨纜，四套只剩一套 | `69efb42f`、`ebd0c9ba`、`8a6d5e5d` | W：HTTP 200 | CONFIRMED | one Cable and Anchor left ... of foure；是錨及纜組，不是說船上只剩一條任何用途繩。 |
| 40 | 淡水桶留岸、糧食不足、船況急迫 | `b9a5329e`、`7de7ba3d` | W：HTTP 200 | CONFIRMED | 先失補給再改航是原記述；「更急」為敘事因果概括，有支持。 |
| 41 | 原計畫南下補給並在千里達一帶過冬，次年再回 | `737af853`、`148173a7`；forced changes steps[0] | W：HTTP 200 | CONFIRMED | 船作此計畫；不得轉述成已實際到千里達。本稿為原計畫。 |
| 42 | 8 月 28 風暴改往亞速群島，再回英格蘭 | `7b5dbe96`、`9b24aa1a`；steps[1:3] | W：HTTP 200 | CONFIRMED | 原文 Trynidad／Açores 航向與日期支持；沒有沿用 EV 誤簡化成實到西印度群島。 |
| 43 | 壞天氣阻止追線索，未到島，也沒家人消息 | `89cdc105`、`bd649f94` | W：HTTP 200；N90：當天可讀 | CONFIRMED | 并非收到留言後自願不找；有斷錨、缺水及風暴的前後。 |
| 44 | 上岸日為外孫女三歲生日 | `adeea438` | W：HTTP 200；EV：web 當天正文可讀 | CONFIRMED | 1587-08-18 與 1590-08-18，相差三年；沒有推定孩子已活到三歲。 |

`5cae000c`、`7ca9a959`、`5c3267a5`、`c2450101` 是承接問題；未假設新的史實，OUT OF SCOPE。字幕縮圖「歷史懸案」、tags 與生成圖的攝影機／光照規格為包裝或藝術示意；它們仍須在最終畫面 QA 看是否誤裝成史料。

## 圖片實體與授權獨立覆核

| 檔案／來源 URL | HTTP／日期／標籤 | 雜湊 | 稿件 caption |
| --- | --- | --- | --- |
| [englishmen-arrival-1590](https://commons.wikimedia.org/wiki/File:The_Englishmen%27s_arrival_in_Virginia_LCCN2001696963.jpg) | API 200；1590；Public domain／Copyrighted False | Commons SHA-1 及 local SHA-256 皆 match | 符合年代與非現場條件；「非實拍」用詞建議改「非現場紀錄」。 |
| [baptism-virginia-dare-1876](https://commons.wikimedia.org/wiki/File:Baptism_of_Virginia_Dare.jpeg) | API 200；1876；Public domain／Copyrighted False | 两種雜湊 match | 想像圖標示合格。 |
| [roanoke-ruins-imagined-1893](https://commons.wikimedia.org/wiki/File:Ruins_of_the_English_Settlement_at_Roanoke.jpg) | API 200；1893；Public domain／Copyrighted False | 两種雜湊 match | 前四章未使用，待完整稿核對場景與警語。 |
| [fort-raleigh-reconstructed-2014](https://commons.wikimedia.org/wiki/File:Panoramic_view_of_the_reconstructed_earthwork_believed_to_have_been_originally_constructed_in_1585._(b95d8d52-1dd8-b71b-0b0b-9ab368abcfb9).jpg) | API 200；2014-04-25；Public domain／Copyrighted False | 两種雜湊 match | 前四章未使用，待確認有「重建的1585工事」，不可當1587聚落證據。 |

## 本部分結論與後續

44 個查核項：CONFIRMED 37、CHANGED 5、NOT FOUND 2（「活樹」須去除；現代南方五十英里待當天重開）。CHANGED 包括圖像史實與字卡因果；未實際套用。第二輪**需要**：目前已超過三個事實／語義修正建議，協調者套用後交另一名 reviewer，不由本輪作者自行宣布已過。

全稿尚缺後三章與 `claims.md`；YouTube description 已預告 Lawson、旱災、刻字石、黃銅戒指、補丁及 2026 宣告，全部仍待後續逐項確認。FCF 的宣告已當天重開，但不能據此說謎團已解；NPS 理論頁更新 2025-07-11 早於 2026-06-04，不是事後反駁。

lint 尚未作為完整稿關卡執行。句長初步量測 76 句全部不超過 40 字；詳細語義、重複和 TTS 建議在 `listener-review.md`。本報告不是旁白試聽或成片驗收。

## 前四章修正讀回

協調者／作者套用後，獨立讀回 SHA-256 `80ec6abc3a7812824900dd7801778312dba0720345acf61cd47408545efb7487`：

- #4 已改船隊；#9 兩景皆屋頂完整、光由門入；#24 已去掉「活樹」。
- #25 已改旁白「五英尺，約是一百五十公分高」，卡片「5英尺，約1.5公尺」，兩者皆是 1.524m 的合理近似，通過。
- #31 已分書封撕毀與畫框地圖雨損；#33 已明說木樁刻字，不再像找到島。
- 兩張 photo 已改 `stock/<SHA-256>.<ext>`，符合既有原檔雜湊；年代／非現場的 captions 保留。

六項修正（含原 NOT FOUND 的「活樹」）均已在此版本確認。表格保留初審 before → after 以供第二輪定位；**前四章沒有未套用的必修項**。#37 的當天重開與後三章仍待驗，完整稿還不能通過。前三句鉤子可懂，新的章標在 `hook-place-not-verdict` 開始第二章，不新增史實。

補驗 #37：2026-10-12 另以 web 當天重開 SM20 正文，2020-11-09 文章確實說 Hatteras 約在 Roanoke 以南五十英里；#37 現改判 **CONFIRMED**。它是現代報導的約距，仍不與懷特原先內陸計畫合併。至此前四章初審列出的待驗項均已解決，後三章與完整稿关卡仍待補。

## 完整稿：後三章及欄位覆核

後三章作者先鎖定 fragment，再由協調者整合。覆核者另讀作者來源表，但沒有把來源表當證據；逐一當天重開下列來源並實際檢視 1893 圖片。

| 代碼 | URL | 當天可讀結果 |
| --- | --- | --- |
| L | [Lawson 原著全文](https://www.gutenberg.org/cache/epub/1838/pg1838-images.html) | web 可讀；同原著純文字 editorial GET HTTP 200。1709 是出版年。 |
| D | [NCpedia Dare Stones](https://www.ncpedia.org/dare-stones) | web 403；editorial 直接 GET HTTP 200 且取得含年代、偽造及第一石條件的正文。 |
| A | [Stahle 等 1998 論文摘要，NCBI 官方介面](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=9554842&rettype=abstract&retmode=text) | editorial GET HTTP 200；讀到 Virginia、1587–1589 及八百年序列。Science 全文未取得。 |
| S17 | [Smithsonian 2017 戒指材料分析訪問](https://www.smithsonianmag.com/history/mystery-roanoke-endures-yet-another-cruel-twist-180962837/) | web 當天完整正文可讀；直接 editorial GET 403 挑戰頁，403 不是正文證據。 |
| G15 | [National Geographic 2015 現地採訪](https://www.nationalgeographic.com/culture/article/150807-lost-colony-roanoke-hatteras-outer-banks-archaeology) | web 當天完整正文可讀；直接 GET 有 404／200 差異，因此依當天 web 的可讀文章核對，不把 HTTP 200 自動當真文。 |
| R | [NCLR：Ewen／Shields 專書書評](https://nclr.ecu.edu/wp-content/pv-uploads/sites/460/Haspel-EwenShields-review.pdf) | web 當天重開 1 頁 PDF 可讀；是書評，不偽裝成原始發掘報告。 |
| F | [FCF 2026 宣告](https://www.firstcolonyfoundation.org/news/lost-colony-is-found/) | web 當天正文可讀；來源刷新收據 HTTP 200。只支持團隊作此宣告。 |
| FN | [FCF 新聞索引](https://www.firstcolonyfoundation.org/news/) | 獨立 editorial GET HTTP 200，宣告的索引日期 June 4, 2026 可讀。 |

| # | 主張 | where | URL／狀態 | 判定 | before → after／核對理由 |
| --- | --- | --- | --- | --- | --- |
| 45 | 1709 年勞森記下祖先故事／1709 年祖先自述 | `04fe502e`；`h02-history-generation-gap.data.left.points[0]` | L：HTTP 200 | CHANGED | 1709 是書出版年，不是已知談話日；→「勞森的書在一七零九年出版，記下島民的祖先故事。」卡片要寫出版的紀錄。 |
| 46 | 祖先有白人、能讀書；隔一百多年不能指認某殖民者 | `72d80a5e`、`d1c58c2b`、`aae17c5d`、`a9e17aca`；generation-gap 卡 | L：HTTP 200 | CONFIRMED | 原文是島民告訴作者的祖先說法；未引用灰眼睛和貶抑評語，未認定現代族群後裔身分。 |
| 47 | 勞森沒見过 1587 年殖民者 | `e8d5e691` | L：HTTP 200 | CHANGED | 来源沒有支持這個絕對否定；→「這不是一五八七年現場留下的紀錄。」由記錄層級說明，而非杜撰作者沒有經歷過的任何接觸。 |
| 48 | 波瓦坦屠殺說是另一個故事／傳聞 | `56df705f` | EV：web 當天正文；R：當天 PDF | CONFIRMED | 掛在「故事」下，未認定確實發生。 |
| 49 | 史崔奇沒有親眼見過屠殺 | `4f036f32` | EV、R：當天可讀 | CHANGED | 書評說 second-hand 資訊；→「史崔奇記下的是轉述，沒有留下親見屠殺的紀錄。」不能以文字缺口當全人生的絕對證明。 |
| 50 | Virginia 樹輪重建 1587–1589 區域旱期 | `7068cff0`、`10df3871`；drought stats[0] | A：HTTP 200 | CONFIRMED | 原始摘要有區域與年份；不是 Outer Banks 當地量測，不推定殖民者剛好只活三年。 |
| 51 | 八百年重建序列最嚴重一段，可能加重糧食壓力 | `0fdf36de`、`dd29a13e`；drought stats[1] | A：HTTP 200 | CONFIRMED | 地域與序列已限縮，可能因果沒有升格全員死於旱災。 |
| 52 | 十九世紀成為文學題材 | `c3df0b73` | SM20：當天正文；R：當天 PDF | CONFIRMED | 不聲稱查明首個命名者、精確首用年或之前完全沒討論此事。 |
| 53 | 1893 畫把完整地名刻在樹上 | `8b0f9364` | C：API 200；實際圖檔目視 | CHANGED | 可清楚看見 CROA…，其餘受線條／樹緣遮住；→「這張畫，把地名刻在一棵大樹上。」只講可目視的位置差異，不說完整文字皆清晰可見。 |
| 54 | 此圖為 1893 後人想像，刻字位置與目擊記述不同 | `8c0f94f7`；`h02-history-ruins-picture.data` | C：API 200；W：HTTP 200；圖檔目視 | CONFIRMED | 年份、作者 John Parker Davis 與警語吻合；不是現場照。 |
| 55 | 1937 起四十幾塊 Dare Stones，多數偽造、第一塊未定 | `9a193f80`、`b2a1a98c` | D：HTTP 200；R：當天 PDF | CONFIRMED | NCpedia 48 與書評 47 不同，稿子近似數字保留；沒有把第一塊說成真品。 |
| 56 | 戒指同出土物只講十七世紀後期 | `14d603d3` | S17：當天可讀／直接 403 | CHANGED | 原來源範圍 1670–1720 跨十八世紀初；→「戒指附近的器物，年代跨到十八世紀初。」不是替戒指本身定年。 |
| 57 | 哈特拉斯戒指曾被當黃金及英格蘭家族線索；後測為銅、鋅黃銅 | `b9949b9c`、`ba949d2f`、`21a67841`；material-owner 卡 | S17：當天可讀／直接 403 | CONFIRMED | 2017 採訪分析人員有高銅、鋅及黃銅結果；家族指認未確認，稿子沒有沿用 2015 金含量。 |
| 58 | 材料、年代、地層、使用者是不同判讀問題 | `eb0658d3`、`3c1a27d4`、`adae2990`、`aeae2b23`、`8087c100`、`15e3784d`、`72e32d98`、`73e32f2b`、`f9f6eb48` | S17、G15：當天可讀；NT：當天可讀 | CONFIRMED（方法性推論） | 原案例實際存在材質改判、較晚混物及交易等解釋。這是對案例的合理判讀，沒有冒稱本片做新測定或知道持有人。 |
| 59 | 其他歐洲器物與十七世紀中期物件混雜 | `ab3af46c` | G15：當天正文 | CONFIRMED | 別與戒指的 1670–1720 範圍合成同一精確層位；稿子分成不同來源的例子。 |
| 60 | 歐洲器物可能因交易到原住民村落 | `515ebefd`、`40e75a82` | NT：當天可讀；S17、G15：當天正文 | CONFIRMED | 有「可能」，沒認定特定物件一定經交易。 |
| 61 | 地圖補丁下堡壘狀符號形成西邊內陸搜尋線索 | `3bd684e6`、`0e523c82` | NT：當天可讀；F：當天正文 | CONFIRMED | 符號不證明該處實建堡壘，生成圖是無字紙張示意，未使用館方數位圖。 |
| 62 | 伯蒂郡出土英格蘭器物、兩处集中地點 | `c9ab868d`、`de06c81d`、`dd06c68a` | NT：當天可讀；F：當天正文 | CONFIRMED | Sites X、Y 是兩處資料；不等於已確認殖民者居住。 |
| 63 | FCF 把兩點解讀為分散農場，2026-06-04 宣告找到 | `f93ec640`、`b475efb8`、`b575f14b`；announcement-dates 左卡 | F：當天正文；FN：HTTP 200 | CONFIRMED（團隊主張） | 說「團隊看成／宣告／判斷」，沒有轉成學界定論，農屋畫面須維持示意。 |
| 64 | NPS 2025-07-11 頁早於 2026 宣告 | `c556a225`；announcement-dates 右卡 | NT：當天可讀；FN：HTTP 200 | CONFIRMED | 兩個日期先後正確，不稱 NPS 是事後回應。「前一年」在此是上一個曆年，卡片顯示精確日期。 |
| 65 | 聚落指認須排除較晚器物／交易；假如房屋可確認會有居住脈絡 | `a2a221f7`、`40e75a82`、`6aaa024d`、`c33bbeea` | NT：當天可讀；S17、G15：當天正文 | CONFIRMED（方法性推論） | 條件式房屋例子沒有冒稱已出土這間屋；也沒有冒稱讀到未取得的 FCF 技術報告。 |
| 66 | 「遷移或融入」都是後人推論 | `3acd91a4`；`h02-close-evidence-levels.data.right.points[0]` | W：HTTP 200；NT：當天可讀 | CHANGED | 懷特本人就把記號讀成遷移到島；→「分散或融入，是後人提出的解釋。」右卡亦去掉「遷移」，不能把他的當時理解全推給後人。 |
| 67 | NPS 較早評估無確定村落連結；器物不能認出每人的結局 | `7aaa7142`、`2b2d8064`、`f08503c5`；evidence-levels 卡 | NT：當天可讀；F：團隊主張併看 | CONFIRMED | 明說較早評估，沒有說全球沒有新評估／FCF 沒提出聚落解釋。 |
| 68 | 刻字為懷特親見、未確認家人或到留言去處 | `3bcd9337`、`6469b019`、`9b2c16c8`、`bf77b9cc`、`a89c5c7f` | W：HTTP 200；N90：當天可讀 | CONFIRMED | 「未完成航程」沒有假裝證明所有後續搜尋都不存在；結尾保留讀法與命運的差別。 |
| 69 | 說明欄稱土壘照片出鏡、c34 列第三圖為土壘 | `youtube.description`；`claims.md:c34`、與企劃差異 | 整稿 photo 實用集合＋C：API 200 | CHANGED | 實際第三張是 1893 想像遺址圖，土壘沒出鏡；同步換說明、主張、URL 與差異段，不描述未採素材。 |
| 70 | 標題 CROATOAN 意思、縮圖非咒語／知道去處卻找不到人 | `youtube.title`；`thumbnail.data` | W：HTTP 200；NT：當天可讀 | CONFIRMED | 記號讀法支持標題承諾；沒有聲稱超自然事件存在或已解案。 |
| 71 | 第三張 image 真檔、SHA256、caption、credit | `h02-history-ruins-picture.data`；stock 原檔 | C：API 200；local hash match；目視 | CONFIRMED | local hash `54495b4e…3d0c` 與來源原件相符；公有領域與歷史警語均已給。 |
| 72 | 問句、CTA、生成圖運鏡與色調 | 承接問句、`a79c5aec`、`aa9c5fa5`；藝術提示 | 不適用 | OUT OF SCOPE | 非新史實。構圖示意不冒充史料；剪輯／播放 QA 尚未發生。 |

後三章修訂版讀回：SHA-256 `c4b09b35350f89778d82f5f91fcd24d5bba4d31da0c1b456abc26c1eadeafe74`，134 句全部不超過 40 字。#45、47、49、53、56、66 的旁白修正均已在此版本讀回；這些行的原 ID 均未改。

整稿源碼／來源表仍由協調者最後合併及做 emotion／outro 格式調整，待其正式 freeze 後記最終哈希、讀回 #45/#66 的卡片和 #69 metadata、執行完整 lint。第二輪必須換獨立 reviewer；本輪報告不是第二輪、旁白或成片驗收。

## 最終首輪收據

2026-10-12 再次讀入最終完整稿及主張表，哈希與開頭一致。初審 12 個 CHANGED、1 個須去除無來源限定的 NOT FOUND，以及南方距離的當天待驗來源，均已解決：

- #45 左卡為「1709 年出版的記錄」；#66 右卡為「分散或融入」。旁白和卡片同步。
- #69 說明欄、三張 assets、`claims.md:c34`、企劃差異及後三章來源表，均為 arrival／baptism／1893 Ruins；未出鏡的 NPS 土壘不再當本片照片。主張表的戒指時代敘述亦已改跨十八世紀初。
- 今日重開來源的日期與來源層級已區分；Gutenberg 原記述、Lawson 原著、NCBI 摘要、研究方宣告與現代採訪各自只支持適當範圍。ECU 官方庫藏指南由第二輪补作，本輪不把它冒稱自己已重開。
- `node tools/video/cli.mjs lint --slug curio-h02` 獨立重跑：**exit 0、0 errors、3 warnings**。三項均為 91 插圖提示中 third／come／daylight 重複詞彙，不是事實錯誤；實際畫面多樣性仍須聯絡表與成片 QA。
- lint 估計 11.3 分鐘、2341 spoken units。這是文字估算，正文與成片至少8分鐘仍待 TTS／媒體實測；不能以估算或額外停頓當達標證據。134 句全部不超過40字。

與 brief 的差異已由稿件／主張表記錄：現場柵欄不寫「新建」；1709 為書出版年；第三照片改1893想像圖；懷特已把記號讀成遷移，不能全列後人的推論。brief 的「當天沒有第三方定論」不作全球不存在評估的可驗證事實，本片正文没有採用這種絕對說法。站主立場仍維持「原記述／傳聞／推論分開、未知不填成超自然」，未見意見不符。

**首輪結論：PASS_FACTS_ROUND_1；SECOND ROUND REQUIRED = YES。** 本輪未編輯作者稿件、未付費、未 approve、未做 Git、未聽合成旁白或驗成片。

最後一次來源表讀回：`claims.md` SHA-256 `6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`，尾部也已將1709年的自述措詞改為出版記錄；`video.json` 哈希未變。沒有新增未核對的旁白或事實。
