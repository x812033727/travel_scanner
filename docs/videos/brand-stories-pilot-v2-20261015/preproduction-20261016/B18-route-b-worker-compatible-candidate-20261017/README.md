# B18 Route B Phase 3：shot-only 工人形狀候選（HOLD）

**本目錄是離線隔離候選，不是現用 B18、正式 worker 章稿、獨立審稿收據或製片授權。** 來源是 Phase 2 凍結 92 景候選、經獨立來源與敘事審查的第三版全文，以及 Row10b 10 項事實設計。現用 `scripts/B18.md` 仍是另一個凍結參考版本；本候選不改它。

第三版全文只在 T06 換一句來源歸屬：「發明協會的沿革還記下另一種變化：後來有店不再每盤同價……」。`B18.md` 保存完整候選，`build.mjs` 對照前一版逐段斷言：25 段裡除 T06 以外全部逐字相同。這句仍只講「有店」，沒有把盤色多價說成所有店家的做法。**因為口播變了，前一版的獨立全文 PASS 不再適用；須重新找獨立來源與敘事審稿。**

`design.json` 給舊 19 張 `title` 卡各一個新事件畫面，全部改為無字、無標誌的 MiniMax `image-01` 靜態插畫提示；沒有要求圖片模型畫來源或數字。新增四個分鏡槽：鉤子萬博一景、1967 年展店一景、1980／1986 分開後的兩個送餐路線景。`now-outro` 收下原 N03 的答案尾句、留言問題與訂閱邀請，三句口播原順序不變。這樣候選是 95 景、94 插畫與 1 張正式 `outro`；它不是已畫好的圖片。

三個開場問題各用不同 line ID 設置 loop，並在 idea、engine、turn 的答句景各寫同一 setup 與其本章 payoff。65 個原 claim ID 維持 `UNCHECKED`；`build.mjs` 要求每一筆精確口播錨點完整落在同一景，不靠跨景拼接。T06 `t18` 先設 `source:2/fact:null`；仍需在正式 verifier 前把這筆寫入真章稿並讀回，不能讓 `checkedRows()` 的舊值回退。

## 唯讀重跑

從儲存庫根目錄執行：

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-route-b-worker-compatible-candidate-20261017/build.mjs --check
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-route-b-worker-compatible-candidate-20261017/verify-worker.mjs
```

第一步比對來源 SHA、設計、章稿、逐段 coverage 與 manifest。第二步只在記憶體內把離線 line IDs 換成模擬的 worker-issued IDs，通過 `readChapterAnswer`、`composeStory`、資料格式與可愛插畫靜態門檻，再讀回三個 loop 和 `t18`。**模擬不等於正式 writer、verifier、listener、narrative panel 或主機版本。**

## 明確保留的 HOLD

- 新 T06 句子、95 景節拍、全部畫面與 65 claim 需要獨立審稿。J-Net21／發明協會與法院判決的限定範圍須保留；特別是 1967 被授權公司仙台直營、東京連鎖及 1972 年僅特定實用新案期滿。
- 逐景畫面只有 prompt，沒有 MiniMax 成像、Jev／音訊、聯絡表或觀影。每一景約 5–8 秒是設計意圖，不能由字數證明。
- 第三版原稿 2,667 漢字／阿拉伯數字以每分鐘 300 字粗估約 8 分 53 秒；T06 改字後須重算，**9–11 分鐘需正式 TTS 的旁白時間軸**。片頭片尾不能替正文補時間。turn 章仍比 10 分鐘 worker 的 463 字預算密；若正式 TTS、畫面節奏或獨立聽讀不過，退回而不灌水。
- Row10b 仍非匯入審核完成的企劃；真實 worker 的 B18 凍結 script reference 也還指向舊全文。要採此版本需新全文與企劃審稿、刻意更新 reference SHA 並完成 CI／部署、實際六章逐項查核及站主成本決策。B18 未授權付費製作。

沒有正式主機寫入、付款、合併、部署、YouTube 上傳或發布。
