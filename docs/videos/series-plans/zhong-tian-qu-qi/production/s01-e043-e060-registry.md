# 第 43–60 集的角色與場景對照（寫稿前先看）

第一季剩下的 18 集（第 43–60 集）用到的每個角色與場景，已經先登記進共用檔：
`production/cast.json`、`hailuo/gen-dh.mjs`（`SET`、`DH`、`EN`、`NAMED`）、`colab/ref2manifest.mjs`（`EN`、`EXTRAS`）、
`hailuo/dub-glossary.json`（`characters`、`terms`）。各集的撰稿人只改自己那一集的檔
（`docs/videos/zhong-tian-qu-qi-e0NN/`、`hailuo/ff-dh-e0NN.json`、`hailuo/clips-dh-e0NN.json`），**不要再改上面這些共用檔**。
還缺什麼（另一個小角色、另一個場景），寫進自己那張票的 Notes 交給主 session 登記，不要自己加。

## 怎麼用

- 角色：`video.json` 的 `characters` 從 `cast.json` 照抄 `id`、`name`、`appearance`、`voice`，一個字都不要改（換臉就是這樣來的）。
- 場景：`gen-dh.mjs` 用鏡頭 prompt 的文字比對 `SET` 正規式，**由上往下找第一個符合的**。所以每鏡 prompt 開頭的場景句要寫下表「prompt 要寫的字」，
  而且整句 prompt 裡**不要寫到別的場景的關鍵字**（例如在客棧院子的鏡頭寫 `examination hall` 就會被貢院搶走；新場景的正規式都排在最前面）。
  寫完跑 `gen-dh.mjs`，檢查 `ff-dh-e0NN.json` 每鏡的 `refs` 是不是你要的那張 `dh-set-*`。
- 畫面上叫得出名字的人用 `EN` 的英文名（`Headmaster Cheng`、`Prefect Chu`…）；`NAMED` 會讓沒列在 `characters` 卻在 prompt 裡被點名的人也帶上定妝照。
- 群眾（考生、衙役、刺客、禁軍、村民）只寫在 prompt，不進 `characters`。`ref2manifest.mjs` 的 `EXTRAS` 這次加了
  `examinees|candidates|runners|constables|assassins|riders|horsemen|drummers|musicians|youths|lads|townsfolk|officials|thugs|henchmen|attendants|eunuchs|troops|cavalry`，
  群眾鏡頭用這些字，才不會被寫成「畫面裡只有他一個人」。

## 新角色（8 位）

| setting_id | cast id | 名字 | EN（prompt 用） | 聲音 | 出場集 |
| --- | --- | --- | --- | --- | --- |
| s01-shanzhang | `chengshanzhang` | 程山長 | Headmaster Cheng | Sadaltager | 43、46、47、50 |
| s01-feng-xuezheng | `fengxuezheng` | 馮學正 | Examiner Feng | Charon | 43、46、47 |
| s01-wei-xun | `weixun` | 魏珣 | Wei Xun | Zubenelgenubi | 43、46、47 |
| s01-du-tie | `dutie` | 杜鐵 | Du Tie | Rasalgethi | 44、48、52、59 |
| s01-chu-zhifu | `chuzhifu` | 褚知府 | Prefect Chu | Orus | 46、47、48、52 |
| s01-deng-yasi | `dengyasi` | 鄧押司 | Sergeant Deng | Fenrir | 53、54 |
| s01-leng-tie | `lengtie` | 冷鐵 | Leng Tie | Iapetus | 56、57、58 |
| s01-chang-gonggong | `changgonggong` | 常公公 | Eunuch Chang | Enceladus | 60 |

男聲的 Gemini 聲音都已經有人用了，這 8 個都是跟原主人**從來不同集**的共用（第 1–42 集的 video.json 與第 1–5 季細綱都查過）：
Sadaltager 鄭伯（25、29、30）、Charon 孫掌櫃（最後一集 29）、Zubenelgenubi 賴三（最後 29）、Orus 趙捕頭（最後 28；e042 書吏也用）、
Rasalgethi 白大夫（38、39）、Fenrir 刁七（37–41；e024–26 魏記夥計也用）、Iapetus 胡縣令（最後一場在 60，冷鐵只在 56–58；e042 掌櫃也用）、
Enceladus 韓伯（55、59，常公公只在 60）。冷鐵扮公公（56–58）與真公公常公公（60）聲音不同。配音前要試聽。

外貌重點（給畫定妝照與檢查換臉）：程山長銀白長鬚、方巾、青灰儒衫、手持書卷；馮學正乾瘦高顴骨、深藍官服、烏紗；
魏珣鳳眼倨傲、月白錦袍、紫香囊；杜鐵瘸左腿拄木拐、補丁舊軍襖；褚知府方臉濃眉三綹黑鬚、緋色官袍；
鄧押司絡腮鬍、皂衣紅腰帶、過長的刀、腰掛鐵鏈；冷鐵面白無鬚冷峻、深紫宮服、拂塵、袖藏短刀；常公公圓臉慈和、鬢白、深青宮服、捧月白宮裝。
魏珣的月白與阿令的月白撞色，但兩人不同集。

