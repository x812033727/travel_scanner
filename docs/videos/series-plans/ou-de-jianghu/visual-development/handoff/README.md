# 第一集資產與開拍交接

2026-10-08。範圍為《偶的江湖》第1集〈幽皇之女〉。站主已選擇保留目前華麗古裝與細緻人物畫風，並授權繼續補齊前置；**個別圖像採用、正式look關卡、v3計畫鎖定及付費動畫小樣，尚不能用這個畫風決定代替。**

本交接與原 e001、production 檔分開保存；未改既有試播票或第8集工作。下游仍接 [原第1集Hailuo試播票](../../../../../../tasks/open/2026-10-04-clip-route-pilot-comparison.md)，沒有另開重複付費試播。

## 先讀什麼

1. [P0–P7審閱包v3](../episode-plan/preproduction-package-v3.md)：條件、9場空間、455鏡、風險、完整預算、三鏡小樣及停止規則。
2. [逐鏡索引](../episode-plan/shot-index.md)、[鏡位與風險ledger](../episode-plan/camera-and-risk-ledger.json)、[分項與批次JSON](../episode-plan/budget-and-batches.json)：實際可執行鏡號、做法及依賴。
3. [v3來源／產物SHA](../episode-plan/proposal-summary.json)、[重建與文件核對](../episode-plan/package-verification.json)、[獨立文字分鏡觀看紀錄](../episode-plan/cold-review-independent.md)：分清來源不變、程式檢查與真正觀看。
4. [九人畫像](../episode1-portraits/README.md)、[独立視圖收據](../episode1-portraits/independent-views-receipt.json)、[場景道具來源及媒體收據](../scene-prop-design/media-receipt.json)、[匯入合約](../import-contract/README.md)：資產版本、用途和原生接入狀態。

新增動畫參照、美術候選清冊及本輪實際匯入證據已整合於 [asset-manifest.json](asset-manifest.json)：12份來源SHA、139張最新候選、9張正面沿用關係、16種shot_looks獨立雜湊與隔離匯入收據。這是前期交接清冊，沒有寫入正常runtime或冒稱模型已使用所有多角度參照。

## 已形成的具體交付

| 項目 | 可交接內容 | 狀態界線 |
| --- | --- | --- |
| 美術方向 | 華麗古裝、細緻人物；9概念與27獨立視圖沿用 | 畫風已接受；各張採用與正常look另記 |
| 新參照範圍 | 已交付74張新增角色參照＋29張場景／道具候選；角色加沿用9張正面共83項用途 | 角色90個保留PNG含89張唯一生成圖與1個同圖別名；所有修訂保留，正式採用尚未決定 |
| 規劃提案 | v3可執行覆寫，455鏡＝420clip＋30still＋5來源切，9空間 | 原劇本、鏡序、597句台詞與action_seconds不變；不是正式lock |
| 鏡位及風險 | 原447組setup收斂343；原10個程式C逐鏡裁定；接觸s036保留人工C | 不把機器C0解讀為動畫零風險；343也不等於343支可直接共用影片 |
| 文字動態分鏡 | 459列，包含4原稿字卡，23:23.533；可本機播放與重建 | 沒有TTS／关键影格／動畫；獨立觀看結論依專人紀錄，不等於成片QA |
| 工程接點 | 外部PNG匯入已實作；9張全身原圖已隔離pending匯入，SHA與重跑去重通過，0次fetch | 229項相關測試通過；尚無judge、choice、正常look核准或runtime採用 |
| 預算及採購次序 | 420支逐一歸入兩個27000點額度期；首末格、聲音、judge、音樂及內建美術分開記帳 | 原始費率、畫面餘額快照與未來可用額度分開；沒有購點或續費授權 |

原稿video SHA為 `82d221350032c02b3b2f8943e72e63795be36e221c45067acf5bd9a751d20443`；工作v3為 `7f7676d1ce39a6f9dbbdc4cacc5bc8cb39b9979e66e4a906213d2ea4235014df`。若後續原稿持有人改了e001，先重新核對與合併提案，不直接把v3覆蓋回原檔。

角色圖冊已驗83張圖片解碼、9人篩選、放大／Escape、390px手機版及3個跨冊連結；詳見 [圖冊檢查](../animation-reference/gallery-verification.json)。原圖與清冊可用 `node docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/build-manifest.mjs <VIDEO_WORKDIR>` 重核。最新概念使用九人receipt，早期三主角receipt保留歷史而不回寫。

