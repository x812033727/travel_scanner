# 十部漫劇：動畫攝製覆核與製作交接

2026-10-01。十部、400 集的故事／人物／道具與拍攝風險已覆核，製作資料與工具已準備；**尚未試音、生成動畫、驗收成片或更新正式站**。沒有用本機通過檢查取代影片驗收。

目前工作目錄：`C:/Users/x8120/.codex/worktrees/ten-drama-production`。分支：`codex/ten-drama-production-readiness-20261001`，本輪基於 `origin/main` 的 `be92a7ab`。原聊天綁定的 `31ce/travel_scanㄐ` 已不存在；本輪所有工具使用新目錄。

## 檢查範圍與結果

覆核目前 repository 的十部來源、60 份文件及可重建資料，對照上一輪修正與現行造型功能。舊修正 `572bb9c9` 已經由 PR #978 合入主線；PR #1068 補的是每集 `characters[].looks` 功能，不能當成十部影片已渲染或正式站文件已同步的證據。未在這輪檢查正式站內是否還有另外編輯的版本。

沒有新增可確定的主要劇情矛盾。這輪修正了製作設計中的造型描述不完整、記憶匣與工具袋交接混淆、開場人物越過當集清單，以及候選發音和畫面時間資訊的解讀。新的分鏡資料不改歷史故事來源或核准收據；新待審 bundle 另以 source、design、profile 和文件雜湊綁定。

| 作品 | 製作覆核 | 主要攝製控制 |
| --- | --- | --- |
| 喜宴未散，清算開始 | [覆核](../binge-five-20260928/wedding-reckoning/production-review.md) | 原件／展示副本／完整副本分清、前世褲裝與現世婚紗、三出口方位、腕錶到桌面 |
| 末班車上的第七個活人 | [覆核](../binge-five-20260928/seventh-passenger/production-review.md) | 白燈與哨音、真假母聲、制服交出與病服、27 歲／20 歲成年回望；未成年角色另需動畫路徑 |
| 朕不是你們的替死鬼 | [覆核](../binge-five-20260928/scapegoat-empress/production-review.md) | 摘戴冠冕按鏡頭切態、收養簿與三枚印證據鏈、糧批與人物知情先後 |
| 這座城欠他一盞燈 | [覆核](../binge-five-20260928/city-owes-a-light/production-review.md) | 救援與顧問職責、借衣和傷後狀態、雨聲不能蓋過回報；未成年角色另需動畫路徑 |
| 世人忘我，死敵記我 | [覆核](../binge-five-20260928/remembered-by-rival/production-review.md) | 藏／露／斷繩、拆徽與交鑰匙、記憶匣只驗不交、被記住的因果；未成年及少年回望需逐鏡確認 |
| 開服第一天，她的天賦叫讀檔 | [覆核](../claude-binge-five-20260928/reload-first-day/production-review.md) | 讀檔母題與實景時鐘分開、系統介面與傷痕、背包／耳機交接；未成年及背景兒童需動畫路徑 |
| 重生回落槌前一秒 | [覆核](../claude-binge-five-20260928/before-the-hammer/production-review.md) | 真偽光紋需同光位對照、手抖／輪椅／腿傷、留置後道具狀態、白薇台灣讀音 |
| 三針 | [覆核](../claude-binge-five-20260928/three-needles/production-review.md) | 摘徽與手套、秤交接、帳與針包實際尺寸、既有地點的轉場；未成年需動畫路徑 |
| 她替公主試毒十年 | [覆核](../claude-binge-five-20260928/taste-of-the-throne/production-review.md) | 暖手器交出／破損、左肩繃帶、串珠／手帕／扇子離手、門縫與空間轉接 |
| 符師與他的鬼 | [覆核](../claude-binge-five-20260928/ghost-at-his-side/production-review.md) | 沈30→120→灰、陸61→93、鬼入符／出符、同人青年身體與鬼拆鏡；未成年需動畫路徑 |

每部有 40 集獨有的主鏡頭、camera／sound、風險解法、道具檢查、聲音與 CC 筆記，以及連到來源的定位。每部開場連續規劃 0–30 秒，鏡頭剪段不超過八秒；秒數是設計，仍需中文配音實測。

## 中文先完成，所有字幕為 CC

執行規格在 [profile.json](profile.json)。先完成 zh-TW 自然台灣口音的角色、旁白、正片與 SRT／VTT；日文、韓文、英文角色音軌與各語 CC 從中文已核准主版開始。這輪没有啟動外語製作，多角色多語自動產線仍標 `planned-not-implemented-for-drama`。

新自動製作固定 `subtitles.burn_in: false`。劇內文件與數字是道具，不是對白燒錄字幕；重要文字要另行排版查核，再合成到有動作的鏡頭，不能信任模型直接畫字。CC 不得提前顯示謎底。

角色固定 speaker id 與選定 Gemini 聲線；旁白另選且不和任何角色共用。已準備每位角色／旁白的三段中文試音材料，涵蓋對峙、低聲、情緒轉折及人名，**尚未合成或聽校**。`audition-plan.json` 的參數陣列可交給現有 `audition` 指令；從 repo 根目錄執行，先核對文字、voice、style 和費用，不批次直接執行全部樣本。發音提示放在 style，試音文字只唸人名與句子，不把拼音／注音當台詞。

