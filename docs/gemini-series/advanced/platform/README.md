# 深入篇內容建置與發布清單

本工具支援課綱 51–86 的六個批次：`work`、`research`、`creative`、`md`、`automation`、`api`。目前網站正式清單仍是原本 50 篇；草稿建置不會改動它，也不會連線匯入資料庫。

共用頁面的深入篩選、伺服器端公開開關、文章導覽仍由 [platform 待辦](../../../../tasks/open/2026-09-14-gemini-advanced-platform.md) 負責。本工具完成不代表 36 篇已完成或可以公開。

## 作者檔案

以第 69 篇為例，在 `docs/gemini-series/advanced/content/md/` 放置：

```text
md/
  69/
    lesson.md
    meta.json
    hero.svg
    diagram-1.svg
    hero.jpg          # 不使用 --render 時才需要
  examples/
    rules.toml
    exercise.zip
  verification/      # 工具產出與實際測試紀錄
```

`lesson.md` 第一段須為純文字摘要。正文需有至少三個二級標題、程式區塊、文字連結、表格、提醒區塊，以及「常見問題」二級標題下至少三個三級問題。正文長度 1,800–3,000 字；程式碼、圖說與標題不計入，禁止用重複填充文字湊字數。一般 Markdown 連結不在此編譯器的語法範圍，跨篇連結使用以下格式：

````markdown
## 開始前準備

