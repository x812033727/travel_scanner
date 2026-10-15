# H05 v2｜第三輪開場圖失敗與混合畫面候選

日期：2026-10-14。本輪看了三張完整 JPEG、判圖 manifest、實際 TTS 時間軸與離線 renderer／lint，並做開場與片尾局部預覽；沒有完成全片實速觀看。現行來源與旁白文字維持不變。

## 第三輪付費小樣：停止同一路線重抽

MiniMax `image-01` 在 `video.json` SHA-256 `acd6c9cb908e4aa12bb389ff14689066a81ffb1607f9b49d527bf519c97692f8`、`look_hash=38b9efa0cb47553f`、`pictures_hash=6ab8bb2bae500724` 下各畫一張。外部 `keyframes/manifest.json` SHA-256 `6b4046143e1cb552d00039c4c1a45f13818ac8ffd9bc2cfdd0108b32963dcedf5`；manifest 的三項 `needs_review=true`。原 manifest、當時 `media/ledger.json`、三張原圖及櫃檯裁切圖已複製到外部 `_receipts/visual-pilot-03-20261014/` 並驗 SHA，原產物不改。此輪帳本六筆為三次 image 和三次 judge，共 **US$0.0405**；三輪累計在 H05 帳本是 **US$0.1215**。

| 鏡頭與第三輪選取圖 SHA-256 | 原 judge | 人工實看、對故事的影響 |
| --- | --- | --- |
| `open-counter`：`132337bbbe63472c46f3915750c67629edf0eb9ea6a5f440b77484837734793e` | 9.00，FAIL；`text=0` | 櫃檯冒出約十名未要求的人；桌上牌卡有假字與數字。顧客站在多人櫃檯前，失去原定單一購票焦點，也可能讓假牌卡被誤認作史料。 |
| `open-ticket`：`5b80a87457df00e88525dff5d6540399da03afb81837e7e0876eb3b7cd9d2cfc` | 9.00，FAIL；`text=0` | 紙票與小卡上生成可辨認的假字、符號，旁邊多了筆與紙墊；不適合在真實機票亦將出現的影片中充作交易物證。 |
| `open-aisle`：`15236df280288f64345ddce8faa3f0c8fc859da1e474aa614e95606d648db338` | 9.71，FAIL；`style=0` | 構圖是成人背影與客艙，但整張轉成擬真攝影畫面，和前兩張 2D 插畫無法連戲，且可能被誤讀為史實影像。 |

三輪分別暴露手部／人物比例、身份與場域連戲、假字與風格漂移；不要在同一「文字提示＋MiniMax 單張 AI 圖」分支加新 seed 重抽，也不要用高總分覆蓋失敗的硬項。既有已登記 FBI 原件照片保留在工作目錄；AI 只考慮沒有精確文字、人物動作或證物形貌要求的環境景。此結論是本案模型與這些提示的實測邊界，不推成所有模型的通則。

## 不改主檔的最小開場候選

在外部 `_tools/mixed-opening-pilot-20261014/video.json` 建立隔離候選，只改前三景 `template`／`data`，不改 line ID、旁白文字、場景順序或來源。第一景 `big` 原生卡顯示「1971 年 11 月／波特蘭機場」；第二景 `photo` 直接顯示已在 `assets[]` 登記的 FBI 機票原件 `stock/d0d8c89a2e3d584d3f0956e85079d1d65b902653d2b96d59fff1b932bdd4a7aa.jpg` 並標明 FBI／公有領域；第三景 `big` 原生卡顯示「波特蘭 → 西雅圖／305 號班機／機票上的名字：Dan Cooper」。這三句文字均在已查核 FBI 案件紀錄及原件範圍內；畫面不假扮買票或登機的現場照片。候選的縮圖 `shot` 指向只在隔離檔移除，使本機渲染不依賴未完成的 `boy-bank` 關鍵影格；正式縮圖設計仍待成片階段。

隔離候選檔 SHA-256 `131761858fc5831b010a5cb6543979fdc36cabbc6e6564d58c3ae2dd3fb47ff`；`lint --file` 為 **0 errors、0 warnings**。改版型使 `narrativeHash` 從 `e0d2eb7016aea429` 變 `09fe77b108894e4a`，故正式採用時需按既有敘事關卡重綁；`speechHash` 仍是 `7d8cb6cb30ba87d9`，已核准音訊不因這項畫面改動而重錄。這是候選，不是正式 `video.json`。沒有新生圖或 TTS 付費請求。

### 實際渲染與 15.2 秒離線預覽

