# H04 v2｜MiniMax 畫面路線離線稽核（2026-10-14）

此筆記只盤點提示詞與現有來源資產，未改鏡頭、模板、台詞、順序或音訊，也未呼叫付費生圖。盤點當時的 `video.json` SHA-256 為 `e6cf1b146c59dfe8b10b2982e09b83de0672557fc821c4ce84a33778cccdfe8f`，屬歷史快照；後續片頭回扣修訂使現行 `video.json` SHA-256 成為 `8cd783e464607233a7ebdf4041618ca80a75181e768d4f14d0c09a179ed83ff3`、敘事 hash `bd49404ff2771d33`、speech hash `939e267cecc8f2cb`。畫面場景和提示詞沒有因此更動：全案仍有 49 個 MiniMax `shot`，只是待驗證配置。

## 來源與畫面分工

- 已登錄的三張 1959 年結案書裁切，分別在 `document-shoes-slot`（385 頁）、`document-footprints-slot`（386 頁）、`natural-force-slot`（387 頁）。資產表記錄 Wikimedia Commons 頁面、作者與 `PD-RU-exempt`；這是既有權利紀錄，不擴張成其他照片或論文插圖的使用權。
- 三張 Mokaair 原創 SVG 分別給 `trail-varied`（風化足跡概念）、`felt-versus-knit`（鞋襪類型）、`slab-edge-displaced`（有條件雪板模型）。它們明標非當年物件、足印描摹或實測剖面。足跡數量、布料切口方向、時間線、模型條件和來源同源性繼續由來源裁切／圖解／數據卡承擔；生成圖不能冒充這些證據。
- 49 個 `shot` 的風險分三組。下列 ID 完整覆蓋現行 49 鏡；分組是製片風險，不是圖像已通過判圖。

| 風險組 | 現行 `shot` ID | 後續處理方向 |
| --- | --- | --- |
| 高：會被誤讀為歷史現場或量測結果（24） | `opening-search`, `opening-inside`, `opening-gear`, `tease-fabric`, `tease-paper`, `tease-expedition`, `opening-question`, `trail-search-start`, `camp-platform-context`, `remaining-boots`, `trail-downhill`, `fire-site-two`, `search-two-times`, `fabric-workbench`, `spring-empty-ravine`, `ground-step-context`, `snow-platform-cut`, `model-snow-sample`, `small-slab-remains`, `wind-softens-edge`, `survey-drone`, `nearby-avalanche-context`, `field-camera-back`, `softer-snow-block` | 優先改成有標示的來源卡／程序化圖，或把生成鏡收斂成不聲稱復原的空景、普通物件。`opening-question` 另被指定為縮圖來源；現有圖像未通過時不得拿來做縮圖。任何更動須重新算時長。 |
| 中：概念地形／過程，須避免變成現場影像（10） | `tent-opening-empty`, `cohesive-snow`, `quiet-platform`, `wind-ridge`, `drift-deposition`, `science-next-evidence`, `survey-step-close`, `survey-two-researchers`, `snow-return-season`, `field-weather` | 保留概念示意界線；無人的連續草坡與未檢測雪面提示已比先前的勘測者、雪剖面安全，但仍須人工對來源看圖。 |
| 較低來源風險：泛用空景或檔案意象（15） | `tease-file`, `search-later-weather`, `forest-edge-absence`, `archive-closed-folder`, `archive-many-pages`, `archive-ribbon`, `empty-speaking-room`, `slope-small-feature`, `camp-open-question`, `smooth-surface`, `measurement-tools`, `separate-ridge`, `natural-slope-no-cut`, `same-evidence-folders`, `closing-folder` | 可作 MiniMax 畫風代表鏡；空資料夾、筆記本或講台只是意象，不當作真實檔案／儀器／記者會照片。所有鏡頭仍要通過 2D 風格與無簽名、無多餘文字的判圖。 |

**最先處理的具體問題：** `ground-step-context` 仍要求可見棕色土線與石頭，會把來源未支持的剖開邊緣畫成已量到的地形；`trail-downhill` 要三個特定凸起殘足印，過往小樣已無法可靠畫對，應由既有足印概念 SVG／卷宗裁切承擔；`nearby-avalanche-context` 與 `softer-snow-block` 要具體破裂形狀或用外觀表現雪板軟硬，容易把 2022 年後續觀察和模型條件畫成可直接目測的史料。`small-slab-remains`、`wind-softens-edge` 的斷緣與 `spring-empty-ravine` 的溪溝形狀也不可當成 1959 年精確復原。`fabric-workbench` 的手套手勢、`survey-drone` 的停放姿態、`field-camera-back` 的持機姿勢都沒有逐動作來源。`opening-gear` 的精確雙靴也有已付費小樣的寫實風格失敗先例。這些均是**未修改的待辦提示**，不可據此直接批量出圖。