## 已預先登記的小角色（只在 video.json 與 dub-glossary）

照 e042 的 `zhanggui`、`shuli`：外貌只寫在該集 `video.json`，`dub-glossary.json` 已經有它們的名字與 persona。聲音是建議值，挑的是該集沒有人用的聲音。

| id | 名字 | 建議聲音 | 用在 |
| --- | --- | --- | --- |
| `zhanggui` | 客棧掌櫃（e042 已有） | Iapetus | 44、45、50、51、52 的州城客棧 |
| `shuli` | 貢院書吏（e042 已有） | Orus | 43 的貢院；46、47 不要用（褚知府是 Orus），換 Alnilam |
| `xunkao` | 巡考 | Alnilam | 43 號舍 |
| `xunbing` | 巡兵 | Orus | 44 街口 |
| `shuliqi` | 書吏娘子（女） | Kore | 45 榜房 |
| `yayi` | 衙役 | Alnilam | 46、47、50、51 |
| `weiguanjia` | 魏家管家 | Charon | 48 暗巷 |
| `baobang` | 報榜人 | Iapetus | 49 城牆下 |
| `tongpan` | 通判 | Charon | 52 州府 |
| `zhifufuren` | 知府夫人（女） | Kore | 52 知府後宅 |
| `xinchai` | 信差 | Puck | 55 許家院子 |
| `shaonian` | 瞭望少年 | Puck | 56 瞭望台 |
| `jinjuntongling` | 禁軍統領 | Orus | 60 許家門口 |

詞彙表也加了 `解元`、`鄉試`、`山長`、`知府`、`公公`、`長公主`、`相府／相爺`、`秦烈山`、`鎮北將軍`。

## 場景

| 細綱的地點 | set id | prompt 要寫的字（`gen-dh.mjs` 的正規式） | 圖 |
| --- | --- | --- | --- |
| 州城書院（門口） | `shuyuan` | `academy gate` | 有 |
| 州城書院（山長的書案） | `shuyuan-zhai`（新） | `headmaster's study` | **要畫** |
| 貢院號舍 | `haoshe`（新） | `examination cells` | **要畫** |
| 貢院彌封房 | `mifeng-fang`（新） | `sealing room` | **要畫** |
| 貢院門口、報名處 | `gongyuan`（e042） | `examination hall`、`registration desk` | **要畫**（e042 起就缺） |
| 州城街口、州城大街、州城長街 | `zhou-jie`（新） | `main street of Qingzhou`、`street corner of Qingzhou`、`long street of Qingzhou` | **要畫** |
| 州城酒肆 | `jiusi`（新） | `tavern` | **要畫** |
| 州城客棧（大堂、樓梯、慶功宴） | `zhou-kezhan`（e042） | `prefectural inn` | **要畫**（e042 起就缺） |
| 州城客棧（樓上客房：44 夜裡窗前、50 給玉佩） | `kezhan`（沿用縣城客棧上房） | `upstairs guest room` | 有 |
| 州城客棧院子 | `zhou-kezhan-yuan`（新） | `back courtyard of the prefectural inn` | **要畫** |
| 州城暗巷 | `xiaoxiang`（沿用） | `back alley`、`narrow alley` | 有 |
| 州城榜房 | `bangfang`（新） | `results office` | **要畫** |
| 州府門口（46 擊鼓） | `xianya`（沿用縣衙大門，有鳴冤鼓） | `yamen gate` | 有 |
| 州府大堂、52 的州府（通判坐堂） | `zhoufu-tang`（新） | `court hall of the Qingzhou prefecture` | **要畫** |
| 州府後堂、知府後宅 | `zhoufu-houtang`（新） | `prefect's back hall`、`prefect's residence` | **要畫** |
| 州城城牆（紅榜從城頭垂下） | `chengmen`（沿用，e042 的州城城門也是這張） | `city gate`、`gatehouse`（不要只寫 city wall：那會落到別的正規式或沒有圖） | 有 |
| 州城北門官道 | `guandao`（沿用） | `official road` | 有 |
| 北邊渡口淺灘 | `beidu-qiantan`（新） | `shallow ford`、`north ferry ford` | **要畫** |
| 河灘篝火 | `hetan`（新） | `campfire` | **要畫** |
| 柳溪村口 | `cunkou`（沿用） | `village entrance` | 有 |
| 許家院子、許家門口 | `xujia-yuan`（沿用） | `farmhouse yard`、`yard gate`、`in the yard` | 有 |
| 柳溪打穀場 | `dagu-chang`（沿用） | `threshing ground` | 有 |
| 柳溪瞭望台 | `liaowangtai`（新） | `lookout tower`、`watchtower` | **要畫** |
| 柳溪村道（57 渠水淹村道、58 糧倉前的窄巷） | `cundao`（新） | `Liuxi village lane` | **要畫** |
| 柳溪糧倉（裡面、糧堆） | `gucang`（沿用） | `granary` | 有 |
| 柳溪水車邊 | `shentan`（沿用：水車在深潭邊，e033、e034 就是這樣拍） | `deep pool`（加 `water wheel` 寫水車） | 有 |

