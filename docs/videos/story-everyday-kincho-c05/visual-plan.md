# C05 金鳥蚊香｜非付費逐鏡畫面計畫

狀態：依 [script.md](script.md) 88 句旁白編成 **65 個暫定畫面狀態**；此稿未經站主逐鏡核准，也沒有生成、下載或購買任何圖片、配音、配樂。逐句查核或敘事盲讀一旦改稿，必須同步重排對應畫面、重新測插圖占比及鉤子間距。下表一列是一個視覺狀態，`shot` 為將來可用 MiniMax `image-01` 生成的插圖意圖，`card` 是後製文字卡；現階段只描述，不送模型。

## 固定畫面與聲音規則

- 作品仍是 `kind: story`、`story-` slug，視覺沿用奇聞檔案局：`look: {"preset":"cute-mystery"}`，不加 `style` 或 `negative`。一人一動作、景別與光線輪替；插圖只表示旁白所講的物件關係，**不是** 1890、1895、1902 年的照片或當事人肖像。年代以後製文字標注，不讓插圖畫可讀文字。
- 圖片提示詞只用一般物件與匿名人物，不放「金鳥／KINCHO」、真人姓名、特定商品／商標、包裝上的圖樣、可讀字、館藏照片或版權角色。木模、擠出機與成對螺旋都畫成**示意**，不描摹博物館禁轉載的影像。`card` 可寫品牌、年份、數字與來源；來源留在後製卡或說明欄，不讓旁白反覆朗讀出處。
- 暫定 65 狀態：`shot` **50**、`card` **15**，插圖狀態占 **76.9%**。這只是狀態數比率；實際規則看**畫面時間**，須在核准旁白時間軸上重新計算達到至少 70%，且任兩張插圖之間最多三張卡。下表最多連續兩張卡。單一畫面狀態不超過 8 秒；兩句同鏡若實測超時，先拆成有新資訊的畫面，不拉長靜圖。
- 0:00 首句直接入場，冷開場 H01–H08 後插入頻道 5 秒片頭；正文每 30–45 秒有可回收鉤子。21 秒 `v4-endscreen` 片尾帶頻道與可點連結；旁白不預告下一支。繁中 CC 可關閉、不燒在畫面；英／日／韓成片後由站主手選。配樂設定固定 `light, curious, a little mysterious, no vocals`、`gain_db: -20`、`duck_db: -10`，本階段不合成。
- `shot` 的英文欄是**畫面意圖**，不是已核准的最終生成 prompt。英文避免畫風字、品牌字與年代數字；光線只用柔和白天、陰天或檯燈，夜景少於一半。相鄰鏡的推、移、俯仰方向在將來 `video.json` 寫定時輪替，避免三張連同運鏡。
- 冷開場的物件稍後回收：V25 可重用 V04 的木模圖並換裁切，V42 可重用 V05 的雙條設備圖，V50 可重用 V06 的成對螺旋圖，V64 可重用 V07 的對照圖。若正式逐鏡稿要生成新圖，須先解釋新視角帶來的資訊，再列入整支報價；此處的 50 個 `shot` 是畫面狀態數，**不是**已核准圖片張數。

## 1｜冷開場：一根先熄掉（H01–H08）

| 畫面 | 句 | 類型 | 畫面意圖／後製字卡 | 驗收重點 |
| --- | --- | --- | --- | --- |
| V01 | H01 | shot | Medium shot at a plain home table at dusk, one anonymous resident lighting a thin straight incense rod, soft lamp light. | 情境示意；不扮演上山本人。 |
| V02 | H02–H03 | card | `早期直條：約 20 公分／約 40 分鐘`；來源：金鳥技術遺產頁。 | 數字是原廠回顧，不與當代七小時混寫。 |
| V03 | H04 | shot | Close-up at the same table after dark, one anonymous resident looking at a short burnt-out rod, gentle lamp light. | 沒有真實夜晚紀錄；不畫蚊蟲受害者。 |
| V04 | H05 | shot | Close-up at a neutral archive table, one anonymous curator examining a plain wooden spiral-shaped trial mold, soft grey light. | 木模為原創示意，不臨摹館藏照片或暗示公開展出。 |
| V05 | H06 | shot | Medium shot in a generic workshop, one anonymous maker holding two previously extruded plain strips beside an unmarked machine, mild window light. | 此設備晚於 1902；不畫成機器同時擠出兩條。 |
| V06 | H07 | shot | Close-up at a present-day plain table, one anonymous hand holding two joined spiral incense pieces, soft daylight. | 成對但未點燃、無商標。 |
| V07 | H08 | shot | Wide shot of the same plain table, one anonymous resident comparing a short straight rod and a paired spiral without touching them, overcast light. | 只作問題構圖，沒有假對照試驗。 |