## 覆蓋門檻與下一次更動

現行已核准語音的實測時間軸 SHA-256 `65e48861f66a7437ba3218a6601c89a1b52040a03fbcc5252ebdc5278fc2bc71`：7,963／15,827 格為 `shot`，即 **50.3128%**；高於 50% 僅約 50 格／1.65 秒。100 畫面狀態最長 7.7 秒、平均 5.3 秒，`cadenceProblems=[]`。下述舊時間軸例子只能解釋風險，若要換掉任何 `shot`，須以此現行時間軸重新算覆蓋額度，不能沿用舊估值。

若日後把高風險 `shot` 改為卡／示意圖，在總時長不變時，移出的 shot 格數不得超過當時約 49.5 格的門檻餘額加上其他**來源安全且已驗證**新增 shot 的格數。現有 `tent-opening-question` 與 `snow-return-question` 是承載提問／證據界線的卡片，不能直接轉成泛用風景補配額。需先提出逐鏡交換與新時間軸計算，再審來源、敘事雜湊與畫面；不要把足跡數量、切口方向、來源同源性或模型條件卡換成無標示生成圖來追百分比。每次改版都重跑 `illustrationShare`、`slideStates`、`cadenceProblems` 與來源／授權覆核，維持 `shot` ≥50%、每狀態 ≤8 秒。

MiniMax 先前第三輪有角落紅章、足跡內容錯位與照片畫風；氈靴襪子一 take 的正常 judge 9.71 仍因 `style=0` 失敗。下一筆付費小樣的**離線候選**是泛用 `empty-speaking-room`／`slope-small-feature` 與一個來源敏感鏡；屆時逐張留 manifest、SHA、正常 judge 與人工來源／2D 判讀，再做帶音訊的連續段試播。站主目前只選擇維持 MiniMax 並做離線規劃，尚未授權再次付費生圖；此輪沒有新圖、成片或播放驗收。

本輪離線檢查：`lint` 為 0 errors、3 個既有主題詞頻 warnings；`renderProblems=[]`；`ground-step-context`、`nearby-avalanche-context`、`softer-snow-block` 的 `keyframes --dry-run` 提示長度皆在上限內，沒有購買圖片。提示長度通過不等於畫面與史料通過。

## 2026-10-14 後續離線補件（現行）

前段是原始稽核快照。這次只更動 13 個 `shot.data.prompt`，沒有更動鏡頭 ID、模板、順序、camera、台詞、畫風、來源或素材檔：

| 處理 | 鏡頭 | 可檢查的變化 |
| --- | --- | --- |
| 不把史料記錄畫成精確現場 | `opening-search`、`opening-gear`、`trail-downhill` | 拿掉搜索者指向手勢、恰好兩雙鞋的虛構擺法、三個精確足印；保留搜救與山下森林的畫面關係。鞋襪種類和足跡形態仍由第 386 頁來源卡與原創示意圖負責。 |
| 避免虛構鑑定或發現時動作 | `fabric-workbench`、`spring-empty-ravine` | 布面保留一般材料細節，拿掉無來源的手套操作；春季溪溝只作未命名空景，不給出四名罹難者位置或實測地形。 |
| 模型和地形以概念圖讀法呈現 | `ground-step-context`、`small-slab-remains`、`wind-softens-edge`、`survey-drone` | 草坡改為連續草皮、沒有外露土層；小雪板與風化只畫局部相對關係；無人機是設備符號，不是現場停放或操作姿勢。模型條件與量測限制仍要讓來源卡／旁白說清楚。 |
| 2022 年後續觀察保持證據界線 | `nearby-avalanche-context`、`field-camera-back`、`softer-snow-block` | 兩處痕跡改為抽象標記、相機改為普通靜物、雪面只作鬆散質地意象；這三鏡不能當作考察照片、當年雪層樣本或雪板硬度測值。 |
| 單張 MiniMax 小樣候選 | `empty-speaking-room` | 空講台提示只描述可見的無標誌講台、空椅與素牆，移除列舉式負面限制。這是泛用意象，可測 2D 畫風、假文字與角落簽名；通過一張也不能推定雪坡或證物鏡會通過。 |

