# 《偶的江湖》第 1–6 集共用角色表說明

`cast.json` 是第 1–6 集角色物件的唯一來源。每一集的 `video.json` 只放這一集會入鏡的角色，但每個角色物件都要從 `cast.json` 整個照抄（`id`、`name`、`appearance`、`voice`、`shot_looks` 全部逐字，不刪 look、不改順序），設定圖才能共用。旁白聲音照抄 `narrator_voice`（與第 1 集表頭 `voice` 相同）。

逐鏡選 look 的寫法是 `scene.data.character_looks: {"<角色 id>": "<look id>"}`。被選的角色必須在同一鏡的 `characters` 裡，而一鏡最多 3 個角色。沒有選 look 的鏡頭一律用基本外觀。所以只拍局部的插鏡（手、胸口、髮尾）不列角色，傷、印、道具都要直接寫進 prompt。

## 第 1 集角色的改動

- `ji-wushuang`：appearance 刪掉「, one faint gold seal mark on the back of her right hand」。她第 2 集起手背有兩道印（書院、玄門），印記一律寫在插鏡 prompt，基本外觀與 look 都不寫印。
- `ji-wen`、`ji-wushuang`、`bao-sanqian`、`yin-wusheng`、`nie-gutie`：加了 `shot_looks`，appearance、name、voice 一字未改。
- `luo-qingyan`、`shen-guihe`、`xuanmen-elder`、`yan-hui`：完全沒動。

## 第 6 集的改動（2026-10-05）

- `shen-guihe`：加了 `shot_looks`（`shen-bedridden`，本體昏臥書齋）；appearance、name、voice 一字未改。
- 新增 `sha-nu`（紗女）、`wuming-jianke`（無名劍客）：沈歸鶴的兩個分魂，都用他的 Iapetus，理由見下方〈兩個化身為什麼用同一個聲音〉。
- 其他十三人與已有的 look 完全沒動。用 node 核對過：第 1–5 集成品 `docs/videos/ou-de-jianghu-e00N/video.json`、`series.json` 與 `ep1–5/header.json` 裡的角色物件，舊欄位（`id`、`name`、`appearance`、`voice`、已有的 `shot_looks`）全部與 `cast.json` 逐字相同；**唯一的差別是 `shen-guihe` 在那五集裡還沒有 `shot_looks` 這個鍵**（新 look 是本次加的）。每集自己的 `video.json` 與 `series.json` 一致，所以第 1–5 集的 lint 照樣過；但照第 1 集的先例（`ji-wen` 在第 1 集成品裡已帶著第 5 集才用的 `jiwen-struck`、`jiwen-sealed`），要讓五集與 `cast.json` 再次逐字相同，得對第 1–5 集各跑一次 `node header.mjs --ep N` 與 `node merge.mjs --ep N`（ids.json 會保住 line id；設定圖還沒畫，不會作廢任何東西），再跑 `cli.mjs script`。這一步由主控決定什麼時候做，本次沒有動成品。

## 角色總表（16 人）

| id | 名字 | 聲音 | 第 2–5 集 | 第 6 集 |
| --- | --- | --- | --- | --- |
| bao-sanqian | 包三錢 | Puck | 2、3、4、5 | 6 |
| ji-wen | 寂聞「怒目佛」 | Alnilam | 2、3、4、5 | 6（`jiwen-sealed`） |
| ji-wushuang | 姬無霜「霜夫人」 | Gacrux | 2、3、4、5 | 6 |
| luo-qingyan | 洛青衍 | Achird | 不出場（第 6 集抵盟） | 6（抵盟，第一次正式出場） |
| nie-gutie | 聶孤鐵「雕匠」 | Algenib | 3 | 不出場 |
| shen-guihe | 沈歸鶴「白鶴先生」 | Iapetus | 2、3、4、5 | 6（分魂前基本外觀；之後 `shen-bedridden`，沒有台詞） |
| xuanmen-elder | 玄門長老 | Schedar | 已死；只在回憶鏡用基本外觀 | 不出場 |
| yan-hui | 燕迴「赤纓」 | Fenrir | 2、3、4、5 | 6 |
| yin-wusheng | 殷無聲「啞劍」 | Sadaltager | 2、3（可省）、4、5 | 6（不說話，`yin-cut-hair`） |
| zhuxu（新） | 竹虛道人 | Umbriel | 2、4 | 不出場（押在玄門） |
| liu-buhuo（新） | 柳不活「求死書生」 | Enceladus | 3、4、5 | 6（`liu-defected`） |
| shuyuan-elder（新） | 書院長老 | Orus | 3、4、5 | 6 |
| xuanmen-steward（新） | 玄門執事長老 | Charon | 3、4、5 | 6 |
| alliance-guard（新） | 客院盟兵 | Sadachbia | 2（不說話）、3（可省，不說話）、5 | 不出場（客院門口的盟兵只寫 prompt） |
| sha-nu（第 6 集新） | 紗女 | Iapetus（沈歸鶴的聲音） | 不出場 | 6 起 |
| wuming-jianke（第 6 集新） | 無名劍客 | Iapetus（沈歸鶴的聲音） | 不出場 | 6 起（第 10 集滅） |

新角色的聲音都沒有跟第 1 集已用的十個聲音（Rasalgethi、Iapetus、Alnilam、Gacrux、Puck、Fenrir、Algenib、Achird、Schedar、Sadaltager）重複，新角色彼此之間也不重複。五個新角色都是男性，從可用男聲裡照年齡挑：中年、乾冷的竹虛用 Umbriel；二十多歲、帶氣音的柳不活用 Enceladus；六十多歲、有分量的書院長老用 Orus；五十多歲、管帳口吻的執事長老用 Charon；二十出頭的盟兵用 Sadachbia。

