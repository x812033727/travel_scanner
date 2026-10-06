# 《偶的江湖》第 1–8 集共用角色表說明

`cast.json` 是第 1–8 集角色物件的唯一來源。每一集的 `video.json` 只放這一集會入鏡的角色，但每個角色物件都要從 `cast.json` 整個照抄（`id`、`name`、`appearance`、`voice`、`shot_looks` 全部逐字，不刪 look、不改順序），設定圖才能共用。旁白聲音照抄 `narrator_voice`（與第 1 集表頭 `voice` 相同）。

逐鏡選 look 的寫法是 `scene.data.character_looks: {"<角色 id>": "<look id>"}`。被選的角色必須在同一鏡的 `characters` 裡，而一鏡最多 3 個角色。沒有選 look 的鏡頭一律用基本外觀。所以只拍局部的插鏡（手、胸口、髮尾）不列角色，傷、印、道具都要直接寫進 prompt。

## 第 1 集角色的改動

- `ji-wushuang`：appearance 刪掉「, one faint gold seal mark on the back of her right hand」。她第 2 集起手背有兩道印（書院、玄門），印記一律寫在插鏡 prompt，基本外觀與 look 都不寫印。
- `ji-wen`、`ji-wushuang`、`bao-sanqian`、`yin-wusheng`、`nie-gutie`：加了 `shot_looks`，appearance、name、voice 一字未改。
- `luo-qingyan`、`shen-guihe`、`xuanmen-elder`、`yan-hui`：完全沒動。

## 第 6 集的改動（2026-10-05）

- `shen-guihe`：加了 `shot_looks`（`shen-bedridden`，本體昏臥書齋）；appearance、name、voice 一字未改。
- 新增 `sha-nu`（紗女）、`wuming-jianke`（無名劍客）：沈歸鶴的兩個分魂，都用他的 Iapetus，理由見下方〈兩個化身為什麼用同一個聲音〉。
- 其他十三人與已有的 look 完全沒動。用 node 核對過：第 1–5 集成品 `docs/videos/ou-de-jianghu-e00N/video.json`、`series.json` 與 `ep1–5/header.json` 裡的角色物件，舊欄位（`id`、`name`、`appearance`、`voice`、已有的 `shot_looks`）全部與 `cast.json` 逐字相同；**唯一的差別是 `shen-guihe` 在那五集裡還沒有 `shot_looks` 這個鍵**（新 look 是本次加的）。每集自己的 `video.json` 與 `series.json` 一致，所以第 1–5 集的 lint 照樣過；但照第 1 集的先例（`ji-wen` 在第 1 集成品裡已帶著第 5 集才用的 `jiwen-struck`、`jiwen-sealed`），要讓五集與 `cast.json` 再次逐字相同，得對第 1–5 集各跑一次 `node header.mjs --ep N` 與 `node merge.mjs --ep N`（ids.json 會保住 line id；設定圖還沒畫，不會作廢任何東西），再跑 `cli.mjs script`。這一步由主控決定什麼時候做，本次沒有動成品。

## 第 7 集的改動（2026-10-05）

- 新增 `canglan-ke`（滄瀾客）、`yuelan-ke`（岳嵐客「赤羽」）：西嶺兩位隱士，第 7 集同日下山。聲音用最後兩個沒用過的男聲——滄瀾客 Zubenelgenubi、岳嵐客 Algieba，理由見下方〈第 7 集的兩個新聲音〉。
- `yuelan-ke` 帶兩個 look（`yuelan-crest`、`yuelan-crippled`），都是第 7 集外港那一場用的；`canglan-ke` 只有基本外觀。基本外觀都只寫第 7 集出場時的樣子（赤羽的素袍與紗巾、滄瀾客的毛皮斗篷與素劍），不寫 setting 裡後面集數的狀態（紅銅折翼冠、左臂藏袖、白髮拄杖、無愧劍）。
- 其他十六人與已有的 look 一字未改。用 node 核對過：第 1–5 集成品 `docs/videos/ou-de-jianghu-e00N/video.json` 的角色物件（含 `shen-guihe` 的 `shot_looks`，第 6 集準備時已重新同步）全部與 `cast.json` 逐字相同；第 6 集成品還沒合併（`ep6/` 只有分場表與表頭）。
- `ep7/meta.json`、`ep7/check-act.mjs` 照第 6 集的形狀建好，`node header.mjs --ep 7` 產出十三個角色的表頭；縮圖只填了 `headline`，`shot` 由主控在幕寫完後填。
- 2026-10-06（第 7 集分場表第 1 輪修訂）：`yuelan-ke` **新增第三個 look `yuelan-covered`**（舊的兩個 look 一字未改）：同 `yuelan-crippled`，但劃開的衣襟被右手攏在胸前、雙淵紋看不見，只在指縫露一線銅線。理由：分場表 a04 場 1 要燕迴「看不到紋」（盟堂上他說「衣裡，我也沒看見」），`yuelan-crippled` 寫死了紋翻在外面，設定圖與每一鏡都會把紋畫在燕迴眼前，prompt 寫「掩著」會跟 look 打架。用在 a04 場 1 第 1 點那一格插鏡（a04-s001，右手攏衣）之後拍到他的每一鏡，到登船離岸。已跑 `node header.mjs --ep 7`。（第 2 輪修訂：分場表 a04 場 1 原第 1 點全景與第 2 點插鏡對調——守衛圍上來、燕迴站在最前的全景若還是 crippled，紋就擺在燕迴面前；現在掩衣是 a04-s001，圍住的全景起就是 covered。look 本身沒改，不必重跑 header。）

## 第 4 集跨集連戲修訂（2026-10-06）

- `zhuxu` **新增第二個 look `zhuxu-disarmed`**（基本外觀與 `zhuxu-returned` 一字未改）：外觀照抄 `zhuxu-returned`，只把「a plain straight sword in a dark-green scabbard at his left hip」換成「nothing at his left hip but the dark-green sash」。理由：第 4 集 a05-s016 他把劍連鞘丟在燕迴腳前（第 4 集分場表第七節 a05 第 8 點），`zhuxu-returned` 寫死了左腰的劍，prompt 說劍不在了、設定圖說劍在腰上，跪交秘錄到被押下那二十來鏡腰間會長回一把劍。刻意不寫「no sword」「an empty sword hanger」這類否定句或帶 sword 字眼的句子：生圖模型常反過來把劍畫出來。用在 a05-s017 起凡是列了 `zhuxu` 的鏡頭（21 鏡）；a05-s016 本身首格劍還在腰上，仍用 `zhuxu-returned`。已跑 `node header.mjs --ep 4` 與 `merge.mjs --ep 4`。
- 第 2 集用不到這個 look，但 `ep2/header.json` 與成品 `docs/videos/ou-de-jianghu-e002/video.json`、`series.json` 裡的 `zhuxu` 因此少了一個 `shot_looks` 元素。要讓第 2 集再跟 `cast.json` 逐字相同，照第 6 集的做法對第 2 集跑 `node header.mjs --ep 2` 與 `node merge.mjs --ep 2`（ids.json 會保住 line id），再跑 `cli.mjs script`；由主控決定什麼時候做，本次沒有動第 2 集。

## 第 8 集的改動（2026-10-06）

- 新增 `guideng-jun`（鬼燈君）：幽都三派之一的首領，第 8 集現身、說話、當場被姬無霜斬殺，只活這一集。聲音用 **Azure 的 `zh-TW-YunJheNeural`，`rate: "-8%"`**——全劇第一個不走 Gemini 的角色聲音，理由見下方〈第 8 集的新聲音：鬼燈君為什麼用 Azure〉。Azure 聲音不能帶 `style`（`tools/video/core/schema.mjs` 的 `validateVoice`：「style and model are for Gemini voices only」），所以他是唯一一個沒有「標準國語，咬字清楚，台北人平常說話的語調；……」那段 style 的角色。
- 外觀照 setting 改寫成第 1 集的寫法（「Original 2D anime … in ornate theatrical wuxia costume」，不寫 puppet-theatre），只寫第 8 集登島時的樣子。識別物件寫死：高高的七角黑冠（a tall seven-pointed black crown）、腰間一串七枚小銅鈴（a chain of seven small bronze bells）、灰白的臉、深陷的紫眼、合不太攏的薄唇、垂肩的灰紫長髮、下襬剪成爪尖的長袖。袍的繡紋用第 5 集山脊黑袍人那一句「embroidered with dark-violet seven-star and skull-lantern motifs」：第 5 集姬無霜在盟堂說「那件鬼燈袍，是他自己的」，觀眾要一眼認出是同一款袍。但他本人**不戴兜帽、不戴面具**（「青面具，是鬼燈君貼身死士戴的」，第 5 集 a03-s021）。setting 的「Appears first as a silhouette on the sea of lanterns」不寫進外觀，剪影只寫 prompt（〈連戲提醒〉第 30 條）。setting 的「陰功」寫成出手時袖尖聚起的一點青綠鬼光（照寂聞「when he gathers force a golden aura rises」的寫法）；青綠是收魂陣的顏色（visual_style），陣是他的，顏色也就是他的。**不建斬首後的 look**（第 31 條）。
- `canglan-ke` **新增 look `canglan-spent`**（基本外觀與 voice 一字未改；他原本沒有 `shot_looks`，這次新建陣列）：一掌碎陣、真氣大耗之後的樣子——布冠撞歪、長髮糾結、眼皮沉、風霜色的臉褪成灰白冒汗、袍子胸前撕開、兩臂袖口破爛、肩上與袍襬落滿石窟的灰、毛皮斗篷撕裂滑到左肩下、素劍仍在左腰。理由：企劃包 state「滄瀾客真氣大耗」，他出窟後要在灘頭把傳單紙交給紗女，整個後半都在場；基本外觀寫的是「Stands planted like a man on a ridge in the wind」，不換 look 的話，後半每一鏡他都站得像沒事。刻意不寫血（布袋戲的寫意；嘴角若要一線血，只寫插鏡 prompt）。
- 其他十七人與已有的 look 一字未改。用 node 核對過：第 1–6 集成品 `docs/videos/ou-de-jianghu-e00N/video.json`、`series.json` 與 `ep1–6/header.json` 的角色物件全部與 `cast.json` 逐字相同。第 7 集成品還沒合併（`docs/videos/ou-de-jianghu-e007/` 不存在）；`ep7/header.json` 唯一的差別是 `canglan-ke` 還沒有 `canglan-spent`，舊欄位全同。**第 7 集合併前要先跑一次 `node header.mjs --ep 7`**（還沒畫設定圖、還沒合併，不會作廢任何東西），否則第 7、8 集的 `canglan-ke` 會不一樣；由主控決定什麼時候跑，本次沒有動 `ep7/`。
- `ep8/meta.json`、`ep8/check-act.mjs` 照第 7 集的形狀建好，`node header.mjs --ep 8` 產出十四個角色的表頭；縮圖只填了 `headline`（「千燈收魂」），`shot` 由主控在幕寫完後填。

## 角色總表（19 人）

