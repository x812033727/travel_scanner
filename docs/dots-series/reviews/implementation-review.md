# dots 實作獨立 code review

審查者：dots_lessons_foundation。日期：2026-10-04（Asia/Taipei）。範圍：`tools/dots-series/{build,authoring_kit,readiness,files,package}.py`、Markdown adapter、相關單元測試、`tools/dots-series.test.mjs`、API 系列 registry／public series／publish holds、dots Playwright e2e。repo 僅讀，沒有修改程式，沒有重跑 full CI。

**最新結果：原一項 P2 已修正，2026-10-04 的獨立 Windows junction 重測七案全通過；目前沒有未結 P1／P2。** 未發現新增系列自動公開或現有預設證據通過驗收的 P1。下方保留修正前 finding 與重現紀錄，修正後收據見末節。

## 已修正 P2：在檔案邊界驗證前，junction 可讓打包讀寫逸出工作區

位置：`tools/dots-series/package.py:23–45`、`:50–58`；同一輸出邊界缺口亦在 `build.py:172–197`、`authoring_kit.py:130–182`。

`package` 初次驗證使用 `contained(path, directory)`。如果 `workspace/examples/11` 本身是指向外部目錄的 junction，`directory.resolve()` 也變成外部目錄，所以外部檔案通過第一次驗證。接著 ZIP 路徑直接組為 `workspace/assets/...`，沒有以最上層 workspace 做解析後的邊界檢查；`assets` 是 junction 時，ZIP 寫到外部。稍後原稿交接的 `contained(source, workspace/examples)` 才拒絕，但六包 ZIP 已經產生；若開 `--install-downloads`，公開下載目錄的複製也發生在這個晚到的驗證之前。

外部測試重現使用自建、無機密的文字檔，未寫 repo。將 `examples/11` 及 `assets` 分別 junction 到測試工作區外的兄弟目錄，`package()` 最終丟出邊界錯誤，但外部 `lesson-11.zip` 已存在，且含外部來源檔案的精確位元組。記錄：`reviews/implementation-path-probe.json`；重現 helper：`_tools/implementation_path_probe.py`。這不是任意猜測的惡意路徑，實際 Windows junction 已重現「先讀寫、後拒絕」。

具體修法：

1. 在建立任何 ZIP、交接或安裝檔前，以 `contained(..., workspace)` 驗證六個來源目錄與每個來源檔；保留每課目錄的內部檢查，但不能把它當作最上層 workspace 邊界。
2. 先以 workspace 驗證完整輸出根 `assets/dots-course/downloads`、`build`／`build-pilot`、`build-authoring`，再驗證每個輸出目的檔。不能只以可能已是 junction 的子目錄當 root。repo 安裝目的檔也應以 repo 最上層做邊界檢查，再限制允許的 content／public／docs 子樹。
3. 在所有驗證成功前不複製到 repo；加入來源目錄 junction、輸出目錄 junction 的回歸案例，確認拒絕時沒有任何外部 ZIP 或 repo 檔案產生。`files.contained()` 本身已正確解析路徑，需修的是呼叫的根與寫入順序。

## 其餘重點核對

- **預設不會假 ready：** readiness 要求 17 個指定 draft pack、16 個具名課次、真實來源標記及截圖、六個初版／新版案例、一次排程執行及三種停止紀錄。缺欄位會累積錯誤，沒有 acceptance manifest 直接拒絕。ffprobe 在 CLI 路線讀實際影音，確認音訊與影片流、正文至少 480 秒及整片不超過 900 秒；不是以腳本估時通過。
- **雜湊與媒體：** 作者輸入、編譯檔、來源 assets、各課文章、操作截圖、影音、字幕、章節、縮圖及說明以當前 SHA 檢查，審查的 files 映射須相同。截圖用 Pillow 解碼；字幕拒絕壞時間與超出片長，章節從零開始且遞增。具名審查與 origin 是人工證據聲明，不是工具能獨立證明的登入或遮罩；README 有明確交代，未把這些聲明等同自動視覺驗收。
- **作者包不冒充影片：** authoring_kit 呼叫既有 helper 產出文字包，`media_generated:false`、影片網址與實測時長留空，章節／上架稿標為估計；check 失敗不安裝。沒有付費、資料庫、部署、上傳或發佈動作。
- **來源主張保留：** adapter 保留提示詞與換行、來源 URL／checked_on，無法辨識的正文格式會報錯。來源節尾部的製作備註不會變成正文；本批 pending 狀態也已在導言／總目錄說明，沒有只靠被移除的尾註承載限制。表格連結目前轉成純文字是既有 schema 的明示限制，可點入口仍由系列目錄及 rich article link 提供。
- **文章與 hub：** compiler 使用既有 ArticlePack 和 lint，子文章回連 hub，六案下载鏈結需存在。API `public_series` 只加入各語系已發布 revision；hub 未發布則不回傳系列，下架課與其他語系不會因 registry 新增而取得本文。
- **公開保留條件：** 17 個 dots slug 都在 `publish_holds.json`。一般批次 publish plan 會留下 held drafts，指定 held slug 的 CLI publish 會明確拒絕。這個 hold 的既有用途是 CLI 匯入保護，並非 admin API 的全面存取控制；`publish_locale` 仍可由有權管理員明確操作。這不是本次新增的自動公開入口，不能把持有檔案或 registry 新增當作公開。
- **e2e 的範圍誠實：** 該 suite 明寫 mock publication fixture 不是 dots 操作證據；桌面與手機驗版面、搜尋／篩選、複製按鈕、實際本機 ZIP 下載 SHA、撤下子文、未發布語系及撤下 hub。它驗的是本站閱讀流程，不宣稱實際 ChatGPT／Slack 操作或正式站已驗。

## 測試連接的一項補強建議