第 6 集的兩個化身是唯一的例外：`sha-nu` 與 `wuming-jianke` 刻意與 `shen-guihe` 共用 Iapetus（企劃包的鉤子寫死「她的聲音是沈歸鶴的聲音」），只靠 `style` 分：紗女更輕、更慢、更柔，無名劍客更硬、更短、更冷，兩個都不咳。工具允不允許，查證結果在〈兩個化身為什麼用同一個聲音〉。

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

## 新角色為什麼要說話

### 竹虛道人 `zhuxu`（第 2、4 集）

竹虛是企劃包的主要人物（第 2、4 集的 characters 裡都有他），他的台詞沒有人能代說：

- 第 2 集後半的高張力：他在三宗盟後山認出沈歸鶴咳出的血裡有鐵屑，把血帕塞進自己懷裡，對寂聞說「只是夜露」。這是他替沈歸鶴說的第一個謊，非他本人開口不可。
- 第 4 集後半：他在齊雲殿外被圍，不還手，走上殿階跪交《裂山秘錄》。

外觀照 setting 改寫成第 2 集的樣子。背上的布包寫成中性的「a cloth-wrapped bundle on his back」，不交代裡面是什麼。另外加了一柄收在鞘裡的劍：他是「Taoist swordsman」，招式是裂山訣劍法。不寫死的話，生圖模型會時有時無地自己補劍。寫死之後，第 4 集的「不還手」也有了畫面：手不碰劍。

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

### 沒有建的角色

- 姬無霜的侍女（第 6 集）：企劃包的轉折寫她在鯨背嶼向柳不活打聽「扶瀾國的船什麼時候到」。不建角色、不配聲音：她只在 prompt 裡（建議寫成幽都舊部的年輕侍女，黑衣、無冠，跟姬無霜分得開），走到柳不活身邊低聲說了一句，**那句話由柳不活重複出來**（「扶瀾國的船？」），或由旁白接一句。要是主編覺得非她本人說不可，就得在 `cast.json` 建角色、配一個沒用過的女聲，再跑 `header.mjs`。
- 扶瀾國使船的隨員與水手（第 6 集）：跟在洛青衍身後的隨員只寫 prompt，不說話；國書由洛青衍自己捧上。
- 第 6 集客院門口的盟兵：只寫 prompt（見上方第 6 集的出場名單）。
- 鬼燈君：第 2–5 集不出場（第 8 集才現身）。
- 第 5 集的「鬼燈君黑袍人」：其實是姬無霜，只寫在 prompt。
- 幽都黑衣人、巡船水手、鯨背嶼老婦與昏睡的孩子、各宗弟子、梵林僧人：都不說話。第 2 集冷開場跪在灘頭的老婦用畫面加旁白交代。孩童昏睡的消息由燕迴（巡船）帶回。「竹虛去玄門分院奔喪」這個說法由沈歸鶴或旁白說。第 4 集傳單上的字由燕迴或包三錢念出（殷無聲不能念）。
- 梵林長老：第 5 集盟堂上，梵林的位子是寂聞的空位，劇情要的就是這張空椅子，所以不補人。

## shot_looks 用在哪裡

| 角色 | look id | 集 | 從哪一段起、到哪一段止 |
| --- | --- | --- | --- |
| bao-sanqian | `bao-soaked` | 2 | 前半：跳海後被燕迴的巡船撈起，濕透、裹著毯子，手裡捏著泡濕的拓片，一直到他上岸回盟府。 |
| bao-sanqian | `bao-chilled` | 2 | 後半：落海受寒、臥床三日（第 3–6 日）的戲，包括懸念那場把拓片攤在沈歸鶴案上（身上裹著被子去）。第 3 集起回基本外觀。 |
| nie-gutie | `nie-nail-wound` | 3 | 他在第 3 集的每一鏡都用這個（冷開場把手釘在砧上、擲釘、說出箭的規矩、砸碎鐵砧）。釘子本身、手被釘在砧上、拿鐵鎚砸砧，都寫在 prompt。這個 look 不拿鍛鉗。 |
| liu-buhuo | `liu-wounded` | 3 | 前半：鐵釘穿過左肩之後，從鐵廬到回盟、在盟堂看見姬無霜的手背，都用這個。押解牌還掛在腰上，折牌的那一鏡也用它（牌在手上）。 |
| liu-buhuo | `liu-defected` | 3、4、5 | 押解牌折斷之後的每一鏡：第 3 集懸念之後（如果還有鏡頭）、第 4 集姬無霜帳中、第 5 集盟堂上站在她身後。腰間沒有押解牌，左肩繃帶只在領口露一角。 |
| zhuxu | 基本外觀 | 2、4 | 第 2 集全集（背著布包西行），以及第 4 集他回到齊雲山外、把火脊鐵藏進廢窯那一段。 |
| zhuxu | `zhuxu-returned` | 4 | 從廢窯出來之後：背上已經沒有布包、一身路塵，被燕迴的追兵圍住、走上殿階跪交秘錄，一直到本集結束。樣鐵和秘錄都收在懷裡，要拿出來時寫在 prompt。 |
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
7. **竹虛的布包**：第 2 集是西行的行囊。第 4 集他先把整塊火脊鐵藏進廢窯，所以藏鐵之前用基本外觀，之後用 `zhuxu-returned`。被燕迴收走、送進庫房的那一小塊樣鐵，只在插鏡 prompt 裡出現。
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