## 素材採用時須處理的具體差異

- 沈歸鶴人物參照的扇外骨偏深色，場景道具依原稿為白玉扇骨；先依原稿統一母版，涉及扇特寫的關鍵影格不得混用兩版。
- 三張客房紙窗候選仍可透出月輪輪廓，只作空間參照；紙窗近景須另做不透景首格。冷光客房只用在茶盤落地後的a05-s031／s035／s042，不能提前用在s023。
- AI棋盤格數／落子不是精確連戲依據；19×19 SVG已備成前後狀態提案，選定後才綁相關首末格。
- 18張半身／全身畫像低於建議交付尺寸；九人角度是2D／I2V參照，部分站姿與透視有差異，不是工程正交轉台或已綁骨架。
- 場景清冊10個地點列將棲雲山／望樓合為分場計畫的同一空間族，共9族。道具逐鏡表保留原劇本索引，重設計動作以採用後v3鏡位／風險表為準。

上述差異保留在既有畫像、動畫參照、場景道具與交接待辦票；沒有以候選張數冒稱全部已通過最終製作驗收。

## 工作產物與播放器證據

repo外工作目錄：`<VIDEO_WORKDIR>/ou-de-jianghu-e001/plan/preflight-20261008-v3/`。其中有完整 `video.json`、分鏡表JSON/CSV/Markdown、覆寫差異、首尾狀態、風險、文字animatic及工具stdout/stderr。可在repo根依下列順序重建到另一個空的repo外目錄：

```powershell
node docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/verify-proposal.mjs <OUTPUT_DIR>
node docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/budget-and-batches.mjs <OUTPUT_DIR>
node docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/serve-proposal.mjs <OUTPUT_DIR> 8767
```

