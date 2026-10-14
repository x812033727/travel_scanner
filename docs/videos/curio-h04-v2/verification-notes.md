# H04 v2｜來源重讀與證據界線

2026-10-14，來源重讀與製片界線筆記。新版逐項來源覆核見 `verify-1.md`；先前 `e9062e4ca246f5d0` 與 `7990f638c3485877` 的獨立盲審各通過 11/11，但後續嚴格重讀指出相鄰台詞重複及搜救時序跳接。站主選定搜救卷宗接法與片頭明示回扣後，**現行** narrative hash `bd49404ff2771d33` 已獨立盲審 11/11 通過，speech hash `939e267cecc8f2cb` 的旁白已正式檢查、後台核准並拉回。下文保留各輪當時的 hash、限制及失敗原因；最新畫面結果另見下一段連結，不把過往段落當成當前的成片播放或站主驗收紀錄。

**最新畫面補充：**保留三個 `shot` 的開場修訂小樣又各做一張 MiniMax，只有 `opening-search` 是條件候選；`opening-inside` 的樹林背景及 `opening-gear` 的具鞋帶靴款／不同帳內佈局均人工退件。三鏡未通過連戲，沒有 storyboard 核准或全片擴批；詳見 [修訂小樣](./visual-pilot-three-opening-revision-20261014.md)。這次只改圖像提示，旁白與音訊核准雜湊未變。

`brief.md` 是已核准選項 A 所綁定的大綱快照，保留了撰稿時「未做旁白」和「下一步審稿」等舊狀態及預估時間。為免使大綱核准雜湊失效，不在該檔追寫進度；本筆記與 `verify-1.md` 記錄目前的審稿、音訊及媒體關卡。

## 本輪直接重讀的歷史卷宗

