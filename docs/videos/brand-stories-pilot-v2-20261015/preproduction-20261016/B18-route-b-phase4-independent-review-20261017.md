# B18 Route B Phase 4 獨立離線覆核：設計 P1=0／P2=0，整體 HOLD

本報告只覆核隔離目錄 `B18-route-b-phase4-candidate-20261017/` 的已凍結稿、分鏡 prompt、來源對位與現行 worker 資料形狀；**不構成正式企劃、全文、事實或製片審核**。受審 `sha256.json` 的 SHA-256 為 `EFDF3994152DB18892D70C35F6AE10BA3F1D4A9076078922A8A988EE0BBD7422`，內列 input/output 雜湊均與檔案相符。任何候選 byte 改變即須重新審查。

## 獨立重跑

從儲存庫根目錄執行：

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-route-b-phase4-candidate-20261017/build.mjs --check
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-route-b-phase4-candidate-20261017/verify-worker.mjs
```

結果分別為 `PASS_OFFLINE_PHASE4_HOLD scenes=95 shots=94 claims=65 loops=3 long=6` 與 `OFFLINE_WORKER_SHAPE_ONLY_HOLD`。模擬 `readChapterAnswer`／`composeStory` 後保留三個不同的開場 setup 與跨章 payoff、95 景（94 個 `shot`、末景 `now-outro`）、`t18=turn-s088/source:2/fact:null/UNCHECKED`。schema、靜態可愛插畫門檻與估時計算的 shot errors 均為零。65 個不同 claim ID 對 Phase 2 綁定的精確錨點全部位於所標單一景，六個來源和十個 Row10b fact 的索引有效；**65/65 仍未正式查核**。

第三版原稿的 25 段口播相對此候選只改第 22 段 T06 開頭，加入可聽的發明協會歸屬。依漢字、阿拉伯數字及 `〇` 計為 2,669。`B18.md` 的隔離候選狀態、T06 製作註和兩種離線估時已更新。

## Phase 3 六類 P2 的覆核

1. `engine-s059` 已畫廚房工將壽司桶放上行進中的輸送帶，對齊口播。
2. `turn-s068b/s068c` 保留 1967 年獲授權公司在仙台直營及東京相關連鎖的邊界；`turn-s065` 的其他經營者移至較晚的店面，不再暗示 1967 年未授權獨立展店。
3. `now-s093` 只畫兩份分開的編輯示意圖，`now-s095b` 只畫另外保存的早期板片，`now-s098` 將板片和仍在店內運行的後來機器置於兩處，不把 1985 年機器搬進檔案室。
4. `idea-s038` 改為匿名業者付工坊材料費的示意，對應家屬回想，不再虛構兒子寫筆記。
5. 萬博 loop 的 payoff 改為 `engine-s059`「放上輸送帶」，接續 `engine-s058` 的三百日圓套組；三個開場問題都有可聽回收。
6. turn／now 章加入連鎖店面、1972 年後不同企業的街景、不同送餐路線與兩地實物畫面，原桌面／檔案室密集問題在 prompt 層面解開。`plate` 41/94、`sushi` 41/94、`japanese` 38/94 仍有主題詞頻警告；逐鏡場所和事件已有變化，詞頻本身不構成新 P2。成像後仍須看連續三鏡樣片。

獨立審查在本次**靜態稿、分鏡與來源對位**未發現新的 P1 或 P2。

## 整體 HOLD 與片長

T06 新口播、95 景與 Row10b 仍須正式獨立來源、敘事及視畫審查；65 筆 claim 須在正式 worker 逐章 verifier。正式主機須先保存並讀回 `t18 fact:null`，且目前 B18 的 frozen script reference 仍指舊全文。尚無真實 MiniMax 成像、連續三鏡小樣、TTS 或成片觀影，因此**不可匯入、啟動付費製作或稱為可看片**。

`estimateTimeline(..., 300)` 為 634.1 秒（約 10:34，未加 5 秒片頭及 21 秒片尾）；加後約 11:00，靠近 11 分鐘上限。它不是實際旁白長度。實際 9–11 分鐘及 80 字 `now-outro` 的聲畫節奏，必須由 TTS／成片驗證；若超界，按正式調整與重審流程處理，不以慢播、補白或重複旁白湊時。

來源：[發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)、[法院判決 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)、[日本機械學會機械遺產 112](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)。