`tools/dots-series.test.mjs:30–33` 只啟動 `test_authoring`、`test_readiness`、`test_authoring_kit`；API 相依的 `test_pipeline.py`（compiler、ZIP、既有 API publication join 的回歸案例）目前由 README 列為另跑，沒有接進標準 `npm run test:tools` 或 CI workflow。這一輪可沿用已執行的本機結果；建議在有 API dependencies 的 CI job 加入這份測試，避免後續編譯器／公開 join 變更只有文字工具測試覆蓋。

本報告沒有宣稱 CI、部署、實際 dots 案例、影音或公開已完成。

## 2026-10-04 修正後獨立覆核收據

審查者：`/root/dots_lessons_foundation`；實際重測時間以 `reviews/implementation-path-recheck.json` 的 UTC checked_at 為準。repo 仍只讀，所有 fixture、junction 與收據均在外部 `_tools`／`reviews` 下；修正前的 `implementation-path-probe.json` 保留不覆寫。

已讀目前的 `files.py:27`／`:40`、`package.py:20–36`、`build.py:183–208`、`authoring_kit.py:127–149`。`scoped` 先以最上層 workspace／repo 查 subtree，再查目標；`tree_files` 在遍歷與讀取前查目錄及逐檔邊界。package 在 ZIP／複製前完成來源、staging 與 repo 目的檔預檢；build 與 authoring_kit 的最上層輸出與安裝檔也在第一個輸出寫入前預檢。`MissingAsset` 與邊界錯誤已分開，hero／diagram 的缺素材 fallback 不會吞掉逸出錯誤。

獨立重測執行真實 `package(..., install_downloads=True)`，repo 參數為測試用空目錄，未對真實 repo 安裝。用原合併案例加六個隔離案例，全部實際建立 Windows junction：來源與 assets 同時逸出、單一來源逸出、assets 輸出根、downloads 子目錄、build-authoring 交接根、repo public 根、repo downloads 子目錄。執行期間監看 `builtins.open`／`io.open`，並在拒絕後盤點外部、工作區 ZIP 與 fake-repo 檔案。

七案全部在任何外部來源內容讀取、ZIP／交接寫入或 repo 安裝前丟出邊界錯誤：外部來源 read-open **0**、外部 output write-open **0**、repo install write-open **0**，外部輸出、repo 安裝檔及工作區 ZIP 亦皆空。完整每案結果、fixture 路徑與四支目前程式 SHA 在 `reviews/implementation-path-recheck.json`；重測 helper 是 `_tools/implementation_path_recheck.py`。因此此 P2 已關閉。

這份獨立執行直接涵蓋 package；build／authoring_kit 的順序則由目前原始碼覆核，沒有在此收據中冒稱重跑它們的 full pipeline 或 full CI。未測並行程序在預檢後更換 junction 的競態；原 finding 的既存 junction 提前拒絕條件已確認。

## 2026-10-04 更新：test_pipeline 的標準檢查連接已完成

審查者：`/root/dots_lessons_foundation`。已只讀確認目前 `tools/dots-series.test.mjs:37–46` 在 API Python 環境可用時執行 `test_pipeline`，工具專用環境未提供 API dependencies 時明確標示 skip；`.github/workflows/ci.yml:45` 則在 API job 的既有 `uv sync --frozen` 後，用 `uv run python -m unittest discover -s ../../tools/dots-series -p test_pipeline.py -v` 執行該測試。上方「測試連接的一項補強建議」保留為初次審查的歷史紀錄，該建議現在已解決。這次核對的是 Node wrapper 與 API CI 步驟的連接，沒有據此宣稱 CI 已執行或整體全綠。

## 2026-10-04 最終 LF 輸出與路徑重測

審查者：`/root/dots_lessons_foundation`。Windows 文字輸出改為明確 UTF-8／LF 後，已重新執行七案真實 junction 測試；外部來源讀取、外部輸出寫入及 repo 安裝寫入仍全部為零，各案在預檢階段拒絕。最上層 `scoped`／`tree_files` 與 package、build、authoring_kit 的預檢順序未被 LF 寫入或複製 helper 移到寫入之後。這次紀錄是 `reviews/implementation-path-recheck-lf.json`，綁定新版本五支工具的 SHA。先前 `implementation-path-probe.json` 和 `implementation-path-recheck.json` 保留為歷史快照；其舊 SHA 僅表示各次檢查當時的版本，不冒稱為這次最終程式位元組。

獨立逐檔核對：外部 **33 份凍結原稿 SHA 全部不變**；production manifest 的 **142 個輸出**及 build manifest 的 **56 個內容／資產**，staging、repo 安裝檔與 manifest SHA 全相符。16 份影片稿只有明示的 LF 與空白 `recorded_on:` 正規化，所有該欄位恰為 `recorded_on:`，正文仍與各自凍結原稿一致。文章／練習輸出是明示 LF 複本，來源與輸出 SHA 分別保存，沒有以正規化後位元組代替原作者稿雜湊。

對 **204 個輸出／manifest／目前工具檔**，用只讀 `git hash-object --stdin-paths` 分別啟用及停用 filters；每個 Git blob hash 相同，證明清理 filters 不會再次更動這些位元組，因此目前 SHA-256 也適用 Git 儲存的內容。沒有執行 git add、commit 或寫入 Git object。完整逐檔 SHA、原稿／輸出分別綁定、五支最終工具 SHA 及兩個 manifest SHA 在 `reviews/implementation-final-lf-audit.json`。

最終獨立結果：這個窄範圍輸出／路徑核對全部通過，未發現新增 P1／P2；不代表 full CI、實際帳號全課、旁白、字幕、成片、部署或公開完成。工具與教材凍結後不再修改，由主代理接續 commit／rebase。
