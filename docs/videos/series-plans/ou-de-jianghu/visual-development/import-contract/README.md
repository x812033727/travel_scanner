# 外部基底角色圖匯入合約

2026-10-08：本票實作 `look import`，把外部 PNG 保存為正常 look 的待判圖候選。工程測試使用隔離的測試圖片及假媒體服務；這份合約不代表首集圖像已匯入、判圖通過、站主採用或正常 look 已核准。

## 命令與狀態

```powershell
node tools/video/cli.mjs look import --slug ou-de-jianghu-e001 --character shen-guihe --image C:/media/shen-sheet.png --source C:/media/shen-source.json --dry-run
node tools/video/cli.mjs look import --slug ou-de-jianghu-e001 --character shen-guihe --image C:/media/shen-sheet.png --source C:/media/shen-source.json
```

`--file` 仍是替代 `--slug` 的 **video.json 專案來源**；`--image` 才是圖片，兩者不混用。`--workdir` 仍代表 VIDEO_WORKDIR 的根目錄，結果寫到 `<根目錄>/<slug>/characters/`，不能放在 Git 倉庫內。`--character` 必須是當集 `video.json.characters` 的基底角色 ID，不接受 `shot_looks` 的造型 ID。

| 呼叫 | 寫入／網路／結果 |
| --- | --- |
| `look import … --dry-run` | 驗來源及 PNG；不寫檔、不碰網路，即使同時指定 `--judge` |
| `look import …` | 離線保存原始 PNG、原始來源收據、候選 manifest；`judge:null`、無建議選項、待審；不生成、不上傳、不選圖、不核准 |
| `look import … --judge` | 明確要求正常媒體服務的 look judge；先查狀態、上傳同 SHA PNG，再使用 `Stage.judge`、既有 SHEET_RUBRIC 與 ledger/cap；不呼叫圖片生成 |
| `look --choose id=N` | 正常選圖；外部候選須已有真實 judge 結果且媒體／來源仍一致；未通過者不自動推薦，人工改選仍沿原有 owner 流程 |
| `review-push --gate look`／`review-pull` | 未判圖的外部候選不列為選項；沒有可審候選的角色阻擋整份提交。回讀只接受同 manifest SHA、實際存在且已判圖、媒體／來源一致的外部候選 |
| `approve --gate look` | 既有明確核准命令；外部 look 必須完整、當前並已判圖，所有選中圖和來源必須匹配。不由 import 代為呼叫 |

`--judge` 是付費操作，執行前依當前任務授權及正常成本關卡決定。本工程沒有呼叫真實 judge。估帳採既有程式常數，不另宣稱供應商今日費率。

同一匯入的 judge POST 只送一次（`attempts:1`）。送出前先保存 `judge_state:submitted`；若網路逾時、回應不明或程序中斷，原候選保留，後續重跑會停止要求核對；不能自動重付、捏造分數或直接把狀態改成 judged。已有判圖結果的重跑不再判圖，包括未通過的結果；要修圖後帶新 SHA 再匯入。

## 來源收據 v1

`--source` 是 UTF-8 JSON（上限 1 MiB）。必要欄位如下；尖括號文字需替換為實際值。

```json
{
  "schema_version": 1,
  "character_id": "shen-guihe",
  "look_hash": "<lookHash(currentVideoJson) 的 16 位值>",
  "image_sha256": "<原始 PNG 的 64 位 SHA-256>",
  "source_files": [
    {
      "path": "docs/videos/ou-de-jianghu-e001/video.json",
      "sha256": "<此檔目前的 64 位 SHA-256>"
    }
  ],
  "prompt_sha256": "<選填：生成提示內容的 64 位 SHA-256>",
  "reference_sha256": "<選填：生成參照圖的 64 位 SHA-256>"
}
```