注意：
- `prefectural inn` 會吃掉所有含這兩個字的鏡頭；樓上客房寫 `upstairs guest room`、院子寫 `back courtyard of the prefectural inn`，這兩條排在前面。
- `examination hall` 會吃掉貢院裡的所有鏡頭；號舍、彌封房、榜房要寫各自的字（排在前面）。
- 村道的鏡頭不要寫 `granary`（會變成糧倉裡面），寫 `Liuxi village lane … the granary door at the far end` 也會先對到 `cundao`（排在前面）。
- 篝火在河灘：寫 `campfire`，不要寫 `bonfire`（沒有對應的正規式，會落到 `riverbank` 的柳溪河邊或沒有圖）。
- 第 49 集紅榜：城牆下的鏡頭寫 `city gate`；同一句又寫 `main street of Qingzhou` 的話會變成大街那張（大街排在前面）。

## 每集

圖：✅ refs-dh 已有；🎨 還要畫。定妝照是 `assets/refs-dh/<id>-portrait-t1.png`（唐小棠用 t2），場景圖是 `assets/refs-dh/set-<id>-t1.png`。
系統（`xitong`）只有聲音，沒有圖。

| 集 | 角色（season-01 id → cast id） | 地點 → set |
| --- | --- | --- |
| 43 貢院 | tang-xiaotang→`tangxiaotang` ✅、xu-yan→`xuyan` ✅、s01-shanzhang→`chengshanzhang` 🎨、s01-feng-xuezheng→`fengxuezheng` 🎨、s01-wei-xun→`weixun` 🎨、xitong | 州城書院→`shuyuan` ✅／`shuyuan-zhai` 🎨；貢院號舍→`haoshe` 🎨；貢院彌封房→`mifeng-fang` 🎨（考場外交摺紙→`gongyuan` 🎨） |
| 44 小將軍 | s01-du-tie→`dutie` 🎨、qin-shuang→`qinshuang` ✅、xu-yan、tang-xiaotang、xitong | 州城街口→`zhou-jie` 🎨；州城酒肆→`jiusi` 🎨；州城客棧→`kezhan` ✅（夜裡窗前）／`zhou-kezhan` 🎨 |
| 45 榜上無名 | xu-yan、qin-shuang、s01-xu-dalang→`xudalang` 🎨、tang-xiaotang、xitong | 州城客棧→`zhou-kezhan` 🎨（樓梯轉角）／`kezhan` ✅；州城榜房→`bangfang` 🎨 |
| 46 當堂默寫 | xu-yan、s01-chu-zhifu→`chuzhifu` 🎨、`fengxuezheng` 🎨、`weixun` 🎨、tang-xiaotang、qin-shuang、`chengshanzhang` 🎨 | 州府大堂→`zhoufu-tang` 🎨（開場擊鼓在州府門口→`xianya` ✅） |
| 47 畫出來 | xu-yan、`weixun` 🎨、`fengxuezheng` 🎨、`chuzhifu` 🎨、`chengshanzhang` 🎨、tang-xiaotang、xitong | 州府大堂→`zhoufu-tang` 🎨；州府後堂→`zhoufu-houtang` 🎨 |
| 48 爹還活著 | xu-yan、`chuzhifu` 🎨、tang-xiaotang、`dutie` 🎨、qin-shuang、`xudalang` 🎨（魏家管家→小角色 `weiguanjia`） | 州府後堂→`zhoufu-houtang` 🎨；州城客棧院子→`zhou-kezhan-yuan` 🎨；州城暗巷→`xiaoxiang` ✅ |
| 49 放榜 | xu-yan、tang-xiaotang、qin-shuang、s01-zhou-yuanwai→`zhouyuanwai` 🎨、`xudalang` 🎨、xitong | 州城城牆→`chengmen` ✅；州城大街→`zhou-jie` 🎨 |
| 50 拿下秦霜 | `zhouyuanwai` 🎨、xu-yan、qin-shuang、tang-xiaotang、`xudalang` 🎨、`chengshanzhang` 🎨、xitong | 州城客棧→`zhou-kezhan` 🎨（宴席、樓梯）／`kezhan` ✅（給玉佩） |
| 51 跟他們走 | qin-shuang、xu-yan、tang-xiaotang、a-ling→`aling` ✅、xitong | 州城客棧→`zhou-kezhan` 🎨；州城長街→`zhou-jie` 🎨 |
| 52 真印假印 | a-ling、xu-yan、tang-xiaotang、`chuzhifu` 🎨、`dutie` 🎨、xitong | 州城客棧→`zhou-kezhan` 🎨／`kezhan` ✅；州府→`zhoufu-tang` 🎨；知府後宅→`zhoufu-houtang` 🎨 |
| 53 渡口截車 | a-ling、xu-yan、wang-erniu→`erniu` ✅、qin-shuang、s01-deng-yasi→`dengyasi` 🎨、xitong | 州城北門官道→`guandao` ✅；北邊渡口淺灘→`beidu-qiantan` 🎨 |
| 54 她第一次哭 | qin-shuang、`dengyasi` 🎨、a-ling、xu-yan、xitong | 北邊渡口淺灘→`beidu-qiantan` 🎨；河灘篝火→`hetan` 🎨 |
| 55 鎖起來 | xu-yan、a-ling、qin-shuang、tang-xiaotang、qian-yuanwai→`qianyuanwai` ✅、s01-han-bo→`hanbo` ✅、xu-xiaohe→`xiaohe` ✅、xitong | 河灘篝火→`hetan` 🎨；柳溪村口→`cunkou` ✅；許家院子→`xujia-yuan` ✅ |
| 56 奉旨接人 | a-ling、xu-yan、qin-shuang、tang-xiaotang、wang-erniu、s01-leng-tie→`lengtie` 🎨、xitong | 許家院子→`xujia-yuan` ✅；柳溪打穀場→`dagu-chang` ✅；柳溪瞭望台→`liaowangtai` 🎨；柳溪村口→`cunkou` ✅ |
| 57 御膳房的問題 | a-ling、`lengtie` 🎨、xu-yan、qin-shuang、tang-xiaotang、wang-erniu、xitong | 柳溪村口→`cunkou` ✅；柳溪村道→`cundao` 🎨；柳溪糧倉→`gucang` ✅ |
| 58 開閘 | xu-yan、`lengtie` 🎨、qin-shuang、a-ling、tang-xiaotang、wang-erniu、xitong | 柳溪糧倉→`gucang` ✅（倉前窄巷→`cundao` 🎨）；柳溪水車邊→`shentan` ✅ |
| 59 謝謝你 | xu-yan、a-ling、qin-shuang、tang-xiaotang、xu-xiaohe、wang-erniu、s01-shi-mujiang→`shimujiang` ✅、s01-han-bo→`hanbo` ✅、`dutie` 🎨、xitong | 許家院子→`xujia-yuan` ✅ |
| 60 長公主殿下 | xu-yan、a-ling、qin-shuang、tang-xiaotang、xu-xiaohe、wang-erniu、s01-hu-xianling→`huxianling` ✅、s01-chang-gonggong→`changgonggong` 🎨、xitong | 許家院子、許家門口→`xujia-yuan` ✅ |

