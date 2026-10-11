# H02 獨立事實覆核：第 2 輪

日期：2026-10-12（Asia/Taipei）。覆核者 `h02_verify2` 未參與本片撰稿，與首輪覆核者不同。**PASS / SCRIPT FACT CHECK**：下列雜湊的完整稿及主張表沒有剩餘必修事實項目。此結論只適用於文字、畫面提示、字卡與既有圖片素材，不代表尚未生成的旁白、插圖或成片已驗收。

- `video.json` SHA-256：`7b8d066cbb42ad7ee621171fcaedcda7c5eeafb9acf9bf8dc6c7d287b08c482d`
- `claims.md` SHA-256：`6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`
- 讀回完整 109 景、134 句、91 個插圖鏡頭；逐句檢查 `text`，本版沒有 `say` 欄位。另檢查全部字卡、photo caption、生成提示、assets、縮圖、YouTube 標題／說明／tags。下表按同一事實合併重複出現的位置，對應全部 37 個作者主張群；沒有把 `claims.md` 當作證據。
- 權限僅寫此報告；未改作者稿、brief 或其他檔，未付費、approve 或操作 Git。第二輪發現的 `living tree trunk` 由協調者修改，本人讀回確認。

## 當天來源與可讀狀態

直接 GET 使用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`；同站直接請求間隔至少一秒。沒有把遭阻擋的頁面當作已讀全文。

| 代碼 | 來源 URL | 本輪可讀狀態／層級 |
|---|---|---|
| W | [White 1587、1590 記述，Hakluyt 卷十三](https://www.gutenberg.org/cache/epub/25645/pg25645-images.html) | editorial GET HTTP 200，web 完整正文可讀；重讀離別與返航原文。是懷特的一份記述，現代轉述不是新增目擊者。 |
| N87 | [NPS 1587 航程](https://www.nps.gov/fora/learn/historyculture/1587-the-lost-colony.htm) | 當天 web 正文可讀；官方歷史解說頁。 |
| N90 | [NPS 1590 航程](https://www.nps.gov/fora/learn/historyculture/1590-rescue-voyage.htm) | 當天 web 正文可讀；官方歷史解說頁。 |
| NT | [NPS 主要假說](https://www.nps.gov/fora/learn/historyculture/major-theories-of-the-lost-colony.htm) | 當天 web 正文可讀；頁尾更新日仍為 2025-07-11。不能當作對 2026 年宣告的回應。 |
| L | [Lawson 原文](https://www.gutenberg.org/cache/epub/1838/pg1838-images.html) | 當天 web 正文與轉錄說明可讀；1709 是出版年。對島民說法屬當事旅行者記錄，對 1587 人員則屬後來的祖先傳聞。 |
| EV | [Encyclopedia Virginia：Roanoke Colonies](https://encyclopediavirginia.org/entries/roanoke-colonies-the/) | 當天 web 完整正文可讀；學術公共歷史解說，非殖民期原件。 |
| D | [Stahle 等 1998 論文摘要，NCBI](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=9554842&rettype=abstract&retmode=text) | editorial GET HTTP 200，完整摘要可讀；原研究摘要。沒有声稱讀到 Science 付費全文。 |
| DS | [NCpedia：Dare Stones](https://www.ncpedia.org/dare-stones) | editorial GET HTTP 200，正文可讀；北卡官方圖書館整理。 |
| E | [ECU Croatan Archaeological Site Collection](https://digital.lib.ecu.edu/special/ead/findingaids/1061/) | web 403；editorial GET HTTP 200，完整庫藏說明可讀。出土研究機構的官方館藏說明，直接支持 2017 年黃銅檢驗及原先金／家族說法。 |
| S17 | [Smithsonian 2017 戒指報導](https://www.smithsonianmag.com/history/mystery-roanoke-endures-yet-another-cruel-twist-180962837/) | editorial GET 403；當天 web 正文可讀。是直接採訪研究者的報導，非原始實驗報告；材料分析另以 E 交叉確認。 |
| NG | [National Geographic 2015 現地報導](https://www.nationalgeographic.com/culture/article/150807-lost-colony-roanoke-hatteras-outer-banks-archaeology) | editorial GET HTTP 200，web 正文可讀。出土年代限制是當年現地報導；其中舊金戒指判斷已失效，沒有沿用。 |
| F | [FCF 宣告](https://www.firstcolonyfoundation.org/news/lost-colony-is-found/) | 當天 web 正文可讀；發掘團隊自己的主張。 |
| FD | [FCF News 日期索引](https://www.firstcolonyfoundation.org/news/) | editorial GET HTTP 200，明列 2026-06-04。 |
| R | [ECU NCLR 2024 專書書評](https://nclr.ecu.edu/wp-content/pv-uploads/sites/460/Haspel-EwenShields-review.pdf) | 當天 web PDF 全文可讀；確認 Strachey 的轉述層級及十九世紀文學案例。這是學術書評，未假裝讀到所評專書全文。 |
| C | [Commons arrival](https://commons.wikimedia.org/wiki/File:The_Englishmen%27s_arrival_in_Virginia_LCCN2001696963.jpg)、[baptism](https://commons.wikimedia.org/wiki/File:Baptism_of_Virginia_Dare.jpeg)、[Ruins](https://commons.wikimedia.org/wiki/File:Ruins_of_the_English_Settlement_at_Roanoke.jpg) | 三份 imageinfo API 各 HTTP 200；原件 metadata、Commons SHA-1 及本機 stock SHA-256 分別重核。 |

表中沒有列 HTTP 數字的 web 可讀來源，是工具未提供 HTTP 狀態碼；沒有自行補成 200。有限查證沒有取得 FCF 宣告之後的独立技術評估，因此本片不宣稱全球不存在第三方評估，也不分析未取得的報告。

## 完整事實清單與判定

以下位置中的短名沿用所列場景前綴。所有 CONFIRMED 都是對稿中受限制的表述，不代表批准其來源中更強的結論。

| #／claim | 可查內容 | 位置（line ID／scene.data） | URL 代碼／狀態 | 最終判定與 before → after |
|---|---|---|---|---|
| 1／c1 | 一百多人／一百一十多人 | `530240f0`、`bd947762`、`c2450101`；description | N87、NT：可讀 | CONFIRMED；保留近似人數，未混用出航及留下的確數。 |
| 2／c2 | 1590-08-18 回島，前夜吹號唱歌、天亮登岸 | `53923c71`、`6387c813`、`c8106dd9`；相應 prompts | W：200；N90：可讀 | CONFIRMED；夜間與清晨有分鏡。 |
| 3／c3 | 8 月 22 日請求、25 日文件、27 日離開；先拒絕 | `55c9e647`、`385bc548`、`be38542e`、`ea6f1c25`；`farewell-august-dates.data` | W：200 | CONFIRMED；三日分開，沒有把聯名日移到離島日。 |
| 4／c4 | 1587 七月船隊抵達；原定乞沙比克灣，領航員使其留島 | `ad443391`、`7d3976ee`、`de9770ac`、`e8e1f755`；destination compare | W：200；N87：可讀 | CONFIRMED；首輪「一艘船」已改「船隊」。單艘示意沒有聲稱整支船隊只一船。 |
| 5／c5 | 舊屋未毀，長瓜，鹿在其中；開始修屋 | `609abd25`、`cb08d4da`；old-dwelling／deer-melon prompts | W：200 | CONFIRMED；首輪塌頂已改完整屋頂、門口採光。堡壘拆毀與住宅仍立沒有合併。 |
| 6／c6 | 曼提歐協助溝通，稱友但曾誤襲；補給與冬季壓力 | `07721bae`、`f6e27da0`、`069ea2a2`、`1ff46026` | W：200；N87、EV：可讀 | CONFIRMED；没有把關係說成始終和平，沒有杜撰對話或傷害畫面。 |
| 7／c7 | 懷特女兒生 Virginia Dare；出生 1587-08-18，離島後 9 日、返島日為第三生日 | `51dcd3dc`、`9950a707`、`be38542e`、`adeea438`；dates card | W：200；EV：可讀 | CONFIRMED；日期差正確，沒有聲稱她當時仍在世或等祖父。 |
| 8／c8 | 先約好刻去處，困境才加十字；現場無十字 | `f8974907`、`1b1b3b7d`、`e86ab0b4`、`369cdc7d`、`d510fc74`；message-rule | W：200 | CONFIRMED；「找到克羅托安」已改明確木樁刻字，未暗示實際已到岛。 |
| 9／c9 | 1588 防守無敵艦隊、補給船遭法國船交戰折返；1590 私掠船 | `e4b5d68e`、`5a4ea7a7`、`deafa764`、`590718a5`、`384b98db`；delay steps | N90、EV：可讀 | CONFIRMED；留港命令與補給船例外都有，不說所有船一律沒出港。 |
| 10／c10 | 樹上 CRO、去皮入口木樁 CROATOAN，5 英尺約 1.5 公尺 | `6abe644b`、`8697084e`、`01e14e26`、`527830a9`；two-carvings、tree-cro prompt | W：200；N90：可讀 | CONFIRMED；首輪活樹 heading 已移除；本輪另發現 prompt 的 living，協調者改成 tree trunk，已讀回。5×0.3048=1.524，口語近似正確。 |
| 11／c11 | 1590 住宅拆下，高大木柵欄及突出防守結構 | `543e602a`、`3ee52e06`；dismantled-houses／defensive-palisade prompts | W：200 | CONFIRMED；不替柵欄單獨定建造年份，不把拆屋說成風暴摧毀。 |
| 12／c12 | 鐵條、鉛等重物仍散置、草覆 | `d30453cd`；heavy-metal prompt | W：200 | CONFIRMED；不說一切搬空。 |
| 13／c13 | 五箱、三箱屬懷特；書封撕下，畫框地圖雨損，盔甲鏽蝕；敵人挖箱是其推測 | `c11d2375`、`435e5db2`、`3f471fa8`、`a1530843`、`344d40fb`、`ecc48106`；chests-and-damage | W：200 | CONFIRMED；卡片已修「雨水」總括因果，沒有把箱損當全聚落遇襲證明。 |
| 14／c14 | 沿溪找船艇、小炮未找到 | `86b291b5`、`9e5b48ba`；creek-search／empty-mooring | W：200 | CONFIRMED；缺失與誰帶走分開，未推斷全員乘船。 |
| 15／c15 | 懷特寫自己高興，認為到朋友島；不等於全員命運證明 | `530240f0`、`ddac8184`、`e3138e28`、`69efb42f`；hook、message-rule、description、thumb | W：200 | CONFIRMED；開場已署為他自己的文字反應，推論界限保留。 |
| 16／c16 | Croatoan 族名兼地名，今日哈特拉斯島一帶 | `f842d461`、`948e50c0`；hook-island-home／route-croatoan-place | NT：可讀 | CONFIRMED；「一帶」保留地域差異，不聲稱現代後裔血統已證實。 |
| 17／c17 | 原先內陸 50 英里與後來南島約 50 英里不同方向 | `421fe082`、`d37cb405`、`9ee17073`、`ced77e9e`；two-fifties | W：200；NG、S17：可讀 | CONFIRMED；本輪重開的現地報導確認島距近似值；不拼成同一搬遷計畫或精密航圖。 |
| 18／c18 | 四套錨纜剩一、水留岸、食物不足；南下過冬計畫，8-28 風暴改亞速後回英格蘭 | `ebd0c9ba`、`8a6d5e5d`、`b9a5329e`、`737af853`、`148173a7`、`7b5dbe96`、`9b24aa1a`、`89cdc105`、`bd649f94`；forced-changes | W：200 | CONFIRMED；原計畫千里達不等於曾抵達；沒有說收留言後自願立刻不找。 |
| 19／c19 | 存世目擊文字為懷特記述，未能到島親見家人 | `4b1ee5e0`、`bd649f94`；description、one-witness | W：200；N90、EV：可讀 | CONFIRMED；「只有懷特」說的是存世目擊文字，沒有說只有一人登岸。 |
| 20／c34 | 三張實採圖的作者、年代、非 1587 現場及授權 | arrival／baptism／Ruins photo.data；assets、description | C：三 API 200 | CONFIRMED；實採集合與 metadata 一致，沒有 NPS 土壘出鏡。 |
| 21／h02e1 | Lawson 1709 出版，島民祖先自述，不能辨認特定殖民者 | `72d80a5e`、`04fe502e`、`d1c58c2b`、`e8d5e691`、`aae17c5d`、`a9e17aca`；generation-gap | L：可讀 | CONFIRMED；1709 已改出版年；不斷言其絕無見過任何殖民者。原文是祖先能讀書，未用灰眼睛論證血統。 |
| 22／h02e2 | Powhatan 下令殺害之說是 Strachey 轉述 | `56df705f`、`4f036f32`；兩個 office prompts | EV、R：可讀 | CONFIRMED；從「沒親眼看過」改為未留下親見紀錄，保留傳聞層級，沒有視覺重演屠殺。 |
| 23／h02e3 | Virginia 樹輪、1587–1589、800 年最嚴重旱期；可能生存壓力 | `7068cff0`、`10df3871`、`0fdf36de`、`dd29a13e`；drought-sequence | D：200 | CONFIRMED；區域重建與因果可能性均限定，沒有把摘要變成外灘實測或全員死因。 |
| 24／h02e4 | 十九世紀成為文學題材 | `c3df0b73`；romantic-book | R：可讀 | CONFIRMED；當天書評可核對十九世紀作品案例；稿中不講最早命名者或精確首用年。 |
| 25／h02e5 | 1893 後世遺址圖將地名畫在大樹上 | `8b0f9364`、`8c0f94f7`；Ruins caption、assets | C：200；W：200 | CONFIRMED；本人打開實檔，樹幹有地名字樣。旁白不要求辨讀整個完整拼字；明示畫作與史料位置不同。 |
| 26／h02e6 | 1937 起四十幾刻字石，多數偽造，第一塊仍未定 | `9a193f80`、`b2a1a98c`；stones prompts | DS：200；R：可讀 | CONFIRMED；保留 47／48 口徑差，沒有認定第一塊是真的。 |
| 27／h02e7 | 島上戒指曾認為金／英格蘭家族，2017 測成黃銅，持有人未定 | `b9949b9c`、`ba949d2f`、`21a67841`、`3c1a27d4`、`adae2990`、`aeae2b23`；material-owner | E：200；S17：可讀 | CONFIRMED；官方庫藏說明確認材質，採訪另述銅、鋅。材質不能替戒指認主人；未用 2015 舊金判定。 |
| 28／h02e8 | 戒指附近器物跨至十八世紀初，其他歐洲器物混十七中物品 | `14d603d3`、`ab3af46c`、`8087c100`；dating-first／mixed-layer | S17、NG：可讀；E：200 | CONFIRMED；首輪已修 1670–1720 跨世紀，未把所有器物定成 1587 年。兩報導描述的器物範圍不同。 |
| 29／h02e9 | 材質、年代、地層、同出土物與身分為不同問題 | `eb0658d3`、`15e3784d`、`72e32d98`、`73e32f2b`、`f9f6eb48`；context prompts | E：200；NT、S17、NG：可讀 | CONFIRMED（作者方法推論）；沒有主張本片新做出年代量測，土層鏡頭是示意。 |
| 30／h02e10 | 歐洲器物可能經交易流動，產地不指認使用者 | `515ebefd`、`f9f6eb48`、`40e75a82`；trade-route | NT：可讀；E：200 | CONFIRMED；可能性限定，未斷言特定器物必為交易品。 |
| 31／h02e11 | 地圖補丁遮堡壘狀符號，提示往西內陸搜索 | `3bd684e6`、`0e523c82`；map-patch／westward-clue | NT、F：可讀 | CONFIRMED；不說堡壘真正建成，示意紙圖沒有冒充館方地圖。 |
| 32／h02e12 | 伯蒂郡發掘英格蘭器物，兩處集中地點 | `c9ab868d`、`de06c81d`、`dd06c68a`；bertie-excavation／two-site-trays | NT、F：可讀 | CONFIRMED；Site X／Y 對照依發掘方公告，不視作殖民者身分已確定。 |
| 33／h02e13 | FCF 2026-06-04 宣告，將兩地視為分散農場 | `f93ec640`、`b475efb8`、`b575f14b`；announcement-dates | F：可讀；FD：200 | CONFIRMED；只确认團隊確實提出此主張，不確認結案。示意農屋已標 hypothetical／reconstruction。 |
| 34／h02e14 | NPS 2025-07-11 早於 2026 宣告 | `c556a225`；announcement-dates | NT：可讀；FD：200 | CONFIRMED；「前一年」指前一曆年，卡片列完整日期，不是滿一年或事後回應。 |
| 35／h02e15 | 身分與生活脈絡須獨立檢驗，並處理交易、晚來可能 | `a2a221f7`、`40e75a82`、`6aaa024d`、`c33bbeea`；identified-house | NT、F：可讀；E：200 | CONFIRMED（作者方法推論）；房屋是假設，不是已挖出的住宅。未宣稱全球無第三方評估。 |
| 36／h02e16 | NPS 較早評估無唯一聚落連結；分散／融入仍可能、無每人結局 | `7aaa7142`、`3acd91a4`、`2b2d8064`、`f08503c5`、outro；evidence-levels | NT、F：可讀 | CONFIRMED；卡片已移除將「遷移」也全歸後人之誤，沒有漏掉懷特本人已解讀搬遷。 |
| 37／h02e17 | 親見刻字、未到指向島、家人結局未確認 | `3bcd9337`、`6469b019`、`9b2c16c8`、`bf77b9cc`、`a89c5c7f`；結尾、title、thumb、description | W：200；N90：可讀 | CONFIRMED；「去向未定」是在區分留言與實際命運，沒有聲稱刻字位置的意義未知。 |

問題句、訂閱邀請、鏡頭方位／採光、無字紙張、沒有額外史實的情緒提示，屬 OUT OF SCOPE（風格），已讀但不另假設事實。縮圖「不是咒語」及 title 的問句受 W 支持；不是聲稱全案已解。製作日期、圖像披露及 tags 与実採資產相符。

## 首輪修正逐項讀回

本輪重查全部首輪變更，加上完整後三章；未只抽查三分之一。首輪前四章需改的船隊、完整屋頂、樹幹／5 英尺、雨損因果及刻字而非抵島，均已確認。後三章 1709 出版年、Lawson 現場紀錄界限、Strachey 轉述、1670–1720 跨十八世紀初與後人推論的範圍，也全部確認。

協調者另同步修正 `claims.md` 作者備註，使 1709 始終標為著作出版年，沒有指定談話年份；本人重讀末段並更新上列最終主張表雜湊。`video.json` 沒有因此變動。

本輪新增一項：`return-tree-cro.data.prompt` 的 `living tree trunk` → `tree trunk`，已由協調者套用，最終雜湊內可見。**本輪新增事實修正 1 項，沒有超過 3 項，不觸發再換人的第三輪。**

## 圖片與授權

| stock 檔名／SHA-256 | 當天 API 與本機讀回 | 圖说與用途 |
|---|---|---|
| `13d6c3c507e6155fee47b2c247ee88ff24ea4fc36498dac8542d910a2f6526ef.jpg` | API 200；Commons SHA-1 match；stock SHA-256 match；1590；Public domain／Copyrighted False | de Bry 依 White 的後世版畫，不是 1587 现场。 |
| `485da4dab0e4dfc7980301bf3fab61b508a099146a998a162f1753f939c09487.jpg` | API 200；兩種 hash match；1876；Public domain／Copyrighted False | Sheppard 想像受洗圖，畫面明示非當年紀錄。 |
| `54495b4e26c7c1ff265295e31ecbc545df9d2f1a7b2479eb18302bac587c3d0c.jpg` | API 200；兩種 hash match；1893；Public domain／Copyrighted False | Davis 想像遺址圖；本人看過實檔，明示刻字位置與目擊文字不同，只用來比較後世畫法。 |

本片不用 NPS 土壘照，不用英國博物館數位地圖，不借用 Dare Stones 或現代考古學家人物肖像。生成圖尚未存在，其考古道具及一般人物提示僅作示意；成片仍須確認字幕警語可見、生成圖沒有意外文字或把想像圖誤装成原始紀錄。

## 聽眾與機械檢查

- 全 134 句已檢查：沒有超過 40 字、Latin 字母、括號或 URL；沒有「經查證／本影片／官方文件」驗證旁白。中文人名仍需实际 `check-audio`，文字合格不證明 TTS 發音。
- 沒有與已選大綱 A 矛盾的作者意見；方法性推論以「可能／假如／需要」與實例相接。
- 本人以 bundled Node 24.19.0 執行 `tools/video/cli.mjs lint --slug curio-h02`：exit 0，**0 errors、3 warnings**。預估 11.3 分鐘、2341 spoken units，開場章 18 秒。這是估算，未聲稱已實測媒體長度。
- 三個 warning 為 prompt 中 `third`、`come`、`daylight` 重複，屬構圖文字／風格提醒。場景實際依船、住宅、島岸、書房、石碑、實驗室、器物與發掘等變換；生成後仍須看聯絡表，不把 lint 當作畫面好看的證明。
- 縮圖 ≤6 單位的文字與史料主線相符。圖卡上的 CRO／CROATOAN 是後期排字，不能依賴 AI 拼字。

## 結論

37 個主張群最終 CONFIRMED；本輪新增已完成修正 1 項；NOT FOUND／未解決必修 0 項。日期易變部分是 FCF／NPS 網頁狀態，已保留 2026-06-04 宣告與 2025-07-11 較早評估的時間差。史料是誰的記述、現代出土物能說明多少、後世圖像與目擊文字的差別都已分清。**可進入旁白合成與媒體品管；尚不能稱影片完成、站主已播放驗收或已上架。**