| id | 名字 | 聲音 | 第 2–5 集 | 第 6 集 | 第 7 集 | 第 8 集 |
| --- | --- | --- | --- | --- | --- | --- |
| bao-sanqian | 包三錢 | Puck | 2、3、4、5 | 6 | 7 | 8（守石窟外） |
| ji-wen | 寂聞「怒目佛」 | Alnilam | 2、3、4、5 | 6（`jiwen-sealed`） | 7（`jiwen-sealed`） | 8（`jiwen-sealed`；梵林寺禪房那一碗藥，可省） |
| ji-wushuang | 姬無霜「霜夫人」 | Gacrux | 2、3、4、5 | 6 | 7（企劃包列了她，地點卻沒有鯨背嶼；主編定，可省） | 8（鯨背嶼室外 `wushuang-armed`；斬首的刀寫 prompt） |
| luo-qingyan | 洛青衍 | Achird | 不出場（第 6 集抵盟） | 6（抵盟，第一次正式出場） | 7（客院旁觀） | 不出場（住盟府客院） |
| nie-gutie | 聶孤鐵「雕匠」 | Algenib | 3 | 不出場 | 不出場 | 不出場 |
| shen-guihe | 沈歸鶴「白鶴先生」 | Iapetus | 2、3、4、5 | 6（分魂前基本外觀；之後 `shen-bedridden`，沒有台詞） | 7（`shen-bedridden`，沒有台詞） | 8（`shen-bedridden`，沒有台詞；只在書齋的切回鏡） |
| xuanmen-elder | 玄門長老 | Schedar | 已死；只在回憶鏡用基本外觀 | 不出場 | 不出場 | 不出場 |
| yan-hui | 燕迴「赤纓」 | Fenrir | 2、3、4、5 | 6 | 7 | 8（守石窟外） |
| yin-wusheng | 殷無聲「啞劍」 | Sadaltager | 2、3（可省）、4、5 | 6（不說話，`yin-cut-hair`） | 7（不說話，`yin-cut-hair`） | 8（不說話，`yin-cut-hair`；倒藥、守石窟外） |
| zhuxu（新） | 竹虛道人 | Umbriel | 2、4 | 不出場（押在玄門） | 不出場（押在玄門） | 不出場（押在玄門） |
| liu-buhuo（新） | 柳不活「求死書生」 | Enceladus | 3、4、5 | 6（`liu-defected`） | 不出場（在島上；企劃包第 7 集沒有他） | 8（`liu-defected`；石窟讓路、塞傳單紙） |
| shuyuan-elder（新） | 書院長老 | Orus | 3、4、5 | 6 | 7 | 8（灘頭代三宗道謝） |
| xuanmen-steward（新） | 玄門執事長老 | Charon | 3、4、5 | 6 | 7 | 8（灘頭；可省） |
| alliance-guard（新） | 客院盟兵 | Sadachbia | 2（不說話）、3（可省，不說話）、5 | 不出場（客院門口的盟兵只寫 prompt） | 不出場（外港的守衛只寫 prompt） | 8（可省：紗女私下押下兩名被收買的盟兵；表頭留著） |
| sha-nu（第 6 集新） | 紗女 | Iapetus（沈歸鶴的聲音） | 不出場 | 6 起 | 7 | 8（灘頭揭局） |
| wuming-jianke（第 6 集新） | 無名劍客 | Iapetus（沈歸鶴的聲音） | 不出場 | 6 起（第 10 集滅） | 7 | 8 |
| canglan-ke（第 7 集新） | 滄瀾客 | Zubenelgenubi | 不出場 | 不出場 | 7 起（第一次正式出場，詩號） | 8（碎陣之後 `canglan-spent`） |
| yuelan-ke（第 7 集新） | 岳嵐客「赤羽」 | Algieba | 不出場 | 不出場 | 7（化名赤羽；外港 `yuelan-crest`→`yuelan-crippled`；第 17 集再現） | 不出場（坐船離港） |
| guideng-jun（第 8 集新） | 鬼燈君 | Azure `zh-TW-YunJheNeural`（`rate: "-8%"`） | 不出場（第 5 集的「鬼燈君黑袍人」是姬無霜，只寫 prompt） | 不出場 | 不出場 | 8（第一次正式出場，詩號；斬首後不再列 id） |

新角色的聲音都沒有跟第 1 集已用的十個聲音（Rasalgethi、Iapetus、Alnilam、Gacrux、Puck、Fenrir、Algenib、Achird、Schedar、Sadaltager）重複，新角色彼此之間也不重複。五個新角色都是男性，從可用男聲裡照年齡挑：中年、乾冷的竹虛用 Umbriel；二十多歲、帶氣音的柳不活用 Enceladus；六十多歲、有分量的書院長老用 Orus；五十多歲、管帳口吻的執事長老用 Charon；二十出頭的盟兵用 Sadachbia。

第 6 集的兩個化身是唯一的例外：`sha-nu` 與 `wuming-jianke` 刻意與 `shen-guihe` 共用 Iapetus（企劃包的鉤子寫死「她的聲音是沈歸鶴的聲音」），只靠 `style` 分：紗女更輕、更慢、更柔，無名劍客更硬、更短、更冷，兩個都不咳。工具允不允許，查證結果在〈兩個化身為什麼用同一個聲音〉。

第 7 集的兩個新角色用掉了最後兩個沒用過的男聲（岳嵐客 Algieba、滄瀾客 Zubenelgenubi），彼此不重複、也不跟前面任何人重複；從第 8 集起新的男角色沒有沒用過的男聲可挑，見〈第 7 集的兩個新聲音〉。

第 8 集的鬼燈君改用 Azure 的 `zh-TW-YunJheNeural`：全劇第一個不走 Gemini 的角色聲音，跟任何人都不重複（Azure 與 Gemini 是兩家供應商的聲音，不會撞名），見〈第 8 集的新聲音：鬼燈君為什麼用 Azure〉。

## 各集出場的角色 id

「入鏡不說話」是已經建了角色、會列進鏡頭 `characters` 的人。群眾、幽都老弱、幽都黑衣人、巡船水手、各宗弟子、第二名客院盟兵都只寫在 prompt 裡，不列 id。

### 第 2 集〈鯨背嶼〉（第 3–6 日）

- 說話：`shen-guihe`、`ji-wen`、`bao-sanqian`、`zhuxu`、`ji-wushuang`、`yan-hui`
- 入鏡不說話：`yin-wusheng`（跟在寂聞身後，只打手勢）；`alliance-guard`（姬無霜在客院向寂聞請命時，他守在月洞門外。先讓觀眾記住這張臉，第 5 集他作證時才認得出來）
- 不出場：`liu-buhuo`、`nie-gutie`、`luo-qingyan`、`shuyuan-elder`、`xuanmen-steward`、`xuanmen-elder`

### 第 3 集〈三十六魂〉（第 8–14 日）

- 說話：`liu-buhuo`、`nie-gutie`、`ji-wushuang`、`shen-guihe`、`ji-wen`、`bao-sanqian`、`yan-hui`、`shuyuan-elder`、`xuanmen-steward`
- 入鏡不說話：`yin-wusheng`（盟堂上站在寂聞身後，可省）；`alliance-guard`（客院門外，可省）
- 不出場：`zhuxu`（還在西行路上）、`luo-qingyan`

### 第 4 集〈裂山秘錄〉（第 15–22 日）

- 說話：`shen-guihe`、`ji-wen`、`bao-sanqian`、`ji-wushuang`、`zhuxu`、`liu-buhuo`、`yan-hui`、`shuyuan-elder`、`xuanmen-steward`
- 入鏡不說話：`yin-wusheng`（冷開場撕下傳單；盟堂上手按劍柄，被沈歸鶴一眼止住）
- 不出場：`nie-gutie`、`luo-qingyan`、`alliance-guard`

### 第 5 集〈封功〉（第 23–26 日）

- 說話：`ji-wen`、`shen-guihe`、`ji-wushuang`、`bao-sanqian`、`yan-hui`、`shuyuan-elder`、`xuanmen-steward`、`alliance-guard`、`liu-buhuo`（在盟堂上站在姬無霜身後，不說話；私下可以說）
- 入鏡不說話：`yin-wusheng`
- 只寫在 prompt、不建角色：山脊上放箭的「鬼燈君黑袍人」（見下方〈連戲提醒〉第 2 條）
- 不出場：`zhuxu`（被玄門收押待審）、`nie-gutie`、`luo-qingyan`

### 第 6 集〈紗女〉（第 27–34 日）

- 說話：`shen-guihe`（**只在分魂之前**：冷開場倒下、被扶上榻、對包三錢與殷無聲交代、分魂那一刻；分魂之後本體昏臥，全集不再有一句台詞——企劃包寫「寂聞與沈歸鶴本體再無法對話」）、`sha-nu`、`wuming-jianke`、`bao-sanqian`、`ji-wen`、`ji-wushuang`、`luo-qingyan`、`liu-buhuo`、`yan-hui`、`shuyuan-elder`、`xuanmen-steward`
- 入鏡不說話：`yin-wusheng`（`yin-cut-hair`；把寂聞抬到書齋外，之後守在書齋或禪房外）
- 只寫在 prompt、不建角色：姬無霜的侍女（見下方〈沒有建的角色〉）、扶瀾國使船的隨員與水手、客院門口的盟兵、幽都舊部、梵林僧人
- 不出場：`zhuxu`（押在玄門）、`nie-gutie`、`xuanmen-elder`、`alliance-guard`（第 5 集結束時兩名盟兵已回盟兵房；本集客院住的是洛青衍，門口若要有人只寫 prompt。主編若要他入鏡，把 id 加進 `ep6/meta.json` 的 `cast`，再跑 `node header.mjs --ep 6`）
- 詩號：洛青衍第 1 集只在船上入鏡、沒有詩號字卡，本集抵盟是他第一次正式出場，照 setting 的規則可以給他詩號（已有詩號的是姬無霜、寂聞、沈歸鶴、竹虛、柳不活、聶孤鐵）。紗女與無名劍客是化身，**不用詩號**（narrative_constraints：「配角與化身不用」）。

### 第 7 集〈西嶺來客〉（第 35–41 日）

- 說話：`canglan-ke`、`yuelan-ke`、`ji-wen`、`sha-nu`、`wuming-jianke`、`bao-sanqian`、`yan-hui`、`luo-qingyan`、`shuyuan-elder`、`xuanmen-steward`。`ji-wushuang`：企劃包第 7 集的 characters 有她，但四個地點——西嶺雪線、盟府客院、盟府外港、梵林寺禪房——都不在鯨背嶼。**主編定：不入鏡、沒有台詞，表頭留著**（`ep7/meta.json` 的 `cast` 仍列她；分場表第 6 行與第十一節）；任何一鏡的 `characters` 都不列她。
- 入鏡不說話：`shen-guihe`（`shen-bedridden`，全集沒有台詞，到第 12 集合魂前都沒有；化身受創那一刻本體咳血，血只寫插鏡 prompt）、`yin-wusheng`（`yin-cut-hair`；禪房門口持劍橫在門口不讓任何人進、端湯藥、懸念那一鏡）
- 只寫在 prompt、不建角色：赤羽的藥童、燕迴帶到外港的盟府守衛、赤羽登的船與水手、梵林僧人、客院門口的盟兵（見下方〈沒有建的角色〉）
- 不出場：`zhuxu`（押在玄門）、`nie-gutie`、`xuanmen-elder`、`alliance-guard`（外港的守衛是 prompt 裡的另一群人）、`liu-buhuo`（在鯨背嶼管帳；企劃包第 7 集的 characters 沒有他。主編若拍島上的姬無霜，他多半在她旁邊——要他入鏡就把 id 加進 `cast` 再跑 `header.mjs`）
- 詩號：**滄瀾客**是企劃包的主要人物、本集第一次正式出場，給（建議放在他走進梵林寺禪房、寂聞認出他的那一刻；嶺口擦肩的冷開場不給——冷開場 ≤ 20 秒）。**岳嵐客**也是主要人物，但他化名赤羽入盟，入盟時給詩號等於開場揭底；建議放在外港揭穿那一刻的定格上（第一劍劃開紅衣、雙淵紋露出，visual_style：「重要一擊在定格上疊詩號」），字卡 `title` 寫「岳嵐客」、`tag` 寫「赤淵宮大宮主」——那也是觀眾第一次聽到他的名字。紗女與無名劍客是化身，不用。已有詩號的七位（姬無霜、寂聞、沈歸鶴、竹虛、柳不活、聶孤鐵、洛青衍）不再給。
- 三宗高層：細綱 consequence「三宗高層得知寂聞可解封，開始催促」「三宗仍視赤羽為被襲的貴客」「無名劍客被盟內記了一筆無故傷客」——照第 3–5 集的做法，這些話要由書院長老或執事長老親口說（旁白代說沒有分量），所以兩人在 `cast` 裡。