- `look_hash` 由 `tools/video/core/drama.mjs` 的 `lookHash(doc)` 算出，涵蓋目前 resolved look 及角色基底 appearance／sheet_prompt。匯入會與當集重新計算值比較。
- `source_files` 至少一檔，應列出實際據以製圖的正典檔案；《偶的江湖》可直接帶本批已核對的 12 個來源檔。每個 path 必須是倉庫相對 POSIX 路徑、不重複；禁止絕對路徑、`..`、磁碟代號及指向倉庫外的 symlink。檔案存在與完整 SHA 都會現查。
- 整份收據原始 bytes 的 SHA 是 `source_sha256`；即使 PNG 相同，收據內容或排版變更仍算新來源版本。要去重請重用同一份收據原檔。
- `prompt_sha256`、`reference_sha256` 是可選的來源紀錄，檢查 hash 格式並保存；不因只有 hash 就宣稱驗證過原提示或參照原檔。額外欄位只隨原收據保存，不映射為 judge、owner approval 或已驗證的生成模型。

## PNG 檢查與原件保存

只接收實際 PNG bytes：8-bit、非交錯 RGB／RGBA，各邊 512–8192 px、像素總數不超過 16×1024×1024、壓縮檔不超過 32 MiB。逐 chunk 檢查 CRC、解壓 IDAT、核對 scanline 長度及 filter；截斷 PNG、假 IHDR、錯誤 CRC、APNG、超限與不支援格式會在寫入前拒絕。

這是工具接收範圍，**不替代畫像清單的 1024／1600／2048 尺寸目標及人工視覺驗收**。不裁切、不重編碼、不放大、不補造像素。PNG 及原收據用完整 hash 派生的 immutable 檔名保存；同路徑若已存在而 bytes 不同，拒絕覆寫。

候選至少記錄 `file`、`sha256`、`key`、`n`、`judge`，及 `external_import` 的來源收據路徑／SHA、source_files、角色 sheetKey、實際尺寸、原檔名、匯入時間和可選提示／參照 SHA。只保存原始檔名，不把外部電腦絕對路徑塞進 manifest。

## 去重、失效與跨集共用

匯入 key 是版本字串、角色 `sheetKey`、PNG SHA、來源收據 SHA 的 SHA-256。完全相同的重跑沿用候選編號、judge、時間及 manifest bytes，因此不使既有核准僅因時間戳重寫而過期。

換圖、換來源收據、換基底 appearance／sheet_prompt／look 會新建候選／當前 manifest；舊 PNG 和來源不刪除。清除受影響角色的舊 choice，讓新候選等待審閱；look manifest 改變會使舊 look 核准 SHA 過期。已存在的 keyframes／clips manifest 先按 SHA 保存到 `characters/history/`，再標 `look_hash:null` 和 `external_look_invalidated_by`；舊鏡頭、付費素材保留，下游須重新建立，舊 storyboard 核准不再匹配。既有成片及 audio/final 的人工核准紀錄不刪改；它們不能當作這個新 look 的完成證據。

正常 `look` 若打算生成的角色已有外部候選，會要求繼續 `look import`／判圖／選圖，不默默重畫。明確只生成其他角色時保留匯入候選。

若來源檔內容變更但基底 look_hash 未變，新匯入會把來源已過期的舊候選標 `superseded_by`，保留原件及原判圖證據，但不再建議、列入審閱選項或允許選用；更新來源收據的新候選可正常繼續審核。

正常 owner review 回讀後仍由原有 `keepSheets` 放進 `_series/<series>/characters/`。外部候選存入及 reuse 都核對實際 PNG SHA；外部來源收據會一併保存及複製。未判圖外部候選不能存成已核准共用圖，也沒有合成「10分通過」的外部 fallback。跨集 reuse 須有 sourceRoot，來源檔仍是原 SHA、角色 sheetKey 未改、PNG／來源收據完整；否則視為 missing。外部圖片不偽裝成當前 Gemini/MiniMax 圖片模型的產物；已核准且來源一致的外部基底可作為不同後續生成模型的參照。