先完成 [[36|GEMINI.md 入門]]，再讀 [[37#section-3|記憶載入檢查]]。

!include-code examples/rules.toml

```powershell 終端機命令
gemini --version
```

| 觀察 | 成功條件 |
| --- | --- |
| 載入內容 | 包含預期標記 |

> 這裡寫本篇的具體操作提醒與驗證限制。
````

`#section-N` 依目的文章的二級標題順序定位；改標題順序後需重新檢查。引用程式碼只能位於同一批次 `examples/` 之內，原文呈現、不執行。表格儲存格不支援未跳脫的直線字元或跨篇標記；需要連結時改放相鄰段落。

`meta.json` 範例（用途是格式說明，不是完成的文章）：

```json
{
  "hero_alt": "記憶載入實驗封面",
  "diagram_alt": "全域、專案與子目錄載入流程",
  "diagram_caption": "依實際驗證結果說明載入時機。",
  "sources": [{
    "title": "Gemini CLI contextual memory",
    "url": "https://geminicli.com/docs/cli/gemini-md/",
    "checked_on": "2026-09-14"
  }],
  "downloads": [{
    "source": "examples/exercise.zip",
    "filename": "practice.zip",
    "text": "下載本篇練習包"
  }]
}
```

日期應填實際重查日。封面與圖解皆為原創 1600×900 SVG，含 `title`、`desc`；禁止脚本、事件處理器與外部參照。下載來源也限同批 `examples/`，輸出名稱需唯一且為普通檔名，允許 ZIP、CSV、JSON、MD、TXT。下載包需另驗證能解壓、內容完整且不含帳密。

## 建置、圖解與連結檢查

從 repository 根目錄執行（其他平台改用對應虛擬環境 Python）：

```powershell
& apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/build.py 69 --track md --render
node docs/gemini-series/render-art.mjs --track md --numbers 69
```

Python 的既有 SVG 渲染器透過 `CHROMIUM_BIN` 選擇瀏覽器。Windows 可設為已安裝 Playwright 的 **chrome-headless-shell.exe** 絕對路徑；先核對實際版本目錄，不能照抄別台機器的版本號。Node 渲染器直接使用 `apps/web` 安裝的 Playwright。缺 Chromium 時先修正依賴，不能以假 JPEG 代替配圖。

省略篇號建置整個批次；建議先用 `--output-root <隔離輸出目錄>` 檢查，再輸出正式檔案。工具會先驗證並在暫存區渲染整批，所有篇章成功後才複製至輸出。檔案系統複製本身不是交易，磁碟錯誤仍須核對部分輸出。每批報告存於輸出目錄 `docs/gemini-series/advanced/content/<track>/verification/`。

```powershell
& apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/build.py --track md --render
node docs/gemini-series/render-art.mjs --track md
node tools/gemini-series.mjs check --draft --track md
```

隔離輸出時，兩個 Node 指令分別加 `--output-root` 與 `--workspace`。整批檢查會核對先修、延伸閱讀、正文連結及章節定位；被引用的深入文章尚未建置時會失敗，須等對應批次完成，不能建空白文章通過。未改動的第一階段參考文章可從 repository 讀取。

編譯報告的 `built-unpublished` 只表示本地內容包建置成功。渲染報告的 `rendered-awaiting-human-review` 只代表產出 PNG、JPEG 與 360px 預覽，且文字沒有越出画布；逐張檢查可讀性、重疊與圖意後才另外記錄視覺驗收。`visual-review/synthetic-*` 是工具測試圖，不能用作正式文章配圖。

## 完整發布清單

`catalogue-contract.json` 固定保留 86 個篇號／slug、八個分類及十一條路線。`draftCatalogue()` 只在作者工具內組合原清單與課綱。正式整合仍需在 platform 任務完成伺服器公開開關後，將正確資料寫入原系列清單。

全套 87 頁完成、例子實測與配圖審閱通過後才執行：

```powershell
node tools/gemini-series.mjs check --phase advanced
node tools/gemini-series.mjs freeze --phase advanced --manifest docs/gemini-series/advanced/release/reviewed-release.json
node tools/gemini-series.mjs dry-run --phase advanced --manifest docs/gemini-series/advanced/release/reviewed-release.json
```

先建立 manifest 所在資料夾；檔案必須不存在，工具不覆蓋舊收據。若本次同時更新既定方案篇 02 或計費篇 49，freeze 另加 `--updates`，值為兩篇允許 slug 的逗號清單。其他既有文章不能夾帶進深入批次。

凍結清單包含 catalogue 雜湊、全部內容包與該篇資產目錄內的檔案雜湊（含下載包），以及本次寫入名單。文字統一換行後雜湊，二進位逐位元組雜湊；不支援連結至工作目錄外的檔案。它是可比對收據，不是簽章、人工核准或內容正確性的證明。任何檔案變動都需要重新審閱與另建收據。

在既定部署環境才執行以下發布命令；替換三個實際值：

```powershell
node tools/gemini-series.mjs publish --phase advanced --manifest docs/gemini-series/advanced/release/reviewed-release.json --actor-email ADMIN_EMAIL --api-origin https://mokaair.com --journal RELEASE_JOURNAL.jsonl
```

發布會先 dry-run 限定名單，逐篇寫入 36 篇與明列更新篇，核對公開 API；再重新核對全部 86 篇，最後更新目錄。每次寫入前重查凍結檔案，記錄 starting／verified。任何失敗立即停止；匯入逐篇提交，沒有整批回滾或自動續跑，重跑前須依 journal 核對已完成部分。同一 journal 不得混用其他 releaseId。

工具不切換網站公開開關、不部署、不取代瀏覽器或 sitemap 驗收。第二階段的入口必須保持關閉，直到所有子文章確定可讀並完成既定 release 任務。第一階段 `check` 與既有發布語法持續可用；`--draft`、`--track`、`--workspace` 僅可用於檢查，不能用來繞過整套發布。

## 工具驗證

```powershell
node --test tools/gemini-series.test.mjs
& apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/platform/test_build.py
node tools/gemini-series.mjs check
npm run test:tools
npm run check:tasks
```

測試以合成資料驗證真實編譯器、型別驗證、邊界與順序，不呼叫雲端模型、不匯入資料庫。第 36 篇的隔離重建另外與已審閱內容包逐欄比較，避免修改編譯器後破壞舊文章。