### 第 8 集〈鬼燈〉（第 42–45 日）

企劃包第 8 集的 characters 是十一人（沈歸鶴、寂聞、殷無聲、包三錢、姬無霜、柳不活、滄瀾客、鬼燈君、紗女、無名劍客、燕迴），四個地點都在鯨背嶼（外海、島底石窟、灘頭、主帳）。`ep8/meta.json` 的 `cast` 另外加了書院長老、執事長老（懸念「三宗長老在灘上向她作揖道謝」）與客院盟兵（state.evidence「紗女揭出並私下押下的兩名被收買的客院盟兵」），共十四人。表頭裡沒入鏡的角色 lint 不檢查；分場表定案時用不到的人，從 `cast` 拿掉再跑 `node header.mjs --ep 8` 即可。

- 說話：`guideng-jun`、`sha-nu`、`wuming-jianke`、`ji-wushuang`、`canglan-ke`、`liu-buhuo`、`bao-sanqian`、`yan-hui`、`shuyuan-elder`。
  - 鬼燈君：登島當眾指控姬無霜、被拆穿後翻臉，見下方〈鬼燈君〉。
  - 柳不活：石窟混戰中讓開一線、把靴底那張傳單紙塞進滄瀾客掌心是他的戲；可以一句不說，要說也只在姬無霜聽不到的地方（他的讓路沒被她看見、卻被鬼燈君的細作看見——企劃包前半 consequence）。
  - 書院長老：三宗在灘上向姬無霜作揖道謝那一句由他說；紗女拆穿之前「三宗以為陣是她的、當場要殺她」（後半 stakes）的那一句也要由長老說，照第 3–5 集，旁白代說沒有分量。
- 說話或只入鏡（主編定，表頭都留著）：
  - `xuanmen-steward`：灘頭附和長老；可省。
  - `ji-wen`（`jiwen-sealed`）：第 7 集停在殷無聲端著浮紅的湯藥、寂聞說「……藥。」，第 8 集要先交代這一碗沒有喝（殷無聲沒有餵，從這一夜起每一碗都倒在井邊，m06）。這一場若拍，寂聞可以有一兩句，也可以不說話；不拍就由殷無聲倒藥的一鏡（只拍手、碗與井口，`characters: []`）帶過。
  - `alliance-guard`：企劃包 consequence 寫紗女回盟後查出第 5 集那夜監看客院的兩名盟兵收了幽都的金、姬無霜根本不在客院，私下押下兩人，沒有當眾說。若分場拍這一場，開口的是他（第 5 集作證的就是他，觀眾認得這張臉），第二名照第 5 集只寫 prompt（年紀較大、留鬍子）；要拍被押、槍被收走的樣子，先看下方 shot_looks 表那一列。若不拍，這件事留給第 9 集回頭交代，`cast` 拿掉他。
- 入鏡不說話：`yin-wusheng`（`yin-cut-hair`；禪房倒藥，之後與燕迴、包三錢守在石窟外）、`shen-guihe`（`shen-bedridden`；本體在盟府書齋，本集的地點都在鯨背嶼，他只出現在書齋的切回鏡；沒有台詞，到第 12 集合魂前都沒有）。
- 只寫在 prompt、不建角色：鬼燈君的貼身死士與幽都精兵、鬼燈君安在舊部營裡的細作、幽都舊部、灘上甦醒的孩童與老弱、第二名被收買的盟兵、千盞青燈（見下方〈沒有建的角色〉與〈連戲提醒〉第 30–41 條）。
- 不出場：`luo-qingyan`（住盟府客院；企劃包第 8 集沒有他）、`zhuxu`（押在玄門）、`nie-gutie`、`xuanmen-elder`、`yuelan-ke`（第 7 集坐船離港，第 17 集再現）。
- 詩號：**鬼燈君**是 setting 的主要人物（「第一季表面的反派」），本集第一次正式出場，給。建議放在他親率幽都精兵登上灘頭、第一次在亮處露臉的定格上；海面千燈上的剪影不給（還看不到臉；冷開場也 ≤ 20 秒）。字卡 `title` 寫「鬼燈君」。只活一集的人有了詩號，姬無霜那一刀才有分量。已有詩號的不再給（第 1–6 集七位，第 7 集的滄瀾客與岳嵐客）；紗女與無名劍客是化身，不用。

## 新角色為什麼要說話

### 竹虛道人 `zhuxu`（第 2、4 集）

竹虛是企劃包的主要人物（第 2、4 集的 characters 裡都有他），他的台詞沒有人能代說：

- 第 2 集後半的高張力：他在三宗盟後山認出沈歸鶴咳出的血裡有鐵屑，把血帕塞進自己懷裡，對寂聞說「只是夜露」。這是他替沈歸鶴說的第一個謊，非他本人開口不可。
- 第 4 集後半：他在齊雲殿外被圍，不還手，走上殿階跪交《裂山秘錄》。

外觀照 setting 改寫成第 2 集的樣子。背上的布包寫成中性的「a cloth-wrapped bundle on his back」，不交代裡面是什麼。另外加了一柄收在鞘裡的劍：他是「Taoist swordsman」，招式是裂山訣劍法。不寫死的話，生圖模型會時有時無地自己補劍。寫死之後，第 4 集的「不還手」也有了畫面：手不碰劍。第 4 集最後交出劍：殿前廣場他解下劍、連鞘丟在燕迴腳前，從下一鏡起換成左腰沒有劍的 `zhuxu-disarmed`。

### 柳不活 `liu-buhuo`（第 3、4、5 集）

柳不活也是企劃包的主要人物，第 3 集起是推動劇情的人：

- 第 3 集前半：在荒原鐵廬逼聶孤鐵說出箭的規矩（「三十六個人裡本該有我……你欠的我也欠」），推算出印只差一道。
- 第 3 集懸念：折斷押解牌，說「我去做她的人」。
- 第 4 集：在姬無霜帳中看見同一疊傳單紙。
- 第 5 集：他是唯一知道箭是誰射的人。

酒葫蘆照指示寫進了基本外觀。

### 書院長老 `shuyuan-elder`（第 3、4、5 集）

第 1 集的盟堂只有三人：沈歸鶴代表書院、寂聞代表梵林、玄門長老代表玄門。第 3 集起，企劃包要的是「三宗長老」這個比沈歸鶴高一層的聲音：

- 第 3 集後半：姬無霜在盟堂請命，劇情要「三宗長老動容」、「三宗准她領兵」，而寂聞沉默未反對。准她的話沈歸鶴不會說，寂聞也不會說，旁白代說又沒有分量，所以要有一位長老親口准奏。
- 第 4 集前半：劇情是「三宗長老攤開通緝令要沈歸鶴蓋印」。逼他蓋印的必須是書院自己人，觀眾才看得出沈歸鶴連自己出身的書院都站不住；這之後三宗高層「開始繞過沈歸鶴議事」。
- 第 5 集後半：三宗長老一致准奏讓姬無霜接掌鯨背嶼防務，沈歸鶴唯一的反對票被壓過。這時三宗高層已經知道玄門長老的死訊，把寂聞中的這一箭叫成「第二支」，這句誤判要由長老說出口。

名字照「玄門長老」的格式取。要注意：第 1 集提過、跪盟前半月死在路上的那一位，台詞裡要說成「書院那位閉關的長老」（第 1 集原話），不要只說「書院長老」，否則會跟這個角色的字幕名撞在一起。

### 玄門執事長老 `xuanmen-steward`（第 3、4、5 集）

- 第 4 集：《裂山秘錄》是玄門的鎮派之典，通緝令由玄門提出。企劃包寫明竹虛把秘錄交給「玄門代掌事的執事長老」，由他翻開，一頁一頁都無字；本集的懸念就落在他翻書的手和那一聲「無字」。之後「竹虛受審時三宗高層都知道長老已死」，揭開閉關之謊的也是玄門自己的人。
- 第 3、5 集：玄門長老「閉關」（其實已死）後，盟堂上玄門的位子由他代坐，跟書院長老一起附議准奏。

他是不會武功的管事，跟第 1 集的玄門長老在外觀上刻意分開：戴布冠不戴玉冠，留稀疏灰鬚而不是長白鬚，不拿拂塵，腰間掛銅鑰匙串和帳冊。

### 客院盟兵 `alliance-guard`（第 5 集說話；第 2、3 集只入鏡）

第 5 集的轉折是「監看客院的兩名盟兵咬定姬無霜整夜未出房門」，盟內因此認定箭在鬼燈君手上。姬無霜的不在場證明只有這一個來源，必須由證人當著長老親口說出。要是改由燕迴或沈歸鶴轉述，「被買通的證人」這一層就沒了，柳不活知情、沈歸鶴半信半疑的戲也落不了地。兩名盟兵只建一個角色：說話的是他，第二名是只寫在 prompt 裡的臨時演員（建議寫成年紀較大、留鬍子，跟他分得開），只點頭附和，不列 id。他的外觀照第 1 集 a03-s040、a03-s082 的「alliance guards in white-and-gold uniforms holding spears」設計。

第 8 集（可省）：企劃包寫紗女回盟後查出這兩人收了幽都的金、姬無霜那夜根本不在客院，私下押下兩人，沒有當眾說。若分場拍這一場，認罪的話要由他自己說出口：第 5 集他當著長老咬定的那一句，觀眾要聽見同一個嗓子把它收回去，旁白代說就沒有這一層。第二名仍只寫 prompt。他被押下、槍被收走的樣子要先加 look（見 shot_looks 表第 8 集那一列）。

### 紗女 `sha-nu`（第 6 集起；第 12 集合魂後不再出現）

紗女是第 6 集的集名角色，也是沈歸鶴分魂之後他在盟內的嘴：

- 冷開場的鉤子：「床前站著一名蒙著白紗的女子，她的聲音是沈歸鶴的聲音」——這句鉤子要成立，她非開口不可，而且開口的一瞬觀眾要聽出是沈歸鶴。所以她的聲音就是沈歸鶴的 Iapetus。
- 後半高張力：盟堂上她代沈歸鶴接扶瀾國書；三宗只知道她是沈歸鶴的「代行」，這個身分要由她自己在長老面前說圓。
- 第 7 集她替昏病的本體拒掉赤羽的藥，第 8 集她在鯨背嶼灘上揭鬼燈君的局，都是她自己的戲。

外觀照 setting 改寫成第 1 集的寫法：識別物件是低低的半透明白紗冠（遮住上半張臉，只露嘴與下巴），月白與灰紗的層疊長袍、拖地長袖、赤足；不帶任何東西。setting 的「影子比常人淡一分」不寫進外觀，只寫在 prompt（見〈連戲提醒〉第 12 條）。

