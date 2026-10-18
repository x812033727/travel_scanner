# A01 v2｜靜態插畫與成本前檢

2026-10-15；**製作規劃，沒有付費呼叫或生成媒體**。以已通過[逐字稿獨立文字審查](scripts/reviews/A01.md)的 [`scripts/A01.md`](scripts/A01.md) 為聲音底本，SHA-256 `f91816021ebea28e1957199a5c73ccc588748e988730efc92e0486d09d5215c6`（口播 59 行、2,712 漢字與數字；稿面正文約 9:02，須以實際 TTS timeline 重排）。兩份來源包與文字審稿只核准敘述，不能當作插畫或成片驗收。

## 聲畫容量

全部正文鏡頭用 `visual: "still"`、MiniMax `image-01`、`look: {"preset":"cute-mystery"}`，片頭接首章後的既有 5 秒動畫，末三句後接既有 21 秒片尾；**生成影片 clip 為 0**。下表 95 張是分鏡容量，不是已產生的檔案。依稿面估時共 106 個正文畫面，平均每畫面約 5.1 秒；語音完成後按句子邊界調整切點，不能拉長空白或慢播補片長。

| 章／對應旁白 | 稿面時間 | 插畫 `shot` | 數字／來源卡 | 要看見的動作及伏筆回收 |
| --- | ---: | ---: | ---: | --- |
| 1 開場 H01–H07 | 約 0:37 | 8 | 1 | 匿名旅客提兩只箱、工人推輪板；1928→1970→1987 只預告，年份由後製卡寫。 |
| 2 前案 O01–O13 | 約 2:07 | 22 | 2 | 家人替箱子裝嬰兒車輪與木拉把、旅途搬運、1943／1946 專利、薩多做四輪繩拖樣品；卡片限日期與專利號。 |
| 3 通路 M01–M11 | 約 1:36 | 16 | 2 | 樣品被退、一般化店員試拉、櫃位展示；1970-10 上架與 1972-04 核准分成不同卡，不能畫作同一時刻。 |
| 4 使用路線 T01–T08 | 約 1:33 | 16 | 2 | 一位旅客穿過抽象航站、輪子在箱蓋／箱身下著地、繩拖與提把兩種搬法；專利文字只在後製卡呈現。 |
| 5 直立改良 P01–P12 | 約 1:50 | 20 | 2 | 安檢拆車的麻煩、車庫螺絲原型、直立兩輪拉桿、機組員在通道拉箱；卡片只標 1987、1989／1991。 |
| 6 四輪與收束 N01–N05、E01–E03 | 約 1:20 | 13 | 2 | 一位旅客站著側移無商標四輪箱，遇到需提起的台階，再回到出發的旅客；1997／2000 年份與來源作卡，末三句不再插年表。 |
| **合計** | **約 9:02** | **95** | **11** | **95／106＝89.6% 插畫**；規劃卡片之間至少一張插畫，最長連續卡片 **1 張**。 |

系列底線是正文插畫至少 70%、兩張插畫之間連續卡片最多 3 張；片頭、章名、片尾不算正文。即使 20 張原訂插畫改為卡片，也只剩 75／106＝70.8%；因此失敗鏡頭先縮簡 prompt 或重用**同章已過評審的相關插畫**，不能把 25 次重畫額度全變成文字卡。`curio-` slug 的 lint 會自動擋比例，但本片 slug 是 `story-rolling-suitcase-v2`，定稿 `video.json` 還需人工計數和逐鏡檢查。逐鏡 judge 後再看連續播放：景別（遠／中／特寫）、位置、緩慢推近／橫移／停留交替；同一運鏡不要連續三張。1K 插畫避免大幅放大，鏡頭縮放以既有可愛解說設定為準。

## 代表鏡頭 prompt（只描述畫面，不寫畫風）

每張只畫**一位匿名人物、一個動作**及當句的焦點物件；提示詞不寫人物姓名、品牌商標、可讀字、專利內容或 `cartoon/chibi/navy` 等已在 `look` 裡的畫風詞。使用柔和頂燈、陰天散射光或中性檯燈，不用戲劇性聚光、正午強光或飽和綠色植物。這些是與來源相關的**情境插畫**，不主張重建真實機場、百貨辦公室或當事人容貌；年份、姓名、專利號與來源交給後製字卡。

