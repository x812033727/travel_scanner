# Mokaair 本機圖片載入實驗

這是可重現的測量套件，尚不是已發布文章。實驗由 Codex 操作真實 Microsoft Edge headless 瀏覽器；沒有真人受試者，也沒有測正式網站。

## 重現

需要 Node.js、Microsoft Edge 與 Playwright。原執行環境是 Node v24.13.0、Playwright 1.64.1、Edge 157.0.4341.42；完整環境與平台在每個 run 的 environment.json。此套件使用機器已有的套件，沒有安裝或購買任何服務。

PowerShell：

```powershell
# 在已安裝 Playwright 的專案根目錄執行，或設定 MOKAAIR_PLAYWRIGHT_ROOT。
node './docs/news-reader-enhancements/lazy-loading-lab/experiment/lab.cjs' run
```

公開衍生 runner 優先使用 `MOKAAIR_PLAYWRIGHT_ROOT`，未設定時由套件目錄與目前工作目錄解析已安裝的 `playwright/package.json`；沒有個人本機 fallback。需要相同版本才能接近原環境，不保證別台機器得出完全相同的預載數量。此公開調整沒有執行新一輪瀏覽器測試。

`run` 會先用程式重新產生固定的 20 張 SVG 與 eager／lazy HTML，再啟動 127.0.0.1 HTTP、依預先規格跑 18 個情境，建立全新時間戳 runs 目錄，結束後關閉伺服器與瀏覽器。成功才回 exit 0；失敗原紀錄保留。

手動操作頁面：

```powershell
node './docs/news-reader-enhancements/lazy-loading-lab/experiment/lab.cjs' serve
```

終端會顯示只在本機可用的兩個網址；在 Edge 開啟，按 F12 進 Network，開 Disable cache、重新整理，依序觀察未捲動／End／回頂逐段捲動的圖片請求。手動觀察與自動結果分開記錄，不能倒填為本輪已做的人工測試。結束在終端 Ctrl+C；沒有背景常駐排程。

## 證據結構

- `experiment-plan.md`：第一次實驗前固定的情境、時間與判定；run 內保留其副本與 SHA。
- `lab.cjs`：fixture generator、本機 HTTP 與完整 runner；公開 run 的 `runner.cjs` 是相同的可攜衍生副本，並非冒稱原執行檔位元組。原／新 hash 見 `PUBLICATION-REBIND.md`。
- `fixtures/`、`fixture-manifest.json`：自有合成素材、兩份頁面、逐檔 hash／bytes。
- 外部官方 HTML 與抽出正文只保留於私有查核目錄，沒有在公開套件重製；來源 URL、取得狀態與原 hash 見套件根目錄 `sources.json`。
- `runs/<timestamp>/environment.json`：版本、OS、viewport 政策、cache 與來源檔 hash。
- `results.json`：18 個情境，每次初始／End 後／完整遍歷後的請求數、loaded、幾何、檢查結果。
- `server-requests.json`、`browser-requests.json`：所有本機頁面請求及階段，彼此可對帳。server 的 bodyBytes 是回應本文 bytes，不含 HTTP headers、TCP／TLS overhead，也不等於遠端網站實際節省流量。
- `blocked-external-requests.json`、`page-errors.json`：非本機頁面請求與瀏覽器錯誤。
- `screenshots/`：每種情境第一次的三個 viewport 截圖，共 18 張。初始截圖不用 fullPage，避免為拍圖而先捲動。
- `receipt.json`：整輪狀態與主要檔案 hash。PASS 表示預設檢查與記錄完整，不代表通過所有瀏覽器或網路效能驗證。

## 可寫與不能寫的結論

可以寫實際版本與條件下的請求／載入數及操作結果；可以用已讀官方規格解釋 lazy 是提示、瀏覽器可在圖片進視窗前載入、停用 JS 的邊界。近視窗提前載入不算錯誤；End 的動作可能經過中間視窗，不能把它說成瞬間只看最後一張。

不能聲稱固定延遲像素門檻、照片流量節省率、頁速倍數、LCP／SEO 提升、所有瀏覽器相同，或真實手機已測。首屏 eager 只是本實驗保留可見主圖的控制條件，沒有比較首圖設 lazy 對 LCP 的效應。全數捲完仍會下載全部圖片，不能只用初始數字暗示整篇永遠省下相同比例資料。

頁面層級只允許本機 origin；這不是整個 OS 或 Edge 背景 telemetry 的網路稽核。未使用帳號、使用者瀏覽資料、正式站或付費 API。

## 公開套件的收據綁定

這份套件在 2026-11-10 去除個人本機路徑。`runs/2026-11-10T12-52-37-220Z/environment.json`、`receipt.json` 明標 `PUBLICATION_DERIVED_NOT_NEW_EXPERIMENT`；同目錄 `original/` 保留無個資的原收據。原始結果、請求紀錄、素材與截圖未改。`verify-and-summarize.cjs` 本身未改，重跑只核對既有檔案並產生衍生簡報，不啟動瀏覽器。

在套件根目錄核對：

```powershell
node ./experiment/verify-and-summarize.cjs ./experiment/runs/2026-11-10T12-52-37-220Z
```

此指令會更新 `verification.json` 的核對時間與 `RESULTS-BRIEF.md`，不是重新實驗；如要保持公開發行套件的檔案雜湊，請在副本執行。重跑會使發行收據中的這兩檔 hash 不再相同，須另存新核對結果，不可冒用本次發行 hash。