### 無名劍客 `wuming-jianke`（第 6 集起；第 10 集滅）

無名劍客是沈歸鶴分魂之後他在江湖上的手：

- 分魂那一場，他與紗女同時自沈歸鶴身側立起；寂聞在書齋外怒斥「你拿命去圓謊」時，能回話的是這兩個化身，不是昏迷的本體。
- 他的台詞少而硬（setting：帶走沈歸鶴的剛直與劍）。第 7 集他攔下赤羽的毒藥、逼出赤羽真身，是整集的武戲主角。

外觀照 setting 改寫：識別物件是素白鐵冠與遮住眼鼻、只露嘴與下巴的無紋白半面具；黑白兩色、完全沒有繡紋的層疊長袍；一柄白柄直劍收在黑鞘裡佩在左腰。髮寫成與沈歸鶴一樣的「very long straight ink-black hair」，只是嚴嚴束起，給認得出的人一個線索。「影子比常人淡」同樣只寫 prompt。

### 兩個化身為什麼用同一個聲音

企劃包的鉤子寫死「她的聲音是沈歸鶴的聲音」，setting 也說兩個化身各帶走他一半的元神；所以 `sha-nu` 與 `wuming-jianke` 的 `voice` 都是沈歸鶴的 `gemini:Iapetus`，只有 `style` 不同：紗女比沈歸鶴更輕、更慢、更柔；無名劍客更硬、更短、更冷；兩個都「不咳」（咳是本體的傷）。

有沒有規定兩個角色不能共用一個聲音？2026-10-05 查過工具：

- `tools/video/core/schema.mjs` 的 `validateVoice` 只檢查 provider（azure／gemini）、聲音名字的格式、`style` ≤ 400 字；`tools/video/core/drama.mjs` 的 `validateCharacters` 只擋重複的 id；`tools/video/core/lint.mjs` 與 `state.mjs` 只要求每集的角色物件與 `series.json` 逐字相同。**沒有任何一條擋兩個角色同一個聲音**，成品 lint 會過。
- 唯一會擋的是 `tools/video/production/design.mjs` 的 `designProblems`（「production actors need distinguishable voice selections」），那是「製作設計書」那條流程（`node tools/video/production/cli.mjs`）的檢查；這部戲沒有製作設計書（企劃包目錄裡沒有 production design 檔），第 1–5 集也沒走那條流程。將來若要走，無名劍客改用還沒用過、最接近 Iapetus 的男聲 **Algieba**（Iapetus 是清亮的男聲；可用男聲裡只剩 Algieba 與 Zubenelgenubi 沒用過，Algieba 較平、較順），紗女仍用 Iapetus；改聲音只動 `cast.json` 的 `voice.name`，不動已錄的集數。
- setting 的 narrative_constraints 寫「每個角色固定一個聲音」，是一個角色不能換聲音，不是兩個角色不能同聲。
- 2026-10-05 第 7 集補記：上面「無名劍客改用 Algieba」的備案不再成立——Algieba 已給了岳嵐客（見〈第 7 集的兩個新聲音〉）。若真要走製作設計書那條流程，要換聲音的那個化身得照第 7 集那節的重用規則另挑。第 7 集又查了一次 `tools/video/core/state.mjs`：裡面關於 voice 的只有 `dubSpeechCurrent`（配音是否過期）那一段，沒有「兩個角色不能同聲」的檢查；成品 lint 對 Iapetus 一聲三用照樣過。

### 滄瀾客 `canglan-ke`（第 7 集起；第 12 集後不告而別，第 20 集再現）

滄瀾客是企劃包的主要人物（第 7、8、10、11、12、20 集的 characters 裡都有他），他第 7 集的戲沒有人能代說：

- 前半高張力：禪房裡他對寂聞說出寒潭引血之法——至交以自己的血引潭水、引血者折壽——「自己已帶來引血的刀」；寂聞以封功之身一掌推開他，「我不用你的壽來買我的功」是對他說的。折壽的條件由要折壽的人自己說出口（narrative_constraints：規則先由正在發生的事與付出的代價呈現，再補當集必要的一句），旁白代說就沒有代價了。
- consequence：他留在梵林寺不走。「三宗高層得知寂聞可解封」不是他去說的——他只對寂聞開口；怎麼傳到三宗（梵林僧人、執事來探）由主編定，他不對長老解釋。
- 第 8 集硬闖島底破陣、第 10 集接劍、第 11 集引血，都是他的戲。

外觀照 setting 改寫成第 7 集下山時的樣子：鐵灰長髮、素色深藍布冠、鼻樑一道細長舊疤、深藍與風暴灰的層疊袍、繡浪紋的袍襬、深灰毛皮斗篷、左腰一柄收在舊鞘裡的素劍。不寫「後來換成無愧劍」、不寫「第 11 集後髮全白、拄杖」（到第 11 集另加 look）。引血的刀只寫 prompt（禪房那場從懷裡拿出來放在寂聞面前），不寫進外觀；setting 的羈絆物件「滄瀾客的血與寒潭」本集只讓刀出現，不見血。

### 岳嵐客（化名「赤羽」）`yuelan-ke`（第 7 集；第 17、21、24 集再現）

岳嵐客是 setting 說的「第一期最深的一盤棋」。第 7 集他以大夫「赤羽」的身分把火脊丹送到書齋，要說服紗女與包三錢給昏病的本體服下——這場的張力全在他的客氣，藥童代說不了；外港被無名劍客追上、紅衣劃開、廢臂，他不喊不叫，揭穿後的話照分場表（`ep7/beats.md` a03 場 4 與 a04 場 1：自報名號、「三宗，不會知道」、「……好劍」、對燕迴演成受害的客人），之後登船而去。第 17 集默許白蘅入爐、第 24 集收下衛千籌，都是這個聲音。

- `name` 寫「岳嵐客「赤羽」」，照 `燕迴「赤纓」` 的格式。字幕沒有 speaker 前綴（`ep1/header.base.json` 的 `subtitles` 沒開 `speaker_prefix`），觀眾看不到名字；只有 `script.md` 的審稿人與設定圖 prompt 讀得到。台詞裡他自稱「赤羽」「在下」，揭穿之前沒有人叫他岳嵐客。
- 外觀：基本外觀是第 7 集化名赤羽的樣子（setting：「As 'Red Feather' in episode 7 he wears a plain russet healer's robe and a half-veil」）：暗赤紅素袍、沒有繡紋、沒有冠、暗紅長髮束成素髻插一根銅簪、遮住口鼻的赤褐紗巾（只露眼與眉）、右肩掛一只黑漆藥箱。setting 的真身（紅銅折翼冠、赤銅繡羽袍）是他在赤淵宮時的樣子，第 7 集不出現，第 17 集再加 look；「左臂廢後藏在長袖裡」也是第 7 集以後的事，到時一起加。
- 三個 look：`yuelan-crest`（第一劍之後：紗巾掉到頸上、臉全露、紅衣從左肩劃開到胸口、內裡的雙淵紋露出、兩臂都好、沒有藥箱）、`yuelan-crippled`（第二劍之後：再加左臂垂著、左袖血濕）、`yuelan-covered`（2026-10-06 新增：同 crippled，但右手把劃開的衣襟攏在胸前、紋看不見，只在指縫露一線銅線；燕迴圍住劍客之後到登船離岸）。雙淵紋的固定寫法是「the twin-abyss crest of the Red Abyss Palace, two dark whirlpools side by side in bronze thread」，第 12、17、21 集赤淵宮的人與物照這句寫。

### 第 7 集的兩個新聲音

- 到第 6 集為止，十六個男聲裡只剩 **Algieba** 與 **Zubenelgenubi** 沒用過（可用聲音照 `tools/video/production/design.mjs` 的 `PRODUCTION_VOICES`，男女之分照 `docs/videos/series-plans/binge-five-20260928/DECISIONS-20260929.md` 第 13 行）。兩個新角色都是男性，剛好一人一個：**岳嵐客用 Algieba**（平穩、溫和、有磁性、永遠不急——大夫在病榻前的嗓子，也是「比衛千籌更會等」的人的嗓子；別部戲對這個聲音的寫法是「禮貌的壓力勝於嘶喊」，就是他）；**滄瀾客用 Zubenelgenubi**（低、乾、隨便，什麼都不要的山上人）。兩個都沒跟任何人重複。
- **第 8 集起沒有沒用過的男聲了。** 鬼燈君（第 8 集現身、說話、當場被斬）就要一個男聲；第二季的冷玉衡、衛千籌、酆赤髓、褚無常、白蘅也都要。第 8 集的角色表主控要先請站主定重用規則：(a) 重用已經不再說話的角色的聲音——玄門長老的 Schedar（第 1 集死，之後只在回憶鏡）最先空出來，柳不活第 9 集死後 Enceladus、聶孤鐵第 10 集後 Algenib 也會空——但 narrative_constraints 寫死者以記憶與他人的台詞出現，回憶鏡可能還要原聲；(b) 用 Gemini 的 `voice_…` 自訂聲音 id（schema 的 `GEMINI_VOICE` 允許）；(c) 像化身那樣刻意同聲。鬼燈君只活一集、台詞少，用 (a) 的 Schedar 最省。
- 紗女與無名劍客仍用沈歸鶴的 Iapetus（上一節），第 7 集不改。

### 鬼燈君 `guideng-jun`（只在第 8 集）

鬼燈君是 setting 的主要人物、第一季表面的反派，只活這一集。他的話沒有人能代說：

- 轉折：滄瀾客破陣之後，他親率幽都精兵登島，**當眾**說收魂陣是姬無霜拿三宗的符嫁禍三宗的局。這句指控要由他本人在三宗長老面前說出口：三宗一信，就要當場殺她（後半 stakes）。旁白代說只是解說，紗女的拆穿也就沒有對手。
- 後半高張力：紗女攤開包三錢的拓片與柳不活靴底的傳單紙，指出陣符與通緝傳單出自他安在舊部營裡的細作之手，他翻臉動手。被拆穿之後的一兩句與那一下出手，是姬無霜那一刀的理由。
- 他要的是三宗殺姬無霜，他好以「為幽皇之女復仇」收服幽都三派。這一層由紗女點破，不由他自白：被拆穿的人不會替拆穿他的人把話說完。
- 他**不是**鑄箭當日奪箭的黑風（setting：「他拿不到箭，所以他不是奪箭的黑風」），第 5 集的箭也不是他放的（是姬無霜借他的名）。他的台詞不認箭，也不能寫成知道箭在誰手上。他的符印從哪裡流出去，第一期沒有證實（setting 的 ending），他的台詞也不交代。
- 台詞少而慢。Azure 聲音不吃逐句的 `emotion`（lint 會警告「emotion … is ignored: the azure voice has no style prompt」，見 `tools/video/core/drama.mjs` 的 `emotionProblems`），他的語氣只能靠字句本身（短句、頓點、刪節號）加上 `rate: "-8%"` 的慢。**他的台詞不要加 `emotion`**；其他角色照舊。cue 覆蓋率的檢查（`cueCoverageProblems`）本來就不算 Azure 的句子，不會因為他沒有 cue 而警告。
- `name` 只寫「鬼燈君」，沒有別號；字幕沒有 speaker 前綴，觀眾看不到名字，台詞裡要有人叫出這三個字（第 1、3、5 集已經叫過很多次了）。

### 第 8 集的新聲音：鬼燈君為什麼用 Azure

