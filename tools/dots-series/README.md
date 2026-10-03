# dots 課程編譯與驗收工具

這裡只產出候選檔案、合成練習下載包及驗收報告，沒有資料庫匯入、付費生成、部署或 YouTube 上傳操作。編譯使用既有 `ArticlePack`、`Catalogue`、`lint_document` 及 `check_svg`；SVG 無障礙與安全檢查在寫入前執行，不新增文章格式或公開 API。

## 製作順序

從 repository 根目錄執行；Windows Python 使用 `apps/api/.venv/Scripts/python.exe`，Linux 使用 `apps/api/.venv/bin/python`。

```powershell
$dotsWorkspace = Join-Path ([Environment]::GetFolderPath('UserProfile')) 'mokaair-work/dots-series'
# 先編譯兩課樣本。其他稿件缺少不影響樣本；樣本不能通過全套發布門檻。
apps/api/.venv/Scripts/python.exe tools/dots-series/build.py --workspace $dotsWorkspace --selected 02,03
# 六個應用寫完後，先打包合成輸入與稿件交接目錄。
apps/api/.venv/Scripts/python.exe tools/dots-series/package.py --workspace $dotsWorkspace
# 作者定稿並交叉查核後，以既有 youtube-video helper 建立16份文字製作包。
apps/api/.venv/Scripts/python.exe tools/dots-series/authoring_kit.py --workspace $dotsWorkspace --install
# 完整編譯17篇；先驗證全部輸入，再建立候選包。
apps/api/.venv/Scripts/python.exe tools/dots-series/build.py --workspace $dotsWorkspace
# 明確安裝已通過schema及lint的草稿和顯示素材；不匯入、不發布。
apps/api/.venv/Scripts/python.exe tools/dots-series/build.py --workspace $dotsWorkspace --install
# 真實操作與媒體全部覆核後，只產出驗收報告。
apps/api/.venv/Scripts/python.exe tools/dots-series/readiness.py --workspace $dotsWorkspace
```

`package.py --install-downloads` 只安裝六個 `/dots-course/downloads/lesson-11.zip`–`lesson-16.zip`；正常的完整 `build.py --install` 也會安裝文章引用的這六個下載包。

候選文章在外部工作區 `build/content/`，顯示素材在 `build/web-public/`，稿件交接在 `build-authoring/{lessons,videos,examples}`。將原稿交接至 `docs/dots-series/` 由協調者執行；工具不替原稿標記實測或發布。影片旁白原稿是 `videos/01.md`–`16.md`，不是音訊或成片。影音原檔始終留在外部工作區。

`authoring_kit.py` 預設只在外部 `build-authoring/docs/` 建立17篇文章原稿、六組合成練習來源及16個 `videos/dots-lesson-NN/` 文字製作包。`--install` 明確複製到repo的 `docs/dots-series/{lessons,examples}`、`docs/videos/dots-lesson-NN/` 和 `docs/dots-series/production-manifest.json`。工具呼叫既有 `video_kit.py` 的check、teleprompter、shots、metadata；任一稿FAIL便不安裝。`recorded_on:null` 在製作包腳本轉為留白，原始和轉換後稿件各有雜湊。`upload-draft.md`、分鏡時間與口播秒數均明確標為估計；不產生SRT、實際章節、音訊、影片或影片網址。文章及下載連結均標為預定尚未公開。

所有產生的文字檔及安裝用文字副本均明確使用 UTF-8／LF，與 `.gitattributes` 的 Git 儲存格式一致；空白錄製日期為 `recorded_on:`，行尾沒有空格。外部凍結原稿的 bytes 完全保留：`sources[].sha256`、`source_article_sha256`、`source_script_sha256` 綁定原始 bytes；`files[].sha256`、`output_sha256`、`article_output_sha256` 與 `normalized_script_sha256` 綁定實際 LF 輸出副本。合成 ZIP 仍封裝原始練習檔 bytes；LF 換行只套用於文字交接及 repo 安裝副本，不改 ZIP 內資料或外部來源。測試以明確 CRLF 原稿核對來源未變、輸出 LF、manifest 雜湊，並在隔離 Git index 比對實際 staged bytes。

所有工具先以最高工作區／repo 邊界驗證來源與輸出，再限制相應子目錄。來源樹會在進入子目錄之前檢查 junction／symlink；六 ZIP、交接、build／build-pilot及全部安裝目的檔在任何打包或安裝寫入前完成路徑檢查。最後一課的越界目的檔也會阻擋前面所有寫入。此檢查處理檔案系統的靜態路徑別名，不能取代作業系統存取控制或防止另一個程序在檢查之後改換連結。

## 作者輸入