| 對應行 | 送給 `image-01` 的構圖內容示例 |
| --- | --- |
| H01 | `Medium shot in a generic airport corridor, one anonymous traveler facing three quarters toward camera while lifting two plain suitcases, a low wheeled platform off to one side, soft overhead light, blank signs.` |
| O02 | `Medium shot in a simple family workroom, one anonymous young traveler fastening two small reclaimed stroller wheels to a plain suitcase, a wooden pull handle on the table, diffuse window light from the left, a blank wall.` |
| M05 | `Medium shot in a generic department-store office, one anonymous employee pulling a plain four-wheeled suitcase by a rope across the floor, a blank display stand nearby, soft ceiling light.` |
| T05 | `Wide shot in a generic airport concourse, one anonymous traveler pulling a plain four-wheeled suitcase by a rope along a long passage, blank direction panels, diffused daylight through high windows.` |
| P02 | `Medium shot in a plain home garage, one anonymous maker fastening a small metal trolley to a hard-shell suitcase on a workbench, soft neutral work light, blank shelves.` |
| N02 | `Medium shot in a narrow generic terminal passage, one anonymous traveler guiding a plain upright four-wheeled suitcase sideways, soft ceiling light, blank signs.` |

樣張的既定系列畫風已選定，毋須為每張圖逐次要求批准；先完成逐鏡清單與整集報價，再按已鎖範圍一次製作。每張圖評審通過就收，只有與旁白事實矛盾或漂成照片、3D、油畫、黑框時才重畫。卡片只放短年份、姓名、專利號或來源，所有文字後製疊上，不請模型畫可讀文件。封面另按[企劃](A01-rolling-suitcase.md)處理，未計入 95 張正文插畫。

## 付費前帳：估算與 US$25 停線

計價基準於 2026-10-15 查：[MiniMax 官方 `image-01` 每張 US$0.0035](https://platform.minimax.io/docs/pricing/overview)、[Gemini 3.8 Flash TTS 在 2026 年底前音訊每 10 秒約 US$0.00225](https://ai.google.dev/gemini-api/docs/pricing)；repo 目前媒體 judge 預估每次 US$0.01（[`tools/video/media/stages.mjs`](../../../tools/video/media/stages.mjs)）。**供應商牌價不等於正式主機實際可用價格、餘額或帳本。**

| 項目 | 有界規劃算式 | 預留 US$ |
| --- | --- | ---: |
| MiniMax 正文圖 | 95 首張＋最多 25 次必要重畫＝120 次 × 0.0035 | 0.42 |
| 圖片 judge | 120 次 × 0.01＝1.20；另暫留 10 次失敗回應可能再問＝0.10 | 1.30 |
| 台灣口音 TTS | 9:02 × 0.0135／分≈0.122；另最多 20% 需重配的語音≈0.024，含少量輸入字費 | 0.15 |
| 轉錄與 Jev 音訊覆核 | 以一次全稿、必要時局部重查預留；正式使用的 Gemini 文字模型、Jev 計費與 token 待主機報價 | 1.50 |
| 後續文字模型／敘事評審 | 若正式工人重寫、逐章驗證或評審，依實際 token 使用；此數是執行預留，**非已知單價** | 10.00 |
| 配樂（僅成片格式需要時） | 最多一首，repo 既有估價 0.08；可沿用已授權片尾音樂 | 0.08 |
| 未知失敗呼叫與價格偏差緩衝 | 供應商回應未記帳、追加一次 QA 等，超額即停 | 5.00 |
| **規劃預留合計／剩餘** | **US$18.45／距 US$25 上限尚有 US$6.55**；不是實際支出或保證報價 | **18.45** |

`image-01` 加成功 judge 的歷史均價約 US$0.0135／張，這張表把圖費、評審、重畫拆開。待部署的 #1508 成本控管設計，Gemini judge／locate 每次發送前可預留最多 **US$1.032192**，回答後才按實際 token 對帳；這不是目前正式環境已生效的保證，也不能把 95 個評審同時派出、拿 US$1.30 當硬上限。一次一鏡／小批次、確認前筆已結算才繼續；遇未明的付費結果先停與供應商用量對帳，不盲重送。文字稿已有本機審稿，沒有為此表產生新的模型費。

執行前須核對正式工人的版本，確認 #1508 的**每 slug `video_pilot_budgets` 帳戶上限 US$25**已部署並能讀回；另查 `/video/media/status`、這支片目前 ledger／預留／供應商餘額與其他進行中工作。全站 `max_usd_per_video` 是媒體限制，不能代替這支片涵蓋文字、音訊和媒體的 US$25 上限；本地草稿設定或 PR 也不能代替正式讀回。每一步用「已花＋仍預留＋下一次最壞請求」判斷，碰到 US$25 或餘額不足立即停止新的付費呼叫。95 張若需超過 25 次重畫、文字或評審超過表內預留，先重排有來源的鏡頭及成本，再決定是否縮範圍；不能改成 0 張圖的文字卡片。影片 TTS、插圖、圖審、聲畫、Studio 片尾三個可點元素與實際播放都還沒有完成證據。