- 十六個 Gemini 男聲（`docs/videos/series-plans/binge-five-20260928/DECISIONS-20260929.md` 第 13 行）到第 7 集已全部有主：旁白 Rasalgethi、沈歸鶴與兩個化身 Iapetus、寂聞 Alnilam、包三錢 Puck、燕迴 Fenrir、聶孤鐵 Algenib、洛青衍 Achird、玄門長老 Schedar、殷無聲 Sadaltager、竹虛 Umbriel、柳不活 Enceladus、書院長老 Orus、執事 Charon、盟兵 Sadachbia、滄瀾客 Zubenelgenubi、岳嵐客 Algieba。十六人之後都還會出場（玄門長老在回憶鏡）；除了玄門長老與天生不能說話的殷無聲（見下方備案），每一位之後都還會開口：柳不活第 9 集、聶孤鐵第 10 集才死，竹虛第 12 集回來，岳嵐客第 17 集再現，盟兵本集可能還要開口。
- 第 7 集那一節列的三條路都不合用：(a) 借不再說話的角色的聲音——最先空出來的是玄門長老的 Schedar，但**不能借**：他的死是第一季的懸疑主線（第 1 集精元被抽走、無傷無血；第 3–5 集閉關之謊；第 4 集受審揭開死訊；第 5 集三宗把射寂聞的箭叫成「第二支」），他的聲音觀眾第 1 集聽過，回憶鏡也可能還要原聲。鬼燈君一開口是長老的嗓子，觀眾會以為長老回來了，或以為兩人有關係，等於在懸疑主線上放一條假線索。(b) Gemini 的 `voice_…` 自訂聲音 id：沒有現成的。(c) 刻意同聲：只有化身那樣「本來就是同一個人」的設定撐得住；鬼燈君跟誰同聲，都會被當成線索。
- 所以改走第二家：Azure 的台灣男聲 `zh-TW-YunJheNeural`。`tools/video/tts` 支援個別角色用 Azure 聲音（`tools/video/tts/tts.test.mjs`：同一部戲旁白用 Gemini、某個角色用 Azure），兩家的聲音名字不會撞，他跟任何人都不重複。Azure 的台灣口音男聲只有這一個（`zh-TW-HsiaoChenNeural`、`zh-TW-HsiaoYuNeural` 是女聲）；預設清單裡另有兩個多語男聲（`en-US-AndrewMultilingualNeural`、`en-US-BrianMultilingualNeural`，會改講台灣國語，口音要先試聽）。之後第二季的新男角（冷玉衡、衛千籌、酆赤髓、褚無常）到時要另議，不能再假設有空的聲音。
- 備案（本次沒用，記下來給主控與站主）：殷無聲的 Sadaltager 從來沒出過聲——他天生不能說話（setting 的 limits），角色檔裡的聲音「只為角色檔完整而設」，觀眾沒聽過。把 Sadaltager 給鬼燈君，台詞還能吃 style 與 `emotion`、音色也跟其他人一致；代價是 `cast.json` 裡有兩個角色同一個聲音物件名（lint 不擋，見〈兩個化身為什麼用同一個聲音〉），而且如果第一期有哪一場要殷無聲出聲（夢、心聲、回憶），就得另想辦法。要改，只動 `guideng-jun` 的 `voice`（改成 `{"provider":"gemini","name":"Sadaltager","style":"標準國語，咬字清楚，台北人平常說話的語調；……"}`），再跑 `node header.mjs --ep 8`。
- 代價：
  1. Azure 沒有 style：不能寫「陰、慢、冷」這種表演指示，也不吃逐句的 `emotion`（lint 只警告、不擋）；能調的只有 `rate`。給 `-8%`：比常速慢一點，聽起來不急不躁，又不會慢到拖垮本集的時段帳。lint 估算時長不看 `rate`，實際會比估算略長；tts 之後先用 `tools/video/qa/pace.mjs` 量。
  2. 音色跟 Gemini 那一群不同、機器感較重。對一個只活一集、從海上燈潮裡走出來的反派不算壞事，但 tts 之後主編要聽一次；太出戲就把他的台詞再砍短。
  3. **TTS 前要請站主確認**後台「API 與供應商設定 → Azure 語音（影片旁白）」已填金鑰與區域，而且「允許的聲音」裡有 `zh-TW-YunJheNeural`。伺服器的預設清單（`apps/api/app/config.py` 的 `azure_speech_voices`）本來就有它，但後台存過自己的清單就以後台為準。不在清單裡，`tts` 會在送出任何一句之前停下，點名「spoken by guideng-jun (鬼燈君)」（`tts.test.mjs`）。有影片工具權杖時，`node tools/video/cli.mjs tts --slug ou-de-jianghu-e008 --dry-run` 會印出「voice zh-TW-YunJheNeural ready」或「NOT ready」與原因。Azure 有自己的每月計費字元上限（預設 450,000，一個中文字算兩個）；鬼燈君一集的台詞量碰不到。
- 2026-10-06 又查了一次「兩個角色能不能同聲」：`tools/video/core/state.mjs` 裡關於 voice 的仍只有 `dubSpeechCurrent`（配音是否過期）；`schema.mjs` 的 `validateVoice` 只查單一聲音物件（provider、名字格式、Azure 不能有 style／model、Gemini 不能有 rate、`rate` 要像「-8%」）；`lint.mjs` 只要求每集的角色物件（含 `voice`）與 `series.json` 逐字相同。唯一會擋同聲的仍是 `tools/video/production/design.mjs` 的 `designProblems`（製作設計書那條流程，這部戲沒走）。鬼燈君沒跟任何人同聲，這一條本來就碰不到。

### 沒有建的角色

- 姬無霜的侍女（第 6 集）：企劃包的轉折寫她在鯨背嶼向柳不活打聽「扶瀾國的船什麼時候到」。不建角色、不配聲音：她只在 prompt 裡（建議寫成幽都舊部的年輕侍女，黑衣、無冠，跟姬無霜分得開），走到柳不活身邊低聲說了一句，**那句話由柳不活重複出來**（「扶瀾國的船？」），或由旁白接一句。要是主編覺得非她本人說不可，就得在 `cast.json` 建角色、配一個沒用過的女聲，再跑 `header.mjs`。
- 扶瀾國使船的隨員與水手（第 6 集）：跟在洛青衍身後的隨員只寫 prompt，不說話；國書由洛青衍自己捧上。
- 第 6 集客院門口的盟兵：只寫 prompt（見上方第 6 集的出場名單）。
- 鬼燈君：第 2–5 集不出場（第 8 集才現身）。
- 第 5 集的「鬼燈君黑袍人」：其實是姬無霜，只寫在 prompt。
- 幽都黑衣人、巡船水手、鯨背嶼老婦與昏睡的孩子、各宗弟子、梵林僧人：都不說話。第 2 集冷開場跪在灘頭的老婦用畫面加旁白交代。孩童昏睡的消息由燕迴（巡船）帶回。「竹虛去玄門分院奔喪」這個說法由沈歸鶴或旁白說。第 4 集傳單上的字由燕迴或包三錢念出（殷無聲不能念）。
- 梵林長老：第 5 集盟堂上，梵林的位子是寂聞的空位，劇情要的就是這張空椅子，所以不補人。
- 赤羽的藥童（第 7 集）：不建角色、不說話。prompt 固定寫「a boy of twelve in a plain russet-brown tunic, hair in two small knots, carrying a small cloth-wrapped bundle」（跟在赤羽身後；藥箱在赤羽肩上，不在他手上）。客院被劍客截下時他只發抖，劍客挑開的丹藥是從他的布包裡拿的；懸念丟空瓶那一鏡只拍一隻小手、瓶子與井口（`characters: []`）。他不能說話的另一個理由：沒有男聲可配。
- 燕迴帶到外港的盟府守衛（第 7 集）：prompt 照第 1 集「alliance guards in white-and-gold uniforms holding spears」，不是 `alliance-guard`；他們圍住劍客、認出赤羽是貴客，台詞由燕迴說。
- 赤羽登的船與水手（第 7 集）：prompt；船寫成一艘無旗的褐帆商船（a two-masted southern merchant junk with patched ochre-brown matting sails, flying no flag），不寫赤淵宮的紋。**不用灰帆**（2026-10-06 改）：第 5 集的三宗運船、第 6 集姬無霜回鯨背嶼的小船都是灰帆，同一個碼頭再出現灰帆，觀眾會把赤羽跟鯨背嶼連在一起。
- 梵林僧人、客院門口的盟兵（第 7 集）：照第 5、6 集，只寫 prompt。
- 西嶺已逝的第三位隱士：不出場、不提名字。
- 鬼燈君的貼身死士與幽都精兵（第 8 集）：prompt。貼身死士照第 5 集姬無霜的話戴青面具，寫「black-clad guards each with a blue-green mask covering the whole face」；精兵寫成黑衣、無冠、持長刀的一群。伏地稱主那一鏡是群眾，不列 id。他們不說話（沒有男聲可配）；喊聲只用畫面，或由旁白帶。
- 鬼燈君安在幽都舊部營裡的細作（第 8 集）：prompt。前半他看見柳不活讓路，後半被紗女指出陣符與傳單是他的筆。**不建角色、不說話**：Gemini 男聲沒有空的，Azure 的台灣男聲只有一個、已經給了鬼燈君。他被指出時的反應只用畫面（例如退半步、被舊部按住），話由紗女、鬼燈君或姬無霜說。他要跟柳不活分得開：柳不活是灰與褪色靛藍的書生袍、灰色書生帽；細作寫成幽都舊部的素黑衣、無冠，**不戴青面具**（戴了就成了鬼燈君的死士，一眼揭底）。分場表第九節要定他的一句固定英文，每一鏡照抄，觀眾才認得前半看見讓路的就是後半被指出的這一個。
- 第二名被收買的客院盟兵（第 8 集）：照第 5 集，prompt（年紀較大、留鬍子），只點頭、不說話。
- 灘上甦醒的孩童與老弱、幽都舊部、幽都黑衣人（第 8 集）：prompt，不說話；孩子一個接一個睜眼用畫面交代，照第 2 集的做法。

## shot_looks 用在哪裡

