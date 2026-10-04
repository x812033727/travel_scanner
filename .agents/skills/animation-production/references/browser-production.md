# Hailuo／Kling 內建瀏覽器製作：先驗三個連續鏡頭

使用者指定 Hailuo 或 Kling，並提供內建瀏覽器時讀。本次 route 沿使用者指定的網頁；CLI／MCP 只有另行選用才切換。風格與鏡位讀 `.agents/skills/animation-camera/references/budaimiao-style.md`，產線匯入程序只在 `stage-preconditions.md` 最後一節；這份管網頁準備、pilot、送出收據與看片，不新增 `video.json` 欄位。

這是製作方法，尚未證明任何模型能達到參考質感。技能更新、開瀏覽器或指定風格本身不等於已授權付費生成。**送出第一支之前先完成 `.agents/skills/animation-preproduction/SKILL.md` 的開拍鎖定包**：分鏡表、每鏡路線與秒數、首尾格、定稿正文、風險、預算、批次順序都由站主確認一次（`plan_lock.mjs --write`）；這篇是照包執行。確認過的範圍內不再逐鏡問，包外的事（超預算、改鎖定的東西、重大缺陷）才再問；不自行訂閱、加購或上架。

## 1. 先查目的地與本次工具能力

**在付費生成前查目的地**：`tools/video/media/clips.mjs` 的 `importClip` 目前只要看見 `series.production.profile` 就以 3 拒絕外部片段，單改 profile 的 provider／model 不會解鎖。既有 profile 的正片須另做受核准的產線支援與契約更新；不能刪 profile 或把 Hailuo／Kling 來源偽標成 Veo。先做沒有 profile、來源與授權明確的 pilot，或完成已有目的地的正常前提。

使用者登入並提供該次分頁後，先讀當前瀏覽器工具回傳的完整 API 文件與頁面狀態。只用其記載的控制、upload、download 方式；本次看見的工具能力才是依據。歷史 Claude 桌面版缺本機 upload 的結果不是 Codex 的能力證明。

| 能力 | 本次要確認與記錄 |
| --- | --- |
| 分頁與登入 | provider、實際建立頁、使用者提供的分頁、讀取日；只記是否已登入，不記登入資料 |
| upload | 工具是否有正式的檔案上傳 API；若可用，確認上傳的是本鏡核准首格，頁面預覽已載入 |
| download | 工具是否有正式下載／保存方式，是否回傳可用本機檔案；下載後檔案可讀且與所選 job 對應 |
| 表單 | 當前可用模型、比例、解析度、時長、參考圖、首／尾格、音訊與多鏡選項；把沒有的欄位記 `not_available` |
| 成本與歷史 | 本次生成顯示的點數、餘額、job／歷史頁；現有隊列可讀，結果可查回 |

能力分開記 `verified`、`not_checked`、`not_available`。如果 upload／download 沒有已記載的方法，就先整理已核准圖片與提示包，請使用者完成缺少的檔案步驟；不要偷換成文生影片試驗首格一致性，也不要接觸 browser profile、cookie／權杖或用頁面注入繞過檔案限制。遇登入或站方挑戰由使用者處理，不繞過。

## 2. 每鏡的輸入：核准首格、一個動作、一個連續鏡頭

在正文生成前完成正常 `look`／`audio`／`storyboard` 前提，跑 lint、craft、shot_reading 與估價。每鏡要買幾秒、首尾格、要貼的定稿正文與它的 SHA-256 來自鎖定包（`animation-preproduction` 的 `shot_plan.mjs --route hailuo|kling`）。`clips --dry-run` 不能拿來規劃：它要 storyboard 核准後才跑得起來（`tools/video/media/clips.mjs`），印的又是伺服器的模型與價。`plan_lock.mjs --ready` 沒過的項目先補齊。