## 2｜直條上市：材料有了，時間不夠（O01–O16）

| 畫面 | 句 | 類型 | 畫面意圖／後製字卡 | 驗收重點 |
| --- | --- | --- | --- | --- |
| V08 | O01 | shot | Wide shot in a generic seed-trading room, one anonymous merchant placing an unmarked exchange note on a desk, soft daylight. | 1885 是交換約定，種子隔年才抵達；不畫真實人物肖像。 |
| V09 | O02–O03 | shot | Close-up at an unmarked desk, one anonymous hand spilling small pale seeds from a blank paper envelope, soft window light. | 種子形態只示意，不標假產地。 |
| V10 | O04 | card | `1887｜首次收成`；來源：金鳥年表。 | 日期從公司年表，不冒稱產量。 |
| V11 | O05 | shot | Medium shot in a simple lodging room, one anonymous traveler examining a plain unlit incense stick, warm lamp light. | 不畫兩人同框或對話、無真人臉復原。 |
| V12 | O06–O07 | shot | Close-up at a generic craft bench, one anonymous maker handling a small plain bamboo tube beside a bowl of dark powder, mild side light. | 1888 年年表記舶來粉與竹筒；這仍是示意，並非當年現場重建。 |
| V13 | O08 | card | `1890｜直條蚊香上市`；來源：金鳥年表。 | 不加世界第一。 |
| V14 | O09 | shot | Medium shot in a plain home, one anonymous resident setting a straight incense rod in a simple dish, soft daylight. | 不畫特定商品包裝。 |
| V15 | O10–O11 | shot | Close-up at the same table, one anonymous hand setting several separate thin rods beside one short burnt rod, soft lamp light. | 多根是原廠回顧；不暗示使用安全。 |
| V16 | O12 | shot | Medium shot at a generic shipping bench, one anonymous packer lifting a fragile plain straight rod from an unmarked box, overcast light. | 折斷是原廠回顧，不能畫實測破損率。 |
| V17 | O13–O14 | shot | Wide shot between a bedside table and an unmarked shipping box, one anonymous resident looking from short rods to a closed carton, soft grey light. | 概念對照，不暗示同一個史實場景。 |
| V18 | O15 | shot | Top-down close-up of one anonymous hand placing a long plain straight strip beside a small round dish on a blank table, mild daylight. | 僅幾何示意；避免虛構精確長度。 |
| V19 | O16 | shot | Top-down close-up of a long plain unlit strip resting in a loose spiral shape beside a round dish on a blank craft bench, soft daylight. | 僅作幾何示意；不畫 1895 年誰如何試作。 |

## 3｜想出螺旋，木模卻卡住（I01–I16）

| 畫面 | 句 | 類型 | 畫面意圖／後製字卡 | 驗收重點 |
| --- | --- | --- | --- | --- |
| V20 | I01 | card | `金鳥後來的記述：構想歸於妻子ゆき`；來源：金鳥年表與博物館登錄。 | 歸屬限公司／館藏後年記述；不給真人肖像。 |
| V21 | I02–I03 | shot | Medium shot at a neutral worktable, one anonymous maker laying a thicker flexible plain strip across a small desk, soft daylight. | 「更粗、更長」示意，不冒稱妻子實際動作。 |
| V22 | I04 | shot | Top-down close-up at the same worktable, one anonymous hand curving the plain strip inside a small round outline, soft window light. | 不加入錯誤箭頭或可讀字。 |
| V23 | I05–I06 | shot | Close-up on a plain table, one anonymous hand tracing the full unlit spiral path from edge toward center, diffuse light. | 說明路徑，不畫殺蚊效率倍增。 |
| V24 | I07 | card | `1895｜螺旋試作開始`；來源：金鳥年表。 | 不是上市卡。 |
| V25 | I08 | shot | Reuse V04 illustration with a closer crop on the wooden mold and the anonymous curator's hand. | 同一物件回收；新裁切仍不能冒充館藏圖。 |
| V26 | I09–I10 | shot | Close-up at a generic workbench, one anonymous maker examining a simple wooden spiral trial mold beside blank raw material, soft side light. | 不斷言木模有兩片；「擬填料成形」只為示意。 |
| V27 | I11 | shot | Wide shot of a plain bench, one anonymous maker looking at a single rough trial shape beside an empty tray, grey daylight. | 不以單一失敗事件冒充記錄。 |
| V28 | I12–I13 | card | `試作品；不適合大量生產`；來源：國立科學博物館登錄、金鳥技術頁。 | 館藏文字改寫，勿複製圖片或長文。 |
| V29 | I14 | shot | Medium shot at a neutral production table, one anonymous maker placing an unused wooden mold aside, soft window light. | 情境插畫，不暗示真實拒用時刻。 |
| V30 | I15 | shot | Close-up at an archive desk, one anonymous hand separating a plain spiral sketch from an unmarked empty shipping box, soft lamp light. | 形狀與商品兩件事，無偽造文件。 |
| V31 | I16 | shot | Wide shot of five blank calendar pages laid along a table, one anonymous hand sliding the last page forward, soft daylight. | 年份由後製卡疊加，模型不畫字。 |