| 角色 | look id | 集 | 從哪一段起、到哪一段止 |
| --- | --- | --- | --- |
| bao-sanqian | `bao-soaked` | 2 | 前半：跳海後被燕迴的巡船撈起，濕透、裹著毯子，手裡捏著泡濕的拓片，一直到他上岸回盟府。 |
| bao-sanqian | `bao-chilled` | 2 | 後半：落海受寒、臥床三日（第 3–6 日）的戲，包括懸念那場把拓片攤在沈歸鶴案上（身上裹著被子去）。第 3 集起回基本外觀。 |
| nie-gutie | `nie-nail-wound` | 3 | 他在第 3 集的每一鏡都用這個（冷開場把手釘在砧上、擲釘、說出箭的規矩、砸碎鐵砧）。釘子本身、手被釘在砧上、拿鐵鎚砸砧，都寫在 prompt。這個 look 不拿鍛鉗。 |
| liu-buhuo | `liu-wounded` | 3 | 前半：鐵釘穿過左肩之後，從鐵廬到回盟、在盟堂看見姬無霜的手背，都用這個。押解牌還掛在腰上，折牌的那一鏡也用它（牌在手上）。 |
| liu-buhuo | `liu-defected` | 3、4、5 | 押解牌折斷之後的每一鏡：第 3 集懸念之後（如果還有鏡頭）、第 4 集姬無霜帳中、第 5 集盟堂上站在她身後。腰間沒有押解牌，左肩繃帶只在領口露一角。 |
| zhuxu | 基本外觀 | 2、4 | 第 2 集全集（背著布包西行），以及第 4 集他回到齊雲山外、把火脊鐵藏進廢窯那一段。 |
| zhuxu | `zhuxu-returned` | 4 | 從廢窯出來之後：背上已經沒有布包、一身路塵，被燕迴的追兵圍住，到殿前廣場卸劍那一鏡（a05-s016）為止。樣鐵和秘錄都收在懷裡，要拿出來時寫在 prompt。 |
| zhuxu | `zhuxu-disarmed` | 4 | 從卸劍後（a05-s017）到全集結束：同 `zhuxu-returned`，但左腰沒有劍，只剩深綠腰帶。搜身、走上殿階跪交秘錄、被玄門弟子押下都用這個。劍的去向只寫 prompt（a05-s017 劍躺在他腳前的霜上、a05-s030 一名追兵拿著）。 |
| ji-wushuang | `wushuang-armed` | 5 | 只在第 5 集：盟堂准奏之後，她率幽都舊部登鯨背嶼那一段（照第 5 集分場表）。第 3 集盟堂與點兵、第 4 集營帳都用基本外觀；第 4 集帳中的弓與箭囊寫成架上的道具。盟堂跪請一律用基本外觀、不帶兵器。 |
| yin-wusheng | `yin-cut-hair` | 5 | 第 5 集他在梵林寺禪房、跪在寂聞榻前以劍割下一截髮尾之後的每一鏡（照第 5 集分場表的禪房版）。割髮那一鏡本身用基本外觀，髮尾還是長的。之後的集數沿用，直到另有變化。 |
| ji-wen | 基本外觀 | 5 | 冷開場、連夜赴鯨背嶼、走到海道上，到箭光射下之前。 |
| ji-wen | `jiwen-struck` | 5 | 前半：箭釘進胸口之後，盤坐自封功力、箭化青煙散去、被抬離海道，都還穿著原本的袈裟、戴著蓮冠，胸口有青色箭痕。殷無聲割髮在禪房，那時寂聞已換成 `jiwen-sealed`（照第 5 集分場表）。 |
| ji-wen | `jiwen-sealed` | 5 | 抬回梵林寺禪房、換下袈裟之後的每一鏡：灰色僧袍、沒有冠，箭痕在鬆開的領口露出邊緣。包括懸念「你還要留她到幾時」。依 setting，他會一直這樣到第 11 集。 |
| shen-guihe | 基本外觀 | 6 | 冷開場倒在書齋（筆從指間滑落）、被包三錢與殷無聲扶上榻、分魂那一場：都還穿著白袍、戴著鶴冠，倒地與被扶的樣子寫在 prompt。 |
| shen-guihe | `shen-bedridden` | 6 起 | 分魂、本體昏迷之後的每一鏡：散髮、無冠、素白中衣、臉色灰白、閉眼或半睜，沒有扇子。從卸下鶴冠、脫去外袍之後那一鏡起（卸冠那一鏡本身用基本外觀，冠在包三錢手上），到本集結束；第 7–11 集本體臥病都沿用，直到第 12 集合魂。 |
| ji-wen | `jiwen-sealed` | 6 | 全集（被殷無聲抬到書齋外、禪房）。 |
| yin-wusheng | `yin-cut-hair` | 6 | 全集。 |
| liu-buhuo | `liu-defected` | 6 | 全集（鯨背嶼主帳）。 |
| ji-wushuang | 基本外觀 | 6 | 盟堂列席（代幽都舊部）、以手傷告退：不帶弓、不帶箭囊。手背的割傷只寫插鏡 prompt（〈連戲提醒〉第 14 條）。 |
| ji-wushuang | `wushuang-armed` | 6 | 第 6 集不用（主編定案：主帳裡的弓與箭囊寫成架上道具，照第 4 集；燈下攤開繡布用基本外觀）。 |
| sha-nu、wuming-jianke | 基本外觀 | 6 起 | 兩人只有基本外觀。影子淡只寫 prompt；白紗冠、半面具、白柄劍都寫死在外觀裡。 |
| shen-guihe | `shen-bedridden` | 7 | 全集（本體昏臥書齋，沒有台詞）。化身受創那一刻本體咳血：唇角的血只寫插鏡 prompt（「a thread of dark blood at the corner of his colourless lips」），look 不改；紗女替他擦，包三錢捧水（分場表 a04 場 2 第 1 點）。 |
| ji-wen | `jiwen-sealed` | 7 | 全集（禪房）。推開滄瀾客那一掌也是這個 look：封功之身的一掌，沒有金色氣勁，寫在 motion。 |
| yin-wusheng | `yin-cut-hair` | 7 | 全集。 |
| ji-wushuang | — | 7 | 主編定：本集不入鏡（表頭留著）。第 8 集入鏡時照第 6 集：基本外觀；右手背的布條只寫插鏡 prompt（第 14 條）；弓與箭囊在架上。 |
| canglan-ke | 基本外觀 | 7 | 全集（雪線、梵林寺禪房）。毛皮斗篷進了禪房也不脫——他剛下山；第 8 集要打鬥時再議要不要加不披斗篷的 look。引血的刀只寫 prompt。 |
| yuelan-ke | 基本外觀 | 7 | 雪線、入盟、書齋送藥、客院，到外港被第一劍劃開紅衣之前：紗巾遮口鼻、藥箱在肩。 |
| yuelan-ke | `yuelan-crest` | 7 | 外港：第一劍劃開紅衣、雙淵紋露出之後，到第二劍廢臂之前——揭穿的定格、詩號字卡、劍客的反應鏡之間回拍他，都用這個（燕迴第二劍之後才到，洛青衍不在外港）。紗巾掉下來掛在頸上、臉全露、兩臂都好、沒有藥箱。 |
| yuelan-ke | `yuelan-crippled` | 7 | 第二劍之後的每一鏡：左臂垂著、左袖血濕，不包紮；到 a04 場 1 第 1 點那一格插鏡（a04-s001：守衛圍上來之前，他用右手把衣襟攏上）為止。a03 場 4 最後一鏡燕迴喊「住手」時還在碼頭根部；守衛圍住劍客的全景（a04 場 1 第 2 點）已經是 `yuelan-covered`。 |
| yuelan-ke | `yuelan-covered` | 7 | 2026-10-06 新增。a04 場 1 第 1 點（a04-s001，右手攏衣的插鏡）之後拍到他的每一鏡（第 2 點守衛圍成半圈的全景起）：同 crippled，但衣襟被右手攏在胸前、雙淵紋看不見，只在指縫露一線銅線；趁亂登船、船舷欠身、船離岸。燕迴從此看不到紋（盟堂上他說「衣裡，我也沒看見」）。第 17 集起他在赤淵宮的樣子另加 look（冠回來、左臂藏在長袖裡）。 |
| sha-nu、wuming-jianke | 基本外觀 | 7 | 仍只有基本外觀。劍客在外港挨了赤羽一指（細綱：本體「因化身受創」咳血）：白袍左胸一個指尖大的焦痕只寫 prompt——外港這一場（a03 場 4 第 21 點起到 a04 場 1 結束）正面拍到他左胸的鏡頭都寫；a04 場 2 起改寫他的左手平按在左胸上蓋住，不寫焦痕、不寫繃帶、不加 look（分場表第二節）。 |
| ji-wushuang | `wushuang-armed` | 8 | 鯨背嶼室外的每一鏡：灘頭、石窟口、率舊部、與鬼燈君對峙、斬首、擲頭顱、受三宗作揖。背弓、有蓋箭囊。**斬首的刀不在 look 裡，寫 prompt**（刀從哪裡來由分場表定，例如從身旁舊部腰間拔出；定了就照抄）。基本外觀寫死了「Unarmed」，所以凡是她手上有刀的鏡頭都必須選 `wushuang-armed`。右手背的布條只寫插鏡 prompt（第 14 條）。主帳內若照第 6 集弓與箭囊在架上，用基本外觀；由分場表定，定了全集不換。 |
| canglan-ke | 基本外觀 | 8 | 梵林下山、登島、躍入石窟、混戰、柳不活把傳單紙塞進他掌心，到一掌碎陣那一鏡為止（碎陣那一掌本身用基本外觀）。引血的刀仍在斗篷裡，本集不出鞘、不寫進 look。 |
| canglan-ke | `canglan-spent` | 8 | 碎陣之後、千燈熄滅的下一鏡起：出窟、把傳單紙交給紗女、灘頭全場，到本集結束。傳單紙在他手上時寫 prompt。第 9 集起沿不沿用由第 9 集定（state：真氣大耗）；第 10 集接劍、第 11 集引血前回不回基本外觀，到時再議；第 11 集後白髮拄杖另加 look。 |
| guideng-jun | 基本外觀 | 8 | 從他在灘頭第一次露臉起，到斬首那一刀為止。海面千燈上的剪影不列 id（第 30 條）。**斬首之後任何一鏡都不列 `guideng-jun`**：設定圖畫的是有頭的人；冠落、身形倒下、頭顱都寫插鏡或群眾鏡的 prompt（第 31 條）。沒有斬首後的 look。 |
| ji-wen | `jiwen-sealed` | 8 | 若入鏡（梵林寺禪房，那一碗藥）。 |
| yin-wusheng | `yin-cut-hair` | 8 | 全集（禪房倒藥、鯨背嶼石窟外）。 |
| liu-buhuo | `liu-defected` | 8 | 全集（石窟混戰讓路、灘頭）。靴底的傳單紙、袖裡的印圖樣、腰間的封口葫蘆照第 6 集第十一節；紙從靴底到滄瀾客掌心那一下寫插鏡 prompt（`characters: []`）。 |
| shen-guihe | `shen-bedridden` | 8 | 若入鏡（書齋切回鏡），全集都是這個；沒有台詞（第 34 條）。 |
| sha-nu、wuming-jianke | 基本外觀 | 8 | 仍只有基本外觀；影子淡只寫 prompt（第 35 條）。劍客左胸的焦痕：照第 7 集第十一節，第 8 集若他換了袍就不再寫——由第 8 集分場表第十一節（承接）定一次，定了全集照辦，不加 look。 |
| alliance-guard | 基本外觀 | 8（可省） | 只拍他被叫來問話（槍在手上、站著回話）就用基本外觀。基本外觀寫死了「a long spear with a white tassel」：要拍他被押下、槍被收走的樣子，先照 `zhuxu-disarmed` 的先例在 `cast.json` 末尾加一個不帶槍的 look（只把那一句換成不提槍的句子，不寫「no spear」這類否定句），再跑 `node header.mjs --ep 8`。加了之後第 2、3、5 集的表頭與成品會少一個 look，要照第 6 集的做法重跑那三集的 `header.mjs`／`merge.mjs`；所以能不拍就不拍，押下兩人可以只用紗女的一句話與一扇關上的門交代。 |

## 連戲提醒