用隔離候選在外部 `_mixed-h05-20261014/curio-h05-v2/` 執行本機 `render --file`：**44 個原生卡／照片狀態新繪、0 個沿用、0 個版面錯誤**，產出 `frames/manifest.json` SHA-256 `82e02974f9fa7a977877aee4bf032157b7090e142ca9b3442cb7d83b071f4abe`。這是渲染器可畫的卡片狀態；尚未生成的其他 `shot` 關鍵影格不在其中，因此不能當作全片圖像完成。前三景實際 1920×1080 靜格如下，檔案均位於該隔離工作目錄的 `frames/`：

| 景 | 渲染檔與 SHA-256 | 實看結果 |
| --- | --- | --- |
| `open-counter` | `56d3aaa2ebf1c30d.png`：`614110a69b24d43fe9655e146868d6b3a33b5df7ca673c6ebdc29649908496aa` | 日期、機場與單程票起點全是編輯指定文字，安全區內清楚，無假招牌或生成角色。 |
| `open-ticket` | `d227942f70c6c903.png`：`d1ef0eaee3d1775547e6d579543c17838e82b2baccf36d5fed3e1b796a58145d` | 已登記原始機票 JPEG 全幅置於框內，姓名／航線／305 可見；`FBI／公有領域` credit 與卡片 caption 均可見，沒有修補票面。caption 在畫面下緣，仍須在最終播放器與啟用 CC 時確認不互蓋。 |
| `open-aisle` | `2a7affc4b80fdff2.png`：`5adbb0528d5918504e3b1c1e80e555a939776fa31ca842c20d9aea784bd29a13` | 航線、航班號與購票用名清楚；與首張同版式，連續兩張文字卡節奏仍須聽看小樣後再評估。 |

以已核准的 `h5v001`–`h5v003` 原 WAV（各 SHA 與 `timeline.json` 相符）、各景 142／153／161 格及句後空白，離線合成 `mixed-opening-preview.mp4`：**15.200 秒，1920×1080、30 fps，影音串流均為 15.200 秒**，SHA-256 `f2f01cdf088ded88d38719f5cb0851d304331ef00a2f2ee52fc1ca2041d84822`。此預覽是核對畫面／音訊時間的候選檔；尚未作全片實速聽看或站主驗收。機票來源 JPEG 在隔離工作目錄的 SHA 仍是登記的 `d0d8c89a2e3d584d3f0956e85079d1d65b902653d2b96d59fff1b932bdd4a7aa`。

以原來的實際 `timeline.json` **535.767 秒** 計算，前三景各 **4.733、5.100、5.367 秒**，都低於單畫面 8 秒。當時 `shot` 覆蓋 **62.29%**；三景轉成原生卡／照片後為 **59.45%**，仍高於目前 QA 的 50% 下限。當時 `outro` 單一狀態 **8.2 秒**，已超出 8 秒；後續同場景逐句揭示修正見下節。

同一套 `cadenceProblems` 對當時候選加舊時間軸實算為 **106 個畫面狀態、平均 5.1 秒、最長 8.2 秒**，問題只有 `outro state 0` 超過 8 秒；前三景本身沒有超時。這是該版候選的歷史預檢，不是現在片尾的結果。

## 主稿片尾修正：同場景三次揭示

主 `video.json` 保留已採用的前三景，也保留 `outro` 場景 ID 與 `h5v109`–`h5v111` 每句文字、順序、情緒與原 WAV；僅把片尾從一張不變的 `outro` 卡改成原生 `bullets` 卡，標題「奇聞檔案局」，三項依「證明贖金，不證明人。」→「哪件物證最意外？」→「訂閱，繼續查證。」逐句揭示。最後仍由合成階段接品牌結束畫面。這是實際不同的三個畫面狀態，非僅在時間軸拆帳。主 `video.json` SHA-256 `7d317e4ae9607cb7d92a4486a8dad7837356edab7147fca1ccdb4ce6c147812a`；重生 `script.md` SHA-256 `7ae168c2b44219a7b42632fe89efa4b5b1602f8544ff8e7b5fbae1348dd272e3`。新 `narrativeHash=65c64491d8a53b77`，舊敘事盲評不可自動套用。

