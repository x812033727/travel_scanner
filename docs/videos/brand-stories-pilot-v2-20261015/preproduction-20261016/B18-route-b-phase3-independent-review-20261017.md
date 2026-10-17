# B18 Route B Phase 3 獨立離線審查：HOLD

審查對象是隔離目錄 `B18-route-b-worker-compatible-candidate-20261017/` 的 `sha256.json`，檔案 SHA-256 為 `14A2CA7370FCBD817C8D2FCE636721780FA4217AF2168A5DF0E0957BE076ECF5`。獨立審查者只讀取候選及來源；本報告不修改該候選、現用 B18、正式主機或付費媒體。

## 可重跑的離線結果

從儲存庫根目錄執行：

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-route-b-worker-compatible-candidate-20261017/build.mjs --check
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-route-b-worker-compatible-candidate-20261017/verify-worker.mjs
```

獨立重跑得 `PASS_OFFLINE_PHASE3_HOLD` 與 `OFFLINE_WORKER_SHAPE_ONLY_HOLD`。來源及輸出雜湊吻合；95 景含 94 個 `shot`、1 個 terminal `outro`；三個不同開場 setup 在模擬 worker line ID roundtrip 後保留跨章 payoff。資料格式、靜態可愛插畫門檻與以每分鐘 300 字估算的 shot errors 均為零。65 個不同 claim ID 的精確口播錨點都完整落在所標單一景，source index 小於 6、fact index 小於 10；**65/65 仍為 `UNCHECKED`**。

25 段口播相對前一版只有 T06 開頭改動；新句可聽見「發明協會的沿革」。發明協會原頁記錄後期依盤色／裝飾分價、郊區大店與家庭用餐；隔離章稿的 `t18` 在 `turn-s088` 保持 `source:2/fact:null/UNCHECKED`。法院判決 P8 L476–495 支持 1967 年獲授權公司在仙台開直營店及東京連鎖；P10 L574–578 僅支持特定實用新案於 1972 年屆滿。日本機械學會把堺東店 1985 年製、2021 年仍使用的輸送機，與另存的早期板片分開描述。

來源：[發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)、[法院判決 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)、[日本機械學會機械遺產 112](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)。

## 需修正的 P2

1. `engine-s059` 畫客人接桶和硬幣，口播卻說三百日圓壽司桶「放上輸送帶」；畫面缺少上帶動作。
2. `turn-s068c` 與 `turn-s065` 畫成 1960 年代獨立店主／新店，會把 1967 年獲授權公司的直營及連鎖擴張誤示為未授權獨立開店。須改畫授權展店的場景，或把其他業者畫面移至較晚段落。
3. `now-s093`、`now-s095b`、`now-s098` 把 1985 年仍在店內使用的機器畫成檔案室／儲藏室零件，且與另外保存的早期板片放在一起；第六章原本刻意區分的兩件實物因此被混淆。
4. `idea-s038` 畫兒子在空白筆記本寫回憶，來源只支持他的回想與材料費說法，未支持寫筆記，畫面也未對應材料費。
5. 第二個 loop 的 setup 是「盤子能跟上人潮嗎」，payoff 卻指定 `engine-s061` 的「壽司仍得由人先備好」。送餐的直接答案在相鄰的三百日圓套組／放上輸送帶景，需改 payoff line ID。
6. shot lint 的 `plate` 42/94、`japanese` 40/94、`sushi` 38/94 只是詞頻警告，單獨不足以判 P2；實際畫面設計的 turn 章連續辦公桌／資料夾／店面模型，now 章八景有多個博物館／儲藏室。需改為與各句相符的事件畫面，並以三鏡樣片驗證節奏。
7. `B18.md` 非口播資訊過期：仍稱第三候選，長度沿用 2,667 字及約 9:19，T06 製作註仍說來源只在註／字卡。現稿 25 段口播依漢字、阿拉伯數字及 `〇` 計為 **2,669**；`estimateTimeline(..., 300)` 為 634.1 秒（10:34，包含逐景預設停頓／間隔，未另加 5 秒片頭及 21 秒片尾）。這些都不是實際 TTS；`now-outro` 80 字也待實際旁白與片尾可讀性驗證。

## HOLD 邊界

新版 T06、95 景及企劃 row 尚未通過獨立全文與畫面審稿；65 筆未經正式 verifier。正式 worker writer、listener、narrative、TTS、MiniMax 成像與觀影尚未做；正式章稿未先寫入並讀回 `t18 fact:null`；worker 的 B18 script reference 還指向舊全文。因此本候選**不可匯入、付費製作或稱為可看片**。離線 shape／anchor 審查未發現新的結構性 P1，但上述 P2 與正式關卡均須完成後重新審查。