1. **姬無霜的印**：基本外觀和 `wushuang-armed` 都不寫印。第 2 集起，凡是拍到她右手背的插鏡，prompt 都要寫「two faint gold seal marks on the back of her right hand, a slanted brush stroke and a small curling cloud hook, with an empty space beside them for a third」（第 3 集起的定句；第 2 集 a05-s054、s055 與第 1 集的一道印「one faint gold seal mark, a slanted brush stroke」都在 2026-10-05 跨集審後改成同一套形狀）。第 3 集她舉手立誓，柳不活看見的「只差梵林一筆」就是這個構圖。她平時用袖子遮手（第 1 集 a03-s051 的做法）。
2. **第 5 集的「鬼燈君黑袍人」**：
   - 只寫在 prompt。這幾鏡的 `characters` 不列 `ji-wushuang`（列了就會帶進她的設定圖），也不配任何聲音；企劃包寫的「冷笑」只用畫面（面具下肩頭一聳、轉身），不放笑聲。
   - prompt 寫成「a tall hooded figure in a black robe embroidered with dark-violet seven-star and skull-lantern motifs, a blue-green mask covering the whole face」，兜帽壓低。不寫銀白長髮、鳳冠、霜蕨紋，也不寫「slim black lacquered bow」，弓只拍成逆著箭光的剪影。
   - `wushuang-armed` 不要跟放箭的鏡頭剪在一起。觀眾第 3 集起就猜得到她，但企劃包要面具下是誰「未揭」。
   - 山脊上留下的「青面具碎角」寫在插鏡 prompt。
3. **姬無霜的弓**：`wushuang-armed` 的弓上的是一條普通黑弦，因為第 1 集冷開場那條暗紅色的血弦斷成兩截，一截在聶孤鐵手裡，一截被釘在玄門長老的窗上、現在在沈歸鶴手上。箭囊是有蓋的，看不到裡面的箭，避免露出第 1 集 a01-s005 那四支帶暗紅紋的箭。
4. **包三錢的銅錢**：第 1 集結尾掉了一枚（a05-s089），但他的基本外觀和兩個 look 都寫三枚。第 2 集開頭最好給一個插鏡，讓他把掉的那枚撿回、穿回紅繩上（照他「數一數，心裡踏實」的性子），之後三枚就都對得上了。如果第 2 集想讓那枚銅錢留在長老房裡另作伏筆，就要在 `cast.json` 另加兩枚銅錢的 look，不能只改 prompt。
5. **柳不活的酒葫蘆**：第 3 集冷開場他「把一壺酒放在砧邊」。建議那一壺寫成另一只陶酒壺，腰間那個封口小葫蘆始終不開、不離身，跟基本外觀和兩個 look 一致。
6. **寂聞的念珠**：第 1 集他捏裂了一顆（a05-s067）。三個外觀都沒提，插鏡可以拍那顆裂珠。兩個 look 都保留念珠，這是他跟沈歸鶴之間的羈絆物件。
7. **竹虛的布包**：第 2 集是西行的行囊。第 4 集他先把整塊火脊鐵藏進廢窯，所以藏鐵之前用基本外觀，之後用 `zhuxu-returned`；殿前廣場卸劍之後換 `zhuxu-disarmed`（見上表）。被燕迴收走、送進庫房的那一小塊樣鐵，只在插鏡 prompt 裡出現。
8. **玄門長老**：第 1 集已死。第 3 集柳不活推算、第 4 集受審揭開死訊時，如果要拍回憶，用 `xuanmen-elder` 的基本外觀，或拍棋盤、窗上白霜等第 1 集已經有的物件。第 1 集的 `source` 只能切同一支片裡的鏡頭，所以不能跨集取用素材。
9. **洛青衍**：第 1 集結束時他留在外港的扶瀾商船上，第 2–5 集不出場，第 6 集才抵盟。這四集不要讓他入鏡。
10. **聶孤鐵的鍛鉗**：基本外觀寫的是「Holds long iron forge tongs」，所以第 3 集一律選 `nie-nail-wound`，否則每一鏡都會被補上鍛鉗。第 1 集冷開場（鑄箭當日）的回憶照舊用基本外觀。
11. **分魂的同框規則（第 6 集起）**：
   - 分魂那一鏡（紗女與無名劍客自沈歸鶴身側立起）`characters` 最多 3 個：`shen-guihe`（基本外觀）、`sha-nu`、`wuming-jianke`；包三錢與殷無聲在這一鏡寫進 prompt，或拍成分切的反應鏡。
   - 本體昏臥之後，凡是拍到他身形或臉的鏡頭，`characters` 列 `shen-guihe` 就要配 `character_looks: {"shen-guihe": "shen-bedridden"}`；只拍手、枕邊紙扇的插鏡不列角色。本體與化身同框（化身守在榻前）照樣是 3 人上限。
   - 分魂之後 `shen-guihe` 沒有台詞；他要說的話由 `sha-nu`（盟內）或 `wuming-jianke`（江湖）用自己的 speaker id 說。寂聞在書齋外看見的是化身，之後整集跟他對話的也是化身。
   - 紗女的聲音是沈歸鶴的（同一個 Iapetus）：她第一句台詞之後給一個包三錢或殷無聲的反應鏡，觀眾才知道這不是配錯。三宗只被告知「代行」，長老與燕迴的台詞裡不能出現「分魂」「元神」「化身」這些字（企劃包 state：三宗不知道是分魂）；知道的只有包三錢、殷無聲、寂聞，以及感應到箭找不到完整元神的姬無霜。
