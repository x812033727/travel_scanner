# B18 v2｜靜態插畫與全片成本前檢

**歷史估算，不是現行 B18 分鏡或預算核准。**本表依舊逐字稿把 1978 年寫成權利期滿；現行資料列及[法院 PDF 分源審查](preproduction-20261016/B18-court-pdf-split-candidate-20261017/independent-review-20261017.md)以特定第 579776 號權利 1972 年期滿為準，1978 年只作來源分歧註記、不口播。付費前須依實際 85 景、88 句及正式 TTS 重新核算。

狀態：**開拍前排程假設，尚未生成插畫、配音、配樂或成片，也未呼叫付費服務。**依據已通過獨立文字審查的 [`scripts/B18.md`](scripts/B18.md)，SHA-256 `5326bd6633ad69931fe542badd6cddd2378324ff0bcc4b0f05652941642dc724`。實際逐鏡表要依本稿 TTS timeline 對齊後鎖定；正文若改字，本表張數與估價重算。

## 聲畫節奏與鏡數

正文預估 9:06，第一章後接頻道既有 **5 秒**片頭，末三句後接既有 **21 秒**片尾；成片粗估 9:32。全片只用 MiniMax `image-01` **靜態圖**、慢移／輕推拉與後製字卡；正文 `visual: "still"`，生成影片 clip **0 鏡**。固定 `look: {"preset":"cute-mystery"}`，不在 prompt 加畫風詞、`style` 或 `negative`。插畫是幫旁白理解機制的卡通示意，不充作當年照片、原機復原或真人肖像。

| 腳本段落 | 估時 | 插畫 `shot` | 資訊卡 | 主要可見動作與剪點 |
| --- | ---: | ---: | ---: | --- |
| 第一章 H01–H03 | 0:38 | 7 | 1 | 匿名參觀者看無標籤瓶子前進 → 壽司盤到轉角；三個未解節點由旁白依 1958／1970／1978 順序說，不提前揭曉。 |
| 第二章 O01–O04 | 1:22 | 14 | 2 | 立食小店的單人遞盤、忙碌的師傅、工廠直線與吧台轉彎之差；只在此處標早期 **20 日圓**。 |
| 第三章 I01–I04 | 1:34 | 16 | 3 | 盤子在轉角失穩 → 兩種**分開、有來源標示**的紙片靈感示意 → 扇形板與 1957 年試作；轉角機構用一般化示意。 |
| 第四章 E01–E05 | 1:55 | 20 | 3 | 1958 年首店取盤與 **50 日圓**、1962 年實用新案、1970 年萬博排隊及桶裝 **300 日圓套組**；三個價位絕不放進同店同年代畫面。 |
| 第五章 T01–T04 | 2:34 | 26 | 4 | 萬博曝光／加盟 → 單人用給茶裝置 → 1978 年期滿後新經營者、直線帶與不同盤色；用接續鏡頭顯示多因素，不拍成期滿一瞬全國開店。 |
| 第六章 N01–N03 | 1:03 | 8 | 4 | 字典詞條、**1985 年製**後期機器與早期魚鱗板分鏡；2022 實績、2023 當時預估各有日期；末三句固定同一張圖，接片尾。 |
| **正文合計** | **9:06** | **91** | **17** | **108 個視覺槽；插畫 91／108＝84.3%**。 |

正文 `shot` 比例以逐鏡欄位重算，必須 ≥70%；片頭、章名、片尾不計分母。17 張卡片是本版上限規劃，不是可用來填時間的空位：每張只留一個必要年代、價位、名稱、來源或統計，兩張插畫間最多 **3 張**卡，目標為一次只接一張。圖片若被退，優先修 prompt 或重用同章已過圖片；換成卡片仍須重跑比例和連卡檢查。後製字幕、數字與來源均不可叫 MiniMax 在圖片裡畫字。

## 代表鏡頭的 prompt 草案

下列只示範**景別、時地、單一匿名人物的一個動作、焦點、中性光線**；同段的遠、中、特寫和冷暖室內光需交錯。提示詞裡的人不命名白石義明、白石博志或真實工廠／店面；真人名字、年代與出處由後製文字處理。生成後只退畫風漂移或與旁白／來源矛盾的圖。