- 首格用此鏡 `keyframes/manifest.json` 中通過的採用圖，核對圖片 SHA-256 與 manifest 的 look／visual 綁定。先確認圖片預覽，再設定參考圖；末格只有分鏡需要且模型支援時才加。
- 長片預設 **16:9**。每次送出前從表單核對比例、模型、解析度與時長，避免沿用上一鏡；2026-10-04 的 Hailuo 歷史 UI 預設是 21:9，不推定今天仍相同。原片 2K、768P 或 720p 要如實記錄，不稱為原生 1080p。
- 提示正文由 `motion`（誰做什麼、幅度、收勢）＋ `camera`（景別、角度、一種運鏡）＋沒有全域運鏡的 `look.motion` 組成；額外限制保留已核准 `look.negative`。圖片的 `prompt` 不會自動進影片模型，動作需要的起點與對象在正文中重述。
- 一次要**一個連續鏡頭**，每鏡一個主要動作。Kling 3.0 把 Multi-Shot 關掉（官方：關掉時預設單鏡）、原生音訊關掉、輸出數設 1；Hailuo H3 沒有關音訊的開關（官方），正文的 `overall_soundscape: N/A`，產線丟棄音軌。Hailuo 的 AI Polish、Kling 的 AI Prompter（關掉時嚴格照你的字）照鎖定包設定並記進收據。CLI 的 `enable_audio`／`prefer_multi_shots` 是 CLI 欄位名，不當成網頁 API。
- 運鏡照各家官方的寫法（`animation-preproduction/references/route-decisions.md` 第六節，2026-10-04 讀）：Hailuo H3 用官方圖生影片格式、運鏡寫成「種類＋幅度＋速度」的句子；方括號指令官方只寫給 Hailuo 2.3／02／Director；Kling 3.0 用自然語言。模型照不照做仍要小樣看，不能靠關鍵字聲稱已執行；Kling 社群 MCP 的 camera control 不是網頁語法。
- 生成秒數要蓋住原配音時窗、主要動作與收勢，從網頁實際可選的檔位取足夠的最短值；不照 Lite 固定 8 秒，也不以凍格、循環或變速掩蓋動作不足。

## 3. 三個連續鏡頭的 pilot

**先做同一場戲中相鄰的三鏡，再擴大**（此次工作預設，編輯判斷）：要看得出空間／人物關係、來源允許的一個主動作，以及它帶來的反應或結果。依既有分鏡選段，不為湊項目加角色、台詞或劇情。三張各自漂亮的孤立圖不能代替這段。

第一次先送第一鏡，確認 route 的首格、輸出與收據可查，再做另外兩鏡；三鏡採同一模型與輸出檔位以便比較。每鏡沿已核定 take 上限；未另定時最多 2 take（沿用 `MAX_CLIP_TAKES` 的保守工作預設），每個 take 都記下，既有更嚴的額度優先。重複重大缺陷就停該分支，保存證據。

**內容性失敗不要當場改 `video.json`**：`motion`、`camera`、`prompt` 都在 `visualHash` 綁的 `scene.data` 裡（`tools/video/core/timeline.mjs`），改一個字 keyframes manifest 就重建、每一鏡再 judge 一次、storyboard 核准失效、已匯入的外部片段要重匯（clips manifest 從空的重建）。記下失敗與想改的寫法，三鏡看完一起改：`plan_lock.mjs --check` 出變更單、站主點頭、一次改完、重鎖。只換網頁正文而不動 `video.json` 也是變更（定稿正文的 SHA-256 會對不上收據），一樣走變更單。

pilot 以原已接受的配音試剪、CC 沿作品設定，生成音軌不混入。使用正常後製與檢驗條件；未滿足匯入前提就如實記「外部素材待匯入」，不手改 manifest。以實速看三鏡的視線、方向、動作接觸與收勢、鏡位切換、顏色／角色／道具一致，再逐幀查疑點；抽格只能證明那些影格的狀態。