12. **化身的影子**：setting 寫「分魂的紗女與無名劍客影子比常人淡一分」。這句**只寫在 prompt**（例如「her shadow on the floor slightly fainter than it should be」），而且只在看得到影子的鏡頭寫（燭光下、日光下的地面）；兩人的 appearance 都不寫，免得設定圖把人畫成半透明。
13. **洛青衍的胎記插鏡**：與第 1 集 a02-s037（姬無霜）、a04-s043（洛青衍）**同構圖**——`camera: "Insert of the back of his neck, locked"`、`characters: []`、prompt 照第 1 集的句型：「The back of Luo's neck seen from behind and slightly above as he bows, the low sea-green coral crown at the top of frame, his long dark blue-black hair swung forward to both sides of his neck, a small crescent-shaped birthmark on the back of the neck at the centre of frame, the ivory collar of his robe below」，`motion` 是行大禮時長髮揚起、露出一瞬。姬無霜那一側接她的眼睛特寫再接茶盞落地，本集不拍她的頸後（她的胎記第 1 集已給過，本集只給他的）。
14. **姬無霜手背的割傷**：基本外觀與 `wushuang-armed` 都不寫傷、不寫印。盟堂碎瓷割手那一鏡與之後拍到她右手背的插鏡，prompt 寫「two faint gold seal marks on the back of her right hand, a slanted brush stroke and a small curling cloud hook, with an empty space beside them for a third, a fresh shallow cut from a porcelain shard running straight across both marks, a bead of blood」；回鯨背嶼之後的手背插鏡改寫成「a strip of white cloth bound across the back of her right hand」。中景、全景不改 look，手照第 1 集的習慣縮在袖裡。
15. **紗女與姬無霜不要混**：兩人都是銀白長髮、身形修長。盟堂上兩人同在，靠服色分：紗女是月白與灰紗、白紗冠、赤足、沒有冠飾；姬無霜是黑袍、紫氅、黑銀鳳冠。全景時兩人放畫面兩側（紗女在書院席，姬無霜在幽都舊部席），不要讓兩人在同一個中景裡並肩；反應鏡各拍各的。
16. **沈歸鶴的紙扇**：分魂之後紙扇留在書齋（榻邊或案上），是本體的羈絆物件，插鏡可以拍；紗女不拿扇，無名劍客用劍（setting：「歸鶴三折」原以紙扇施展，第 10 集隨無名劍客被毀而失去）。不要讓化身把扇子帶出書齋。
17. **第 5 集留下的狀態**：寂聞 `jiwen-sealed`、殷無聲 `yin-cut-hair`、柳不活 `liu-defected` 照第 5 集分場表第十一節沿用；書齋案抽屜裡的封條、斷弦、鐵釘、拓片照第 2、3、5 集寫在抽屜（不是木盒）；竹虛的青瓷藥瓶仍在沈歸鶴左袖、沒有人知道——本集他倒下時藥瓶要不要被包三錢發現，由本集主編定，定了就寫進分場表第十一節交給第 7 集（第 7 集赤羽送藥那場要用）。
18. **第 6 集留下的狀態（第 7 集要守）**：照 `ep6/beats.md` 第十一節〈本集結束時交給第 7 集〉。本體 `shen-bedridden`、鶴冠與國書在書案上、紙扇在枕邊矮几、染血的外袍在榻底；**青瓷藥瓶空了、在包三錢懷裡**（第 6 集主編定案：他撿到、看見、不知道來歷）——赤羽送火脊丹時，包三錢知道本體曾靠一種藥撐著、現在沒有了，紗女對「有沒有第二瓶」只說「別問」；傷的來歷（寒毒、火脊鐵、竹虛）仍沒有人說出口，本集也不說。寂聞 `jiwen-sealed`、殷無聲 `yin-cut-hair`、柳不活 `liu-defected`（若入鏡）沿用。
19. **第 7 集的三張遮著的臉**：紗女（白紗冠遮上半臉，露嘴與下巴）、無名劍客（白半面具遮上半臉，素白鐵冠）、赤羽（赤褐紗巾遮口鼻，露眼與眉，沒有冠）。三個人遮的不是同一半；prompt 寫到任何一個都照 `cast.json` 的句子，不要只寫「veiled」「masked」。赤羽與無名劍客同框（客院截藥童、外港）時，一個遮下、一個遮上，剛好分得開。
20. **赤羽與燕迴不要混**：兩人都帶紅。燕迴是鏽褐與黑、左袖撕掉、裂銅冠、紅纓刀；赤羽是暗赤紅素袍、沒有冠、紗巾、藥箱、兩袖完整。外港一場兩人同框，燕迴在守衛那一側，赤羽在跳板那一側（軸線由分場表第四節定，定了就不換）。
21. **雙淵紋**：固定句「the twin-abyss crest of the Red Abyss Palace, two dark whirlpools side by side in bronze thread」；第 7 集只在 `yuelan-crest`、`yuelan-crippled`、「紅衣碎片」插鏡（細綱 evidence：「赤羽紅衣內的雙淵紋碎片」——劍客手裡那一角布，`characters: []`）與外港幾格出招插鏡（a03 場 4 第 11、13、26 點，`characters` 為空，衣服與紋寫在 prompt）寫；`yuelan-covered` 不寫紋（衣襟攏上了，燕迴看不到）。三宗長老看不懂這個紋、也不信；叫得出「赤淵宮」的只有劍客與紗女。
22. **赤羽的藥與寂聞的湯藥是兩件事**：赤羽送到書齋的是「火脊丹」，寫成「a small red lacquered pill case holding a single glossy crimson pill the size of a longan seed, flecked with fine gold」（2026-10-06 改：原本的 single dark-red pill 跟竹虛那瓶藥的 small dark-red pill 幾乎一樣，觀眾會當成同一種藥；火脊丹故意比它大、亮、帶金點），被劍客劍尖挑開（挑開後的寫法由分場表第九節定）；藥童換進禪房的是另一種藥，碗照第 6 集的句子「a plain black earthenware bowl of dark herbal broth」，加「a thin film of red floating on the dark broth」；丟進井裡的空瓶寫成「a small plain brown glazed bottle」——**不是**第 6 集的青瓷藥瓶（那只空瓶在包三錢懷裡；本集若入畫照第 6 集的句子「a small round celadon medicine bottle with a cork stopper」）。
23. **本體與化身的同框（第 7 集的場）**：紗女與包三錢在榻前決定要不要服藥，`characters` 是 `sha-nu`、`bao-sanqian`、`shen-guihe`（配 `character_looks: {"shen-guihe": "shen-bedridden"}`）三個就滿了；赤羽若在同一鏡，拆成兩鏡，或把本體拍成榻上的局部（插鏡不列角色）。化身受創、本體咳血是兩地同一刻：外港一鏡、書齋一鏡交叉剪，不要把化身與本體放進同一鏡去「感應」。本體仍沒有台詞；他要說的話仍由紗女（盟內）或劍客（江湖）說。
24. **影子淡（第 7 集）**：外港是日光下的碼頭，劍客在石面上的影子每一鏡都看得見，凡是拍到地面就寫「his shadow on the stone slightly fainter than it should be」；紗女在書齋燭光下同樣。look 與設定圖都不寫（第 12 條）。
25. **三宗不知道分魂（第 7 集）**：長老、執事、燕迴、洛青衍、赤羽、滄瀾客聽得見的台詞裡沒有「分魂」「元神」「化身」「影子」；赤羽懂（他的藥是衝著元神來的），但他只說「先生的病」「舊傷」。盟內記劍客「無故傷客」用的稱呼是「先生的人」。滄瀾客對寂聞只談封功與寒潭，不談沈歸鶴。
26. **滄瀾客與寂聞**：滄瀾客五十多歲、鐵灰長髮、深藍布冠；寂聞四十多歲、光頭、`jiwen-sealed`。禪房一場兩人隔榻；寂聞推開他那一掌是封功之身的一掌（motion 寫「his palm lands with no light and no force」，沒有金色氣勁），滄瀾客被推開是因為他不擋。滄瀾客的深藍袍與玄門執事的暗青灰袍別混：執事戴布帽、掛鑰匙與帳冊、袖手；滄瀾客披毛皮、佩劍。滄瀾客的「至交」身分只用動作與那把刀呈現，不寫「我把你當朋友」（narrative_constraints）。
27. **寂聞每日的湯藥**：第 6 集 a04 場 3 立下的——殷無聲端、殷無聲餵、黑陶碗；本集懸念就是這一碗（第 22 條的寫法）。殷無聲發現後「從那夜起每一碗都倒在井邊」是第 8 集起的事（m06），本集只到他端在手上、看見浮紅。
28. **洛青衍在第 7 集**：他住客院，截藥童那場他在旁觀（細綱：「在客院旁觀整場，對無名劍客生出敬意」）——他不知道劍客是誰，也沒有人告訴他。本集不拍他的頸後（第 6 集已給過；主編若真要再給一次胎記插鏡，照第 13 條同構圖）；手腕還沒有黑繩（第 16 集起）；他與那位夫人仍沒有正臉同框。
29. **岳嵐客的左臂**：第 7 集外港被劍客廢去之後永久不能用。本集 `yuelan-crippled` 是血濕垂臂、不包紮；第 17 集起的 look 要寫「左臂藏在長袖裡」。第 7 集之後他不再入盟。第 7 集的黑漆藥箱在外港落海（`ep7` a03-s072），第 17 集的 look 若照 setting 寫藥箱，寫成另一只（不寫 black、不寫 right shoulder）。
30. **鬼燈君的剪影（第 8 集）**：setting 寫「Appears first as a silhouette on the sea of lanterns」。千燈上的剪影鏡 `characters: []`，prompt 寫「a tall gaunt figure seen only as a black silhouette against the glow of the lanterns, the seven points of his crown and the ragged claw-pointed hems of his long sleeves sharp in outline」，不寫臉、不寫髮色。要到灘頭露臉那一鏡才列 `guideng-jun`（列了，設定圖就會把臉畫出來）。腰間七枚銅鈴的聲音可以比臉先到（sfx）。
31. **斬首的寫法（第 8 集）**：照布袋戲的寫意，不拍血腥，分三格：一刀（刀光一閃；出刀那一格 `characters` 可以是 `ji-wushuang`（`wushuang-armed`）與 `guideng-jun`，刀寫 prompt）→ 七角黑冠落地的插鏡（`characters: []`，「the tall seven-pointed black crown falling onto the wet sand」）→ 身形倒下（背光全景或剪影，`characters: []`，「a tall gaunt figure in a black-and-violet robe crumpling onto the sand, seen against the light」）。不拍頸上的斷口，不見血。頭顱一律寫成被黑布裹住（「a round bundle wrapped in black cloth」）或背光的剪影。懸念「姬無霜拾起鬼燈君的頭顱向幽都方向一擲」：`characters: ["ji-wushuang"]` 配 `wushuang-armed`，手裡是黑布裹著的圓包，擲出的弧線逆光；屍身與頭顱都不列 `guideng-jun`。narrative_constraints：死者只以遺物、記憶與他人的台詞出現。之後的集數若要提他，拍冠、銅鈴、鬼燈袍這些遺物，不用他的設定圖。
32. **鬼燈君與姬無霜不要混（第 8 集）**：兩人都是幽都的黑與紫（visual_style：幽都用黑紫）。姬無霜是銀白長髮、黑銀鳳冠帶銀鏈、黑袍繡白霜蕨、深紫外氅、背弓（`wushuang-armed`）；鬼燈君是灰紫長髮、七角黑冠、灰白臉、黑與暗紫袍繡七星與骷髏燈紋、爪尖長袖、腰間七枚銅鈴、空手。灘頭對峙的軸線由分場表第四節定，定了不換，兩人各占畫面一側；反應鏡各拍各的。紗女（月白、白紗冠）也在灘上時照第 15 條。
33. **鬼燈袍與青面具（第 8 集）**：第 5 集山脊上的黑袍人（其實是姬無霜）穿「a black robe embroidered with dark-violet seven-star and skull-lantern motifs」、戴「a blue-green mask covering the whole face」，她在盟堂說「青面具，是鬼燈君貼身死士戴的」「那件鬼燈袍，是他自己的」。本集鬼燈君本人的袍用同一句繡紋，觀眾一眼認得；但他戴七角冠，不戴兜帽、不戴面具。他的貼身死士戴青面具（prompt）。紗女在灘頭若提到第 5 集那一夜，台詞不能讓三宗知道放箭的是姬無霜：三宗本集只知道陣是鬼燈君布的、她是幫他們除害的恩人；知道箭是她從齊雲殿後山射的，只有觀眾與紗女（state.knowledge）。
34. **分魂的同框規則（第 8 集）**：本集的地點都在鯨背嶼，本體在盟府書齋。凡是拍到本體身形或臉的鏡頭（書齋切回鏡），`characters` 列 `shen-guihe` 就要配 `character_looks: {"shen-guihe": "shen-bedridden"}`；只拍手、枕邊紙扇的插鏡不列角色。本體與化身不在同一地，不要放進同一鏡；化身在灘上、本體在書齋，照第 7 集化身受創那一刻的做法兩地交叉剪。一鏡仍是 3 人上限。本體仍沒有台詞；紗女、無名劍客、本體仍是同一個 Iapetus。姬無霜知道兩人是分魂（第 6 集「找不到了，一個整的人」），但在三宗面前不說。長老、燕迴、鬼燈君聽得見的台詞裡仍不出現「分魂」「元神」「化身」；本集的陣收的是「魂」，台詞要小心，別讓長老把紗女跟「魂」連在一起。
35. **化身的影子（第 8 集）**：紗女與無名劍客的影子「比應有的淡」**只寫在 prompt**（「her shadow on the sand slightly fainter than it should be」「his shadow on the sand slightly fainter than it should be」），appearance、look、設定圖都不寫（第 12 條）。只在看得到地面影子的鏡頭寫。收魂陣的青綠光與千盞燈光底下，每個人的影子都會被打亂，看不出誰淡；建議放在破陣、千燈熄滅之後的灘頭（火把或日光下）。
36. **胎記插鏡（第 8 集）**：本集若拍姬無霜頸後的胎記（例如斬首那一刀她長髮揚起），與第 1 集 a02-s037（姬無霜）、a04-s043（洛青衍）**同構圖**：`camera: "Insert of the back of her neck, locked"`、`characters: []`；prompt 照第 1 集的句型——從背後稍高處看頸後，冠的底部在畫面頂端，長髮被一陣風吹向頸的兩側，「a small crescent-shaped birthmark on the back of the neck at the centre of frame」，下面是袍領；`motion` 是一陣風把長髮分開、停一口氣。不換別的構圖，觀眾才連得起第 1、6 集。洛青衍本集不出場，不拍他的。
37. **姬無霜的弓弦（第 8 集）**：後半「無名劍客在她身後看見她袖中一截弓弦滑過，紗女也看見了」與懸念「紗女手裡捏著一截新的斷弦」都是道具，只寫 prompt。`wushuang-armed` 背上那把弓寫死是上著弦的「a plain black cord」，袖中那一截與紗女手裡那一截都**不是**背上那條弦。分場表第九節要定這一截的固定英文（顏色、長短），而且要跟第 1 集那條暗紅血弦（斷成兩截：一截在聶孤鐵手裡，一截在沈歸鶴書齋案抽屜）分得開，或刻意連上，定了照抄（第 3 條）。若分場要讓背上那把弓的弦斷掉，得另加一個沒有弦的 look，不能只改 prompt。
38. **紗女的兩張紙（第 8 集）**：包三錢第 2 集拓下的陣符拓片，照第 2 集 a03-s036 的句子「a sodden, crumpled sheet of thin paper, its grey charcoal rubbing smeared and blurred」（泡過海水，乾了仍是糊的；本集寫 dried and stiff 即可）；柳不活靴底的通緝傳單，照第 4 集 a01-s003／s004 的句子「a grey hemp-paper leaflet with four short columns of thick black brush strokes」「the black pine-soot ink bleeding at the edges with a faint blue-black sheen」。筆跡比對的插鏡 `characters: []`，兩張紙並排。拓片怎麼從書齋抽屜到了鯨背嶼（紗女帶來），由分場表定。島底陣符的刻槽照第 2 集 a02-s072 的「cold blue-green light rising from the carved grooves」。
39. **千盞青燈的顏色（第 8 集）**：visual_style 寫「鯨背嶼用海面千燈的暖黃對照島底收魂陣的青綠」，企劃包第 8 集的 hook 寫「千盞青燈，每盞燈裡一縷幽光」。建議兩者合起來寫：燈罩是暖黃的紙燈，燈芯是一縷青綠的幽光（孩子的魂）；破陣時青綠一齊熄滅。第 2 集鯨背嶼山脊上的「tiny warm lamps」照舊。由分場表第九節定一句固定英文，全集照抄。
40. **鬼燈君的聲音（第 8 集）**：Azure、沒有 style；他的台詞**不加 `emotion`**（lint 會警告），語氣靠短句與標點。他與任何人都不同聲，質地也跟 Gemini 那一群不一樣，tts 之後主編要聽一次。TTS 前要站主確認後台允許清單有 `zh-TW-YunJheNeural`（〈第 8 集的新聲音〉）。
41. **第 7 集留下的狀態（第 8 集要守）**：照 `ep7/beats.md` 第十一節〈本集結束時交給第 8 集〉。寂聞 `jiwen-sealed`、殷無聲 `yin-cut-hair`、本體 `shen-bedridden`（不服任何人的藥，紗女每夜用玄門養氣法暫壓）；第 8 集先交代那一碗浮紅的湯藥沒有喝（殷無聲沒有餵、倒在井邊，m06；倒在井邊的藥渣第 11 集滄瀾客會認出來）。滄瀾客的刀在斗篷裡，本集不出鞘。柳不活 `liu-defected`，靴底傳單紙、袖裡印圖樣、腰間封口葫蘆都在身上。姬無霜右手背的布條（第 14 條），繡布與木匣在主帳。包三錢懷裡仍是那只空青瓷瓶。劍客的焦痕照 shot_looks 表。三宗仍不知道分魂、陣、盟兵被收買。
