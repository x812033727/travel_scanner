# 實驗結果簡報（非文章稿）

執行時間：2026-11-10T12:52:37.223Z 至 2026-11-10T12:55:23.939Z（UTC）。Edge 157.0.4341.42，Windows kernel 10.0.26300／arm64，Playwright 1.64.1，headless。兩種 CSS viewport、DPR 1、每次新 context、關 cache、本機 HTTP，18 次均完成；沒有測實體手機或其他瀏覽器。

## 實測結果

| CSS viewport | 條件 | 重複次數 | 未捲動 3 秒 loaded | 按 End 後 loaded | 逐段捲完 loaded |
|---|---|---:|---:|---:|---:|
| 1440×900 | eager-js | 3 | 20/20 | 20/20 | 20/20 |
| 1440×900 | lazy-js | 3 | 2/20 | 17–18/20 | 20/20 |
| 1440×900 | lazy-nojs | 3 | 20/20 | 20/20 | 20/20 |
| 390×844 | eager-js | 3 | 20/20 | 20/20 | 20/20 |
| 390×844 | lazy-js | 3 | 2/20 | 17–18/20 | 20/20 |
| 390×844 | lazy-nojs | 3 | 20/20 | 20/20 | 20/20 |

- eager 視窗外圖片初始就已請求並載入；lazy＋JS 只載入第 1、2 張，遠處第 3 張尚未請求。
- 第 2 張雖在視窗外，lazy 仍已載入：桌機 top=1411.875px，高度 900px；窄視窗 top=1165.078125px，高度 844px。此為幾何觀察，不是精確預載門檻測量。
- 第 3 張桌機 top=8012px，窄視窗 top=7484.328125px；lazy＋JS 初始未載入，eager 與 lazy-nojs 初始已載入。
- 按 End 後最後一張全部成功載入；End 可能經過中間視窗，不能解讀成瞬間跳躍時只會載入最後幾張。逐段捲完整頁後，每個條件都載入全部 20 張。
- JavaScript 停用時頁內 sentinel 未執行，圖片初始全部載入。DOM 觀察由瀏覽器自動化介面讀取，不表示頁內 JavaScript 被啟用。

初始數字同時有 server 請求與 DOM loaded 狀態作證；不能從本組 2/20 推成照片流量省 90% 或頁速提升。素材是小型 SVG，本機連線與正式站不同。

## 官方規格解釋，與觀察分開

[MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/loading) 將 loading 描述為瀏覽器提示。[WHATWG HTML](https://html.spec.whatwg.org/multipage/urls-and-fetching.html#lazy-loading-attributes) 規定 scripting disabled 時不採 lazy，且預載 margin 由實作決定，可考慮裝置、網路與偏好。兩者均於 2026-11-10 實讀並存 HTTP 200／SHA 收據；文件符合本輪觀察，但未代替實測。

## 收據與後續作者須保留的限制

- 執行 receipt：ca402a83accabe19b73d89f41f799bebaf685dedb64e7d3e17a984b778dc41a9
- 結果 SHA：60e340a2e4a2e2100dc9de8a40ec33017dc529cf99112bd5b7f0fb17c638aca9
- 原始 server requests SHA：ba704282ea0bbc47e8109ce434e7963f0cdc8c4707c0de5bff59a95c6c25d7e0
- 事後交叉核對：165 個檢查全部通過，包括素材／執行檔／規格 hash、18 次的 browser/server 請求一致、幾何一致、截圖存在及 loaded 計數。這是資料一致性檢查，不是新一輪瀏覽器實驗。
- 18 張 viewport 截圖；0 pageerror；0 非本機頁面請求，0 被阻擋外部請求。未稽核 OS／瀏覽器背景 telemetry。
- 未測 LCP、SEO、真實網速、照片、Safari／Firefox、JS library lazy loader 或使用者主站；不得稱全平台效能驗收或真人受試測試。
- 可銜接既有 lazy-loading-images 教學，但公開 URL／現行內容仍須發文前再讀。
- 實驗完成、證據可供獨立覆核；文章尚未撰寫、匯入或發布。