- [1959-05-28 結案決定書第 384–387 頁俄文轉錄與掃描索引](https://dyatlovpass.com/case-files-384-387-ru)：第 384 頁列十名成員、尤丁因病折返；第 385 頁記 2 月 26 日找到帳篷，設備、幾乎全部鞋子及外衣留在帳內，「突然離開」為調查員推論；第 386 頁記 8–9 組不同鞋襪的足跡近林緣被雪覆蓋、林邊火堆旁兩人、朝帳篷直線上的另外三人，以及 5 月 4 日在溪溝旁約四至四點五公尺積雪下找到最後四人。三人中僅 Slobodin 和 Kolmogorova 的姿勢被卷宗解讀為像往帳篷爬；Dyatlov 仰臥、頭朝帳篷。這些都不是逐人行動目擊。第 387 頁以自然力量概括結論，未指明雪板機制。英譯只作閱讀便利，關鍵語應由俄文掃描對照，不把英譯當另一份證據。
- [1959-04-16 帳篷鑑定第 303–304 頁俄文轉錄與掃描索引](https://dyatlovpass.com/case-files-303-304-ru)：鑑定依切口旁布料內側的表面傷痕，判定刀切由帳內側作出。它沒有證明動刀者、九人各自的出口或離帳順序。`h4v033–h4v034` 留在這個範圍。
- [Tempalov 訊問第 309–312 頁俄文轉錄與掃描索引](https://dyatlovpass.com/case-files-309-312-ru)：第 312 頁說確認 8 組、第 9 組未確認；足跡顯示所見短段像正常步行，未稱測量步距。`h4v019–h4v025` 不把它延伸成全程路線或全員情緒。
- [Slobtsov 訊問第 298–300 頁英譯與掃描索引](https://dyatlovpass.com/case-files-298-300)：記 2 月 26 日下午發現帳篷、當日除雪見帳內無人、足跡是相對周遭雪面凸起的壓實形。影片的足跡插圖只是概念示意，不復原個別鞋底。

## 科學文章與必要更正

- [Gaume、Puzrin 2021 原始研究](https://www.nature.com/articles/s43247-020-00081-8) 題為小型雪板的釋放與撞擊機制。公開摘要／索引及第一版獨立來源讀取支持局部較陡地形、埋藏弱層、搭帳切坡與風搬雪的條件組合。研究用推定時距檢查模型，不能把模型數字當成獨立測出的當夜時間；本片也沒有口播精確延遲時數。
- [Puzrin、Gaume 2022 後續考察 Comment](https://www.nature.com/articles/s43247-022-00393-x) 指 2021 年地形量測與後來鄰近坡的新雪板痕跡。**2022-01-28 出發到現場的是兩位當地專業嚮導 Oleg Demyanenko 與 Dmitriy Borisov**；研究者組織考察，文中沒有說兩名論文作者當次親自上山。本版 `h4v007`、`h4v081` 已改為「兩位當地嚮導」。看到的是雪崩**事後痕跡**，不是滑動過程影像，也不是 1959 年當晚同一片雪。
- 撰稿時 `web.open` 對 Nature 的讀取遭身分驗證轉址，當時只取得搜尋摘要。後續獨立查核已直接讀回出版方完整 HTML 與 2022 年 Comment PDF，讀取結果和主張核對記於 `verify-1.md`；這段保留為撰稿輪的歷史限制。
- 2019／2020 檢方表述來自 [Interfax 2019](https://www.interfax.ru/russia/649229)、[Interfax 2020](https://www.interfax.ru/russia/716956) 的記者報導與引述；本版只說對外說明複查及記者會提出雪崩說法，不把報導當完整官方報告。

## 來源畫面與產物狀態

- 三張文件裁切分別對應 [Commons 385](https://commons.wikimedia.org/wiki/File:Dyatlov.Volume_1.Page_385.jpg)、[386](https://commons.wikimedia.org/wiki/File:Dyatlov.Volume_1.Page_386.jpg)、[387](https://commons.wikimedia.org/wiki/File:Dyatlov.Volume_1.Page_387.jpg)。頁面列 Lev Nikitich Ivanov、1959-05-28、`PD-RU-exempt`；Commons 的原始來源欄是民間論壇，不是官方檔案館直供。裁切僅保留公文文字，沿用第一版 `asset-register.md` 記錄的區域與像素核對。新 `stock/` 檔在 repo 外 H04-v2 工作目錄，三檔的 SHA-256 均與檔名相同。
- 舊草稿的九張 SVG 已依奇聞系列畫風規格改為三個 MiniMax `image-01` 鏡頭與六張文字卡，九筆 SVG 資產及檔案不再使用。`video.json.assets[]` 只列三張公有領域文件裁切；換圖後 `renderProblems(doc, root, {workdir})` 的檔案與來源靜態預檢回傳空清單。新增鏡頭仍須實際生成和人工看圖；靜態預檢不是成片播放驗收。
- 本版 `youtube.video_id` 為 `null`。舊 H04 的私人上傳 ID 與媒體收據不移植。現行 100 句語音的時間軸長 8:40、語音雜湊 `ed9b3d4509f1a7b9`，`review/check-flags.json` 為零標記；音訊審查推送自動核准，拉回後 `status` 顯示 `narration approved`。先前 101 句、8:41 的檢查與核准只屬歷史版本。至本次視覺修訂前，H04 累計生成 201 張 MiniMax 圖、199 次判圖，帳本約 US$2.69；本次增加 14 張圖與 14 次判圖，約 US$0.19。最後全站讀回為圖片 9,139／10,000、判圖 10,014／11,000。新 `look.style` 與 52 張鏡頭的提示詞已通過 lint 和一張一 take 的全片 dry-run，尚未以新 look 生成圖片。分鏡、渲染、字幕、MP4、上傳包、站主播放驗收及 YouTube 上傳均未完成。

### 視覺小樣與暫停紀錄

- 舊 look 的三張開場小樣最終通過 judge 與人工構圖檢查；`opening-inside` 僅是帳內示意，不宣稱重建當年帳篷內部。接著的一 take 首輪新增九張圖，有七張遭 judge 退回。`remaining-boots` 的服務請求以終局上游錯誤結束，費用 US$0；當時媒體工作與保留額均為零。依專案 STOP 流程在安全邊界停下，沒有第二 take 批次。
- 人工逐張檢查 12 張已選圖片：`tease-fabric` 呈現照片感與過大的切口；`tease-file` 頂端有黑邊；`tease-paper` 和 `camp-platform-context` 有角落簽名或浮水印；`tease-expedition` 將步行嚮導畫成坐在長椅上；`opening-question` 有照片／3D 感與不符敘事的樹林；`trail-search-start` 雖經 judge 通過，足跡卻像分離的大雪塊；`journey-pack` 有照片感；`search-later-weather` 未清楚畫出風化的凸起足跡。這些是插畫品質與敘事對位缺陷，不改寫史料主張。
- 修訂在全片 `look.style` 明示純手繪線條、平面 2D 色塊、每種物件皆遵循同一畫法、滿版 16:9 且角落乾淨，並以正向詞句指定道具是普通無表情的無生命物件。十張鏡頭的場景提示詞縮短或修正，包括無樹坡面、步行嚮導、概念性凸起足跡與風化淺痕；風格只放在 `look.style`。舊 look hash `0f2ff6840b867375` 改為 `c9ddd653e1d021c2`，picture hash `59713eec7b8ed03b` 改為 `1d268431c42f509a`。舊 manifest 與 12 張選圖已保存在工作目錄的 `keyframes/audit-pre-look-revision-20261014/`；全部只是稽核證物，不是現行分鏡。
- 新 look 擬先以 `opening-question`、`trail-search-start`、`journey-pack` 三個連續鏡頭各一 take 試畫，dry-run 三鏡均在提示詞長度上限內，估計約 US$0.04；完整 52 張一 take 約 US$0.70。專案 `STOP` 仍存在：授權後清除該檔的操作遭自動政策阻擋，沒有改用其他刪除或移動方式，也沒有以新 look 付費試畫。待 STOP 由受支援的方式解除後，須先重讀額度／保留額，再執行已授權的三鏡小樣並逐張人工檢查。

### 第三輪三鏡小樣與畫面路線（2026-10-14，較上段新）

站主其後自行解除專案 `STOP`，製作端讀回為不存在。第二輪失敗後，`look.style` 只保留畫法、配色與構圖，移除會污染每張圖的帳篷、足跡等物件名；三鏡提示也在離線修正。當前 `video.json` SHA-256 為 `8bda81b1d4bdcb7106d5541d0968c3bf5308f718b58804f687b1330b079b4dbd`，look hash `b252d62b5b2f560d`，pictures hash `cf6e39349f507852`，旁白敘事雜湊仍為 `e9062e4ca246f5d0`。第三輪各一 take 的 manifest SHA-256 為 `e509539b62932850a87350cbd09ef48988d314beb8a6a06dffc08d564fbb65f1`。以下是實際打開三張輸出後的觀察，並非只讀 judge 分數。

| 鏡頭 | 實際查看圖檔 SHA-256 | Judge | 人工觀察與狀態 |
| --- | --- | --- | --- |
| `opening-question` | `opening-question-1-trim.jpg`：`b89c5432d2aee27a219b7b089c42f5948f33b5424bf9de976fb2ec415ecf26a6` | 9.71，**未通過**：右下紅色簽名印 | 單一空帳篷、無樹雪坡與 2D 畫風可讀，但紅印裁切後仍可見；不可採用。 |
| `trail-search-start` | `trail-search-start-1-trim.jpg`：`3bd03e7cdde5ecaa9e1d4dbe1dafbb771e2cbbb36bb4c4358642452b29ecd26d` | 9.29，**通過**；細節題指出長裂縫不像三個足印 | 兩名搜索者與森林方向可讀，但前景是數道連續雪裂，不是來源所需近乎貼平的舊足跡；人工未通過。 |
| `journey-pack` | `journey-pack-1.jpg`：`d16106f9d1a438550b7c056eea062d89caaab55332ded780926df80f780ba2f4` | 9.00，**未通過**：照片畫風與正面機位 | 背包被畫成桌上正面寫實照片，與 2D 插畫及俯視單扣帶要求相反；不可採用。 |

三張圖及前兩輪圖片、判圖與費用收據保留在 repo 外工作目錄；完整第三輪紀錄見 `review/pilot-revised-look-20261014.md`。**本輪不能作為 52 鏡全片批量生成依據**：零張同時通過自動判圖與人工敘事對位，且第二輪的缺陷並未因增加提示詞而穩定消失。這只判斷當前影像路線，並未否定已核准的旁白或史料查核。

下一步應先把每鏡的畫面任務拆開：MiniMax 插畫可用於無精確證物要求的雪坡、空帳篷、林緣、檔案桌等氛圍場景；足跡的凸起形態、帳篷切口方向、卷宗日期與文字、雪層弱層／平台／小雪板的幾何關係應由已登錄的原件裁切、現有 `big`／`compare`／`steps` 字卡，或另行繪製並逐項核對的**明標「示意」**圖承擔。`trail-search-start` 若仍是插畫，只讓兩名匿名搜索者在山坡上朝林線尋找，精確足跡形態留給隨後有來源的卡片；`journey-pack` 所在旁白只說隊伍中有已工作成員，道具背包不能替代身份證據，宜改成有卷宗來源的簡潔字卡。開場帳篷畫面需先解決紅印、重新判圖與人工看圖，不能直接覆蓋或忽略失敗收據。

可先逐組改分鏡而非逐張盲抽：`trail-search-start`、`search-later-weather`、`trail-varied`、`trail-downhill` 的插圖只交代搜索者、地形與時間差，凸起壓實雪及足跡種類由 `document-footprints-slot`、`boot-print-evidence`、`footprint-count` 的來源文字與明標示意圖交代；`tease-fabric`、`search-two-times`、`fabric-workbench` 的布面畫面只作鑑定桌氛圍，內側割出的結論留給 `tent-examination`、`inside-fabric` 與卷宗來源；`tease-paper`、`cohesive-snow`、`snow-platform-cut`、`slab-edge-displaced`、`small-slab-remains` 等模型形狀需要對照 2021 論文的**條件示意**，不能讓通用雪景替代機制說明。現行時間軸的插圖占比約 54.07%，最終 QA 至少要 50%、單張最多 8 秒；若把多鏡改成字卡／照片，必須重新計算節奏並以來源清楚、但仍合規的插畫鏡補回，不應靠重複同一張景觀灌比例。新的代表小樣應包含一張無浮水印環境鏡、一個來源卡／示意與其前後剪接、以及一個真正難畫的機制鏡；三者都需人工看圖與原旁白試播後才考慮擴批。

目前只確定三張卷宗裁切已登錄來源、作者、Commons 檔頁、`PD-RU-exempt` 標記及檔案 SHA；Commons 頁的原始上傳來源是民間論壇，並非官方檔案館直供。新增歷史照片或研究圖表時，須先逐張確認拍攝時間／地點、原始持有者、可用授權或必要引用範圍，保存原檔與裁切 SHA、URL、署名和片中標示，再加入 `assets[]`；不得把鄰近坡的後來照片剪成 1959 年現場，也不能把生成示意誤稱史料。尚未取得新照片授權或做任何新素材匯入。本路線尚是離線設計建議，未改 52 鏡分鏡、未產生新圖片或成片。

### 離線來源重配與混合小樣預檢（2026-10-14，較上段新）

第三輪三張圖與 manifest 已原樣複製到工作目錄 `keyframes/audit-third-hybrid-replan-20261014/`，manifest SHA-256 仍為 `e509539b62932850a87350cbd09ef48988d314beb8a6a06dffc08d564fbb65f1`。原始三張圖、判圖回執、先前兩輪與費用收據均保留；新設計不把它們當作可用畫面。旁白 `script.md` SHA-256 `3bfdfb11bccfb8e1f017cdd6edcfdc9c4b1b5bee491e049f8e081dfd56ad8fae`、100 句及語音雜湊 `ed9b3d4509f1a7b9` 未變，也未重做音訊。

現行 `video.json` SHA-256 為 `0e77893bbeb425bef3b8fdefb2cca287b1ec3405809371b78e06a73a2e20b4c9`，look hash `6bb6c75bf6919df9`、pictures hash `8c6e69ce5bb26dd0`。新版全域畫風拿掉容易變成簽名紅印的紅色點綴；`trail-search-start` 只畫匿名搜索者朝林線尋找，不要求模型畫出精確足跡；`search-later-weather` 只作風雪時間差氣氛。`journey-pack` 改用結案書卷一第 384 頁支撐的成員身分字卡；`trail-varied` 改用原創足跡概念 SVG；`slab-edge-displaced` 改用原創有條件小雪板 SVG。這些是視覺路線變更，沒有改寫旁白或史料結論。

兩張 SVG 已在 `assets[]` 登錄為 `Mokaair original`，不取用研究論文的圖版，也不冒充當年足跡拓印或雪剖面。`weathered-footprints.svg` SHA-256 `c4990a49728d85dd105778142f95a4e9cf688cd525939dff077341e4cbebd901`，依 [1959 結案書](https://dyatlovpass.com/case-files-384-387-ru)及 [Slobtsov 證詞](https://dyatlovpass.com/case-files-298-300)抽象示意風化後的壓實凸起雪面；`conditional-small-slab.svg` SHA-256 `dba1146cfee698c3705adccd699ccc791ad2995a09d19f72c872490f9b3b1cc1`，依 [Gaume、Puzrin 2021](https://www.nature.com/articles/s43247-020-00081-8)標明模型條件而非 1959 年剖面或時鐘。三張既有第 385／386／387 頁裁切實際檔案存在、SHA 與登錄檔名一致；Commons 頁標 `PD-RU-exempt`，但上傳來源欄為民間論壇，片中只以「結案書局部」呈現，不稱官方檔案館供圖。本輪無新增權利未查明的歷史照片或研究圖，也不使用 `photo` 卡；模板的 `diagram` 支援 repo 內 SVG，`screenshot` 使用已登錄的 `stock/` 裁切。

離線計畫在 8:40 實際時間軸有 49 個生成插畫鏡，插畫時長占比 `50.83%`（門檻 `50%`），98 個畫面狀態最長 `7.5` 秒（門檻 `8` 秒），`cadenceProblems=[]`。`lint` 為零錯誤、三個既有雪／冬季主題詞頻警告；`renderProblems` 亦為空清單。這些僅是分鏡與素材路徑靜態檢查，不代表全片可看。

首段選 91.53–121.30 秒五個連續鏡作混合小樣：`trail-varied` 原創 SVG（5.27 秒）→ `document-footprints-slot` 已登錄第 386 頁裁切（5.23 秒）→ `boot-print-evidence` 字卡（6.40 秒）→ `felt-versus-knit` 插圖（4.40 秒，**尚未生成**）→ `footprint-count` 來源比較卡（總 8.47 秒、分兩個各低於 8 秒的狀態）。已用現有 renderer 做七張**局部靜格**，放在工作目錄 `review/h04-hybrid-pilot-preflight/`；人眼讀回 SVG、卷宗裁切、身分卡與比較卡的排版／來源標籤。`felt-versus-knit` 僅 dry-run，提示詞符合上限，未付費、未產圖；整段帶旁白試播、生成插圖人工審圖、獨立盲審與站主驗收仍待辦。局部靜格不是全片渲染或 MP4。

分鏡模板參與敘事雜湊後，現行 narrative hash 已由盲審通過的 `e9062e4ca246f5d0` 改為 `7990f638c3485877`；`status` 正確顯示 storytelling panel `stale`。舊 11/11 不可沿用到現行設計，也不可據此展開 49 鏡付費批量。需對現行 hash 做新的獨立盲審，且混合小樣的待生成插圖須通過判圖、人工來源對位與實際影音試播，再決定擴批。

### 氈靴／襪子失敗小樣後的再重配（2026-10-14，現行狀態）

在上段 49 鏡混合方案下，`felt-versus-knit` 一 take 產出 `felt-versus-knit-1-trim.jpg`，SHA-256 `29bb8d9b710c87bb565032a6640e5fae29a90feb1b56b1e4d108e2f56f5914bc`。正常 judge 總分 9.71 仍**未通過**：`style=0`，整張是寫實照片而非平面 2D。人工打開圖片也確認氈靴與襪子可辨，但木桌與織物光影為攝影風格，不可當作 1959 年史料或本系列插畫。原圖、裁切、當時 manifest、ledger、state 都以原 SHA 複製到 `keyframes/audit-felt-hybrid-replan-20261014/`，原檔與舊收據未移除；snapshot manifest SHA-256 `0068f3591a6b4ed0b8d57c6962d7b70aa88d1aab50357e6bd86782d19796fe8a`，ledger SHA-256 `d7bc319d9ca5159d57e49047b97105db49949c703cab63edafdf638bf1c75b97`。Ledger 末兩筆是 MiniMax 圖 US$0.0035 與 Gemini 判圖 US$0.01，snapshot 累計 US$2.7845、208 圖、206 判圖、零保留額。此圖不經人工覆寫判圖而採用。

`felt-versus-knit` 於相同 108.43–112.83 秒改為自製 `diagram`：`felt-and-sock-types.svg` SHA-256 `975f735923d87f073a6474b5fa62fde26456dcfbed9415a03ff22f0c9917512e`，`assets[]` 登錄 `Mokaair original`、依 1959 結案書的鞋襪類型抽象畫普通薄襪與氈靴，片中明標**非當年實物或足印描摹**。局部 renderer 靜格 SHA-256 `27ffc763d080dd14ee41acbcc4beade76545bca3e3a3d247eb74f5e3542b8f0d`，`problems=[]`；人工看圖可讀兩欄類型、來源界線與通往下一張足跡數量卡的問句。仍未做整段影音試播。

為保留原規格至少 50% 的**生成插畫 `shot`** 時長，`empty-speaking-room` 在 261.17–268.00 秒、6.83 秒改成泛用無標誌的空講台場景鏡，承接 2020 年對外說法後「雪如何移動」的問題；不描繪特定記者會場所、人物、日期、旗幟或文字。此鏡只做一 take `keyframes --dry-run`，提示詞符合上限，**尚無圖片、更無人工或 judge 通過**。現行 `video.json` SHA-256 `1f9259a26c1a2ce2a0193952ac8a946c2f14a63340492467c37bf370066fd89d`，look hash `6bb6c75bf6919df9`、pictures hash `4bb5d93e066be4db`。實際 15,604 格旁白時間軸上，49 個生成鏡占 8,004 格／266.8 秒，即 **51.2945%**，比 50% 多 202 格／6.73 秒；98 畫面狀態最長 7.5 秒。`lint` 零錯誤、三個既有雪／冬季／continuous 詞頻警告，`renderProblems=[]`、`cadenceProblems=[]`。這是可行的**分鏡計算**，不是已有 51.2945% 合格成片畫面。

100 句旁白、已核准音訊、`script.md` SHA-256 `3bfdfb11bccfb8e1f017cdd6edcfdc9c4b1b5bee491e049f8e081dfd56ad8fae`、speech hash `ed9b3d4509f1a7b9` 均未變。上段模板 `7990f638c3485877` 的第 18 輪獨立盲審後來通過 11/11，但這次兩鏡模板交換使**現行** narrative hash 成為 `461d52806a07de55`，`status` 為 storytelling panel `stale`，不得沿用第 18 輪。MiniMax 連續小樣有簽名、照片畫風及內容錯位問題；史料精確鏡改來源卡／自製圖可降低風險，卻未證明剩餘 49 鏡的 2D 畫風可穩定通過。下一段畫風關卡可選 253.37–271.70 秒三個連續鏡：`review-timeline` 來源步驟卡 → `empty-speaking-room` 空講台生成鏡 → `slope-small-feature` 坡面生成鏡。先只生成、判圖並人工看空講台；通過後再決定是否畫坡面及帶原旁白試播。另須試播 91.53–121.30 秒五鏡來源圖卡串接，但它已無生成鏡，不能獨自證明 MiniMax 畫風穩定。須先新獨立盲審、有限量代表鏡判圖及人工對位、兩段試播，才能考慮批量；不能以靜態 51.29% 直接開整片。

### 相鄰重述修正與勘測畫面去虛構（2026-10-14，現行來源修訂）

嚴格敘事重讀指出 `h4v079` 已說無人機測地表、未量到當年的弱層，原 `h4v080` 又用坡形無法推弱層厚度／強度重述同一限制；`h4v093` 已說作者與校方使用同一批觀察，原 `h4v094` 再說文章數量不等於獨立重演，也重複。舊評語及回執留在工作目錄 `review/`，不改寫舊答案。現在保留兩個 line ID，`h4v080` 改為「研究團隊還安排下一趟冬季考察，想直接檢驗雪層。」；`h4v094` 改為「那這個模型，究竟解釋到哪一步？」。前者從量測界線推進到下一趟**計畫**，後者把來源同源性推進到模型範圍並由 `h4v099` 回答。兩句的情緒也分別改為「轉入下一趟考察，語速略提」與「問句上揚，停半拍」，因此都需要重錄，不可沿用舊聲音。

[EPFL 2022 作者訪談](https://actu.epfl.ch/news/intense-press-coverage-prompts-new-expeditions-to-/) 明說研究者**決定組織** 2022 年 1 月的第三趟考察，目的包括另一輪無人機勘測、雪剖面與穩定度試驗，卻因天氣無法執行試驗；[2022 年作者 Comment](https://www.nature.com/articles/s43247-022-00393-x) 說實際出發的是兩位當地專業嚮導。`h4v080` 只說研究團隊安排、**想**檢驗雪層，不說兩名瑞士作者本人當次上山或已取得剖面；`h4v091` 仍交代試驗被天氣阻礙。`claims.md` 因此將 `h4v080` 由 c37 移到 c42，`h4v106` 轉到 c38；`h4v094` 作 c44 的模型範圍提問，c43 僅覆蓋同源觀察。

三個 2021 地形鏡的 prompt 已去掉沒有來源的勘測者、手持測量桿、棕色外露土切面：`science-next-evidence`、`survey-step-close`、歷史 ID 仍名為 `survey-two-researchers` 的鏡頭都只畫**無人的連續草坡、局部坡度變化**，不冒充實地手工測量或可見地層。`snow-return-season` 從已切開的雪層剖面改成尚未測試的完整冬季雪面；`snow-return-question` 字卡收窄為「當夜雪層沒有直接剖面」。`shared-source` 比較卡第二欄改成「模型能解釋全部經過嗎？」對應新提問。這些只是來源安全的提示與字卡，沒有生成或核准新圖。

現行 `video.json` SHA-256 `bc8916fe1602fb5c0448936cf1e3b1aa85bb89d3c367bd1d6c938c3813c767d9`，重生的 `script.md` SHA-256 `59f7f68000cdfa0587d566e70eef5d390c0303cbcc5ea0f36bb37d24f276a1f6`；narrative hash `a9d39df4503a5de8`，speech hash `2e6221d584b4ab8a`，look hash `6bb6c75bf6919df9`，pictures hash `0261120cebbf8c56`。`status` 顯示 `timeline.json was built for an older script`、storytelling panel `stale`；原 100 句音訊與收據保持不動，尚未 TTS 或推送新審核。

Lint 零錯誤、三個主題詞頻警告；四個改過的 `shot` 一 take `keyframes --dry-run` 通過提示長度，無付費呼叫。`renderProblems=[]`。現行仍是 49 個 `shot`；用**舊實測時間軸只作改詞前的時長基準**，8,004／15,604 格為 51.2945%，98 畫面狀態最長 7.5 秒、`cadenceProblems=[]`。以改詞後腳本估時則插畫占 51.60%、最長 7.7 秒、`cadenceProblems=[]`。兩句重錄後的**新實測**節奏與 50% 門檻仍須重算，不能把舊時間軸視為新語音驗收。只做了三張局部卡片靜格，排版檢查 `problems=[]`，回執在 `review/h04-source-repair-preflight/`；未渲染整片或做帶新語音試播。

## 製片時仍須檢查

來源覆核已將「事實／當年調查者推論／後來模型假設／後來現場觀察／編輯判斷」分開；剪輯和字幕仍須維持此界線。尤其不可把八與八到九組足跡混成確定九條路、把四月內側切口說成目擊動刀、把五月結案詞說成官方確認雪板、把模型時間當成獨立時鐘，或把 2022 年兩位嚮導看到的鄰近痕跡當成 1959 年同一事件。示意圖和文件裁切也不可剪成當夜連續影像。

### 搜救敘事時序修正（2026-10-14，現行順序）

新獨立盲審對前一 narrative hash `a9d39df4503a5de8` 的十項必要題回答是，其 `one_line` 指出 h4v107 一開始跟足跡搜救，h4v009–011 卻回到出發／營地，h4v012 又回搜救。因此只移動 h4v009–011 三個完整場景到 h4v107 前，並把章節斷點從 h4v107 移到 h4v009；章名為「一人因病折返，九人繼續上山」，h4v009 人數卡標示「出發前｜隊伍人數」。現在冷開場止於 h4v008，接背景、最後營地，再沿足跡進入搜救。h4v009、010、011、107、012 的旁白與來源綁定均未改，未增加史實主張或畫面。

本次 `video.json` SHA-256 `5b2a1d5671bf1ddab54369d4ac7980e4dfc3c5455f5f6a3d626330e1d721d517`；重生 `script.md` SHA-256 `62893505b6be4ee326df5e2e1eed3f4c1089ca95abe5bdc8711db3af6a479ebc`。現行 narrative hash `2e0568274b4949ca`，speech hash `4f3031a715d75761`，look hash `6bb6c75bf6919df9`，pictures hash `7a1424ed1ba8de23`。詞句未變，但場景順序進入語音雜湊；要重新建立並核對時間軸，現行順序尚未通過音訊與敘事關卡。本次未執行 TTS、`check-audio`、付費生圖、整片渲染或提交審核。

Lint 零錯誤、三個既有主題詞頻警告；靜態渲染計畫 `renderProblems=[]`。新順序估計 15,473 格，49 個 `shot` 占 51.60%，98 畫面狀態最長 7.7 秒、平均 5.3 秒，`cadenceProblems=[]`。這些是乾跑估值，重建時間軸後仍須實測確認。

### 兩句重錄、實測與新盲審（2026-10-14，後續紀錄）

上節敘述的是時序修訂代理交件時的狀態。協調者先按新稿重錄 `h4v080`、`h4v094`，TTS 實報 **2 requests、38 billable characters**，其餘 97 requests 從快取取回。為重排場景，再按 `h4v009–011` 提前的順序重建時間軸，TTS 實報 **0 requests synthesized、0 billable characters、99 reused**。每次覆寫前均把 `timeline.json`、`approvals.json`、`narration.wav` 複製並驗 SHA 到外部 `review/audio-before-two-line-20261014/` 或 `review/audio-before-chronology-reorder-20261014/`；原始媒體仍可追溯。

重排後的正式 `timeline.json` SHA-256 為 `533ef139b2b4e96f984fd29fd536b6e806b14b2a8bd2de52520f2c60ca83b1cf`，`narration.wav` SHA-256 為 `9912b2fd05fb59ee07749610da38f0b57cc5ec2e312fd9f1e13c3fcede27dce7`。實際 **15,554 格／30 fps＝518.467 秒（8:38.47）**；98 個畫面狀態最長 7.5 秒，49 個 `shot` 佔 51.247%，`cadenceProblems=[]`。這取代上節的估時，但只證明時間軸與畫面規劃合規，並非影像已通過品質檢查。

正式 `check-audio` 首次轉錄一筆 146,284 位元組請求收到無明確代碼的 HTTP 502，請求 SHA-256 `1678c26e9ab58175f9d2e8fdd7df7b18ad602e2301816316b9338285a35919ce`，可能已計費，工具據此保留暫停檔。原暫停檔 SHA-256 `e2e16d95e968ccb9a9a258b924eeb09707ae5baedf7008a2cf98bf822441ba4b` 已保存於上述外部回執。站主明確准許**只重試一次**後，才對該 exact SHA 執行 `speech-journal forget` 並重跑；第二次成功，100/100 句已檢、83 句逐字相同、13 句只差同音字或語氣詞、4 句沿用 Jev 先前合格判定、**0 句旗標**，本輪新轉錄兩段、0 新 Jev calls。`review/check.json` SHA-256 `791971db3eac309da62aae70142aa2e5fb67842391fe231ffa849b8b6d17282e946c`，`review/check-flags.json` SHA-256 `9cc4312f86c600f5022aae70142aae9ff88b23632555ea32df56a051c9fa6601`；speech journal 現已無 held 項。另用本機 Whisper medium 聽 `h4v080`、`h4v094`，後者逐字對上，前者把「想／雪」轉成同音的「向／血」，這僅是離線第二意見。

另一次完全隔離的敘事盲審對**現行** `narrative_hash=2e0568274b4949ca` 判 **10 是、1 否**：`chapters_link` 指出開場 `h4v008` 問為何離開帳篷，第一正文句 `h4v009` 卻回到出發人數，沒有承接問題；前一版 `a9d39df4503a5de8` 則是 `one_line` 因搜救後回講出發而未過。兩次判詞分別保留隔離收據，不覆寫成通過。依 `youtube-video` 的兩輪未過須停等站主規則，下一版接法待站主選定；本輪**未把新旁白送成已核准**，舊 `approvals.json` 對新時間軸仍失效。

### 站主選定搜救卷宗接法與片頭回扣（2026-10-14，現行）

站主先選「保留強片頭，改用搜救卷宗帶出十人名單」，再選「保留片頭，正文首句明示回扣」。稿中 h4v107 緊接 h4v008 搜救疑問；h4v009–011 是事後卷宗對十人名單與營地的交代，未宣稱二月搜救者持有五月結案書。h4v048 明說「開場那兩位研究者」，h4v081 明說「開場那兩位當地嚮導」。h4v009 為畫面節奏縮短，h4v082 改為接上嚮導觀察；結尾 h4v102 以「或許」及直接證據限制回答開場。現行 `video.json` SHA-256 `8cd783e464607233a7ebdf4041618ca80a75181e768d4f14d0c09a179ed83ff3`、`script.md` SHA-256 `7366c0d7b972880b78daaf3327dc650c1417034a45b39ac11a15efc9cc2d3757`，narrative hash `bd49404ff2771d33`。新獨立盲審 11/11 通過，原始答案及匯入證據見 `narrative-review-callback-20261014.json`；外部 `review/narrative.json` 已記通過。上節兩輪失敗與中途 `3698a43458031807` 的通過均為歷史狀態。

覆寫前將舊時間軸、整段 WAV、核准、語音檢查與四句 WAV 複製到外部 `review/audio-before-callback-20261014/` 並逐檔驗 SHA。現行 TTS 實報 4 次合成、98 計費字元，95 次沿用快取。新時間軸 SHA-256 `65e48861f66a7437ba3218a6601c89a1b52040a03fbcc5252ebdc5278fc2bc71`，旁白 WAV SHA-256 `f6eeaff7f57e66453262a962ad382e84f00867f1c404c102f6d1c5b90cdb3abd`；100 句共 15,827 格，8:47.57。正式 `check-audio` 檢 100/100：83 句逐字相同、11 句同音字或語氣詞差、6 句 Jev 判可接受、0 句旗標。推送音訊審核後自動核准，拉回及 `status` 確認現行旁白已核准、敘事審稿通過。實測 49 個 `shot` 佔 7,963／15,827 格（50.3128%），100 個畫面狀態最長 7.7 秒，`cadenceProblems=[]`；離門檻只餘約 49.5 格。圖像仍是 MiniMax 離線方案，沒有已核准的全片分鏡或完成的 MP4、字幕、上架包。

### 站主加額後的三鏡小樣（2026-10-14，最新畫面關卡）

站主在各一張小樣後准許維持 MiniMax，對 H04／H05／H06 再各畫三個相鄰鏡頭、每鏡一次。H04 的 `opening-search`、`opening-inside`、`opening-gear` 已各產一張並判圖，增加 US$0.0405；詳見 [`visual-pilot-three-opening-20261014.md`](visual-pilot-three-opening-20261014.md)。人工與獨立覆核 **0／3 可採用為連續段**：搜尋者與帳篷上下坡關係錯、帳內畫風偏繪景、最後一鏡機位與前鏡場景不一致。正常 judge 的兩張通過與一張失敗均保留，退件圖不算現行分鏡已完成。音訊、敘事與來源核准狀態未變；未做新圖批量或整片渲染。
