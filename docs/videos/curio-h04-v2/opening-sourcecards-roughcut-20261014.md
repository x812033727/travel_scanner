# H04 v2｜來源圖卡與片頭離線有聲草剪（2026-10-14）

**狀態：候選草剪，非正式分鏡或成片。**站主選擇免費來源圖卡加離線有聲草剪後，僅對前兩張人工退件圖設計原生 SVG。正式 `video.json`、現有圖片 manifest、核准旁白、時間軸與 `approvals.json` 都沒有改動；本輪沒有 MiniMax、判圖、TTS、轉錄或後台請求。片尾查核的正式 `video.json` SHA-256 為 `77cc48df04e88fc35caa57fbfe7328ea984c63c296875912d32128a911429eed`，manifest 為 `1e4f2001198c93afe78cefb3461634b4f2be43e4993bf94bfb384fb7cd1e1fcc`，帳本為 `3360f754379d1c33d1c89f6f4043d72e44934e4d80f9847a3b694de1cc3fa3fd`（US$2.879、reserved 0），皆與前輪結尾相同。此前三鏡的退件與費用見[修訂小樣](./visual-pilot-three-opening-revision-20261014.md)。

## 三鏡試播與來源

獨立預覽資料在 repo 外 `<VIDEO_WORKDIR>/curio-h04-v2/review/offline-opening-sourcecards-20261014/`，包括 `video.preview-sourcecards.json`、來源 SVG 的 1920×1080 光柵副本、三句 CC、MP4 與 `receipt.json`。預覽副本只把下表兩鏡改成 `diagram`；正式規格未落地。片頭三句固定以現行時間軸的 0–621 格、30 fps 播放：