## 4｜申請與上市相隔兩年（E01–E20）

| 畫面 | 句 | 類型 | 畫面意圖／後製字卡 | 驗收重點 |
| --- | --- | --- | --- | --- |
| V32 | E01–E02 | card | `1900｜公司年表：發明專利申請`；來源：金鳥年表。 | **申請**，不寫授權、發明人欄或專利號。 |
| V33 | E03–E04 | card | `1902｜螺旋產品上市`；來源：金鳥年表。 | 與 1900 申請分兩卡；卡片不超連三。 |
| V34 | E05 | shot | Close-up at a plain table, one anonymous hand setting a trial wooden mold beside an unmarked spiral product, soft daylight. | 七年由後製文字標示，不讓兩件物件冒充同時照片。 |
| V35 | E06 | shot | Medium shot at a neutral archive desk, one anonymous researcher pausing between two separate blank object folders, gentle lamp light. | 僅表示本次物件資料缺完整 1902 工序；不暗示全部史料缺失或被毀。 |
| V36 | E07–E08 | shot | Wide shot in a neutral exhibit room, one anonymous curator standing beside an unmarked hand-winding extrusion device, soft daylight. | 這是後來保存的設備示意，不能充當 1902 年量產紀錄。 |
| V37 | E09 | shot | Close-up at a neutral exhibit label area, one anonymous curator pointing beside a plain extrusion device, soft window light. | `約 1910 起` 由後製標字，不讓模型畫字。 |
| V38 | E10 | card | `後年設備 ≠ 1902 年上市工法紀錄`；來源：金鳥技術頁。 | 明確區隔有物件年代與未知的上市工序。 |
| V39 | E11 | shot | Close-up in a generic workshop, one anonymous worker guiding one plain narrow strip out of an unmarked extruder, soft daylight. | 不畫今日壓片打型。 |
| V40 | E12–E13 | shot | Medium shot at a workbench, one anonymous worker winding a narrow strip by hand while a plain wooden mold sits far aside, diffuse light. | 兩種年代工法對照，用後製示意標籤。 |
| V41 | E14 | shot | Wide shot in a modern archive room, one anonymous researcher looking between two unmarked object silhouettes on separate shelves, soft grey light. | 不聲稱中間只有兩件設備。 |
| V42 | E15–E16 | shot | Reuse V05 illustration with a closer crop on the maker's hands holding two separate extruded strips. | 同一設備回收；不暗示機器同時擠出。 |
| V43 | E17 | shot | Medium shot at a generic workbench, one anonymous worker winding two plain strips into one paired spiral, mild daylight. | 兩條合盤而非兩條同點。 |
| V44 | E18 | card | `1940｜公司年表：自動打型機完成`；來源：金鳥戰前年表。 | 只表示完成，不說當年全面替代手卷。 |
| V45 | E19 | shot | Medium shot in a generic older workshop, one anonymous worker still hand-winding two plain strips at an extrusion bench, soft daylight. | 手卷設備據記載用到約 1957 年；不畫 1940 年單一工廠實況。 |
| V46 | E20 | shot | Wide shot at a neutral shipping desk, one anonymous packer holding a paired spiral above a blank carton, overcast light. | 問運送，不捏造折損率。 |

## 5｜成對運送，單卷使用（T01–T12）