提示詞鎖定時 `video.json` SHA-256 為 `bf31048cfd52326eb46cf688c12e298af94b0d06c071cd4eb42df59ae7de94e4`；單張出圖後僅修訂 `youtube.description`，將對外不可讀的 `claims.md` 提示換成四個主要公開來源連結、圖像性質揭露和給觀眾的開頭說明。**現行** `video.json` SHA-256 因 metadata 變成 `cc74761fbe854d47e16011cae78fef032fc600f3e41aef6c502aba92d6a17658`，picture hash 仍是 `d6930252d1790616`；narrative hash `bd49404ff2771d33`、look hash `6bb6c75bf6919df9` 和核准旁白所綁的 speech hash `939e267cecc8f2cb` 皆不變。現行 `timeline.json` SHA-256 仍為 `65e48861f66a7437ba3218a6601c89a1b52040a03fbcc5252ebdc5278fc2bc71`，`narration.wav` SHA-256 仍為 `f6eeaff7f57e66453262a962ad382e84f00867f1c404c102f6d1c5b90cdb3abd`。舊圖像、判圖和費用回執留在 repo 外；新的 picture hash 不沿用歷史圖像結論。

本次 `lint` 為 0 errors、4 warnings：雪／broad／winter 三個詞頻提醒，以及 `model-paper-card` 的**估算** 8.2 秒提醒；用核准旁白實測是 100 個畫面狀態、最長 231 格＝7.7 秒，`cadenceProblems=[]`。`illustrationShare=7963/15827=50.3128%`、`renderProblems=[]`；49 個 `shot` 的 `keyframes --dry-run` 全通過提示長度，0 超限。單張候選 `empty-speaking-room` 的乾跑為 351／1181 字元，畫面尚未生成或判讀。

片身字幕可在正式成片前依已核准語音作離線逐句預檢，但工具的正式 `captions` 需要 `assemble` 後的片頭片尾品牌雜湊。外部 `review/body-captions-preflight-20261014/` 存有**片身時間從 0 起算、不可直接上傳**的 zh-TW SRT／VTT：100 句、101 cues、缺句 0、`checkCues` 問題 0；當時的 SRT SHA-256 `8ef77ec5b9dd16d4a768cad55e16e22864402eb12f7c57ec889b9675b460b08b`。這份暫定字幕綁上列同一個 timeline／WAV，畫面 prompt 修訂不改字幕文字或時間；正式成片後仍須重新跑 `captions`，核對片頭片尾偏移、整片播放和 CC 同步。第 386 頁來源裁切卡、足跡數量卡與氈靴／襪子 SVG 卡已逐張打開檢視局部靜格，能讀到來源標示與「示意」界線；它們不是完整 storyboard 或連續有聲小樣。

站主其後授權 H04、H05、H06 各**一張** MiniMax 小樣；協調者以 `--shot empty-speaking-room --takes 1` 生成 H04 的這一張，沒有啟動其餘 48 鏡。`empty-speaking-room-1-trim.jpg` SHA-256 `39a698ef3c60b51264adf8dd92e4503c1514394007dbf5afe6cfb2892db8c3c6`；現行 manifest SHA-256 `64c8d3906a06da9701e41a31b14b9418344bfd6b22514d70bef99ca1473d902e`，其中 look／picture hash 與上文相符、該鏡 judge 10/10、`needs_review=false`。人工打開圖檔可見平面 2D 空講台、空座椅與一大片空白投影幕；沒有可見人像、假文字或角落簽名。它可作泛用轉場**候選**，但空白幕佔面積大，未經與旁白及相鄰卡片實速試播；此一鏡也不能證明雪坡、帳篷、鞋或科學機制鏡會穩定過關。完整 keyframes／storyboard 關卡仍未過。

縮圖仍指向未通過的 `opening-question`，不能把舊輸出用作縮圖；沒有正式 CC、完整 MP4、QA 或上傳包。片身暫定 SRT／VTT 已在 metadata 修訂後重算，字幕 SHA 與前段相同；外部 `review/body-captions-preflight-20261014/receipt.json` 的 SHA-256 現為 `439a60d349fa20222ef4dbb41b48eef21bac2ffe1ee2ecb394d0e4d23664ba8c`，`video_sha256` 欄對應上文現行 metadata，仍非正式上傳字幕。