- `lessons/01.md`–`16.md` 必須存在，含一個 H1 標題、正文、H2/H3、清單、表格、提示框、可複製提示詞及最末的 `## 官方來源`。`00.md` 可指定原創總目錄；沒有時建立標有驗證範圍的系列索引。
- 程式碼圍欄須帶語言和輸入位置，例如 `` ```text 在 dots 對話輸入 ``。提示詞保留換行。支援現有 Markdown 連結與行內 code；站內生活文章連結轉為出版狀態可檢查的 `article` inline。既有表格欄位只有純文字，表格中的連結顯示標題；可點擊的課程入口由系列目錄與正文 `article` inline 提供。
- 摘要由作者明確寫 `:::summary`、2–5個 `- 句子`、結尾 `:::`，放在第一個H2之前；轉成現有 `SummaryBlock`，不自動重寫導言。
- 官方來源用 `[標題](https://...)`，同一行寫日期，或來源節只有一個共同 `YYYY-MM-DD` 查核日期。缺少、衝突或重複來源會失敗。來源是文章 `sources`，不混進操作正文。
- 封面在外部 `assets/guides/<slug>/hero.png|jpg|webp`，也可使用 checkout 已有的同路徑素材。圖說、寬高及其他圖以外部 `assets.json` 的 `slug -> ImageBlock metadata[]` 提供；子文章未提供時使用已存在的原創 `diagram-1.svg`。總目錄保留封面，只有作者明確指定才加入正文圖片。工具不生成或偽造 UI 截圖。
- 六個應用初始輸入、變更輸入與作者基準在 `examples/11`–`16`。下載 ZIP 可重現、標記合成練習輸入，不是 dots 的實際輸出。

## 真實驗收紀錄

在外部工作區建立 `evidence/acceptance.json`。格式為 `version: 1`、`lessons`（16筆）、`applications`（第11–16課各一筆）、`scheduling`。初始模板故意沒有可通過的證據。

```json
{"version":1,"lessons":[],"applications":[],"scheduling":{}}
```

每個檔案參照都包含工作區相對 `path` 和實檔 `sha256`。路徑不能逸出工作區；空檔、變更過的雜湊、標為 fixture/mock/illustration 的檔案不是實測證據。API虛擬環境的Pillow實際解碼PNG、JPEG及WebP截圖；沒有Pillow的純合約測試只支援PNG回退檢查。來源記錄與視覺遮罩仍需指定覆核人驗證，檔案存在不等於來源真實。

每課 `lessons` 紀錄：

| 欄位 | 內容 |
| --- | --- |
| `number` | 1–16，不重複 |
| `article_sha256` | `build/content/dots-lesson-NN.json` 的當前雜湊 |
| `capture` | 檔案參照，加 `origin: real-dots`、`authenticated: true`、帶時區的 `captured_at` |
| `screenshots` | 實際截圖參照陣列；每筆加 `origin: real-dots`、`redacted: true`、帶時區的 `captured_at` |
| `review` | `reviewer`、帶時區的 `checked_at`、`files` 映射（capture與screenshots的path -> sha256，另加 `article -> article_sha256`）；`steps_reproduced`、`result_checked`、`redaction` 都為true |
| `video` | 成片參照、正文起迄 `body_start_seconds`／`body_end_seconds`、`cc`／`chapters`／`thumbnail`／`description`四個檔案參照及 `review` |

影片 `review.files` 必須完整且精確綁定成片及四個上架素材；含 reviewer、checked_at，且 `screen_readable`、`audio`、`cc_sync`、`chapters`、`redaction` 全為true。工具自行用 `ffprobe` 讀實際音軌、影像軌及時長，不接受JSON自報時長。正文至少480秒，整片不超過900秒。SRT逐段核對索引、格式、文字與時間，不得逆序或超過影片結尾；章節檔有至少兩個由00:00開始的順序時間點，均在影片內；縮圖須可實際解碼。這些檢查不取代真人觀看與聆聽。

每個應用紀錄包含 `number: 11..16`、`origin: real-dots`、`updated_in_same_task: true`、`before`／`after`／`verification`檔案參照。前後結果的雜湊必須不同。`review`綁定這三檔，`result_checked: true`；第13課還須 `independent_calculation: true`。合成輸入和作者基準不能填進 before/after 當作實際結果。

`scheduling` 分別提供 `execution`、`main_stopped`、`delegated_stopped`、`schedule_cancelled`檔案參照；`review`綁定四檔，`execution_observed`及`stop_scopes_checked`都為true。必須使用專用測試工作，不能停止站主原有工作來補證據。

日期使用例如 `2026-10-03T23:00:00+08:00`。沒有額外的owner approval欄位；既有影片審核規則和Studio權限仍適用。

`readiness.py`成功為exit0，缺證、失敗或變更為exit2。`--write-manifest <工作區內路徑>`僅在全綠後寫出檔案雜湊、精確17篇whitelist及「16課先、總目錄最後」順序，狀態是 `ready-for-owner-release`，`published`仍為false。工具不解除 `publish_holds.json`，不把準備完成當作公開完成。

## 測試

```powershell
node --test tools/dots-series.test.mjs
apps/api/.venv/Scripts/python.exe -m unittest discover -s tools/dots-series -p test_pipeline.py -v
npm run build:web
npx playwright test --config tools/dots-series/playwright.config.mjs
```

Node測試執行無第三方依賴的作者格式、門檻及路徑合約案例。偵測到API虛擬環境（或明確設定 `DOTS_API_TEST_PYTHON`）時，也執行真正呼叫 `ArticlePack`、`lint_document`與系列出版過濾邏輯的 `test_pipeline.py`；只有工具環境尚未建置API時明確skip。CI的api-checks在 `uv sync --frozen` 後固定執行這份API測試，包含撤回總目錄、撤回子文章及缺少其他語系。Directory symlink無權限時，Windows測試會嘗試建立真正junction；仍無權限才明確skip，Linux直接測symlink。UI測試只使用localhost API fixture和已安裝候選包，驗證桌面／手機目錄、複製、下載內容雜湊、撤回與語系隱藏，封鎖外部請求。所有測試fixture都只證明程式行為，不能作為真實dots操作、畫面或媒體驗收。
