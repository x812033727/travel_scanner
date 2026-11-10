# 預先固定實驗規格 v1

日期：2026-11-10。目的：觀察 native `<img loading>` 的請求／載入行為，而非量測網際網路速度、LCP、SEO 或收入。此規格在第一輪開啟實驗頁前寫入，runner 會記錄本檔 SHA-256。

- 使用現有 Microsoft Edge，由 Playwright 啟動全新 headless 瀏覽器，禁止使用登入 profile。保存實際版本；不宣稱代表 Safari、Firefox、真實手機或所有 Edge 安裝。
- 20 張本機產生的 SVG 圖片，各 1200×675；固定 `width`、`height`、alt，沒有外部圖片／字型／分析碼。圖像只是可辨識的自有測試標記，不代表新聞照片。
- 兩份固定 HTML：全部 eager；第一張 eager、其餘 19 張 lazy。兩份只差標題識別及 loading 屬性，素材、位置與尺寸相同。第 2 張稍離首屏，第 3 張之前保留 6000px 空白，最後一張作捲動目標。
- 條件：eager＋JS 啟用、lazy＋JS 啟用、lazy＋JS 停用。頁內有一行 sentinel script，啟用時將 body 標記改成 enabled；停用時維持 not-run。DevTools／Playwright 只讀 DOM 與操作捲動，不啟用頁內 JavaScript。
- 桌機 viewport 1440×900，窄視窗 390×844；兩者 DPR 1，不用 mobile 裝置模擬。每條件 3 次獨立 context，共 18 次；輪替執行 eager／lazy／no-JS 以明示執行順序。
- HTTP 僅綁 127.0.0.1 的隨機 port；所有圖片 Cache-Control: no-store；每次新 context、CDP cache disabled、service workers blocked，無 network throttle。Playwright 阻擋並記錄非該 origin 的頁面請求；未稽核瀏覽器／OS 背景 telemetry。
- 每次開頁等 DOMContentLoaded 後 3 秒，在未捲動時保存請求／載入狀態與所有圖片幾何。以鍵盤 End 到底，等 1 秒再記錄。以 Ctrl+Home 回頂部，每次 wheel 700px、等 80ms，逐段至底（最多 200 步）；最後等 1 秒再記錄。
- 主要觀察：初始已請求／loaded 數；第 3 張初始是否在視窗外且未請求；eager 是否已載入視窗外圖片；最後一張捲到底後是否載入；完整逐段捲動後是否 20 張均 loaded；JS 停用時 lazy 是否失去延遲效果。`loaded` 定義為 complete 且 naturalWidth>0，不能只看 complete。
- 三次各記原始 request log／server log／DOM snapshot，第一輪各條件拍初始、到底、完整遍歷後 viewport PNG。禁止 fullPage screenshot 在初始量測前觸發額外捲動。
- 真實觀察若與預期不同，原紀錄照留，不為迎合結論改 fixture 重跑。執行錯誤保留 failed receipt；若需修 runner，另開 run 目錄並記原因。
- 不能從沒有初始請求推論圖片永不下載；不能把近視窗預載判為 lazy 失效；不能聲稱固定像素門檻；不從 SVG 大小推論照片流量或壓縮率。只有這部電腦、這個版本、這組情境的行為可寫成實測結果。

查閱依據（2026-11-10 實讀）：

1. [MDN loading](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/loading)：loading 是給瀏覽器的提示。
2. [WHATWG HTML lazy loading](https://html.spec.whatwg.org/multipage/urls-and-fetching.html#lazy-loading-attributes)：scripting disabled 時 will-lazy-load 回 false；scroll margin 由實作定義，可能受網路與裝置影響。此輪讀到 Living Standard 頁首 Last Updated 9 November 2026。
3. [Chrome 團隊說明](https://web.dev/articles/browser-level-image-lazy-loading)：不要把首屏主要圖片一律 lazy；width／height 有助穩定排版。

執行前結果：尚未測量，不填數字。正式收據會另存於新的 `runs/` 子目錄。