## 還要畫的圖（25 張）

`assets/refs-dh/`，畫好才能做那幾集的 Ref2VA（缺圖時 `ref2manifest.mjs` 會列為 missing）：

- 定妝照（10）：`xudalang-portrait-t1.png`、`zhouyuanwai-portrait-t1.png`（e042 起就缺）、`chengshanzhang-portrait-t1.png`、
  `fengxuezheng-portrait-t1.png`、`weixun-portrait-t1.png`、`dutie-portrait-t1.png`、`chuzhifu-portrait-t1.png`、
  `dengyasi-portrait-t1.png`、`lengtie-portrait-t1.png`、`changgonggong-portrait-t1.png`。
- 場景（15）：`set-zhou-kezhan-t1.png`、`set-gongyuan-t1.png`（e042 起就缺）、`set-shuyuan-zhai-t1.png`、`set-haoshe-t1.png`、
  `set-mifeng-fang-t1.png`、`set-bangfang-t1.png`、`set-jiusi-t1.png`、`set-zhou-jie-t1.png`、`set-zhoufu-tang-t1.png`、
  `set-zhoufu-houtang-t1.png`、`set-zhou-kezhan-yuan-t1.png`、`set-beidu-qiantan-t1.png`、`set-hetan-t1.png`、
  `set-liaowangtai-t1.png`、`set-cundao-t1.png`。

外貌與場景的英文描述在 `cast.json`；畫法照 `hailuo/refs-dh-jobs*.json`（定妝照 3:4 正面半身、深灰藍漸層背景；場景 16:9、沒有人物、不能有字）。
最急的是第 43 集（程山長、馮學正、魏珣、書齋、號舍、彌封房、貢院）與州城客棧（第 44、45、50、51、52 集都要）。