實際 WAV 的快取預檢回報 **102 requests、0 要合成、0 billable**，正式 `tts` 快取重建亦是 **0 synthesized、102 reused**；沒有付費語音請求或重錄。新 `timeline.json` SHA-256 `8128f74e74f2dad44ea0c6a1465f2a333c4cb30d0b7f9cfb14829f414becd984`，舊版 SHA-256 `66996c424a387b5a73f8132a713056a3371a16fca26c7b617358b767c76b8adc` 已另存外部 `_receipts/outro-before-reveal-timeline-20261014.json`。新舊 `speechHash` 均 `7d8cb6cb30ba87d9`；108 句每句起迄格完全相同、總長仍 **16073 格／535.767 秒**，`narration.wav` SHA-256 仍 `8b519d908e7b85d7d214288d3bf8c7ebb5bc897456a4b32c74143cff50253ba3`。正式時間軸的 `outro` 三狀態為 **82／71／92 格**，即 **2.733／2.367／3.067 秒**。

主稿 `lint --slug` 為 **0 errors、0 warnings**；用新實際時間軸跑 `cadenceProblems=[]`，共 **108 個畫面狀態、平均 5.0 秒、最長 7.3 秒**，`shot` 覆蓋 **59.45%**。離線 renderer 另為片尾畫出三張 1920×1080 靜格並人工檢查逐句增項、文字與安全區；三圖 SHA-256 依次為 `fe426fa63ad89770b88943c7895b0dc947ea20af6cdae1712c2b010128426da6`、`83d444144f3066c58c621eb22ea720afcb22992d7db65fec9b36b8f2aa3c9d3d`、`23767d3d2e583978b1494690dc56a97758ab561bee14b12b4c285fbfff9c7e8a`。本機 `outro-reveal-preview.mp4` 影音同長 **8.166667 秒**、1920×1080／30 fps，SHA-256 `2ca7b6fd44050a1f45d8a099c970e76e1b49d4618ffa82a9f5d7596eb6350bab`，位於外部 `_mixed-h05-20261014/curio-h05-v2/`。

**核准綁定不可略過：** `approvals.json` 原音訊核准綁舊 `timeline.json` 完整 SHA。儘管音檔、語音 hash、每句時間都未改，重建後 `status` 仍讀回 `[ ] narration approved: changed since it was approved`；不得私改核准收據或把原後台核准冒稱仍有效。敘事盲評也因模板而變更 hash。這兩項需按原流程重綁；完整圖片、合成片、字幕與最終 11 項 `qa` 仍待後續製作。

## 全片混合畫面的可行邊界

可直接重用的來源照片是購票機票、尋回贖金、留在機上的領帶三張，均已在 `assets[]` 含來源和授權。數字、日期、航線、索引、身分限制、研究對照與機票／鈔票／領帶的精確物證應使用照片卡及由編輯寫入的文字或圖表卡。AI 僅用於沒有假文字與精確人手動作的空機場、空客艙、雲層、森林、河岸和實驗室環境；生成後仍逐張看假招牌、假文件、是否像史實照片及與其他畫面的風格關係。不得批次照舊 65 個 shot prompt 生圖。

**來源／授權邊界（2026-10-14 查回）：** [Commons 機票檔案頁](https://commons.wikimedia.org/wiki/File:July_2016_D.B._Cooper_Plane_Ticket_(28379315406).jpg) 與 [贖金檔案頁](https://commons.wikimedia.org/wiki/File:Money_stolen_by_D._B._Cooper.jpg) 均標示 FBI 員工公務作品，在**美國**屬公有領域；[FBI 案件頁](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)與[領帶圖頁](https://www.fbi.gov/image-repository/black-tie.jpg/view)確認領帶是官方刊載的案件物證照。[DOJ 政策](https://www.justice.gov/legalpolicies)說明其網站素材通常可複製，但個別第三方作品例外，且官方標誌與名稱不可用於暗示背書。故沿用 `asset-register.md` 的原檔 SHA、來源與 credit，不擴及 FBI 素描、品牌圖樣、新聞照、論文圖表或未登記照片；不把美國公有領域註記寫成已查明全球各地權利，也不宣稱 FBI 贊助影片。票面上的航空公司名稱只隨原件照片出現，不另作品牌宣傳圖。

目前 `tools/video/core/cadence.mjs` 的 `illustrationShare` **只計 `template:"shot"` 的時間**，不計 `photo`、`diagram` 或其他原生卡。現行 65 個 shot 共約 333.8 秒；50% 下限是約 267.9 秒，除前三景外只餘約 50.7 秒可改成照片／卡片而不觸發 QA。若全片真正改成「AI 只畫空景，其餘皆照片或原生卡」，現有 `shot` 數量會遠低於 50%；必須先正式定義並實作原創非 AI 圖像如何進入圖片覆蓋檢查，或在維持品質的前提下重新設計足夠的 `shot` 畫面。不能靠改名、手改 manifest 或忽略 QA 來當作已過關。結尾 8.2 秒問題已在主稿修正；全片圖片覆蓋設計仍須在擴批前處理。
