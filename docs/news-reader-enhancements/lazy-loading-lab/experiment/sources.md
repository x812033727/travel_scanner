# 實驗來源及觀察邊界

checked_on：2026-11-10。下列兩頁已透過網頁工具實讀相關段落，再用固定 UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 取得 HTTP 200 原始 HTML，保存於 source-evidence。抓來源是閱讀程序，與只連本機的實驗頁面分開。

| 來源 | 讀到的依據 | 本輪實測與限制 |
|---|---|---|
| [MDN: HTMLImageElement.loading](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/loading) | loading 向瀏覽器提示如何處理視窗外圖片，包含 eager／lazy | 可據此稱 native lazy 是提示，不保證剛進視窗才下載。官方說明不能取代本輪 request log |
| [WHATWG HTML: Lazy loading attributes](https://html.spec.whatwg.org/multipage/urls-and-fetching.html#lazy-loading-attributes) | scripting disabled 時 will lazy load 回 false；lazy load scroll margin 由實作定義，可考慮裝置、捲動、網路與使用者偏好 | 本輪只測 Edge 的 JS 開／關與兩個 CSS viewport，沒測不同網速／瀏覽器，也不估計精確門檻 |

補充已讀來源：[Chrome 團隊 browser-level image lazy loading](https://web.dev/articles/browser-level-image-lazy-loading) 與 [Microsoft Edge Network 教學](https://learn.microsoft.com/en-us/microsoft-edge/devtools/network/)。前者支持不要一律延遲首屏主要圖片、先給尺寸；後者提供 Network 檢查操作。本文沒有把教學中歷史門檻數字移植為本機結果，也沒有宣稱已人工執行 DevTools 教學流程。

原始 HTML 收據：`source-evidence/receipts.json`，分別約 161KB／81KB。原始檔用於查核，不是要在文章全文重製來源。結果簡報須將「實測觀察」與「官方規格解釋」分開標示。

## 2026-11-10 公開版本註

上方 `source-evidence/` 指原私有證據位置，不是此公開套件內的路徑。官方 HTML 與抽出全文沒有複製進此套件；可公開的 URL／取得狀態／原 hash 已列於根目錄 `sources.json`。實驗的自有 HTML／SVG fixture 不受此排除影響。
