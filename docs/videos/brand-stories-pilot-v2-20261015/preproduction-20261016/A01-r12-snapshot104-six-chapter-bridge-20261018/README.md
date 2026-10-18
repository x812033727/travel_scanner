# A01 r12 → 六章離線橋接候選：正式製作 HOLD

這份資料只把 [r12 離線編輯稿](../A01-editorial-candidate-20261018-r12/README.md)拆成 `hook`、`origin`、`idea`、`engine`、`turn`、`now` 六份候選章檔，並對 [104 鏈舊快照差異](../A01-r11-snapshot104-diff-20261018/README.md)逐 ID 對照。r12 全文獨立複審對精確 manifest `17cc760b8573f97d189db7c476d57c61eddd4050f79e54a0460eee5c15b7a9d3` 判離線稿 P0／P1 為零，但明說正式製作仍 HOLD。此包不把那個離線結論當成正式 verifier、listener、敘事 panel 或 `story/reviews/script-review.json`。

## 內容與對照基準

- `candidate/chapters/*.json` 有 65 鏡、77 句、78 筆主張和 11 個已收回的故事鉤子。鏡頭與口播取 r12 原位元組內容；所有候選主張明確設為 `UNCHECKED`，不繼承 104 鏈的 `PLAN`／`CONFIRMED` 或 r12 的 `PENDING` 作正式判定。跨章鉤子在設問章留未收回紀錄，在回答章留完整 setup／payoff；hook 縮圖鏡位仍是 `hook-01`。
- `mapping.json` 把 104 鏈與 r12 的每個 scene、line、claim ID 及所在章、鏡位和順序對上；候選文字與場景用 SHA-256，舊快照文字只留下雜湊、ID 和公開來源 URL，不複製舊主機原稿。全片退役、保留、新增 ID 另列清單。`manifest.json` 綁 r12 稿、其獨立複審、104 差異報告、104 快照清單、本檢查器與每份輸出。
- `candidate/series.json` 是**來源索引提案**：保留 r12 企劃原本 23 筆來源及所有 `must_verify` 索引，只在尾端加入 Plath 2024 校友刊第 17 頁來源與 r12 新的 Travelpro 樓梯比較頁；已引用來源的查核日期對齊 r12 公開來源表。六章主張的 `source` 整數都指這份 25 筆提案。新增的 `archive` 類別只是校友刊掃描件的暫定分類，正式來源審查仍要判定。
- `source-plan-assessment.json` 精確列出原企劃缺少的 **2** 筆、原企劃有而 r12 未引用的 **7** 筆、5 筆查核日期和 17 筆來源標題／出版者欄差異，以及 78 筆主張的 URL／來源索引。因此目前 worker 若直接按企劃來源合稿，會公開 25 筆來源，而 r12 經審離線稿只有 18 筆；影片說明與來源索引**不相同**，不能直接安裝。原有 23 筆來源也可能服務 `must_verify` 或保留研究資料；此包不替站主刪除。
- `reset-assessment.json` 列出六章全數不同、A01 舊保存目標 9–11 分鐘、舊 `auto.json`／系列仍 10 分鐘、r12 正文目標 7–8 分鐘，以及必須重新跑的正式查核、盲聽和敘事關卡。即使先不論來源和片長，現行 `composeStory` 也會省略 r12 三個無主張鏡的明示 `claims: []`，並依章序重排 11 個鉤子；內容集合可重建，`video.json` 位元組**不能直接重現**。這些差異要在正式採用設計中處理，不能沿用 r12 離線稿的雜湊。7–8 分鐘僅是 r12 的文字目標；434.0／468.4 秒是 300／275 CPM 代理估算，並非實際 TTS 或剪完片長。
- **主張 ID 採用阻擋：** `turn-09` 的 `t7b` 是 r12 離線稿留下的非純數字 ID；`tools/video/automation/story.mjs` 的 `numberClaims` 只保留章節字首加數字的 ID。正式逐章 verifier 清理並保存結果時，`t7b` 會被重編號，實際新 ID 取決於當次保存的章稿。此包的 `mapping.json`、`claims`、章稿及相關雜湊都只是**驗證前候選**；必須等正式 verifier 保存精確六章後，依實際 ID 重建 scene／line／claim／來源對照、合稿雜湊與審稿收據，不能直接移植本包的 `t7b` 綁定。
- `current-capture-assessment.json` 額外對 2026-10-18 取得的完整 254 檔唯讀擷取做**逐檔雜湊**比較：相對舊 `snapshot-104`，唯一不同的是共用 `docs/videos/lexicon.json`；A01 的六章、合稿、企劃、`auto.json` 與其餘擷取檔位元組相同。新的全檔清單 SHA-256 是 `7807ee9daf03bd747d6de45ffa9903469fa8309f1611944de879df8293966c9e`。提供者回報擷取 tar SHA-256 `13fedb2bcdb44bd2dd1bf484ea5557c2d217a0ddf71e6c1b57e33b2ba46912ed`；本檢查器核資料夾清單，**未**重新核 tar。共用發音表新增其他詞，正式 TTS 前須以當時主機版本重新釘選，不能沿用舊表的驗收。

## 純唯讀重算

在儲存庫根目錄使用**本機絕對路徑**；快照和驗證收據保留在本機，不加入 Git：

```powershell
$a01Snapshot = '<absolute local immutable snapshot-104 directory>'
$a01Verified = '<absolute local verified-review104.json>'
$a01Current = '<absolute local full current capture directory>'
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-r12-snapshot104-six-chapter-bridge-20261018/check.mjs --check --snapshot $a01Snapshot --verified $a01Verified --current $a01Current
```

`check.mjs` **沒有寫入模式**。它先核 r12 manifest／獨立複審／所有 r12 輸出雜湊，驗 104 快照 254 檔清單、104 鏈 tip、兩份讀回收據與六章原檔雜湊，再驗目前完整擷取的 254 檔清單與唯一變動檔，重建橋接包並逐檔比位元組；任何差異退出 2 並維持 HOLD。它不連正式機、後台、模型或媒體供應商。**檔案相同只能證明擷取之間的位元組關係，不能代替當下主機出處、STOP／lease／工作與預算核對。**

下一步須另取得**新鮮正式機唯讀**六章、完整 audit/journal、worker／release／STOP／lease／付費工作與 US$25 帳本，和此舊 104 鏈重新對照。再由獨立審查者判斷新的企劃來源重併、六章修訂、A01 專屬片長及舊持久狀態如何安全處置；正式章稿的事實查核、listener、整片 narrative panel 均須對採用後的**精確位元組**重跑。後面還有實際 TTS、插畫聯絡表、成片與站主看片。本候選不建立審稿收據、不清 STOP／舊事件、不修改主機、不購買圖片或配音、不匯入 A01／B18／後五集，也不上傳 YouTube。