另一名沒寫提示的審查者依 `visual-quality.md` 冷看，分開回報技術、美術、敘事表演、剪輯聲音以及使用者接受狀態。三鏡與指定參考的相似處、差距及尚未檢查項目寫清楚；遇只能抽格或無法聽音時保留待驗。沿既有接受流程固定方向，達到已接受標準後才擴下一小批；不新增每鏡一次批准，也不以 job ready、QC 或 judge 過線代替接受。

小樣之後照鎖定包的批次順序送：每場母鏡頭先、再 C、B、A；第一場做完是檢查點，用 `animatic.mjs` 把買到的素材換進動態分鏡實速看，查漂移與連戲。照併發送（Hailuo Pro 以上 2 支同時、排隊 8–12；Kling 一次一份輸出），不要一口氣把整集排進隊列：中途發現的問題只會影響還沒送的。

## 4. 每一次送出與下載的收據

每鏡每 take 的附加紀錄放 `<VIDEO_WORKDIR>/<SLUG>/`，可以用 Markdown／JSON，不改 `video.json` schema。沒有讀到的值填 `not_available` 或 `not_checked`，不要猜。

| 類別 | 必留欄位 |
| --- | --- |
| 身分與輸入 | slug、shot id、take、來源版本、look／visual／speech hash、採用首格檔與 SHA-256；有末格／參考圖也記採用檔與 hash |
| 請求 | provider 與 route（`hailuo-web`／`kling-web`）、模型、實際提交提示文字及 UTF-8 SHA-256（要等於鎖定包的定稿正文）、negative 的實際輸入方式、16:9／解析度／秒數、音訊與單鏡設定、輸出數、AI Polish／AI Prompter 開或關 |
| 送出 | 送出時間、頁面顯示的估計點數、送出前餘額、job id／可查的歷史項目；只送一次 |
| 結果 | 完成／失敗／未知、完成時間、送出後餘額、實際扣點差額與退款狀態；未知不填 0 |
| 下載與驗證 | 所選 job、官方下載選項、檔案 SHA-256、ffprobe 實際尺寸／fps／時長／音軌、浮水印觀察、採用區間、QC／judge／冷看／接受狀態 |

點擊生成之後遇逾時、頁面斷線、餘額變化或拿不到 job id，**先查當前隊列／任務歷史與餘額**，用首格、提示與設定紀錄對應結果。正在跑就繼續等，已完成就取同一份，失敗先核對狀態和退款。結果仍不明時記 `unknown` 與可能扣點，不以新 job 或改提示重送；繼續不依賴此素材的離線工作。查詢成功不等於素材接受。

下載走官方無浮水印選項，完成後實看畫面角落與整段，不直接把卡片播放網址當可交付母帶。Hailuo 曾有卡片播放檔含浮水印、官方無浮水印下載另給乾淨檔的歷史實測；Kling 本次選項要從 UI 核對。遇下載失敗先取回同一 job，不重買。檔案與私人收據不進公開 repo。

## 5. 進產線與狀態回報

依 `stage-preconditions.md` 的唯一匯入程序執行。Hailuo 網頁用 `--provider hailuo-web`；Kling 網頁用現有 `--provider external`，在 `--note` 記 `route=kling-web` 及外部收據位置／job id；`kling-mcp` 留給 CLI／MCP，來源不偽標。點數用實際差額、美元有可查換算才給；不給美元時帳本的 0 不代表免費。

`clips import` 跑本機 ffmpeg QC；`--judge` 另是沿授權預算的一筆模型評審，不帶它就不要宣稱已 judge。首格 PSNR、黑格／凍格／切鏡通過不代表沒有浮水印或像參考，技術問題也不靠 `--force` 宣稱過關。保留正常 manifest 與核准 hash，不手改 passed。

收工分開報：已寫分鏡、已送出 job、外部 ready、已下載、已匯入、QC、judge、實速／聽音／冷看、使用者 accepted；附每鏡費用與所有 unknown。沒有生成或只改提示就是待試拍。發布仍沿原本的 final／publish 流程。