| 對位 | 交給 `image-01` 的單鏡 prompt 草案 | 後製／來源界線 |
| --- | --- | --- |
| H01 工廠起點 | `Medium shot in a generic Japanese bottling room in the late 1940s, one anonymous visitor facing the camera while watching plain glass bottles move along a straight conveyor, bottles as the focus, soft overcast window light from the left.` | [0][1][2] 只示意看見輸送帶；不指定啤酒廠名稱，也不畫同一台機器搬進壽司店。 |
| O03 遞盤瓶頸 | `Medium shot inside a small standing sushi counter in late 1940s Japan, one anonymous sushi cook facing the camera while reaching out with one plain sushi plate, the plate as the focus, soft indoor daylight.` | [0][2] 只有一個人在遞盤；不捏造精確排隊時間或工時。20 日圓留給此章卡片。 |
| I02 說法 A | `Close medium shot at a plain tabletop in 1950s Japan, one anonymous child facing the camera while spreading a fan of simple playing cards, the cards as the focus, gentle cloudy daylight.` | **[0] J-Net21「孩子攤撲克牌」版本**；後製標來源，不宣稱確切現場。 |
| I02 說法 B | `Close medium shot at a separate plain tabletop in 1950s Japan, one anonymous adult facing the camera while spreading a fan of blank business cards, the cards as the focus, soft desk-lamp light.` | **[2] 發明協會「攤名片」版本**；與 A 用不同畫面、不同出處卡，不剪成同一天的連續動作，也不據此判唯一版本。 |
| I03 轉彎解法 | `Close medium shot at a simple workshop bench in 1950s Japan, one anonymous craft worker facing the camera while placing a single fan-shaped plate beside a curved conveyor corner, the plate as the focus, neutral workshop light.` | [0][1][2] 扇形板示意；「ウロコ」由後製卡片加，不能宣稱尺寸／材質精確復原。 |
| E05 萬博客流 | `Medium shot in a generic exhibition food counter around 1970, one anonymous server facing the camera while placing a plain sushi tub on a moving belt, the tub as the focus, soft diffused hall light.` | [0] 只示意萬博賣 **300 日圓套組**的出餐；不畫真實展館、品牌標誌或 1958 年單盤價。 |
| T01a 給茶 | `Medium shot at a generic conveyor sushi counter in the early 1970s, one anonymous guest facing the camera while pressing a plain tea cup toward a simple tea dispenser, the cup as the focus, gentle indoor light.` | [0][2] 設備與操作示意，不宣稱每家店都有同款機器。 |
| T03 新路線 | `Medium shot in a generic later sushi restaurant, one anonymous kitchen worker facing the camera while setting one sushi plate on a straight conveyor leading from the back kitchen, the straight belt as the focus, soft indoor daylight.` | [2] 只代表**有些**新業者採直線帶，與早期必須轉彎的吧台對照。 |

每張檢查主體、解剖、文字、畫框、畫風與對位事實；不能因卡通多一個無關小物就重畫。標題／縮圖可另行設計，但不把示意插畫說成史料。兩個靈感版本、20／50／300 日圓三個價位、1970 萬博、1978 期滿、1985 年製與 2021 年認定是抽樣審片的必查鏡頭。

## 全片 US$25 停損草算

此表是**預算分配假設，不是供應商報價或可開工證明**。2026-10-15 唯讀查得 [MiniMax 官方價格](https://platform.minimax.io/docs/pricing/overview)的 `image-01` 為 **US$0.0035／張**；[奇聞檔案局 skill](../../../.agents/skills/curio-episode/SKILL.md)舊案「含評審約 US$0.0135／張」僅供期望值參考，非 judge 費率或硬上限。Gemini 評審按[官方模型價格](https://ai.google.dev/gemini-api/docs/pricing)與實際 token 計，語音依正式路由與帳單計。v4 片頭／片尾重用，clip 為零，不預設它們另有供應商生成費。

| 項目 | 試算用量與可動用額度（US$） |
| --- | --- |
| `image-01` | 91 張首畫＋最多 27 次重畫＝**118 次**，按目前官價 **0.413**；首畫 91 次為 0.3185。 |
| 圖像 judge | 118 張各一次＋最多 12 次有因重審＝**130 次**；先暫列 **3.00**，實際每次按輸入／輸出 token 結算，不能把 3.00 當保證。 |
| 撰稿、改稿、事實／敘事模型與 Jev | 包含必要重試，暫列 **6.00**；免費本機文字審查不冒充服務成本。 |
| 台灣口音單人 TTS 與有證據的局部重錄 | 暫列 **3.00**；實際語音模型、字數與每次音檔結果需逐次登帳。 |
| 轉錄／字幕對齊 | 暫列 **2.00**；若發生其他付費字幕或語言步驟也從本片總額扣。 |
| 可選配樂 | 至多一條、先取得確定上限，暫列 **1.00**；既有曲可用且權利清楚時不生成。 |
| 未列明付費步驟與波動緩衝 | **9.587**；只作本片總額餘裕，不授權額外鏡頭或無界重試。 |
| **本片總額硬停損** | **25.000**，含所有付費項目與重試。 |

此用量按舊案約 US$0.0135／張推，118 次圖像加一次評審的**期望**約 US$1.593，另 12 次重審仍需按實際 token 另計；這與上表的 US$3.413 圖像＋judge 暫列額度用途不同。若新模型輸入、失敗重試或語音成本較高，刪減非必要步驟或停工重排，絕不以「約 US$1.593」宣稱全片能在 US$25 完成。

正式機的每片共用美元預留閘仍在草案 PR #1508，不能用目前 `max_usd_per_video=US$200` 的**媒體估算**代替。該草案的 Gemini 3.8 Flash judge 單次派發前最高預留 **US$1.032192**，回覆後按實際 token 結算；130 次評審不可同時當作已付小額費用。只在 A01 試作的聲畫、帳本與站主驗收及 B18 正式機／供應商唯讀前檢完成後，逐鏡串行核「已花＋未結預留＋下一次最壞預留 ≤ US$25」；不確定的請求維持預留，不重複派發。若不能證明本片所有付費路徑受同一上限、不能取得可用額度，或剩餘款不足下一次預留，**在下一次付費呼叫前停住**，留下帳本與已完成媒體供站主判斷。本文沒有授權匯入、部署、生成、上傳或發布。
