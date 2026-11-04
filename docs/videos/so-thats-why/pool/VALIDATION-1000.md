# 首批素材池驗證

驗證日期：2026-11-01。使用 Node **v24.19.0**，本機候選資料與研究文件。未執行正式站匯入、媒體生成、排程或上架。

## 資料與研究

- 最後 [資料與索引收據](reviews/final-validation.json)：1,224 原始紀錄、1,192 核心、1,046 可選、1,000 入選、32 別名、0 未處理高相似警示；313 歷史紀錄全部可回查。879 個入選核心來自本輪，121 個為歷史題。
- 入選 2,212 個來源關係都有 origin、小節定位和對應閱讀紀錄。合併保留兩邊來源；L151 暫緩且不能入選。
- 來源研究共 226 個本輪 URL；歷史來源另列，沒有把 3,195 全庫 URL 冒稱本輪已讀。
- 作者之外逐題編輯審閱：自然 282、物理 295、生命科技 324、太空工程 10。獨立外站覆核為 **39 個批次來源頁的風險抽查**，另有補充背景頁／研究摘要，不是所有題目的全文事實查核。
- [自然組覆核](reviews/life-reviews-nature.json)、[物理與太空組覆核](reviews/nature-reviews-physics.json)、[生命科技與工具覆核](reviews/physics-reviews-life.json) 保留讀取範圍與原版本雜湊。
- 已修 N266 近地軌道限定、P237 濃度術語、P298 彈性形變措辭、R009 無線電科學路徑、L259 重複時間規則，並在吞噬相關題加上不可概括 clathrin 的提醒。舊審閱雜湊不覆寫，新批次雜湊見最後收據。

## 影片編輯

[12 組企劃審閱](reviews/theme-editorial.json) 檢查了全部題名、主線、引用、章節新資訊、時間及刪除條件；不是劇本盲讀、實際試讀或觀眾測試。

G01 原本的糖題名不能涵蓋後半段，已統一為混合液判別；G10/G12 將主矛盾移到開場，刪短成冰／造浪背景，正文預算降為 8 分鐘、範圍 8–9 分鐘。獨立讀回的 followup_resolution 已解除三項問題。全部時間仍為估計，刪重述後不足 8 分鐘應退出長片。

## 程式與索引

```powershell
node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/so-thats-why/cli.mjs check
node tools/video/long-form/cli.mjs check
node tools/tasks.mjs check
```

素材池與既有 selector 的定向 12 項測試通過；加上 repository hygiene、JSON key parser、docs-videos 測試入口，總共 26 項通過（0 失敗／略過／取消）；涵蓋精確與人工合併、來源保留、歷史退題不可復活、同機制熱門詞漏檢回歸、答案相同但題名不同的召回、來源解析、匯入交易中斷回復、重複匯入、修訂保留、過期索引拒絕、候選限制及 HTML 資料跳脫。

既有 selector 檢查與 473 個長片的來源／時長收據通過，任務格式檢查通過（2,287 檔；其餘既有 stale／scope 警告保留）。[獨立程式覆核](reviews/final-code-review.json) 記錄來源小節顯示修正及當時產物；其 README 待補註記已由本次 README 與連結驗證解決。

最後實際索引第一次匯入成功，第二次同快照 **UNCHANGED／0 writes**；「地下水」查回 9 筆，原題 N098 找回 L097，L151 仍未入選。快照和批次雜湊均在最後收據。沒有把記憶體測試當成實際索引匯入。

完整 tools／docs-videos 本機套件未完成，沒有宣稱整套 PASS；本次 26 項檢查與 PR CI 的當期結果分開報告。

## 瀏覽器與檔案

[Playwright 實際瀏覽收據](reviews/browser-qa.json) 綁定最後 index.html 雜湊：

- 首頁報 1,000 筆；初始 50 張卡，下一頁增至 100。
- 查原 ID N098 只出現合併後 L097；展開後可見原題及兩邊來源小節。
- G01 主題篩選數量符合定義；L259 的修正題名可見。
- 390×844 手機畫面沒有水平溢出，1440×1000 桌面畫面人工看過。
- 沒有瀏覽器 JavaScript 錯誤；四個首頁文件入口均存在。

截圖留在忽略版控的 `.cache/`，不是影片畫面或媒體製作成果。Markdown 本機連結及 whitespace 在提交前另檢；外部舊來源的當期可達性未全量掃描。

## 已知界線與接續

相似檢索和人工閱讀不能保證沒有漏掉語意重複；121 筆歷史入選題需刷新來源；新題推導的生活例證、定量結果和畫面權利仍待逐主張查核。索引在此批規模已驗證，10,000／100,000 的效能和語意召回率沒有測量值。

後續擴庫記在 `2026-11-01-so-thats-why-expand-the-reviewed`；沒有啟動背景擴庫。原來如此的正式產線規則同步仍由既有獨立任務承接，本資料池不修改主機工人。