服務只綁本機；運行時入口為 [文字animatic](http://127.0.0.1:8767/animatic.html)。已在獨立 `preflight-20261008-v3-rebuild-check/` 重建，video、HTML、shot-plan、camera-ledger、risk-ledger、proposal-edits六份SHA全部與v3相同。HTML SHA為 `2d8d5457f4056a3b99f46cf34d580b41791dd172aec0d60119b22a406b96353c`。

舊v2曾在15.7秒真的崩潰：共用generator省略字卡但保留時間洞，字幕索引變負；另有終點回第一格的邊界缺陷。v3在 [scope renderer](../episode-plan/render-proposal.mjs)補回4字卡及字幕／終點邊界，459段連續、2295邊界probe通過。舊v2目錄、未修的 `animatic-upstream.html`、錯誤時間與console證據均保留。

**共用generator兩份來源尚未修。** [追蹤票](../../../../../../tasks/open/2026-10-08-animatic-title-gap-subtitle-boundary.md)已明列 `.agents`／`.claude`同步及相關回歸測試；本次修的是可重建wrapper，不稱共用工程已完成。冷看者的實播時間與觀察限制，另見獨立紀錄。

v3後續已完成全長1倍速播放；373張卡即時觀察、86張補看，459張全覆蓋，但有工具觀察間隙及最初AX暴露全表，不稱完全盲看。冷看指出still卡缺首格線索，故另做 [v3.1卡面版](http://127.0.0.1:8768/animatic.html)：顯示原首格／靜態結果與3末格，video、台詞、時間及預算不改。其23卡獨立停格複看已完成，證據在 [呈現覆核收據](../episode-plan/presentation-review.json)；沒有把v3全長證據冒稱v3.1第二次全長。原版及修訂版各自保留SHA，重建補充器見v3包。

工具真實結果：lint與shot_reading strict過；craft strict保留a03-s052～s054三反應警告與人工理由；shot_plan strict保留整集期望超單月的警告。原生readiness為1過／429尚未到位，因尚無正式核准與媒體；這是製作送出前檢查，不能反過來說所有前期文件都未完成。

## 正式採用之後的執行順序

| 次序 | 具體行動／證據 | 開始條件 |
| --- | --- | --- |
| 1 | 站主審v3、資產採用清冊、兩期額度及分項上限；保留原話及對應SHA | 對這份具體包作決定；畫風接受不代替整包採用 |
| 2 | 將採用版本接回正常劇本與look流程；外部圖正式judge／choice／review，核對series-store和參照SHA | 原生來源仍一致，實際判圖與owner決定可追查 |
| 3 | 正常 `plan_lock --write --note "站主原話" --assist off`，附兩期逐鏡分配 | 明確採用此包後才執行；不手寫lock，不改計費常數 |
| 4 | 製作TTS、ASR／聽審及audio；依真實時間重算秒數／剪點／價檔 | 當次成本範圍、有效runtime與餘額已核對；原估23:23.533超原驗收上緣23.533秒，需實測處理 |
| 5 | 製作450張獨立首格及3末格，核對实际reference SHA與當鏡造型；關鍵影格animatic及storyboard審閱 | look與audio當前；不能以單人概念圖充當場景首格 |
| 6 | 原生ready全部適用項通過；先做下面三鏡連續動畫小樣 | 送出前帳號／頁面模型／秒數／2K／參照上傳／AI潤飾off確認；留請求與實扣收據 |
| 7 | 小樣實速觀看、逐格及匯入QA，站主接受才依場景批次放量 | 不用三張靜圖或不連續抽樣宣稱小樣完成 |

原生plan_lock只拒`refuse`；本版月配額問題為`waste`，正常寫鎖會保留警告。兩期配額不由原生鎖自動管理，執行者須按JSON每期shot清單及即時可用餘額檢查。已見27000的頁面快照不是可無限支用的預約。

## 唯一首批動畫小樣

| 順序 | 鏡號／剪入秒 | 具體起終與主要風險 |
| --- | --- | --- |
| 1 | a02-s035／3秒 | 寂聞從右側最後三級階下來停在跪於左側的姬前；殷留上階。固定全身鏡，驗階梯、腿袍與站跪高度 |
| 2 | a02-s036／1.733秒 | 右掌首格離實體冠脊1cm→落到冠脊即停，說「你不躲？」；人工C，驗指頭、穿透、冠鏈及接觸 |
| 3 | a02-s037／2秒 | 後頸銀髮首格完全遮印→一次風分髮→末格一個月牙；驗左右、胎記及與s038落髮銜接 |

同場連續6.733秒，每支買4秒。一次144點、人工期望240點、最多2takes合計288點；含10%管理預留264／316.8點。它們已在420支整集預算內，不重複計費。第二次同缺陷仍在即停止，改提接觸局部／前後狀態的具體變更；不能悄悄第三次重買、改still或循環補秒。

成功標準包含實速連看、身份和道具、动作可读、首格匹配／PSNR、ffprobe原生尺寸與音軌、下載／匯入可用性、request ID、首末格及正文SHA、實扣、採用區間與站主接受。H3歷史原生2K／24fps需首支再測，不以1080p／30fps交片轉碼冒稱生成原生規格。小樣沒有沈的動畫，沈的臉／冠／扇仍在其第一批逐項驗。

## 預算與未決欄

v3片段人工期望30494.4點、2takes上限44304點；含10%為33543.84／48734.4點。兩期分配分別236／184支，上限加預留26980.8／21753.6點。

新增API分項期望US$98.7016、上限223.1652，含10%為108.5718／245.4817；若兩期Max均需新付款，另外2×216＝432，已知項上限合計677.4817。內建imagegen實際美元、稅額、已付訂閱及未來額度未知，不能把677.4817當已支付總額或完整最終帳單。完整當日官方來源、費率假設及逐项算式見v3包。

送出前據實補：當期帳號／可用餘額／其他保留額、付款或續費授權、API有效模型／單集上限、圖像採用及look核准SHA、真實TTS時間、首末格SHA、storyboard與plan lock指紋。API提案上限高於文件中200美元預設，實際有效設定未查；沒有修改後端設定解除限制。

任何request回覆不明先查job、餘額和收據；不把timeout當作免費失敗重送。達單鏡／批次／額度期上限、同缺陷兩次、左右／身份或道具連戲不明，就停該鏡及依賴鏡，保留已有合格素材。

## 所有權及後續接線

[本交接票](../../../../../../tasks/open/2026-10-08-ou-de-jianghu-visual-handoff.md)目前只持有handoff範圍。production README過期角色數、正式工作檔採用與原試播票依賴接線，取得原持有人交接後再改；本README不是對另一持有者的機械鎖。第8集劇情與後續14人／16造型仍由各自票推進，不阻塞首集規劃包交審。

文件與工程透過既有草稿PR #1388保存。媒體原件存repo外，repo內保存來源、提示、版本、原生尺寸及SHA；沒有付費片段、TTS或正式影片輸出，也沒有填寫不存在的judge、choice、look、audio、storyboard或plan approval。