| 時窗 | 預覽畫面 | 人工抽格結論與來源界線 |
| --- | --- | --- |
| 0–219 格，0–7.300 秒，`opening-search`／`h4v001` | 沿用 `opening-search-1-trim.jpg`，SHA-256 `5b15c122f4664ef392f08a51fa9abc829cf8fe14f0f6aef74a39411384492d0b` | **暫用條件候選**。無樹雪坡、遠處帳篷與兩個匿名搜救者可讀，但帳篷被坡線遮住大半；人物數與位置都不是史實重建。[c08](./claims.md) 的發現日由 [S1](https://dyatlovpass.com/case-files-384-387-ru) 與 [S4](https://dyatlovpass.com/case-files-298-300) 支持。 |
| 219–419 格，7.300–13.967 秒，`opening-inside`／`h4v002` | [帳內無人 SVG](./diagrams/opening-inside-source-card.svg)，SHA-256 `91993b66c17d004297f763068d885cf65e6531884716958a322cd091022898f8` | **草剪候選**。抽象空帳篷與「帳內未見隊員」替代先前畫出樹林的退件圖。卡上明示非內部結構或清雪動作復原；[c09](./claims.md) 依 [S4](https://dyatlovpass.com/case-files-298-300) 第 298–300 頁。2 月 26 日是搜救發現日，不是事故日。 |
| 419–621 格，13.967–20.700 秒，`opening-gear`／`h4v003` | [留物與足跡 SVG](./diagrams/opening-gear-source-card.svg)，SHA-256 `2c77fc6ee9d5eddfe2f6f89c19e4e97d50f37e3dee5291ab06db5cf6e3c8c0a1` | **草剪候選**。鞋形和外衣形是圖標，不代表件數、款式或擺放；向下箭頭只表達足跡方向，不連成逐人路線。[c01、c04](./claims.md) 的兩項觀察依 [S1](https://dyatlovpass.com/case-files-384-387-ru) 第 385–386 頁。退件 MiniMax 靴款圖不採用。 |

草剪 `H04-opening-three-sourcecards-roughcut.mp4` SHA-256 **`4f594cf91db0387cc71ca906de727d7006f354a13d319eebb4264bf650974004`**，20.700 秒、621 格、1920×1080、H.264／AAC、30 fps；旁白從已核准 `narration.wav` 原速截取，可關閉的繁中 CC 是 `mov_text` 軌。三句 CC 與既有 body-only SRT 前三句文字和時碼一致：0–6.680、7.300–13.340、13.967–20.097 秒；每句末到下一鏡約留 0.6 秒。MP4 全檔解碼通過。正式 WAV SHA-256 `f6eeaff7f57e66453262a962ad382e84f00867f1c404c102f6d1c5b90cdb3abd`；正式時間軸 SHA-256 `65e48861f66a7437ba3218a6601c89a1b52040a03fbcc5252ebdc5278fc2bc71`，與現行音訊核准相符。

我抽看搜尋末格、帳內首末格、留物首格及兩張有字幕的中段影格。第一次合成時，`opening-gear` 來源註記與雙行 CC 撞字；已把兩張卡的來源／示意註記上移、簡寫並放大，再輸出上列雜湊的 MP4，以字幕模擬抽格確認沒有重疊。這僅驗證該字幕樣式；播放器字型或定位仍要實播確認。由雪坡插畫硬切到米色資訊卡，節奏與風格可能突然；6.7 秒靜卡能否撐住句子也須正常速率播放確認。工具無法接收音訊，亦沒有連續影片播放能力，因此**沒有宣稱已從頭實速看聽**；清晰度、語調、真實過渡、站主接受及獨立冷看均為 `pending`。常規判圖未對免費 SVG 執行，不能把既有 MiniMax judge 分數挪給新圖卡。

## 正式替換前的 50% 門檻

現行完整時間軸 15,827 格，`shot` 7,963 格，50.3128%；整數門檻為 `ceil(15,827/2)=7,914`，餘裕只有 **49 格**。若正式把 `opening-inside` 的 200 格和 `opening-gear` 的 202 格換成 `diagram`，在台詞和時窗不變時只剩 **7,561／15,827＝47.7728%**，缺 **353 格**，所以這份預覽不能直接覆蓋正式 `video.json`。

只提出兩個**有敘事任務但尚未生成、尚未驗證**的交換候選：

| 原非 `shot` 場景 | 現行時長 | 後續候選畫面與必要邊界 |
| --- | ---: | --- |
| `tent-opening-question`／`h4v105` | 143 格，4.767 秒 | 近看匿名、未標出裂口方向的普通帳布與陰影，為旁白「裂口從哪面劃開」建立懸念；不畫下刀的人、由內外的動作、真實切痕形狀或當年證物照片。畫上須以獨立排版標「情境插畫／非證物復原」，鑑定依據回到 [S2](https://dyatlovpass.com/case-files-303-304-ru)。銜接既有 `tent-opening-empty` 與後續足跡圖解時，不能重複一張泛帳篷。 |
| `model-paper-card`／`h4v048` | 231 格，7.700 秒 | 以小規模雪板的**概念模型**回答片頭預告並帶入機制；不用假論文頁、虛構公式、研究者肖像或 1959 年實測剖面。需在生成畫面之外排版可讀的「2021 年模型概念／[S5](https://www.nature.com/articles/s43247-020-00081-8)」來源及非現場示意標記，保留正文首次明示回扣。前後 `camp-open-question`、`cohesive-snow` 不可變成重複雪坡。 |

兩鏡共 **374 格**；若兩鏡都經來源、畫面、連戲與實播驗收，且時間軸分母不變，`shot` 才會到 **7,935／15,827＝50.1358%**，僅剩 **21 格**餘裕。這是驗算過的**條件方案**，不是把未生成鏡頭計入現況。兩鏡若不能保留必要來源標籤、生成出假文件，或任何一鏡人工退件，方案即失效；不把 `journey-pack`、`buried-layer-close`、`unmeasured-snow` 等人身分、模型條件或未知界線卡硬改成雪景湊數。站主日後若授權付費，可先各做一張 MiniMax、各鏡僅一 take（最多兩張，先驗來源標籤與 `model-paper-card`），逐張看原圖與實際選圖後才決定是否繼續；**目前沒有執行**。在兩張示範片與相鄰鏡的連戲、50% 比率都實證前，不應全片擴批。

## 後續關卡

正式採用圖卡須把兩個 `data.svg`／`caption` 接到 `video.json`，先驗圖卡在正式 renderer 中的縮放與字幕安全區。預覽副本 `lint --file` 為 0 errors／5 warnings（含估算插畫比例不足；**實際時間軸**以 47.7728% 為準）；不能把它當正式片核准。若將上列額外場景改為 `shot`，須重新做來源與 storyboard 審查、小批 MiniMax 人工實看、全片 `lint`、時間軸和 cadence／`illustrationShare` 實算。即使台詞、順序、narrative hash `bd49404ff2771d33` 與原 WAV 不變，模板變更後的時間軸雜湊也要重新建立與核對，按 `youtube-video` 流程把音訊核准綁到**新**雜湊；不得沿用舊 `approvals.json` 代替新版本核准。其後才做正式可關閉 CC、全片正常速率看聽、QA、站主分鏡及成片驗收。
