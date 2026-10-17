# B18 第三版全文：本機編輯底本採用收據

2026-10-17。**只採用本機完整逐字稿及其獨立文字審稿作為編輯底本。** 來源為[說書節奏第三版候選](../B18-spoken-source-cadence-candidate-20261017/B18.md)及[該版獨立全文審稿](../B18-spoken-source-cadence-candidate-20261017/review-candidate.md)。獨立審稿綁定逐字稿 SHA-256 `7b2865668d8cdd21a87cd813b015ebc0088f3728712181063768d9323200e8c1`，結論只限離線全文文字 PASS，P1 0、P2 0。企劃 row 的 canonical story SHA-256 是 `d0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648`；採用前使用既有 `storyHash`／`reviewProblems` 讀回 active row，row review 問題為空。

採用前先執行候選 `check.mjs --check`，exit 0，六章、25 段口播、25 條來源製作註與三組開場伏筆／回收均符合候選機械檢查。該檢查把舊 active 稿的 SHA 作為採用前前提；**採用後直接重跑會因預期中的 active 稿更換而失敗**，不可把它的歷史狀態欄位當作採用後關卡結果。

| 檔案 | SHA-256 | 採用處理與讀回 |
| --- | --- | --- |
| 舊 `scripts/B18.md` | `5326bd6633ad69931fe542badd6cddd2378324ff0bcc4b0f05652941642dc724` | 採用前逐位元組備份為本目錄 [`scripts-B18.md`](scripts-B18.md)，備份讀回相同 |
| 舊 `scripts/reviews/B18.md` | `1583b36311fde688a49f70aa546bb1c30b53ab294afeb1119bb576c73a479cdb` | 採用前逐位元組備份為本目錄 [`reviews-B18.md`](reviews-B18.md)，備份讀回相同 |
| 候選 `B18.md` → 新 [`scripts/B18.md`](../../scripts/B18.md) | `7b2865668d8cdd21a87cd813b015ebc0088f3728712181063768d9323200e8c1` | 逐位元組複製；active 讀回與獨立審稿綁定的稿件完全相同 |
| 獨立 `review-candidate.md` | `603f0a5340b197cc6cbe527991e63bb1629c4f1245e780fdb3981109dea871d4` | 原件不變；審稿內容複製至 active |
| 新 [`scripts/reviews/B18.md`](../../scripts/reviews/B18.md) | `3d50bc64bc3228fe6fe05e79bc032aca15885b2b57fd73e382a1dbabaeb7b109` | 只把搬移後失效的「本目錄 `B18.md`」連結改成指向 `../B18.md` 的「現用 `B18.md`」；受審稿 SHA、判讀與關卡界線未改 |
| 採用時 active `episodes/B18.json` | `c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681` | 僅讀取；對應上述 canonical story SHA，企劃審稿 `verdict: pass` |

候選逐字稿的狀態行、候選 README 與 `verification.json` 記錄的是**獨立全文審稿產生前**的時間點，因此其中「未通過審稿」及 `formal_new_fullscript_review_complete: false` 不是現在的全文文字結論；後來的獨立審稿收據以相同稿件 SHA 給出文字 PASS。本次採用不會使候選稿與正式 worker 六章逐字一致，也不會把企劃審稿延伸到旁白或 65 筆逐景主張。

逐句對齊有已知差異：本稿 H02 的第三問是「盤子怎麼從後場送到客席」，85 景 hook 仍預告權利到期後「其他店會怎麼用這條送餐路」，並用萬博會場觀眾反應作第二問；本稿 T01 引法院對 **1967 年仙台／東京展店**的記載，85 景 turn 目前未有該段。正式章稿須處理這些出入、來源路由及新句子的逐景審查，不能直接用本稿替換 worker 場景。

**未完成：** 正式 worker 章稿與此編輯底本的逐句對齊、65 筆場景 claim 的 verifier、逐章 listener／narrative、TTS 實測時長和發音、MiniMax 插圖、可關閉繁中 CC、聲畫 QA、成片及站主看片。沒有主機寫入、影片匯入、付費呼叫、上傳或發布；這份收據不授權上述階段。