既有生成圖的 image provider/model 選擇與 legacy reuse 邏輯保留。正常跨集全數共用時沿用原有「先前已核准」行為；這不是本命令建立新的 owner approval。

`shot_looks` 仍是每鏡文字外觀覆寫，沒有每個命名造型的獨立圖像引用。每角色仍由正常 `chosenSheets` 選一張基底圖，keyframe 請求帶該圖實際 SHA；多視圖、表情、道具、場景包不會因存進磁碟就自動成為模型參照。

## 離線驗證

```powershell
node --test tools/video/media/look-keyframes.test.mjs tools/video/media/series-store.test.mjs tools/video/review/sync.test.mjs
npm run test:tools
npm run check:tasks
```

新增測試涵蓋：合法完整 PNG、非法角色／壞檔／尺寸／來源逃逸／hash不符；離線 dry-run、無網路匯入、STOP、immutable原件；精確重跑不重寫、不重付；真實 schema 的 mock judge 成功／失敗／不明回應；正常選圖／核准及 keyframe request 的匯入圖 SHA；換圖／來源／appearance／style 使 look與storyboard核准及下游失效；series-store來源保存、跨集reuse、來源或媒體被修改的拒絕；review提交不含未判圖選項，回讀拒絕偽造或過時的外部證據。

## 首集 9 張原圖：隔離 staging 實證

2026-10-08，主控指定以 `portraits/20261008/<id>-full-body-v1.png` 九張既有原件驗證來源管線。`selection_for_offline_candidate_validation_only=true`；這不是選用或站主採用，也沒有以新動畫多角度包替代基底。

- 工作專案是凍結的 v3 working video，SHA `7f7676d1ce39a6f9dbbdc4cacc5bc8cb39b9979e66e4a906213d2ea4235014df`；原圖、參照圖與 12 個正典來源檔均現查 SHA，與製圖收據一致。
- 九份 source sidecar、原始命令輸出及完整結果在 `<VIDEO_WORKDIR>/ou-de-jianghu-e001/external-look-staging/20261008/`。隔離 workbase 是其 `workspaces/`，沒有寫入正常 `<VIDEO_WORKDIR>/ou-de-jianghu-e001/characters/`。
- 每張各做 dry-run、import、相同參數重跑。首輪 27 個 CLI 呼叫全 exit 0；驗證器最後誤把自身執行中的 `LEASE` 當成其他媒體而 exit 1，該 lease 隨程序退出自動释放。修正驗證器後明確續接這個自有 staging，再跑 27 次，全 exit 0。**54 個 CLI 呼叫全 0，最終驗證器 exit 0**；沒有刪 lock 或重建原图。
- 九個角色均只有候選 1，`judge:null`、`suggested:null`、`needs_review:true`；原 PNG／收據 bytes 與 SHA 一致。manifest SHA `fd02c531d0b6a42eb306b313fe933fb7ba566dec3a72d37a3b14e5e6bb8d6521`，相同來源重跑保持 bytes。程序退出後 workdir 只剩 `characters/`，没有 choice、approvals、ledger 或下游媒體。
- 執行器把 fetch 替換為會立即拒絕的本地函式，最後記錄 **0 次 fetch 嘗試**；參數中沒有 `--judge`／`--choose`／approve／review。付費 judge、真實生成、owner approval 都沒有執行。
- 九圖原生皆 **1024×1536、2:3**，沒有改圖或放大。通過的是 PNG 匯入最低技術規格；全身圖長邊 2048 的美術目標仍未達，不能因此把圖像完成度改成已核准。

可攜收據：[pending-staging-receipt.json](pending-staging-receipt.json)，只含公共 `VIDEO_WORKDIR` 相對路徑。正常 runtime 的 judge／選用／owner approval 仍須依前述流程取得真實證據。

實際測試結果及 runtime 見本票 Notes。測試中的 owner decision、模型回應與 PNG 都在隔離 fixture；沒有寫首集 owner approval，也沒有付费、部署或發布。