白薇的「薇」採台灣教育部標準 `ㄨㄟˊ／wéi`，修正本輪候選拼音的一聲誤判；來源的二聲保留，仍需實際試聽。[教育部《國語辭典簡編本》](https://dict.concised.moe.edu.tw/dictView.jsp?ID=43453&la=0&powerMode=0)，2026-10-01 核對。

保留 TTS 每句原檔、speaker／line id、乾聲旁白、獨立音樂與音效來源。Veo 原生音訊始終生成，正片排除它並使用獨立配音。外語版重建角色人聲與混音，不使用完整中文混音作底；各語 CC 依自己的實測音軌重算。中文畫面時長仍會限制外語句子，預留反應鏡與停頓，先改可演措辭，再考慮小幅句速調整。

## Veo Lite 與放量前的實際限制

此次 Gemini API 選 `veo-3.1-lite-generate-preview`，1080p、16:9、八秒素材、24 fps；現有剪輯採30 fps網格，轉換不能增加真正的動作細節。Lite 支援首／末格，不支援 `referenceImages` 或 extension。角色一致性由已核准臉部圖製成首格，再用 judge 比對；不能把 Lite 沒有的多參考圖能力寫成已完成。[官方 Veo 文件](https://ai.google.dev/gemini-api/docs/veo)，2026-10-01 核對。

正式動畫鏡頭有準備、接觸、重量、收勢、眼線及角色反應；一鏡一主要動作、一個 camera 意圖。此 profile 拒靜圖縮放冒充動畫、超過八秒後的尾格停格，以及模型／解析度不符或舊短片快取通過；16:9／1080p 必須有實測1920×1080證據，不能把720p放大當成原生1080p。直接 `assemble` 也在 ffmpeg 前使用同一檢查。這些技術檢查仍不能證明演技和故事節奏好；需要代表小樣。

**六部含未成年角色或兒童背景，不能宣稱已全部具備 Lite 首幀生成路徑。** 現有 I2V 接口僅 `allow_adult`；兩批共有八名明確未成年角色，以及未登記 cast id 的兒童鏡頭。`readiness.json` 列具體人物與集數。付費 clip 階段遇到這些視覺人物／明示的兒童集會停止；純畫外配音不因此變更年齡或被誤擋。保留原劇情，另行驗證合適的手繪／動畫供應流程，不能把遮脸、背影或省略年齡當成已驗證解法。[官方人物生成參數](https://ai.google.dev/gemini-api/docs/veo)。

嘴部大特寫需單獨驗收對嘴；目前沒有自動 lip-sync。可按劇情使用反應、越肩與證物插鏡承接台詞。源故事涉及的唱歌、真假母聲、術法與物理音效也需實聽，不能用資料檢查代替。

## 製作順序與費用

1. 核對新待審設定、每集 director plan 與來源版本，解決未成年動畫路徑。
2. 實際試聽中文角色／旁白，修人名、聲線與表演，固定已接受樣片。
3. 用中文實測對白做 timed animatic，檢查每集鉤子、首次回報、場景與道具交接；靜畫只在這個前製階段使用。
4. 做含對話、接觸動作、關鍵道具及造型轉換的代表 pilot；先修臉、手、年齡、音訊、CC 和節奏再放量。
5. 鎖定風格、角色圖、聲線與音效母題，按篇章製作並保留有限重試及預算守門。
6. 驗收完整中文版與可關 CC，再製作日／韓／英角色音軌、混音及各語 CC；上架接受狀態獨立記錄。

官方 Lite 1080p 價格為每生成秒 US$0.08，即每次八秒素材 US$0.64。假設一部120分鐘、每鏡採3–6秒，約1200–2400段八秒素材，僅影片生成約 US$768–1536；不含廢片／重試、圖片、TTS、judge、配樂或製作工時。這是規劃算式，不是報價或已支出。[官方價格](https://ai.google.dev/gemini-api/docs/pricing)，2026-10-01 核對。此輪沒有付費生成、修改預算或啟用正式站。

百萬觀看是目標，不是預測。已為各劇安排前5秒衝突、30秒第一次回報、獨有動作與情緒代價，標題／縮圖承諾需由開場兌現。發行後比較頻道本身的曝光、點擊與留存基準，對照流失／重看片段調整，不設定沒有根據的通用 CTR 門檻。[YouTube 留存報告](https://support.google.com/youtube/answer/9314415)。

## 本機工具與驗證

```text
node tools/video/cli.mjs production-check
node tools/video/cli.mjs production-build
node tools/video/cli.mjs production-build --out <LOCAL_REVIEW_DIR>
```

指令均離線。`production-check` 驗來源雜湊、40集覆蓋、角色與地點、首30秒、完整命名造型、候選聲線和交付規格。`production-build` 產生 `bundles/<slug>/documents.json`、`series-request.json`、新 manifest、試音文字與參數、[readiness.json](readiness.json)、[build-receipt.json](build-receipt.json)，以及[互動分鏡預覽](storyboard.html)。六份文件中的總綱／細綱保留，設定集加入新聲線、造型與製作指引。新 bundle 仍待審，沒有導入後台或替人核准。

本輪驗證：全面影片工具回歸924項通過、1項Windows測試略過；最後直接組片及原生尺寸守門的相关65項通過。兩批來源／交接38項通過；API58項通過、3項資料庫整合略過；ruff、mypy通過。另以實際十包驗證10個 `SeriesIn`、60份 `SeriesDocSubmitIn` 與 `doc_problem`。預覽頁在桌面／手機測過十部、400集切換，無 JS 錯誤或手機橫向溢出。這些僅證明本機工具與規劃頁，沒有實測配音／動畫，也没有宣稱正式站、YouTube播放器或觀看成效已驗收。