| 畫面 | 句 | 類型 | 畫面意圖／後製字卡 | 驗收重點 |
| --- | --- | --- | --- | --- |
| V47 | T01 | shot | Medium shot at a plain shipping bench, one anonymous packer lifting a paired spiral beside an unmarked box, soft grey daylight. | 雙卷用途不與慢燃混成一個機制。 |
| V48 | T02–T03 | card | `原廠說法：雙卷減少運送折斷、降低運輸成本`；來源：金鳥技術頁。 | 無測得降幅，不畫任何百分比。 |
| V49 | T04–T05 | shot | Top-down at a present-day neutral table, one anonymous hand arranging a single unlit spiral beside a joined pair and a plain carton, soft light. | 單圈／雙卷作功能對照；T05 已切到現行用法，不畫實測。 |
| V50 | T06–T07 | shot | Reuse V06 illustration with a closer crop on the unlit joined pair. | 同一成對物件回收；不能畫成同時點燃。 |
| V51 | T08 | shot | Medium shot at the same home table, one anonymous resident gently separating a paired spiral into single pieces, soft daylight. | 拆成單卷，形狀清楚。 |
| V52 | T09–T10 | card | `從中心輕按，再拆成單卷；勿由外側硬拉`；來源：金鳥現行 Q&A。 | 只作現行使用步驟，避免生成模型畫錯手指。 |
| V53 | T11 | shot | Close-up at a plain storage shelf, one anonymous hand setting an unlit joined pair into an unmarked box, soft daylight. | 保管與使用是兩個時刻。 |
| V54 | T12 | shot | Medium shot at a home table, one anonymous resident watching one separated spiral burn slowly in a simple dish, gentle lamp light. | 不以此畫面證明密度實驗。 |

## 6｜同一輪廓，製法與燃燒條件變了（N01–N16）

| 畫面 | 句 | 類型 | 畫面意圖／後製字卡 | 驗收重點 |
| --- | --- | --- | --- | --- |
| V55 | N01–N02 | shot | Wide shot in a generic modern factory, one anonymous worker guiding a plain flat sheet from an unmarked extruder, soft overhead light. | 現行製程先混料，再經擠出機成片；非舊時工廠。 |
| V56 | N03 | shot | Close-up at a generic machine, one anonymous worker lifting a blank spiral cutout from a plain sheet, diffuse light. | 先打型後乾燥，不混作 1902 工法。 |
| V57 | N04 | shot | Medium shot in a neutral exhibit room, one anonymous curator placing a hand-wound silhouette beside a stamped silhouette, soft daylight. | 兩時代比較卡由後製上字。 |
| V58 | N05–N06 | card | `現行一般規格：約 75 公分／約 7 小時`；來源：金鳥現行 Q&A。 | 不倒推 1902 年，不作獨立性能實驗。 |
| V59 | N07 | card | `現行另有：約 3 小時／約 12 小時`；來源：金鳥現行 Q&A。 | 尺寸不同，不暗示同一卷改轉速。 |
| V60 | N08 | shot | Medium shot at a plain home table, one anonymous resident adjusting an open window beside an unlit spiral in a dish, soft daylight. | 只表達環境影響，安全指示另依實際包裝。 |
| V61 | N09–N10 | shot | Close-up at a neutral craft bench, one anonymous worker examining the compact cross-section of a plain incense strip, mild side light. | 是氧氣／密度的抽象示意，不畫虛構對照試驗。 |
| V62 | N11 | shot | Medium shot at a simple home table, one anonymous resident observing a slowly smoldering single spiral, gentle lamp light. | 不畫誇大的殺蚊或健康效果。 |
| V63 | N12–N13 | card | `早年直條：以除蟲菊為原料；現行金鳥工廠說明：合成擬除蟲菊酯`；來源：金鳥蚊香解說與工廠頁。 | 不把成分差異說成效力比較；不推及所有品牌。 |
| V64 | N14 | shot | Reuse V07 comparison illustration with a slower crop toward the short rod and paired spiral. | 回收開場的同一圖，後製卡點出長度與運送兩個答案。 |
| V65 | N15–N16 | shot | Medium shot at the same table, one anonymous resident looking curiously between one long single spiral and a joined pair near a blank carton, soft daylight. | 後製留言問「久燃／完整送達」；片尾另留可點連結，不畫字。 |

## 逐鏡審核清單（非旁白）

1. 獨立逐句查核對 88 句每句確認來源、年代、歸屬；若刪句，該鏡一起刪或重新映射。兩位盲讀者只讀旁白，不先看 Treatment／畫面提示。
2. 核准逐字稿後才把本表轉成 `video.json`，用實測旁白重切 5–8 秒狀態，驗正文插圖畫面時間 ≥70%、連續卡片 ≤3、至少八個回收鉤子、冷開場 30–60 秒、正文純旁白至少八分鐘；不合就縮短或換題／向站主說明，不補虛構場景。
3. 付費前逐張數與全片 TTS、圖片、配樂一次估價，連上限一起報站主另行核准。前集 US$25 額度不得移轉到 C05。核准前不送出任何模型生圖或音訊請求。
