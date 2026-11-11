# 實測稿獨立作者覆核：PASS

2026-11-10，覆核者 `/root/layout_review`；作者 `/root/article_layout`。待修事實／用語：0。未修改作者稿件。

角色邊界：覆核者是原實驗執行者，這次檢查另一位作者是否忠實使用結果，並另行讀取官方來源；不是宣稱第二人重新執行了 18 次實驗。這是內容預覽稿查核通過，不等於內容包、素材、版面、正式匯入或發布驗收。

## 固定稿件

| 檔案 | SHA-256 |
|---|---|
| article.md | `99faeb1f74c8de21d0e00e7e03c30a7fb115cfa619cb14e335b08dc1a879736b` |
| draft.json | `c1124b81363b1de0d8792dac57577c854e0163e785fbb1f5893f16bfbda7acfe` |

以另寫的唯讀渲染程式從 draft.json 重建 Markdown，與 article.md 位元組內容完全一致，SHA 相同；不是只信作者聲明。

## 實驗事實核對

- 獨立重新計算 results.json 的六組表格，每組正好 3 次，六列 initial／End／逐段完成數字與稿件完全一致。
- receipt、results.json、CSV、server/browser logs、environment、verification、預先規格共 8 份檔案，逐一對照 sources.json 的 bytes／SHA，全部相符。receipt 為 `ca402a83accabe19b73d89f41f799bebaf685dedb64e7d3e17a984b778dc41a9`。
- 環境、版本、兩個 CSS viewport、DPR 1、無 mobile emulation、20 張 1200×675 SVG、首張 eager／其他 19 張 lazy、cache 與 service-worker 設定、等待與捲動步驟均符合 runner／environment。
- 2/20 初始載入與第 2 張仍在視窗外的敘述正確；第 3 張未請求、停用 JS 初始 20/20、最後一張 End 後載入、完整遍歷後 20/20 均有原始資料支持。
- 18 次瀏覽器情境與 165 項事後一致性核對分開；18 張截圖不冒充視窗外請求證據。

## 覆核者今天另讀的來源

以固定公開 UA 重新取得三份官方頁及站內延伸閱讀，均 HTTP 200；原始 HTML、抽出正文與取得時間／SHA 存在 `review-evidence-1/`，不沿用作者收據作為自己已讀的證明。

- [MDN loading](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/loading)：支持「瀏覽器提示」，不支持固定下載距離。
- [WHATWG HTML](https://html.spec.whatwg.org/multipage/urls-and-fetching.html#lazy-loading-attributes)：scripting disabled 時不採 lazy，與防止由圖片請求推測捲動位置有關；margin 由實作決定，考慮裝置、捲動、網路與偏好。
- [web.dev 官方說明](https://web.dev/articles/browser-level-image-lazy-loading)：首屏／可能 LCP 圖片不宜 lazy，尺寸用於預留空間；稿件有標明這是文件建議，並未測 LCP。
- [站內原教學](https://mokaair.com/zh-TW/life/lazy-loading-images)：本次實際回 200，標題與涉及首屏、尺寸、WordPress 分工的描述相符；沒有把它提到的外掛相容性或 SEO 說法轉成這次實驗結論。

## 用語與限制

標題有具體問題與測量對象，沒有承諾省流量、速度或 SEO。稿件清楚保留單機／單 Edge／headless／SVG／本機連線邊界，窄視窗不叫手機實測；End 的 17–18 不推論為瞬間跳躍策略。兩圖 HTML 範例明示未另跑、圖片 URL 是替換用示例，不宣稱可重現原 20 張計數。沒有虛構公開實驗下載或產品實測。

精確修正清單：無。

## v2：讀者優先改稿覆核 PASS（現行稿）

2026-11-10，保留上方 v1 歷史紀錄；本節及 `review-evidence-1/v2-check.json` 對應現行版本。新增待修事實或讀者用語：0。這次沒有重跑瀏覽器、沒有修改作者稿件、沒有重抓相同官方頁；沿用本覆核者當日實讀的來源，重新比對原始實驗檔與完整 v2 文字。

| 檔案 | 現行 SHA-256 |
|---|---|
| article.md | `c5d1921ab2e1a94f131967bab73348484d3e2dfd38593a10dc1ba1a09aa5ce64` |
| draft.json | `dbc15e22ce69249465d3d7719b312646dd3e855bac129a4cc8702395ee2a3810` |
| sources.json | `d18bb841a71613650f9497448b33c63cbe2dbe7519b6fdb66e92c3788495ec03` |
| AUTHOR-NOTES.md | `932e656c9e1c1b371666d53882b2a2b0af91182e9d5a94cf832be364574cb37d` |

- 開頭已移除「文件當天重新查讀」等編輯流程語；文末來源日期保留，讀者仍可判斷查讀時效。
- 165 項收據一致性檢查與 18 張截圖保存的敘述已移入作者註；正文保留有解釋價值的實驗設計（2 種視窗 × 3 個條件 × 3 次，共 18 次）。
- 正文首次出現已補上 lazy「延後載入」、eager「正常載入」及 JavaScript「網頁腳本」；沒有把 eager 說成下載優先權提高。
- 方法先交代單機 Edge、相同 20 張圖、兩個視窗與腳本條件；OS kernel／架構／工具細版本移到作者註，Edge 版本與 headless 邊界保留文末，結果與方法較容易讀到。
- 再次從原始 results.json 計算六組（每組三次）的最小／最大值，六列表格完全相符；8 份凍結證據逐一 bytes／SHA 檢查相符。
- 再以獨立唯讀 renderer 重建 Markdown，與現行 article.md 位元組完全一致；sources.json 所列兩份稿件雜湊同步正確。

查核方式限制：目前可讀目錄僅保留 v1 雜湊與查核紀錄，未提供 v1 完整位元組快照，因此本次是「整篇 v2 重讀＋對原始證據重新核對」，不宣稱已完成 v1／v2 的逐位元 exact diff。這不影響上述現行稿的事實與讀者用語判定。

## 2026-11-10 公開衍生套件重新綁定

上方 v1／v2 hash 是原私有成稿與查核的歷史紀錄，沒有改寫。`review-evidence-1/` 為原私有來源快照目錄，不隨公開套件提供；公開 `review-evidence/v2-check.original.json` 保留原 v2 收據，`review-evidence/v2-check.json` 明標公開衍生綁定，記錄現行來源索引、作者註與證據 hash。文章／draft 仍與上方 v2 hash 相同。

原 verifier 完全未修改，對公開衍生 runner → environment → receipt 與原始結果重新執行，165 項一致性核對通過。這是既有資料的對帳，不是新的 18 次瀏覽器實驗；原 environment／receipt／verification 在 run 的 `original/` 中原樣保留。精確原／新 hash、變更範圍與個資檢查見 `PUBLICATION-REBIND.md`。
